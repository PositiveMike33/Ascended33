@echo off
REM ============================================================================
REM LAUNCH_HEXSTRIKE.bat — HexStrike Docker Integration Launcher
REM ============================================================================
REM
REM Launches HexStrike with full MCP server integration and 150+ red team tools
REM Purpose: Security research, penetration testing, OSINT investigations
REM
REM Status: HexStrike running on port 8001 (Docker)
REM         Streamlit UI: http://localhost:8501
REM         MCP Server: http://localhost:8001
REM
REM ============================================================================

setlocal enabledelayedexpansion

echo.
echo ╔════════════════════════════════════════════════════════════════════════╗
echo ║                     🔐 HEXSTRIKE LAUNCHER                              ║
echo ║            Cybersecurity Research Platform with Red Team Tools         ║
echo ╚════════════════════════════════════════════════════════════════════════╝
echo.

REM Check if Docker is installed
docker --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Docker not found. Please install Docker Desktop.
    echo    Download: https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)

echo ✅ Docker detected
echo.

REM Get the script directory
set SCRIPT_DIR=%~dp0
set VAULT_PATH=D:\Vault\Vault

echo 📁 Project Path: %SCRIPT_DIR%
echo 📁 Vault Path: %VAULT_PATH%
echo.

REM Check if docker-compose.yml exists
if not exist "%SCRIPT_DIR%docker-compose.yml" (
    echo ❌ docker-compose.yml not found in %SCRIPT_DIR%
    pause
    exit /b 1
)

echo ⏳ Checking Docker daemon...
docker ps >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Docker daemon is not running
    echo    Please start Docker Desktop
    pause
    exit /b 1
)

echo ✅ Docker daemon is running
echo.

echo ════════════════════════════════════════════════════════════════════════
echo 🚀 LAUNCHING HEXSTRIKE CONTAINERS
echo ════════════════════════════════════════════════════════════════════════
echo.

REM Start docker-compose
cd /d "%SCRIPT_DIR%"
docker-compose up -d

if %ERRORLEVEL% EQ 0 (
    echo.
    echo ✅ HexStrike containers started successfully!
    echo.
    echo ════════════════════════════════════════════════════════════════════════
    echo 📡 SERVICE ENDPOINTS
    echo ════════════════════════════════════════════════════════════════════════
    echo.
    echo 🌐 Streamlit UI:        http://localhost:8501
    echo 🔌 HexStrike API:       http://localhost:8001
    echo 🤖 HackerGPT:           http://localhost:8000
    echo 🧅 Tor Network:         localhost:9050 (SOCKS5)
    echo.
    echo ════════════════════════════════════════════════════════════════════════
    echo 📊 CONTAINER STATUS
    echo ════════════════════════════════════════════════════════════════════════
    echo.
    
    docker-compose ps
    
    echo.
    echo ════════════════════════════════════════════════════════════════════════
    echo 🛠️  AVAILABLE TOOLS (150+)
    echo ════════════════════════════════════════════════════════════════════════
    echo.
    echo Scanning:     nmap, masscan, nessus, nuclei, zaproxy, burpsuite, metasploit
    echo OSINT:        shodan, censys, maltego, spiderfoot, recon-ng, theHarvester
    echo Enumeration:  enum4linux, snmp-check, ldap-search, rpcinfo, docker-enum
    echo Cloud:        aws-enum, azure-enum, gcp-enum, s3-scanner, cloudtracker
    echo Injection:    sqlmap, wfuzz, paramspider, arjun, template-engine-fuzzer
    echo Crypto:       hashcat, john, jwt-cracker, ysoserial
    echo Post-Exploit: meterpreter, cobalt-strike payload gen, mimikatz
    echo Detection:    yara-scanner, clamscan, kubesec, docker-bench
    echo ...and 100+ more!
    echo.
    echo ════════════════════════════════════════════════════════════════════════
    echo ✨ QUICK COMMANDS
    echo ════════════════════════════════════════════════════════════════════════
    echo.
    echo  View logs:     docker-compose logs -f th3-hexstrike
    echo  Stop services: docker-compose down
    echo  Restart:       docker-compose restart th3-hexstrike
    echo.
    
    timeout /t 5 /nobreak
    
    REM Open Streamlit UI in browser
    echo 🌐 Opening HexStrike interface in browser...
    start http://localhost:8501
    
    echo.
    echo ✅ HexStrike is ready! Navigate to http://localhost:8501
    echo.
    echo 📝 Keep this window open. Press Ctrl+C to stop all services.
    echo.
    
    REM Keep window open for logs
    docker-compose logs -f th3-hexstrike
    
) else (
    echo.
    echo ❌ Failed to start HexStrike containers
    echo    Check Docker logs: docker-compose logs
    echo.
    pause
    exit /b 1
)

endlocal
