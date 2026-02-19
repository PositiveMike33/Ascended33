"""
network_scan.py — Active network reconnaissance via Nmap on Kali VM.

Runs Nmap scans through the Kali SSH client and parses XML output into
typed Python structures. All scans are gated by OPSEC verification and
require explicit authorization confirmation before executing.

Scan types available:
  quick   — Top 100 ports, no OS/version detection (fastest)
  default — Top 1000 ports + service version detection
  full    — All ports (0-65535) + version + OS + default scripts
  stealth — SYN scan only, reduced timing (slower, less noisy)

Usage:
    from scripts.recon.network_scan import NetworkScanner, ScanType

    scanner = NetworkScanner.from_config()
    results = scanner.scan(
        target="target.example.com",
        scan_type=ScanType.DEFAULT,
        authorization_confirmed=True,
    )
    print(results.summary())
    for host in results.hosts:
        for port in host.open_ports:
            print(f"  {port.port}/{port.protocol} {port.service} {port.version}")
"""

import logging
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional

logger = logging.getLogger(__name__)


class ScanType(Enum):
    QUICK = "quick"
    DEFAULT = "default"
    FULL = "full"
    STEALTH = "stealth"


# ----------------------------------------------------------------
# DATA CLASSES
# ----------------------------------------------------------------

@dataclass
class PortResult:
    port: int
    protocol: str
    state: str
    service: str = ""
    version: str = ""
    extra_info: str = ""
    cpe: str = ""

    @property
    def is_open(self) -> bool:
        return self.state == "open"

    def __str__(self) -> str:
        svc = f"{self.service} {self.version}".strip()
        return f"{self.port}/{self.protocol} [{self.state}] {svc}"


@dataclass
class OsMatch:
    name: str
    accuracy: int
    os_family: str = ""
    os_gen: str = ""


@dataclass
class HostResult:
    ip: str
    hostname: str = ""
    state: str = ""
    ports: list[PortResult] = field(default_factory=list)
    os_matches: list[OsMatch] = field(default_factory=list)

    @property
    def open_ports(self) -> list[PortResult]:
        return [p for p in self.ports if p.is_open]

    @property
    def best_os_guess(self) -> Optional[OsMatch]:
        return max(self.os_matches, key=lambda o: o.accuracy) if self.os_matches else None


@dataclass
class ScanResult:
    target: str
    scan_type: str
    started_at: datetime
    completed_at: Optional[datetime]
    hosts: list[HostResult] = field(default_factory=list)
    nmap_command: str = ""
    nmap_version: str = ""
    raw_xml: str = ""
    error: Optional[str] = None

    @property
    def success(self) -> bool:
        return self.error is None and len(self.hosts) > 0

    @property
    def open_port_count(self) -> int:
        return sum(len(h.open_ports) for h in self.hosts)

    def summary(self) -> str:
        if self.error:
            return f"[network_scan] ERROR: {self.error}"
        duration = (
            f"{(self.completed_at - self.started_at).seconds}s"
            if self.completed_at else "N/A"
        )
        lines = [
            f"[network_scan] Scan complete — {self.target} ({self.scan_type})",
            f"  Hosts up       : {len(self.hosts)}",
            f"  Open ports     : {self.open_port_count}",
            f"  Duration       : {duration}",
            f"  Nmap command   : {self.nmap_command}",
        ]
        for host in self.hosts:
            lines.append(f"\n  Host: {host.ip} ({host.hostname or 'no hostname'})")
            if host.best_os_guess:
                lines.append(
                    f"    OS: {host.best_os_guess.name} "
                    f"({host.best_os_guess.accuracy}% confidence)"
                )
            for p in host.open_ports:
                lines.append(f"    {p}")
        return "\n".join(lines)


# ----------------------------------------------------------------
# XML PARSER
# ----------------------------------------------------------------

def _parse_nmap_xml(xml_content: str) -> list[HostResult]:
    """
    Parse Nmap XML output into HostResult objects.

    Args:
        xml_content: Raw Nmap XML string.

    Returns:
        List of HostResult objects.
    """
    hosts: list[HostResult] = []
    try:
        root = ET.fromstring(xml_content)
    except ET.ParseError as e:
        logger.error("Failed to parse Nmap XML: %s", e)
        return hosts

    for host_elem in root.findall("host"):
        status = host_elem.find("status")
        host_state = status.get("state", "") if status is not None else ""

        # IP address
        ip = ""
        hostname = ""
        for addr in host_elem.findall("address"):
            if addr.get("addrtype") == "ipv4":
                ip = addr.get("addr", "")
                break

        # Hostname
        hostnames = host_elem.find("hostnames")
        if hostnames is not None:
            hn = hostnames.find("hostname")
            if hn is not None:
                hostname = hn.get("name", "")

        host = HostResult(ip=ip, hostname=hostname, state=host_state)

        # Ports
        ports_elem = host_elem.find("ports")
        if ports_elem is not None:
            for port_elem in ports_elem.findall("port"):
                state_elem = port_elem.find("state")
                service_elem = port_elem.find("service")
                port_state = state_elem.get("state", "") if state_elem is not None else ""
                service_name = ""
                service_version = ""
                extra_info = ""
                cpe_str = ""
                if service_elem is not None:
                    service_name = service_elem.get("name", "")
                    service_version = (
                        f"{service_elem.get('product', '')} "
                        f"{service_elem.get('version', '')} "
                        f"{service_elem.get('extrainfo', '')}"
                    ).strip()
                    extra_info = service_elem.get("extrainfo", "")
                    cpe_elem = service_elem.find("cpe")
                    cpe_str = cpe_elem.text or "" if cpe_elem is not None else ""

                host.ports.append(PortResult(
                    port=int(port_elem.get("portid", 0)),
                    protocol=port_elem.get("protocol", "tcp"),
                    state=port_state,
                    service=service_name,
                    version=service_version,
                    extra_info=extra_info,
                    cpe=cpe_str,
                ))

        # OS detection
        os_elem = host_elem.find("os")
        if os_elem is not None:
            for match in os_elem.findall("osmatch"):
                osclass = match.find("osclass")
                host.os_matches.append(OsMatch(
                    name=match.get("name", ""),
                    accuracy=int(match.get("accuracy", 0)),
                    os_family=osclass.get("osfamily", "") if osclass is not None else "",
                    os_gen=osclass.get("osgen", "") if osclass is not None else "",
                ))

        hosts.append(host)

    return hosts


# ----------------------------------------------------------------
# NMAP COMMAND BUILDER
# ----------------------------------------------------------------

_SCAN_PROFILES: dict[ScanType, str] = {
    ScanType.QUICK: (
        "-sS -T4 --top-ports 100 -oX -"
    ),
    ScanType.DEFAULT: (
        "-sS -sV -T4 --top-ports 1000 -oX -"
    ),
    ScanType.FULL: (
        "-sS -sV -sC -O -T4 -p- -oX -"
    ),
    ScanType.STEALTH: (
        "-sS -sV -T2 --top-ports 1000 -oX -"
    ),
}


def _build_nmap_command(target: str, scan_type: ScanType, extra_args: str = "") -> str:
    flags = _SCAN_PROFILES[scan_type]
    cmd = f"nmap {flags} {target}"
    if extra_args:
        cmd += f" {extra_args}"
    return cmd


# ----------------------------------------------------------------
# SCANNER CLASS
# ----------------------------------------------------------------

class NetworkScanner:
    """
    Active network scanner using Nmap via Kali SSH.

    All scans require:
      1. OPSEC verification (VPN active)
      2. Explicit authorization_confirmed=True flag

    Args:
        ssh_client: Connected KaliSSHClient instance.
        nmap_timeout: Max seconds to wait for Nmap (default 600s / 10 min).
    """

    def __init__(self, ssh_client, nmap_timeout: int = 600) -> None:
        self.ssh = ssh_client
        self.nmap_timeout = nmap_timeout

    @classmethod
    def from_config(cls) -> "NetworkScanner":
        """Create scanner loading Kali SSH config from config.yaml."""
        from mcp.kali_ssh_client import KaliSSHClient
        return cls(ssh_client=KaliSSHClient.from_config())

    def scan(
        self,
        target: str,
        scan_type: ScanType = ScanType.DEFAULT,
        authorization_confirmed: bool = False,
        extra_args: str = "",
        require_vpn: bool = True,
    ) -> ScanResult:
        """
        Run an Nmap scan against a target via Kali SSH.

        Args:
            target: IP address, hostname, or CIDR range to scan.
            scan_type: ScanType enum defining the scan profile.
            authorization_confirmed: Must be True — explicit consent that
                                     this target is in authorized scope.
            extra_args: Additional Nmap flags appended to the command.
            require_vpn: If True (default), verifies VPN is active first.

        Returns:
            ScanResult with parsed host/port data.
        """
        started_at = datetime.now()

        # ---- Authorization gate ----
        if not authorization_confirmed:
            return ScanResult(
                target=target,
                scan_type=scan_type.value,
                started_at=started_at,
                completed_at=datetime.now(),
                error=(
                    "Authorization required. "
                    "Pass authorization_confirmed=True only after confirming "
                    "this target is within your authorized scope "
                    "(client letter / bug bounty scope / personal lab)."
                ),
            )

        # ---- OPSEC gate ----
        from scripts.opsec.vpn_check import verify_opsec
        opsec = verify_opsec(require_vpn=require_vpn)
        if not opsec.safe:
            return ScanResult(
                target=target,
                scan_type=scan_type.value,
                started_at=started_at,
                completed_at=datetime.now(),
                error=f"OPSEC check failed: {opsec.reason}",
            )

        # ---- Build and run Nmap command ----
        nmap_cmd = _build_nmap_command(target, scan_type, extra_args)
        logger.info("Starting %s scan on %s: %s", scan_type.value, target, nmap_cmd)

        try:
            result = self.ssh.run(nmap_cmd, timeout=self.nmap_timeout)
        except Exception as e:
            return ScanResult(
                target=target,
                scan_type=scan_type.value,
                started_at=started_at,
                completed_at=datetime.now(),
                nmap_command=nmap_cmd,
                error=f"SSH/Nmap execution failed: {e}",
            )

        if not result.success:
            return ScanResult(
                target=target,
                scan_type=scan_type.value,
                started_at=started_at,
                completed_at=datetime.now(),
                nmap_command=nmap_cmd,
                error=f"Nmap exited with code {result.exit_code}: {result.stderr}",
            )

        # ---- Parse XML output ----
        hosts = _parse_nmap_xml(result.stdout)
        completed_at = datetime.now()

        return ScanResult(
            target=target,
            scan_type=scan_type.value,
            started_at=started_at,
            completed_at=completed_at,
            hosts=hosts,
            nmap_command=nmap_cmd,
            raw_xml=result.stdout,
        )

    def quick_tcp(self, target: str, authorization_confirmed: bool = False) -> ScanResult:
        """Quick TCP scan of top 100 ports."""
        return self.scan(target, ScanType.QUICK,
                         authorization_confirmed=authorization_confirmed)

    def service_scan(self, target: str, authorization_confirmed: bool = False) -> ScanResult:
        """Default scan with service/version detection (top 1000 ports)."""
        return self.scan(target, ScanType.DEFAULT,
                         authorization_confirmed=authorization_confirmed)

    def full_scan(self, target: str, authorization_confirmed: bool = False) -> ScanResult:
        """Full scan: all 65535 ports + OS + scripts. Slow but thorough."""
        return self.scan(target, ScanType.FULL,
                         authorization_confirmed=authorization_confirmed)


# ----------------------------------------------------------------
# CLI ENTRY POINT
# ----------------------------------------------------------------

def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(
        description="network_scan — Nmap active recon via Kali SSH",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 scripts/recon/network_scan.py --target <KALI_IP> --type default --authorized
  python3 scripts/recon/network_scan.py --target <LAB_CIDR> --type quick --authorized
  python3 scripts/recon/network_scan.py --target lab.example.com --type full --authorized

WARNING: Only scan targets you are authorized to test.
        """,
    )
    parser.add_argument("--target", required=True, help="IP, hostname or CIDR range")
    parser.add_argument(
        "--type",
        choices=[t.value for t in ScanType],
        default="default",
        help="Scan profile (default: default)",
    )
    parser.add_argument(
        "--authorized",
        action="store_true",
        help="Confirm this target is within authorized scope (required)",
    )
    parser.add_argument("--no-vpn", action="store_true",
                        help="Skip VPN requirement (not recommended)")
    parser.add_argument("--extra-args", default="",
                        help="Extra Nmap flags (e.g. '--script vuln')")
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s: %(message)s",
    )

    if not args.authorized:
        print("ERROR: --authorized flag required. Only scan targets in your authorized scope.")
        return 1

    scanner = NetworkScanner.from_config()
    result = scanner.scan(
        target=args.target,
        scan_type=ScanType(args.type),
        authorization_confirmed=True,
        extra_args=args.extra_args,
        require_vpn=not args.no_vpn,
    )

    print(result.summary())
    return 0 if result.success else 1


if __name__ == "__main__":
    sys.exit(main())
