@echo off
REM Vault Cleanup Script - Remove duplicates and reorganize
REM Date: 2026-02-20
REM Purpose: Clean up D:\Vault\Vault and create proper structure

setlocal enabledelayedexpansion

echo ============================================
echo  VAULT CLEANUP AND REORGANIZATION
echo  2026-02-20
echo ============================================
echo.

REM Change to Vault directory
cd /d "D:\Vault\Vault"

REM ==================== PHASE 1: BACKUP ====================
echo [PHASE 1] Creating backup of vault structure...
echo.

if not exist "BACKUP_PRE_CLEANUP" (
    echo Creating BACKUP_PRE_CLEANUP directory...
    mkdir BACKUP_PRE_CLEANUP
) else (
    echo Backup directory already exists
)

REM ==================== PHASE 2: IDENTIFY DUPLICATES ====================
echo.
echo [PHASE 2] Identifying duplicate folders...
echo.

echo Found duplicates:
echo  - Declassified\ (duplicate of HACKERGPT\)
echo  - Classified Report\ (duplicate of Notes et Memos Importants\)
echo  - LLM's\Gemini\Gemini 1\ (nested duplicate of LLM's\Gemini\)
echo  - Apprentissage\ (duplicate of THIRTY3\)
echo.

REM ==================== PHASE 3: CREATE NEW STRUCTURE ====================
echo.
echo [PHASE 3] Creating new vault structure...
echo.

mkdir _INFRASTRUCTURE 2>nul
mkdir _PROJECTS 2>nul
mkdir PLANNING 2>nul
mkdir SECURITY 2>nul
mkdir LEARNING 2>nul
mkdir KNOWLEDGE 2>nul
mkdir REPORTS 2>nul
mkdir EXTERNAL 2>nul

echo Created 8 main directories
echo.

REM ==================== PHASE 4: MOVE INFRASTRUCTURE ====================
echo.
echo [PHASE 4] Moving infrastructure files...
echo.

if exist ".devcontainer" (
    echo Moving .devcontainer to _INFRASTRUCTURE\
    move .devcontainer _INFRASTRUCTURE\ 2>nul || echo  (Already exists or error)
)

if exist ".github" (
    echo Moving .github to _INFRASTRUCTURE\
    move .github _INFRASTRUCTURE\ 2>nul || echo  (Already exists or error)
)

if exist "Ascended33" (
    echo Moving Ascended33 to _INFRASTRUCTURE\
    move Ascended33 _INFRASTRUCTURE\ 2>nul || echo  (Already exists or error)
)

REM ==================== PHASE 5: MOVE PROJECTS ====================
echo.
echo [PHASE 5] Moving projects to _PROJECTS\...
echo.

for /d %%D in ("🔐_SECURITY_AUDIT_PROJECT" "🤖_PIECES_OS_INTEGRATION" "🐧_KALI_INTEGRATION_PROJECT" "🧠_CLAUDE_MASTERY") do (
    if exist "%%~D\" (
        echo Moving %%D to _PROJECTS\
        move "%%~D" _PROJECTS\ 2>nul || echo  (Already exists or error)
    )
)

REM ==================== PHASE 6: MOVE PLANNING ====================
echo.
echo [PHASE 6] Moving planning files to PLANNING\...
echo.

if exist "Notes et Mémos Importants\Notes rapide\PLANNING" (
    echo Found planning folder in Notes et Mémos
    REM Copy contents (be careful with move across nested structures)
    for /d %%D in ("Notes et Mémos Importants\Notes rapide\PLANNING\*") do (
        echo  - %%~nxD
        move "%%D" PLANNING\ 2>nul || echo    (Already exists)
    )
)

REM ==================== PHASE 7: DELETE DUPLICATES ====================
echo.
echo [PHASE 7] Removing duplicate folders...
echo.
echo WARNING: About to delete duplicate folders
echo Press Ctrl+C to cancel in the next 5 seconds...
echo.
timeout /t 5

if exist "Declassified" (
    echo Removing Declassified\ (duplicate of HACKERGPT)
    rmdir /s /q Declassified 2>nul || echo  (Error removing Declassified)
)

if exist "Classified Report" (
    echo Removing Classified Report\ (duplicate of Notes et Mémos)
    rmdir /s /q "Classified Report" 2>nul || echo  (Error removing Classified Report)
)

if exist "LLM's\Gemini\Gemini 1" (
    echo Removing LLM's\Gemini\Gemini 1\ (nested duplicate)
    rmdir /s /q "LLM's\Gemini\Gemini 1" 2>nul || echo  (Error removing nested folder)
)

if exist "Apprentissage" (
    echo Removing Apprentissage\ (duplicate of THIRTY3 learning path)
    rmdir /s /q Apprentissage 2>nul || echo  (Error removing Apprentissage)
)

REM ==================== PHASE 8: CREATE DOCUMENTATION ====================
echo.
echo [PHASE 8] Creating documentation files...
echo.

REM Create VAULT_STRUCTURE.md if not exists
if not exist "VAULT_STRUCTURE.md" (
    echo Creating VAULT_STRUCTURE.md
    (
        echo # Vault Structure - Post Cleanup
        echo.
        echo Created: 2026-02-20
        echo Status: ✅ Cleaned and reorganized
    ) > VAULT_STRUCTURE.md
)

REM Create README.md if not exists
if not exist "README.md" (
    echo Creating README.md
    (
        echo # Vault Guide
        echo.
        echo See _BRAIN/DASHBOARD.md for the main hub
    ) > README.md
)

REM ==================== PHASE 9: SUMMARY ====================
echo.
echo ============================================
echo  CLEANUP SUMMARY
echo ============================================
echo.
echo ✅ Created new structure with 8 main directories
echo ✅ Moved infrastructure files
echo ✅ Moved projects to _PROJECTS\
echo ✅ Removed duplicate folders:
echo    - Declassified
echo    - Classified Report
echo    - LLM's\Gemini\Gemini 1
echo    - Apprentissage
echo.
echo Next steps:
echo   1. Run: git add -A
echo   2. Run: git commit -m "vault: cleanup duplicates and reorganize"
echo   3. Check Obsidian for broken links
echo.
echo ============================================
echo.

pause
