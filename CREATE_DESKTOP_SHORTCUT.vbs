' ============================================================
' Créateur de raccourci bureau — VAULT LAUNCHER
' Double-cliquer ce fichier UNE SEULE FOIS pour créer le raccourci
' ============================================================

Dim WshShell, oShortcut, strDesktop

Set WshShell  = CreateObject("WScript.Shell")
strDesktop    = WshShell.SpecialFolders("Desktop")

Set oShortcut = WshShell.CreateShortcut(strDesktop & "\🚀 VAULT LAUNCH.lnk")

' Commande: PowerShell silencieux (sans fenêtre noire cmd)
oShortcut.TargetPath       = "PowerShell.exe"
oShortcut.Arguments        = "-NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File ""D:\Vault\Vault\LAUNCH_VAULT.ps1"""
oShortcut.WorkingDirectory = "D:\Vault\Vault"
oShortcut.WindowStyle      = 1
oShortcut.Description      = "Lance 100% du projet Vault (Docker, Obsidian, Streamlit, VS Code)"

' Icône PowerShell par défaut (belle icône bleue)
oShortcut.IconLocation = "C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe, 0"

oShortcut.Save

MsgBox "✅ Raccourci créé sur le Bureau!" & Chr(13) & Chr(10) & Chr(13) & Chr(10) & "Double-cliquez sur '🚀 VAULT LAUNCH' pour tout démarrer.", 64, "Vault Launcher"

Set oShortcut = Nothing
Set WshShell  = Nothing
