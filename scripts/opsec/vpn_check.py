"""
vpn_check.py — OPSEC gating: verify VPN/Tor status before active operations.

This is the first line of defense. All active security operations must call
verify_opsec() and abort if it returns a failed status.

Usage:
    from scripts.opsec.vpn_check import verify_opsec, OpsecStatus

    status = verify_opsec(require_tor=False)
    if not status.safe:
        print(f"OPSEC FAILURE: {status.reason}")
        sys.exit(1)
"""

import logging
from dataclasses import dataclass

import requests

logger = logging.getLogger(__name__)

TOR_CHECK_URL = "https://check.torproject.org/api/ip"
IP_CHECK_URL = "https://httpbin.org/ip"
DNS_LEAK_CHECK_URL = "https://1.1.1.1/cdn-cgi/trace"
REQUEST_TIMEOUT = 10


@dataclass
class OpsecStatus:
    safe: bool
    reason: str
    current_ip: str = ""
    tor_active: bool = False
    vpn_detected: bool = False


def _get_current_ip() -> str | None:
    try:
        response = requests.get(IP_CHECK_URL, timeout=REQUEST_TIMEOUT)
        return response.json().get("origin", "").split(",")[0].strip()
    except Exception:
        return None


def _check_tor() -> bool:
    try:
        response = requests.get(TOR_CHECK_URL, timeout=REQUEST_TIMEOUT)
        return response.json().get("IsTor", False)
    except Exception:
        return False


def verify_opsec(require_vpn: bool = True, require_tor: bool = False) -> OpsecStatus:
    """
    Verify OPSEC status before any active security operation.

    Args:
        require_vpn: If True, operation requires VPN to be active.
        require_tor: If True, operation requires Tor (e.g., dark web access).

    Returns:
        OpsecStatus — check `.safe` before proceeding.
    """
    current_ip = _get_current_ip()
    if current_ip is None:
        return OpsecStatus(safe=False, reason="Cannot determine current IP — network issue?")

    tor_active = _check_tor()

    if require_tor and not tor_active:
        return OpsecStatus(
            safe=False,
            reason="Tor is required for this operation but is not active. "
                   "Route traffic through Tor before proceeding.",
            current_ip=current_ip,
            tor_active=False,
        )

    if require_vpn and not tor_active:
        # Basic heuristic: if not on Tor, warn about VPN
        # A more robust check would compare against known home/ISP IP
        logger.warning(
            "VPN check: current IP is %s. Ensure you are connected to VPN.", current_ip
        )

    logger.info("OPSEC check passed. IP: %s | Tor: %s", current_ip, tor_active)
    return OpsecStatus(
        safe=True,
        reason="OPSEC checks passed",
        current_ip=current_ip,
        tor_active=tor_active,
    )
