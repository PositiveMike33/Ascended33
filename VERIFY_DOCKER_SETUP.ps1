# ============================================================================
# VERIFY DOCKER SETUP - Pre-Launch Validation Script
# Checks all prerequisites before launching Ascended33 Docker Stack
# ============================================================================

param(
    [switch]$Verbose = $false
)

$ErrorActionPreference = "SilentlyContinue"
$checks_passed = 0
$checks_failed = 0

function Write-Check {
    param([string]$Message, [string]$Status, [string]$Details = "")
    
    $symbol = if ($Status -eq "PASS") { "✓" } else { "✗" }
    $color = if ($Status -eq "PASS") { "Green" } else { "Red" }
    
    $msg = "$symbol $Message"
    if ($Details) { $msg += " ($Details)" }
    
    Write-Host $msg -ForegroundColor $color
    
    if ($Status -eq "PASS") { $global:checks_passed++ } else { $global:checks_failed++ }
}

Write-Host ""
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "         ASCENDED33 DOCKER SETUP VERIFICATION" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""

# Check 1: Docker is installed
Write-Host "Checking Docker Installation..." -ForegroundColor Yellow
try {
    $docker_version = & docker --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Check "Docker installed" "PASS" $docker_version
    } else {
        Write-Check "Docker installed" "FAIL" "Docker not found in PATH"
    }
} catch {
    Write-Check "Docker installed" "FAIL" "Docker command failed"
}

# Check 2: Docker daemon running
Write-Host "`nChecking Docker Daemon..." -ForegroundColor Yellow
try {
    $info = & docker info 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Check "Docker daemon running" "PASS" "Daemon responsive"
    } else {
        Write-Check "Docker daemon running" "FAIL" "Daemon not responding"
    }
} catch {
    Write-Check "Docker daemon running" "FAIL" "Cannot connect to daemon"
}

# Check 3: Docker Compose installed
Write-Host "`nChecking Docker Compose..." -ForegroundColor Yellow
try {
    $compose_version = & docker-compose --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Check "Docker Compose installed" "PASS" $compose_version
    } else {
        Write-Check "Docker Compose installed" "FAIL" "Compose not found"
    }
} catch {
    Write-Check "Docker Compose installed" "FAIL" "Compose command failed"
}

# Check 4: Required directories exist
Write-Host "`nChecking Required Directories..." -ForegroundColor Yellow
$paths = @(
    "D:\Vault\Vault",
    "D:\Vault\Vault\Ascended33",
    "D:\Vault\Vault\REPORT"
)

foreach ($path in $paths) {
    if (Test-Path $path) {
        Write-Check "Directory: $path" "PASS"
    } else {
        Write-Check "Directory: $path" "FAIL" "Directory not found"
    }
}

# Check 5: Required files exist
Write-Host "`nChecking Required Files..." -ForegroundColor Yellow
$files = @(
    "D:\Vault\Vault\Ascended33\docker-compose.yml",
    "D:\Vault\Vault\Ascended33\docker_orchestrator.py",
    "D:\Vault\Vault\Ascended33\DOCKER_LAUNCHER.ps1",
    "D:\Vault\Vault\Ascended33\anonymous_report_generator.py",
    "D:\Vault\Vault\Ascended33\config\docker_config.json"
)

foreach ($file in $files) {
    $filename = Split-Path $file -Leaf
    if (Test-Path $file) {
        $size = (Get-Item $file).Length / 1KB
        Write-Check "File: $filename" "PASS" "$([math]::Round($size, 1))KB"
    } else {
        Write-Check "File: $filename" "FAIL" "File not found"
    }
}

# Check 6: Desktop shortcut exists
Write-Host "`nChecking Desktop Shortcut..." -ForegroundColor Yellow
$shortcut = "C:\Users\th3th\OneDrive\Desktop\Ascended33-Docker.lnk"
if (Test-Path $shortcut) {
    Write-Check "Desktop shortcut" "PASS" "Ascended33-Docker.lnk"
} else {
    Write-Check "Desktop shortcut" "FAIL" "Shortcut not found (can create with CREATE_DOCKER_SHORTCUT.ps1)"
}

# Check 7: Python installed
Write-Host "`nChecking Python Installation..." -ForegroundColor Yellow
try {
    $python_version = & python --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Check "Python installed" "PASS" $python_version
    } else {
        Write-Check "Python installed" "FAIL" "Python not in PATH"
    }
} catch {
    Write-Check "Python installed" "FAIL" "Python not found"
}

# Check 8: Required Python packages
Write-Host "`nChecking Python Packages..." -ForegroundColor Yellow
$packages = @("docker", "watchdog", "requests")

foreach ($package in $packages) {
    try {
        $check = & python -c "import $package" 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Check "Python package: $package" "PASS"
        } else {
            Write-Check "Python package: $package" "FAIL" "Not installed (run: pip install $package)"
        }
    } catch {
        Write-Check "Python package: $package" "FAIL" "Check failed"
    }
}

# Check 9: Available disk space
Write-Host "`nChecking Disk Space..." -ForegroundColor Yellow
try {
    $drive = Get-PSDrive D
    $free_gb = $drive.Free / 1GB
    
    if ($free_gb -gt 5) {
        Write-Check "Available disk space on D:" "PASS" "$([math]::Round($free_gb, 1))GB free"
    } else {
        Write-Check "Available disk space on D:" "FAIL" "Only $([math]::Round($free_gb, 1))GB free (need 5GB)"
    }
} catch {
    Write-Check "Available disk space" "FAIL" "Cannot check drive"
}

# Check 10: Available memory
Write-Host "`nChecking Available Memory..." -ForegroundColor Yellow
try {
    $mem = Get-WmiObject Win32_ComputerSystem
    $total_gb = $mem.TotalPhysicalMemory / 1GB
    $free_mem = (Get-WmiObject Win32_OperatingSystem).FreePhysicalMemory / 1MB
    $free_gb = $free_mem / 1024
    
    if ($free_gb -gt 2048) {
        Write-Check "Available RAM" "PASS" "$([math]::Round($free_gb, 0))MB free (need 2GB)"
    } else {
        Write-Check "Available RAM" "FAIL" "Only $([math]::Round($free_gb, 0))MB free (need 2GB+)"
    }
} catch {
    Write-Check "Available RAM" "FAIL" "Cannot check memory"
}

# Check 11: Network connectivity
Write-Host "`nChecking Network..." -ForegroundColor Yellow
try {
    $test = Test-NetConnection -ComputerName 8.8.8.8 -Port 443 -ErrorAction Stop
    if ($test.TcpTestSucceeded) {
        Write-Check "Internet connectivity" "PASS" "Network available"
    } else {
        Write-Check "Internet connectivity" "FAIL" "Cannot reach external network"
    }
} catch {
    Write-Check "Internet connectivity" "FAIL" "Network check failed"
}

# Check 12: docker-compose.yml validation
Write-Host "`nValidating docker-compose.yml..." -ForegroundColor Yellow
try {
    Set-Location "D:\Vault\Vault\Ascended33"
    $validate = & docker-compose config --quiet 2>&1
    
    if ($LASTEXITCODE -eq 0) {
        Write-Check "docker-compose.yml syntax" "PASS" "Valid YAML"
    } else {
        Write-Check "docker-compose.yml syntax" "FAIL" "Invalid syntax"
    }
} catch {
    Write-Check "docker-compose.yml validation" "FAIL" "Validation error"
}

# Summary
Write-Host ""
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "                        VERIFICATION SUMMARY" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan

$total = $checks_passed + $checks_failed
$pass_rate = if ($total -gt 0) { ($checks_passed / $total * 100) } else { 0 }

Write-Host ""
Write-Host "Checks Passed: $checks_passed / $total" -ForegroundColor Green
Write-Host "Checks Failed: $checks_failed / $total" -ForegroundColor $(if ($checks_failed -gt 0) { "Red" } else { "Green" })
Write-Host "Pass Rate: $([math]::Round($pass_rate, 1))%" -ForegroundColor $(if ($pass_rate -ge 90) { "Green" } else { "Yellow" })
Write-Host ""

if ($checks_failed -eq 0) {
    Write-Host "✅ ALL CHECKS PASSED - Ready to launch!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next step: Double-click 'Ascended33-Docker.lnk' on your desktop" -ForegroundColor Cyan
    exit 0
} else {
    Write-Host "⚠ SOME CHECKS FAILED - Please fix above issues before launching" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Common fixes:" -ForegroundColor Yellow
    Write-Host "  • Docker not running: Start Docker Desktop application" -ForegroundColor Gray
    Write-Host "  • Missing directories: Create manually or check permissions" -ForegroundColor Gray
    Write-Host "  • Missing Python packages: Run 'pip install -r requirements.txt'" -ForegroundColor Gray
    Write-Host "  • Low disk space: Free up at least 5GB on D: drive" -ForegroundColor Gray
    exit 1
}
