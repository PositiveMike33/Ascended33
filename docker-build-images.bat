@echo off
setlocal enabledelayedexpansion

REM =================================================
REM  BUILD ALL DOCKER IMAGES
REM =================================================

echo.
echo =================================================
echo   BUILDING DOCKER IMAGES
echo =================================================
echo.

cd /d "%~dp0"

REM Check Docker
echo [*] Checking Docker...
docker ps >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Docker not running
    exit /b 1
)

REM Build images with docker-compose
echo [*] Building images (this may take 10-20 minutes)...
echo.

docker-compose build --no-cache

if %errorlevel% neq 0 (
    echo [!] Build failed
    pause
    exit /b 1
)

echo.
echo [OK] Images built successfully!
echo.
