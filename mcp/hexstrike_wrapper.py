"""
hexstrike_wrapper.py — Professional HexStrike MCP Client Wrapper

Provides a clean, reusable interface to HexStrike with:
  - Connection pooling and health checks
  - Job tracking and status monitoring
  - Error handling and retries
  - Async task support
  - Result caching
"""

import asyncio
import json
import logging
import time
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Optional, Dict, List

import aiohttp
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)


class JobStatus(Enum):
    """HexStrike job status codes"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    TIMEOUT = "timeout"


@dataclass
class JobResult:
    """Container for HexStrike job results"""
    job_id: str
    status: JobStatus
    started_at: datetime
    completed_at: Optional[datetime]
    result: Optional[Dict[str, Any]]
    error: Optional[str]
    execution_time: Optional[float]

    def to_dict(self) -> dict:
        return {
            "job_id": self.job_id,
            "status": self.status.value,
            "started_at": self.started_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "result": self.result,
            "error": self.error,
            "execution_time": self.execution_time,
        }


class HexStrikeClient:
    """
    Professional client for HexStrike MCP Server.
    
    Usage:
        client = HexStrikeClient("http://localhost:8888")
        
        # Sync operations
        result = client.run_scan("nmap", {"target": "192.168.1.1"})
        
        # Async operations
        job = await client.run_scan_async("nmap", {"target": "192.168.1.1"})
        status = await client.get_job_status(job["job_id"])
    """

    def __init__(
        self,
        base_url: str = "http://localhost:8001",
        timeout: int = 30,
        max_retries: int = 3,
        enable_caching: bool = True,
    ):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries
        self.enable_caching = enable_caching
        self._cache: Dict[str, JobResult] = {}
        self._job_history: List[str] = []
        
        # Setup requests session with retries
        self.session = requests.Session()
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    @property
    def is_reachable(self) -> bool:
        """Check if HexStrike server is reachable"""
        try:
            response = self.session.get(
                f"{self.base_url}/health",
                timeout=5,
            )
            return response.status_code == 200
        except Exception as e:
            logger.error(f"HexStrike health check failed: {e}")
            return False

    @property
    def is_healthy(self) -> bool:
        """Detailed health check"""
        try:
            response = self.session.get(
                f"{self.base_url}/health",
                timeout=5,
            )
            if response.status_code == 200:
                health = response.json()
                return health.get("status") == "healthy"
            return False
        except Exception as e:
            logger.error(f"HexStrike health check failed: {e}")
            return False

    def get_info(self) -> Optional[Dict[str, Any]]:
        """Get HexStrike server info"""
        try:
            response = self.session.get(
                f"{self.base_url}/info",
                timeout=self.timeout,
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to get HexStrike info: {e}")
            return None

    def get_tools(self) -> Optional[List[str]]:
        """List available HexStrike tools"""
        try:
            response = self.session.get(
                f"{self.base_url}/tools",
                timeout=self.timeout,
            )
            response.raise_for_status()
            tools = response.json()
            return tools.get("tools", [])
        except Exception as e:
            logger.error(f"Failed to get tools list: {e}")
            return None

    def run_scan(
        self,
        tool: str,
        params: Dict[str, Any],
        wait: bool = True,
        timeout: Optional[int] = None,
    ) -> Optional[Dict[str, Any]]:
        """
        Run a HexStrike scan tool synchronously.
        
        Args:
            tool: Tool name (e.g., 'nmap', 'masscan', 'nuclei')
            params: Tool parameters
            wait: Wait for completion if True
            timeout: Override timeout
            
        Returns:
            Job result or None on error
        """
        try:
            # Submit job
            response = self.session.post(
                f"{self.base_url}/job/submit",
                json={"tool": tool, "params": params},
                timeout=timeout or self.timeout,
            )
            response.raise_for_status()
            
            job_data = response.json()
            job_id = job_data.get("job_id")
            
            if not job_id:
                logger.error("Server did not return job_id")
                return None
            
            logger.info(f"Job {job_id} submitted for tool '{tool}'")
            
            if not wait:
                return job_data
            
            # Wait for completion
            return self._wait_for_job(job_id, timeout=timeout)
            
        except Exception as e:
            logger.error(f"Failed to run scan '{tool}': {e}")
            return None

    def _wait_for_job(
        self,
        job_id: str,
        timeout: Optional[int] = None,
        poll_interval: int = 2,
    ) -> Optional[Dict[str, Any]]:
        """Wait for job to complete"""
        timeout = timeout or self.timeout
        elapsed = 0
        
        while elapsed < timeout:
            try:
                response = self.session.get(
                    f"{self.base_url}/job/{job_id}",
                    timeout=self.timeout,
                )
                response.raise_for_status()
                
                job_data = response.json()
                status = job_data.get("status")
                
                if status in ["completed", "failed"]:
                    return job_data
                
                logger.debug(f"Job {job_id} status: {status}")
                time.sleep(poll_interval)
                elapsed += poll_interval
                
            except Exception as e:
                logger.error(f"Failed to check job status: {e}")
                return None
        
        logger.error(f"Job {job_id} timed out after {timeout}s")
        return None

    async def run_scan_async(
        self,
        tool: str,
        params: Dict[str, Any],
    ) -> Optional[Dict[str, Any]]:
        """
        Submit a HexStrike scan asynchronously (fire-and-forget).
        
        Returns job info without waiting for completion.
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/job/submit",
                    json={"tool": tool, "params": params},
                    timeout=aiohttp.ClientTimeout(total=self.timeout),
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        job_id = data.get("job_id")
                        if job_id:
                            self._job_history.append(job_id)
                        return data
                    else:
                        logger.error(f"Server returned {response.status}")
                        return None
        except Exception as e:
            logger.error(f"Async scan failed: {e}")
            return None

    async def get_job_status_async(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Get job status asynchronously"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/job/{job_id}",
                    timeout=aiohttp.ClientTimeout(total=self.timeout),
                ) as response:
                    if response.status == 200:
                        return await response.json()
                    return None
        except Exception as e:
            logger.error(f"Failed to get job status: {e}")
            return None

    def get_job_status(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Get job status synchronously"""
        try:
            response = self.session.get(
                f"{self.base_url}/job/{job_id}",
                timeout=self.timeout,
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to get job status: {e}")
            return None

    def get_job_result(self, job_id: str) -> Optional[JobResult]:
        """Get structured job result"""
        try:
            if job_id in self._cache:
                return self._cache[job_id]
            
            response = self.session.get(
                f"{self.base_url}/job/{job_id}",
                timeout=self.timeout,
            )
            response.raise_for_status()
            
            data = response.json()
            status = JobStatus(data.get("status", "failed"))
            
            result = JobResult(
                job_id=job_id,
                status=status,
                started_at=datetime.fromisoformat(data.get("started_at", datetime.now().isoformat())),
                completed_at=datetime.fromisoformat(data["completed_at"]) if data.get("completed_at") else None,
                result=data.get("result"),
                error=data.get("error"),
                execution_time=data.get("execution_time"),
            )
            
            if self.enable_caching:
                self._cache[job_id] = result
            
            return result
        except Exception as e:
            logger.error(f"Failed to get job result: {e}")
            return None

    def cancel_job(self, job_id: str) -> bool:
        """Cancel a running job"""
        try:
            response = self.session.post(
                f"{self.base_url}/job/{job_id}/cancel",
                timeout=self.timeout,
            )
            response.raise_for_status()
            logger.info(f"Job {job_id} cancelled")
            return True
        except Exception as e:
            logger.error(f"Failed to cancel job: {e}")
            return False

    def get_job_history(self, limit: int = 50) -> List[str]:
        """Get recent job IDs"""
        return self._job_history[-limit:]

    def clear_cache(self):
        """Clear cached results"""
        self._cache.clear()
        logger.info("Cache cleared")

    def close(self):
        """Close session"""
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
