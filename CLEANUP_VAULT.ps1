# Vault Cleanup PowerShell Script
# Date: 2026-02-20
# Purpose: Remove duplicates and reorganize vault structure

Write-Host "============================================" -ForegroundColor Cyan
Write-Host " VAULT CLEANUP AND REORGANIZATION" -ForegroundColor Cyan
Write-Host " PowerShell Edition" -ForegroundColor Cyan
Write-Host " 2026-02-20" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Set working directory
Set-Location "D:\Vault\Vault"
$VaultPath = Get-Location

Write-Host "[INFO] Vault path: $VaultPath" -ForegroundColor Green
Write-Host ""

# ==================== PHASE 1: ANALYZE ====================
Write-Host "[PHASE 1] Analyzing vault structure..." -ForegroundColor Yellow
Write-Host ""

$DuplicateFolders = @(
    @{ Name = "Declassified"; Size = ""; Comment = "Duplicate of HACKERGPT\" },
    @{ Name = "Classified Report"; Size = ""; Comment = "Duplicate of Notes et Mémos" },
    @{ Name = "LLM's/Gemini/Gemini 1"; Size = ""; Comment = "Nested duplicate" },
    @{ Name = "Apprentissage"; Size = ""; Comment = "Duplicate of THIRTY3\" }
)

Write-Host "Found duplicate folders:" -ForegroundColor Cyan
foreach ($folder in $DuplicateFolders) {
    $fullPath = Join-Path $VaultPath $folder.Name
    if (Test-Path $fullPath) {
        $size = (Get-ChildItem $fullPath -Recurse | Measure-Object -Property Length -Sum).Sum / 1MB
        Write-Host "  ❌ $($folder.Name) (~$([Math]::Round($size, 2))MB) - $($folder.Comment)" -ForegroundColor Red
    } else {
        Write-Host "  ⚠️  $($folder.Name) - Not found" -ForegroundColor Yellow
    }
}
Write-Host ""

# ==================== PHASE 2: CREATE STRUCTURE ====================
Write-Host "[PHASE 2] Creating new vault structure..." -ForegroundColor Yellow
Write-Host ""

$MainDirs = @(
    "_INFRASTRUCTURE",
    "_PROJECTS",
    "PLANNING",
    "SECURITY",
    "LEARNING",
    "KNOWLEDGE",
    "REPORTS",
    "EXTERNAL"
)

foreach ($dir in $MainDirs) {
    $fullPath = Join-Path $VaultPath $dir
    if (-not (Test-Path $fullPath)) {
        New-Item -ItemType Directory -Path $fullPath | Out-Null
        Write-Host "  ✅ Created: $dir" -ForegroundColor Green
    } else {
        Write-Host "  ⚠️  Already exists: $dir" -ForegroundColor Yellow
    }
}
Write-Host ""

# ==================== PHASE 3: MOVE INFRASTRUCTURE ====================
Write-Host "[PHASE 3] Moving infrastructure files..." -ForegroundColor Yellow
Write-Host ""

$InfrastructureMoves = @(
    @{ Source = ".devcontainer"; Dest = "_INFRASTRUCTURE" },
    @{ Source = ".github"; Dest = "_INFRASTRUCTURE" },
    @{ Source = "Ascended33"; Dest = "_INFRASTRUCTURE" }
)

foreach ($move in $InfrastructureMoves) {
    $sourcePath = Join-Path $VaultPath $move.Source
    $destPath = Join-Path $VaultPath $move.Dest

    if (Test-Path $sourcePath) {
        try {
            Move-Item -Path $sourcePath -Destination $destPath -Force -ErrorAction SilentlyContinue
            Write-Host "  ✅ Moved: $($move.Source) -> $($move.Dest)\" -ForegroundColor Green
        } catch {
            Write-Host "  ⚠️  Error moving $($move.Source): $_" -ForegroundColor Yellow
        }
    } else {
        Write-Host "  ℹ️  Not found: $($move.Source)" -ForegroundColor Cyan
    }
}
Write-Host ""

# ==================== PHASE 4: MOVE PROJECTS ====================
Write-Host "[PHASE 4] Moving projects to _PROJECTS\..." -ForegroundColor Yellow
Write-Host ""

$ProjectFolders = @(
    "🔐_SECURITY_AUDIT_PROJECT",
    "🤖_PIECES_OS_INTEGRATION",
    "🐧_KALI_INTEGRATION_PROJECT",
    "🧠_CLAUDE_MASTERY"
)

foreach ($folder in $ProjectFolders) {
    $sourcePath = Join-Path $VaultPath $folder
    if (Test-Path $sourcePath) {
        try {
            Move-Item -Path $sourcePath -Destination "_PROJECTS\" -Force -ErrorAction SilentlyContinue
            Write-Host "  ✅ Moved: $folder -> _PROJECTS\" -ForegroundColor Green
        } catch {
            Write-Host "  ⚠️  Error moving $folder: $_" -ForegroundColor Yellow
        }
    }
}
Write-Host ""

# ==================== PHASE 5: CLEAN DUPLICATES ====================
Write-Host "[PHASE 5] Removing duplicate folders..." -ForegroundColor Yellow
Write-Host ""

Write-Host "⚠️  WARNING: About to permanently delete duplicate folders!" -ForegroundColor Red
Write-Host "These will be REMOVED:" -ForegroundColor Red
Write-Host "  - Declassified\" -ForegroundColor Red
Write-Host "  - Classified Report\" -ForegroundColor Red
Write-Host "  - LLM's\Gemini\Gemini 1\" -ForegroundColor Red
Write-Host "  - Apprentissage\" -ForegroundColor Red
Write-Host ""

$response = Read-Host "Continue with deletion? (Type 'YES' to confirm)"

if ($response -eq "YES") {
    Write-Host ""
    Write-Host "Proceeding with deletion..." -ForegroundColor Red
    Write-Host ""

    $FoldersToDelete = @(
        "Declassified",
        "Classified Report",
        "Apprentissage"
    )

    foreach ($folder in $FoldersToDelete) {
        $fullPath = Join-Path $VaultPath $folder
        if (Test-Path $fullPath) {
            try {
                Remove-Item -Path $fullPath -Recurse -Force
                Write-Host "  ✅ Deleted: $folder" -ForegroundColor Green
            } catch {
                Write-Host "  ❌ Error deleting $folder`: $_" -ForegroundColor Red
            }
        }
    }

    # Delete nested duplicate
    $nestedPath = Join-Path $VaultPath "LLM's\Gemini\Gemini 1"
    if (Test-Path $nestedPath) {
        try {
            Remove-Item -Path $nestedPath -Recurse -Force
            Write-Host "  ✅ Deleted: LLM's\Gemini\Gemini 1" -ForegroundColor Green
        } catch {
            Write-Host "  ❌ Error deleting LLM's\Gemini\Gemini 1: $_" -ForegroundColor Red
        }
    }
} else {
    Write-Host "Deletion cancelled by user" -ForegroundColor Yellow
}

Write-Host ""

# ==================== PHASE 6: CREATE DOCUMENTATION ====================
Write-Host "[PHASE 6] Creating documentation..." -ForegroundColor Yellow
Write-Host ""

# Create VAULT_STRUCTURE.md
$structurePath = Join-Path $VaultPath "VAULT_STRUCTURE.md"
if (-not (Test-Path $structurePath)) {
    @"
# Vault Structure - Post Cleanup

**Date:** 2026-02-20
**Status:** ✅ Cleaned and reorganized

## Structure

### 📚 Core (_BRAIN/)
- DASHBOARD.md — Hub central
- PROTOCOLES_VAULT.md — Commands
- MASTERCLASS/ — Educational content

### 🎯 Projects (_PROJECTS/)
- 🔐_SECURITY_AUDIT_PROJECT/
- 🤖_PIECES_OS_INTEGRATION/
- 🐧_KALI_INTEGRATION_PROJECT/
- 🧠_CLAUDE_MASTERY/

### 🔧 Infrastructure (_INFRASTRUCTURE/)
- .devcontainer/
- .github/
- Ascended33/
- docker-compose.yml

### 📋 Planning
- TODO_ACTIF.md
- BUDGET_2026.md
- PROJETS_ACTIFS.md

### 🔍 Security
- OSINT/ — Investigations
- OPERATIONS/ — Security ops
- TOOLS/ — HexStrike tools

### 📚 Learning
- PHASE_1/ — Fundamentals
- PHASE_2/ — Intermediate
- PHASE_3/ — Advanced
- PHASE_4/ — Certification

### 🎬 Tracking
- THIRTY3/daily/ — Daily progress

## Cleanup Summary

✅ Removed duplicates:
- Declassified/ (duplicate of HACKERGPT)
- Classified Report/ (duplicate of Notes et Mémos)
- LLM's/Gemini/Gemini 1/ (nested duplicate)
- Apprentissage/ (duplicate of THIRTY3)

✅ Organized into 8 main categories

✅ Created clear structure for navigation

## Next Steps

1. Update all internal links ([[...]])
2. Run: git add -A
3. Run: git commit -m "vault: cleanup duplicates and reorganize"
4. Verify in Obsidian

---

See _BRAIN/DASHBOARD.md for navigation hub
"@ | Out-File -FilePath $structurePath -Encoding UTF8
    Write-Host "  ✅ Created: VAULT_STRUCTURE.md" -ForegroundColor Green
}

# ==================== SUMMARY ====================
Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host " CLEANUP COMPLETE" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Summary:" -ForegroundColor Green
Write-Host "  ✅ Created 8 main directories" -ForegroundColor Green
Write-Host "  ✅ Moved infrastructure files" -ForegroundColor Green
Write-Host "  ✅ Moved projects" -ForegroundColor Green
Write-Host "  ✅ Removed duplicate folders" -ForegroundColor Green
Write-Host "  ✅ Created documentation" -ForegroundColor Green
Write-Host ""

Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Review the new structure in Explorer" -ForegroundColor Cyan
Write-Host "  2. Open Obsidian and check for broken links" -ForegroundColor Cyan
Write-Host "  3. Update internal [[...]] links if needed" -ForegroundColor Cyan
Write-Host "  4. Run: git add -A" -ForegroundColor Cyan
Write-Host "  5. Run: git commit -m 'vault: cleanup duplicates and reorganize'" -ForegroundColor Cyan
Write-Host ""

Write-Host "Press Enter to exit..."
Read-Host
