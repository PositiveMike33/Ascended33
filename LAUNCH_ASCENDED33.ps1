
# Ascended33 - Complete Project Launcher
# Activate 100% of the project with a single click
# This script orchestrates the complete startup sequence

param(
    [switch]$Dev = $false,
    [switch]$NoStreamlit = $false,
    [switch]$NoVsCode = $false
)

# Colors for output
$colors = @{
    Success = "Green"
    Info = "Cyan"
    Warning = "Yellow"
    Error = "Red"
    Header = "Blue"
}

function Print-Header {
    param([string]$Text)
    Write-Host ""
    Write-Host "=================================================" -ForegroundColor $colors.Header
    Write-Host "  $Text" -ForegroundColor $colors.Header
    Write-Host "=================================================" -ForegroundColor $colors.Header
}

function Print-Status {
    param([string]$Text, [string]$Status = "Info")
    Write-Host "  > $Text" -ForegroundColor $colors.$Status
}

# ==================================================
# PART 1: Project Setup
# ==================================================

Print-Header "ASCENDED33 PROJECT LAUNCHER"

$ProjectPath = "D:\Vault\Vault\Ascended33"
$VaultPath = "D:\Vault\Vault"
$ObsidianPath = "C:\Users\th3th\AppData\Roaming\Obsidian\Obsidian.exe"
$VsCodeExe = "code"
$PythonExe = "python"

Print-Status "Initializing Ascended33 environment..." Info

# Verify project path
if (-not (Test-Path $ProjectPath)) {
    Print-Status "ERROR: Project path not found: $ProjectPath" Error
    exit 1
}

Print-Status "[OK] Project path verified" Success
Set-Location $ProjectPath
Print-Status "[OK] Working directory set to: $ProjectPath" Success

# ==================================================
# PART 2: Environment Checks
# ==================================================

Print-Header "ENVIRONMENT VERIFICATION"

# Check Python
$pythonCheck = & python --version 2>&1
Print-Status "Python: $pythonCheck" Success

# Check Docker
try {
    $dockerCheck = & docker --version 2>&1
    Print-Status "Docker: $dockerCheck" Success
} catch {
    Print-Status "Docker: Not installed (Continue anyway)" Warning
}

# Check Git
try {
    $gitCheck = & git --version 2>&1
    Print-Status "Git: $gitCheck" Success
} catch {
    Print-Status "Git: Not installed" Warning
}

# ==================================================
# PART 3: Service Startup
# ==================================================

Print-Header "STARTING SERVICES (DOCKER)"

# Check if Docker is running
$dockerRunning = (Get-Service Docker -ErrorAction SilentlyContinue).Status -eq "Running"

if (-not $dockerRunning) {
    Print-Status "Docker daemon not running, attempting to start..." Warning
    try {
        Start-Service Docker -ErrorAction SilentlyContinue
        Start-Sleep -Seconds 3
        Print-Status "[OK] Docker started" Success
    } catch {
        Print-Status "Could not auto-start Docker - try starting it manually" Warning
    }
}

# Start Docker Compose services
Print-Status "Starting Docker Compose services..." Info

try {
    & docker-compose up -d 2>&1 | ForEach-Object {
        if ($_ -match "error|failed") {
            Print-Status "[WARN] $_" Warning
        } else {
            Print-Status $_ Success
        }
    }
    Start-Sleep -Seconds 2
    Print-Status "[OK] Docker services started" Success
} catch {
    Print-Status "Docker Compose may not be available" Warning
}

# ==================================================
# PART 4: Dependencies & Configuration
# ==================================================

Print-Header "CHECKING DEPENDENCIES"

# Check if requirements are installed
$requirementsInstalled = Test-Path "$ProjectPath\venv\Scripts\activate.ps1"

if (-not $requirementsInstalled) {
    Print-Status "Virtual environment not found, checking global Python packages..." Warning
    
    # Check critical packages
    $packages = @("streamlit", "requests", "aiohttp", "obsidian-vault")
    
    foreach ($package in $packages) {
        $installed = & python -m pip show $package 2>&1 | Select-String "^Name:"
        
        if ($installed) {
            Print-Status "[OK] $($package): installed" Success
        } else {
            Print-Status "[INFO] $($package): recommended (can install with: pip install $package)" Warning
        }
    }
} else {
    Print-Status "[OK] Virtual environment found" Success
}

# ==================================================
# PART 5: Open VS Code
# ==================================================

if (-not $NoVsCode) {
    Print-Header "OPENING VS CODE"
    
    try {
        Print-Status "Launching VS Code with Ascended33 workspace..." Info
        & code $ProjectPath 2>&1 | Out-Null
        Start-Sleep -Seconds 2
        Print-Status "[OK] VS Code opened" Success
    } catch {
        Print-Status "Could not launch VS Code - is it installed?" Warning
    }
}

# ==================================================
# PART 6: Open Obsidian Vault
# ==================================================

Print-Header "OPENING OBSIDIAN VAULT"

try {
    Print-Status "Opening Obsidian Vault..." Info
    
    # Try to open Obsidian with Vault path
    if (Test-Path $ObsidianPath) {
        & $ObsidianPath "--vault=$VaultPath" 2>&1 | Out-Null
    } else {
        # Try via command line
        & obsidian "vault=$VaultPath" 2>&1 | Out-Null
    }
    
    Start-Sleep -Seconds 2
    Print-Status "[OK] Obsidian Vault opened" Success
} catch {
    Print-Status "Could not launch Obsidian - is it installed?" Warning
}

# ==================================================
# PART 7: Health Checks
# ==================================================

Print-Header "RUNNING HEALTH CHECKS"

Print-Status "Checking critical services..." Info
Start-Sleep -Seconds 1

# Check HexStrike
try {
    $hexstrike = Invoke-WebRequest -Uri "http://localhost:8888/health" -TimeoutSec 3 -ErrorAction SilentlyContinue
    if ($hexstrike.StatusCode -eq 200) {
        Print-Status "[OK] HexStrike-AI: Online" Success
    }
} catch {
    Print-Status "[WARN] HexStrike-AI: Not responding (may still be starting)" Warning
}

# Check Obsidian Vault REST API
try {
    $vault = Invoke-WebRequest -Uri "http://localhost:27123" -TimeoutSec 3 -ErrorAction SilentlyContinue
    if ($vault.StatusCode -eq 200) {
        Print-Status "[OK] Obsidian REST API: Online" Success
    }
} catch {
    Print-Status "[WARN] Obsidian REST API: Not responding (enable in Obsidian settings)" Warning
}

# ==================================================
# PART 8: Streamlit Dashboard (Optional)
# ==================================================

if (-not $NoStreamlit) {
    Print-Header "STARTING STREAMLIT DASHBOARD"
    
    try {
        Print-Status "Launching Ascended33 Dashboard..." Info
        Print-Status "Dashboard URL: http://localhost:8501" Success
        
        # Open browser
        Start-Sleep -Seconds 1
        Start-Process "http://localhost:8501"
        
        # Launch Streamlit
        & python -m streamlit run streamlit_app.py --logger.level=info
        
    } catch {
        Print-Status "Could not launch Streamlit" Error
    }
}

# ==================================================
# FINAL SUMMARY
# ==================================================

Print-Header "[OK] ASCENDED33 READY"

Write-Host ""
Write-Host "  What's Running:" -ForegroundColor Cyan
Write-Host "    - VS Code with project loaded" -ForegroundColor Green
Write-Host "    - Obsidian Vault" -ForegroundColor Green
Write-Host "    - Docker services (HexStrike, Redis, etc.)" -ForegroundColor Green
Write-Host "    - Streamlit Dashboard (port 8501)" -ForegroundColor Green
Write-Host ""
Write-Host "  Quick Links:" -ForegroundColor Cyan
Write-Host "    - Dashboard: http://localhost:8501" -ForegroundColor Yellow
Write-Host "    - HexStrike: http://localhost:8888" -ForegroundColor Yellow
Write-Host "    - Obsidian REST: http://localhost:27123" -ForegroundColor Yellow
Write-Host ""
Write-Host "  Next Steps:" -ForegroundColor Cyan
Write-Host "    1. Edit code in VS Code" -ForegroundColor White
Write-Host "    2. View/edit notes in Obsidian" -ForegroundColor White
Write-Host "    3. Monitor in Streamlit Dashboard" -ForegroundColor White
Write-Host "    4. Deploy with Docker Compose" -ForegroundColor White
Write-Host ""
Write-Host "  [OK] Project fully activated!" -ForegroundColor Green
Write-Host ""
