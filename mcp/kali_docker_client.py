"""
kali_docker_client.py — Docker exec client for Kali container.

Drop-in replacement for KaliSSHClient when Kali runs in Docker.
Uses `docker exec` to run commands in the ascended33_kali container.
All outbound traffic from the container is routed through Tor.

Usage:
    client = KaliDockerClient.from_config()
    result = client.run("nmap -sV target.com")
    print(result.stdout)

    # Or as context manager:
    with KaliDockerClient.from_config() as client:
        result = client.run("curl https://check.torproject.org/api/ip")
"""

import logging
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

logger = logging.getLogger(__name__)

DEFAULT_CONTAINER = "ascended33_kali"
DEFAULT_TIMEOUT = 300


@dataclass
class CommandResult:
    command: str
    stdout: str
    stderr: str
    exit_code: int

    @property
    def success(self) -> bool:
        return self.exit_code == 0


class KaliDockerError(Exception):
    pass


class KaliDockerClient:
    """
    Execute commands inside the ascended33_kali Docker container.

    All commands run via `docker exec <container> /bin/bash -c <command>`.
    Traffic from the container is routed through Tor (see docker-compose.yml).
    """

    def __init__(
        self,
        container: str = DEFAULT_CONTAINER,
        timeout: int = DEFAULT_TIMEOUT,
        shell: str = "/bin/bash",
    ):
        self.container = container
        self.timeout = timeout
        self.shell = shell

    @classmethod
    def from_config(cls) -> "KaliDockerClient":
        """Load Docker client config from config/config.yaml."""
        try:
            import yaml  # type: ignore[import]
            cfg_path = Path(__file__).parent.parent / "config" / "config.yaml"
            with cfg_path.open() as f:
                cfg = yaml.safe_load(f)
            docker_cfg = cfg.get("docker", {})
            return cls(
                container=docker_cfg.get("kali_container", DEFAULT_CONTAINER),
                timeout=docker_cfg.get("exec_timeout", DEFAULT_TIMEOUT),
            )
        except FileNotFoundError:
            logger.warning("config/config.yaml not found — using defaults")
            return cls()

    def _docker_bin(self) -> str:
        """Return the path to the docker binary."""
        docker = shutil.which("docker")
        if not docker:
            raise KaliDockerError(
                "docker binary not found in PATH. "
                "Is Docker Desktop running?"
            )
        return docker

    def run(self, command: str, timeout: int | None = None) -> CommandResult:
        """
        Execute a command inside the Kali container via docker exec.

        Args:
            command: Shell command to run inside the container.
            timeout: Optional timeout override (seconds).

        Returns:
            CommandResult with stdout, stderr, exit_code.

        Raises:
            KaliDockerError: If docker is not found or times out.
        """
        docker = self._docker_bin()
        cmd = [docker, "exec", self.container, self.shell, "-c", command]
        logger.info("Kali Docker exec: %s", command)

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout or self.timeout,
            )
            return CommandResult(
                command=command,
                stdout=result.stdout.strip(),
                stderr=result.stderr.strip(),
                exit_code=result.returncode,
            )
        except subprocess.TimeoutExpired as e:
            raise KaliDockerError(
                f"Command timed out after {timeout or self.timeout}s: {command}"
            ) from e
        except FileNotFoundError as e:
            raise KaliDockerError("docker binary not found") from e

    def upload_file(self, local_path: str, remote_path: str) -> None:
        """Copy a local file into the Kali container via docker cp."""
        docker = self._docker_bin()
        result = subprocess.run(
            [docker, "cp", local_path, f"{self.container}:{remote_path}"],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            raise KaliDockerError(
                f"docker cp failed ({result.returncode}): {result.stderr.strip()}"
            )
        logger.info("Uploaded %s → %s:%s", local_path, self.container, remote_path)

    def is_reachable(self) -> bool:
        """Check if the Kali container is running."""
        try:
            docker = self._docker_bin()
            result = subprocess.run(
                [docker, "inspect", "--format", "{{.State.Running}}", self.container],
                capture_output=True,
                text=True,
                timeout=10,
            )
            return result.stdout.strip() == "true"
        except (KaliDockerError, subprocess.TimeoutExpired, FileNotFoundError, OSError):
            return False

    def start_hexstrike(self) -> CommandResult:
        """
        hexstrike is managed by docker-compose — this is a no-op.

        To start hexstrike: docker compose up -d hexstrike
        """
        logger.info(
            "hexstrike is managed by docker-compose. "
            "Run: docker compose up -d hexstrike"
        )
        return CommandResult(
            command="docker compose up -d hexstrike",
            stdout="hexstrike is managed by docker-compose. Use: docker compose up -d",
            stderr="",
            exit_code=0,
        )

    def stop_hexstrike(self) -> CommandResult:
        """hexstrike is managed by docker-compose — use docker compose stop hexstrike."""
        return CommandResult(
            command="docker compose stop hexstrike",
            stdout="Use: docker compose stop hexstrike",
            stderr="",
            exit_code=0,
        )

    def hexstrike_status(self) -> bool:
        """Check if hexstrike container is running."""
        try:
            docker = self._docker_bin()
            result = subprocess.run(
                [docker, "inspect", "--format", "{{.State.Running}}", "ascended33_hexstrike"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            return result.stdout.strip() == "true"
        except (KaliDockerError, subprocess.TimeoutExpired, FileNotFoundError, OSError):
            return False

    def __enter__(self) -> "KaliDockerClient":
        return self

    def __exit__(self, *_) -> None:
        pass    # No persistent connection to close
