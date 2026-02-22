"""
test-vault-connection.py — Test Obsidian Vault REST API connection

Usage:
    python3 test-vault-connection.py

This script tests the connection and provides troubleshooting help.
"""

import sys
from pathlib import Path

# Add repo to path
sys.path.insert(0, str(Path(__file__).parent))


def test_vault_connection():
    """Test Obsidian Vault REST API connection with detailed diagnostics"""

    print("\n" + "=" * 70)
    print("OBSIDIAN VAULT REST API CONNECTION TEST")
    print("=" * 70 + "\n")

    # Step 1: Load configuration
    print("[1/5] Loading configuration...")
    try:
        import yaml

        with open("config/config.yaml") as f:
            config = yaml.safe_load(f)
            vault_cfg = config.get("vault", {})

        base_url = vault_cfg.get("base_url", "http://localhost:27123")
        api_key = vault_cfg.get("api_key", "")
        mode = vault_cfg.get("mode", "rest_api")

        print(f"  ✓ Mode: {mode}")
        print(f"  ✓ Base URL: {base_url}")
        print(f"  ✓ API Key: {'*' * len(api_key) if api_key else '(NOT SET)'}")

    except FileNotFoundError:
        print("  ✗ config/config.yaml not found")
        print("     → Copy config.example.yaml to config.yaml first")
        return False
    except Exception as e:
        print(f"  ✗ Failed to load config: {e}")
        return False

    # Step 2: Check API key
    print("\n[2/5] Checking API key...")
    if not api_key or api_key.strip() == "":
        print("  ✗ API key is EMPTY!")
        print("\n  To fix:")
        print("    1. Open Obsidian")
        print("    2. Settings → Community Plugins → Local REST API")
        print("    3. Click gear icon to see your API key")
        print("    4. Copy the key (long alphanumeric string)")
        print("    5. Edit config/config.yaml")
        print("    6. Update: api_key: \"your_key_here\"")
        return False
    else:
        print(f"  ✓ API key is set ({len(api_key)} chars)")

    # Step 3: Check if Obsidian API is reachable
    print("\n[3/5] Testing Obsidian Vault connection...")
    try:
        import requests

        # Test basic connectivity
        response = requests.get(f"{base_url}/", timeout=5)
        print(f"  ✓ Vault API reachable (HTTP {response.status_code})")

    except requests.ConnectionError:
        print(f"  ✗ Cannot connect to {base_url}")
        print("\n  To fix:")
        print("    1. Verify Obsidian is running (check system tray)")
        print("    2. Verify Vault is open: D:\\Vault")
        print("    3. Verify Local REST API plugin is ENABLED (toggle on)")
        print("    4. Check if Obsidian is on different port (not 27123)")
        return False
    except Exception as e:
        print(f"  ✗ Connection error: {e}")
        return False

    # Step 4: Test authentication
    print("\n[4/5] Testing authentication...")
    try:
        headers = {
            "Content-Type": "application/json",
        }

        # Try with Bearer token
        if api_key and not api_key.startswith("Bearer "):
            headers["Authorization"] = f"Bearer {api_key}"
        else:
            headers["Authorization"] = api_key

        # Try to list vault
        response = requests.get(f"{base_url}/vault/", headers=headers, timeout=5)

        if response.status_code == 200:
            print("  ✓ Authentication successful!")
        elif response.status_code == 401:
            print("  ✗ Authentication FAILED (401 Unauthorized)")
            print("\n  To fix:")
            print("    1. Verify API key is correct (no extra spaces)")
            print("    2. Check if key format is correct (should be alphanumeric)")
            print("    3. Try regenerating API key in Obsidian")
            print("    4. Update config/config.yaml with new key")
            return False
        else:
            print(f"  ⚠ Unexpected response: HTTP {response.status_code}")
            print(f"     Response: {response.text[:100]}")

    except Exception as e:
        print(f"  ✗ Auth check failed: {e}")
        return False

    # Step 5: Test actual vault operations
    print("\n[5/5] Testing vault operations...")
    try:
        from vault_sync.vault_api import ObsidianVaultClient

        vault = ObsidianVaultClient.from_config()

        # Try to read a template
        try:
            content = vault.read_note("Templates/osint_report.md")
            if content:
                print(f"  ✓ Successfully read template ({len(content)} chars)")
            else:
                print("  ⚠ Template exists but is empty (this is OK)")

        except Exception as e:
            print(f"  ⚠ Could not read template: {e}")
            print("     (This is OK if template doesn't exist yet)")

        print("  ✓ Vault client works!")

    except Exception as e:
        print(f"  ✗ Vault operations failed: {e}")
        return False

    # Success!
    print("\n" + "=" * 70)
    print("✓ ALL TESTS PASSED - Vault connection is working!")
    print("=" * 70)
    print("\nYou can now:")
    print("  - Use Streamlit dashboard's 'Full Vault Sync' button")
    print("  - Run OPSEC operations with auto-logging to Vault")
    print("  - Access operations in: D:\\Vault\\Security\\Operations\\")
    print()

    return True


if __name__ == "__main__":
    success = test_vault_connection()
    sys.exit(0 if success else 1)
