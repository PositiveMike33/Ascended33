# create_shortcut.ps1
# Cree un raccourci "Ascended33" sur le bureau
#
# Lancer UNE SEULE FOIS depuis PowerShell :
#   powershell -ExecutionPolicy Bypass -File "D:\Vault\Vault\Ascended33\create_shortcut.ps1"

$RepoPath     = Split-Path -Parent $MyInvocation.MyCommand.Path
$BatchFile    = "$RepoPath\start_ascended33.bat"
$Desktop      = [Environment]::GetFolderPath("Desktop")
$ShortcutPath = "$Desktop\Ascended33.lnk"

# Verifier que le .bat existe
if (-not (Test-Path $BatchFile)) {
    Write-Host ""
    Write-Host " [ERREUR] Fichier introuvable : $BatchFile" -ForegroundColor Red
    Write-Host " Verifiez que REPO_PATH est correct dans ce script." -ForegroundColor Yellow
    exit 1
}

# Debloquer tous les .bat et .ps1 du repo (supprimer le marqueur "telecharge d internet")
Write-Host " Deblocage des fichiers du repo..." -ForegroundColor Gray
Get-ChildItem -Path $RepoPath -Recurse -Include "*.bat","*.ps1" | ForEach-Object {
    Unblock-File -Path $_.FullName -ErrorAction SilentlyContinue
}
Write-Host " [OK] Fichiers debloquees." -ForegroundColor Gray

# Supprimer l ancien raccourci si existant
if (Test-Path $ShortcutPath) {
    Remove-Item $ShortcutPath -Force
}

$WScriptShell = New-Object -ComObject WScript.Shell
$Shortcut = $WScriptShell.CreateShortcut($ShortcutPath)

$Shortcut.TargetPath       = "C:\Windows\System32\cmd.exe"
$Shortcut.Arguments        = "/k `"$BatchFile`""
$Shortcut.WorkingDirectory = $RepoPath
$Shortcut.Description      = "Ascended33 - Lance Kali VM, hexstrike-ai, Obsidian et le dashboard"
$Shortcut.WindowStyle      = 1

# Icone : VMware en priorite, sinon cmd
$Icons = @(
    "C:\Program Files (x86)\VMware\VMware Workstation\vmware.exe",
    "C:\Program Files\VMware\VMware Workstation\vmware.exe",
    "C:\Windows\System32\cmd.exe"
)
foreach ($icon in $Icons) {
    if (Test-Path $icon) {
        $Shortcut.IconLocation = "$icon,0"
        break
    }
}

$Shortcut.Save()

Write-Host ""
Write-Host " [OK] Raccourci cree : $ShortcutPath" -ForegroundColor Green
Write-Host ""
Write-Host " Au double-clic, le launcher fait dans l ordre :" -ForegroundColor Cyan
Write-Host "   [1/4]  Kali VM demarre dans VMware (skip si deja en ligne)" -ForegroundColor White
Write-Host "   [2/4]  hexstrike-ai MCP server demarre sur Kali (port 8888)" -ForegroundColor White
Write-Host "   [3/4]  Obsidian ouvre D:\Vault" -ForegroundColor White
Write-Host "   [4/4]  Dashboard Ascended33 : http://localhost:8501" -ForegroundColor White
Write-Host ""
