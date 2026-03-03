---
type: OPSEC
tags: [TOR, OPSEC, anonymity]
updated: 2026-03-03
---

# ⊛ Tor OPSEC Master Checklist

## PRE-OPERATION
- [ ] Physical location: Not home/office for sensitive ops
- [ ] Device: Dedicated or clean VM (th3-kali)
- [ ] VPN active BEFORE launching Tor
- [ ] DNS leak test passed (dnsleaktest.com via Tor)
- [ ] Browser: Tor Browser or configured Firefox (no JS)
- [ ] Real accounts: Not logged into ANY personal service
- [ ] Browser history, cookies, cache cleared
- [ ] Threat model documented for this operation

## TOR CONFIGURATION
```bash
# Verify Tor is routing correctly
curl --socks5-hostname 127.0.0.1:9050 https://check.torproject.org/api/ip
# Expected: {"IsTor": true, "IP": "x.x.x.x"}

# Use proxychains for CLI tools
proxychains4 -q tool [args]

# Renew circuit (signal Tor)
echo -e 'AUTHENTICATE ""\nSIGNAL NEWNYM\nQUIT' | nc 127.0.0.1 9051
```

## DURING OPERATION
- [ ] Circuit renewed every 10 minutes
- [ ] No file downloads without sandboxing (th3-kali VM)
- [ ] No login to real personal accounts
- [ ] No reuse of usernames/emails across ops
- [ ] All findings timestamped immediately in vault
- [ ] Screenshots: No personal identifiers visible
- [ ] Tabs: Never mix personal + operational browsing

## OPSEC THREAT MATRIX
| Threat | Risk | Mitigation |
|--------|------|------------|
| IP leak via WebRTC | HIGH | Disable WebRTC, use Tor Browser |
| DNS leak | HIGH | Use Tor DNS only (9053) |
| JS fingerprinting | MEDIUM | NoScript, JS disabled |
| Timing attacks | MEDIUM | Add random delays in scripts |
| Exit node MITM | MEDIUM | HTTPS only, certificate pinning |
| Metadata in files | HIGH | Strip with exiftool before sharing |
| Correlation attacks | LOW | Vary circuit, entry guards |

## POST-OPERATION
- [ ] All findings saved to Vault
- [ ] Tor circuit renewed before closing
- [ ] Browser history, cache cleared
- [ ] Downloaded files moved to encrypted storage
- [ ] Report generated
- [ ] Evidence chain of custody documented
- [ ] VM snapshot taken (if needed)
- [ ] Legal review completed

## EMERGENCY ABORT PROCEDURE
1. Kill Tor immediately: `pkill tor`
2. Kill browser: `pkill -9 firefox`
3. Stop all Docker containers: `docker compose stop`
4. Clear RAM: `sync; echo 3 > /proc/sys/vm/drop_caches`
5. Document abort reason in ops log

---
*HexStrike OPSEC Framework — 2026-03-03*
