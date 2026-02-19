"""
kali_ssh_client.py — SSH client for Kali Linux VM.

Provides a typed interface to run commands on the Kali VM via SSH (paramiko).
Credentials and host info are loaded from config/config.yaml.

Usage:
    client = KaliSSHClient.from_config()
    result = client.run("nmap -sV -p 80,443 target.com")
    print(result.stdout)
"""

import logging
import os
from dataclasses import dataclass
from pathlib import Path

import paramiko

logger = logging.getLogger(__name__)


@dataclass
class CommandResult:
    command: str
    stdout: str
    stderr: str
    exit_code: int

    @property
    def success(self) -> bool:
        return self.exit_code == 0


class KaliSSHError(Exception):
    pass


class KaliSSHClient:
    def __init__(
        self,
        host: str,
        user: str = "kali",
        key_file: str | None = None,
        password: str | None = None,
        port: int = 22,
        timeout: int = 30,
    ):
        self.host = host
        self.user = user
        self.key_file = str(Path(key_file).expanduser()) if key_file else None
        self.password = password
        self.port = port
        self.timeout = timeout
        self._client: paramiko.SSHClient | None = None

    @classmethod
    def from_config(cls) -> "KaliSSHClient":
        """Load Kali VM SSH config from config/config.yaml."""
        try:
            import yaml
            with open("config/config.yaml") as f:
                cfg = yaml.safe_load(f)
            kali = cfg.get("kali_vm", {})
            return cls(
                host=kali.get("host", "kali-lab"),
                user=kali.get("user", "kali"),
                key_file=kali.get("key_file"),
                password=kali.get("password"),
                port=kali.get("port", 22),
            )
        except FileNotFoundError:
            logger.warning("config/config.yaml not found — using defaults")
            return cls(host="kali-lab")

    def connect(self) -> None:
        """Establish SSH connection to Kali VM."""
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        connect_kwargs: dict = {
            "hostname": self.host,
            "username": self.user,
            "port": self.port,
            "timeout": self.timeout,
        }
        if self.key_file and os.path.exists(self.key_file):
            connect_kwargs["key_filename"] = self.key_file
        elif self.password:
            connect_kwargs["password"] = self.password
        else:
            # Try agent / default key
            connect_kwargs["look_for_keys"] = True
            connect_kwargs["allow_agent"] = True

        try:
            client.connect(**connect_kwargs)
            self._client = client
            logger.info("SSH connected to Kali VM at %s", self.host)
        except paramiko.AuthenticationException as e:
            raise KaliSSHError(
                f"SSH authentication failed for {self.user}@{self.host}. "
                "Check key_file or password in config/config.yaml."
            ) from e
        except (paramiko.SSHException, OSError) as e:
            raise KaliSSHError(
                f"Cannot connect to Kali VM at {self.host}:{self.port}. "
                "Is VMware running? Is the VM booted? Check the IP in config/config.yaml."
            ) from e

    def disconnect(self) -> None:
        """Close SSH connection."""
        if self._client:
            self._client.close()
            self._client = None
            logger.info("SSH disconnected from Kali VM")

    def run(self, command: str, timeout: int | None = None) -> CommandResult:
        """
        Execute a command on Kali VM.

        Args:
            command: Shell command to execute
            timeout: Optional timeout in seconds (overrides default)

        Returns:
            CommandResult with stdout, stderr, and exit_code
        """
        if self._client is None:
            self.connect()

        logger.info("Kali SSH run: %s", command)
        try:
            _, stdout, stderr = self._client.exec_command(  # type: ignore[union-attr]
                command, timeout=timeout or self.timeout
            )
            exit_code = stdout.channel.recv_exit_status()
            return CommandResult(
                command=command,
                stdout=stdout.read().decode("utf-8", errors="replace").strip(),
                stderr=stderr.read().decode("utf-8", errors="replace").strip(),
                exit_code=exit_code,
            )
        except paramiko.SSHException as e:
            raise KaliSSHError(f"Command failed: {command}") from e

    def upload_file(self, local_path: str, remote_path: str) -> None:
        """Upload a file to the Kali VM via SFTP."""
        if self._client is None:
            self.connect()
        sftp = self._client.open_sftp()  # type: ignore[union-attr]
        try:
            sftp.put(local_path, remote_path)
            logger.info("Uploaded %s → %s on Kali", local_path, remote_path)
        finally:
            sftp.close()

    def is_reachable(self) -> bool:
        """Check if the Kali VM is reachable via SSH."""
        try:
            self.connect()
            self.disconnect()
            return True
        except KaliSSHError:
            return False

    def start_hexstrike(self) -> CommandResult:
        """Start the hexstrike-ai MCP server on Kali in the background."""
        return self.run(
            "cd ~/hexstrike-ai && "
            "source hexstrike-env/bin/activate && "
            "nohup python3 hexstrike_server.py > ~/hexstrike.log 2>&1 &"
        )

    def stop_hexstrike(self) -> CommandResult:
        """Stop the hexstrike-ai MCP server on Kali."""
        return self.run("pkill -f hexstrike_server.py")

    def hexstrike_status(self) -> bool:
        """Check if hexstrike-ai server is running on Kali."""
        result = self.run("pgrep -f hexstrike_server.py")
        return result.success

    def __enter__(self) -> "KaliSSHClient":
        self.connect()
        return self

    def __exit__(self, *_) -> None:
        self.disconnect()
