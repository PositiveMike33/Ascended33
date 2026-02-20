# OPSEC Complete Implementation Guide

**Ascended33 OPSEC System** — Full anonymity & security orchestration for self-testing operations.

## Overview

This OPSEC system provides:
- ✅ **VPN Protection** — NordVPN with automatic fallback to Mullvad/ProtonVPN
- ✅ **Tor Routing** — Always-active via `th3-tor` Docker container
- ✅ **Docker Containerization** — Isolated Kali environment (`th3-kali`)
- ✅ **Operation Logging** — Auto-logs all activities to Obsidian Vault
- ✅ **Anonymity Verification** — IP masking, DNS leak checks, Tor validation
- ✅ **Self-Testing Only** — Target = yourself for authorized security research

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│ ASCENDED33 OPSEC LAYER                                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. VPN PROTECTION                                          │
│     ├─ Primary: NordVPN                                    │
│     ├─ Fallback: Mullvad                                   │
│     └─ Fallback: ProtonVPN                                 │
│                                                             │
│  2. TOR ROUTING (Always Active)                             │
│     ├─ th3-tor Docker container                            │
│     ├─ SOCKS5 proxy: localhost:9050                        │
│     └─ Auto-health checks                                  │
│                                                             │
│  3. SECURITY ISOLATION                                      │
│     ├─ th3-kali (Kali Linux container)                     │
│     ├─ No personal accounts                                │
│     └─ Shared /root/workspaces volume                      │
│                                                             │
│  4. OPERATION LOGGING                                       │
│     ├─ Every operation timestamped                         │
│     ├─ Auto-logged to Vault: Security/Operations/          │
│     ├─ OPSEC status captures                               │
│     └─ Finding documentation                               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Quick Start

### 1. Prerequisites

Ensure you have installed:
- Docker & Docker Compose
- One VPN client:
  - `nordvpn` (primary)
  - `mullvad` (fallback)
  - `protonvpn` (fallback)
- Python 3.11+
- Obsidian with Local REST API plugin running

### 2. Make launch script executable

```bash
chmod +x launch-opsec-session.sh
```

### 3. Start a secure session

```bash
# Start OSINT investigation on target "self"
./launch-opsec-session.sh "OSINT Self-Testing" "self" "osint"

# Access the Kali container
docker exec -it th3-kali bash

# Inside th3-kali, all traffic routes through VPN + Tor
# Run your tools here (nmap, nuclei, etc.)
```

---

## Configuration

### config.yaml — OPSEC Settings

```yaml
opsec:
  # VPN
  vpn_enabled: true
  vpn_provider: "mullvad"           # Primary provider
  require_vpn: true

  # Tor
  tor_enabled: true
  tor_docker_container: "th3-tor"
  require_tor_for_darkweb: true

  # Containers
  kali_docker_container: "th3-kali"

  # Vault logging
  vault_enabled: true
  vault_operations_path: "Security/Operations"

  # Anonymity requirements
  anonymous_accounts: true          # No personal logins
  browser_isolation: true           # Isolated browser profile
```

### docker-compose-opsec.yml

Defines three services:
- **th3-kali** — Kali Linux security container
- **th3-tor** — Tor exit node
- **hexstrike-ai** (optional) — Automation framework

### config/torrc

Tor configuration for SOCKS5 proxy on port 9050.

---

## Usage Workflows

### Workflow 1: Self-Testing OSINT Investigation

```bash
# 1. Launch secure session
./launch-opsec-session.sh "OSINT Investigation" "self" "osint"

# Output:
# [1/4] Starting Docker containers (th3-kali + th3-tor)...
# [2/4] Verifying Tor connectivity...
# [3/4] Checking VPN protection...
# [4/4] Initializing OPSEC manager and logging to Vault...
#
# ✓ Operation logged to Vault: Security/Operations/2026-02-19/...

# 2. Access Kali container
docker exec -it th3-kali bash

# 3. Inside th3-kali — all traffic through VPN + Tor
# Example: Check your own IP
curl https://httpbin.org/ip
# Returns: 45.88.190.23 (VPN-masked IP)

# Check via Tor
curl -x socks5://th3-tor:9050 https://check.torproject.org
# Confirms Tor routing

# 4. Run security tools (nmap, nuclei, sqlmap, etc.)
# All auto-logged to Vault

# 5. Exit and close operation
exit
```

### Workflow 2: Tor-Only Dark Web Monitoring

```bash
./launch-opsec-session.sh "Dark Web Threat Intel" "self" "threat_intel"

# Inside th3-kali:
# Access .onion sites via Tor
curl -x socks5://th3-tor:9050 http://example.onion
```

### Workflow 3: Using with hexstrike-ai

```bash
# Start all services including hexstrike-ai
docker-compose -f docker-compose-opsec.yml up -d

# From within th3-kali, connect to hexstrike-ai on localhost:8888
# All requests auto-tunneled through VPN + Tor
```

---

## VPN Failover Logic

The system automatically selects from this chain:

1. **NordVPN** (primary)
   - Command: `nordvpn connect`
   - Fallback: ✓ (if enabled)

2. **Mullvad** (secondary)
   - Command: `mullvad connect`
   - Fallback: ✓ (if enabled)

3. **ProtonVPN** (tertiary)
   - Command: `protonvpn c`
   - Fallback: Warn

If all fail → **DEGRADED MODE** (Tor still active, but VPN protection lost)

### Activate manually

```bash
# Check NordVPN status
nordvpn status

# Activate NordVPN
nordvpn connect

# If NordVPN not working, activate Mullvad
mullvad connect

# Verify (should show masked IP)
curl https://httpbin.org/ip
```

---

## Tor Verification

Tor is always active and verified:

```bash
# Check Tor container
docker ps | grep th3-tor

# Test Tor connectivity from host
curl -x socks5://127.0.0.1:9050 https://check.torproject.org/api/ip

# From within th3-kali, check router
curl -x socks5://th3-tor:9050 https://check.torproject.org/api/ip
```

---

## Operation Logging to Vault

Every operation is auto-logged to Obsidian Vault:

```
D:\Vault\
└── Security/Operations/
    └── 2026-02-19/
        └── 20260219_150330-OSINT-Investigation.md
            ├── Operation ID: 20260219_150330
            ├── Type: osint
            ├── Target: self
            ├── OPSEC Status (VPN/Tor/IP)
            ├── Findings section
            ├── Timeline
            └── Status (In Progress → Completed)
```

### Log a finding

```python
from scripts.opsec.operation_logger import get_operation_logger

logger = get_operation_logger()
logger.start_operation(...)
logger.log_finding("vulnerability", "SQL Injection", "Input not sanitized", severity="high")
logger.end_operation("completed", summary="3 SQL injections found", total_findings=3)
```

---

## Anonymity Checklist

Before starting any sensitive operation:

- [ ] VPN active (`nordvpn status` or `mullvad status`)
- [ ] Tor container running (`docker ps | grep th3-tor`)
- [ ] IP masked (run `curl https://httpbin.org/ip`)
- [ ] Tor verified (curl via SOCKS5 returns .onion-safe response)
- [ ] No personal accounts logged in on test systems
- [ ] Operation logged to Vault with timestamp
- [ ] Target is only "self" (personal security research)
- [ ] Browser profile isolated (no history/cookies)

---

## Troubleshooting

### Tor won't start

```bash
docker logs th3-tor
# Check if port 9050 is already in use
netstat -tulpn | grep 9050
```

### VPN not connecting

```bash
# Verify NordVPN installed
which nordvpn

# Check status
nordvpn status

# If frozen, restart
nordvpn disconnect
nordvpn connect
```

### Docker compose error

```bash
# Ensure Docker daemon is running
sudo systemctl start docker

# Rebuild images
docker-compose -f docker-compose-opsec.yml build
docker-compose -f docker-compose-opsec.yml up -d
```

---

## Security Best Practices

1. **Always use VPN + Tor** — Never trust a single layer
2. **Never log personal accounts** — Only use disposable/test accounts
3. **Self-test only** — Target is always "self" or authorized scope
4. **Verify anonymity** — Check IP before every operation
5. **Log operations** — Vault history is your audit trail
6. **Clean up after** — Use `scripts/opsec/trace_cleaner.py` before shutdown
7. **Rotate VPN** — Periodically disconnect/reconnect
8. **Monitor Tor** — Ensure Tor is always active

---

## Commands Reference

```bash
# Start entire OPSEC session (recommended)
./launch-opsec-session.sh "Operation Name" "target" "type"

# Manually start containers
docker-compose -f docker-compose-opsec.yml up -d

# Access Kali container
docker exec -it th3-kali bash

# Check Tor status
docker logs th3-tor

# Check OPSEC status (Python)
python3 -c "from scripts.opsec.opsec_manager import verify_opsec; verify_opsec()"

# Stop and clean up
docker-compose -f docker-compose-opsec.yml down

# Clean traces (before shutdown)
python3 scripts/opsec/trace_cleaner.py --scope full
```

---

## Support & Troubleshooting

For issues:
1. Check logs: `docker-compose -f docker-compose-opsec.yml logs`
2. Verify IP masking: `curl https://httpbin.org/ip`
3. Test Tor: `curl -x socks5://127.0.0.1:9050 https://check.torproject.org`
4. Check Vault logging: Open Vault → Security/Operations/

---

*Last Updated: 2026-02-19*
*Ascended33 OPSEC System v2.0*
