@echo off
REM =================================================
REM  BUILD DOCKER IMAGES & START SERVICES
REM =================================================

setlocal enabledelayedexpansion

cd /d "%~dp0"

echo.
echo =================================================
echo   HEXSTRIKE DOCKER BUILD & LAUNCH
echo =================================================
echo.

REM Check Docker
echo [*] Checking Docker daemon...
docker ps >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Docker daemon not running - starting...
    start "" "C:\Program Files\Docker\Docker\Docker.exe"
    timeout /t 10 /nobreak
)

echo [OK] Docker is ready
echo.

REM Build images
echo [*] Building Docker images...
echo [*] Starting build at %time%
echo.

docker-compose build --no-cache

if %errorlevel% neq 0 (
    echo.
    echo [!] Build failed!
    echo [*] Check Docker logs for details
    pause
    exit /b 1
)

echo.
echo [OK] Build complete!
echo.

REM Start services
echo [*] Starting Docker Compose services...
docker-compose up -d

echo.
echo [*] Waiting for services to initialize (15 seconds)...
timeout /t 15 /nobreak

echo.
echo =================================================
echo   SERVICE STATUS
echo =================================================
echo.

docker-compose ps

echo.
echo [OK] Setup complete!
echo.
echo Available endpoints:
echo   - Streamlit Dashboard: http://localhost:8501
echo   - HackerGPT API:       http://localhost:8000
echo   - HexStrike API:       http://localhost:8001
echo   - Tor SOCKS5:          localhost:9050
echo.
echo To view logs:
echo   docker-compose logs -f
echo.

pause
