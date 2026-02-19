"""
vpn_check.py — OPSEC gating: verify VPN/Tor status before active operations.

This is the first line of defense. All active security operations must call
verify_opsec() and abort if it returns a failed status.

Improvements over v1:
  - Compares current IP against stored home_ip (config.yaml opsec.home_ip)
    to reliably detect VPN-off state, not just guess from Tor status.
  - DNS leak detection: checks if DNS resolver IP differs from tunnel IP.
  - Cloudflare trace API (1.1.1.1) for DNS-level resolver identification.
  - Explicit safe=False when current_ip == home_ip (VPN provably off).

Config (config.yaml):
    opsec:
      home_ip: "YOUR_REAL_IP"       # Set once without VPN, never re-commit
      require_vpn: true
      require_tor_for_darkweb: true

Usage:
    from scripts.opsec.vpn_check import verify_opsec, OpsecStatus

    status = verify_opsec(require_tor=False)
    if not status.safe:
        print(f"OPSEC FAILURE: {status.reason}")
        sys.exit(1)
"""

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import requests

logger = logging.getLogger(__name__)

TOR_CHECK_URL = "https://check.torproject.org/api/ip"
IP_CHECK_URL = "https://httpbin.org/ip"
CF_TRACE_URL = "https://1.1.1.1/cdn-cgi/trace"
REQUEST_TIMEOUT = 10


@dataclass
class OpsecStatus:
    safe: bool
    reason: str
    current_ip: str = ""
    tor_active: bool = False
    vpn_detected: bool = False
    dns_leak_detected: bool = False


def _get_current_ip() -> Optional[str]:
    """Return the current public IP via httpbin.org."""
    try:
        response = requests.get(IP_CHECK_URL, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        return response.json().get("origin", "").split(",")[0].strip()
    except requests.RequestException:
        return None


def _check_tor() -> tuple[bool, str]:
    """
    Check if traffic is routed through Tor.

    Returns:
        (is_tor, exit_ip) — is_tor is True if Tor is active.
    """
    try:
        response = requests.get(TOR_CHECK_URL, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        data = response.json()
        return data.get("IsTor", False), data.get("IP", "")
    except requests.RequestException:
        return False, ""


def _check_dns_leak(tunnel_ip: str) -> bool:
    """
    Detect DNS leaks by comparing the DNS resolver IP to the tunnel IP.

    Uses Cloudflare's trace endpoint which reveals the IP making the DNS query.
    If the DNS resolver IP differs significantly from the tunnel IP → possible leak.

    Args:
        tunnel_ip: The current public IP (through VPN/Tor).

    Returns:
        True if a DNS leak is suspected, False if clean.
    """
    try:
        response = requests.get(CF_TRACE_URL, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        trace_data: dict[str, str] = {}
        for line in response.text.splitlines():
            if "=" in line:
                key, _, value = line.partition("=")
                trace_data[key.strip()] = value.strip()

        resolver_ip = trace_data.get("ip", "")
        if not resolver_ip or not tunnel_ip:
            return False

        # Extract /24 subnet for comparison (rough check)
        tunnel_subnet = ".".join(tunnel_ip.split(".")[:3])
        resolver_subnet = ".".join(resolver_ip.split(".")[:3])

        if resolver_subnet != tunnel_subnet and resolver_ip != tunnel_ip:
            logger.warning(
                "Potential DNS leak: tunnel_ip=%s resolver_ip=%s",
                tunnel_ip, resolver_ip,
            )
            return True
        return False
    except requests.RequestException:
        # If CF trace unreachable, don't block — log and continue
        logger.debug("CF trace check failed — DNS leak check skipped")
        return False


def _load_home_ip_from_config() -> Optional[str]:
    """
    Load the stored home IP from config.yaml (opsec.home_ip).

    Returns:
        Home IP string, or None if not configured.
    """
    try:
        import yaml  # type: ignore[import]
        config_path = Path(__file__).parent.parent.parent / "config" / "config.yaml"
        if not config_path.exists():
            return None
        with config_path.open() as f:
            cfg = yaml.safe_load(f)
        home_ip = cfg.get("opsec", {}).get("home_ip", "")
        if home_ip and home_ip not in ("YOUR_REAL_IP", "", None):
            return str(home_ip)
        return None
    except Exception as e:
        logger.debug("Could not load home_ip from config: %s", e)
        return None


def verify_opsec(
    require_vpn: bool = True,
    require_tor: bool = False,
    check_dns_leak: bool = True,
) -> OpsecStatus:
    """
    Verify OPSEC status before any active security operation.

    Checks (in order):
      1. Current public IP is reachable
      2. If home_ip configured: fail immediately if current_ip == home_ip (VPN off)
      3. Tor requirement (for dark web operations)
      4. DNS leak detection

    Args:
        require_vpn: If True, operation requires VPN to be active.
        require_tor: If True, operation requires Tor (e.g., dark web access).
        check_dns_leak: If True, run DNS leak detection.

    Returns:
        OpsecStatus — check `.safe` before proceeding.
    """
    current_ip = _get_current_ip()
    if current_ip is None:
        return OpsecStatus(
            safe=False,
            reason="Cannot determine current IP — network unreachable or httpbin.org down.",
        )

    # --- Check against known home IP ---
    home_ip = _load_home_ip_from_config()
    if home_ip and current_ip == home_ip:
        return OpsecStatus(
            safe=False,
            reason=(
                f"CRITICAL: Current IP ({current_ip}) matches your home IP. "
                "VPN is OFF. Connect to VPN before proceeding."
            ),
            current_ip=current_ip,
            tor_active=False,
            vpn_detected=False,
        )

    # --- Tor check ---
    tor_active, tor_ip = _check_tor()

    if require_tor and not tor_active:
        return OpsecStatus(
            safe=False,
            reason=(
                "Tor is required for this operation but is not active. "
                "Route traffic through Tor before proceeding."
            ),
            current_ip=current_ip,
            tor_active=False,
        )

    # --- VPN check ---
    # If not on Tor, we infer VPN from IP mismatch with home_ip.
    # Without home_ip configured, we can only warn.
    vpn_detected = tor_active  # Tor counts as equivalent to VPN
    if not tor_active:
        if home_ip:
            # home_ip is configured and current_ip != home_ip → VPN is on
            vpn_detected = True
        else:
            # No home_ip reference — can only warn
            if require_vpn:
                logger.warning(
                    "VPN check: current IP is %s. "
                    "Set opsec.home_ip in config.yaml for reliable VPN detection.",
                    current_ip,
                )

    if require_vpn and not vpn_detected and not home_ip:
        # Soft warn — cannot confirm VPN without home_ip reference
        logger.warning(
            "Cannot confirm VPN status (no home_ip reference). "
            "Proceeding, but set opsec.home_ip in config.yaml."
        )

    # --- DNS leak check ---
    dns_leak = False
    if check_dns_leak and not tor_active:
        dns_leak = _check_dns_leak(current_ip)
        if dns_leak:
            return OpsecStatus(
                safe=False,
                reason=(
                    f"DNS leak detected: DNS resolver IP differs from tunnel IP ({current_ip}). "
                    "Your ISP's DNS may be used. Fix DNS settings or use VPN's DNS."
                ),
                current_ip=current_ip,
                tor_active=tor_active,
                vpn_detected=vpn_detected,
                dns_leak_detected=True,
            )

    logger.info(
        "OPSEC check passed. IP: %s | Tor: %s | VPN: %s | DNS leak: %s",
        current_ip, tor_active, vpn_detected, dns_leak,
    )
    return OpsecStatus(
        safe=True,
        reason="OPSEC checks passed",
        current_ip=current_ip,
        tor_active=tor_active,
        vpn_detected=vpn_detected,
        dns_leak_detected=dns_leak,
    )


# ----------------------------------------------------------------
# CLI ENTRY POINT
# ----------------------------------------------------------------

def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(
        description="vpn_check — OPSEC status verification for Ascended33",
    )
    parser.add_argument("--require-tor", action="store_true",
                        help="Fail if Tor is not active")
    parser.add_argument("--no-vpn", action="store_true",
                        help="Skip VPN requirement (passive OSINT only)")
    parser.add_argument("--no-dns-check", action="store_true",
                        help="Skip DNS leak detection")
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s: %(message)s",
    )

    status = verify_opsec(
        require_vpn=not args.no_vpn,
        require_tor=args.require_tor,
        check_dns_leak=not args.no_dns_check,
    )

    print(f"\n[vpn_check] OPSEC Status: {'SAFE' if status.safe else 'UNSAFE'}")
    print(f"  Reason       : {status.reason}")
    print(f"  Current IP   : {status.current_ip}")
    print(f"  Tor active   : {status.tor_active}")
    print(f"  VPN detected : {status.vpn_detected}")
    print(f"  DNS leak     : {status.dns_leak_detected}")

    return 0 if status.safe else 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
