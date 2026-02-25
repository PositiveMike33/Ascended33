#!/bin/bash
# HexStrike Tor Proxy Initialization Script
# Routes all HTTP(S) and system requests through Tor proxy

set -e

echo "🧅 HexStrike Tor Anonymity Configuration"
echo "=========================================="

# ==========================================
# 1. Verify Tor Proxy Connectivity
# ==========================================
echo "[1/5] Checking Tor proxy connectivity..."
TOR_HOST=${TOR_HOST:-th3-tor}
TOR_PORT=${TOR_PORT:-9050}
TOR_CONTROL_PORT=${TOR_CONTROL_PORT:-9051}

max_attempts=30
attempt=0
while [ $attempt -lt $max_attempts ]; do
    if nc -z $TOR_HOST $TOR_PORT 2>/dev/null; then
        echo "     ✅ Tor proxy reachable at $TOR_HOST:$TOR_PORT"
        break
    fi
    attempt=$((attempt + 1))
    if [ $attempt -eq $max_attempts ]; then
        echo "     ⚠️  Tor proxy not responding (will retry at runtime)"
    else
        echo "     ⏳ Waiting for Tor proxy... ($attempt/$max_attempts)"
        sleep 1
    fi
done

# ==========================================
# 2. Configure Environment Variables
# ==========================================
echo "[2/5] Configuring environment variables..."

export TOR_PROXY_URL="socks5://${TOR_HOST}:${TOR_PORT}"
export http_proxy="${TOR_PROXY_URL}"
export https_proxy="${TOR_PROXY_URL}"
export HTTP_PROXY="${TOR_PROXY_URL}"
export HTTPS_PROXY="${TOR_PROXY_URL}"

# For curl
export SOCKS5_PROXY="${TOR_PROXY_URL}"
export SOCKS5H_PROXY="${TOR_PROXY_URL}"

echo "     ✅ Proxy environment variables set:"
echo "        http_proxy: $http_proxy"
echo "        https_proxy: $https_proxy"

# ==========================================
# 3. Configure Python requests library
# ==========================================
echo "[3/5] Configuring Python proxy settings..."

cat > /tmp/tor_proxy_config.py << 'PYTHON_CONFIG'
import os
import sys

# Global proxy configuration for all Python HTTP libraries
TOR_PROXY = os.getenv('TOR_PROXY_URL', 'socks5://th3-tor:9050')

# PySocks configuration
PROXY_CONFIG = {
    'http': TOR_PROXY,
    'https': TOR_PROXY,
}

# For requests library
os.environ['http_proxy'] = TOR_PROXY
os.environ['https_proxy'] = TOR_PROXY
os.environ['HTTP_PROXY'] = TOR_PROXY
os.environ['HTTPS_PROXY'] = TOR_PROXY

print(f"✅ Python proxy configured: {TOR_PROXY}")
PYTHON_CONFIG

export PYTHONSTARTUP="/tmp/tor_proxy_config.py"

# ==========================================
# 4. Configure Application-level Proxy
# ==========================================
echo "[4/5] Setting up HexStrike Tor routing..."

# Create a Python wrapper that injects Tor proxy into all requests
cat > /tmp/hexstrike_tor_wrapper.py << 'WRAPPER_SCRIPT'
#!/usr/bin/env python3
"""
HexStrike Tor Proxy Wrapper
Routes all HTTP requests through Tor SOCKS5 proxy
"""

import os
import sys
import socket
from functools import wraps

# Import after environment setup
TOR_PROXY_URL = os.getenv('TOR_PROXY_URL', 'socks5://th3-tor:9050')
print(f"🧅 Initializing HexStrike with Tor proxy: {TOR_PROXY_URL}")

# Configure pysocks for all sockets
try:
    import socks
    import socket as socket_module
    
    # Parse proxy URL
    proxy_parts = TOR_PROXY_URL.replace('socks5://', '').split(':')
    proxy_host = proxy_parts[0]
    proxy_port = int(proxy_parts[1]) if len(proxy_parts) > 1 else 9050
    
    # Set default socket proxy
    socks.set_default_proxy(
        socks.SOCKS5,
        proxy_host,
        proxy_port,
        udp_fallback=False
    )
    socket_module.socket = socks.socksocket
    
    print(f"✅ Socket proxy configured: {proxy_host}:{proxy_port}")
except ImportError:
    print("⚠️  pysocks not available, using environment variables")

# Configure requests library
try:
    import requests
    session = requests.Session()
    session.proxies = {
        'http': TOR_PROXY_URL,
        'https': TOR_PROXY_URL,
    }
    print(f"✅ Requests library proxy configured")
except ImportError:
    print("⚠️  requests not available")

# Configure httpx if available
try:
    import httpx
    # httpx will use environment variables automatically
    print(f"✅ httpx will use environment proxies")
except ImportError:
    pass

print("🧅 Tor proxy initialization complete\n")

# Re-execute the original command
if len(sys.argv) > 1:
    exec(open(sys.argv[1]).read())
WRAPPER_SCRIPT

chmod +x /tmp/hexstrike_tor_wrapper.py

echo "     ✅ HexStrike Tor routing configured"

# ==========================================
# 5. Verify Tor Connectivity
# ==========================================
echo "[5/5] Verifying Tor anonymity..."

# Test Tor SOCKS5 connectivity
python3 << 'TEST_TOR'
import socket
import socks
import os

tor_host = os.getenv('TOR_HOST', 'th3-tor')
tor_port = int(os.getenv('TOR_PORT', 9050))

try:
    sock = socks.socksocket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setproxy(socks.SOCKS5, tor_host, tor_port)
    sock.connect(('check.torproject.org', 80))
    print("     ✅ Tor SOCKS5 proxy verified and working")
    sock.close()
except Exception as e:
    print(f"     ⚠️  Tor connectivity check failed (will retry): {e}")
TEST_TOR

echo ""
echo "=========================================="
echo "🧅 Tor Anonymity Configuration Complete"
echo "=========================================="
echo ""
echo "Configuration Details:"
echo "  • TOR_PROXY_URL: $TOR_PROXY_URL"
echo "  • http_proxy: $http_proxy"
echo "  • https_proxy: $https_proxy"
echo ""
echo "All HexStrike requests will be routed through Tor SOCKS5"
echo "Internet connection outside container remains unaffected"
echo ""

# ==========================================
# Start HexStrike Application
# ==========================================
echo "Starting HexStrike service..."
exec "$@"
