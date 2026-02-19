"""
domain_recon.py — Passive domain reconnaissance module.

Performs fully passive recon against a domain using only public APIs and
DNS queries. No active scanning, no direct target interaction beyond DNS.

Sources used:
  - DNS records (A, MX, NS, TXT, CNAME) via dnspython
  - WHOIS registration data via python-whois
  - Certificate Transparency logs via crt.sh (free, no auth)
  - Wayback Machine CDX API for historical URLs
  - IPinfo.io for IP geolocation (free tier)

Usage:
    from scripts.osint.domain_recon import DomainRecon

    recon = DomainRecon("example.com")
    results = recon.run_all()
    print(results.summary())
"""

import json
import logging
import socket
from dataclasses import dataclass, field
from datetime import datetime

import requests

logger = logging.getLogger(__name__)

CRTSH_URL = "https://crt.sh/?q={domain}&output=json"
WAYBACK_CDX_URL = (
    "http://web.archive.org/cdx/search/cdx"
    "?url=*.{domain}&output=json&fl=original&collapse=urlkey&limit=50"
)
IPINFO_URL = "https://ipinfo.io/{ip}/json"
REQUEST_TIMEOUT = 15


# ── Data containers ──────────────────────────────────────────────────────────

@dataclass
class DNSResults:
    a_records: list[str] = field(default_factory=list)
    mx_records: list[str] = field(default_factory=list)
    ns_records: list[str] = field(default_factory=list)
    txt_records: list[str] = field(default_factory=list)
    cname_records: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


@dataclass
class WhoisData:
    registrar: str = ""
    creation_date: str = ""
    expiration_date: str = ""
    name_servers: list[str] = field(default_factory=list)
    emails: list[str] = field(default_factory=list)
    org: str = ""
    country: str = ""
    raw_text: str = ""
    error: str = ""


@dataclass
class SubdomainEntry:
    name: str
    common_name: str
    issuer: str
    logged_at: str


@dataclass
class IPInfo:
    ip: str
    hostname: str = ""
    city: str = ""
    region: str = ""
    country: str = ""
    org: str = ""
    asn: str = ""


@dataclass
class ReconResults:
    domain: str
    timestamp: str
    dns: DNSResults = field(default_factory=DNSResults)
    whois: WhoisData = field(default_factory=WhoisData)
    subdomains: list[SubdomainEntry] = field(default_factory=list)
    wayback_urls: list[str] = field(default_factory=list)
    ip_info: list[IPInfo] = field(default_factory=list)

    def summary(self) -> str:
        lines = [
            f"# Domain Recon: {self.domain}",
            f"Timestamp: {self.timestamp}",
            "",
            "## DNS",
            f"  A records:   {', '.join(self.dns.a_records) or 'none'}",
            f"  MX records:  {', '.join(self.dns.mx_records) or 'none'}",
            f"  NS records:  {', '.join(self.dns.ns_records) or 'none'}",
            f"  TXT records: {len(self.dns.txt_records)} found",
            "",
            "## WHOIS",
            f"  Registrar:  {self.whois.registrar}",
            f"  Created:    {self.whois.creation_date}",
            f"  Expires:    {self.whois.expiration_date}",
            f"  Org:        {self.whois.org}",
            f"  Country:    {self.whois.country}",
            "",
            f"## Subdomains (crt.sh): {len(self.subdomains)} found",
            *[f"  - {s.name}" for s in self.subdomains[:20]],
            "",
            f"## Wayback Machine URLs: {len(self.wayback_urls)} found",
            "",
            f"## IP Info: {len(self.ip_info)} IPs resolved",
            *[f"  - {ip.ip} | {ip.org} | {ip.city}, {ip.country}" for ip in self.ip_info],
        ]
        return "\n".join(lines)

    def to_dict(self) -> dict:
        return {
            "domain": self.domain,
            "timestamp": self.timestamp,
            "dns": {
                "a": self.dns.a_records,
                "mx": self.dns.mx_records,
                "ns": self.dns.ns_records,
                "txt": self.dns.txt_records,
                "cname": self.dns.cname_records,
            },
            "whois": {
                "registrar": self.whois.registrar,
                "created": self.whois.creation_date,
                "expires": self.whois.expiration_date,
                "org": self.whois.org,
                "country": self.whois.country,
                "emails": self.whois.emails,
            },
            "subdomains": [s.name for s in self.subdomains],
            "wayback_urls": self.wayback_urls,
            "ip_info": [
                {"ip": i.ip, "org": i.org, "city": i.city, "country": i.country}
                for i in self.ip_info
            ],
        }


# ── DomainRecon class ─────────────────────────────────────────────────────────

class DomainRecon:
    """Passive domain reconnaissance aggregator."""

    def __init__(self, domain: str):
        self.domain = domain.lower().strip().removeprefix("https://").removeprefix("http://").rstrip("/")

    # ── DNS ──────────────────────────────────────────────────────────────────

    def get_dns(self) -> DNSResults:
        """Resolve common DNS record types for the domain."""
        results = DNSResults()
        try:
            import dns.resolver  # dnspython
        except ImportError:
            results.errors.append("dnspython not installed — run: pip install dnspython")
            logger.warning("dnspython not available, falling back to socket for A records")
            try:
                results.a_records = [r[4][0] for r in socket.getaddrinfo(self.domain, None)]
            except Exception:
                pass
            return results

        resolver = dns.resolver.Resolver()
        resolver.timeout = 5
        resolver.lifetime = 10

        record_map = {
            "A": results.a_records,
            "MX": results.mx_records,
            "NS": results.ns_records,
            "CNAME": results.cname_records,
        }

        for rtype, target in record_map.items():
            try:
                answers = resolver.resolve(self.domain, rtype)
                for rdata in answers:
                    target.append(str(rdata).rstrip("."))
            except Exception:
                pass

        try:
            txt_answers = resolver.resolve(self.domain, "TXT")
            results.txt_records = [str(r) for r in txt_answers]
        except Exception:
            pass

        logger.info("DNS: %d A, %d MX, %d NS records for %s",
                    len(results.a_records), len(results.mx_records),
                    len(results.ns_records), self.domain)
        return results

    # ── WHOIS ─────────────────────────────────────────────────────────────────

    def get_whois(self) -> WhoisData:
        """Query WHOIS registration data."""
        data = WhoisData()
        try:
            import whois as python_whois
            w = python_whois.whois(self.domain)

            def _str(val) -> str:
                if isinstance(val, list):
                    return str(val[0]) if val else ""
                return str(val) if val else ""

            def _date(val) -> str:
                if isinstance(val, list):
                    val = val[0]
                if hasattr(val, "strftime"):
                    return val.strftime("%Y-%m-%d")
                return str(val) if val else ""

            data.registrar = _str(w.registrar)
            data.creation_date = _date(w.creation_date)
            data.expiration_date = _date(w.expiration_date)
            data.org = _str(w.org)
            data.country = _str(w.country)
            data.emails = list(set(w.emails)) if isinstance(w.emails, list) else ([w.emails] if w.emails else [])
            data.name_servers = [ns.lower() for ns in (w.name_servers or [])]
            data.raw_text = str(w.text or "")
        except ImportError:
            data.error = "python-whois not installed — run: pip install python-whois"
        except Exception as e:
            data.error = str(e)
            logger.warning("WHOIS error for %s: %s", self.domain, e)

        return data

    # ── Certificate Transparency ──────────────────────────────────────────────

    def get_subdomains_crtsh(self) -> list[SubdomainEntry]:
        """
        Enumerate subdomains via Certificate Transparency logs (crt.sh).
        Fully passive — no interaction with the target.
        """
        subdomains = []
        seen = set()
        try:
            url = CRTSH_URL.format(domain=self.domain)
            response = requests.get(url, timeout=REQUEST_TIMEOUT)
            if response.status_code != 200:
                logger.warning("crt.sh returned %d for %s", response.status_code, self.domain)
                return subdomains

            entries = response.json()
            for entry in entries:
                name = entry.get("name_value", "").strip()
                for subdomain in name.split("\n"):
                    subdomain = subdomain.strip().lstrip("*.")
                    if subdomain and subdomain not in seen and self.domain in subdomain:
                        seen.add(subdomain)
                        subdomains.append(SubdomainEntry(
                            name=subdomain,
                            common_name=entry.get("common_name", ""),
                            issuer=entry.get("issuer_name", ""),
                            logged_at=entry.get("entry_timestamp", ""),
                        ))

            # Sort by name, deduplicate
            subdomains.sort(key=lambda s: s.name)
            logger.info("crt.sh: %d subdomains found for %s", len(subdomains), self.domain)
        except requests.RequestException as e:
            logger.warning("crt.sh request failed: %s", e)
        except json.JSONDecodeError:
            logger.warning("crt.sh returned non-JSON response for %s", self.domain)

        return subdomains

    # ── Wayback Machine ───────────────────────────────────────────────────────

    def get_wayback_urls(self, limit: int = 50) -> list[str]:
        """Retrieve historical URLs from the Wayback Machine CDX API."""
        try:
            url = WAYBACK_CDX_URL.format(domain=self.domain)
            response = requests.get(url, timeout=REQUEST_TIMEOUT)
            if response.status_code != 200:
                return []
            data = response.json()
            # First row is the header ["original"]
            urls = [row[0] for row in data[1:] if row] if data else []
            logger.info("Wayback: %d URLs for %s", len(urls), self.domain)
            return urls[:limit]
        except Exception as e:
            logger.warning("Wayback Machine error for %s: %s", self.domain, e)
            return []

    # ── IP Info ───────────────────────────────────────────────────────────────

    def get_ip_info(self, ips: list[str]) -> list[IPInfo]:
        """Geolocate and enrich IPs via ipinfo.io (free tier, no auth needed)."""
        results = []
        for ip in ips[:5]:  # Limit to avoid rate limiting on free tier
            try:
                response = requests.get(IPINFO_URL.format(ip=ip), timeout=REQUEST_TIMEOUT)
                if response.status_code == 200:
                    data = response.json()
                    results.append(IPInfo(
                        ip=ip,
                        hostname=data.get("hostname", ""),
                        city=data.get("city", ""),
                        region=data.get("region", ""),
                        country=data.get("country", ""),
                        org=data.get("org", ""),
                    ))
            except Exception as e:
                logger.warning("IPInfo error for %s: %s", ip, e)
        return results

    # ── Full run ──────────────────────────────────────────────────────────────

    def run_all(self) -> ReconResults:
        """Run all passive recon modules and return aggregated results."""
        logger.info("Starting passive recon on: %s", self.domain)
        results = ReconResults(
            domain=self.domain,
            timestamp=datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        )

        results.dns = self.get_dns()
        results.whois = self.get_whois()
        results.subdomains = self.get_subdomains_crtsh()
        results.wayback_urls = self.get_wayback_urls()

        if results.dns.a_records:
            results.ip_info = self.get_ip_info(results.dns.a_records)

        logger.info("Recon complete for %s", self.domain)
        return results


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    import argparse
    import sys

    parser = argparse.ArgumentParser(description="Passive domain reconnaissance")
    parser.add_argument("domain", help="Target domain (e.g., example.com)")
    parser.add_argument("--output", choices=["print", "json", "vault"], default="print")
    parser.add_argument("--report", action="store_true", help="Generate full report to Vault")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

    recon = DomainRecon(args.domain)
    results = recon.run_all()

    if args.output == "json":
        print(json.dumps(results.to_dict(), indent=2))
    elif args.output == "vault" or args.report:
        from scripts.reporting.report_generator import generate_report
        generate_report(
            "osint",
            {
                "{{target}}": args.domain,
                "{{authorization_type}}": "Passive OSINT — public data only",
                "{{opsec_level}}": "Standard",
                "{{executive_summary}}": f"Passive reconnaissance of {args.domain}.",
                "{{domain_findings}}": results.summary(),
                "{{investigation_type}}": "Domain footprinting",
                "{{data_sources}}": "DNS, WHOIS, crt.sh, Wayback Machine, IPInfo",
                "{{social_findings}}": "N/A — domain recon only",
                "{{breach_findings}}": "Not checked in this run",
                "{{darkweb_findings}}": "Not checked in this run",
                "{{other_findings}}": "",
                "{{recommendations}}": "Review subdomains for exposure. Check TXT records for SPF/DMARC policy.",
                "{{raw_sources}}": "crt.sh, web.archive.org/cdx, ipinfo.io",
                "{{tools_used}}": "domain_recon.py (DNS, WHOIS, crt.sh, Wayback, IPInfo)",
                "{{target_identifiers}}": args.domain,
                "{{methodology}}": "Fully passive — no direct target interaction beyond public DNS resolution.",
            },
            output="vault",
        )
    else:
        print(results.summary())


if __name__ == "__main__":
    main()
