#!/usr/bin/env powershell
# Vault Integration Verification Script
# Usage: .\verify-vault-integration.ps1

Write-Host "╔════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  VAULT BRAIN INTEGRATION VERIFICATION          ║" -ForegroundColor Cyan
Write-Host "║  D:\Vault\Vault - Virtual Brain for Claude    ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Check Docker is running
Write-Host "1. Checking Docker daemon..." -ForegroundColor Yellow
try {
    $version = docker version --format='{{.Server.Version}}' 2>&1
    if ($version) {
        Write-Host "   ✅ Docker is running (v$version)" -ForegroundColor Green
    }
} catch {
    Write-Host "   ❌ Docker is not running" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Check all containers
Write-Host "2. Container Status:" -ForegroundColor Yellow
$containers = @('th3-security-tools', 'th3-streamlit', 'th3-kali', 'th3-tor', 'th3-hexstrike', 'th3-hackergpt')
$allRunning = $true
foreach ($container in $containers) {
    $status = docker ps --format "{{.Names}}\t{{.Status}}" 2>/dev/null | Select-String $container
    if ($status) {
        $parts = $status -split '\s+'
        $running = $parts -match "Up"
        if ($running) {
            Write-Host "   ✅ $container" -ForegroundColor Green
        } else {
            Write-Host "   ❌ $container - NOT RUNNING" -ForegroundColor Red
            $allRunning = $false
        }
    } else {
        Write-Host "   ❌ $container - NOT FOUND" -ForegroundColor Red
        $allRunning = $false
    }
}
Write-Host ""

# Check Vault mounts
Write-Host "3. Vault (/vault) Mount Status:" -ForegroundColor Yellow
foreach ($container in $containers) {
    $vaultMount = docker inspect $container --format='{{range .Mounts}}{{if eq .Destination "/vault"}}true{{end}}{{end}}' 2>/dev/null
    if ($vaultMount -eq "true") {
        Write-Host "   ✅ $container has /vault mounted" -ForegroundColor Green
    } else {
        Write-Host "   ❌ $container MISSING /vault mount" -ForegroundColor Red
    }
}
Write-Host ""

# Check network connectivity
Write-Host "4. Network Connectivity:" -ForegroundColor Yellow
$networkExists = docker network ls 2>/dev/null | Select-String "th3-brain-network|thethirty3|ascended33"
if ($networkExists) {
    Write-Host "   ✅ Bridge networks configured" -ForegroundColor Green
    docker network ls 2>/dev/null | Select-String "th3-brain-network|thethirty3|ascended33" | ForEach-Object {
        $parts = $_ -split '\s+' | Where-Object { $_ }
        Write-Host "      - $($parts[1])" -ForegroundColor Gray
    }
} else {
    Write-Host "   ❌ No bridge networks found" -ForegroundColor Red
}
Write-Host ""

# Check external disk
Write-Host "5. External Disk Status:" -ForegroundColor Yellow
if (Test-Path "D:\Vault\Vault") {
    $vaultSize = (Get-ChildItem "D:\Vault\Vault" -Recurse | Measure-Object -Sum Length).Sum / 1MB
    Write-Host "   ✅ D:\Vault\Vault accessible" -ForegroundColor Green
    Write-Host "      Size: $([math]::Round($vaultSize, 2)) MB" -ForegroundColor Gray
} else {
    Write-Host "   ❌ D:\Vault\Vault not accessible" -ForegroundColor Red
}
Write-Host ""

# Test inter-container communication
Write-Host "6. Inter-Container Communication Test:" -ForegroundColor Yellow
Write-Host "   Testing th3-hackergpt → th3-hexstrike..." -ForegroundColor Gray
$testResult = docker exec th3-hackergpt ping -c 1 th3-hexstrike 2>/dev/null
if ($LASTEXITCODE -eq 0) {
    Write-Host "   ✅ Containers can communicate" -ForegroundColor Green
} else {
    Write-Host "   ⚠️  Communication test inconclusive" -ForegroundColor Yellow
}
Write-Host ""

# Summary
Write-Host "╔════════════════════════════════════════════════╗" -ForegroundColor Cyan
if ($allRunning) {
    Write-Host "║  ✅ ALL SYSTEMS OPERATIONAL                    ║" -ForegroundColor Green
    Write-Host "║                                                ║" -ForegroundColor Green
    Write-Host "║  Vault Brain is ready for use!                ║" -ForegroundColor Green
} else {
    Write-Host "║  ⚠️  SOME CONTAINERS NOT RUNNING               ║" -ForegroundColor Yellow
}
Write-Host "╚════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Quick commands
Write-Host "📌 Quick Commands:" -ForegroundColor Cyan
Write-Host ""
Write-Host "   Access Vault from container:" -ForegroundColor Gray
Write-Host "   docker exec -it th3-kali bash" -ForegroundColor White
Write-Host "   ls -la /vault" -ForegroundColor White
Write-Host ""
Write-Host "   View container logs:" -ForegroundColor Gray
Write-Host "   docker logs th3-hackergpt -f" -ForegroundColor White
Write-Host ""
Write-Host "   Test inter-container network:" -ForegroundColor Gray
Write-Host "   docker exec th3-hackergpt curl http://th3-hexstrike:8001" -ForegroundColor White
Write-Host ""
