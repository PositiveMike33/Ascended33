# setup.ps1 - Ascended33 Bootstrap universel
#
# Lance ce script UNE SEULE FOIS sur chaque nouvelle machine :
#   powershell -ExecutionPolicy Bypass -File ".\setup.ps1"
#
# Ce script installe et configure tout automatiquement :
#   - Git, Python 3.13, Obsidian (via winget)
#   - Packages Python (requirements.txt)
#   - Cle SSH Kali (si presente dans config\ssh\)
#   - Raccourci bureau Ascended33

$RepoPath = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host ""
Write-Host " +==========================================+" -ForegroundColor Cyan
Write-Host " |     ASCENDED33  SETUP & BOOTSTRAP       |" -ForegroundColor Cyan
Write-Host " |  Configure ce PC pour travailler        |" -ForegroundColor Cyan
Write-Host " +==========================================+" -ForegroundColor Cyan
Write-Host ""

# --- Debloquer tous les fichiers du repo ---
Write-Host "[0] Deblocage des fichiers du repo..." -ForegroundColor Yellow
Get-ChildItem -Path $RepoPath -Recurse -Include "*.bat","*.ps1","*.py" -ErrorAction SilentlyContinue | ForEach-Object {
    Unblock-File -Path $_.FullName -ErrorAction SilentlyContinue
}
Write-Host " [OK] Fichiers debloquees." -ForegroundColor Green
Write-Host ""

# --- 1. Git ---
Write-Host "[1/6] Git..." -ForegroundColor Yellow
if (Get-Command git -ErrorAction SilentlyContinue) {
    Write-Host " [OK] Git deja installe." -ForegroundColor Green
} else {
    Write-Host " Installation de Git via winget..." -ForegroundColor Gray
    winget install --id Git.Git -e --silent --accept-package-agreements --accept-source-agreements
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
    Write-Host " [OK] Git installe." -ForegroundColor Green
}

# --- 2. Python ---
Write-Host "[2/6] Python..." -ForegroundColor Yellow
$PythonExe = $null
$PythonCandidates = @(
    "$env:LOCALAPPDATA\Programs\Python\Python313\python.exe",
    "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe",
    "$env:LOCALAPPDATA\Programs\Python\Python311\python.exe"
)
foreach ($p in $PythonCandidates) {
    if (Test-Path $p) { $PythonExe = $p; break }
}
if (-not $PythonExe) {
    $found = Get-Command python -ErrorAction SilentlyContinue
    if ($found) { $PythonExe = $found.Source }
}
if ($PythonExe) {
    Write-Host " [OK] Python trouve : $PythonExe" -ForegroundColor Green
} else {
    Write-Host " Installation de Python 3.13 via winget..." -ForegroundColor Gray
    winget install --id Python.Python.3.13 -e --silent --accept-package-agreements --accept-source-agreements
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
    $PythonExe = "$env:LOCALAPPDATA\Programs\Python\Python313\python.exe"
    Write-Host " [OK] Python installe." -ForegroundColor Green
}

# --- 3. Packages Python ---
Write-Host "[3/6] Packages Python (requirements.txt)..." -ForegroundColor Yellow
$ReqFile = Join-Path $RepoPath "requirements.txt"
if (Test-Path $ReqFile) {
    & $PythonExe -m pip install -r $ReqFile --quiet --disable-pip-version-check
    Write-Host " [OK] Packages installes." -ForegroundColor Green
} else {
    Write-Host " [WARN] requirements.txt introuvable." -ForegroundColor Yellow
}

# --- 4. Obsidian ---
Write-Host "[4/6] Obsidian..." -ForegroundColor Yellow
$ObsidianExe = "$env:LOCALAPPDATA\Obsidian\Obsidian.exe"
if (Test-Path $ObsidianExe) {
    Write-Host " [OK] Obsidian deja installe." -ForegroundColor Green
} else {
    Write-Host " Installation d Obsidian via winget..." -ForegroundColor Gray
    winget install --id Obsidian.Obsidian -e --silent --accept-package-agreements --accept-source-agreements
    Write-Host " [OK] Obsidian installe." -ForegroundColor Green
}

# --- 5. Cle SSH Kali ---
Write-Host "[5/6] Cle SSH Kali..." -ForegroundColor Yellow
$SshDir     = "$env:USERPROFILE\.ssh"
$SshKeyDest = "$SshDir\kali_lab_key"
$SshKeySrc  = Join-Path $RepoPath "config\ssh\kali_lab_key"

if (Test-Path $SshKeyDest) {
    Write-Host " [OK] Cle SSH deja presente dans ~/.ssh/" -ForegroundColor Green
} elseif (Test-Path $SshKeySrc) {
    if (-not (Test-Path $SshDir)) { New-Item -ItemType Directory -Path $SshDir | Out-Null }
    Copy-Item $SshKeySrc $SshKeyDest
    icacls $SshKeyDest /inheritance:r /grant:r "${env:USERNAME}:(R)" | Out-Null
    Write-Host " [OK] Cle SSH copiee vers $SshKeyDest" -ForegroundColor Green
} else {
    Write-Host " [INFO] Cle SSH non trouvee sur le disque." -ForegroundColor Yellow
    Write-Host "   Pour la portabilite, copie ta cle ici :" -ForegroundColor Gray
    Write-Host "   $SshKeySrc" -ForegroundColor DarkYellow
    Write-Host "   (Ce dossier est gitignore - securise)" -ForegroundColor Gray
}

# --- 6. Raccourci bureau ---
Write-Host "[6/6] Raccourci bureau Ascended33..." -ForegroundColor Yellow
$ShortcutScript = Join-Path $RepoPath "create_shortcut.ps1"
& powershell -ExecutionPolicy Bypass -File $ShortcutScript

# --- Resume ---
Write-Host ""
Write-Host " +==========================================+" -ForegroundColor Green
Write-Host " |   SETUP TERMINE - Pret a travailler !   |" -ForegroundColor Green
Write-Host " +------------------------------------------+" -ForegroundColor Green
Write-Host " |  Double-clic sur 'Ascended33' (bureau)  |" -ForegroundColor White
Write-Host " |  pour tout lancer automatiquement.      |" -ForegroundColor White
Write-Host " +==========================================+" -ForegroundColor Green
Write-Host ""
Write-Host " Note : VMware Workstation doit etre installe manuellement" -ForegroundColor Gray
Write-Host " (logiciel commercial - non automatisable via winget)" -ForegroundColor Gray
Write-Host ""
pause
