#!/usr/bin/env powershell
# ============================================================
# 🔧 VPN/TOR FIX - Update Ascended33 Infrastructure
# Adds Privoxy layer between HexStrike and Tor
# ============================================================

Write-Host "`n╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  🔧 Updating VPN/Tor Infrastructure                           ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════════╝`n" -ForegroundColor Cyan

$VaultPath = "D:\Vault\Vault"

Write-Host "[1/4] Stopping current containers..." -ForegroundColor Yellow
& docker stop th3-hexstrike th3-privoxy 2>$null
& docker rm th3-hexstrike th3-privoxy 2>$null

Write-Host "`n[2/4] Starting Privoxy (DNS/SOCKS converter)..." -ForegroundColor Yellow

$privoxy_cmd = @"
apk add --no-cache privoxy; privoxy --no-daemon /etc/privoxy/config
"@

& docker run -d `
  --name th3-privoxy `
  --network ascended33_ascended33-network `
  -p 8118:8118 `
  -v "$VaultPath\privoxy-config.conf:/etc/privoxy/config:ro" `
  --restart unless-stopped `
  alpine:latest sh -c $privoxy_cmd

Write-Host "✅ Privoxy started on port 8118"

Write-Host "`n[3/4] Restarting HexStrike with Privoxy routing..." -ForegroundColor Yellow

& docker run -d `
  --name th3-hexstrike `
  --network ascended33_ascended33-network `
  -p 8001:8001 `
  -e "HTTP_PROXY=http://th3-privoxy:8118" `
  -e "HTTPS_PROXY=http://th3-privoxy:8118" `
  -e "http_proxy=http://th3-privoxy:8118" `
  -e "https_proxy=http://th3-privoxy:8118" `
  -e "VAULT_PATH=/vault" `
  -e "KALI_HOST=th3-kali" `
  -e "HACKERGPT_HOST=th3-hackergpt" `
  -e "REPORT_DESTINATION=/vault/_BRAIN/hexstrike_reports" `
  -v ascended33_kali-workspace:/workspace:rw `
  -v ascended33_hexstrike-data:/app/data:rw `
  -v "D:/Vault/Vault:/vault:rw" `
  --restart unless-stopped `
  th3-hexstrike:latest python3 -m uvicorn workers.hexstrike_worker_api:app --host 0.0.0.0 --port 8001

Write-Host "✅ HexStrike restarted with Privoxy proxy routing"

Write-Host "`n[4/4] Verifying connectivity..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

$privoxy_status = & docker ps --format "{{.Names}}`t{{.Status}}" | Select-String "th3-privoxy"
$hexstrike_status = & docker ps --format "{{.Names}}`t{{.Status}}" | Select-String "th3-hexstrike"
$tor_status = & docker ps --format "{{.Names}}`t{{.Status}}" | Select-String "th3-tor"

if ($privoxy_status) { Write-Host "✅ Privoxy running" -ForegroundColor Green }
if ($hexstrike_status) { Write-Host "✅ HexStrike running" -ForegroundColor Green }
if ($tor_status) { Write-Host "✅ Tor running" -ForegroundColor Green }

Write-Host "`n╔════════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║  ✅ VPN/TOR INFRASTRUCTURE UPDATED                            ║" -ForegroundColor Green
Write-Host "║                                                                ║" -ForegroundColor Green
Write-Host "║  Traffic Flow:                                                 ║" -ForegroundColor Green
Write-Host "║  HexStrike → Privoxy (port 8118)                               ║" -ForegroundColor Green
Write-Host "║            → Tor SOCKS5 (port 9050)                            ║" -ForegroundColor Green
Write-Host "║            → Internet (Anonymized)                             ║" -ForegroundColor Green
Write-Host "║                                                                ║" -ForegroundColor Green
Write-Host "║  Tor dashboard should now show VPN/TOR as CONNECTED ✅         ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════════════════════════════╝`n" -ForegroundColor Green

Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Refresh Ascended33 dashboard (F5)" -ForegroundColor Gray
Write-Host "  2. Check SYSTEM STATUS: VPN & TOR should now be CONNECTED" -ForegroundColor Gray
Write-Host "  3. Try running a mission in HexStrike" -ForegroundColor Gray

Read-Host "`nPress Enter to continue..."
