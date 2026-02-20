@echo off
REM Add Python to system PATH - FIXED VERSION
REM This script adds Python313 to the PATH so python command works globally

setlocal enabledelayedexpansion

echo.
echo ============================================================
echo SETUP: Ajout de Python au PATH Systeme [FIXED]
echo ============================================================
echo.

REM Check current PATH
echo Verification de l'installation Python...
set PYTHON_PATH=C:\Users\th3th\AppData\Local\Programs\Python\Python313

if exist "%PYTHON_PATH%\python.exe" (
    echo [OK] Python trouve: %PYTHON_PATH%
    echo [OK] Fichier: %PYTHON_PATH%\python.exe
) else (
    echo [ERREUR] Python non trouve au chemin: %PYTHON_PATH%
    pause
    exit /b 1
)

echo.
echo Ajout de Python au PATH systeme...
echo.

REM Add to user PATH
setx PATH "%PATH%;%PYTHON_PATH%"

echo [OK] Python a ete ajoute au PATH
echo.
echo IMPORTANT - Pour que les modifications prennent effet:
echo   1. Fermez TOUS les terminaux CMD/PowerShell ouverts
echo   2. Ouvrez un NOUVEAU terminal (CMD ou PowerShell)
echo   3. Testez en tapant: python --version
echo.
echo Si cela ne fonctionne pas:
echo   - Redemarrez votre ordinateur
echo   - Ou utilisez le chemin complet:
echo     "%PYTHON_PATH%\python.exe" --version
echo.
echo ============================================================
pause
