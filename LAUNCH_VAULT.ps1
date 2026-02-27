# ============================================================
# VAULT MASTER LAUNCHER - Michael G. Guillet
# Lance 100% du projet en une seule commande
# ============================================================

$VaultPath    = "D:\Vault\Vault"
$Ascended33   = "$VaultPath\_INFRASTRUCTURE\Ascended33"
$ObsidianExe  = "C:\Users\th3th\AppData\Local\Obsidian\Obsidian.exe"
$StreamlitApp = "$VaultPath\_INFRASTRUCTURE\Ascended33\streamlit_app.py"
$StreamlitCwd  = "$VaultPath\_INFRASTRUCTURE\Ascended33"

# Cherche le Python
$PythonEnv = "$Ascended33\.venv\Scripts\python.exe"
if (-not (Test-Path $PythonEnv)) { $PythonEnv = "$Ascended33\venv\Scripts\python.exe" }
if (-not (Test-Path $PythonEnv)) { $PythonEnv = "$VaultPath\_INFRASTRUCTURE\.env\Scripts\python.exe" }
if (-not (Test-Path $PythonEnv)) { $PythonEnv = "python" }

# ============================================================
# HELPERS
# ============================================================
function Banner {
    Clear-Host
    Write-Host ""
    Write-Host "  VAULT - Ascended33 Intelligence System" -ForegroundColor Cyan
    Write-Host "  Michael G. Guillet" -ForegroundColor Cyan
    Write-Host "  $(Get-Date -Format 'yyyy-MM-dd HH:mm')" -ForegroundColor Gray
    Write-Host "  ============================================" -ForegroundColor DarkGray
    Write-Host ""
}

function Step { 
    param([string]$Icon, [string]$Msg, [string]$Color = "Cyan")
    Write-Host "  $Icon  $Msg" -ForegroundColor $Color 
}

function OK   { 
    param([string]$Msg) 
    Write-Host "  [+] $Msg" -ForegroundColor Green 
}

function WARN { 
    param([string]$Msg) 
    Write-Host "  [!] $Msg" -ForegroundColor Yellow 
}

function ERR  { 
    param([string]$Msg) 
    Write-Host "  [X] $Msg" -ForegroundColor Red 
}

Banner

# ── 1. DOCKER (containers) ───────────────────────────────────
Write-Host "  [1/5] Docker - Containers" -ForegroundColor Magenta
Write-Host ""

$dockerAvailable = $false
try {
    $testDocker = & docker --version 2>&1
    if ($testDocker -match "version") {
        $dockerAvailable = $true
    }
} 
catch { 
    # Docker not found, continue without it
}

if ($dockerAvailable) {
    try {
        Step "[+]" "Verification des containers..." "Cyan"
        
        # Get list of running containers using native PowerShell
        $containerList = @()
        try {
            $containerList = & docker ps --format "{{.Names}}" 2>$null
        } 
        catch { }
        
        $hasContainers = $false
        if ($containerList) {
            foreach ($item in $containerList) {
                if ($item -match "th3-") {
                    $hasContainers = $true
                }
            }
        }
        
        if ($hasContainers) {
            WARN "Containers deja actifs. Skip rebuild."
        } 
        else {
            Step "[+]" "Demarrage des 4 containers..." "Cyan"
            Push-Location $Ascended33
            
            # Demarrer docker compose
            & docker compose up -d --no-build 2>$null | Out-Null
            Start-Sleep -Seconds 3
            
            # Verifier le démarrage
            $containerList = @()
            try {
                $containerList = & docker ps --format "{{.Names}}" 2>$null
            } 
            catch { }
            
            foreach ($c in @("th3-tor","th3-kali","th3-hackergpt","th3-hexstrike")) {
                $found = $false
                if ($containerList) {
                    foreach ($item in $containerList) {
                        if ($item -eq $c) {
                            $found = $true
                        }
                    }
                }
                
                if ($found) { 
                    OK "$c actif" 
                } 
                else { 
                    WARN "$c non demarre" 
                }
            }
            Pop-Location
        }
    } 
    catch {
        ERR "Docker erreur: $_"
        WARN "Continuons sans Docker..."
    }
} 
else {
    WARN "Docker non trouve. Continuons sans Docker..."
}

Write-Host ""
Start-Sleep -Seconds 1

# ── 2. OBSIDIAN ──────────────────────────────────────────────
Write-Host "  [2/5] Obsidian" -ForegroundColor Magenta
Write-Host ""

$obsidianRunning = Get-Process -Name "Obsidian" -ErrorAction SilentlyContinue
if ($obsidianRunning) {
    WARN "Obsidian deja ouvert. Skip."
} 
else {
    if (Test-Path $ObsidianExe) {
        Step "[+]" "Ouverture d'Obsidian..." "Cyan"
        Start-Process $ObsidianExe
        OK "Obsidian lance"
    } 
    else {
        $obs = Get-Command "obsidian" -ErrorAction SilentlyContinue
        if ($obs) {
            Start-Process "obsidian"
            OK "Obsidian lance (PATH)"
        } 
        else {
            WARN "Obsidian non trouve."
        }
    }
}

Write-Host ""
Start-Sleep -Seconds 1

# ── 3. STREAMLIT (HexStrike + Vault) ─────────────────────────
Write-Host "  [3/5] Streamlit - HexStrike" -ForegroundColor Magenta
Write-Host ""

$streamlitRunning = Get-Process -Name "streamlit" -ErrorAction SilentlyContinue
if ($streamlitRunning) {
    WARN "Streamlit deja actif. Skip."
} 
else {
    if (Test-Path $StreamlitApp) {
        Step "[+]" "Lancement Streamlit sur http://localhost:8501..." "Cyan"
        $streamlitCmd = "Set-Location '$StreamlitCwd'; & '$PythonEnv' -m streamlit run '$StreamlitApp' --server.port 8501 --server.headless false"
        Start-Process powershell -WorkingDirectory $StreamlitCwd -ArgumentList "-NoProfile -WindowStyle Normal -Title 'Streamlit - Ascended33' -Command $streamlitCmd"
        Start-Sleep -Seconds 3
        OK "Streamlit demarre"
    } 
    else {
        $fallback = "$VaultPath\streamlit_app.py"
        if (Test-Path $fallback) {
            Step "[+]" "Lancement Streamlit (vault root)..." "Yellow"
            $streamlitCmd = "& '$PythonEnv' -m streamlit run '$fallback' --server.port 8501 --server.headless false"
            Start-Process powershell -ArgumentList "-NoProfile -WindowStyle Normal -Title 'Streamlit - Ascended33' -Command $streamlitCmd"
            Start-Sleep -Seconds 3
            OK "Streamlit demarre"
        } 
        else {
            WARN "Aucun streamlit_app.py trouve."
        }
    }
}

Write-Host ""
Start-Sleep -Seconds 1

# ── 4. VS CODE ───────────────────────────────────────────────
Write-Host "  [4/5] VS Code" -ForegroundColor Magenta
Write-Host ""

$vsRunning = Get-Process -Name "Code" -ErrorAction SilentlyContinue
if ($vsRunning) {
    WARN "VS Code deja ouvert. Skip."
} 
else {
    Step "[+]" "Ouverture VS Code..." "Cyan"
    try {
        & code $VaultPath 2>$null | Out-Null
        OK "VS Code lance"
    } 
    catch {
        WARN "VS Code non trouve dans PATH."
    }
}

Write-Host ""
Start-Sleep -Seconds 1

# ── 5. NAVIGATEUR ────────────────────────────────────────────
Write-Host "  [5/5] Navigateur" -ForegroundColor Magenta
Write-Host ""

Start-Sleep -Seconds 2
Step "[+]" "Ouverture http://localhost:8501..." "Cyan"
Start-Process "http://localhost:8501"
OK "Navigateur ouvert"

# ── RESUME FINAL ─────────────────────────────────────────────
Write-Host ""
Write-Host "  ============================================" -ForegroundColor DarkGray
Write-Host ""
Write-Host "  [SUCCESS] VAULT OPERATIONNEL" -ForegroundColor Green
Write-Host ""
Write-Host "  Services actifs:" -ForegroundColor White
Write-Host "     DOCKER    => 4 containers (th3-tor, th3-kali, th3-hackergpt, th3-hexstrike)" -ForegroundColor Gray
Write-Host "     OBSIDIAN  => D:\Vault\Vault" -ForegroundColor Gray
Write-Host "     STREAMLIT => http://localhost:8501" -ForegroundColor Gray
Write-Host "     HEXSTRIKE => http://localhost:8001" -ForegroundColor Gray
Write-Host "     HACKERGPT => http://localhost:8000" -ForegroundColor Gray
Write-Host ""
Write-Host "  ============================================" -ForegroundColor DarkGray
Write-Host ""
Write-Host "  Appuie sur Enter pour fermer cette fenetre..." -ForegroundColor DarkGray
Read-Host | Out-Null
