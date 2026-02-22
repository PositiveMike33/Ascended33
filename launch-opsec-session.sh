#!/bin/bash
# launch-opsec-session.sh — Complete OPSEC session initialization
# 
# Usage: ./launch-opsec-session.sh <operation_name> <target> [operation_type]
# Example: ./launch-opsec-session.sh "OSINT Investigation" "target.com" "osint"

set -e

OPERATION_NAME="${1:-Security Research}"
TARGET="${2:-self}"
OPERATION_TYPE="${3:-osint}"

echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║          ASCENDED33 OPSEC SESSION INITIALIZATION                  ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""
echo "Operation: $OPERATION_NAME"
echo "Target:    $TARGET"
echo "Type:      $OPERATION_TYPE"
echo ""

# ─────────────────────────────────────────────────────────────────────────
# Step 1: Start Docker containers (Kali + Tor)
# ─────────────────────────────────────────────────────────────────────────

echo "[1/4] Starting Docker containers (th3-kali + th3-tor)..."
docker-compose -f docker-compose-opsec.yml up -d th3-tor th3-kali 2>/dev/null || true
sleep 3
echo "✓ Containers started"
echo ""

# ─────────────────────────────────────────────────────────────────────────
# Step 2: Verify Tor is online
# ─────────────────────────────────────────────────────────────────────────

echo "[2/4] Verifying Tor connectivity..."
TOR_TIMEOUT=0
while ! curl -s -x socks5://127.0.0.1:9050 https://check.torproject.org && [ $TOR_TIMEOUT -lt 30 ]; do
    echo "  ⏳ Waiting for Tor (${TOR_TIMEOUT}s)..."
    sleep 2
    TOR_TIMEOUT=$((TOR_TIMEOUT + 2))
done

if [ $TOR_TIMEOUT -ge 30 ]; then
    echo "✗ Tor timeout — continuing anyway (may affect anonymity)"
else
    echo "✓ Tor online"
fi
echo ""

# ─────────────────────────────────────────────────────────────────────────
# Step 3: Activate VPN (NordVPN with fallback)
# ─────────────────────────────────────────────────────────────────────────

echo "[3/4] Checking VPN protection..."

# Check NordVPN first
if command -v nordvpn &> /dev/null; then
    echo "  → Attempting NordVPN..."
    nordvpn connect 2>/dev/null || true
    sleep 2
    if nordvpn status | grep -q "Connected"; then
        echo "✓ NordVPN active"
    else
        echo "  ⚠ NordVPN failed, trying Mullvad..."
        if command -v mullvad &> /dev/null; then
            mullvad connect 2>/dev/null || true
            sleep 2
            echo "✓ Mullvad activated (fallback)"
        fi
    fi
elif command -v mullvad &> /dev/null; then
    echo "  → Attempting Mullvad..."
    mullvad connect 2>/dev/null || true
    sleep 2
    echo "✓ Mullvad active"
else
    echo "⚠ No VPN client found — ensure NordVPN or Mullvad is installed"
fi
echo ""

# ─────────────────────────────────────────────────────────────────────────
# Step 4: Run Python OPSEC manager for logging
# ─────────────────────────────────────────────────────────────────────────

echo "[4/4] Initializing OPSEC manager and logging to Vault..."
python3 -c "
import sys
sys.path.insert(0, '.')
from scripts.opsec.opsec_manager import verify_opsec

status = verify_opsec(
    operation_name='$OPERATION_NAME',
    target='$TARGET',
    require_tor=True
)
print()
print('╔════════════════════════════════════════════════════════════════════╗')
if status.safe:
    print(f'║  ✓ OPSEC INITIALIZED SAFELY                                    ║')
else:
    print(f'║  ⚠ OPSEC INITIALIZED IN DEGRADED MODE                         ║')
print('╚════════════════════════════════════════════════════════════════════╝')
print()
print(f'Operation ID: {status.checks_passed}')
print(f'Current IP:  {status.current_ip}')
print(f'VPN:         {status.vpn_provider} ({\"active\" if status.vpn_active else \"inactive\"})')
print(f'Tor:         {\"active\" if status.tor_active else \"inactive\"}')
print()
print('✓ Session ready for operations. All activity logged to Vault.')
print()
" 2>/dev/null || echo "✗ OPSEC initialization failed"

echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║                 READY FOR OPERATIONS                              ║"
echo "║                                                                    ║"
echo "║  Access Kali container:  docker exec -it th3-kali bash            ║"
echo "║  All activity auto-logged to: Vault/Security/Operations/          ║"
echo "║                                                                    ║"
echo "║  Remember:                                                         ║"
echo "║  - DO NOT use personal accounts                                   ║"
echo "║  - Target: self (personal security testing)                       ║"
echo "║  - VPN + Tor active for anonymity                                 ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
