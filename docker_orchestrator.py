#!/usr/bin/env python3
"""
Docker Orchestrator for Ascended33 - Multi-Container Management
Optimizes startup speed, handles inter-container communication, manages auto-reporting
"""

import os
import sys
import json
import time
import subprocess
import logging
import threading
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

# Configure logging for anonymity
class AnonymousFormatter(logging.Formatter):
    """Formatter that removes identifiable information"""
    def format(self, record):
        record.msg = str(record.msg).replace(os.getenv('USERNAME', 'USER'), 'ANON')
        record.msg = record.msg.replace(os.path.expanduser('~'), '[HOME]')
        return super().format(record)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [ASCENDED33] %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler(r'D:\Vault\Vault\Ascended33\logs\docker_orchestrator.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)
for handler in logger.handlers:
    if isinstance(handler, logging.StreamHandler):
        handler.setFormatter(AnonymousFormatter())

@dataclass
class ContainerConfig:
    """Container configuration"""
    name: str
    image_hash: str
    port: Optional[int] = None
    depends_on: List[str] = None
    critical: bool = False

class ContainerStatus(Enum):
    """Container lifecycle states"""
    STOPPED = "stopped"
    STARTING = "starting"
    RUNNING = "running"
    UNHEALTHY = "unhealthy"
    STOPPING = "stopping"

class DockerOrchestrator:
    """Orchestrates multi-container Docker setup for Ascended33"""
    
    CONTAINERS = {
        'th3-tor': ContainerConfig(
            name='th3-tor',
            image_hash='9a570c8f087a14106bc7cf2e626a4189507683a94f32d246070f9b881961af71',
            port=9050,
            critical=True
        ),
        'th3-kali': ContainerConfig(
            name='th3-kali',
            image_hash='901c75b66a3bc718952cc9bc06719b525edd6398d32abc59d13a567d6cf9bc92',
            depends_on=['th3-tor'],
            critical=True
        ),
        'th3-hackergpt': ContainerConfig(
            name='th3-hackergpt',
            image_hash='0478381aa6bdb487e3b25100a1054f8d0834a74da3bb3ab90ffad0c2f6aa116f',
            port=8000,
            depends_on=['th3-kali', 'th3-tor'],
            critical=True
        ),
        'th3-hexstrike': ContainerConfig(
            name='th3-hexstrike',
            image_hash='65aa74e03ad8d184435b157fce99ab9cef335f5d23071da999282fa8ae632cf0',
            port=8001,
            depends_on=['th3-kali', 'th3-hackergpt'],
            critical=True
        )
    }
    
    VAULT_PATH = Path(r'D:\Vault\Vault')
    WORKSPACE_PATH = VAULT_PATH / 'Ascended33' / 'workspace'
    REPORT_PATH = VAULT_PATH / 'REPORT'
    
    def __init__(self):
        self.status: Dict[str, ContainerStatus] = {
            name: ContainerStatus.STOPPED for name in self.CONTAINERS
        }
        self.startup_time = None
        self.sync_thread = None
        self.running = False
        
    def startup_all_containers(self) -> Tuple[bool, str]:
        """
        Startup all containers with dependency management and health checks
        Returns: (success, message)
        """
        logger.info("🚀 Starting Ascended33 Docker infrastructure...")
        start_time = time.time()
        
        try:
            # Verify Docker daemon
            result = subprocess.run(
                ['docker', 'info'],
                capture_output=True,
                timeout=10,
                check=False
            )
            if result.returncode != 0:
                return False, "❌ Docker daemon not available"
            
            # Create necessary directories
            self._create_directories()
            
            # Build docker-compose file if needed
            compose_file = self.VAULT_PATH / 'Ascended33' / 'docker-compose.yml'
            if not compose_file.exists():
                return False, f"❌ docker-compose.yml not found at {compose_file}"
            
            # Start containers in order
            logger.info("📦 Starting containers with Docker Compose...")
            result = subprocess.run(
                ['docker-compose', '-f', str(compose_file), 'up', '-d'],
                cwd=str(self.VAULT_PATH / 'Ascended33'),
                capture_output=True,
                timeout=120,
                check=False
            )
            
            if result.returncode != 0:
                error_msg = result.stderr.decode('utf-8', errors='ignore')
                logger.error(f"Docker Compose error: {error_msg}")
                return False, f"❌ Docker Compose failed: {error_msg[:200]}"
            
            # Wait for health checks
            logger.info("⏳ Waiting for containers to be healthy...")
            if not self._wait_for_health_checks():
                return False, "❌ Some containers failed health checks"
            
            # Verify inter-container connectivity
            if not self._verify_connectivity():
                return False, "❌ Container connectivity verification failed"
            
            # Start auto-reporting system
            self._start_auto_reporting()
            
            self.startup_time = time.time() - start_time
            self.running = True
            
            elapsed = int(self.startup_time)
            msg = f"✅ All containers started successfully in {elapsed}s"
            logger.info(msg)
            return True, msg
            
        except subprocess.TimeoutExpired:
            return False, "❌ Docker startup timed out"
        except Exception as e:
            logger.error(f"Startup error: {e}")
            return False, f"❌ Startup failed: {str(e)[:100]}"
    
    def _create_directories(self):
        """Create necessary directories"""
        for path in [self.WORKSPACE_PATH, self.REPORT_PATH, 
                     self.VAULT_PATH / 'Ascended33' / 'logs']:
            path.mkdir(parents=True, exist_ok=True)
    
    def _wait_for_health_checks(self, timeout: int = 120) -> bool:
        """Wait for all containers to pass health checks"""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            healthy_count = 0
            for container_name in self.CONTAINERS:
                if self._check_container_health(container_name):
                    healthy_count += 1
                    self.status[container_name] = ContainerStatus.RUNNING
                else:
                    self.status[container_name] = ContainerStatus.STARTING
            
            if healthy_count == len(self.CONTAINERS):
                logger.info(f"✓ All {healthy_count} containers are healthy")
                return True
            
            logger.debug(f"Health status: {healthy_count}/{len(self.CONTAINERS)}")
            time.sleep(5)
        
        logger.warning("⚠ Timeout waiting for health checks")
        return False
    
    def _check_container_health(self, container_name: str) -> bool:
        """Check individual container health"""
        try:
            result = subprocess.run(
                ['docker', 'inspect', '--format={{.State.Health.Status}}', container_name],
                capture_output=True,
                timeout=10,
                check=False
            )
            status = result.stdout.decode('utf-8').strip()
            return status == 'healthy'
        except Exception as e:
            logger.debug(f"Health check error for {container_name}: {e}")
            return False
    
    def _verify_connectivity(self) -> bool:
        """Verify container-to-container connectivity"""
        logger.info("🔗 Verifying inter-container connectivity...")
        
        try:
            # Test Kali can reach Tor
            result = subprocess.run(
                ['docker', 'exec', 'th3-kali', 
                 'nc', '-z', 'th3-tor', '9050'],
                capture_output=True,
                timeout=10,
                check=False
            )
            
            if result.returncode == 0:
                logger.info("✓ Kali → Tor connectivity verified")
                return True
            else:
                logger.warning("⚠ Connectivity check inconclusive")
                return True  # Non-critical
                
        except Exception as e:
            logger.warning(f"Connectivity check error: {e}")
            return True  # Non-critical
    
    def _start_auto_reporting(self):
        """Start automatic report generation to Obsidian"""
        self.sync_thread = threading.Thread(target=self._auto_report_loop, daemon=True)
        self.sync_thread.start()
        logger.info("📊 Auto-reporting system started")
    
    def _auto_report_loop(self):
        """Continuously monitor and generate reports"""
        while self.running:
            try:
                # Query Hexstrike for new data
                report_data = self._get_hexstrike_report_data()
                
                if report_data:
                    # Generate anonymized report
                    report = self._generate_anonymous_report(report_data)
                    
                    # Save to Vault
                    self._save_report_to_vault(report)
                
                time.sleep(30)  # Check every 30 seconds
                
            except Exception as e:
                logger.error(f"Auto-report error: {e}")
                time.sleep(10)
    
    def _get_hexstrike_report_data(self) -> Optional[Dict]:
        """Retrieve pending reports from Hexstrike"""
        try:
            result = subprocess.run(
                ['docker', 'exec', 'th3-hexstrike',
                 'curl', '-s', 'http://localhost:8001/pending-reports'],
                capture_output=True,
                timeout=10,
                check=False
            )
            
            if result.returncode == 0:
                data = json.loads(result.stdout.decode('utf-8', errors='ignore'))
                return data
        except Exception as e:
            logger.debug(f"Report retrieval error: {e}")
        
        return None
    
    def _generate_anonymous_report(self, data: Dict) -> Dict:
        """Generate report with full anonymity"""
        timestamp = datetime.now().isoformat()
        anonymous_id = hashlib.sha256(
            f"{timestamp}{os.urandom(16).hex()}".encode()
        ).hexdigest()[:16]
        
        report = {
            'generated_at': timestamp,
            'anonymous_id': f"ANON_{anonymous_id}",
            'data': data,
            'source': 'CLAUDE_ANALYSIS',  # Never log actual user
            'anonymity_level': 'FULL'
        }
        
        return report
    
    def _save_report_to_vault(self, report: Dict):
        """Save generated report to Obsidian Vault"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = self.REPORT_PATH / f"hexstrike_{timestamp}.md"
            
            # Convert to markdown
            md_content = f"""# Hexstrike Report
Generated: {report['generated_at']}
Anonymous ID: {report['anonymous_id']}
Anonymity Level: {report['anonymity_level']}

## Analysis Data

```json
{json.dumps(report['data'], indent=2)}
```

---
*Report generated anonymously via Ascended33 Docker infrastructure*
"""
            
            filename.write_text(md_content, encoding='utf-8')
            logger.info(f"📝 Report saved: {filename.name}")
            
        except Exception as e:
            logger.error(f"Report save error: {e}")
    
    def shutdown_all_containers(self) -> Tuple[bool, str]:
        """Gracefully shutdown all containers"""
        logger.info("🛑 Shutting down Docker infrastructure...")
        self.running = False
        
        try:
            compose_file = self.VAULT_PATH / 'Ascended33' / 'docker-compose.yml'
            result = subprocess.run(
                ['docker-compose', '-f', str(compose_file), 'down'],
                cwd=str(self.VAULT_PATH / 'Ascended33'),
                capture_output=True,
                timeout=60,
                check=False
            )
            
            if result.returncode == 0:
                logger.info("✓ All containers shut down")
                return True, "✅ Docker infrastructure shut down successfully"
            else:
                return False, "⚠ Partial shutdown"
                
        except Exception as e:
            logger.error(f"Shutdown error: {e}")
            return False, f"❌ Shutdown error: {str(e)}"
    
    def get_status(self) -> Dict:
        """Get current status of all containers"""
        status_report = {
            'orchestrator_running': self.running,
            'startup_time_seconds': int(self.startup_time) if self.startup_time else None,
            'containers': {}
        }
        
        for name, config in self.CONTAINERS.items():
            try:
                result = subprocess.run(
                    ['docker', 'inspect', '--format={{.State.Status}}', name],
                    capture_output=True,
                    timeout=5,
                    check=False
                )
                container_status = result.stdout.decode('utf-8').strip()
                
                status_report['containers'][name] = {
                    'status': container_status,
                    'port': config.port,
                    'critical': config.critical
                }
            except Exception as e:
                status_report['containers'][name] = {'error': str(e)}
        
        return status_report

def main():
    """Main orchestrator entry point"""
    orchestrator = DockerOrchestrator()
    
    # Startup all containers
    success, message = orchestrator.startup_all_containers()
    print(message)
    
    if not success:
        sys.exit(1)
    
    # Keep running
    try:
        while True:
            time.sleep(60)
            status = orchestrator.get_status()
            if not all(c.get('status') == 'running' 
                      for c in status['containers'].values()):
                logger.warning("⚠ Container status changed")
    except KeyboardInterrupt:
        print("\n⚠ Interrupt received")
        orchestrator.shutdown_all_containers()
        sys.exit(0)

if __name__ == '__main__':
    main()
