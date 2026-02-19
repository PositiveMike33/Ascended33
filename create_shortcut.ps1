# create_shortcut.ps1
# Cree un raccourci "Ascended33" sur le bureau
#
# Lancer UNE SEULE FOIS depuis PowerShell :
#   powershell -ExecutionPolicy Bypass -File "D:\Vault\Vault\Ascended33\create_shortcut.ps1"

$RepoPath     = "D:\Vault\Vault\Ascended33"
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

$WScriptShell = New-Object -ComObject WScript.Shell
$Shortcut = $WScriptShell.CreateShortcut($ShortcutPath)

$Shortcut.TargetPath       = $BatchFile
$Shortcut.WorkingDirectory = $RepoPath
$Shortcut.Description      = "Ascended33 — Lance Kali VM, hexstrike-ai, Obsidian et le dashboard"
$Shortcut.WindowStyle      = 1  # Fenetre normale

# Icone : VMware en priorite, sinon PowerShell, sinon cmd
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
Write-Host " Au double-clic, le launcher fera dans l'ordre :" -ForegroundColor Cyan
Write-Host "   [1/4]  Kali VM demarre dans VMware (si pas deja en ligne)" -ForegroundColor White
Write-Host "   [2/4]  hexstrike-ai MCP server demarre sur Kali (port 8888)" -ForegroundColor White
Write-Host "   [3/4]  Obsidian s'ouvre sur D:\Vault" -ForegroundColor White
Write-Host "   [4/4]  Dashboard Ascended33 demarre (http://localhost:8501)" -ForegroundColor White
Write-Host ""
Write-Host " IMPORTANT — Avant de l'utiliser :" -ForegroundColor Yellow
Write-Host "   Verifie KALI_VMX dans start_ascended33.bat" -ForegroundColor Yellow
Write-Host "   Chemin actuel : C:\Users\th3th\Documents\Virtual Machines\Kali-Linux\Kali-Linux.vmx" -ForegroundColor DarkYellow
Write-Host ""
Write-Host " Pour trouver ton .vmx : VMware > VM > Settings > resume le chemin en titre" -ForegroundColor Gray
Write-Host ""
