@echo off
REM Build Docker images in background
cd /d "%~dp0"

echo [*] Building Docker images...
echo [*] This will take 10-20 minutes
echo [*] You can safely close this window
echo.

docker-compose build --no-cache

if %errorlevel% equ 0 (
    echo.
    echo [OK] Build complete!
    docker-compose ps
) else (
    echo.
    echo [!] Build failed with error %errorlevel%
)

pause
