# ============================================================================
# CREATE_HEXSTRIKE_SHORTCUT.ps1 — Create Desktop Shortcut for HexStrike
# ============================================================================

param(
    [string]$DesktopPath = "$env:USERPROFILE\Desktop",
    [string]$VaultPath = "D:\Vault\Vault\Ascended33"
)

# Check if paths exist
if (-not (Test-Path $VaultPath)) {
    Write-Host "❌ Vault path not found: $VaultPath" -ForegroundColor Red
    exit 1
}

# Paths
$ShortcutPath = "$DesktopPath\HexStrike.lnk"
$TargetPath = "$VaultPath\LAUNCH_HEXSTRIKE.bat"

# Create Windows shortcut
try {
    $WshShell = New-Object -ComObject WScript.Shell
    $Shortcut = $WshShell.CreateShortcut($ShortcutPath)
    $Shortcut.TargetPath = $TargetPath
    $Shortcut.WorkingDirectory = $VaultPath
    $Shortcut.Description = "HexStrike - Cybersecurity Research Platform with 150+ Red Team Tools"
    $Shortcut.IconLocation = "D:\Vault\Vault\Ascended33\favicon.ico"
    $Shortcut.WindowStyle = 1  # Normal window
    $Shortcut.Save()
    
    Write-Host "✅ HexStrike shortcut created successfully!" -ForegroundColor Green
    Write-Host "📁 Location: $ShortcutPath" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "🚀 You can now launch HexStrike from your Desktop" -ForegroundColor Green
    
} catch {
    Write-Host "❌ Failed to create shortcut: $_" -ForegroundColor Red
    exit 1
}

# Create README for shortcut
$ReadmePath = "$DesktopPath\HexStrike_README.txt"

@"
╔════════════════════════════════════════════════════════════════════════╗
║                     🔐 HEXSTRIKE LAUNCHER                              ║
║            Cybersecurity Research Platform - Quick Start               ║
╚════════════════════════════════════════════════════════════════════════╝

📌 QUICK START
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Double-click HexStrike.lnk to launch
2. Wait for Docker containers to start (~30-60 seconds)
3. Browser will open to http://localhost:8501 automatically
4. Select tool from sidebar and launch scans

📡 ENDPOINTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Streamlit Dashboard:  http://localhost:8501
HexStrike API:        http://localhost:8001
HackerGPT:            http://localhost:8000
Tor Network:          localhost:9050 (SOCKS5)

🛠️  AVAILABLE TOOLS (150+)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Scanning & Recon:
  • nmap, masscan, nessus, nuclei, shodan, censys
  
Web Security:
  • burpsuite, zaproxy, wfuzz, sqlmap, nuclei, ffuf
  
OSINT & Intelligence:
  • maltego, spiderfoot, recon-ng, theHarvester, shodan-cli
  
Enumeration:
  • enum4linux, snmp-check, ldap-search, smtp-user-enum
  
Cloud Security:
  • aws-enum, azure-enum, gcp-enum, s3-scanner, cloudtracker
  
Exploitation:
  • metasploit, hashcat, john, hydra, aircrack-ng
  
And 100+ more tools!

📊 USAGE GUIDE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. LAUNCH TOOL
   - Select tool from dropdown
   - Enter target (IP, domain, CIDR)
   - Configure parameters
   - Click "Launch Task"

2. MONITOR JOBS
   - Real-time status of running scans
   - View progress and execution time
   - Cancel tasks if needed

3. VIEW RESULTS
   - Browse completed job results
   - Export to JSON
   - View tool statistics

⚙️  SYSTEM REQUIREMENTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

• Docker Desktop (running)
• 8GB RAM minimum
• 20GB free disk space
• Windows 10/11 or Linux

🔒 SECURITY & OPSEC
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

• All tools run in isolated Docker containers
• Tor anonymization available
• Results cached locally to Obsidian Vault
• OPSEC monitoring enabled

❓ TROUBLESHOOTING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Q: "Connection refused" error
A: Ensure Docker Desktop is running and started properly

Q: Containers won't start
A: Check Docker logs: docker-compose logs
   Run: docker-compose up -d

Q: Port 8501 already in use
A: Close other Streamlit apps or change port in docker-compose.yml

Q: Out of disk space
A: Run: docker system prune -a
   Removes unused Docker images

📚 LEARNING RESOURCES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Red Team Learning Path:
  D:\Vault\Vault\HexStrike\Pentest\
  D:\Vault\Vault\HexStrike\OSINT\
  D:\Vault\Vault\HACKERGPT\RESSOURCES_LEARNING\

Documentation:
  D:\Vault\Vault\Ascended33\README.md
  D:\Vault\Vault\Ascended33\HEXSTRIKE_INTEGRATION_GUIDE.md

════════════════════════════════════════════════════════════════════════

For more information, see:
  • HEXSTRIKE_INTEGRATION_GUIDE.md
  • OPERATIONAL_GUIDE.md
  • DEPLOYMENT_COMPLETE.md

Last updated: 2026-02-20
"@ | Out-File -FilePath $ReadmePath -Encoding UTF8 -Force

Write-Host ""
Write-Host "✅ README created: $ReadmePath" -ForegroundColor Green
