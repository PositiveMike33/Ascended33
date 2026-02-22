=================================================
  ASCENDED33 DOCKER SETUP - BUILD & LAUNCH
=================================================

# Check if running as admin
$currentUser = [System.Security.Principal.WindowsIdentity]::GetCurrent()
$principal = New-Object System.Security.Principal.WindowsPrincipal($currentUser)
$adminRole = [System.Security.Principal.WindowsBuiltInRole]::Administrator

if (-not $principal.IsInRole($adminRole)) {
    Write-Host "[!] This script must be run as Administrator" -ForegroundColor Red
    Write-Host "[*] Restarting with admin privileges..." -ForegroundColor Yellow
    Start-Process powershell.exe -ArgumentList "-File `"$PSCommandPath`"" -Verb RunAs
    exit
}

# Set working directory
Set-Location $PSScriptRoot

Write-Host "`n=================================================" -ForegroundColor Cyan
Write-Host "  ASCENDED33 DOCKER SETUP & BUILD" -ForegroundColor Cyan
Write-Host "=================================================" -ForegroundColor Cyan
Write-Host ""

# Check if Docker is running
Write-Host "[*] Checking Docker daemon..." -ForegroundColor Yellow
try {
    $null = docker ps 2>$null
    Write-Host "[OK] Docker daemon is running" -ForegroundColor Green
} catch {
    Write-Host "[!] Docker daemon not running, attempting to start..." -ForegroundColor Red
    try {
        Start-Process "C:\Program Files\Docker\Docker\Docker.exe"
        Write-Host "[*] Docker started, waiting 10 seconds..." -ForegroundColor Yellow
        Start-Sleep -Seconds 10
    } catch {
        Write-Host "[!] Could not start Docker" -ForegroundColor Red
        Write-Host "[*] Please start Docker manually from: C:\Program Files\Docker\Docker\Docker.exe" -ForegroundColor Yellow
        exit 1
    }
}

Write-Host ""
Write-Host "[*] Building Docker images locally..." -ForegroundColor Cyan
Write-Host ""

# Build images
$buildStart = Get-Date

try {
    docker-compose build --no-cache
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "[OK] Docker images built successfully" -ForegroundColor Green
        
        $buildEnd = Get-Date
        $buildTime = ($buildEnd - $buildStart).TotalSeconds
        Write-Host "[*] Build time: $([Math]::Round($buildTime, 2))s" -ForegroundColor Cyan
    } else {
        Write-Host ""
        Write-Host "[!] Docker build failed with exit code: $LASTEXITCODE" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "[!] Error during docker build: $_" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "[*] Starting Docker Compose services..." -ForegroundColor Yellow

# Start services
try {
    docker-compose up -d
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[OK] Docker Compose services starting..." -ForegroundColor Green
    } else {
        Write-Host "[!] Docker Compose startup failed" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "[!] Error starting Docker Compose: $_" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "[*] Waiting for services to initialize (15 seconds)..." -ForegroundColor Yellow
Start-Sleep -Seconds 15

Write-Host ""
Write-Host "=================================================" -ForegroundColor Cyan
Write-Host "  SERVICE STATUS" -ForegroundColor Cyan
Write-Host "=================================================" -ForegroundColor Cyan
Write-Host ""

docker-compose ps

Write-Host ""
Write-Host "=================================================" -ForegroundColor Cyan
Write-Host "  SETUP COMPLETE!" -ForegroundColor Green
Write-Host "=================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Open Streamlit dashboard: http://localhost:8501" -ForegroundColor Yellow
Write-Host "  2. Check HexStrike status: http://localhost:8001/status" -ForegroundColor Yellow
Write-Host "  3. View logs: docker-compose logs -f" -ForegroundColor Yellow
Write-Host ""

Write-Host "Available endpoints:" -ForegroundColor Cyan
Write-Host "  - Streamlit Dashboard: http://localhost:8501" -ForegroundColor White
Write-Host "  - HackerGPT API:       http://localhost:8000" -ForegroundColor White
Write-Host "  - HexStrike API:       http://localhost:8001" -ForegroundColor White
Write-Host "  - Tor SOCKS5:          localhost:9050" -ForegroundColor White
Write-Host ""

Write-Host "For troubleshooting, run: .\VERIFY_HEXSTRIKE.bat" -ForegroundColor Cyan
Write-Host ""

Read-Host "Press Enter to exit"
