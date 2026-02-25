@echo off
REM ============================================================
REM 🚀 VAULT MASTER LAUNCHER — Clean PowerShell Session
REM Lance le script dans une nouvelle session PowerShell vierge
REM ============================================================

cd /d "%~dp0"

echo.
echo  ██╗   ██╗ █████╗ ██╗   ██╗██╗  ████████╗
echo  ██║   ██║██╔══██╗██║   ██║██║  ╚══██╔══╝
echo  ██║   ██║███████║██║   ██║██║     ██║
echo  ╚██╗ ██╔╝██╔══██║██║   ██║██║     ██║
echo   ╚████╔╝ ██║  ██║╚██████╔╝███████╗██║
echo    ╚═══╝  ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝
echo.
echo  🧠 Vault Intelligence System
echo  Démarrage dans une nouvelle session PowerShell...
echo.

REM Lance PowerShell avec le chemin complet
"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -ExecutionPolicy Bypass -File "%~dp0LAUNCH_VAULT.ps1"

pause
