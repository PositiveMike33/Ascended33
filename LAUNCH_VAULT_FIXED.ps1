# Vault Launcher - Fixed Version
$VaultPath = "D:\Vault\Vault"
$Ascended33 = "$VaultPath\_INFRASTRUCTURE\Ascended33"
$ObsidianExe = "C:\Users\th3th\AppData\Local\Obsidian\Obsidian.exe"
$PythonEnv = "$VaultPath\_INFRASTRUCTURE\.env\Scripts\python.exe"

# ASCII Banner
Clear-Host
Write-Host ""
Write-Host "  VAULT LAUNCHER" -ForegroundColor Cyan
Write-Host "  $(Get-Date -Format 'yyyy-MM-dd HH:mm')" -ForegroundColor Gray
Write-Host ""

# 1. Docker
Write-Host "  [1/5] Docker - Launching containers..." -ForegroundColor Magenta
try {
    Push-Location $Ascended33
    docker-compose up -d 2>$null
    Write-Host "  OK - Docker containers started" -ForegroundColor Green
    Pop-Location
} catch {
    Write-Host "  WARNING - Docker not available or failed" -ForegroundColor Yellow
}

Start-Sleep -Seconds 2

# 2. Obsidian
Write-Host "  [2/5] Obsidian - Vault" -ForegroundColor Magenta
if (Test-Path $ObsidianExe) {
    Start-Process $ObsidianExe
    Write-Host "  OK - Obsidian started" -ForegroundColor Green
} else {
    Write-Host "  WARNING - Obsidian not found" -ForegroundColor Yellow
}

Start-Sleep -Seconds 2

# 3. Streamlit
Write-Host "  [3/5] Streamlit - Ascended33 Dashboard" -ForegroundColor Magenta
$streamlitApp = "$Ascended33\streamlit_app.py"
if (Test-Path $streamlitApp) {
    $pythonToUse = if (Test-Path $PythonEnv) { $PythonEnv } else { "python" }
    Start-Process powershell -ArgumentList "-NoProfile -Command `"cd '$Ascended33' && & '$pythonToUse' -m streamlit run streamlit_app.py --server.port 8501`""
    Write-Host "  OK - Streamlit started at http://localhost:8501" -ForegroundColor Green
} else {
    Write-Host "  WARNING - streamlit_app.py not found" -ForegroundColor Yellow
}

Start-Sleep -Seconds 2

# 4. VS Code
Write-Host "  [4/5] VS Code - Vault workspace" -ForegroundColor Magenta
if (Get-Command code -ErrorAction SilentlyContinue) {
    Start-Process code -ArgumentList $VaultPath
    Write-Host "  OK - VS Code started" -ForegroundColor Green
} else {
    Write-Host "  WARNING - VS Code not installed" -ForegroundColor Yellow
}

Start-Sleep -Seconds 2

# 5. Summary
Write-Host "  [5/5] Launch Complete" -ForegroundColor Magenta
Write-Host ""
Write-Host "  Services running:" -ForegroundColor Cyan
Write-Host "     Obsidian (Vault)" -ForegroundColor Gray
Write-Host "     Streamlit Dashboard - http://localhost:8501" -ForegroundColor Gray
Write-Host "     VS Code - Vault workspace" -ForegroundColor Gray
Write-Host "     Docker containers (if available)" -ForegroundColor Gray
Write-Host ""
Write-Host "  Press Enter to close this window..." -ForegroundColor DarkGray
Read-Host | Out-Null
