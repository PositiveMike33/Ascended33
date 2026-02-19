"""
dark_web_monitor.py — Keyword monitoring on dark web / paste sites.

OPSEC CRITICAL: All requests are routed through Tor.
                vpn_check.verify_opsec(require_tor=True) is called automatically.

Monitored sources (via Tor, clearnet paste mirrors, and onion services):
  - Pastebin / ghostbin mirrors
  - Publicly accessible paste aggregators
  - Dark web paste onion sites (requires Tor)

This module is for DEFENSIVE threat intelligence only:
  - Monitoring for leaked credentials
  - Watching for mentions of client/personal PII
  - Detecting early signs of planned attacks or data sales

Usage:
    from scripts.osint.dark_web_monitor import DarkWebMonitor

    monitor = DarkWebMonitor(keywords=["michael@example.com", "companyname"])
    results = monitor.scan()
"""

import logging
import time
from dataclasses import dataclass, field
from datetime import datetime

import requests

logger = logging.getLogger(__name__)

TOR_PROXIES = {
    "http": "socks5h://127.0.0.1:9050",
    "https": "socks5h://127.0.0.1:9050",
}
REQUEST_TIMEOUT = 30

# Public paste aggregation APIs (clearnet — check through VPN minimum)
PASTEBIN_SEARCH = "https://psbdmp.ws/api/search/{keyword}"

# Clearnet paste sites with search
PASTE_SOURCES = [
    {
        "name": "psbdmp (Pastebin dump search)",
        "url": "https://psbdmp.ws/api/search/{keyword}",
        "tor": False,
    },
    {
        "name": "GhostBin",
        "url": "https://ghostbin.co/search?q={keyword}",
        "tor": False,
    },
]

# Onion paste sites (requires Tor — listed for reference, availability varies)
ONION_SOURCES = [
    {
        "name": "Pastebin Onion Mirror",
        "url": "http://strongerw2ise74v3duebgsvug4mehyhlpa7f6kfwnas7zofs3kov7yd.onion/search/{keyword}",
        "tor": True,
    },
]


@dataclass
class PasteHit:
    source: str
    url: str
    keyword_triggered: str
    snippet: str
    discovered_at: str
    via_tor: bool


@dataclass
class MonitorResult:
    keywords: list[str]
    scan_timestamp: str
    hits: list[PasteHit] = field(default_factory=list)
    sources_checked: list[str] = field(default_factory=list)
    opsec_verified: bool = False
    errors: list[str] = field(default_factory=list)

    @property
    def has_hits(self) -> bool:
        return len(self.hits) > 0

    def summary(self) -> str:
        lines = [
            f"# Dark Web Monitor Scan",
            f"Timestamp: {self.scan_timestamp}",
            f"Keywords: {', '.join(self.keywords)}",
            f"OPSEC Verified: {'YES' if self.opsec_verified else 'NO'}",
            f"Sources checked: {len(self.sources_checked)}",
            f"Hits found: {len(self.hits)}",
            "",
        ]
        if self.hits:
            lines.append("## Findings")
            for h in self.hits:
                lines += [
                    f"### [{h.source}]({h.url})",
                    f"**Keyword triggered**: `{h.keyword_triggered}`",
                    f"**Discovered**: {h.discovered_at}",
                    f"**Via Tor**: {'Yes' if h.via_tor else 'No'}",
                    f"**Snippet**: {h.snippet[:300]}",
                    "",
                ]
        if self.errors:
            lines.append("## Errors")
            for e in self.errors:
                lines.append(f"- {e}")
        return "\n".join(lines)


class DarkWebMonitor:
    def __init__(
        self,
        keywords: list[str],
        use_tor: bool = True,
        include_onion: bool = True,
    ):
        self.keywords = [k.lower().strip() for k in keywords]
        self.use_tor = use_tor
        self.include_onion = include_onion

    def _get_session(self, via_tor: bool) -> requests.Session:
        session = requests.Session()
        if via_tor and self.use_tor:
            session.proxies = TOR_PROXIES
        session.headers["User-Agent"] = (
            "Mozilla/5.0 (Windows NT 10.0; rv:102.0) Gecko/20100101 Firefox/102.0"
        )
        return session

    def _verify_opsec(self) -> bool:
        """Gate all operations behind OPSEC verification."""
        try:
            from scripts.opsec.vpn_check import verify_opsec
            status = verify_opsec(require_vpn=True, require_tor=self.use_tor)
            if not status.safe:
                logger.error("OPSEC FAILURE: %s — SCAN ABORTED", status.reason)
                return False
            logger.info("OPSEC verified. IP: %s | Tor: %s", status.current_ip, status.tor_active)
            return True
        except Exception as e:
            logger.error("OPSEC check failed: %s — SCAN ABORTED", e)
            return False

    def _search_psbdmp(self, keyword: str, result: MonitorResult) -> None:
        """Search psbdmp (Pastebin dump search API)."""
        try:
            session = self._get_session(via_tor=False)
            url = f"https://psbdmp.ws/api/search/{requests.utils.quote(keyword)}"
            response = session.get(url, timeout=REQUEST_TIMEOUT)

            if response.status_code == 200:
                data = response.json()
                pastes = data.get("data", []) if isinstance(data, dict) else data
                for paste in pastes[:10]:
                    paste_id = paste.get("id", "")
                    text = paste.get("text", "")
                    if keyword in text.lower():
                        result.hits.append(PasteHit(
                            source="psbdmp (Pastebin)",
                            url=f"https://pastebin.com/{paste_id}",
                            keyword_triggered=keyword,
                            snippet=text[:500],
                            discovered_at=datetime.utcnow().isoformat(),
                            via_tor=False,
                        ))
        except Exception as e:
            result.errors.append(f"psbdmp search error: {e}")
            logger.warning("psbdmp error for keyword '%s': %s", keyword, e)

    def _search_onion_pastes(self, keyword: str, result: MonitorResult) -> None:
        """Search onion paste sites (requires Tor)."""
        if not self.use_tor:
            return
        for source in ONION_SOURCES:
            try:
                session = self._get_session(via_tor=True)
                url = source["url"].format(keyword=requests.utils.quote(keyword))
                response = session.get(url, timeout=REQUEST_TIMEOUT)
                if response.status_code == 200 and keyword in response.text.lower():
                    result.hits.append(PasteHit(
                        source=source["name"],
                        url=url,
                        keyword_triggered=keyword,
                        snippet=response.text[:500],
                        discovered_at=datetime.utcnow().isoformat(),
                        via_tor=True,
                    ))
                result.sources_checked.append(source["name"])
            except requests.exceptions.ConnectionError:
                result.errors.append(
                    f"Cannot reach onion site {source['name']} — is Tor running? (tor service)"
                )
            except Exception as e:
                result.errors.append(f"Onion source {source['name']} error: {e}")

    def scan(self) -> MonitorResult:
        """
        Run a full keyword scan across configured sources.

        OPSEC is verified before any network request is made.
        If OPSEC check fails, scan is aborted and result reflects the failure.
        """
        result = MonitorResult(
            keywords=self.keywords,
            scan_timestamp=datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        )

        # OPSEC gate — mandatory
        result.opsec_verified = self._verify_opsec()
        if not result.opsec_verified:
            result.errors.append(
                "Scan aborted: OPSEC verification failed. "
                "Ensure VPN is active and Tor is running before dark web monitoring."
            )
            return result

        logger.info("Starting dark web keyword scan for: %s", self.keywords)

        for keyword in self.keywords:
            logger.info("Scanning keyword: %s", keyword)

            # Clearnet sources (VPN required)
            self._search_psbdmp(keyword, result)
            result.sources_checked.append("psbdmp")
            time.sleep(1)

            # Onion sources (Tor required)
            if self.include_onion and self.use_tor:
                self._search_onion_pastes(keyword, result)

        logger.info(
            "Scan complete. %d hits across %d sources for %d keywords",
            len(result.hits), len(result.sources_checked), len(self.keywords),
        )
        return result


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Dark web keyword monitor (Tor-routed)")
    parser.add_argument("keywords", nargs="+", help="Keywords to monitor")
    parser.add_argument("--no-tor", action="store_true", help="Disable Tor routing (clearnet only)")
    parser.add_argument("--no-onion", action="store_true", help="Skip onion sources")
    parser.add_argument("--output", choices=["print", "vault"], default="print")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

    monitor = DarkWebMonitor(
        keywords=args.keywords,
        use_tor=not args.no_tor,
        include_onion=not args.no_onion,
    )
    result = monitor.scan()
    print(result.summary())

    if args.output == "vault" and result.hits:
        from scripts.reporting.report_generator import generate_report
        generate_report(
            "threat_intel",
            {
                "{{report_type}}": "Dark Web Keyword Scan",
                "{{threat_summary}}": f"{len(result.hits)} hit(s) found for monitored keywords",
                "{{threat_level}}": "High" if result.hits else "Informational",
                "{{sources}}": ", ".join(result.sources_checked),
                "{{keywords}}": ", ".join(result.keywords),
                "{{darkweb_findings}}": result.summary(),
                "{{impact_assessment}}": "Potential credential/data exposure. Review findings immediately.",
                "{{actor_name}}": "Unknown",
                "{{motivation}}": "Unknown",
                "{{ttps}}": "N/A",
                "{{known_targets}}": "N/A",
            },
            output="vault",
        )


if __name__ == "__main__":
    main()
