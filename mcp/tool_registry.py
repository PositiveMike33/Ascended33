"""
tool_registry.py — Registry of available security tools across hexstrike-ai and Kali VM.

Maps tool names to metadata (category, description, requires_active_recon).
Used to validate tool selection and enforce OPSEC rules.

Usage:
    registry = ToolRegistry()
    tool = registry.get("nmap")
    if tool.requires_active_recon:
        verify_opsec()
"""

from dataclasses import dataclass, field
from enum import Enum


class ToolCategory(str, Enum):
    PASSIVE_RECON = "passive_recon"
    ACTIVE_RECON = "active_recon"
    WEB_ENUM = "web_enum"
    VULN_SCAN = "vuln_scan"
    EXPLOIT = "exploit"
    OSINT = "osint"
    REPORTING = "reporting"
    OPSEC = "opsec"


@dataclass
class ToolDefinition:
    name: str
    category: ToolCategory
    description: str
    requires_active_recon: bool = False
    requires_authorization: bool = False
    hexstrike_agent: str = "decision_engine"
    aliases: list[str] = field(default_factory=list)


_REGISTRY: list[ToolDefinition] = [
    # --- Passive OSINT / Recon ---
    ToolDefinition(
        name="whois",
        category=ToolCategory.PASSIVE_RECON,
        description="WHOIS domain registration lookup",
        hexstrike_agent="decision_engine",
    ),
    ToolDefinition(
        name="dnslookup",
        category=ToolCategory.PASSIVE_RECON,
        description="DNS record enumeration (A, MX, NS, TXT, SOA)",
        hexstrike_agent="decision_engine",
        aliases=["dns", "dig"],
    ),
    ToolDefinition(
        name="amass",
        category=ToolCategory.PASSIVE_RECON,
        description="Subdomain enumeration and ASN discovery",
        hexstrike_agent="decision_engine",
    ),
    ToolDefinition(
        name="shodan",
        category=ToolCategory.PASSIVE_RECON,
        description="Shodan search for exposed services and banners",
        hexstrike_agent="decision_engine",
    ),
    ToolDefinition(
        name="theHarvester",
        category=ToolCategory.OSINT,
        description="Email, subdomain, and employee OSINT harvesting",
        hexstrike_agent="decision_engine",
        aliases=["harvester"],
    ),
    ToolDefinition(
        name="breach_check",
        category=ToolCategory.OSINT,
        description="Check emails/domains against breach databases (HaveIBeenPwned)",
        hexstrike_agent="decision_engine",
    ),
    # --- Active Recon ---
    ToolDefinition(
        name="nmap",
        category=ToolCategory.ACTIVE_RECON,
        description="Network port scanning and service version detection",
        requires_active_recon=True,
        requires_authorization=True,
        hexstrike_agent="decision_engine",
    ),
    ToolDefinition(
        name="masscan",
        category=ToolCategory.ACTIVE_RECON,
        description="High-speed port scanner",
        requires_active_recon=True,
        requires_authorization=True,
        hexstrike_agent="decision_engine",
    ),
    # --- Web Enumeration ---
    ToolDefinition(
        name="nuclei",
        category=ToolCategory.WEB_ENUM,
        description="Template-based vulnerability scanner for web apps",
        requires_active_recon=True,
        requires_authorization=True,
        hexstrike_agent="decision_engine",
    ),
    ToolDefinition(
        name="ffuf",
        category=ToolCategory.WEB_ENUM,
        description="Web fuzzer for directories, files, and parameters",
        requires_active_recon=True,
        requires_authorization=True,
        hexstrike_agent="decision_engine",
    ),
    ToolDefinition(
        name="wpscan",
        category=ToolCategory.WEB_ENUM,
        description="WordPress vulnerability scanner",
        requires_active_recon=True,
        requires_authorization=True,
        hexstrike_agent="decision_engine",
        aliases=["wordpress"],
    ),
    ToolDefinition(
        name="sqlmap",
        category=ToolCategory.WEB_ENUM,
        description="Automated SQL injection detection and exploitation",
        requires_active_recon=True,
        requires_authorization=True,
        hexstrike_agent="decision_engine",
    ),
    # --- Vulnerability Scanning ---
    ToolDefinition(
        name="nikto",
        category=ToolCategory.VULN_SCAN,
        description="Web server vulnerability scanner",
        requires_active_recon=True,
        requires_authorization=True,
        hexstrike_agent="decision_engine",
    ),
    ToolDefinition(
        name="openvas",
        category=ToolCategory.VULN_SCAN,
        description="Full vulnerability assessment (OpenVAS/GVM)",
        requires_active_recon=True,
        requires_authorization=True,
        hexstrike_agent="decision_engine",
    ),
    # --- CVE Intelligence ---
    ToolDefinition(
        name="cve_lookup",
        category=ToolCategory.OSINT,
        description="CVE lookup, CVSS scoring, PoC availability",
        hexstrike_agent="cve_intelligence",
        aliases=["cve"],
    ),
    # --- CTF ---
    ToolDefinition(
        name="ctf_analyze",
        category=ToolCategory.OSINT,
        description="CTF challenge analysis and solver",
        hexstrike_agent="ctf_solver",
        aliases=["ctf"],
    ),
    # --- Bug Bounty ---
    ToolDefinition(
        name="bug_bounty",
        category=ToolCategory.ACTIVE_RECON,
        description="Multi-stage bug bounty workflow manager",
        requires_active_recon=True,
        requires_authorization=True,
        hexstrike_agent="bug_bounty_manager",
    ),
]


class ToolNotFoundError(Exception):
    pass


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, ToolDefinition] = {}
        for tool in _REGISTRY:
            self._tools[tool.name] = tool
            for alias in tool.aliases:
                self._tools[alias] = tool

    def get(self, name: str) -> ToolDefinition:
        """Get a tool definition by name or alias."""
        tool = self._tools.get(name.lower())
        if tool is None:
            raise ToolNotFoundError(
                f"Tool '{name}' not found in registry. "
                f"Available: {', '.join(self.list_names())}"
            )
        return tool

    def list_names(self) -> list[str]:
        """Return all unique tool names (no aliases)."""
        return sorted({t.name for t in _REGISTRY})

    def by_category(self, category: ToolCategory) -> list[ToolDefinition]:
        """Return all tools in a given category."""
        return [t for t in _REGISTRY if t.category == category]

    def passive_only(self) -> list[ToolDefinition]:
        """Return tools that do NOT require active recon."""
        return [t for t in _REGISTRY if not t.requires_active_recon]

    def requires_auth(self) -> list[ToolDefinition]:
        """Return tools that require explicit authorization."""
        return [t for t in _REGISTRY if t.requires_authorization]
