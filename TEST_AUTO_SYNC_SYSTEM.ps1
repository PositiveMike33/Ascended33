# TEST_AUTO_SYNC_SYSTEM.ps1
# Comprehensive test script for ASCENDED33 Auto-Sync system
# ================================================================

param(
    [switch]$Full = $false,
    [switch]$Verbose = $false
)

$ErrorActionPreference = "Continue"

# Configuration
$VAULT_PATH = "D:\Vault\Vault"
$REPO_PATH = "D:\Vault\Vault\Ascended33"
$PYTHON_EXE = "C:\Users\th3th\AppData\Local\Programs\Python\Python313\python.exe"

# Colors
$colors = @{
    "SUCCESS" = "Green"
    "ERROR" = "Red"
    "WARN" = "Yellow"
    "INFO" = "Cyan"
    "TEST" = "Magenta"
}

# ================================================================
# TEST FUNCTIONS
# ================================================================

function Write-TestResult {
    param([string]$Test, [bool]$Passed, [string]$Message = "")
    
    $timestamp = (Get-Date).ToString("HH:mm:ss")
    $status = if ($Passed) { "✅ PASS" } else { "❌ FAIL" }
    $color = if ($Passed) { "Green" } else { "Red" }
    
    Write-Host "[$timestamp] " -NoNewline -ForegroundColor Gray
    Write-Host "$status " -NoNewline -ForegroundColor $color
    Write-Host "$Test"
    
    if ($Message) {
        Write-Host "         → $Message" -ForegroundColor Gray
    }
}

function Test-Dependencies {
    Write-Host "`n[TESTING DEPENDENCIES]" -ForegroundColor $colors["TEST"]
    Write-Host "=" * 60
    
    $passed = 0
    $failed = 0
    
    # Python
    if (Test-Path $PYTHON_EXE) {
        $version = & $PYTHON_EXE --version 2>&1
        Write-TestResult "Python executable found" $true $version
        $passed++
    } else {
        Write-TestResult "Python executable found" $false "Not found at $PYTHON_EXE"
        $failed++
    }
    
    # Watchdog
    $watchdog = & $PYTHON_EXE -c "import watchdog; print(watchdog.__version__)" 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-TestResult "watchdog library installed" $true $watchdog
        $passed++
    } else {
        Write-TestResult "watchdog library installed" $false "Install with: pip install watchdog"
        $failed++
    }
    
    # PyYAML
    $yaml = & $PYTHON_EXE -c "import yaml; print('OK')" 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-TestResult "PyYAML library installed" $true
        $passed++
    } else {
        Write-TestResult "PyYAML library installed" $false "Install with: pip install pyyaml"
        $failed++
    }
    
    return @{ "passed" = $passed; "failed" = $failed }
}

function Test-VaultStructure {
    Write-Host "`n[TESTING VAULT STRUCTURE]" -ForegroundColor $colors["TEST"]
    Write-Host "=" * 60
    
    $passed = 0
    $failed = 0
    
    # Main vault path
    if (Test-Path $VAULT_PATH) {
        Write-TestResult "Vault path exists" $true $VAULT_PATH
        $passed++
    } else {
        Write-TestResult "Vault path exists" $false "Not found: $VAULT_PATH"
        $failed++
        return @{ "passed" = $passed; "failed" = $failed }
    }
    
    # Required folders
    $requiredFolders = @(
        "HACKERGPT",
        "ENQUETES_OSINT",
        "_BRAIN",
        "REPORT",
        "Ascended33/config",
        "Ascended33/vault_sync"
    )
    
    foreach ($folder in $requiredFolders) {
        $path = Join-Path $VAULT_PATH $folder
        if (Test-Path $path) {
            Write-TestResult "Folder: $folder" $true
            $passed++
        } else {
            Write-TestResult "Folder: $folder" $false "Missing folder"
            $failed++
        }
    }
    
    return @{ "passed" = $passed; "failed" = $failed }
}

function Test-VaultFiles {
    Write-Host "`n[TESTING VAULT FILES]" -ForegroundColor $colors["TEST"]
    Write-Host "=" * 60
    
    $passed = 0
    $failed = 0
    
    # Config file
    $configPath = Join-Path $REPO_PATH "config\auto_sync.json"
    if (Test-Path $configPath) {
        Write-TestResult "auto_sync.json config file" $true
        
        try {
            $config = Get-Content $configPath | ConvertFrom-Json
            if ($config.vault.path -eq $VAULT_PATH) {
                Write-TestResult "Config vault path correct" $true
                $passed++
            } else {
                Write-TestResult "Config vault path correct" $false "Path: $($config.vault.path)"
                $failed++
            }
        } catch {
            Write-TestResult "Config file valid JSON" $false "Parse error"
            $failed++
        }
        $passed++
    } else {
        Write-TestResult "auto_sync.json config file" $false "Not found"
        $failed++
    }
    
    # Monitor script
    $monitorPath = Join-Path $REPO_PATH "vault_sync\vault_monitor.py"
    if (Test-Path $monitorPath) {
        Write-TestResult "vault_monitor.py script" $true
        $passed++
    } else {
        Write-TestResult "vault_monitor.py script" $false "Not found"
        $failed++
    }
    
    # Auto-sync config script
    $autoSyncPath = Join-Path $REPO_PATH "vault_sync\auto_sync_config.py"
    if (Test-Path $autoSyncPath) {
        Write-TestResult "auto_sync_config.py script" $true
        $passed++
    } else {
        Write-TestResult "auto_sync_config.py script" $false "Not found"
        $failed++
    }
    
    # Launcher script
    $launcherPath = Join-Path $REPO_PATH "start_with_auto_sync.ps1"
    if (Test-Path $launcherPath) {
        Write-TestResult "start_with_auto_sync.ps1 launcher" $true
        $passed++
    } else {
        Write-TestResult "start_with_auto_sync.ps1 launcher" $false "Not found"
        $failed++
    }
    
    return @{ "passed" = $passed; "failed" = $failed }
}

function Test-VaultWrite {
    Write-Host "`n[TESTING VAULT WRITE PERMISSIONS]" -ForegroundColor $colors["TEST"]
    Write-Host "=" * 60
    
    $passed = 0
    $failed = 0
    
    $testFile = Join-Path $VAULT_PATH ".test_write_$(Get-Random).txt"
    
    try {
        Set-Content -Path $testFile -Value "Test write at $(Get-Date)" -ErrorAction Stop
        Write-TestResult "Write test file" $true
        $passed++
        
        if (Test-Path $testFile) {
            Remove-Item $testFile -ErrorAction Stop
            Write-TestResult "Clean up test file" $true
            $passed++
        } else {
            Write-TestResult "Clean up test file" $false
            $failed++
        }
    } catch {
        Write-TestResult "Write test file" $false "Permission denied"
        $failed++
    }
    
    return @{ "passed" = $passed; "failed" = $failed }
}

function Test-PythonScripts {
    Write-Host "`n[TESTING PYTHON SCRIPTS]" -ForegroundColor $colors["TEST"]
    Write-Host "=" * 60
    
    $passed = 0
    $failed = 0
    
    # Test vault_monitor.py syntax
    $monitorPath = Join-Path $REPO_PATH "vault_sync\vault_monitor.py"
    $syntaxCheck = & $PYTHON_EXE -m py_compile $monitorPath 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-TestResult "vault_monitor.py syntax" $true
        $passed++
    } else {
        Write-TestResult "vault_monitor.py syntax" $false $syntaxCheck
        $failed++
    }
    
    # Test auto_sync_config.py syntax
    $configPath = Join-Path $REPO_PATH "vault_sync\auto_sync_config.py"
    $syntaxCheck = & $PYTHON_EXE -m py_compile $configPath 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-TestResult "auto_sync_config.py syntax" $true
        $passed++
    } else {
        Write-TestResult "auto_sync_config.py syntax" $false $syntaxCheck
        $failed++
    }
    
    return @{ "passed" = $passed; "failed" = $failed }
}

function Test-Requirements {
    Write-Host "`n[TESTING REQUIREMENTS.TXT]" -ForegroundColor $colors["TEST"]
    Write-Host "=" * 60
    
    $passed = 0
    $failed = 0
    
    $reqPath = Join-Path $REPO_PATH "requirements.txt"
    
    if (Test-Path $reqPath) {
        Write-TestResult "requirements.txt exists" $true
        $passed++
        
        $content = Get-Content $reqPath
        if ($content -match "watchdog") {
            Write-TestResult "watchdog in requirements" $true
            $passed++
        } else {
            Write-TestResult "watchdog in requirements" $false "Missing watchdog package"
            $failed++
        }
    } else {
        Write-TestResult "requirements.txt exists" $false "Not found"
        $failed++
    }
    
    return @{ "passed" = $passed; "failed" = $failed }
}

function Show-Summary {
    param([hashtable]$Results)
    
    Write-Host "`n[TEST SUMMARY]" -ForegroundColor $colors["TEST"]
    Write-Host "=" * 60
    
    $totalPassed = ($Results.Values | Measure-Object -Property passed -Sum).Sum
    $totalFailed = ($Results.Values | Measure-Object -Property failed -Sum).Sum
    $totalTests = $totalPassed + $totalFailed
    
    Write-Host "`nTotal Tests: $totalTests"
    Write-Host "Passed: " -NoNewline
    Write-Host "$totalPassed" -ForegroundColor Green
    Write-Host "Failed: " -NoNewline
    Write-Host "$totalFailed" -ForegroundColor Red
    
    if ($totalFailed -eq 0) {
        Write-Host "`n✅ ALL TESTS PASSED! System is ready." -ForegroundColor Green
        Write-Host "Run: .\start_with_auto_sync.ps1" -ForegroundColor Cyan
    } else {
        Write-Host "`n⚠️  Some tests failed. Review messages above." -ForegroundColor Yellow
    }
    
    Write-Host "`n" + ("=" * 60)
}

# ================================================================
# MAIN
# ================================================================

Write-Host "`n"
Write-Host "  ╔════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "  ║  ASCENDED33 AUTO-SYNC TEST SUITE      ║" -ForegroundColor Cyan
Write-Host "  ║  Comprehensive System Verification    ║" -ForegroundColor Cyan
Write-Host "  ╚════════════════════════════════════════╝" -ForegroundColor Cyan

$results = @{}

$results["Dependencies"] = Test-Dependencies
$results["VaultStructure"] = Test-VaultStructure
$results["VaultFiles"] = Test-VaultFiles
$results["VaultWrite"] = Test-VaultWrite
$results["PythonScripts"] = Test-PythonScripts
$results["Requirements"] = Test-Requirements

Show-Summary $results

Write-Host "`nTest complete at $(Get-Date)" -ForegroundColor Gray
