@echo off
REM =================================================
REM  HEXSTRIKE DOCKER VERIFICATION
REM =================================================

setlocal enabledelayedexpansion

echo.
echo =================================================
echo   HEXSTRIKE SERVICE VERIFICATION
echo =================================================
echo.

REM Check Docker daemon
echo [*] Checking Docker daemon...
docker ps >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Docker daemon not running
    exit /b 1
) else (
    echo [OK] Docker daemon running
)

REM Get current directory
cd /d "%~dp0"

echo.
echo [*] Checking Docker Compose configuration...
docker-compose config >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Invalid docker-compose.yml
    docker-compose config
    exit /b 1
) else (
    echo [OK] Configuration valid
)

echo.
echo =================================================
echo   SERVICE STATUS
echo =================================================
docker-compose ps

echo.
echo =================================================
echo   CONTAINER HEALTH
echo =================================================

REM Check Tor
echo.
echo [*] Tor (SOCKS5:9050)...
docker exec th3-tor nc -z localhost 9050 >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Tor is healthy
) else (
    echo [!] Tor is not responding
)

REM Check Kali
echo.
echo [*] Kali workspace...
docker exec th3-kali test -d /workspace >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Kali workspace ready
) else (
    echo [!] Kali workspace issue
)

REM Check HackerGPT
echo.
echo [*] HackerGPT API (8000)...
docker exec th3-hackergpt curl -s -f http://localhost:8000/health >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] HackerGPT API responding
) else (
    echo [!] HackerGPT API not responding
)

REM Check HexStrike
echo.
echo [*] HexStrike API (8001)...
docker exec th3-hexstrike curl -s -f http://localhost:8001/status >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] HexStrike API responding
) else (
    echo [!] HexStrike API not responding
)

echo.
echo =================================================
echo   ENDPOINT ACCESSIBILITY
echo =================================================
echo.
echo Streamlit Dashboard:
echo   http://localhost:8501
echo.
echo HackerGPT API:
echo   http://localhost:8000
echo.
echo HexStrike API:
echo   http://localhost:8001
echo.
echo Tor SOCKS5 Proxy:
echo   localhost:9050
echo.

echo [OK] Verification complete!
echo.

pause
