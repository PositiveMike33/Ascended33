"""
vault_api.py — Obsidian Vault integration client.

Supports two modes:
  - "rest_api": Uses Obsidian Local REST API plugin (preferred, bidirectional)
  - "filesystem": Direct file read/write (fallback, when on same machine as Vault)

Obsidian Local REST API plugin: https://github.com/coddingtonbear/obsidian-local-rest-api
Default port: 27123

Usage:
    vault = ObsidianVaultClient.from_config()
    vault.create_note("Security/OSINT/2026-02-19-target.md", content)
    vault.read_note("Templates/osint_report.md")
    vault.append_to_note("Security/OSINT/index.md", "- [[2026-02-19-target]]\\n")
"""

import logging
from pathlib import Path

import requests

logger = logging.getLogger(__name__)


class VaultConnectionError(Exception):
    pass


class ObsidianVaultClient:
    def __init__(
        self,
        mode: str = "rest_api",
        base_url: str = "http://localhost:27123",
        api_key: str = "",
        vault_path: str = "D:/Vault",
    ):
        self.mode = mode
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.vault_path = Path(vault_path)

    @classmethod
    def from_config(cls) -> "ObsidianVaultClient":
        """Load configuration from config/config.yaml."""
        try:
            import yaml
            with open("config/config.yaml") as f:
                cfg = yaml.safe_load(f)
            vault_cfg = cfg.get("vault", {})
            return cls(
                mode=vault_cfg.get("mode", "rest_api"),
                base_url=vault_cfg.get("base_url", "http://localhost:27123"),
                api_key=vault_cfg.get("api_key", ""),
                vault_path=vault_cfg.get("vault_path", "D:/Vault"),
            )
        except FileNotFoundError:
            logger.warning(
                "config/config.yaml not found — using defaults. "
                "Copy config/config.example.yaml to config/config.yaml and configure it."
            )
            return cls()

    def _headers(self) -> dict:
        headers = {"Content-Type": "text/markdown"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    def _api_get(self, path: str) -> str:
        url = f"{self.base_url}/vault/{path.lstrip('/')}"
        try:
            response = requests.get(url, headers=self._headers(), timeout=10)
            if response.status_code == 404:
                return ""
            response.raise_for_status()
            return response.text
        except requests.ConnectionError as e:
            raise VaultConnectionError(
                f"Cannot reach Obsidian REST API at {self.base_url}. "
                "Is Obsidian running with the Local REST API plugin active?"
            ) from e

    def _api_put(self, path: str, content: str) -> None:
        url = f"{self.base_url}/vault/{path.lstrip('/')}"
        try:
            response = requests.put(url, data=content.encode(), headers=self._headers(), timeout=10)
            response.raise_for_status()
        except requests.ConnectionError as e:
            raise VaultConnectionError(
                f"Cannot reach Obsidian REST API at {self.base_url}."
            ) from e

    def read_note(self, vault_path: str) -> str:
        """Read the content of a note in the Vault."""
        if self.mode == "rest_api":
            return self._api_get(vault_path)
        note_path = self.vault_path / vault_path
        if not note_path.exists():
            return ""
        return note_path.read_text(encoding="utf-8")

    def create_note(self, vault_path: str, content: str, tags: list[str] | None = None) -> None:
        """Create or overwrite a note in the Vault."""
        if tags:
            tag_line = " ".join(f"#{t}" for t in tags)
            if not content.endswith("\n"):
                content += "\n"
            content += f"\n{tag_line}\n"

        if self.mode == "rest_api":
            self._api_put(vault_path, content)
        else:
            note_path = self.vault_path / vault_path
            note_path.parent.mkdir(parents=True, exist_ok=True)
            note_path.write_text(content, encoding="utf-8")

        logger.info("Vault note created/updated: %s", vault_path)

    def append_to_note(self, vault_path: str, text: str) -> None:
        """Append text to an existing note, or create it if it doesn't exist."""
        existing = self.read_note(vault_path)
        self.create_note(vault_path, existing + text)

    def note_exists(self, vault_path: str) -> bool:
        """Check if a note exists in the Vault."""
        if self.mode == "rest_api":
            return bool(self._api_get(vault_path))
        return (self.vault_path / vault_path).exists()

    def is_reachable(self) -> bool:
        """Check if the Vault / REST API is accessible."""
        if self.mode == "filesystem":
            return self.vault_path.exists()
        try:
            requests.get(f"{self.base_url}/", timeout=5)
            return True
        except (requests.ConnectionError, requests.Timeout):
            return False
