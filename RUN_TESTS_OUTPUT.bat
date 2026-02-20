@echo off
REM Test runner with output capture for Ascended33 JOUR 1 validation

echo.
echo ================================================================================
echo JOUR 1 VALIDATION TEST SUITE - Ascended33 OSINT Platform
echo ================================================================================
echo.

cd /d D:\Vault\Vault\Ascended33

REM Install pytest if needed
echo Installing test dependencies...
C:\Users\th3th\AppData\Local\Programs\Python\Python313\python.exe -m pip install -q pytest pytest-cov watchdog pyyaml 2>nul

echo.
echo ================================================================================
echo Running validation tests...
echo ================================================================================
echo.

REM Run tests with output
C:\Users\th3th\AppData\Local\Programs\Python\Python313\python.exe -m pytest tests/test_obsidian_sync.py -v --tb=short

echo.
echo ================================================================================
echo Test execution complete
echo ================================================================================
pause
