"""
hexstrike_client.py — Client wrapper for hexstrike-ai MCP server.

hexstrike-ai exposes 150+ security tools via MCP at localhost:8888.
This module provides a typed Python interface for Claude Code to call
hexstrike agents and tools programmatically.

In Docker mode (recommended), hexstrike runs as a container with all
traffic routed through Tor. Port 8888 is mapped to localhost.

Start: docker compose up -d hexstrike
"""

import logging
from pathlib import Path
from typing import Any

import requests

logger = logging.getLogger(__name__)

HEXSTRIKE_MCP_URL = "http://localhost:8888"
DEFAULT_TIMEOUT = 30


class HexStrikeConnectionError(Exception):
    pass


class HexStrikeClient:
    def __init__(self, base_url: str = HEXSTRIKE_MCP_URL, timeout: int = DEFAULT_TIMEOUT):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def _post(self, endpoint: str, payload: dict) -> dict:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        try:
            response = requests.post(url, json=payload, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.HTTPError as e:
            raise HexStrikeConnectionError(
                f"hexstrike-ai returned HTTP {e.response.status_code} for {endpoint}. "
                "Check that the endpoint path is correct for your hexstrike version."
            ) from e
        except requests.ConnectionError as e:
            raise HexStrikeConnectionError(
                f"Cannot reach hexstrike-ai at {self.base_url}. "
                "Is the Docker container running? Run: docker compose up -d hexstrike"
            ) from e

    def _jsonrpc(self, method: str, params: dict | None = None) -> dict:
        """
        Send a JSON-RPC 2.0 request (standard MCP over HTTP transport).

        MCP uses JSON-RPC 2.0, not plain REST. Tries /messages (SSE transport)
        then / (streamable HTTP) to find the active endpoint.
        """
        body = {"jsonrpc": "2.0", "method": method, "params": params or {}, "id": 1}
        for path in ("/messages", "/"):
            try:
                response = requests.post(
                    f"{self.base_url}{path}", json=body, timeout=self.timeout
                )
                if response.ok:
                    data = response.json()
                    if "result" in data:
                        return data["result"]
                    if "error" in data:
                        raise HexStrikeConnectionError(
                            f"JSON-RPC error {data['error'].get('code')}: "
                            f"{data['error'].get('message')}"
                        )
            except (requests.ConnectionError, requests.Timeout, requests.HTTPError):
                continue
        raise HexStrikeConnectionError(
            f"MCP JSON-RPC '{method}' failed on all endpoints. "
            "Check hexstrike logs: docker compose logs hexstrike"
        )

    def list_tools(self) -> list[dict]:
        """
        Return all available tools registered in hexstrike-ai.

        Tries MCP JSON-RPC (standard protocol) first, then legacy REST fallback.
        Returns empty list (never raises) so callers can check len(tools) == 0.
        """
        # 1. Standard MCP JSON-RPC: method = "tools/list"
        try:
            result = self._jsonrpc("tools/list")
            tools = result.get("tools", [])
            if tools:
                return tools
        except HexStrikeConnectionError:
            pass

        # 2. Legacy REST: POST /tools/list
        try:
            return self._post("/tools/list", {}).get("tools", [])
        except HexStrikeConnectionError:
            return []

    def run_tool(self, tool_name: str, parameters: dict[str, Any]) -> dict:
        """
        Execute a specific hexstrike tool by name.

        Args:
            tool_name: Name of the tool (e.g., "nmap", "nuclei", "amass")
            parameters: Tool-specific parameters dict

        Returns:
            Tool execution result as a dict
        """
        logger.info("Running hexstrike tool: %s with params: %s", tool_name, parameters)
        return self._post("/tools/call", {"name": tool_name, "arguments": parameters})

    def run_agent(self, agent_name: str, mission: str, context: dict | None = None) -> dict:
        """
        Invoke a hexstrike AI agent for a higher-level mission.

        Args:
            agent_name: Agent name (e.g., "bug_bounty_manager", "ctf_solver",
                        "cve_intelligence", "decision_engine")
            mission: Natural language description of the mission
            context: Optional dict with additional context (target, scope, etc.)

        Returns:
            Agent execution result
        """
        payload = {
            "agent": agent_name,
            "mission": mission,
            "context": context or {},
        }
        logger.info("Invoking hexstrike agent: %s — %s", agent_name, mission)
        return self._post("/agents/run", payload)

    def network_recon(self, target: str, ports: str = "top-1000") -> dict:
        """Convenience: run full network recon against a target."""
        return self.run_agent(
            "decision_engine",
            f"Perform passive and active network reconnaissance on {target}",
            context={"target": target, "port_range": ports},
        )

    def web_scan(self, target_url: str) -> dict:
        """Convenience: run web application security scan."""
        return self.run_agent(
            "decision_engine",
            f"Perform comprehensive web application security assessment on {target_url}",
            context={"target": target_url, "type": "web"},
        )

    def cve_lookup(self, cve_id: str) -> dict:
        """Convenience: look up CVE details and exploitability."""
        return self.run_agent(
            "cve_intelligence",
            f"Analyze {cve_id}: severity, exploitability, affected versions, PoC availability",
            context={"cve_id": cve_id},
        )

    def ctf_analyze(self, challenge_description: str, files: list[str] | None = None) -> dict:
        """Convenience: analyze a CTF challenge."""
        return self.run_agent(
            "ctf_solver",
            challenge_description,
            context={"files": files or []},
        )

    @classmethod
    def from_config(cls) -> "HexStrikeClient":
        """Load hexstrike URL and timeout from config/config.yaml."""
        try:
            import yaml  # type: ignore[import]
            cfg_path = Path(__file__).parent.parent / "config" / "config.yaml"
            with cfg_path.open() as f:
                cfg = yaml.safe_load(f)
            hexstrike_cfg = cfg.get("hexstrike", {})
            url = hexstrike_cfg.get("mcp_url", HEXSTRIKE_MCP_URL)
            timeout = hexstrike_cfg.get("timeout_seconds", DEFAULT_TIMEOUT)
            return cls(base_url=url, timeout=timeout)
        except FileNotFoundError:
            logger.warning("config/config.yaml not found — using defaults")
            return cls()

    def is_reachable(self) -> bool:
        """Check if hexstrike-ai MCP server is reachable."""
        try:
            requests.get(f"{self.base_url}/health", timeout=5)
            return True
        except (requests.ConnectionError, requests.Timeout):
            return False
