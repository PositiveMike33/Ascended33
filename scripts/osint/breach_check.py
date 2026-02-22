"""
breach_check.py — Check emails and domains against breach databases.

Uses the HaveIBeenPwned (HIBP) v3 API:
  - Email breach lookup (requires HIBP API key)
  - Password hash check via k-anonymity (no API key needed — privacy-safe)
  - Domain breach search

HIBP k-anonymity model for passwords:
  Only the first 5 chars of the SHA-1 hash are sent to the API.
  The full hash never leaves the local machine.

Usage:
    from scripts.osint.breach_check import BreachChecker

    checker = BreachChecker(api_key="your-hibp-key")  # optional for email checks
    result = checker.check_email("target@example.com")
    result = checker.check_domain("example.com")
    result = checker.check_password("hunter2")  # uses k-anonymity, no API key needed
"""

import hashlib
import logging
from dataclasses import dataclass, field

import requests

logger = logging.getLogger(__name__)

HIBP_BASE = "https://haveibeenpwned.com/api/v3"
HIBP_PWNED_PASSWORDS = "https://api.pwnedpasswords.com/range/{prefix}"
REQUEST_TIMEOUT = 15


@dataclass
class BreachEntry:
    name: str
    domain: str
    breach_date: str
    pwn_count: int
    data_classes: list[str]
    description: str
    is_sensitive: bool
    is_verified: bool


@dataclass
class EmailBreachResult:
    email: str
    breached: bool
    breach_count: int = 0
    breaches: list[BreachEntry] = field(default_factory=list)
    pastes: list[dict] = field(default_factory=list)
    error: str = ""


@dataclass
class DomainBreachResult:
    domain: str
    breaches_found: list[BreachEntry] = field(default_factory=list)
    affected_emails: list[str] = field(default_factory=list)
    error: str = ""


@dataclass
class PasswordCheckResult:
    password_hint: str       # Only first 2 chars shown — never log plaintext
    is_pwned: bool
    occurrence_count: int
    risk_level: str          # "Critical" / "High" / "Low" / "Safe"


class BreachChecker:
    def __init__(self, api_key: str = ""):
        self.api_key = api_key
        self._headers = {
            "hibp-api-key": api_key,
            "user-agent": "Ascended33-Security-Research/1.0",
        }

    def _get(self, endpoint: str, params: dict | None = None) -> requests.Response:
        if not self.api_key:
            raise ValueError(
                "HIBP API key required for email/domain checks. "
                "Get a key at https://haveibeenpwned.com/API/Key — "
                "or use check_password() which requires no API key."
            )
        return requests.get(
            f"{HIBP_BASE}/{endpoint}",
            headers=self._headers,
            params=params,
            timeout=REQUEST_TIMEOUT,
        )

    def check_email(self, email: str, include_unverified: bool = False) -> EmailBreachResult:
        """
        Check if an email address appears in known data breaches.
        Requires HIBP API key.
        """
        result = EmailBreachResult(email=email, breached=False)
        try:
            params = {"truncateResponse": "false", "includeUnverified": str(include_unverified).lower()}
            response = self._get(f"breachedaccount/{email}", params=params)

            if response.status_code == 404:
                result.breached = False
                return result

            response.raise_for_status()
            data = response.json()

            result.breached = True
            result.breach_count = len(data)
            result.breaches = [
                BreachEntry(
                    name=b.get("Name", ""),
                    domain=b.get("Domain", ""),
                    breach_date=b.get("BreachDate", ""),
                    pwn_count=b.get("PwnCount", 0),
                    data_classes=b.get("DataClasses", []),
                    description=b.get("Description", ""),
                    is_sensitive=b.get("IsSensitive", False),
                    is_verified=b.get("IsVerified", True),
                )
                for b in data
            ]
            logger.info("Email %s: found in %d breaches", email, result.breach_count)

        except ValueError as e:
            result.error = str(e)
        except requests.HTTPError as e:
            if e.response.status_code == 401:
                result.error = "HIBP API key invalid or missing"
            elif e.response.status_code == 429:
                result.error = "Rate limited by HIBP — wait before retrying"
            else:
                result.error = str(e)
        except Exception as e:
            result.error = str(e)
            logger.warning("Breach check error for %s: %s", email, e)

        return result

    def check_domain(self, domain: str) -> DomainBreachResult:
        """
        List all breaches that include a given domain.
        Returns known breach metadata for the domain (not individual emails).
        Uses the public breaches API — no API key needed for this call.
        """
        result = DomainBreachResult(domain=domain)
        try:
            response = requests.get(
                f"{HIBP_BASE}/breaches",
                params={"domain": domain},
                headers={"user-agent": "Ascended33-Security-Research/1.0"},
                timeout=REQUEST_TIMEOUT,
            )
            if response.status_code == 200:
                data = response.json()
                result.breaches_found = [
                    BreachEntry(
                        name=b.get("Name", ""),
                        domain=b.get("Domain", ""),
                        breach_date=b.get("BreachDate", ""),
                        pwn_count=b.get("PwnCount", 0),
                        data_classes=b.get("DataClasses", []),
                        description=b.get("Description", ""),
                        is_sensitive=b.get("IsSensitive", False),
                        is_verified=b.get("IsVerified", True),
                    )
                    for b in data
                ]
                logger.info("Domain %s: %d breach records found", domain, len(result.breaches_found))
        except Exception as e:
            result.error = str(e)
        return result

    def check_password(self, password: str) -> PasswordCheckResult:
        """
        Check if a password has appeared in data breaches.

        Uses k-anonymity: only the first 5 chars of the SHA-1 hash are sent.
        The actual password or full hash NEVER leaves the local machine.
        """
        sha1 = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()  # noqa: S324
        prefix, suffix = sha1[:5], sha1[5:]
        hint = password[:2] + "*" * max(0, len(password) - 2)

        result = PasswordCheckResult(
            password_hint=hint,
            is_pwned=False,
            occurrence_count=0,
            risk_level="Safe",
        )

        try:
            response = requests.get(
                HIBP_PWNED_PASSWORDS.format(prefix=prefix),
                timeout=REQUEST_TIMEOUT,
            )
            response.raise_for_status()

            for line in response.text.splitlines():
                hash_suffix, count = line.split(":")
                if hash_suffix == suffix:
                    count = int(count)
                    result.is_pwned = True
                    result.occurrence_count = count
                    if count > 100_000:
                        result.risk_level = "Critical"
                    elif count > 1_000:
                        result.risk_level = "High"
                    else:
                        result.risk_level = "Low"
                    break

            logger.info("Password check (%s): pwned=%s count=%d",
                        hint, result.is_pwned, result.occurrence_count)
        except Exception as e:
            logger.warning("Password check error: %s", e)

        return result

    def format_report_section(self, results: list[EmailBreachResult | DomainBreachResult]) -> str:
        """Format breach results as an Obsidian-compatible markdown section."""
        lines = ["## Breach Intelligence\n"]
        for r in results:
            if isinstance(r, EmailBreachResult):
                status = f"**BREACHED** — {r.breach_count} breaches" if r.breached else "Clean"
                lines.append(f"### Email: `{r.email}`")
                lines.append(f"Status: {status}")
                for b in r.breaches:
                    lines.append(f"- **{b.name}** ({b.breach_date}) — {b.pwn_count:,} records")
                    lines.append(f"  - Data: {', '.join(b.data_classes)}")
                lines.append("")
            elif isinstance(r, DomainBreachResult):
                lines.append(f"### Domain: `{r.domain}`")
                if r.breaches_found:
                    lines.append(f"Found in {len(r.breaches_found)} breach(es):")
                    for b in r.breaches_found:
                        lines.append(f"- **{b.name}** ({b.breach_date}) — {b.pwn_count:,} records")
                else:
                    lines.append("No known breaches found.")
                lines.append("")
        return "\n".join(lines)


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Breach database checker (HIBP)")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--email", help="Email to check")
    group.add_argument("--domain", help="Domain to check")
    group.add_argument("--password", help="Password to check (k-anonymity, safe)")
    parser.add_argument("--api-key", default="", help="HIBP API key (for email checks)")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    checker = BreachChecker(api_key=args.api_key)

    if args.email:
        result = checker.check_email(args.email)
        if result.error:
            print(f"Error: {result.error}")
        elif result.breached:
            print(f"BREACHED: {args.email} found in {result.breach_count} breach(es)")
            for b in result.breaches:
                print(f"  - {b.name} ({b.breach_date}): {', '.join(b.data_classes)}")
        else:
            print(f"Clean: {args.email} not found in any known breaches")

    elif args.domain:
        result = checker.check_domain(args.domain)
        print(checker.format_report_section([result]))

    elif args.password:
        result = checker.check_password(args.password)
        if result.is_pwned:
            print(f"PWNED: appeared {result.occurrence_count:,} times — Risk: {result.risk_level}")
        else:
            print("Safe: password not found in known breach databases")


if __name__ == "__main__":
    main()
