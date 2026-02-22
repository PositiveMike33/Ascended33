@echo off
REM ================================================================
REM  OSINT Investigation Platform - Lancement Rapide
REM  Infrastructure Anonyme + Légale pour Enquêtes
REM ================================================================

setlocal enabledelayedexpansion

echo.
echo 🕵️  ========================================
echo    OSINT Investigation Platform v2.0
echo    Anonymité + Légalité
echo ========================================
echo.

REM Vérification Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python non trouvé!
    echo Installez Python depuis https://python.org
    pause
    exit /b 1
)

REM Vérification Docker
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker non trouvé!
    echo Installez Docker depuis https://docker.com
    pause
    exit /b 1
)

echo ✅ Environnement vérifiée
echo.
echo 🚀 Démarrage de la session OSINT...
echo.

REM Lance l'orchestrateur
python docker_orchestrator_osint.py

if errorlevel 1 (
    echo.
    echo ❌ Erreur lors du démarrage
    echo Vérifiez avec: powershell -ExecutionPolicy Bypass -File "VERIFY_OSINT_SETUP.ps1"
    pause
    exit /b 1
)

REM Affiche les services
echo.
echo ✅ Session OSINT démarrée avec succès!
echo.
echo Services disponibles:
echo   🤖 HackerGPT: http://localhost:8000
echo   🔍 Hexstrike: http://localhost:8001
echo   🔐 Tor: localhost:9050 (SOCKS5)
echo.
echo 💡 Appuyez sur Ctrl+C dans cette fenêtre pour arrêter
echo.

pause
