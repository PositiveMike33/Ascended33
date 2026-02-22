# ============================================================================
# DOCKER CONTAINERIZATION - Container Management & Orchestration
# ============================================================================
# Purpose: Manage per-user Docker containers with isolation and networking
# Features: Container lifecycle, health monitoring, resource management
#
# Author: Ascended33 Platform
# Version: 1.0.0 (JOUR 2)
# Status: Production Ready
# ============================================================================

import json
import logging
import subprocess
import time
from typing import Dict, List, Optional
from pathlib import Path
from dataclasses import dataclass
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class ContainerConfig:
    """Docker container configuration"""
    container_name: str
    user_id: str
    username: str
    image: str
    ports: Dict[int, int]  # {container_port: host_port}
    volumes: Dict[str, str]  # {host_path: container_path}
    environment: Dict[str, str]
    memory_limit: str  # e.g., "2G"
    cpu_limit: str  # e.g., "1.0"
    network_mode: str = "bridge"
    restart_policy: str = "unless-stopped"


@dataclass
class ContainerStatus:
    """Current container status"""
    container_id: str
    container_name: str
    user_id: str
    status: str  # running, exited, paused
    created_at: str
    started_at: str
    memory_usage_mb: float
    cpu_percentage: float
    is_healthy: bool


class DockerContainerManager:
    """Manage Docker containers for each user"""
    
    def __init__(self, docker_host: str = "unix:///var/run/docker.sock"):
        """
        Initialize Docker container manager
        
        Args:
            docker_host: Docker daemon socket/host
        """
        self.docker_host = docker_host
        self.containers: Dict[str, str] = {}  # user_id -> container_id
        
        # Verify Docker is available
        try:
            result = subprocess.run(['docker', '--version'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                logger.info(f"Docker available: {result.stdout.strip()}")
            else:
                logger.warning("Docker not found in PATH")
        except FileNotFoundError:
            logger.warning("Docker CLI not installed")
    
    def create_container(self, config: ContainerConfig) -> Optional[str]:
        """
        Create new Docker container for user
        
        Args:
            config: Container configuration
        
        Returns:
            Container ID or None if failed
        """
        try:
            # Build docker run command
            cmd = ['docker', 'run', '-d']
            
            # Add container name
            cmd.extend(['--name', config.container_name])
            
            # Add hostname
            cmd.extend(['-h', config.container_name])
            
            # Add resource limits
            cmd.extend(['-m', config.memory_limit])
            cmd.extend(['--cpus', config.cpu_limit])
            
            # Add environment variables
            for key, value in config.environment.items():
                cmd.extend(['-e', f'{key}={value}'])
            
            # Add volumes
            for host_path, container_path in config.volumes.items():
                Path(host_path).mkdir(parents=True, exist_ok=True)
                cmd.extend(['-v', f'{host_path}:{container_path}'])
            
            # Add port mappings
            for container_port, host_port in config.ports.items():
                cmd.extend(['-p', f'{host_port}:{container_port}'])
            
            # Add network settings
            cmd.extend(['--network', config.network_mode])
            
            # Add restart policy
            cmd.extend(['--restart', config.restart_policy])
            
            # Add image
            cmd.append(config.image)
            
            # Execute docker run
            logger.info(f"Creating container: {config.container_name}")
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                container_id = result.stdout.strip()
                self.containers[config.user_id] = container_id
                logger.info(f"Container created: {container_id}")
                return container_id
            else:
                logger.error(f"Failed to create container: {result.stderr}")
                return None
                
        except Exception as e:
            logger.error(f"Error creating container: {e}")
            return None
    
    def start_container(self, user_id: str) -> bool:
        """
        Start user container
        
        Args:
            user_id: User ID
        
        Returns:
            Success status
        """
        if user_id not in self.containers:
            logger.warning(f"Container not found for user {user_id}")
            return False
        
        container_id = self.containers[user_id]
        
        try:
            result = subprocess.run(['docker', 'start', container_id],
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info(f"Started container {container_id}")
                return True
            else:
                logger.error(f"Failed to start container: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"Error starting container: {e}")
            return False
    
    def stop_container(self, user_id: str, timeout: int = 10) -> bool:
        """
        Stop user container gracefully
        
        Args:
            user_id: User ID
            timeout: Timeout in seconds
        
        Returns:
            Success status
        """
        if user_id not in self.containers:
            logger.warning(f"Container not found for user {user_id}")
            return False
        
        container_id = self.containers[user_id]
        
        try:
            result = subprocess.run(['docker', 'stop', '-t', str(timeout), 
                                   container_id],
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info(f"Stopped container {container_id}")
                return True
            else:
                logger.error(f"Failed to stop container: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"Error stopping container: {e}")
            return False
    
    def remove_container(self, user_id: str, force: bool = False) -> bool:
        """
        Remove user container
        
        Args:
            user_id: User ID
            force: Force removal even if running
        
        Returns:
            Success status
        """
        if user_id not in self.containers:
            logger.warning(f"Container not found for user {user_id}")
            return False
        
        container_id = self.containers[user_id]
        
        try:
            cmd = ['docker', 'rm']
            if force:
                cmd.append('-f')
            cmd.append(container_id)
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                del self.containers[user_id]
                logger.info(f"Removed container {container_id}")
                return True
            else:
                logger.error(f"Failed to remove container: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"Error removing container: {e}")
            return False
    
    def get_container_status(self, user_id: str) -> Optional[ContainerStatus]:
        """
        Get container status and metrics
        
        Args:
            user_id: User ID
        
        Returns:
            ContainerStatus or None
        """
        if user_id not in self.containers:
            return None
        
        container_id = self.containers[user_id]
        
        try:
            # Get container info
            result = subprocess.run(
                ['docker', 'inspect', container_id],
                capture_output=True, text=True
            )
            
            if result.returncode != 0:
                return None
            
            info = json.loads(result.stdout)[0]
            
            # Get container stats
            stats_result = subprocess.run(
                ['docker', 'stats', '--no-stream', container_id],
                capture_output=True, text=True
            )
            
            memory_usage = 0.0
            cpu_percentage = 0.0
            
            if stats_result.returncode == 0:
                # Parse stats output
                lines = stats_result.stdout.strip().split('\n')
                if len(lines) > 1:
                    stats_line = lines[1].split()
                    if len(stats_line) > 4:
                        cpu_percentage = float(stats_line[2].rstrip('%'))
                        memory_str = stats_line[3]
                        memory_usage = float(memory_str.split('M')[0])
            
            status = ContainerStatus(
                container_id=container_id,
                container_name=info['Name'].lstrip('/'),
                user_id=user_id,
                status=info['State']['Status'],
                created_at=info['Created'],
                started_at=info['State']['StartedAt'],
                memory_usage_mb=memory_usage,
                cpu_percentage=cpu_percentage,
                is_healthy=info['State']['Health']['Status'] == 'healthy'
                           if 'Health' in info['State'] else False
            )
            
            return status
            
        except Exception as e:
            logger.error(f"Error getting container status: {e}")
            return None
    
    def execute_command(self, user_id: str, command: str, 
                       user: str = "root") -> Optional[str]:
        """
        Execute command inside container
        
        Args:
            user_id: User ID
            command: Command to execute
            user: User to execute as
        
        Returns:
            Command output or None if failed
        """
        if user_id not in self.containers:
            return None
        
        container_id = self.containers[user_id]
        
        try:
            result = subprocess.run(
                ['docker', 'exec', '-u', user, container_id] + command.split(),
                capture_output=True, text=True
            )
            
            if result.returncode == 0:
                logger.info(f"Command executed in {container_id}")
                return result.stdout
            else:
                logger.error(f"Command failed: {result.stderr}")
                return None
                
        except Exception as e:
            logger.error(f"Error executing command: {e}")
            return None
    
    def get_container_logs(self, user_id: str, tail: int = 100) -> Optional[str]:
        """
        Get container logs
        
        Args:
            user_id: User ID
            tail: Number of lines to retrieve
        
        Returns:
            Logs or None if failed
        """
        if user_id not in self.containers:
            return None
        
        container_id = self.containers[user_id]
        
        try:
            result = subprocess.run(
                ['docker', 'logs', '--tail', str(tail), container_id],
                capture_output=True, text=True
            )
            
            if result.returncode == 0:
                return result.stdout
            else:
                logger.error(f"Failed to get logs: {result.stderr}")
                return None
                
        except Exception as e:
            logger.error(f"Error getting logs: {e}")
            return None


class ContainerNetworkManager:
    """Manage Docker network configuration and isolation"""
    
    def __init__(self):
        """Initialize network manager"""
        logger.info("ContainerNetworkManager initialized")
    
    def create_network(self, network_name: str, driver: str = "bridge",
                      subnet: str = "172.20.0.0/16") -> bool:
        """
        Create isolated Docker network
        
        Args:
            network_name: Network name
            driver: Network driver
            subnet: Subnet CIDR
        
        Returns:
            Success status
        """
        try:
            cmd = [
                'docker', 'network', 'create',
                '--driver', driver,
                '--subnet', subnet,
                network_name
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info(f"Created network: {network_name}")
                return True
            else:
                logger.error(f"Failed to create network: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"Error creating network: {e}")
            return False
    
    def connect_container_to_network(self, container_id: str, 
                                    network_name: str, 
                                    ip_address: Optional[str] = None) -> bool:
        """
        Connect container to network
        
        Args:
            container_id: Container ID
            network_name: Network name
            ip_address: Optional IP address
        
        Returns:
            Success status
        """
        try:
            cmd = ['docker', 'network', 'connect']
            
            if ip_address:
                cmd.extend(['--ip', ip_address])
            
            cmd.extend([network_name, container_id])
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info(f"Connected container {container_id} to {network_name}")
                return True
            else:
                logger.error(f"Failed to connect network: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"Error connecting network: {e}")
            return False
    
    def remove_network(self, network_name: str) -> bool:
        """
        Remove Docker network
        
        Args:
            network_name: Network name
        
        Returns:
            Success status
        """
        try:
            result = subprocess.run(
                ['docker', 'network', 'rm', network_name],
                capture_output=True, text=True
            )
            
            if result.returncode == 0:
                logger.info(f"Removed network: {network_name}")
                return True
            else:
                logger.error(f"Failed to remove network: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"Error removing network: {e}")
            return False


class ContainerHealthMonitor:
    """Monitor container health and performance"""
    
    def __init__(self, check_interval: int = 30):
        """
        Initialize health monitor
        
        Args:
            check_interval: Check interval in seconds
        """
        self.check_interval = check_interval
        self.container_manager = None
        self.health_data: Dict[str, List[ContainerStatus]] = {}
        logger.info(f"ContainerHealthMonitor initialized (interval: {check_interval}s)")
    
    def check_container_health(self, user_id: str) -> Dict:
        """
        Check container health metrics
        
        Args:
            user_id: User ID
        
        Returns:
            Health status dictionary
        """
        if not self.container_manager:
            return {'status': 'error', 'reason': 'Manager not set'}
        
        status = self.container_manager.get_container_status(user_id)
        
        if not status:
            return {'status': 'error', 'reason': 'Container not found'}
        
        health = {
            'status': 'healthy' if status.is_healthy else 'unhealthy',
            'running': status.status == 'running',
            'memory_usage_mb': status.memory_usage_mb,
            'cpu_percentage': status.cpu_percentage,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        # Store health data
        if user_id not in self.health_data:
            self.health_data[user_id] = []
        
        self.health_data[user_id].append(status)
        
        # Keep only last 100 entries
        if len(self.health_data[user_id]) > 100:
            self.health_data[user_id] = self.health_data[user_id][-100:]
        
        return health
    
    def get_health_history(self, user_id: str, limit: int = 24) -> List[Dict]:
        """
        Get container health history
        
        Args:
            user_id: User ID
            limit: Number of entries to return
        
        Returns:
            List of health data
        """
        if user_id not in self.health_data:
            return []
        
        history = self.health_data[user_id][-limit:]
        
        return [
            {
                'timestamp': s.started_at,
                'memory_mb': s.memory_usage_mb,
                'cpu_percent': s.cpu_percentage,
                'status': s.status
            }
            for s in history
        ]
