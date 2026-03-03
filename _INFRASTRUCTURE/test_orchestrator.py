#!/usr/bin/env python3

"""
═══════════════════════════════════════════════════════════════════════════════
HexStrike Ascended33 - TEST ORCHESTRATOR
Orchestrate, validate, and troubleshoot all Docker containers and APIs
═══════════════════════════════════════════════════════════════════════════════
"""

import os
import sys
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
    SUCCESS = "✓"
    FAILURE = "✗"
    WARNING = "⚠"
    INFO = "ℹ"

@dataclass
class TestResult:
    name: str
    status: Status
    message: str
    duration: float = 0.0
    details: Optional[str] = None

class Colors:
    RESET = "\033[0m"
    SUCCESS = "\033[32m"    # Green
    ERROR = "\033[31m"      # Red
    WARNING = "\033[33m"    # Yellow
    INFO = "\033[36m"       # Cyan
    HEADER = "\033[1;35m"   # Magenta Bold

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
    width = 40
    print(f"\n{Colors.HEADER}╔{'═' * (width - 2)}╗{Colors.RESET}")
    print(f"{Colors.HEADER}║ {text:<{width - 4}} ║{Colors.RESET}")
    print(f"{Colors.HEADER}╚{'═' * (width - 2)}╝{Colors.RESET}\n")

def print_result(result: TestResult):
    """Print single test result"""
    status_color = {
        Status.SUCCESS: Colors.SUCCESS,
        Status.FAILURE: Colors.ERROR,
        Status.WARNING: Colors.WARNING,
        Status.INFO: Colors.INFO,
    }[result.status]
    
    print(f"{status_color}{result.status.value} {result.name}:{Colors.RESET} {result.message}")
    if result.details:
        print(f"  → {result.details}")

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
    """Execute command inside Docker container (Windows-safe: uses list args, no shell quoting)"""
    import shlex
    args = ["docker", "exec", container, "sh", "-c", cmd]
    try:
        result = subprocess.run(args, capture_output=True, text=True, timeout=timeout)
        return result.returncode == 0, result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        return False, "Command timeout"
    except Exception as e:
        return False, str(e)

def get_container_status(container: str) -> str:
    """Get container running status"""
    success, output = run_command(f"docker inspect -f '{{{{.State.Status}}}}' {container}")
    return output.strip() if success else "unknown"

def test_endpoint(url: str, timeout: int = 5) -> bool:
    """Test HTTP endpoint"""
    try:
        response = requests.get(url, timeout=timeout)
        return response.status_code < 500
    except:
        return False

# ═════════════════════════════════════════════════════════════════════════════
# TEST SUITES
# ═════════════════════════════════════════════════════════════════════════════

class TestSuite:
    def __init__(self):
        self.results: List[TestResult] = []
        self.start_time = time.time()

    def add_result(self, result: TestResult):
        """Add test result"""
        self.results.append(result)
        print_result(result)

    def test_infrastructure(self) -> List[TestResult]:
        """Test Docker infrastructure"""
        print_header("PHASE 1 - Vérification Infrastructure Docker")
        
        containers = ["th3-hexstrike", "th3-tor", "th3-kali", "th3-hackergpt", "th3-streamlit"]
        
        for container in containers:
            start = time.time()
            status = get_container_status(container)
            duration = time.time() - start
            
            # docker inspect wraps value in single quotes on some platforms: 'running'
            clean_status = status.strip("'\"")
            if clean_status == "running":
                result = TestResult(
                    f"Container {container}",
                    Status.SUCCESS,
                    "Is RUNNING",
                    duration
                )
            elif clean_status == "exited":
                result = TestResult(
                    f"Container {container}",
                    Status.FAILURE,
                    "Is EXITED",
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
        
        # List all containers with ports
        success, output = run_command("docker ps --format 'table {{.Names}}\\t{{.Status}}\\t{{.Ports}}'")
        if success:
            result = TestResult(
                "Docker containers list",
                Status.INFO,
                "Retrieved",
                details=output
            )
            self.add_result(result)

    def test_internal_connections(self) -> List[TestResult]:
        """Test internal Docker connections"""
        print_header("PHASE 2 - Tests de Connexion Interne")
        
        # Test HexStrike health
        start = time.time()
        success, output = docker_exec("th3-hexstrike", "curl -s --noproxy localhost http://localhost:8888/health/ping")
        duration = time.time() - start
        
        result = TestResult(
            "HexStrike Health Check",
            Status.SUCCESS if success else Status.FAILURE,
            "Health endpoint responding" if success else "No response",
            duration,
            output[:100] if output else None
        )
        self.add_result(result)
        
        # Test Redis connectivity
        start = time.time()
        success, output = docker_exec("th3-hexstrike", "redis-cli -h redis ping")
        duration = time.time() - start
        
        result = TestResult(
            "Redis Connectivity",
            Status.SUCCESS if success else Status.WARNING,
            "Redis accessible" if success else "Redis not reachable (optional)",
            duration
        )
        self.add_result(result)
        
        # Test network
        start = time.time()
        success, output = run_command("docker network inspect th3-thirty3_th3-network")
        duration = time.time() - start
        
        result = TestResult(
            "Docker Network (ascended33-network)",
            Status.SUCCESS if success else Status.WARNING,
            "Network accessible" if success else "Network not found",
            duration
        )
        self.add_result(result)

    def test_volumes(self) -> List[TestResult]:
        """Test volume mounts"""
        print_header("PHASE 3 - Tests Applicatifs")
        
        # Check Vault volume
        start = time.time()
        vault_exists = VAULT_PATH.exists()
        duration = time.time() - start
        
        result = TestResult(
            "Vault Volume",
            Status.SUCCESS if vault_exists else Status.FAILURE,
            f"Mounted at {VAULT_PATH}" if vault_exists else f"Not found at {VAULT_PATH}",
            duration
        )
        self.add_result(result)
        
        # Test write permission
        if vault_exists:
            start = time.time()
            test_file = VAULT_PATH / f"test_{int(time.time())}.txt"
            try:
                test_file.write_text("Test write")
                test_file.unlink()
                result = TestResult(
                    "Vault Write Permission",
                    Status.SUCCESS,
                    "Can write to Vault",
                    time.time() - start
                )
            except Exception as e:
                result = TestResult(
                    "Vault Write Permission",
                    Status.FAILURE,
                    f"Cannot write: {str(e)}",
                    time.time() - start
                )
            self.add_result(result)
        
        # Check REPORT structure
        report_path = VAULT_PATH / "REPORT" / "Classified"
        if report_path.exists():
            file_count = len(list(report_path.glob("**/*")))
            result = TestResult(
                "REPORT/Classified Directory",
                Status.SUCCESS,
                f"Exists with {file_count} items",
                0
            )
        else:
            result = TestResult(
                "REPORT/Classified Directory",
                Status.WARNING,
                "Directory not yet created",
                0
            )
        self.add_result(result)

    def test_apis(self) -> List[TestResult]:
        """Test external APIs"""
        print_header("PHASE 4 - Tests API Externes")
        
        endpoints = [
            ("http://localhost:8888/health/ping", "HexStrike AI (8888) — ping"),
            ("http://localhost:8888/health", "HexStrike AI (8888) — full health"),
            ("http://localhost:8501/_stcore/health", "Streamlit Dashboard (8501)"),
            ("http://localhost:5000/health", "GPU Trainer API (5000)"),
            ("http://127.0.0.1:27123", "Obsidian REST API (27123)"),
            ("http://localhost:39300/model_context_protocol/2025-03-26/mcp", "Pieces MCP (39300)"),
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

    def test_tor(self) -> List[TestResult]:
        """Test Tor connectivity"""
        print_header("PHASE 5 - Tests Tor & Anonymité")
        
        # Test Tor SOCKS5 — depuis hexstrike (valide que le proxy est accessible depuis le bon conteneur)
        start = time.time()
        success, output = docker_exec(
            "th3-hexstrike",
            "curl -s --socks5 th3-tor:9050 https://check.torproject.org/api/ip"
        )
        duration = time.time() - start
        
        is_tor = "istor" in output.lower() and "true" in output.lower()
        result = TestResult(
            "Tor SOCKS5 (9050)",
            Status.SUCCESS if is_tor else Status.FAILURE,
            "Tor operational" if is_tor else "Tor not working",
            duration,
            output[:100] if output else None
        )
        self.add_result(result)

    def test_logging(self) -> List[TestResult]:
        """Test logging and persistence"""
        print_header("PHASE 6 - Tests Persistance & Logging")
        
        # HexStrike logs
        start = time.time()
        success, logs = run_command("docker logs th3-hexstrike 2>&1 | tail -20", timeout=5)
        duration = time.time() - start
        
        result = TestResult(
            "HexStrike Logs",
            Status.SUCCESS if success else Status.WARNING,
            "Logs retrieved" if success else "Cannot retrieve logs",
            duration,
            logs[:100] if logs else None
        )
        self.add_result(result)
        
        # Docker volumes
        start = time.time()
        success, output = run_command("docker volume ls", timeout=5)
        duration = time.time() - start
        
        result = TestResult(
            "Docker Volumes",
            Status.SUCCESS if success else Status.WARNING,
            "Volumes listed" if success else "Cannot list volumes",
            duration,
            output[:100] if output else None
        )
        self.add_result(result)

    def test_integrations(self) -> List[TestResult]:
        """Test Pieces OS and MCP integrations"""
        print_header("PHASE 7 - Tests Intégration Pieces OS & MCP")
        
        # Pieces OS
        start = time.time()
        success = test_endpoint("http://localhost:39300/health")
        duration = time.time() - start
        
        result = TestResult(
            "Pieces OS (39300)",
            Status.SUCCESS if success else Status.WARNING,
            "Responding" if success else "Not accessible",
            duration
        )
        self.add_result(result)
        
        # Obsidian API
        start = time.time()
        success = test_endpoint("http://127.0.0.1:27123")
        duration = time.time() - start

        result = TestResult(
            "Obsidian API (27123)",
            Status.SUCCESS if success else Status.WARNING,
            "Responding" if success else "Not accessible (Obsidian must be open)",
            duration
        )
        self.add_result(result)

        # HexStrike MCP
        mcp_script = Path("C:/Users/th3th/th3-thirty3/hexstrike-ai/hexstrike_mcp.py")
        if mcp_script.exists():
            result = TestResult(
                "HexStrike MCP Script",
                Status.SUCCESS,
                "Script found",
                0
            )
        else:
            result = TestResult(
                "HexStrike MCP Script",
                Status.WARNING,
                "Script not found",
                0
            )
        self.add_result(result)

    def run_all(self):
        """Run all test suites"""
        self.test_infrastructure()
        self.test_internal_connections()
        self.test_volumes()
        self.test_apis()
        self.test_tor()
        self.test_logging()
        self.test_integrations()

    def summary(self):
        """Print summary"""
        print_header("RÉSUMÉ DES TESTS")
        
        counts = {
            Status.SUCCESS: len([r for r in self.results if r.status == Status.SUCCESS]),
            Status.FAILURE: len([r for r in self.results if r.status == Status.FAILURE]),
            Status.WARNING: len([r for r in self.results if r.status == Status.WARNING]),
        }
        total = sum(counts.values())
        success_rate = (counts[Status.SUCCESS] / total * 100) if total > 0 else 0
        
        print(f"Total Tests: {total}")
        print(f"{Colors.SUCCESS}✓ Succès: {counts[Status.SUCCESS]}{Colors.RESET}")
        print(f"{Colors.ERROR}✗ Échecs: {counts[Status.FAILURE]}{Colors.RESET}")
        print(f"{Colors.WARNING}⚠ Avertissements: {counts[Status.WARNING]}{Colors.RESET}")
        print(f"Taux de réussite: {success_rate:.1f}%")
        
        total_time = time.time() - self.start_time
        print(f"\nTemps total: {total_time:.2f}s")
        print(f"Résultats sauvegardés: {RESULTS_LOG}")
        
        # Save to JSON
        self._save_results(counts, success_rate, total_time)

    def _save_results(self, counts, success_rate, total_time):
        """Save results to JSON file"""
        results_data = {
            "timestamp": datetime.now().isoformat(),
            "total_time_seconds": total_time,
            "summary": {
                "total": len(self.results),
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
        
        print(f"\n{Colors.SUCCESS}✓ Suite de tests terminée !{Colors.RESET}\n")
        
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}Interrupted by user{Colors.RESET}")
        sys.exit(1)
    except Exception as e:
        print(f"{Colors.ERROR}✗ Error: {str(e)}{Colors.RESET}")
        sys.exit(1)

if __name__ == "__main__":
    main()
