#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import io

# Force UTF-8 output on Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

"""
HexStrike Ascended33 - TEST ORCHESTRATOR (Windows Compatible)
Orchestrate, validate, and troubleshoot all Docker containers and APIs
"""

import os
import json
import time
import subprocess
import requests
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

# ═════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═════════════════════════════════════════════════════════════════════════════

class Status(Enum):
    SUCCESS = "OK"
    FAILURE = "FAIL"
    WARNING = "WARN"
    INFO = "INFO"

@dataclass
class TestResult:
    name: str
    status: Status
    message: str
    duration: float = 0.0
    details: Optional[str] = None

class Colors:
    RESET = ""
    SUCCESS = ""    
    ERROR = ""      
    WARNING = ""    
    INFO = ""       
    HEADER = ""

# ═════════════════════════════════════════════════════════════════════════════
# PATHS
# ═════════════════════════════════════════════════════════════════════════════

SCRIPT_DIR = Path(__file__).parent.absolute()
PROJECT_ROOT = SCRIPT_DIR.parent
VAULT_PATH = Path(os.getenv("VAULT_PATH", "D:/Vault/Vault"))
RESULTS_DIR = SCRIPT_DIR / "test-results"
RESULTS_DIR.mkdir(exist_ok=True)
RESULTS_LOG = RESULTS_DIR / f"test-{datetime.now().strftime('%Y-%m-%d_%H%M%S')}.json"

# ═════════════════════════════════════════════════════════════════════════════
# UTILITY FUNCTIONS
# ═════════════════════════════════════════════════════════════════════════════

def print_header(text: str):
    """Print formatted header"""
    width = 50
    print(f"\n{'=' * width}")
    print(f"  {text}")
    print(f"{'=' * width}\n")

def print_result(result: TestResult):
    """Print single test result"""
    status_map = {
        Status.SUCCESS: "[OK]",
        Status.FAILURE: "[FAIL]",
        Status.WARNING: "[WARN]",
        Status.INFO: "[INFO]",
    }
    
    print(f"{status_map[result.status]} {result.name}: {result.message}")
    if result.details:
        print(f"    Details: {result.details}")

def run_command(cmd: str, timeout: int = 10) -> Tuple[bool, str]:
    """Execute shell command and return success status and output"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result.returncode == 0, result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        return False, "Command timeout"
    except Exception as e:
        return False, str(e)

def docker_exec(container: str, cmd: str, timeout: int = 10) -> Tuple[bool, str]:
    """Execute command inside Docker container"""
    full_cmd = f"docker exec {container} sh -c \"{cmd}\""
    return run_command(full_cmd, timeout)

def get_container_status(container: str) -> str:
    """Get container running status"""
    success, output = run_command(f"docker inspect -f \"{{{{.State.Status}}}}\" {container}")
    return output.strip() if success else "unknown"

def test_endpoint(url: str, timeout: int = 5) -> bool:
    """Test HTTP endpoint"""
    try:
        response = requests.get(url, timeout=timeout)
        return response.status_code < 500
    except:
        return False

# ═════════════════════════════════════════════════════════════════════════════
# TEST SUITE
# ═════════════════════════════════════════════════════════════════════════════

class TestSuite:
    def __init__(self):
        self.results: List[TestResult] = []
        self.start_time = time.time()

    def add_result(self, result: TestResult):
        """Add test result"""
        self.results.append(result)
        print_result(result)

    def test_infrastructure(self):
        """Test Docker infrastructure"""
        print_header("PHASE 1 - Docker Infrastructure Verification")
        
        containers = ["th3-hexstrike", "th3-tor", "th3-kali", "th3-hackergpt", "th3-streamlit"]
        
        for container in containers:
            start = time.time()
            status = get_container_status(container)
            duration = time.time() - start
            
            if status == "running":
                result = TestResult(
                    f"Container {container}",
                    Status.SUCCESS,
                    f"Is {status.upper()}",
                    duration
                )
            elif status == "exited":
                result = TestResult(
                    f"Container {container}",
                    Status.FAILURE,
                    f"Is {status.upper()}",
                    duration
                )
            else:
                result = TestResult(
                    f"Container {container}",
                    Status.WARNING,
                    f"Status: {status}",
                    duration
                )
            
            self.add_result(result)

    def test_internal_connections(self):
        """Test internal Docker connections"""
        print_header("PHASE 2 - Internal Connections")
        
        start = time.time()
        success, output = docker_exec("th3-hexstrike", "curl -s http://localhost:8001/health")
        duration = time.time() - start
        
        result = TestResult(
            "HexStrike Health Check",
            Status.SUCCESS if success else Status.FAILURE,
            "Health endpoint responding" if success else "No response",
            duration,
            output[:100] if output else None
        )
        self.add_result(result)

    def test_volumes(self):
        """Test volume mounts"""
        print_header("PHASE 3 - Volume Tests")
        
        start = time.time()
        vault_exists = VAULT_PATH.exists()
        duration = time.time() - start
        
        result = TestResult(
            "Vault Volume",
            Status.SUCCESS if vault_exists else Status.FAILURE,
            f"Mounted at {VAULT_PATH}" if vault_exists else f"Not found",
            duration
        )
        self.add_result(result)

    def test_apis(self):
        """Test external APIs"""
        print_header("PHASE 4 - API Endpoints")
        
        endpoints = [
            ("http://localhost:8001/health", "HexStrike API (8001)"),
            ("http://localhost:8000/health", "HackerGPT API (8000)"),
            ("http://localhost:8501/_stcore/health", "Streamlit (8501)"),
        ]
        
        for url, name in endpoints:
            start = time.time()
            success = test_endpoint(url)
            duration = time.time() - start
            
            result = TestResult(
                name,
                Status.SUCCESS if success else Status.FAILURE,
                "Responding" if success else "No response",
                duration
            )
            self.add_result(result)

    def test_logging(self):
        """Test logging"""
        print_header("PHASE 5 - Logging & Persistence")
        
        start = time.time()
        success, logs = run_command("docker logs th3-hexstrike 2>&1")
        duration = time.time() - start
        
        result = TestResult(
            "HexStrike Logs",
            Status.SUCCESS if success else Status.WARNING,
            "Logs retrieved" if success else "Cannot retrieve logs",
            duration
        )
        self.add_result(result)

    def run_all(self):
        """Run all test suites"""
        self.test_infrastructure()
        self.test_internal_connections()
        self.test_volumes()
        self.test_apis()
        self.test_logging()

    def summary(self):
        """Print summary"""
        print_header("TEST SUMMARY")
        
        counts = {
            Status.SUCCESS: len([r for r in self.results if r.status == Status.SUCCESS]),
            Status.FAILURE: len([r for r in self.results if r.status == Status.FAILURE]),
            Status.WARNING: len([r for r in self.results if r.status == Status.WARNING]),
        }
        total = sum(counts.values())
        success_rate = (counts[Status.SUCCESS] / total * 100) if total > 0 else 0
        
        print(f"Total Tests: {total}")
        print(f"[OK]   Success: {counts[Status.SUCCESS]}")
        print(f"[FAIL] Failures: {counts[Status.FAILURE]}")
        print(f"[WARN] Warnings: {counts[Status.WARNING]}")
        print(f"Success Rate: {success_rate:.1f}%")
        
        total_time = time.time() - self.start_time
        print(f"\nTotal Time: {total_time:.2f}s")
        print(f"Results saved: {RESULTS_LOG}\n")
        
        # Save to JSON
        results_data = {
            "timestamp": datetime.now().isoformat(),
            "total_time_seconds": total_time,
            "summary": {
                "total": total,
                "success": counts[Status.SUCCESS],
                "failure": counts[Status.FAILURE],
                "warning": counts[Status.WARNING],
                "success_rate_percent": success_rate
            },
            "tests": [
                {
                    "name": r.name,
                    "status": r.status.name,
                    "message": r.message,
                    "duration_seconds": r.duration,
                    "details": r.details
                }
                for r in self.results
            ]
        }
        
        with open(RESULTS_LOG, "w") as f:
            json.dump(results_data, f, indent=2)

# ═════════════════════════════════════════════════════════════════════════════
# MAIN
# ═════════════════════════════════════════════════════════════════════════════

def main():
    try:
        suite = TestSuite()
        suite.run_all()
        suite.summary()
        
        print("\n[OK] Test suite completed!\n")
        
    except KeyboardInterrupt:
        print("\n[WARN] Interrupted by user\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n[FAIL] Error: {str(e)}\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
