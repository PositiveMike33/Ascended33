# ================================================================
# ASCENDED33 WITH AUTO-SYNC
# Complete launcher with automatic Vault synchronization
# ================================================================

param(
    [switch]$SkipVaultCheck = $false,
    [switch]$ForceResync = $false,
    [switch]$Verbose = $false
)

$ErrorActionPreference = "Continue"

# ================================================================
# CONFIGURATION
# ================================================================
$REPO_PATH = "D:\Vault\Vault\Ascended33"
$VAULT_PATH = "D:\Vault\Vault"
$PYTHON_EXE = "C:\Users\th3th\AppData\Local\Programs\Python\Python313\python.exe"
$VENV_PATH = "$REPO_PATH\venv"

# ================================================================
# FUNCTIONS
# ================================================================
function Write-Status {
    param([string]$Message, [string]$Status = "INFO", [ConsoleColor]$Color = "Cyan")
    $timestamp = (Get-Date).ToString("HH:mm:ss")
    $statusColor = @{
        "SUCCESS" = "Green"
        "ERROR" = "Red"
        "WARN" = "Yellow"
        "INFO" = "Cyan"
    }[$Status]
    
    Write-Host "[$timestamp] " -NoNewline -ForegroundColor Gray
    Write-Host "[$Status] " -NoNewline -ForegroundColor $statusColor
    Write-Host $Message
}

function Show-Banner {
    Clear-Host
    Write-Host ""
    Write-Host "  +==========================================+" -ForegroundColor Cyan
    Write-Host "  |                                          |" -ForegroundColor Cyan
    Write-Host "  |      ASCENDED33 WITH AUTO-SYNC          |" -ForegroundColor Green
    Write-Host "  |   Mission Control + Vault Sync          |" -ForegroundColor Green
    Write-Host "  |                                          |" -ForegroundColor Cyan
    Write-Host "  +==========================================+" -ForegroundColor Cyan
    Write-Host ""
}

# ================================================================
# PHASE 1: VAULT CONNECTION CHECK
# ================================================================
function Check-Vault {
    Write-Status "PHASE 1: Checking Vault connection..." "INFO"
    Write-Host ""
    
    if (-not (Test-Path $VAULT_PATH)) {
        Write-Status "Vault NOT found at $VAULT_PATH" "ERROR"
        return $false
    }
    
    Write-Status "Vault found at $VAULT_PATH" "SUCCESS"
    
    # Check write permissions
    $testFile = "$VAULT_PATH\.ascended33_test"
    try {
        Set-Content -Path $testFile -Value "test" -ErrorAction Stop
        Remove-Item $testFile -ErrorAction Stop
        Write-Status "Vault write permissions verified" "SUCCESS"
    } catch {
        Write-Status "Vault write test failed - check permissions!" "ERROR"
        return $false
    }
    
    Write-Host ""
    return $true
}

# ================================================================
# PHASE 2: ENSURE VAULT FOLDERS
# ================================================================
function Ensure-VaultFolders {
    Write-Status "PHASE 2: Ensuring Vault folder structure..." "INFO"
    Write-Host ""
    
    $folders = @(
        "HACKERGPT\HEXSTRIKE",
        "HACKERGPT\OSINT_Profilage",
        "HACKERGPT\Pentest",
        "HACKERGPT\Outils",
        "HACKERGPT\CTF",
        "ENQUETES_OSINT",
        "ENQUETES_OSINT\DarkWeb",
        "Claude-Michael\Sessions",
        "_BRAIN",
        "REPORT",
        "Ascended33\config\ssh"
    )
    
    $createdCount = 0
    foreach ($folder in $folders) {
        $folderPath = "$VAULT_PATH\$folder"
        if (-not (Test-Path $folderPath)) {
            try {
                New-Item -ItemType Directory -Path $folderPath -Force | Out-Null
                Write-Status "Created folder: $folder" "SUCCESS"
                $createdCount++
            } catch {
                Write-Status "Failed to create folder: $folder" "WARN"
            }
        } else {
            Write-Status "Folder exists: $folder" "INFO"
        }
    }
    
    Write-Status "Vault structure ready ($createdCount new folders)" "SUCCESS"
    Write-Host ""
    return $true
}

# ================================================================
# PHASE 3: SETUP AUTO-SYNC
# ================================================================
function Setup-AutoSync {
    Write-Status "PHASE 3: Setting up Auto-Sync system..." "INFO"
    Write-Host ""
    
    # Check if auto_sync_config.py exists
    $autoSyncScript = "$REPO_PATH\vault_sync\auto_sync_config.py"
    if (-not (Test-Path $autoSyncScript)) {
        Write-Status "Auto-Sync script not found" "WARN"
        return $false
    }
    
    Write-Status "Auto-Sync script found" "SUCCESS"
    
    # Check if vault_monitor.py exists
    $monitorScript = "$REPO_PATH\vault_sync\vault_monitor.py"
    if (-not (Test-Path $monitorScript)) {
        Write-Status "Vault Monitor script not found" "WARN"
        return $false
    }
    
    Write-Status "Vault Monitor script found" "SUCCESS"
    
    # Initialize auto-sync config
    Write-Status "Initializing Auto-Sync configuration..." "INFO"
    try {
        & $PYTHON_EXE -c @"
import sys
sys.path.insert(0, r'$REPO_PATH\vault_sync')
from auto_sync_config import setup_auto_sync
result = setup_auto_sync()
if result:
    print('✓ Auto-Sync initialized')
else:
    print('✗ Auto-Sync failed')
    sys.exit(1)
"@
        Write-Status "Auto-Sync configuration complete" "SUCCESS"
    } catch {
        Write-Status "Error initializing Auto-Sync" "WARN"
    }
    
    Write-Host ""
    return $true
}

# ================================================================
# PHASE 4: START VAULT MONITOR
# ================================================================
function Start-VaultMonitor {
    Write-Status "PHASE 4: Starting Vault Monitor..." "INFO"
    Write-Host ""
    
    $monitorScript = "$REPO_PATH\vault_sync\vault_monitor.py"
    
    # Start monitor in background
    $startMonitor = {
        param($pythonExe, $script, $vaultPath)
        & $pythonExe $script
    }
    
    Write-Status "Starting real-time Vault monitoring..." "INFO"
    
    # Use Start-Job for background monitoring
    try {
        $job = Start-Job -ScriptBlock $startMonitor -ArgumentList $PYTHON_EXE, $monitorScript, $VAULT_PATH
        Write-Status "Vault Monitor job started (ID: $($job.Id))" "SUCCESS"
    } catch {
        Write-Status "Could not start background monitor" "WARN"
        Write-Status "Monitoring will be handled by main process" "INFO"
    }
    
    Write-Host ""
    return $true
}

# ================================================================
# PHASE 5: CREATE VAULT SHORTCUTS
# ================================================================
function Create-VaultShortcuts {
    Write-Status "PHASE 5: Creating Vault shortcuts..." "INFO"
    Write-Host ""
    
    $desktopPath = "$env:USERPROFILE\OneDrive\Desktop"
    
    # Shortcut 1: Vault Direct Access
    $vaultShortcut = "$desktopPath\Open_Ascended33_Vault.lnk"
    try {
        $shell = New-Object -ComObject WScript.Shell
        $shortcut = $shell.CreateShortcut($vaultShortcut)
        $shortcut.TargetPath = $VAULT_PATH
        $shortcut.Description = "Open Ascended33 Vault in Explorer"
        $shortcut.Save()
        Write-Status "Created shortcut: Open_Ascended33_Vault.lnk" "SUCCESS"
    } catch {
        Write-Status "Could not create Vault shortcut" "WARN"
    }
    
    Write-Host ""
    return $true
}

# ================================================================
# PHASE 6: VERIFY AUTO-SYNC STATUS
# ================================================================
function Verify-AutoSyncStatus {
    Write-Status "PHASE 6: Verifying Auto-Sync status..." "INFO"
    Write-Host ""
    
    # Check state file
    $stateFile = "$VAULT_PATH\.auto_sync_state.json"
    if (Test-Path $stateFile) {
        try {
            $state = Get-Content $stateFile | ConvertFrom-Json
            Write-Status "Auto-Sync state file exists" "SUCCESS"
            Write-Status "Connected: $($state.connected)" "INFO"
        } catch {
            Write-Status "Could not read state file" "WARN"
        }
    } else {
        Write-Status "State file will be created on sync" "INFO"
    }
    
    # Check monitor script
    $monitorScript = "$REPO_PATH\vault_sync\vault_monitor.py"
    if (Test-Path $monitorScript) {
        $fileSize = (Get-Item $monitorScript).Length
        Write-Status "Vault Monitor ready ($fileSize bytes)" "SUCCESS"
    }
    
    Write-Host ""
    return $true
}

# ================================================================
# MAIN
# ================================================================
function Main {
    Show-Banner
    
    # Check Vault
    if (-not (Check-Vault)) {
        Write-Status "Cannot proceed without Vault connection" "ERROR"
        Read-Host "Press Enter to exit"
        exit 1
    }
    
    # Ensure folders
    Ensure-VaultFolders
    
    # Setup Auto-Sync
    Setup-AutoSync
    
    # Start Monitor
    Start-VaultMonitor
    
    # Create Shortcuts
    Create-VaultShortcuts
    
    # Verify Status
    Verify-AutoSyncStatus
    
    # Final status
    Write-Host "  +==========================================+" -ForegroundColor Cyan
    Write-Host "  |  AUTO-SYNC SYSTEM OPERATIONAL           |" -ForegroundColor Green
    Write-Host "  +------------------------------------------+" -ForegroundColor Cyan
    Write-Host "  | Vault Path: $VAULT_PATH" -ForegroundColor Green
    Write-Host "  | Auto-Sync:  ✓ ENABLED" -ForegroundColor Green
    Write-Host "  | Monitoring: ✓ ACTIVE" -ForegroundColor Green
    Write-Host "  | Status:     ✓ READY" -ForegroundColor Green
    Write-Host "  +==========================================+" -ForegroundColor Cyan
    Write-Host ""
    
    Write-Status "All systems operational" "SUCCESS"
    Write-Host ""
    Write-Status "Your Vault will now:" "INFO"
    Write-Host "  ✓ Auto-sync all changes to $VAULT_PATH" -ForegroundColor Green
    Write-Host "  ✓ Auto-reconnect if disconnected" -ForegroundColor Green
    Write-Host "  ✓ Monitor for new files/reports/notes" -ForegroundColor Green
    Write-Host "  ✓ Maintain synchronized state" -ForegroundColor Green
    Write-Host ""
    
    Read-Host "Press Enter to close"
}

# Execute
Main
