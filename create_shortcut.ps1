# create_shortcut.ps1
# Cree un raccourci "Ascended33" sur le bureau
# Lancer UNE SEULE FOIS depuis PowerShell :
#   powershell -ExecutionPolicy Bypass -File "D:\Vault\Vault\Ascended33\create_shortcut.ps1"

$RepoPath    = "D:\Vault\Vault\Ascended33"
$BatchFile   = "$RepoPath\start_ascended33.bat"
$Desktop     = [Environment]::GetFolderPath("Desktop")
$ShortcutPath = "$Desktop\Ascended33.lnk"

$WScriptShell = New-Object -ComObject WScript.Shell
$Shortcut = $WScriptShell.CreateShortcut($ShortcutPath)

$Shortcut.TargetPath       = $BatchFile
$Shortcut.WorkingDirectory = $RepoPath
$Shortcut.Description      = "Lancer le dashboard Ascended33"
$Shortcut.IconLocation     = "C:\Windows\System32\cmd.exe,0"
$Shortcut.WindowStyle      = 1

$Shortcut.Save()

Write-Host ""
Write-Host " [OK] Raccourci cree sur le bureau : $ShortcutPath" -ForegroundColor Green
Write-Host " Double-clique sur 'Ascended33' pour tout lancer automatiquement." -ForegroundColor Cyan
Write-Host ""
