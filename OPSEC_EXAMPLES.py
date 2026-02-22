"""
OPSEC Integration Example

This demonstrates how to use the complete OPSEC system:
1. Initialize OPSEC (VPN + Tor verification)
2. Log operation to Vault
3. Execute security tools
4. Clean traces before shutdown
"""

import sys
from pathlib import Path

# Add repo to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.opsec.opsec_manager import OpsecManager
from scripts.opsec.operation_logger import get_operation_logger


def example_osint_investigation():
    """Example: Self-testing OSINT investigation"""

    print("\n" + "=" * 70)
    print("EXAMPLE: OSINT SELF-TESTING INVESTIGATION")
    print("=" * 70 + "\n")

    # Step 1: Initialize OPSEC
    print("[1/4] Initializing OPSEC...")
    opsec_manager = OpsecManager()
    opsec_status = opsec_manager.initialize_opsec(
        operation_name="OSINT Self-Testing",
        target="self",
        require_tor=True,
    )

    if not opsec_status.safe:
        print("✗ OPSEC initialization failed — aborting")
        return False

    print("✓ OPSEC initialized safely\n")

    # Step 2: Start operation logging
    print("[2/4] Starting operation logging...")
    op_logger = get_operation_logger()
    op_id = op_logger.start_operation(
        operation_name="OSINT Self-Test",
        operation_type="osint",
        target="self",
        opsec_status={
            "vpn_active": opsec_status.vpn_active,
            "vpn_provider": opsec_status.vpn_provider,
            "tor_active": opsec_status.tor_active,
            "current_ip": opsec_status.current_ip,
            "safe": opsec_status.safe,
        },
        mission_description="""
# OSINT Investigation

**Objective**: Perform passive reconnaissance on self to verify OPSEC layers

**Scope**: 
- Domain registration info (whois)
- DNS records
- Social media presence
- Previous breaches (HaveIBeenPwned)

**Authorization**: Self-testing (cible: moi-même)
        """,
    )

    if not op_id:
        print("✗ Operation logging failed — continuing anyway\n")
    else:
        print(f"✓ Operation logged: {op_id}\n")

    # Step 3: Simulate security tool execution
    print("[3/4] Executing OSINT tools (simulated)...")
    print("  → Running domain_recon...")
    op_logger.log_finding(
        finding_type="info",
        title="Domain Registration",
        description="Domain registered via privacy service",
        severity="info",
        evidence={
            "domain": "example.com",
            "registrar": "Namecheap",
            "privacy": True,
        },
    )

    print("  → Running social_footprint...")
    op_logger.log_finding(
        finding_type="info",
        title="Social Media Presence",
        description="GitHub profile found with public repositories",
        severity="low",
        evidence={
            "platform": "GitHub",
            "username": "ascended33",
            "repos": 15,
        },
    )

    print("  → Running breach_check...")
    op_logger.log_finding(
        finding_type="credential",
        title="Previous Breach Detection",
        description="Email found in 2 known breaches (HaveIBeenPwned)",
        severity="high",
        evidence={
            "email": "***@example.com",
            "breaches": ["Adobe", "Equifax"],
            "action": "Change password / enable 2FA",
        },
    )

    print("✓ Tools executed (3 findings)\n")

    # Step 4: Close operation
    print("[4/4] Closing operation log...")
    op_logger.end_operation(
        status="completed",
        summary="3 findings discovered — no critical vulnerabilities",
        total_findings=3,
    )

    print("✓ Operation closed\n")

    print("=" * 70)
    print("✓ OPSEC INVESTIGATION COMPLETE")
    print("=" * 70)
    print("\nNext steps:")
    print("1. Review findings in Vault: Security/Operations/")
    print("2. Run trace cleanup: python3 scripts/opsec/trace_cleaner.py --scope full")
    print("3. Disconnect VPN: nordvpn disconnect or mullvad disconnect")
    print()

    return True


def example_with_hexstrike():
    """Example: Using hexstrike-ai within OPSEC container"""

    print("\n" + "=" * 70)
    print("EXAMPLE: HEXSTRIKE-AI INTEGRATION")
    print("=" * 70 + "\n")

    print("""
When hexstrike-ai is running in Docker:

1. Initialize OPSEC:
   ./launch-opsec-session.sh "Hexstrike Operation" "self" "pentest"

2. Access th3-kali container:
   docker exec -it th3-kali bash

3. Inside th3-kali, connect to hexstrike-ai on localhost:8888:
   python3 -c "
   from mcp.hexstrike_client import HexStrikeClient
   client = HexStrikeClient()
   result = client.network_recon('target.com')
   print(result)
   "

4. All traffic routes through:
   VPN (NordVPN/Mullvad) → Tor (th3-tor) → Internet

5. Exit container:
   exit

6. Clean traces:
   python3 scripts/opsec/trace_cleaner.py --scope full
    """)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="OPSEC Integration Examples")
    parser.add_argument(
        "--mode",
        choices=["osint", "hexstrike", "all"],
        default="osint",
        help="Example mode to run",
    )

    args = parser.parse_args()

    try:
        if args.mode in ["osint", "all"]:
            example_osint_investigation()

        if args.mode in ["hexstrike", "all"]:
            example_with_hexstrike()

    except KeyboardInterrupt:
        print("\n\n⛔ Interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)
