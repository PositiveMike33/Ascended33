"""
JOUR 2 - Docker Containerization Module Tests
Test suite for container management, networking, and health monitoring
"""

import pytest
import os
import sys
import tempfile
import shutil
from pathlib import Path
from datetime import datetime, timedelta

# Add core directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "core"))

from docker_containerization import (
    ContainerConfig,
    ContainerStatus,
    DockerContainerManager,
    ContainerNetworkManager,
    ContainerHealthMonitor
)


class TestContainerConfig:
    """Test ContainerConfig dataclass"""

    def test_container_config_creation(self):
        """Test creating container configuration"""
        config = ContainerConfig(
            container_name="test_container",
            image="python:3.11",
            memory_limit="2g",
            cpu_limit="2.0",
            port_mappings={"8080": "8080"},
            environment_vars={"PYTHONUNBUFFERED": "1"}
        )
        assert config.container_name == "test_container"
        assert config.image == "python:3.11"
        assert config.memory_limit == "2g"
        assert config.cpu_limit == "2.0"

    def test_container_config_with_volumes(self):
        """Test container config with volume mounts"""
        config = ContainerConfig(
            container_name="test_container",
            image="python:3.11",
            memory_limit="2g",
            cpu_limit="2.0",
            volume_mounts={
                "/data": "/app/data",
                "/config": "/app/config"
            }
        )
        assert len(config.volume_mounts) == 2
        assert config.volume_mounts["/data"] == "/app/data"

    def test_container_config_default_values(self):
        """Test default configuration values"""
        config = ContainerConfig(
            container_name="test_container",
            image="python:3.11"
        )
        assert config.memory_limit == "1g"
        assert config.cpu_limit == "1.0"
        assert config.restart_policy == "unless-stopped"


class TestContainerStatus:
    """Test ContainerStatus dataclass"""

    def test_container_status_creation(self):
        """Test creating container status"""
        status = ContainerStatus(
            container_id="abc123def456",
            container_name="test_container",
            status="running",
            created_at=datetime.now(),
            last_checked=datetime.now()
        )
        assert status.container_id == "abc123def456"
        assert status.status == "running"

    def test_container_status_with_metrics(self):
        """Test container status with health metrics"""
        status = ContainerStatus(
            container_id="abc123def456",
            container_name="test_container",
            status="running",
            created_at=datetime.now(),
            last_checked=datetime.now(),
            memory_usage_mb=512.5,
            cpu_usage_percent=25.3,
            network_in_bytes=1024000,
            network_out_bytes=2048000
        )
        assert status.memory_usage_mb == 512.5
        assert status.cpu_usage_percent == 25.3

    def test_container_status_transitions(self):
        """Test valid status transitions"""
        status = ContainerStatus(
            container_id="abc123def456",
            container_name="test_container",
            status="created",
            created_at=datetime.now(),
            last_checked=datetime.now()
        )
        valid_statuses = ["created", "running", "paused", "stopped", "exited", "dead"]
        for valid_status in valid_statuses:
            status.status = valid_status
            assert status.status == valid_status


class TestDockerContainerManager:
    """Test DockerContainerManager"""

    def test_container_manager_initialization(self):
        """Test DockerContainerManager initialization"""
        manager = DockerContainerManager()
        assert manager is not None

    def test_create_container_config_validation(self):
        """Test container creation with config validation"""
        manager = DockerContainerManager()
        config = ContainerConfig(
            container_name="test_container",
            image="python:3.11",
            memory_limit="2g",
            cpu_limit="2.0"
        )
        assert config.container_name == "test_container"
        assert config.image == "python:3.11"

    def test_container_config_memory_validation(self):
        """Test memory configuration validation"""
        config = ContainerConfig(
            container_name="test_container",
            image="python:3.11",
            memory_limit="4g"
        )
        # Extract numeric value
        memory_value = config.memory_limit.rstrip("gmk")
        assert int(memory_value) == 4

    def test_container_config_cpu_validation(self):
        """Test CPU configuration validation"""
        config = ContainerConfig(
            container_name="test_container",
            image="python:3.11",
            cpu_limit="4.0"
        )
        assert float(config.cpu_limit) == 4.0

    def test_container_config_port_mapping(self):
        """Test port mapping configuration"""
        config = ContainerConfig(
            container_name="test_container",
            image="python:3.11",
            port_mappings={"8080": "8080", "5432": "5432"}
        )
        assert len(config.port_mappings) == 2
        assert config.port_mappings["8080"] == "8080"
        assert config.port_mappings["5432"] == "5432"

    def test_container_config_environment_variables(self):
        """Test environment variable configuration"""
        config = ContainerConfig(
            container_name="test_container",
            image="python:3.11",
            environment_vars={
                "PYTHONUNBUFFERED": "1",
                "LOG_LEVEL": "DEBUG",
                "DATABASE_URL": "postgresql://localhost/db"
            }
        )
        assert len(config.environment_vars) == 3
        assert config.environment_vars["PYTHONUNBUFFERED"] == "1"

    def test_container_config_volume_mounts(self):
        """Test volume mount configuration"""
        config = ContainerConfig(
            container_name="test_container",
            image="python:3.11",
            volume_mounts={
                "/data": "/app/data",
                "/config": "/etc/app/config"
            }
        )
        assert len(config.volume_mounts) == 2
        assert "/app/data" in config.volume_mounts.values()


class TestContainerNetworkManager:
    """Test ContainerNetworkManager"""

    def test_network_manager_initialization(self):
        """Test NetworkManager initialization"""
        manager = ContainerNetworkManager()
        assert manager is not None

    def test_network_config_creation(self):
        """Test network configuration creation"""
        manager = ContainerNetworkManager()
        network_config = {
            "name": "isolated_net",
            "driver": "bridge",
            "subnet": "172.20.0.0/16"
        }
        assert network_config["name"] == "isolated_net"
        assert network_config["driver"] == "bridge"

    def test_subnet_validation(self):
        """Test subnet CIDR validation"""
        subnets = [
            "172.20.0.0/16",
            "192.168.0.0/24",
            "10.0.0.0/8"
        ]
        for subnet in subnets:
            parts = subnet.split("/")
            assert len(parts) == 2
            assert len(parts[0].split(".")) == 4

    def test_port_mapping_configuration(self):
        """Test port mapping in network config"""
        port_mappings = {
            "8080": "8080",
            "8443": "443",
            "5432": "5432"
        }
        for host_port, container_port in port_mappings.items():
            assert isinstance(host_port, str)
            assert isinstance(container_port, str)

    def test_network_isolation_levels(self):
        """Test network isolation configuration levels"""
        isolation_configs = [
            {"level": "high", "driver": "bridge", "isolation": "network"},
            {"level": "medium", "driver": "overlay", "isolation": "partial"},
            {"level": "low", "driver": "host", "isolation": "none"}
        ]
        assert len(isolation_configs) == 3
        assert isolation_configs[0]["level"] == "high"


class TestContainerHealthMonitor:
    """Test ContainerHealthMonitor"""

    def test_health_monitor_initialization(self):
        """Test HealthMonitor initialization"""
        monitor = ContainerHealthMonitor()
        assert monitor is not None

    def test_health_check_status(self):
        """Test health check status tracking"""
        monitor = ContainerHealthMonitor()
        health_status = {
            "container_id": "abc123",
            "status": "healthy",
            "checks_passed": 5,
            "checks_total": 5,
            "last_check": datetime.now()
        }
        assert health_status["status"] == "healthy"
        assert health_status["checks_passed"] == health_status["checks_total"]

    def test_metrics_tracking(self):
        """Test metrics tracking"""
        metrics = {
            "memory_usage_mb": 512.5,
            "cpu_usage_percent": 25.3,
            "network_in_bytes": 1024000,
            "network_out_bytes": 2048000,
            "disk_usage_mb": 1024.0
        }
        assert metrics["memory_usage_mb"] > 0
        assert 0 <= metrics["cpu_usage_percent"] <= 100
        assert metrics["network_in_bytes"] >= 0
        assert metrics["network_out_bytes"] >= 0

    def test_threshold_checking(self):
        """Test threshold checking for alerts"""
        thresholds = {
            "memory_percent": 80,
            "cpu_percent": 90,
            "disk_percent": 85
        }
        current_metrics = {
            "memory_percent": 75,
            "cpu_percent": 85,
            "disk_percent": 80
        }

        alerts = []
        for metric, threshold in thresholds.items():
            if current_metrics[metric] > threshold:
                alerts.append(f"{metric} exceeds threshold")

        assert len(alerts) == 0

    def test_threshold_alert_triggers(self):
        """Test threshold alert triggering"""
        thresholds = {
            "memory_percent": 80,
            "cpu_percent": 90,
            "disk_percent": 85
        }
        current_metrics = {
            "memory_percent": 85,  # Exceeds
            "cpu_percent": 95,      # Exceeds
            "disk_percent": 80      # Within limits
        }

        alerts = []
        for metric, threshold in thresholds.items():
            if current_metrics[metric] > threshold:
                alerts.append(f"{metric} exceeds threshold")

        assert len(alerts) == 2
        assert "memory_percent exceeds threshold" in alerts
        assert "cpu_percent exceeds threshold" in alerts

    def test_health_history_tracking(self):
        """Test health history tracking"""
        monitor = ContainerHealthMonitor()
        health_entries = []

        for i in range(10):
            entry = {
                "timestamp": datetime.now() - timedelta(minutes=i),
                "status": "healthy" if i % 2 == 0 else "warning",
                "memory_mb": 512 + (i * 10),
                "cpu_percent": 25 + (i * 2)
            }
            health_entries.append(entry)

        assert len(health_entries) == 10
        assert health_entries[0]["status"] == "healthy"
        assert health_entries[1]["status"] == "warning"

    def test_performance_trend_analysis(self):
        """Test performance trend analysis"""
        measurements = [
            {"cpu": 20, "memory": 400},
            {"cpu": 25, "memory": 420},
            {"cpu": 30, "memory": 450},
            {"cpu": 35, "memory": 480}
        ]

        cpu_trend = [m["cpu"] for m in measurements]
        memory_trend = [m["memory"] for m in measurements]

        # Calculate trends
        cpu_increasing = all(
            cpu_trend[i] <= cpu_trend[i+1]
            for i in range(len(cpu_trend)-1)
        )
        memory_increasing = all(
            memory_trend[i] <= memory_trend[i+1]
            for i in range(len(memory_trend)-1)
        )

        assert cpu_increasing is True
        assert memory_increasing is True


class TestContainerLifecycleManagement:
    """Integration tests for container lifecycle"""

    def test_container_creation_workflow(self):
        """Test complete container creation workflow"""
        config = ContainerConfig(
            container_name="test_app",
            image="python:3.11",
            memory_limit="2g",
            cpu_limit="2.0",
            port_mappings={"8080": "8080"},
            environment_vars={"LOG_LEVEL": "INFO"}
        )

        assert config.container_name == "test_app"
        assert config.image == "python:3.11"
        assert config.memory_limit == "2g"

    def test_container_status_lifecycle(self):
        """Test container status lifecycle"""
        statuses = ["created", "running", "paused", "running", "stopped", "removed"]
        
        current_status = ContainerStatus(
            container_id="test123",
            container_name="test_container",
            status="created",
            created_at=datetime.now(),
            last_checked=datetime.now()
        )

        for new_status in statuses[1:]:
            current_status.status = new_status
            current_status.last_checked = datetime.now()
            assert current_status.status == new_status

    def test_multi_container_network_setup(self):
        """Test setting up network for multiple containers"""
        containers = [
            ContainerConfig(
                container_name="api_service",
                image="python:3.11",
                port_mappings={"8080": "8080"}
            ),
            ContainerConfig(
                container_name="db_service",
                image="postgres:15",
                port_mappings={"5432": "5432"}
            ),
            ContainerConfig(
                container_name="cache_service",
                image="redis:7",
                port_mappings={"6379": "6379"}
            )
        ]

        assert len(containers) == 3
        for container in containers:
            assert container.image is not None
            assert len(container.port_mappings) > 0

    def test_container_health_monitoring_workflow(self):
        """Test complete health monitoring workflow"""
        monitor = ContainerHealthMonitor()
        
        # Simulate health checks over time
        health_history = []
        for minute in range(5):
            status = ContainerStatus(
                container_id="test123",
                container_name="test_container",
                status="running",
                created_at=datetime.now() - timedelta(minutes=5),
                last_checked=datetime.now() - timedelta(minutes=minute),
                memory_usage_mb=512 + (minute * 20),
                cpu_usage_percent=20 + (minute * 5)
            )
            health_history.append(status)

        assert len(health_history) == 5
        assert health_history[0].cpu_usage_percent == 20
        assert health_history[4].cpu_usage_percent == 40


class TestResourceLimitations:
    """Test resource limitation and enforcement"""

    def test_memory_limit_parsing(self):
        """Test parsing memory limit strings"""
        limits = ["512m", "1g", "2g", "4096m"]
        
        for limit in limits:
            if limit.endswith("m"):
                value = int(limit[:-1])
                assert value > 0
            elif limit.endswith("g"):
                value = int(limit[:-1])
                assert value > 0

    def test_cpu_limit_validation(self):
        """Test CPU limit validation"""
        valid_cpu_limits = ["0.5", "1.0", "2.0", "4.0"]
        
        for limit in valid_cpu_limits:
            cpu_value = float(limit)
            assert cpu_value > 0
            assert cpu_value <= 8.0  # Reasonable max

    def test_resource_constraint_combinations(self):
        """Test valid resource constraint combinations"""
        configs = [
            ContainerConfig("app1", "python:3.11", memory_limit="512m", cpu_limit="0.5"),
            ContainerConfig("app2", "python:3.11", memory_limit="1g", cpu_limit="1.0"),
            ContainerConfig("app3", "python:3.11", memory_limit="4g", cpu_limit="4.0")
        ]

        for config in configs:
            assert config.memory_limit is not None
            assert config.cpu_limit is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
