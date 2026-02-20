@echo off
REM =================================================
REM  ASCENDED33 DOCKER SETUP - BUILD & LAUNCH
REM =================================================
REM This script builds all required Docker images and starts the stack

setlocal enabledelayedexpansion

echo.
echo =================================================
echo   ASCENDED33 DOCKER SETUP & BUILD
echo =================================================
echo.

REM Check if running as admin
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] This script must be run as Administrator
    echo [*] Please re-run this script as Administrator
    pause
    exit /b 1
)

REM Change to script directory
cd /d "%~dp0"

REM Start Docker if not running
echo [*] Checking Docker daemon...
docker ps >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Docker daemon not running, starting...
    start "" "C:\Program Files\Docker\Docker\Docker.exe"
    timeout /t 10 /nobreak
)

REM Build Docker images
echo.
echo [*] Building Docker images...
echo.

REM Build using docker-compose with explicit image tags
docker-compose -f docker-compose.yml build --no-cache

if %errorlevel% neq 0 (
    echo [!] Docker build failed
    pause
    exit /b 1
)

echo.
echo [OK] Docker images built successfully
echo.

REM Start services
echo [*] Starting Docker Compose services...
docker-compose up -d

if %errorlevel% neq 0 (
    echo [!] Docker Compose startup failed
    pause
    exit /b 1
)

echo.
echo [OK] Docker services starting...
timeout /t 15 /nobreak

REM Show status
echo.
echo =================================================
echo   SERVICE STATUS
echo =================================================
docker-compose ps

echo.
echo [OK] ASCENDED33 Docker setup complete!
echo.
echo Next steps:
echo   1. Open Streamlit dashboard: http://localhost:8501
echo   2. Check HexStrike status: http://localhost:8001/status
echo   3. View logs: docker-compose logs -f
echo.

pause
