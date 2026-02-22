"""
hexstrike_worker.py — Asynchronous Job Queue for HexStrike

Provides:
  - Background job processing
  - Job scheduling and retry logic
  - Status tracking and callbacks
  - Integration with Obsidian cache
"""

import asyncio
import json
import logging
import threading
import time
import uuid
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
from pathlib import Path
from queue import PriorityQueue, Queue
from typing import Any, Callable, Dict, Optional

from mcp.hexstrike_wrapper import HexStrikeClient, JobStatus, JobResult

logger = logging.getLogger(__name__)


class TaskPriority(Enum):
    """Task priority levels"""
    LOW = 3
    NORMAL = 2
    HIGH = 1
    URGENT = 0


@dataclass
class Task:
    """Represents a HexStrike task"""
    task_id: str
    tool: str
    params: Dict[str, Any]
    priority: TaskPriority
    created_at: datetime
    scheduled_for: Optional[datetime] = None
    callback: Optional[Callable] = None
    cache_result: bool = True
    retry_count: int = 0
    max_retries: int = 3

    def __lt__(self, other):
        """Compare tasks by priority for queue ordering"""
        if self.priority.value != other.priority.value:
            return self.priority.value < other.priority.value
        return self.created_at < other.created_at


class HexStrikeWorker:
    """
    Manages background HexStrike job execution.
    
    Usage:
        worker = HexStrikeWorker()
        worker.start()
        
        task_id = worker.submit_task(
            tool="nmap",
            params={"target": "192.168.1.0/24"},
            priority=TaskPriority.HIGH,
            callback=my_callback
        )
        
        status = worker.get_task_status(task_id)
        worker.stop()
    """

    def __init__(
        self,
        hexstrike_url: str = "http://localhost:8888",
        max_workers: int = 3,
        vault_path: Optional[Path] = None,
    ):
        self.hexstrike_url = hexstrike_url
        self.max_workers = max_workers
        self.vault_path = vault_path
        
        self._queue: PriorityQueue = PriorityQueue()
        self._tasks: Dict[str, Task] = {}
        self._results: Dict[str, JobResult] = {}
        self._running = False
        self._worker_threads = []
        self._task_lock = threading.Lock()
        
        self.client = HexStrikeClient(hexstrike_url)

    def start(self):
        """Start worker threads"""
        if self._running:
            logger.warning("Worker already running")
            return
        
        self._running = True
        
        for i in range(self.max_workers):
            thread = threading.Thread(
                target=self._work_loop,
                name=f"HexStrikeWorker-{i}",
                daemon=True,
            )
            thread.start()
            self._worker_threads.append(thread)
        
        logger.info(f"Started {self.max_workers} worker threads")

    def stop(self, timeout: int = 10):
        """Stop worker threads gracefully"""
        self._running = False
        
        for thread in self._worker_threads:
            thread.join(timeout=timeout)
        
        self._worker_threads.clear()
        logger.info("Worker threads stopped")

    def submit_task(
        self,
        tool: str,
        params: Dict[str, Any],
        priority: TaskPriority = TaskPriority.NORMAL,
        scheduled_for: Optional[datetime] = None,
        callback: Optional[Callable] = None,
        cache_result: bool = True,
    ) -> str:
        """
        Submit a task to the queue.
        
        Returns:
            Task ID
        """
        task_id = str(uuid.uuid4())
        task = Task(
            task_id=task_id,
            tool=tool,
            params=params,
            priority=priority,
            created_at=datetime.now(),
            scheduled_for=scheduled_for,
            callback=callback,
            cache_result=cache_result,
        )
        
        with self._task_lock:
            self._tasks[task_id] = task
        
        # Add to queue with priority
        self._queue.put((priority.value, task_id, task))
        
        logger.info(f"Task {task_id} submitted: {tool} (priority={priority.name})")
        return task_id

    def get_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get task status"""
        with self._task_lock:
            task = self._tasks.get(task_id)
            
            if not task:
                return None
            
            result = self._results.get(task_id)
            
            return {
                "task_id": task_id,
                "tool": task.tool,
                "status": result.status.value if result else "pending",
                "created_at": task.created_at.isoformat(),
                "result": result.to_dict() if result else None,
            }

    def get_all_tasks(self) -> Dict[str, Dict[str, Any]]:
        """Get all tasks and their statuses"""
        with self._task_lock:
            return {
                task_id: self.get_task_status(task_id)
                for task_id in self._tasks.keys()
            }

    def cancel_task(self, task_id: str) -> bool:
        """Cancel a pending task"""
        with self._task_lock:
            if task_id not in self._tasks:
                return False
            
            task = self._tasks[task_id]
            
            # Try to cancel on server
            if task.get("hexstrike_job_id"):
                self.client.cancel_job(task["hexstrike_job_id"])
            
            logger.info(f"Task {task_id} cancelled")
            return True

    def _work_loop(self):
        """Main worker loop"""
        while self._running:
            try:
                # Get next task with timeout
                _, task_id, task = self._queue.get(timeout=1)
                
                if not self._running:
                    break
                
                # Check if task is scheduled for later
                if task.scheduled_for and datetime.now() < task.scheduled_for:
                    # Re-queue task
                    self._queue.put((task.priority.value, task_id, task))
                    continue
                
                logger.debug(f"Processing task {task_id}: {task.tool}")
                self._execute_task(task)
                
            except:
                # Queue timeout, loop again
                continue

    def _execute_task(self, task: Task):
        """Execute a single task"""
        try:
            # Run HexStrike job
            start_time = datetime.now()
            result_data = self.client.run_scan(
                task.tool,
                task.params,
                wait=True,
                timeout=300,  # 5 min timeout
            )
            elapsed = (datetime.now() - start_time).total_seconds()
            
            if not result_data:
                raise Exception("HexStrike returned no result")
            
            # Create result object
            result = JobResult(
                job_id=result_data.get("job_id", "unknown"),
                status=JobStatus(result_data.get("status", "failed")),
                started_at=start_time,
                completed_at=datetime.now(),
                result=result_data.get("result"),
                error=result_data.get("error"),
                execution_time=elapsed,
            )
            
            with self._task_lock:
                self._results[task.task_id] = result
            
            logger.info(
                f"Task {task.task_id} completed: {task.tool} "
                f"({elapsed:.2f}s, status={result.status.value})"
            )
            
            # Cache result to Obsidian if enabled
            if task.cache_result and self.vault_path:
                self._cache_to_vault(task, result)
            
            # Run callback if provided
            if task.callback:
                try:
                    task.callback(task.task_id, result)
                except Exception as e:
                    logger.error(f"Callback failed for task {task.task_id}: {e}")
            
        except Exception as e:
            logger.error(f"Task {task.task_id} failed: {e}")
            
            # Retry logic
            with self._task_lock:
                task.retry_count += 1
                if task.retry_count < task.max_retries:
                    logger.info(f"Retrying task {task.task_id} ({task.retry_count}/{task.max_retries})")
                    task.scheduled_for = datetime.fromtimestamp(
                        datetime.now().timestamp() + (5 * task.retry_count)
                    )
                    self._queue.put((task.priority.value, task.task_id, task))
                else:
                    # Mark as failed
                    result = JobResult(
                        job_id="unknown",
                        status=JobStatus.FAILED,
                        started_at=datetime.now(),
                        completed_at=datetime.now(),
                        result=None,
                        error=str(e),
                        execution_time=None,
                    )
                    self._results[task.task_id] = result

    def _cache_to_vault(self, task: Task, result: JobResult):
        """Cache result to Obsidian Vault"""
        if not self.vault_path:
            return
        
        try:
            from vault_sync.vault_api import ObsidianVaultClient
            
            vault_client = ObsidianVaultClient.from_config()
            
            # Prepare note content
            content = f"""# HexStrike Job Result
## {task.tool}

**Task ID**: {task.task_id}
**Job ID**: {result.job_id}
**Status**: {result.status.value}
**Execution Time**: {result.execution_time:.2f}s if result.execution_time else "N/A"

## Parameters
```json
{json.dumps(task.params, indent=2)}
```

## Result
```json
{json.dumps(result.result, indent=2) if result.result else "No result"}
```

## Error
{result.error if result.error else "None"}

---
*Generated: {result.completed_at.isoformat()}*
"""
            
            # Create note in Vault
            note_path = f"HexStrike/Jobs/{datetime.now().strftime('%Y-%m-%d')}/{task.task_id}.md"
            vault_client.create_note(note_path, content)
            
            logger.info(f"Task {task.task_id} cached to {note_path}")
            
        except Exception as e:
            logger.error(f"Failed to cache result to vault: {e}")

    def wait_all(self, timeout: int = 300) -> Dict[str, JobResult]:
        """Wait for all tasks to complete"""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            with self._task_lock:
                pending = [
                    task_id for task_id, task in self._tasks.items()
                    if task_id not in self._results
                ]
                
                if not pending:
                    return self._results
            
            time.sleep(1)
        
        logger.warning(f"Timeout waiting for tasks (timeout={timeout}s)")
        return self._results


# Singleton instance
_worker_instance: Optional[HexStrikeWorker] = None


def get_worker(
    hexstrike_url: str = "http://localhost:8888",
    vault_path: Optional[Path] = None,
) -> HexStrikeWorker:
    """Get or create worker singleton"""
    global _worker_instance
    
    if _worker_instance is None:
        _worker_instance = HexStrikeWorker(hexstrike_url, vault_path=vault_path)
        _worker_instance.start()
    
    return _worker_instance


def shutdown_worker():
    """Shutdown worker singleton"""
    global _worker_instance
    
    if _worker_instance:
        _worker_instance.stop()
        _worker_instance = None
