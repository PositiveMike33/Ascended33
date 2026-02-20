@echo off
cd D:\Vault\Vault\Ascended33
echo.
echo ====================================================================
echo JOUR 1 - VALIDATION DES TESTS
echo ====================================================================
echo.
echo Execution des tests Obsidian Sync Engine...
echo.
python -m pytest tests/test_obsidian_sync.py -v --tb=short
echo.
echo ====================================================================
if %ERRORLEVEL% EQU 0 (
    echo TEST RESULTS: TOUS LES TESTS PASSES
) else (
    echo TEST RESULTS: CERTAINS TESTS ONT ECHOUES
)
echo ====================================================================
echo.
pause
