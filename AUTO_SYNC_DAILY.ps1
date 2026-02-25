# ============================================
# SYNCHRONISATION AUTOMATIQUE VAULT ↔ GITHUB
# Backup et Disaster Recovery System
# ============================================

param(
    [ValidateSet("VaultToGitHub", "GitHubToVault", "BiSync")]
    [string]$SyncDirection = "VaultToGitHub",
    [switch]$DryRun,
    [switch]$Verbose
)

# Configuration
$vaultPath = "D:\Vault\Vault"
$githubPath = "C:\Users\th3th\OneDrive\Documents\GitHub\Ascended33"
$logPath = "$vaultPath\SYNC_LOGS"
$timestamp = Get-Date -Format "yyyy-MM-dd_HHmmss"
$logFile = "$logPath\sync_$timestamp.log"

# Créer répertoire logs s'il n'existe pas
if (-not (Test-Path $logPath)) {
    New-Item -ItemType Directory -Path $logPath -Force | Out-Null
}

function Write-Log {
    param([string]$Message, [ValidateSet("INFO", "WARNING", "ERROR", "SUCCESS")]$Level = "INFO")
    $logMessage = "[$timestamp] [$Level] $Message"
    Add-Content -Path $logFile -Value $logMessage
    Write-Host $logMessage -ForegroundColor $(
        switch ($Level) {
            "ERROR"   { "Red" }
            "WARNING" { "Yellow" }
            "SUCCESS" { "Green" }
            default  { "Gray" }
        }
    )
}

function Invoke-RoboCopy {
    param(
        [string]$Source,
        [string]$Destination,
        [string]$Direction
    )
    
    $robocopyArgs = @(
        $Source,
        $Destination,
        "/S", "/E",                    # All subdirectories
        "/COPY:DAT",                   # Copy: Data, Attributes, Timestamps
        "/R:3", "/W:10",               # Retries on error
        "/XO",                         # Exclude older files (preserve dest)
        "/FFT",                        # FAT file time tolerance
        "/NJH", "/NJS"                 # No job header/summary
    )
    
    if ($Verbose) {
        $robocopyArgs += "/V"
    }
    
    if ($DryRun) {
        $robocopyArgs += "/L"
        Write-Log "DRY RUN MODE - No files will be copied" "INFO"
    }
    
    Write-Log "Starting sync: $Direction" "INFO"
    Write-Log "Source: $Source" "INFO"
    Write-Log "Destination: $Destination" "INFO"
    
    $output = & robocopy @robocopyArgs 2>&1
    
    # Robocopy exit codes
    # 0 = Success, no change
    # 1 = Success, files copied
    # 2+ = Errors
    
    if ($LASTEXITCODE -le 1) {
        Write-Log "Sync completed successfully: $Direction" "SUCCESS"
        return $true
    } else {
        Write-Log "Sync encountered errors (exit code: $LASTEXITCODE)" "WARNING"
        foreach ($line in $output) {
            Add-Content -Path $logFile -Value $line
        }
        return $false
    }
}

# ============== MAIN EXECUTION ==============

Write-Log "Synchronisation Starting - Direction: $SyncDirection" "INFO"
Write-Log "Vault Path: $vaultPath" "INFO"
Write-Log "GitHub Path: $githubPath" "INFO"

# Validation des chemins
if (-not (Test-Path $vaultPath)) {
    Write-Log "Vault path not found: $vaultPath" "ERROR"
    exit 1
}

if (-not (Test-Path $githubPath)) {
    Write-Log "GitHub path not found: $githubPath" "ERROR"
    exit 1
}

try {
    switch ($SyncDirection) {
        "VaultToGitHub" {
            $success = Invoke-RoboCopy -Source $vaultPath -Destination $githubPath -Direction "Vault → GitHub (Primary Backup)"
        }
        
        "GitHubToVault" {
            $success = Invoke-RoboCopy -Source $githubPath -Destination $vaultPath -Direction "GitHub → Vault (Dev Files)"
        }
        
        "BiSync" {
            Write-Log "Bi-directional sync: Phase 1 (GitHub → Vault)" "INFO"
            $success1 = Invoke-RoboCopy -Source $githubPath -Destination $vaultPath -Direction "Phase 1: GitHub → Vault"
            
            if ($success1) {
                Write-Log "Bi-directional sync: Phase 2 (Vault → GitHub)" "INFO"
                $success = Invoke-RoboCopy -Source $vaultPath -Destination $githubPath -Direction "Phase 2: Vault → GitHub"
            } else {
                $success = $false
            }
        }
    }
    
    if ($success) {
        Write-Log "✅ Synchronisation COMPLETED SUCCESSFULLY" "SUCCESS"
        
        # Statut final
        $vaultSize = (Get-ChildItem $vaultPath -Recurse -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum / 1GB
        $githubSize = (Get-ChildItem $githubPath -Recurse -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum / 1GB
        
        Write-Log "Vault size: $([Math]::Round($vaultSize, 2)) GB" "INFO"
        Write-Log "GitHub size: $([Math]::Round($githubSize, 2)) GB" "INFO"
        Write-Log "Log file: $logFile" "INFO"
        exit 0
    } else {
        Write-Log "❌ Synchronisation FAILED - Check logs" "ERROR"
        exit 2
    }
}
catch {
    Write-Log "Exception occurred: $($_.Exception.Message)" "ERROR"
    Write-Log $_.ScriptStackTrace "ERROR"
    exit 1
}
