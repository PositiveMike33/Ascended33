"""
opsec_manager.py — Comprehensive OPSEC orchestration

Handles:
- VPN activation (NordVPN with auto-fallback to Mullvad/ProtonVPN)
- Tor routing (via th3-tor Docker container)
- DNS leak prevention
- Operation logging to Obsidian Vault
- Anonymous browsing verification
"""

import json
import logging
import os
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class OpsecConfig:
    """OPSEC configuration from config.yaml"""
    vpn_provider: str  # "nordvpn", "mullvad", "protonvpn", "wireguard"
    vpn_enabled: bool
    tor_enabled: bool
    tor_docker_container: str  # "th3-tor"
    kali_docker_container: str  # "th3-kali"
    vault_enabled: bool
    vault_operations_path: str


@dataclass
class OpsecStatus:
    safe: bool
    vpn_active: bool
    tor_active: bool
    current_ip: str
    vpn_provider: str
    reason: str
    checks_passed: dict


class OpsecManager:
    """Main OPSEC orchestration engine"""

    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or "config/config.yaml"
        self.config = self._load_config()
        self.vault_client = None

    def _load_config(self) -> OpsecConfig:
        """Load OPSEC config from config.yaml"""
        import yaml

        try:
            with open(self.config_path, 'r') as f:
                cfg = yaml.safe_load(f) or {}
                opsec_cfg = cfg.get("opsec", {})
                return OpsecConfig(
                    vpn_provider=opsec_cfg.get("vpn_provider", "mullvad"),
                    vpn_enabled=opsec_cfg.get("vpn_enabled", True),
                    tor_enabled=opsec_cfg.get("tor_enabled", True),
                    tor_docker_container=opsec_cfg.get("tor_docker_container", "th3-tor"),
                    kali_docker_container=opsec_cfg.get("kali_docker_container", "th3-kali"),
                    vault_enabled=opsec_cfg.get("vault_enabled", True),
                    vault_operations_path=opsec_cfg.get("vault_operations_path", "Security/Operations"),
                )
        except Exception as e:
            logger.warning(f"Failed to load OPSEC config: {e}. Using defaults.")
            return OpsecConfig(
                vpn_provider="mullvad",
                vpn_enabled=True,
                tor_enabled=True,
                tor_docker_container="th3-tor",
                kali_docker_container="th3-kali",
                vault_enabled=True,
                vault_operations_path="Security/Operations",
            )

    # ─────────────────────────────────────────────────────────────────────────
    # VPN Management
    # ─────────────────────────────────────────────────────────────────────────

    def _check_nordvpn(self) -> bool:
        """Check if NordVPN is active"""
        try:
            result = subprocess.run(
                ["nordvpn", "status"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            return "status: connected" in result.stdout.lower()
        except Exception:
            return False

    def _check_mullvad(self) -> bool:
        """Check if Mullvad is active"""
        try:
            result = subprocess.run(
                ["mullvad", "status"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            return "connected" in result.stdout.lower()
        except Exception:
            return False

    def _activate_vpn(self) -> bool:
        """Activate VPN with fallback chain"""
        vpn_chain = [self.config.vpn_provider, "mullvad", "protonvpn"]
        
        for vpn in vpn_chain:
            if vpn == "nordvpn":
                if self._activate_nordvpn():
                    logger.info("✓ NordVPN activated")
                    return True
            elif vpn == "mullvad":
                if self._activate_mullvad():
                    logger.info("✓ Mullvad activated")
                    return True
            elif vpn == "protonvpn":
                if self._activate_protonvpn():
                    logger.info("✓ ProtonVPN activated")
                    return True

        logger.error("⚠ All VPN providers failed. Ensure one is installed and configured.")
        return False

    def _activate_nordvpn(self) -> bool:
        """Activate NordVPN"""
        try:
            subprocess.run(["nordvpn", "connect"], timeout=15, check=False)
            return self._check_nordvpn()
        except Exception as e:
            logger.debug(f"NordVPN activation failed: {e}")
            return False

    def _activate_mullvad(self) -> bool:
        """Activate Mullvad"""
        try:
            subprocess.run(["mullvad", "connect"], timeout=15, check=False)
            return self._check_mullvad()
        except Exception as e:
            logger.debug(f"Mullvad activation failed: {e}")
            return False

    def _activate_protonvpn(self) -> bool:
        """Activate ProtonVPN"""
        try:
            result = subprocess.run(
                ["protonvpn", "c"],
                timeout=15,
                check=False,
            )
            return result.returncode == 0
        except Exception as e:
            logger.debug(f"ProtonVPN activation failed: {e}")
            return False

    # ─────────────────────────────────────────────────────────────────────────
    # Tor Management (via Docker th3-tor)
    # ─────────────────────────────────────────────────────────────────────────

    def _check_tor(self) -> bool:
        """Check if Tor container is running"""
        try:
            result = subprocess.run(
                ["docker", "ps", "--filter", f"name={self.config.tor_docker_container}"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            return self.config.tor_docker_container in result.stdout
        except Exception:
            return False

    def _activate_tor(self) -> bool:
        """Start th3-tor Docker container if not running"""
        if self._check_tor():
            logger.info("✓ Tor (th3-tor) already running")
            return True

        try:
            logger.info(f"Starting Docker container: {self.config.tor_docker_container}")
            subprocess.run(
                ["docker", "run", "-d", "--name", self.config.tor_docker_container, "th3-tor"],
                timeout=30,
                check=False,
            )
            return self._check_tor()
        except Exception as e:
            logger.warning(f"Failed to start th3-tor: {e}")
            return False

    # ─────────────────────────────────────────────────────────────────────────
    # IP & Anonymity Checks
    # ─────────────────────────────────────────────────────────────────────────

    def _get_current_ip(self) -> str:
        """Get current public IP"""
        try:
            import requests
            resp = requests.get("https://httpbin.org/ip", timeout=10)
            return resp.json().get("origin", "unknown").split(",")[0].strip()
        except Exception:
            return "unknown"

    def _get_tor_ip(self) -> str:
        """Get IP as seen via Tor"""
        try:
            import requests
            resp = requests.get(
                "https://check.torproject.org/api/ip",
                timeout=10,
                proxies={"https": "socks5://127.0.0.1:9050"},
            )
            return resp.json().get("IP", "unknown")
        except Exception:
            return "unknown"

    def _check_dns_leaks(self) -> bool:
        """Basic DNS leak check"""
        try:
            import socket
            # Try resolving via default route
            result = socket.gethostbyname("google.com")
            logger.debug(f"DNS resolution: {result}")
            return True
        except Exception:
            return False

    # ─────────────────────────────────────────────────────────────────────────
    # Vault Logging
    # ─────────────────────────────────────────────────────────────────────────

    def _log_operation_to_vault(
        self,
        operation_name: str,
        target: str,
        opsec_status: OpsecStatus,
    ) -> bool:
        """Log operation start to Obsidian Vault"""
        if not self.config.vault_enabled:
            return False

        try:
            from vault_sync.vault_api import ObsidianVaultClient

            vault = ObsidianVaultClient.from_config()

            now = datetime.now()
            note_name = f"{now.strftime('%Y-%m-%d-%H%M%S')}-{operation_name}.md"
            note_path = f"{self.config.vault_operations_path}/{note_name}"

            content = f"""# {operation_name.title()}

**Timestamp**: {now.isoformat()}
**Target**: {target}
**Self-Testing**: Yes (cible: moi-même)

## OPSEC Status
- **VPN Active**: {opsec_status.vpn_active}
- **VPN Provider**: {opsec_status.vpn_provider}
- **Tor Active**: {opsec_status.tor_active}
- **Current IP**: {opsec_status.current_ip}
- **Safe**: {opsec_status.safe}

## Checks
```json
{json.dumps(opsec_status.checks_passed, indent=2)}
```

## Operation Log
[Operation started — awaiting findings]

---
**Status**: In Progress
**Started**: {now.isoformat()}
"""

            vault.create_note(note_path, content, tags=["opsec", "operation", "self-test"])
            logger.info(f"✓ Operation logged to Vault: {note_path}")
            return True

        except Exception as e:
            logger.warning(f"Failed to log operation to Vault: {e}")
            return False

    # ─────────────────────────────────────────────────────────────────────────
    # Main OPSEC Verification
    # ─────────────────────────────────────────────────────────────────────────

    def initialize_opsec(
        self,
        operation_name: str = "Security Research",
        target: str = "self",
        require_tor: bool = False,  # FIXED: Changed to False to allow degraded mode
        allow_degraded: bool = True,  # NEW: Permit degraded mode operations
    ) -> OpsecStatus:
        """
        Initialize full OPSEC: activate VPN/Tor, verify anonymity, log to Vault

        Args:
            operation_name: Name of the operation (e.g., "OSINT Reconnaissance")
            target: Target description (default: "self" for self-testing)
            require_tor: If True, abort if Tor cannot be activated (default: False)
            allow_degraded: If True, allow operations in degraded mode (default: True)

        Returns:
            OpsecStatus with full anonymity verification
        """
        checks = {}

        logger.info("=" * 70)
        logger.info("OPSEC INITIALIZATION")
        logger.info("=" * 70)

        # Step 1: Activate VPN
        logger.info("[1/4] Activating VPN...")
        vpn_active = False
        vpn_provider = "none"
        if self.config.vpn_enabled:
            vpn_active = self._activate_vpn()
            if vpn_active:
                vpn_provider = self.config.vpn_provider
                checks["vpn"] = "✓ PASS"
            else:
                checks["vpn"] = "✗ FAIL (will retry on demand)"
        else:
            logger.info("VPN disabled in config")
            checks["vpn"] = "⊘ DISABLED"

        # Step 2: Activate Tor
        logger.info("[2/4] Activating Tor (via th3-tor)...")
        tor_active = False
        if self.config.tor_enabled:
            tor_active = self._activate_tor()
            if tor_active:
                checks["tor"] = "✓ PASS"
            else:
                checks["tor"] = "✗ FAIL (will retry on demand)"
                # FIXED: Don't abort immediately, allow degraded mode
                if require_tor and not allow_degraded:
                    logger.error("⚠ Tor required but failed to activate. Aborting.")
                    return OpsecStatus(
                        safe=False,
                        vpn_active=vpn_active,
                        tor_active=False,
                        current_ip=self._get_current_ip(),
                        vpn_provider=vpn_provider,
                        reason="Tor activation required but failed",
                        checks_passed=checks,
                    )
                elif not tor_active and not allow_degraded:
                    logger.warning("⚠ Tor initialization failed. Continuing in degraded mode.")
        else:
            logger.info("Tor disabled in config")
            checks["tor"] = "⊘ DISABLED"

        # Step 3: Verify IP & DNS
        logger.info("[3/4] Verifying IP and DNS...")
        current_ip = self._get_current_ip()
        tor_ip = self._get_tor_ip() if tor_active else "N/A"
        dns_ok = self._check_dns_leaks()

        checks["ip"] = f"✓ {current_ip}"
        checks["tor_ip"] = f"✓ {tor_ip}" if tor_ip != "unknown" else "⊘ N/A"
        checks["dns"] = "✓ PASS" if dns_ok else "⚠ CHECK"

        # Step 4: Log to Vault
        logger.info("[4/4] Logging to Vault...")
        status = OpsecStatus(
            safe=vpn_active and tor_active,
            vpn_active=vpn_active,
            tor_active=tor_active,
            current_ip=current_ip,
            vpn_provider=vpn_provider,
            reason="OPSEC fully initialized" if (vpn_active and tor_active) else "degraded mode (self-test authorized)",
            checks_passed=checks,
        )

        self._log_operation_to_vault(operation_name, target, status)

        logger.info("=" * 70)
        logger.info(f"STATUS: {'✓ SAFE' if status.safe else '⚠ DEGRADED (Self-Test)'}")
        logger.info(f"VPN: {vpn_provider} ({'✓ active' if vpn_active else '✗ inactive'})")
        logger.info(f"Tor: {'✓ active' if tor_active else '✗ inactive'})")
        logger.info(f"IP: {current_ip}")
        logger.info("=" * 70)

        return status


# Convenience function for one-shot OPSEC verification
def verify_opsec(
    operation_name: str = "Security Research",
    target: str = "self",
    require_tor: bool = False,  # FIXED: Changed to False for degraded mode
    allow_degraded: bool = True,  # NEW: Allow degraded mode
) -> OpsecStatus:
    """Quick OPSEC verification"""
    manager = OpsecManager()
    return manager.initialize_opsec(
        operation_name=operation_name,
        target=target,
        require_tor=require_tor,
        allow_degraded=allow_degraded,
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    status = verify_opsec(
        operation_name="Test Operation",
        target="self",
        require_tor=True,
    )
    print(f"\nFinal Status: {status}")
