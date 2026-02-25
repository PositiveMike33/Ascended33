# 🧅 HexStrike + Tor Anonymity Integration

**Status**: ✅ Complete and Operational  
**Last Updated**: 2026-02-19

---

## Overview

HexStrike is now configured to route **all HTTP/HTTPS traffic through Tor SOCKS5 proxy** while keeping the rest of your system unaffected. This provides **complete anonymity** for security analysis and penetration testing.

### Architecture

```
┌─────────────────────────────────────────────────────────┐
│                Your Host System                         │
│  (Normal Internet Connection - UNAFFECTED)              │
└──────────────────────┬──────────────────────────────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼
   ┌─────────┐    ┌──────────┐   ┌──────────┐
   │th3-kali │    │th3-hackr │   │Other th3 │
   │Direct   │    │GPT Direct│   │Containers│
   │Internet │    │Internet  │   │Direct    │
   └─────────┘    └──────────┘   └──────────┘

        ┌──────────────────────────┐
        │   th3-hexstrike          │
        │   (HexStrike Service)    │
        │   Port 8001              │
        └──────────┬───────────────┘
                   │
        (All requests route through)
                   │
        ┌──────────▼───────────────┐
        │   th3-tor SOCKS5         │
        │   (Anonymous Proxy)      │
        │   Port 9050              │
        └──────────┬───────────────┘
                   │
        (Tor Network - Multiple Hops)
                   │
        ┌──────────▼───────────────┐
        │   Internet              │
        │   (Anonymized IP)        │
        └─────────────────────────┘
```

---

## Current Configuration

### HexStrike Environment Variables

All HexStrike requests automatically use these proxy settings:

```
TOR_ENABLED=true
TOR_HOST=th3-tor
TOR_PORT=9050
TOR_PROXY_URL=socks5://th3-tor:9050

# Applied to all HTTP libraries
http_proxy=socks5://th3-tor:9050
https_proxy=socks5://th3-tor:9050
SOCKS5_PROXY=socks5://th3-tor:9050
```

### Security Features

✅ **Header Stripping**: Removes identifying headers
- X-Forwarded-For (client IP)
- X-Real-IP (real client IP)
- User-Agent (system info)
- Accept-Language (location hint)

✅ **Isolated Circuits**: Each request can use separate Tor circuits  
✅ **SSL/TLS 1.3**: Encrypted communication  
✅ **SOCKS5 Proxy**: Encrypted Tor protocol  

---

## How It Works

### 1. Request Flow (Inside HexStrike Container)

```
HexStrike Application
    ↓
Python requests library (automatically uses proxies)
    ↓
PySocks library (SOCKS5 client)
    ↓
th3-tor SOCKS5 server (port 9050)
    ↓
Tor Network (3-hop circuit)
    ↓
Destination Server
    ↓
Response back through Tor
```

### 2. Initialization Process

When th3-hexstrike starts:
1. Waits for th3-tor to be ready (health check)
2. Verifies SOCKS5 connectivity to th3-tor:9050
3. Sets environment variables for all HTTP libraries
4. Configures Python's socket layer for SOCKS5
5. Injects Tor proxy into requests library
6. Starts HexStrike application

### 3. Proxy Configuration Layers

**Layer 1: Environment Variables**
```bash
http_proxy=socks5://th3-tor:9050
https_proxy=socks5://th3-tor:9050
```
Picked up by: curl, wget, system tools

**Layer 2: Python Libraries**
```python
SOCKS5_PROXY=socks5://th3-tor:9050
```
Used by: requests, httpx, urllib

**Layer 3: Socket Layer**
```python
socks.set_default_proxy(SOCKS5, 'th3-tor', 9050)
```
Catches any remaining socket calls

---

## Usage

### Access HexStrike API (via Tor)

```bash
# From your host, requests go through HexStrike → Tor → Internet
curl http://localhost:8001/api/scan

# Check your anonymity (returns Tor exit node IP, not your real IP)
docker exec th3-hexstrike curl --socks5 th3-tor:9050 https://api.ipify.org
```

### Run Security Scans

All scanning automatically uses Tor:

```bash
# Port scan (through Tor)
docker exec th3-hexstrike python3 -c "
import requests
proxies = {'http': 'socks5://th3-tor:9050'}
r = requests.get('http://target.com', proxies=proxies)
"

# Web reconnaissance (through Tor)
docker exec th3-hexstrike hexstrike scan --target example.com --anonymous
```

### Access Vault from HexStrike

Reports and findings saved to your Vault (also readable via Tor analysis):

```bash
# Inside HexStrike container
ls /vault/_BRAIN/hexstrike_reports/
cat /vault/RAPPORT\ QUOTIDIEN/findings.md
```

---

## Verification

### 1. Run Verification Script

```powershell
.\verify-hexstrike-tor.ps1
```

Output shows:
- ✅ Containers running
- ✅ Network connectivity
- ✅ Proxy environment variables
- ✅ SOCKS5 connectivity test
- ✅ API health status

### 2. Manual Verification

```bash
# Check proxy environment in container
docker exec th3-hexstrike env | grep -i proxy

# Check network connectivity to Tor
docker exec th3-hexstrike ping th3-tor

# Verify Tor proxy working
docker exec th3-hexstrike python3 << 'EOF'
import socket
import socks

sock = socks.socksocket()
sock.setproxy(socks.SOCKS5, 'th3-tor', 9050)
sock.connect(('check.torproject.org', 80))
print("✅ Tor proxy working!")
sock.close()
EOF

# Check your exit IP (should be Tor exit node, not your real IP)
docker exec th3-hexstrike curl --socks5 th3-tor:9050 https://api.ipify.org
```

### 3. Monitor Tor Traffic

```bash
# View HexStrike logs (shows Tor connections)
docker logs th3-hexstrike -f | grep -i tor

# View Tor logs
docker logs th3-tor -f
```

---

## Important Notes

### What Goes Through Tor

✅ All HTTP/HTTPS requests from HexStrike  
✅ DNS queries (routed through Tor)  
✅ TCP connections to remote servers  
✅ API calls to external services  

### What Does NOT Go Through Tor

❌ Communication between containers on docker network (direct)  
❌ Communication from host to containers (direct)  
❌ Other containers' traffic (unless configured separately)  
❌ Host system internet (completely unaffected)  

### Security Best Practices

⚠️ **WARNING**: While Tor provides anonymity, remember:
1. Exit node can see unencrypted traffic
2. Use HTTPS for all sensitive communications
3. Disable plugins/extensions that might leak IP
4. Don't maximize browser window (fingerprinting)
5. Multiple requests in session may be linked

✅ **RECOMMENDATIONS**:
- Use HTTPS/TLS for all connections
- Enable certificate verification (already configured)
- Rotate Tor circuits when needed
- Use isolated circuits per request for critical scans

---

## Configuration Files

### Location: D:\Vault\Vault\

**docker-compose.yml**
- Updated with full Tor configuration for th3-hexstrike
- Sets all proxy environment variables
- Mounts Tor config files

**hexstrike-tor-config.conf**
- Tor proxy settings
- Security parameters
- Header stripping configuration
- Anonymity levels

**tor_hexstrike_init.sh**
- Initialization script
- Verifies Tor connectivity
- Configures socket-level proxy
- Sets up Python proxy settings

---

## Advanced Configuration

### Modify Tor Settings

Edit `hexstrike-tor-config.conf`:

```ini
[network]
# Use different Tor circuits per request
NEW_CIRCUIT_PER_REQUEST=true

# Increase timeouts for slow Tor connections
CONNECT_TIMEOUT=60
READ_TIMEOUT=120

# Use specific Tor exit country
TOR_EXIT_COUNTRY=US
```

Then restart:
```bash
docker restart th3-hexstrike
```

### Route Other Containers Through Tor

To route th3-kali or other containers through Tor as well:

```yaml
  th3-kali:
    # ... existing config ...
    environment:
      - http_proxy=socks5://th3-tor:9050
      - https_proxy=socks5://th3-tor:9050
      # ... other vars ...
```

### Monitor Tor Circuit Usage

```bash
# Connect to Tor control port
docker exec th3-tor nc localhost 9051

# Issue commands like GETINFO or NEWIDENTITY
# (requires Tor control port authentication)
```

---

## Troubleshooting

### HexStrike can't connect to Tor

```bash
# Check both containers running
docker ps | grep -E "th3-hexstrike|th3-tor"

# Check network connectivity
docker exec th3-hexstrike ping th3-tor

# Check Tor SOCKS5 port is listening
docker exec th3-tor ss -tlnp | grep 9050
```

### Slow Tor connections

```bash
# Tor builds 3-hop circuits - normal latency is 2-5 seconds
# For faster but less anonymous scanning, use direct requests:
docker exec th3-hexstrike python3 -c "
import requests
# Direct (not through Tor)
r = requests.get('http://fast-target.com')
"
```

### IP Still Leaking

```bash
# Verify your exit IP is not your real IP
docker exec th3-hexstrike curl --socks5 th3-tor:9050 https://api.ipify.org

# Check environment variables are set
docker exec th3-hexstrike env | grep -i proxy
```

### HexStrike API not responding

```bash
# Check if service started
docker logs th3-hexstrike

# Restart service
docker restart th3-hexstrike

# Check if port is listening
docker exec th3-hexstrike ss -tlnp | grep 8001
```

---

## Performance Metrics

### Expected Latency (First Request)

- Tor circuit establishment: 2-5 seconds
- Tor exit node assignment: 1-3 seconds
- Actual request: +50-200ms (depends on exit node)
- **Total first request**: ~3-8 seconds

### Subsequent Requests

- Circuit reuse: ~100-500ms latency overhead
- **Typical request time**: Original + 200-500ms

### Bandwidth

Tor typically provides:
- **Download**: 1-10 Mbps (depending on circuit)
- **Upload**: Similar to download
- **Sustained use**: May be throttled after heavy usage

---

## Logs and Monitoring

### View HexStrike Tor Logs

```bash
docker logs th3-hexstrike -f | grep -E "TOR|proxy|connect"
```

### View Tor Activity

```bash
docker logs th3-tor -f
```

### Check Circuit Status

```bash
docker exec th3-hexstrike python3 << 'EOF'
import socket
import socks

sock = socks.socksocket()
sock.setproxy(socks.SOCKS5, 'th3-tor', 9050)
sock.connect(('check.torproject.org', 80))
response = sock.recv(4096)
print(response.decode()[:500])
EOF
```

---

## Emergency Disable

### Temporarily Disable Tor (Direct Internet)

```bash
# Stop th3-hexstrike
docker stop th3-hexstrike

# Restart without Tor proxy
docker run -d --name th3-hexstrike-direct \
  -p 8001:8001 \
  --network ascended33_ascended33-network \
  -v D:/Vault/Vault:/vault:rw \
  th3-hexstrike:latest
```

### Revert to Tor-Enabled

```bash
docker rm -f th3-hexstrike-direct
docker restart th3-hexstrike
```

---

## Related Documentation

- **Vault Integration**: `VAULT_INTEGRATION_REPORT.md`
- **Quick Start**: `VAULT_QUICKSTART.md`
- **Docker Compose**: `docker-compose.yml`
- **Verification**: `verify-hexstrike-tor.ps1`

---

## Summary

✅ **HexStrike is fully anonymized through Tor**

- All HTTP/HTTPS traffic routed through SOCKS5
- Headers stripped for anonymity
- Other containers and host unaffected
- Can be disabled/reconfigured at any time
- Full audit trail in logs
- Integration with Vault brain maintained

**Use Case**: Perfect for anonymous security research, pentesting, and threat analysis.

**Status**: 🟢 Operational and Ready
