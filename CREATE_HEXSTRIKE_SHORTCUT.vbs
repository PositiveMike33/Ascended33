' ============================================================================
' CREATE_HEXSTRIKE_SHORTCUT.vbs — Create Desktop Shortcut for HexStrike
' ============================================================================

Set objWshShell = CreateObject("WScript.Shell")
Set objFSO = CreateObject("Scripting.FileSystemObject")

' Paths
strDesktop = objWshShell.SpecialFolders("Desktop")
strVault = "D:\Vault\Vault\Ascended33"
strShortcut = strDesktop & "\HexStrike.lnk"
strTarget = strVault & "\LAUNCH_HEXSTRIKE.bat"

' Check if vault path exists
If Not objFSO.FolderExists(strVault) Then
    MsgBox "Vault path not found: " & strVault, vbCritical, "Error"
    WScript.Quit 1
End If

' Create shortcut
Set objShortcut = objWshShell.CreateShortcut(strShortcut)
objShortcut.TargetPath = strTarget
objShortcut.WorkingDirectory = strVault
objShortcut.Description = "HexStrike - Cybersecurity Research Platform with 150+ Red Team Tools"
objShortcut.WindowStyle = 1
objShortcut.Save

' Create README
strReadme = strDesktop & "\HexStrike_README.txt"
Set objFile = objFSO.CreateTextFile(strReadme, True)
objFile.WriteLine "╔════════════════════════════════════════════════════════════════════════╗"
objFile.WriteLine "║                     🔐 HEXSTRIKE LAUNCHER                              ║"
objFile.WriteLine "║            Cybersecurity Research Platform - Quick Start               ║"
objFile.WriteLine "╚════════════════════════════════════════════════════════════════════════╝"
objFile.WriteLine ""
objFile.WriteLine "📌 QUICK START"
objFile.WriteLine "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
objFile.WriteLine ""
objFile.WriteLine "1. Double-click HexStrike.lnk to launch"
objFile.WriteLine "2. Wait for Docker containers to start (~30-60 seconds)"
objFile.WriteLine "3. Browser will open to http://localhost:8501 automatically"
objFile.WriteLine "4. Select tool from sidebar and launch scans"
objFile.WriteLine ""
objFile.WriteLine "📡 ENDPOINTS"
objFile.WriteLine "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
objFile.WriteLine ""
objFile.WriteLine "Streamlit Dashboard:  http://localhost:8501"
objFile.WriteLine "HexStrike API:        http://localhost:8001"
objFile.WriteLine "HackerGPT:            http://localhost:8000"
objFile.WriteLine "Tor Network:          localhost:9050 (SOCKS5)"
objFile.WriteLine ""
objFile.WriteLine "🛠️  AVAILABLE TOOLS (150+)"
objFile.WriteLine "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
objFile.WriteLine ""
objFile.WriteLine "Scanning & Recon:    nmap, masscan, nessus, nuclei, shodan, censys"
objFile.WriteLine "Web Security:        burpsuite, zaproxy, wfuzz, sqlmap, nuclei, ffuf"
objFile.WriteLine "OSINT & Intelligence: maltego, spiderfoot, recon-ng, theHarvester"
objFile.WriteLine "Enumeration:         enum4linux, snmp-check, ldap-search, smtp-user-enum"
objFile.WriteLine "Cloud Security:      aws-enum, azure-enum, gcp-enum, s3-scanner"
objFile.WriteLine "Exploitation:        metasploit, hashcat, john, hydra, aircrack-ng"
objFile.WriteLine "And 100+ more tools!"
objFile.WriteLine ""
objFile.Close

MsgBox "✅ HexStrike shortcut created successfully!" & vbCrLf & vbCrLf & _
        "📁 Location: " & strShortcut & vbCrLf & vbCrLf & _
        "📖 Quick guide: " & strReadme & vbCrLf & vbCrLf & _
        "🚀 You can now launch HexStrike from your Desktop", vbInformation, "HexStrike Setup Complete"
