"""
verify_connections.py — Test all Ascended33 integrations.

Run this after setup to confirm everything is connected:
    python verify_connections.py

Checks:
  1. Obsidian Vault REST API (localhost:27123)
  2. hexstrike-ai MCP server (localhost:8888)
  3. Kali VM SSH connection
  4. hexstrike-ai running on Kali VM
"""

import sys
import time

PASS = "\033[92m[PASS]\033[0m"
FAIL = "\033[91m[FAIL]\033[0m"
WARN = "\033[93m[WARN]\033[0m"
INFO = "\033[94m[INFO]\033[0m"


def check(label: str, fn) -> bool:
    print(f"  {INFO} {label}...", end=" ", flush=True)
    try:
        result = fn()
        if result:
            print(PASS)
            return True
        else:
            print(f"{FAIL} — not reachable")
            return False
    except Exception as e:
        print(f"{FAIL} — {e}")
        return False


def main() -> None:
    print()
    print("=" * 55)
    print("  ASCENDED33 — Connection Verification")
    print("=" * 55)
    print()

    results: dict[str, bool] = {}

    # --- 1. Obsidian Vault REST API ---
    print("[ Obsidian Vault REST API ]")
    try:
        from vault_sync.vault_api import ObsidianVaultClient
        vault = ObsidianVaultClient.from_config()
        results["obsidian"] = check("Obsidian REST API at localhost:27123", vault.is_reachable)
        if results["obsidian"]:
            results["obsidian_write"] = check(
                "Test write note to Vault",
                lambda: (
                    vault.create_note(
                        "Claude-Michael/Sessions/_connection_test.md",
                        "# Connection Test\nAscended33 connected successfully.\n#claude",
                    ) or True
                ),
            )
    except ImportError as e:
        print(f"  {FAIL} Import error: {e}")
        results["obsidian"] = False

    print()

    # --- 2. hexstrike-ai (local — if running locally) ---
    print("[ hexstrike-ai MCP Server (localhost:8888) ]")
    try:
        from mcp.hexstrike_client import HexStrikeClient
        hexstrike = HexStrikeClient()
        results["hexstrike_local"] = check(
            "hexstrike-ai at localhost:8888",
            hexstrike.is_reachable,
        )
    except ImportError as e:
        print(f"  {WARN} Import error: {e}")
        results["hexstrike_local"] = False

    print()

    # --- 3. Kali VM SSH ---
    print("[ Kali Linux VM — SSH ]")
    try:
        from mcp.kali_ssh_client import KaliSSHClient
        kali = KaliSSHClient.from_config()

        results["kali_ssh"] = check("SSH connection to Kali VM", kali.is_reachable)

        if results.get("kali_ssh"):
            with KaliSSHClient.from_config() as k:
                # Check hexstrike on Kali
                results["hexstrike_kali"] = check(
                    "hexstrike-ai running on Kali VM",
                    k.hexstrike_status,
                )

                if not results.get("hexstrike_kali"):
                    print(f"  {WARN} Attempting to start hexstrike-ai on Kali...")
                    start_result = k.start_hexstrike()
                    time.sleep(3)
                    results["hexstrike_kali"] = check(
                        "hexstrike-ai running on Kali VM (after start)",
                        k.hexstrike_status,
                    )

                # Verify Kali tools
                results["kali_nmap"] = check(
                    "nmap installed on Kali",
                    lambda: k.run("which nmap").success,
                )
                results["kali_ip"] = check(
                    "Get Kali IP address",
                    lambda: bool(k.run("hostname -I").stdout),
                )
                if results["kali_ip"]:
                    kali_ip = k.run("hostname -I").stdout.split()[0]
                    print(f"  {INFO} Kali VM IP: \033[96m{kali_ip}\033[0m")

    except ImportError as e:
        print(f"  {FAIL} paramiko not installed — run: pip install paramiko")
        results["kali_ssh"] = False

    print()

    # --- Summary ---
    print("=" * 55)
    print("  SUMMARY")
    print("=" * 55)

    total = len(results)
    passed = sum(1 for v in results.values() if v)
    failed = total - passed

    for name, ok in results.items():
        icon = PASS if ok else FAIL
        print(f"  {icon} {name}")

    print()
    if failed == 0:
        print(f"\033[92m  All {total} checks passed — Ascended33 fully operational!\033[0m")
    else:
        print(f"\033[93m  {passed}/{total} checks passed — see failures above\033[0m")
        print()
        print("  Troubleshooting:")
        if not results.get("obsidian"):
            print("  • Obsidian: Open Obsidian on Windows, verify Local REST API plugin is enabled")
        if not results.get("kali_ssh"):
            print("  • Kali SSH: Run scripts/setup_kali.sh on Kali, set up SSH keys")
            print("              Update config/config.yaml with correct Kali IP")
        if not results.get("hexstrike_local") and not results.get("hexstrike_kali"):
            print("  • hexstrike-ai: Run scripts/setup_kali.sh on Kali VM")
    print()


if __name__ == "__main__":
    main()
    sys.exit(0)
