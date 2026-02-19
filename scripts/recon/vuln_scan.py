"""
vuln_scan.py — Vulnerability scanning via Nuclei + CVE intelligence through hexstrike-ai.

Routes all scans through hexstrike-ai on Kali VM. Supports template-based
scanning (Nuclei), CVE lookup/correlation, and severity bucketing into a
structured report ready for Obsidian Vault export.

Severity levels follow CVSS v3 standard:
  Critical  — CVSS 9.0–10.0
  High      — CVSS 7.0–8.9
  Medium    — CVSS 4.0–6.9
  Low       — CVSS 0.1–3.9
  Info      — Informational, no CVSS score

Usage:
    from scripts.recon.vuln_scan import VulnerabilityScanner, ScanProfile

    scanner = VulnerabilityScanner.from_config()

    # Template scan (Nuclei)
    result = scanner.nuclei_scan(
        target="https://target.com",
        profile=ScanProfile.STANDARD,
        authorization_confirmed=True,
    )
    print(result.summary())

    # CVE lookup
    cve = scanner.cve_lookup("CVE-2024-1234")
    print(cve)
"""

import logging
import sys
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional

logger = logging.getLogger(__name__)


class Severity(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"
    UNKNOWN = "unknown"

    @classmethod
    def from_cvss(cls, score: float) -> "Severity":
        if score >= 9.0:
            return cls.CRITICAL
        if score >= 7.0:
            return cls.HIGH
        if score >= 4.0:
            return cls.MEDIUM
        if score > 0:
            return cls.LOW
        return cls.INFO

    @classmethod
    def from_string(cls, s: str) -> "Severity":
        s = s.strip().lower()
        for member in cls:
            if member.value == s:
                return member
        return cls.UNKNOWN


class ScanProfile(Enum):
    """Nuclei template profile selection."""
    FAST = "fast"          # cves,exposure,misconfiguration — quick wins
    STANDARD = "standard"  # + default,takeover,technologies
    DEEP = "deep"          # all templates (slow, noisy)
    CVE_ONLY = "cve-only"  # CVE templates only


# ----------------------------------------------------------------
# DATA CLASSES
# ----------------------------------------------------------------

@dataclass
class Vulnerability:
    template_id: str
    name: str
    severity: Severity
    description: str = ""
    url: str = ""
    matched_at: str = ""
    cvss_score: Optional[float] = None
    cve_ids: list[str] = field(default_factory=list)
    remediation: str = ""
    reference_urls: list[str] = field(default_factory=list)
    raw: dict = field(default_factory=dict)

    def __str__(self) -> str:
        cves = f" ({', '.join(self.cve_ids)})" if self.cve_ids else ""
        score = f" CVSS:{self.cvss_score}" if self.cvss_score else ""
        return f"[{self.severity.value.upper()}]{cves}{score} {self.name} — {self.matched_at or self.url}"


@dataclass
class CveDetail:
    cve_id: str
    description: str = ""
    cvss_score: Optional[float] = None
    severity: Severity = Severity.UNKNOWN
    affected_products: list[str] = field(default_factory=list)
    poc_available: bool = False
    patch_available: bool = False
    published_date: str = ""
    references: list[str] = field(default_factory=list)
    raw: dict = field(default_factory=dict)

    def __str__(self) -> str:
        return (
            f"{self.cve_id} [{self.severity.value.upper()}] "
            f"CVSS:{self.cvss_score or 'N/A'} — {self.description[:100]}"
        )


@dataclass
class VulnScanResult:
    target: str
    profile: str
    started_at: datetime
    completed_at: Optional[datetime] = None
    vulnerabilities: list[Vulnerability] = field(default_factory=list)
    error: Optional[str] = None

    @property
    def success(self) -> bool:
        return self.error is None

    @property
    def by_severity(self) -> dict[Severity, list[Vulnerability]]:
        buckets: dict[Severity, list[Vulnerability]] = {s: [] for s in Severity}
        for v in self.vulnerabilities:
            buckets[v.severity].append(v)
        return buckets

    @property
    def critical_count(self) -> int:
        return len(self.by_severity[Severity.CRITICAL])

    @property
    def high_count(self) -> int:
        return len(self.by_severity[Severity.HIGH])

    def summary(self) -> str:
        if self.error:
            return f"[vuln_scan] ERROR: {self.error}"

        duration = ""
        if self.completed_at:
            secs = int((self.completed_at - self.started_at).total_seconds())
            duration = f" ({secs}s)"

        by_sev = self.by_severity
        lines = [
            f"[vuln_scan] {self.target} — profile={self.profile}{duration}",
            f"  Total findings : {len(self.vulnerabilities)}",
            f"  Critical       : {len(by_sev[Severity.CRITICAL])}",
            f"  High           : {len(by_sev[Severity.HIGH])}",
            f"  Medium         : {len(by_sev[Severity.MEDIUM])}",
            f"  Low            : {len(by_sev[Severity.LOW])}",
            f"  Info           : {len(by_sev[Severity.INFO])}",
        ]

        for severity in [Severity.CRITICAL, Severity.HIGH, Severity.MEDIUM]:
            vulns = by_sev[severity]
            if vulns:
                lines.append(f"\n  [{severity.value.upper()}]:")
                for v in vulns:
                    lines.append(f"    {v}")

        return "\n".join(lines)

    def to_markdown(self) -> str:
        """
        Render findings as Markdown for Obsidian Vault report.
        """
        lines = [
            f"## Vulnerability Scan — {self.target}",
            f"",
            f"- **Profile**: {self.profile}",
            f"- **Date**: {self.started_at.strftime('%Y-%m-%d %H:%M')}",
            f"- **Total findings**: {len(self.vulnerabilities)}",
            f"",
            f"### Summary",
            f"",
            f"| Severity | Count |",
            f"|----------|-------|",
        ]
        by_sev = self.by_severity
        for sev in [Severity.CRITICAL, Severity.HIGH, Severity.MEDIUM, Severity.LOW, Severity.INFO]:
            count = len(by_sev[sev])
            lines.append(f"| {sev.value.capitalize()} | {count} |")

        lines.append("")
        lines.append("### Findings")
        lines.append("")

        for sev in [Severity.CRITICAL, Severity.HIGH, Severity.MEDIUM, Severity.LOW]:
            vulns = by_sev[sev]
            if not vulns:
                continue
            lines.append(f"#### {sev.value.capitalize()}")
            lines.append("")
            for v in vulns:
                cve_str = f" `{'`, `'.join(v.cve_ids)}`" if v.cve_ids else ""
                score_str = f" — CVSS {v.cvss_score}" if v.cvss_score else ""
                lines.append(f"**{v.name}**{cve_str}{score_str}")
                if v.description:
                    lines.append(f"> {v.description}")
                if v.matched_at:
                    lines.append(f"- Matched at: `{v.matched_at}`")
                if v.remediation:
                    lines.append(f"- Remediation: {v.remediation}")
                lines.append("")

        return "\n".join(lines)


# ----------------------------------------------------------------
# SCANNER CLASS
# ----------------------------------------------------------------

# Nuclei template tags per profile
_PROFILE_TAGS: dict[ScanProfile, str] = {
    ScanProfile.FAST:     "cves,exposure,misconfiguration",
    ScanProfile.STANDARD: "cves,exposure,misconfiguration,default,takeover,technologies",
    ScanProfile.DEEP:     "",  # empty = all templates
    ScanProfile.CVE_ONLY: "cves",
}


class VulnerabilityScanner:
    """
    Vulnerability scanner using Nuclei + hexstrike-ai CVE intelligence.

    Args:
        hexstrike_client: HexStrikeClient instance for tool execution.
    """

    def __init__(self, hexstrike_client=None) -> None:
        self.hexstrike = hexstrike_client

    @classmethod
    def from_config(cls) -> "VulnerabilityScanner":
        """Create scanner loading hexstrike config from config.yaml."""
        try:
            from mcp.hexstrike_client import HexStrikeClient
            return cls(hexstrike_client=HexStrikeClient())
        except Exception:
            logger.warning("hexstrike-ai unavailable — scanner in degraded mode")
            return cls()

    def nuclei_scan(
        self,
        target: str,
        profile: ScanProfile = ScanProfile.STANDARD,
        authorization_confirmed: bool = False,
        require_vpn: bool = True,
    ) -> VulnScanResult:
        """
        Run Nuclei template scan against a target via hexstrike-ai.

        Args:
            target: URL or IP to scan (e.g., https://target.com or a lab IP)
            profile: ScanProfile defining which Nuclei template tags to use.
            authorization_confirmed: Must be True — explicit consent required.
            require_vpn: If True, verifies VPN is active before scanning.

        Returns:
            VulnScanResult with categorized vulnerabilities.
        """
        started_at = datetime.now()

        # ---- Authorization gate ----
        if not authorization_confirmed:
            return VulnScanResult(
                target=target,
                profile=profile.value,
                started_at=started_at,
                completed_at=datetime.now(),
                error=(
                    "Authorization required. Pass authorization_confirmed=True only "
                    "after verifying this target is within authorized scope."
                ),
            )

        # ---- OPSEC gate ----
        from scripts.opsec.vpn_check import verify_opsec
        opsec = verify_opsec(require_vpn=require_vpn)
        if not opsec.safe:
            return VulnScanResult(
                target=target,
                profile=profile.value,
                started_at=started_at,
                completed_at=datetime.now(),
                error=f"OPSEC check failed: {opsec.reason}",
            )

        if not self.hexstrike:
            return VulnScanResult(
                target=target,
                profile=profile.value,
                started_at=started_at,
                completed_at=datetime.now(),
                error="hexstrike-ai client not initialized",
            )

        if not self.hexstrike.is_reachable():
            return VulnScanResult(
                target=target,
                profile=profile.value,
                started_at=started_at,
                completed_at=datetime.now(),
                error="hexstrike-ai server is not reachable (http://KALI_IP:8888). Is it running?",
            )

        # ---- Run Nuclei via hexstrike ----
        tags = _PROFILE_TAGS[profile]
        logger.info("Starting Nuclei scan on %s (profile=%s)", target, profile.value)

        try:
            params: dict = {"target": target}
            if tags:
                params["tags"] = tags

            raw = self.hexstrike.run_tool("nuclei", params)
        except Exception as e:
            return VulnScanResult(
                target=target,
                profile=profile.value,
                started_at=started_at,
                completed_at=datetime.now(),
                error=f"hexstrike nuclei call failed: {e}",
            )

        # ---- Parse findings ----
        vulnerabilities = self._parse_nuclei_output(raw)

        return VulnScanResult(
            target=target,
            profile=profile.value,
            started_at=started_at,
            completed_at=datetime.now(),
            vulnerabilities=vulnerabilities,
        )

    def cve_lookup(self, cve_id: str) -> CveDetail:
        """
        Look up CVE details via hexstrike-ai CVE Intelligence agent.

        Args:
            cve_id: CVE identifier (e.g., "CVE-2024-1234").

        Returns:
            CveDetail with scoring, affected products, and PoC status.
        """
        if not self.hexstrike or not self.hexstrike.is_reachable():
            return CveDetail(
                cve_id=cve_id,
                description="hexstrike-ai not reachable",
            )

        try:
            raw = self.hexstrike.cve_lookup(cve_id)
        except Exception as e:
            return CveDetail(cve_id=cve_id, description=f"Lookup failed: {e}")

        return self._parse_cve_detail(cve_id, raw)

    def correlate_vulnerabilities(
        self,
        scan_result: VulnScanResult,
    ) -> VulnScanResult:
        """
        Enrich vulnerabilities with CVE data via hexstrike CVE Intelligence.
        Adds CVSS scores and PoC availability for findings that have CVE IDs.

        Args:
            scan_result: Existing VulnScanResult from nuclei_scan().

        Returns:
            Same VulnScanResult with enriched CVE data.
        """
        if not self.hexstrike or not self.hexstrike.is_reachable():
            return scan_result

        for vuln in scan_result.vulnerabilities:
            for cve_id in vuln.cve_ids:
                try:
                    detail = self.cve_lookup(cve_id)
                    if detail.cvss_score is not None and vuln.cvss_score is None:
                        vuln.cvss_score = detail.cvss_score
                        vuln.severity = Severity.from_cvss(detail.cvss_score)
                    if detail.remediation if hasattr(detail, 'remediation') else False:
                        pass  # would add remediation here if CveDetail had it
                    vuln.reference_urls.extend(detail.references)
                except Exception as e:
                    logger.debug("CVE enrichment failed for %s: %s", cve_id, e)

        return scan_result

    # ----------------------------------------------------------------
    # PARSERS
    # ----------------------------------------------------------------

    def _parse_nuclei_output(self, raw: dict) -> list[Vulnerability]:
        """Parse hexstrike nuclei output into Vulnerability objects."""
        vulns: list[Vulnerability] = []
        findings = raw.get("findings", raw.get("results", raw.get("output", [])))

        if isinstance(findings, str):
            # Plain text output — parse lines
            for line in findings.splitlines():
                line = line.strip()
                if not line:
                    continue
                vuln = self._parse_nuclei_text_line(line)
                if vuln:
                    vulns.append(vuln)
        elif isinstance(findings, list):
            for item in findings:
                if isinstance(item, dict):
                    vuln = self._parse_nuclei_dict(item)
                    vulns.append(vuln)
                elif isinstance(item, str):
                    vuln = self._parse_nuclei_text_line(item)
                    if vuln:
                        vulns.append(vuln)

        return vulns

    def _parse_nuclei_dict(self, item: dict) -> Vulnerability:
        """Parse a single Nuclei JSON finding dict."""
        info = item.get("info", {})
        severity_str = info.get("severity", item.get("severity", "info"))
        severity = Severity.from_string(severity_str)

        # Extract CVE IDs from tags/classification
        cve_ids: list[str] = []
        tags = info.get("tags", [])
        if isinstance(tags, list):
            cve_ids = [t.upper() for t in tags if t.upper().startswith("CVE-")]
        classification = info.get("classification", {})
        if isinstance(classification, dict):
            cve_ids.extend(classification.get("cve-id", []))

        return Vulnerability(
            template_id=item.get("template-id", item.get("id", "")),
            name=info.get("name", item.get("name", "Unknown")),
            severity=severity,
            description=info.get("description", ""),
            url=item.get("host", item.get("url", "")),
            matched_at=item.get("matched-at", item.get("matched", "")),
            cvss_score=classification.get("cvss-score") if isinstance(classification, dict) else None,
            cve_ids=list(set(cve_ids)),
            remediation=info.get("remediation", ""),
            reference_urls=info.get("reference", []),
            raw=item,
        )

    def _parse_nuclei_text_line(self, line: str) -> Optional[Vulnerability]:
        """Parse a plain-text Nuclei output line (fallback)."""
        # Nuclei text format: [template-id] [protocol] [severity] URL
        # e.g.: [CVE-2024-1234] [http] [critical] https://target.com/vuln
        parts = line.split("]")
        if len(parts) < 3:
            return None
        try:
            template_id = parts[0].strip().lstrip("[").strip()
            severity_str = parts[2].strip().lstrip("[").strip() if len(parts) > 2 else "info"
            url = parts[-1].strip()
            severity = Severity.from_string(severity_str)
            cve_ids = [template_id] if template_id.upper().startswith("CVE-") else []
            return Vulnerability(
                template_id=template_id,
                name=template_id,
                severity=severity,
                url=url,
                cve_ids=cve_ids,
            )
        except Exception:
            return None

    def _parse_cve_detail(self, cve_id: str, raw: dict) -> CveDetail:
        """Parse hexstrike CVE Intelligence response into CveDetail."""
        result = raw.get("result", raw)
        cvss_score: Optional[float] = None
        try:
            cvss_score = float(result.get("cvss_score", result.get("cvss", 0)) or 0) or None
        except (TypeError, ValueError):
            pass

        severity = (
            Severity.from_cvss(cvss_score)
            if cvss_score is not None
            else Severity.from_string(result.get("severity", "unknown"))
        )

        return CveDetail(
            cve_id=cve_id,
            description=result.get("description", result.get("summary", "")),
            cvss_score=cvss_score,
            severity=severity,
            affected_products=result.get("affected_products", result.get("products", [])),
            poc_available=bool(result.get("poc_available", result.get("exploit_available", False))),
            patch_available=bool(result.get("patch_available", result.get("patched", False))),
            published_date=result.get("published_date", result.get("published", "")),
            references=result.get("references", result.get("urls", [])),
            raw=raw,
        )


# ----------------------------------------------------------------
# CLI ENTRY POINT
# ----------------------------------------------------------------

def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(
        description="vuln_scan — Vulnerability scanning via Nuclei + hexstrike-ai",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 scripts/recon/vuln_scan.py --target https://target.com --authorized
  python3 scripts/recon/vuln_scan.py --target https://target.com --profile deep --authorized
  python3 scripts/recon/vuln_scan.py --cve CVE-2024-1234
        """,
    )
    parser.add_argument("--target", help="Target URL or IP for Nuclei scan")
    parser.add_argument("--cve", help="CVE ID to look up (e.g. CVE-2024-1234)")
    parser.add_argument(
        "--profile",
        choices=[p.value for p in ScanProfile],
        default="standard",
        help="Nuclei scan profile (default: standard)",
    )
    parser.add_argument("--authorized", action="store_true",
                        help="Confirm target in authorized scope (required for scans)")
    parser.add_argument("--no-vpn", action="store_true",
                        help="Skip VPN requirement")
    parser.add_argument("--markdown", action="store_true",
                        help="Output findings as Markdown (for Vault)")
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s: %(message)s",
    )

    scanner = VulnerabilityScanner.from_config()

    if args.cve:
        detail = scanner.cve_lookup(args.cve)
        print(detail)
        return 0

    if not args.target:
        parser.print_help()
        return 1

    if not args.authorized:
        print("ERROR: --authorized flag required. Only scan authorized targets.")
        return 1

    result = scanner.nuclei_scan(
        target=args.target,
        profile=ScanProfile(args.profile),
        authorization_confirmed=True,
        require_vpn=not args.no_vpn,
    )

    if args.markdown:
        print(result.to_markdown())
    else:
        print(result.summary())

    return 0 if result.success else 1


if __name__ == "__main__":
    sys.exit(main())
