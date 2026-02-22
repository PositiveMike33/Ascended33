@echo off
REM Add Python to system PATH
REM This script adds Python314 to the PATH so python command works globally

setlocal enabledelayedexpansion

echo.
echo ============================================================
echo SETUP: Ajout de Python au PATH Systeme
echo ============================================================
echo.

REM Check current PATH
echo Verification de l'installation Python...
set PYTHON_PATH=C:\Users\th3th\AppData\Local\Programs\Python\Python314

if exist "%PYTHON_PATH%\python.exe" (
    echo [OK] Python trouve: %PYTHON_PATH%
) else (
    echo [ERREUR] Python non trouve au chemin attendu
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
echo Pour que les modifications prennent effet:
echo   1. Fermez tous les terminaux CMD/PowerShell ouverts
echo   2. Ouvrez un NOUVEAU terminal
echo   3. Tapez: python --version
echo.
echo ============================================================
pause
