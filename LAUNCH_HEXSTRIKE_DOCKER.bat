@echo off
REM =================================================
REM  LAUNCH HEXSTRIKE WITH DOCKER
REM =================================================

setlocal enabledelayedexpansion

cd /d "%~dp0"

echo.
echo =================================================
echo   HEXSTRIKE - DOCKER LAUNCH
echo =================================================
echo.

REM Check Docker
echo [*] Checking Docker daemon...
docker ps >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Docker not running, starting...
    start "" "C:\Program Files\Docker\Docker\Docker.exe"
    timeout /t 10 /nobreak
)

REM Launch compose
echo [*] Starting Docker Compose stack...
docker-compose up -d

echo.
echo [*] Waiting for services to initialize...
timeout /t 10 /nobreak

echo.
echo =================================================
echo   SERVICE STATUS
echo =================================================
docker-compose ps

echo.
echo [OK] HexStrike services launching!
echo.
echo Available endpoints:
echo   - Streamlit Dashboard: http://localhost:8501
echo   - HackerGPT API:        http://localhost:8000
echo   - HexStrike API:        http://localhost:8001
echo   - Tor SOCKS5:           localhost:9050
echo.
echo View logs: docker-compose logs -f
echo Stop services: docker-compose down
echo.

pause
