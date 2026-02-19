"""
hexstrike_client.py — Client wrapper for hexstrike-ai MCP server.

hexstrike-ai exposes 150+ security tools via MCP at localhost:8888.
This module provides a typed Python interface for Claude Code to call
hexstrike agents and tools programmatically.

Requires hexstrike-ai server to be running:
    cd ~/hexstrike-ai && source hexstrike-env/bin/activate
    python3 hexstrike_server.py
"""

import json
import logging
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
        except requests.ConnectionError as e:
            raise HexStrikeConnectionError(
                f"Cannot reach hexstrike-ai at {self.base_url}. "
                "Is the MCP server running? Run: python3 hexstrike_server.py"
            ) from e

    def list_tools(self) -> list[dict]:
        """Return all available tools registered in hexstrike-ai."""
        return self._post("/tools/list", {}).get("tools", [])

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

    def is_reachable(self) -> bool:
        """Check if hexstrike-ai MCP server is reachable."""
        try:
            requests.get(f"{self.base_url}/health", timeout=5)
            return True
        except (requests.ConnectionError, requests.Timeout):
            return False
