@echo off
REM ============================================================================
REM HexStrike Ascended33 - TEST SUITE LAUNCHER
REM Multiplatform test orchestration for Docker infrastructure
REM ============================================================================

setlocal enabledelayedexpansion

REM Configuration
set SCRIPT_DIR=%~dp0
set PROJECT_ROOT=%SCRIPT_DIR:~0,-1%
set PROJECT_ROOT=%PROJECT_ROOT:~0,-15%
set PYTHON_SCRIPT=%SCRIPT_DIR%test_orchestrator.py
set PS_SCRIPT=%SCRIPT_DIR%TEST_SUITE_WINDOWS.ps1

REM Colors (via ANSI escape codes)
set ESC=[
set GREEN=%ESC%32m
set RED=%ESC%31m
set YELLOW=%ESC%33m
set CYAN=%ESC%36m
set MAGENTA=%ESC%35m
set RESET=%ESC%0m

REM ============================================================================
REM BANNER
REM ============================================================================

cls
echo.
echo %MAGENTA%╔════════════════════════════════════════════════════════════╗%RESET%
echo %MAGENTA%║       HexStrike Ascended33 - TEST SUITE LAUNCHER          ║%RESET%
echo %MAGENTA%╚════════════════════════════════════════════════════════════╝%RESET%
echo.

REM ============================================================================
REM CHECK PREREQUISITES
REM ============================================================================

echo %CYAN%[CHECKING PREREQUISITES]%RESET%

REM Check Docker
where docker >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo %RED%✗ Docker not found in PATH%RESET%
    echo.
    echo Please install Docker Desktop from: https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)
echo %GREEN%✓ Docker found%RESET%

REM Check Python (optional but recommended)
where python >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    set HAS_PYTHON=1
    echo %GREEN%✓ Python found%RESET%
) else (
    set HAS_PYTHON=0
    echo %YELLOW%⚠ Python not found (using PowerShell instead)%RESET%
)

REM Check Docker Compose
docker-compose --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo %RED%✗ Docker Compose not found%RESET%
    echo.
    echo Please update Docker Desktop or install Docker Compose
    pause
    exit /b 1
)
echo %GREEN%✓ Docker Compose found%RESET%

echo.

REM ============================================================================
REM MENU
REM ============================================================================

:MENU
echo %MAGENTA%Select test execution method:%RESET%
echo.
if %HAS_PYTHON% EQU 1 (
    echo  [1] %CYAN%Python%RESET% - Full featured (recommended)
    echo  [2] PowerShell - Windows native
) else (
    echo  [1] PowerShell - Windows native
)
echo  [3] Docker PS - Quick container check
echo  [4] Docker Logs - View service logs
echo  [5] System Cleanup - Clean Docker resources
echo  [6] Exit
echo.
set /p CHOICE="Choose option (1-6): "

REM ============================================================================
REM EXECUTE
REM ============================================================================

if "%CHOICE%"=="1" goto OPTION1
if "%CHOICE%"=="2" goto OPTION2
if "%CHOICE%"=="3" goto OPTION3
if "%CHOICE%"=="4" goto OPTION4
if "%CHOICE%"=="5" goto OPTION5
if "%CHOICE%"=="6" goto EXIT_SCRIPT

echo %RED%Invalid choice%RESET%
echo.
goto MENU

:OPTION1
if %HAS_PYTHON% EQU 0 (
    goto OPTION2
)
echo.
echo %CYAN%[RUNNING PYTHON TEST SUITE]%RESET%
echo.
python "%PYTHON_SCRIPT%"
goto MENU

:OPTION2
echo.
echo %CYAN%[RUNNING POWERSHELL TEST SUITE]%RESET%
echo.
powershell -ExecutionPolicy Bypass -File "%PS_SCRIPT%"
goto MENU

:OPTION3
echo.
echo %CYAN%[DOCKER CONTAINER STATUS]%RESET%
echo.
docker ps -a --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
echo.
pause
goto MENU

:OPTION4
echo.
echo %CYAN%[SELECT CONTAINER FOR LOGS]%RESET%
echo.
echo  [1] th3-hexstrike
echo  [2] th3-tor
echo  [3] th3-kali
echo  [4] th3-hackergpt
echo  [5] th3-streamlit
echo  [6] All (recent 20 lines each)
echo.
set /p LOG_CHOICE="Choose container (1-6): "

if "%LOG_CHOICE%"=="1" (
    docker logs --tail=50 th3-hexstrike
) else if "%LOG_CHOICE%"=="2" (
    docker logs --tail=50 th3-tor
) else if "%LOG_CHOICE%"=="3" (
    docker logs --tail=50 th3-kali
) else if "%LOG_CHOICE%"=="4" (
    docker logs --tail=50 th3-hackergpt
) else if "%LOG_CHOICE%"=="5" (
    docker logs --tail=50 th3-streamlit
) else if "%LOG_CHOICE%"=="6" (
    for %%C in (th3-hexstrike th3-tor th3-kali th3-hackergpt th3-streamlit) do (
        echo.
        echo %CYAN%--- Logs for %%C ---%RESET%
        docker logs --tail=20 %%C 2>&1 || echo (No logs available)
    )
) else (
    echo %RED%Invalid choice%RESET%
)
echo.
pause
goto MENU

:OPTION5
echo.
echo %YELLOW%[CLEANUP OPTIONS]%RESET%
echo.
echo  [1] Remove stopped containers
echo  [2] Remove dangling images
echo  [3] Remove unused volumes
echo  [4] Full cleanup (containers, images, volumes)
echo  [5] Back to menu
echo.
set /p CLEANUP_CHOICE="Choose option (1-5): "

if "%CLEANUP_CHOICE%"=="1" (
    echo %CYAN%Removing stopped containers...%RESET%
    docker container prune -f
) else if "%CLEANUP_CHOICE%"=="2" (
    echo %CYAN%Removing dangling images...%RESET%
    docker image prune -f
) else if "%CLEANUP_CHOICE%"=="3" (
    echo %CYAN%Removing unused volumes...%RESET%
    docker volume prune -f
) else if "%CLEANUP_CHOICE%"=="4" (
    echo %RED%WARNING: This will remove all Docker resources not in use!%RESET%
    set /p CONFIRM="Continue? (y/N): "
    if /i "!CONFIRM!"=="y" (
        echo %CYAN%Running full cleanup...%RESET%
        docker system prune -a --volumes -f
        echo %GREEN%Cleanup complete%RESET%
    ) else (
        echo %YELLOW%Cleanup cancelled%RESET%
    )
) else if "%CLEANUP_CHOICE%"=="5" (
    goto MENU
) else (
    echo %RED%Invalid choice%RESET%
)

echo.
pause
goto MENU

:EXIT_SCRIPT
echo.
echo %GREEN%Goodbye!%RESET%
echo.
exit /b 0
