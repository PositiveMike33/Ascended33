"""
web_enum.py — Web application enumeration and passive analysis.

Performs passive and active web reconnaissance against a target URL.
Passive checks (headers, TLS, robots.txt) run directly from the operator
machine. Active checks (directory bruteforce, CMS detection) route through
hexstrike-ai on Kali.

Checks performed:
  Passive (always safe, no footprint on target beyond a single request):
    - HTTP response headers analysis (security headers, server banner)
    - SSL/TLS certificate inspection (expiry, SANs, issuer)
    - CORS misconfiguration detection
    - robots.txt and sitemap.xml discovery
    - Redirect chain analysis

  Active (requires authorization_confirmed=True + VPN):
    - Directory/file bruteforce via hexstrike-ai (Gobuster/FFuf)
    - CMS detection via hexstrike-ai (WPScan, CMSeeK)
    - Technology fingerprinting via hexstrike-ai (WhatWeb)

Usage:
    from scripts.recon.web_enum import WebEnumerator

    enum = WebEnumerator.from_config()

    # Passive only — safe, no explicit auth needed
    result = enum.passive_scan("https://target.com")
    print(result.summary())

    # Full (passive + active) — requires authorization
    result = enum.full_scan("https://target.com", authorization_confirmed=True)
    print(result.summary())
"""

import logging
import socket
import ssl
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional
from urllib.parse import urlparse

import requests

logger = logging.getLogger(__name__)

REQUEST_TIMEOUT = 15

# Security headers to check (header_name, description, criticality)
_SECURITY_HEADERS: list[tuple[str, str, str]] = [
    ("Strict-Transport-Security", "HSTS — forces HTTPS", "high"),
    ("Content-Security-Policy", "CSP — XSS / injection protection", "high"),
    ("X-Frame-Options", "Clickjacking protection", "medium"),
    ("X-Content-Type-Options", "MIME sniffing protection", "medium"),
    ("Referrer-Policy", "Referrer data leakage control", "low"),
    ("Permissions-Policy", "Browser feature access control", "low"),
    ("X-XSS-Protection", "Legacy XSS filter (deprecated but checked)", "low"),
]

# Headers that reveal server/tech info (information disclosure)
_DISCLOSURE_HEADERS = [
    "Server", "X-Powered-By", "X-Generator", "X-AspNet-Version",
    "X-AspNetMvc-Version", "X-Runtime", "X-Version",
]


# ----------------------------------------------------------------
# DATA CLASSES
# ----------------------------------------------------------------

@dataclass
class SecurityHeaderResult:
    name: str
    present: bool
    value: str = ""
    criticality: str = "medium"
    description: str = ""


@dataclass
class TlsResult:
    valid: bool
    subject: str = ""
    issuer: str = ""
    expires: Optional[datetime] = None
    days_until_expiry: Optional[int] = None
    san_domains: list[str] = field(default_factory=list)
    protocol_version: str = ""
    error: str = ""

    @property
    def is_expired(self) -> bool:
        return self.days_until_expiry is not None and self.days_until_expiry < 0

    @property
    def expiry_warning(self) -> bool:
        return self.days_until_expiry is not None and 0 <= self.days_until_expiry <= 30


@dataclass
class CorsResult:
    allow_origin: str = ""
    allow_credentials: str = ""
    misconfigured: bool = False
    details: str = ""


@dataclass
class RobotsTxtResult:
    found: bool = False
    disallowed_paths: list[str] = field(default_factory=list)
    sitemaps: list[str] = field(default_factory=list)
    raw: str = ""


@dataclass
class ActiveScanResult:
    tool: str
    findings: list[str] = field(default_factory=list)
    raw_output: str = ""
    error: Optional[str] = None


@dataclass
class WebEnumResult:
    target_url: str
    started_at: datetime
    completed_at: Optional[datetime] = None

    # Passive results
    final_url: str = ""
    status_code: int = 0
    server_banner: str = ""
    disclosure_headers: dict[str, str] = field(default_factory=dict)
    security_headers: list[SecurityHeaderResult] = field(default_factory=list)
    tls: Optional[TlsResult] = None
    cors: Optional[CorsResult] = None
    robots: Optional[RobotsTxtResult] = None

    # Active results
    active_scans: list[ActiveScanResult] = field(default_factory=list)

    error: Optional[str] = None

    @property
    def missing_security_headers(self) -> list[SecurityHeaderResult]:
        return [h for h in self.security_headers if not h.present]

    @property
    def high_priority_missing(self) -> list[SecurityHeaderResult]:
        return [h for h in self.missing_security_headers if h.criticality == "high"]

    def summary(self) -> str:
        if self.error:
            return f"[web_enum] ERROR: {self.error}"

        duration = ""
        if self.completed_at:
            secs = int((self.completed_at - self.started_at).total_seconds())
            duration = f" ({secs}s)"

        lines = [
            f"[web_enum] {self.target_url}{duration}",
            f"  Final URL      : {self.final_url or self.target_url}",
            f"  Status         : {self.status_code}",
            f"  Server         : {self.server_banner or 'not disclosed'}",
        ]

        if self.disclosure_headers:
            lines.append(f"  Tech disclosure: {', '.join(f'{k}: {v}' for k, v in self.disclosure_headers.items())}")

        # Security headers
        missing_high = self.high_priority_missing
        if missing_high:
            lines.append(f"\n  ⚠  Missing HIGH security headers ({len(missing_high)}):")
            for h in missing_high:
                lines.append(f"    - {h.name} ({h.description})")
        present_count = len([h for h in self.security_headers if h.present])
        lines.append(f"  Security headers: {present_count}/{len(self.security_headers)} present")

        # TLS
        if self.tls:
            if not self.tls.valid:
                lines.append(f"  TLS            : ERROR — {self.tls.error}")
            else:
                expiry_note = ""
                if self.tls.is_expired:
                    expiry_note = " [EXPIRED]"
                elif self.tls.expiry_warning:
                    expiry_note = f" [EXPIRES IN {self.tls.days_until_expiry}d]"
                lines.append(
                    f"  TLS            : {self.tls.protocol_version} | "
                    f"Expires: {self.tls.days_until_expiry}d{expiry_note} | "
                    f"Issuer: {self.tls.issuer}"
                )

        # CORS
        if self.cors and self.cors.misconfigured:
            lines.append(f"  ⚠  CORS misconfiguration: {self.cors.details}")

        # Robots
        if self.robots and self.robots.found:
            lines.append(
                f"  robots.txt     : {len(self.robots.disallowed_paths)} disallowed paths, "
                f"{len(self.robots.sitemaps)} sitemap(s)"
            )

        # Active scans
        for scan in self.active_scans:
            if scan.error:
                lines.append(f"  [{scan.tool}] ERROR: {scan.error}")
            else:
                lines.append(f"  [{scan.tool}] {len(scan.findings)} findings")
                for finding in scan.findings[:5]:
                    lines.append(f"    - {finding}")
                if len(scan.findings) > 5:
                    lines.append(f"    ... +{len(scan.findings) - 5} more")

        return "\n".join(lines)


# ----------------------------------------------------------------
# PASSIVE CHECK FUNCTIONS
# ----------------------------------------------------------------

def _check_security_headers(headers: requests.structures.CaseInsensitiveDict) -> list[SecurityHeaderResult]:
    results = []
    for name, description, criticality in _SECURITY_HEADERS:
        value = headers.get(name, "")
        results.append(SecurityHeaderResult(
            name=name,
            present=bool(value),
            value=value,
            criticality=criticality,
            description=description,
        ))
    return results


def _check_disclosure_headers(headers: requests.structures.CaseInsensitiveDict) -> dict[str, str]:
    found = {}
    for header in _DISCLOSURE_HEADERS:
        value = headers.get(header, "")
        if value:
            found[header] = value
    return found


def _check_tls(hostname: str, port: int = 443) -> TlsResult:
    try:
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(
            socket.create_connection((hostname, port), timeout=REQUEST_TIMEOUT),
            server_hostname=hostname,
        ) as sock:
            cert = sock.getpeercert()
            protocol = sock.version() or ""

        # Parse expiry
        not_after_str = cert.get("notAfter", "")
        expires = None
        days_left = None
        if not_after_str:
            expires = datetime.strptime(not_after_str, "%b %d %H:%M:%S %Y %Z").replace(
                tzinfo=timezone.utc
            )
            days_left = (expires - datetime.now(timezone.utc)).days

        # Subject / Issuer
        subject = dict(x[0] for x in cert.get("subject", []))
        issuer = dict(x[0] for x in cert.get("issuer", []))

        # SANs
        san_list = [
            value for rtype, value in cert.get("subjectAltName", []) if rtype == "DNS"
        ]

        return TlsResult(
            valid=True,
            subject=subject.get("commonName", ""),
            issuer=issuer.get("organizationName", issuer.get("commonName", "")),
            expires=expires,
            days_until_expiry=days_left,
            san_domains=san_list,
            protocol_version=protocol,
        )
    except ssl.SSLError as e:
        return TlsResult(valid=False, error=f"SSL error: {e}")
    except (socket.timeout, ConnectionRefusedError, OSError) as e:
        return TlsResult(valid=False, error=f"Connection error: {e}")


def _check_cors(url: str, session: requests.Session) -> CorsResult:
    """Send an OPTIONS request with a crafted Origin to test CORS policy."""
    try:
        resp = session.options(
            url,
            headers={"Origin": "https://evil.example.com", "Access-Control-Request-Method": "GET"},
            timeout=REQUEST_TIMEOUT,
            allow_redirects=False,
        )
        allow_origin = resp.headers.get("Access-Control-Allow-Origin", "")
        allow_creds = resp.headers.get("Access-Control-Allow-Credentials", "")

        misconfigured = False
        details = ""

        if allow_origin == "*" and allow_creds.lower() == "true":
            misconfigured = True
            details = "ACAO: * with ACAC: true — credentials leak possible"
        elif allow_origin == "https://evil.example.com":
            misconfigured = True
            details = "Reflects arbitrary Origin — CORS bypass possible"
        elif allow_origin == "null":
            misconfigured = True
            details = "ACAO: null — may be exploitable from sandboxed contexts"

        return CorsResult(
            allow_origin=allow_origin,
            allow_credentials=allow_creds,
            misconfigured=misconfigured,
            details=details,
        )
    except requests.RequestException:
        return CorsResult()


def _check_robots(base_url: str, session: requests.Session) -> RobotsTxtResult:
    parsed = urlparse(base_url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
    try:
        resp = session.get(robots_url, timeout=REQUEST_TIMEOUT)
        if resp.status_code != 200:
            return RobotsTxtResult(found=False)

        raw = resp.text
        disallowed = []
        sitemaps = []
        for line in raw.splitlines():
            line = line.strip()
            if line.lower().startswith("disallow:"):
                path = line.split(":", 1)[1].strip()
                if path:
                    disallowed.append(path)
            elif line.lower().startswith("sitemap:"):
                sm = line.split(":", 1)[1].strip()
                if sm:
                    sitemaps.append(sm)

        return RobotsTxtResult(
            found=True,
            disallowed_paths=disallowed,
            sitemaps=sitemaps,
            raw=raw,
        )
    except requests.RequestException:
        return RobotsTxtResult(found=False)


# ----------------------------------------------------------------
# ENUMERATOR CLASS
# ----------------------------------------------------------------

class WebEnumerator:
    """
    Web application enumerator combining passive analysis and active tools.

    Args:
        hexstrike_client: Optional HexStrikeClient for active scans.
                          If None, active scans are skipped.
        user_agent: HTTP User-Agent for requests.
    """

    DEFAULT_UA = (
        "Mozilla/5.0 (X11; Linux x86_64; rv:125.0) Gecko/20100101 Firefox/125.0"
    )

    def __init__(
        self,
        hexstrike_client=None,
        user_agent: str = DEFAULT_UA,
    ) -> None:
        self.hexstrike = hexstrike_client
        self.user_agent = user_agent

    @classmethod
    def from_config(cls) -> "WebEnumerator":
        """Create enumerator loading hexstrike config from config.yaml."""
        try:
            from mcp.hexstrike_client import HexStrikeClient
            return cls(hexstrike_client=HexStrikeClient())
        except Exception:
            logger.warning("hexstrike-ai unavailable — passive-only mode")
            return cls()

    def passive_scan(self, url: str) -> WebEnumResult:
        """
        Passive web enumeration: headers, TLS, CORS, robots.txt.
        No authorization required — only makes standard HTTP requests.

        Args:
            url: Target URL (e.g., https://target.com)

        Returns:
            WebEnumResult with passive findings.
        """
        started_at = datetime.now()
        parsed = urlparse(url)
        result = WebEnumResult(target_url=url, started_at=started_at)

        session = requests.Session()
        session.headers.update({"User-Agent": self.user_agent})

        try:
            resp = session.get(url, timeout=REQUEST_TIMEOUT, allow_redirects=True)
            result.final_url = resp.url
            result.status_code = resp.status_code
            result.server_banner = resp.headers.get("Server", "")
            result.security_headers = _check_security_headers(resp.headers)
            result.disclosure_headers = _check_disclosure_headers(resp.headers)
        except requests.RequestException as e:
            result.error = f"HTTP request failed: {e}"
            result.completed_at = datetime.now()
            return result

        # TLS check (only for HTTPS)
        if parsed.scheme == "https":
            port = parsed.port or 443
            result.tls = _check_tls(parsed.hostname or "", port)

        # CORS check
        result.cors = _check_cors(url, session)

        # robots.txt
        result.robots = _check_robots(url, session)

        result.completed_at = datetime.now()
        return result

    def full_scan(
        self,
        url: str,
        authorization_confirmed: bool = False,
        require_vpn: bool = True,
    ) -> WebEnumResult:
        """
        Full enumeration: passive + active (directory bruteforce, CMS, fingerprint).

        Args:
            url: Target URL.
            authorization_confirmed: Must be True for active scans.
            require_vpn: If True, verifies VPN before active scans.

        Returns:
            WebEnumResult with passive + active findings.
        """
        # Always run passive first
        result = self.passive_scan(url)
        if result.error:
            return result

        if not authorization_confirmed:
            logger.warning(
                "Active scans skipped — authorization_confirmed=False. "
                "Returning passive results only."
            )
            return result

        # OPSEC gate for active scans
        from scripts.opsec.vpn_check import verify_opsec
        opsec = verify_opsec(require_vpn=require_vpn)
        if not opsec.safe:
            result.active_scans.append(ActiveScanResult(
                tool="opsec",
                error=f"OPSEC check failed: {opsec.reason}",
            ))
            result.completed_at = datetime.now()
            return result

        # Active scans via hexstrike-ai
        if self.hexstrike and self.hexstrike.is_reachable():
            self._run_dir_bruteforce(url, result)
            self._run_cms_detection(url, result)
            self._run_tech_fingerprint(url, result)
        else:
            logger.warning("hexstrike-ai not reachable — active scans skipped")

        result.completed_at = datetime.now()
        return result

    def _run_dir_bruteforce(self, url: str, result: WebEnumResult) -> None:
        try:
            raw = self.hexstrike.run_tool("gobuster", {
                "target": url,
                "wordlist": "/usr/share/wordlists/dirb/common.txt",
                "mode": "dir",
                "extensions": "php,html,txt,js",
            })
            findings = raw.get("found_paths", raw.get("output", "").splitlines())
            result.active_scans.append(ActiveScanResult(
                tool="gobuster",
                findings=[str(f) for f in findings],
                raw_output=str(raw),
            ))
        except Exception as e:
            result.active_scans.append(ActiveScanResult(tool="gobuster", error=str(e)))

    def _run_cms_detection(self, url: str, result: WebEnumResult) -> None:
        try:
            raw = self.hexstrike.run_agent(
                "decision_engine",
                f"Detect CMS platform on {url} — WordPress, Joomla, Drupal, etc.",
                context={"target": url, "type": "cms_detection"},
            )
            findings = raw.get("findings", [raw.get("result", "")])
            result.active_scans.append(ActiveScanResult(
                tool="cms_detect",
                findings=[str(f) for f in findings if f],
                raw_output=str(raw),
            ))
        except Exception as e:
            result.active_scans.append(ActiveScanResult(tool="cms_detect", error=str(e)))

    def _run_tech_fingerprint(self, url: str, result: WebEnumResult) -> None:
        try:
            raw = self.hexstrike.run_tool("whatweb", {"target": url})
            findings = raw.get("technologies", raw.get("output", "").splitlines())
            result.active_scans.append(ActiveScanResult(
                tool="whatweb",
                findings=[str(f) for f in findings if f],
                raw_output=str(raw),
            ))
        except Exception as e:
            result.active_scans.append(ActiveScanResult(tool="whatweb", error=str(e)))


# ----------------------------------------------------------------
# CLI ENTRY POINT
# ----------------------------------------------------------------

def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(
        description="web_enum — Web application enumeration for Ascended33",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Passive only (safe — just HTTP requests)
  python3 scripts/recon/web_enum.py --url https://target.com

  # Full scan with active tools (requires --authorized)
  python3 scripts/recon/web_enum.py --url https://target.com --authorized
        """,
    )
    parser.add_argument("--url", required=True, help="Target URL (https://...)")
    parser.add_argument("--authorized", action="store_true",
                        help="Confirm target in authorized scope (enables active scans)")
    parser.add_argument("--passive-only", action="store_true",
                        help="Force passive mode only, skip active tools")
    parser.add_argument("--no-vpn", action="store_true",
                        help="Skip VPN requirement for active scans")
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s: %(message)s",
    )

    enum = WebEnumerator.from_config()

    if args.passive_only or not args.authorized:
        if not args.passive_only and not args.authorized:
            print("[web_enum] No --authorized flag — running passive scan only.")
        result = enum.passive_scan(args.url)
    else:
        result = enum.full_scan(
            args.url,
            authorization_confirmed=True,
            require_vpn=not args.no_vpn,
        )

    print(result.summary())
    return 0 if not result.error else 1


if __name__ == "__main__":
    sys.exit(main())
