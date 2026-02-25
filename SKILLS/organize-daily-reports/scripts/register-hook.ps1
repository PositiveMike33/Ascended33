#requires -Version 5.0

param(
    [string]$ClaudeCodePath = "$env:USERPROFILE\.claude",
    [string]$Schedule = "0 9 * * *",
    [string]$Timezone = "UTC",
    [switch]$DryRun
)

# Configuration
$skillName = "organize-daily-reports"
$skillPath = "D:\Vault\Vault\SKILLS\organize-daily-reports"
$hooksDir = Join-Path $ClaudeCodePath "hooks"

# Hook definition
$hookConfig = @{
    id           = "organize-daily-reports-hook"
    name         = "organize-daily-reports-automated"
    description  = "Daily automatic organization of report files from THIRTY3/daily"
    enabled      = $true
    type         = "scheduled"
    schedule     = $Schedule
    timezone     = $Timezone
    skill        = $skillName
    parameters   = @{
        source_path          = "D:\Vault\Vault\THIRTY3\daily"
        destination_base     = "D:\Vault\Vault\REPORT\declassified report\02 Rapport Février"
        dry_run              = $false
        verbose              = $true
        notify_on_completion = $true
    }
    notifications = @{
        on_success = $true
        on_error   = $true
        digest     = "weekly"
    }
    created_at   = (Get-Date -Format "o")
    created_by   = "organize-daily-reports-skill"
}

Write-Host "Hook Registration" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Validate paths
if (-not (Test-Path $skillPath)) {
    Write-Error "Skill path not found: $skillPath"
    exit 1
}

Write-Host "Skill path verified: $skillPath" -ForegroundColor Green

# Create hooks directory if needed
if (-not (Test-Path $hooksDir)) {
    if ($DryRun) {
        Write-Host "[DRY RUN] Would create hooks directory: $hooksDir"
    } else {
        New-Item -Path $hooksDir -ItemType Directory -Force | Out-Null
        Write-Host "Created hooks directory: $hooksDir" -ForegroundColor Green
    }
}

# Hook configuration file path
$hookFile = Join-Path $hooksDir "$($hookConfig.id).json"

Write-Host ""
Write-Host "Hook Configuration:" -ForegroundColor Cyan
Write-Host "  Name:        $($hookConfig.name)"
Write-Host "  Schedule:    $Schedule"
Write-Host "  Timezone:    $Timezone"
Write-Host "  Type:        $($hookConfig.type)"
Write-Host ""
Write-Host "Parameters:" -ForegroundColor Cyan
Write-Host "  Source:      $($hookConfig.parameters.source_path)"
Write-Host "  Destination: $($hookConfig.parameters.destination_base)"
Write-Host "  Dry Run:     $($hookConfig.parameters.dry_run)"
Write-Host "  Verbose:     $($hookConfig.parameters.verbose)"
Write-Host ""

if ($DryRun) {
    Write-Host "[DRY RUN] Would save Hook config to: $hookFile" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Configuration preview:" -ForegroundColor Cyan
    $hookConfig | ConvertTo-Json -Depth 3 | Write-Host
} else {
    # Save configuration
    $hookConfig | ConvertTo-Json -Depth 3 | Set-Content -Path $hookFile -Encoding UTF8
    
    if (Test-Path $hookFile) {
        Write-Host "Hook registered successfully" -ForegroundColor Green
        Write-Host "  Location: $hookFile" -ForegroundColor Green
    } else {
        Write-Error "Failed to save Hook configuration"
        exit 1
    }
}

Write-Host ""
Write-Host "================================" -ForegroundColor Cyan
Write-Host "Next Steps:" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host "1. Restart Claude Code to load the Hook"
Write-Host "2. Go to Hooks settings and verify the Hook appears"
Write-Host "3. Click Test Hook to manually trigger execution"
Write-Host "4. Check logs at: $skillPath\reports\automation-log.txt"
Write-Host ""
Write-Host "Documentation: $skillPath\HOOK-CONFIG.md" -ForegroundColor Yellow
Write-Host ""
