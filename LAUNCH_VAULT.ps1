# ============================================================
# 🚀 VAULT MASTER LAUNCHER — Michaël G. Guillet
# Lance 100% du projet en une seule commande
# Double-cliquer sur LAUNCH_VAULT.bat pour démarrer
# ============================================================

$VaultPath    = "D:\Vault\Vault"
$Ascended33   = "$VaultPath\_INFRASTRUCTURE\Ascended33"
$ObsidianExe  = "C:\Users\th3th\AppData\Local\Obsidian\Obsidian.exe"
$StreamlitApp = "$VaultPath\_INFRASTRUCTURE\Ascended33\streamlit_app.py"
$StreamlitCwd  = "$VaultPath\_INFRASTRUCTURE\Ascended33"

# Cherche le Python dans cet ordre : venv Ascended33 > venv Vault > python global
$PythonEnv = "$Ascended33\.venv\Scripts\python.exe"
if (-not (Test-Path $PythonEnv)) { $PythonEnv = "$Ascended33\venv\Scripts\python.exe" }
if (-not (Test-Path $PythonEnv)) { $PythonEnv = "$VaultPath\.env\Scripts\python.exe" }
if (-not (Test-Path $PythonEnv)) { $PythonEnv = "python" }

# ============================================================
# HELPERS
# ============================================================
function Banner {
    Clear-Host
    Write-Host ""
    Write-Host "  ██╗   ██╗ █████╗ ██╗   ██╗██╗  ████████╗" -ForegroundColor Cyan
    Write-Host "  ██║   ██║██╔══██╗██║   ██║██║  ╚══██╔══╝" -ForegroundColor Cyan
    Write-Host "  ██║   ██║███████║██║   ██║██║     ██║   " -ForegroundColor Cyan
    Write-Host "  ╚██╗ ██╔╝██╔══██║██║   ██║██║     ██║   " -ForegroundColor Blue
    Write-Host "   ╚████╔╝ ██║  ██║╚██████╔╝███████╗██║   " -ForegroundColor Blue
    Write-Host "    ╚═══╝  ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝   " -ForegroundColor Blue
    Write-Host ""
    Write-Host "  🧠 Vault Intelligence System — Michaël G. Guillet" -ForegroundColor White
    Write-Host "  📅 $(Get-Date -Format 'yyyy-MM-dd HH:mm')" -ForegroundColor Gray
    Write-Host "  ─────────────────────────────────────────────────" -ForegroundColor DarkGray
    Write-Host ""
}

function Step {
    param([string]$Icon, [string]$Msg, [string]$Color = "Cyan")
    Write-Host "  $Icon  $Msg" -ForegroundColor $Color
}

function OK   { param([string]$Msg) Write-Host "  ✅  $Msg" -ForegroundColor Green }
function WARN { param([string]$Msg) Write-Host "  ⚠️   $Msg" -ForegroundColor Yellow }
function ERR  { param([string]$Msg) Write-Host "  ❌  $Msg" -ForegroundColor Red }

# ============================================================
# DÉMARRAGE
# ============================================================
Banner

# ── 1. DOCKER (containers) ───────────────────────────────────
Write-Host "  [1/5] Docker — Containers Ascended33" -ForegroundColor Magenta
Write-Host ""

$dockerRunning = docker ps 2>&1 | Select-String "th3-"
if ($dockerRunning) {
    WARN "Containers déjà actifs. Skip rebuild."
} else {
    Step "🐳" "Démarrage des 4 containers..." "Cyan"
    try {
        Push-Location $Ascended33
        docker compose up -d --no-build 2>&1 | Out-Null
        $result = docker ps --format "{{.Names}}" 2>&1
        foreach ($c in @("th3-tor","th3-kali","th3-hackergpt","th3-hexstrike")) {
            if ($result -match $c) { OK "$c actif" }
            else { WARN "$c non démarré (image manquante?)" }
        }
        Pop-Location
    } catch {
        ERR "Docker introuvable ou erreur: $_"
        WARN "Continuons sans Docker..."
    }
}

Write-Host ""
Start-Sleep -Seconds 1

# ── 2. OBSIDIAN ──────────────────────────────────────────────
Write-Host "  [2/5] Obsidian — Vault D:\Vault\Vault" -ForegroundColor Magenta
Write-Host ""

$obsidianRunning = Get-Process -Name "Obsidian" -ErrorAction SilentlyContinue
if ($obsidianRunning) {
    WARN "Obsidian déjà ouvert. Skip."
} else {
    if (Test-Path $ObsidianExe) {
        Step "📓" "Ouverture d'Obsidian..." "Cyan"
        Start-Process $ObsidianExe
        OK "Obsidian lancé"
    } else {
        # Fallback: chercher Obsidian dans PATH
        $obs = Get-Command "obsidian" -ErrorAction SilentlyContinue
        if ($obs) {
            Start-Process "obsidian"
            OK "Obsidian lancé (PATH)"
        } else {
            WARN "Obsidian non trouvé. Installez-le ou ajustez le chemin."
        }
    }
}

Write-Host ""
Start-Sleep -Seconds 1

# ── 3. STREAMLIT (HexStrike + Vault) ─────────────────────────
Write-Host "  [3/5] Streamlit — HexStrike Dashboard" -ForegroundColor Magenta
Write-Host ""

$streamlitRunning = Get-Process -Name "streamlit" -ErrorAction SilentlyContinue
if ($streamlitRunning) {
    WARN "Streamlit déjà actif. Skip."
} else {
    if (Test-Path $StreamlitApp) {
        Step "⚡" "Lancement Streamlit sur http://localhost:8501 ..." "Cyan"
        Start-Process powershell -ArgumentList "-NoProfile -WindowStyle Normal -Title 'Streamlit — Ascended33' -Command `"Set-Location '$StreamlitCwd'; & '$PythonEnv' -m streamlit run '$StreamlitApp' --server.port 8501 --server.headless false`""
        Start-Sleep -Seconds 3
        OK "Streamlit démarré → http://localhost:8501"
    } else {
        # Fallback: streamlit_app.py à la racine du vault
        $fallback = "$VaultPath\streamlit_app.py"
        if (Test-Path $fallback) {
            Step "⚡" "Lancement Streamlit (vault root)..." "Yellow"
            Start-Process powershell -ArgumentList "-NoProfile -WindowStyle Normal -Title 'Streamlit — Ascended33' -Command `"& '$PythonEnv' -m streamlit run '$fallback' --server.port 8501 --server.headless false`""
            Start-Sleep -Seconds 3
            OK "Streamlit démarré → http://localhost:8501"
        } else {
            WARN "Aucun streamlit_app.py trouvé. Skip."
        }
    }
}

Write-Host ""
Start-Sleep -Seconds 1

# ── 4. VS CODE ───────────────────────────────────────────────
Write-Host "  [4/5] VS Code — Vault workspace" -ForegroundColor Magenta
Write-Host ""

$vsRunning = Get-Process -Name "Code" -ErrorAction SilentlyContinue
if ($vsRunning) {
    WARN "VS Code déjà ouvert. Skip."
} else {
    Step "💻" "Ouverture VS Code sur le Vault..." "Cyan"
    try {
        code $VaultPath 2>&1 | Out-Null
        OK "VS Code lancé"
    } catch {
        WARN "VS Code non trouvé dans PATH."
    }
}

Write-Host ""
Start-Sleep -Seconds 1

# ── 5. NAVIGATEUR ────────────────────────────────────────────
Write-Host "  [5/5] Navigateur — HexStrike Dashboard" -ForegroundColor Magenta
Write-Host ""

Start-Sleep -Seconds 2
Step "🌐" "Ouverture http://localhost:8501 dans le navigateur..." "Cyan"
Start-Process "http://localhost:8501"
OK "Navigateur ouvert"

# ── RÉSUMÉ FINAL ─────────────────────────────────────────────
Write-Host ""
Write-Host "  ─────────────────────────────────────────────────" -ForegroundColor DarkGray
Write-Host ""
Write-Host "  🎉 VAULT 100% OPÉRATIONNEL" -ForegroundColor Green
Write-Host ""
Write-Host "  📊 Services actifs:" -ForegroundColor White
Write-Host "     🐳  Docker    → 4 containers (Tor/Kali/HackerGPT/HexStrike)" -ForegroundColor Gray
Write-Host "     📓  Obsidian  → D:\Vault\Vault" -ForegroundColor Gray
Write-Host "     ⚡  Streamlit → http://localhost:8501" -ForegroundColor Gray
Write-Host "     🔌  HexStrike → http://localhost:8001" -ForegroundColor Gray
Write-Host "     🌐  HackerGPT → http://localhost:8000" -ForegroundColor Gray
Write-Host ""
Write-Host "  ─────────────────────────────────────────────────" -ForegroundColor DarkGray
Write-Host ""

Write-Host "  Appuie sur Enter pour fermer cette fenêtre..." -ForegroundColor DarkGray
Read-Host | Out-Null
