# VAULT CLEANUP SCRIPT - 2026-02-19
# Suppression des doublons, redondances et nettoyage des caches

$vaultPath = "D:\Vault\Vault"
$logFile = "$vaultPath\CLEANUP_LOG_$(Get-Date -Format 'yyyy-MM-dd_HHmmss').txt"
$deletedItems = @()
$totalSpace = 0

function Log {
    param([string]$message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "$timestamp | $message" | Tee-Object -FilePath $logFile -Append
}

function RemoveItem {
    param([string]$path, [string]$reason)
    try {
        if (Test-Path $path) {
            $item = Get-Item $path
            $size = 0
            
            if ($item.PSIsContainer) {
                $size = (Get-ChildItem $path -Recurse | Measure-Object -Property Length -Sum).Sum
            } else {
                $size = $item.Length
            }
            
            Remove-Item $path -Recurse -Force -ErrorAction Stop
            $deletedItems += @{
                Path = $path
                Size = $size
                Reason = $reason
            }
            $script:totalSpace += $size
            Log "✓ DELETED: $path ($([math]::Round($size/1MB, 2)) MB) - $reason"
        }
    }
    catch {
        Log "✗ ERROR deleting $path : $_"
    }
}

Log "========== STARTING VAULT CLEANUP =========="
Log "Vault Path: $vaultPath"

# ==========================================
# ÉTAPE 1: SUPPRESSION DES DOUBLONS
# ==========================================
Log ""
Log "--- PHASE 1: Suppression des doublons ---"

# 1.1 Supprimer doublons Declassified/Cybersécurité (garder HACKERGPT)
Log ""
Log "1.1 Removing Declassified/Cybersécurité duplicates..."
RemoveItem "$vaultPath\Declassified\Cybersécurité\5 outils Hacking.md" "Doublon de HACKERGPT\"
RemoveItem "$vaultPath\Declassified\Cybersécurité\Documentation KALI TOR GHOST GUIDE.md.md" "Doublon de HACKERGPT (extension double)"
RemoveItem "$vaultPath\Declassified\Cybersécurité\MindMap.canvas" "Doublon de HACKERGPT"
RemoveItem "$vaultPath\Declassified\Cybersécurité\Operation Security.md" "Doublon de HACKERGPT"
RemoveItem "$vaultPath\Declassified\Cybersécurité\Scan.md" "Doublon de HACKERGPT"

# 1.2 Supprimer piecesdb.json doublons
Log ""
Log "1.2 Removing piecesdb.json duplicates..."
RemoveItem "$vaultPath\Notes et Mémos Importants\Notes rapide\piecesdb.json" "Doublon (root copy retained)"
RemoveItem "$vaultPath\Notes et Mémos Importants\Notes rapide\piecesdb 1.json" "Numbered duplicate"

# 1.3 Supprimer Clawdbot 1 (doublon)
Log ""
Log "1.3 Removing Clawdbot 1 folder..."
RemoveItem "$vaultPath\LLM's\Clawdbot 1" "Complete duplicate of Clawdbot folder"

# 1.4 Supprimer "The Thirty3.md" (garder "Th3 Thirty3.md" version optimisée)
Log ""
Log "1.4 Removing The Thirty3.md variant..."
RemoveItem "$vaultPath\Notes et Mémos Importants\Notes rapide\The Thirty3.md" "Keeping Th3 Thirty3.md (optimized naming)"

# 1.5 Supprimer Protection du consomateur duplicate
Log ""
Log "1.5 Removing Protection du consomateur from Classified Report..."
RemoveItem "$vaultPath\Classified Report\Protection du consomateur" "Duplicate (keeping in Notes et Mémos)"

# ==========================================
# ÉTAPE 2: ARCHIVAGE DES FICHIERS REDONDANTS
# ==========================================
Log ""
Log "--- PHASE 2: Archivage des redondances Ascended33 ---"

# Créer dossier d'archive
$archiveFolder = "$vaultPath\Ascended33\ARCHIVE_REDUNDANT_REPORTS"
if (-not (Test-Path $archiveFolder)) {
    New-Item -ItemType Directory -Path $archiveFolder -Force | Out-Null
    Log "Created archive folder: $archiveFolder"
}

# 2.1 Archiver les résumés redondants
Log ""
Log "2.1 Archiving redundant Ascended33 report files..."

$redundantFiles = @(
    "$vaultPath\Ascended33\JOUR_1_STATUS.txt",
    "$vaultPath\Ascended33\DAY_1_COMPLETION_REPORT.md",
    "$vaultPath\Ascended33\SESSION_2_SUMMARY.md",
    "$vaultPath\Ascended33\SESSION_3_CLOSURE_FINAL.md",
    "$vaultPath\Ascended33\JOUR2_COMPLETION_REPORT.md",
    "$vaultPath\Ascended33\JOUR2_VALIDATION_STATUS.md",
    "$vaultPath\Ascended33\TODAY_SUMMARY.txt",
    "$vaultPath\Ascended33\FINAL_DELIVERY_SUMMARY.txt"
)

foreach ($file in $redundantFiles) {
    if (Test-Path $file) {
        $filename = Split-Path $file -Leaf
        Move-Item $file "$archiveFolder\$filename" -Force -ErrorAction SilentlyContinue
        Log "✓ ARCHIVED: $filename"
    }
}

# ==========================================
# ÉTAPE 3: NETTOYAGE DES CACHES
# ==========================================
Log ""
Log "--- PHASE 3: Cleaning Python and Test caches ---"

# 3.1 Supprimer caches
Log ""
Log "3.1 Removing cache directories..."
RemoveItem "$vaultPath\.mypy_cache" "Python mypy cache"
RemoveItem "$vaultPath\.pytest_cache" "Python pytest cache"
RemoveItem "$vaultPath\Ascended33\__pycache__" "Python cache"
RemoveItem "$vaultPath\Ascended33\.pytest_cache" "Pytest cache"

# 3.2 Supprimer caches imbriqués
$pycacheDirs = Get-ChildItem -Path $vaultPath -Filter "__pycache__" -Recurse -Directory -ErrorAction SilentlyContinue
foreach ($dir in $pycacheDirs) {
    RemoveItem $dir.FullName "Nested __pycache__"
}

# ==========================================
# ÉTAPE 4: RÉORGANISATION STRUCTURELLE
# ==========================================
Log ""
Log "--- PHASE 4: Structural reorganization ---"

# 4.1 Créer nouvelle structure
Log ""
Log "4.1 Creating optimized folder structure..."

$newFolders = @(
    "$vaultPath\PROJECTS",
    "$vaultPath\PROJECTS\Ascended33",
    "$vaultPath\PROJECTS\Kali_Integration",
    "$vaultPath\PROJECTS\Pieces_OS_Integration",
    "$vaultPath\PROJECTS\Security_Audit"
)

foreach ($folder in $newFolders) {
    if (-not (Test-Path $folder)) {
        New-Item -ItemType Directory -Path $folder -Force | Out-Null
        Log "✓ Created: $folder"
    }
}

# 4.2 Fusionner les structures redondantes
Log ""
Log "4.2 Note: REPORT/Declassified Report should be consolidated with Declassified/"
Log "      Review required: Different data structures detected"

# ==========================================
# RÉSUMÉ FINAL
# ==========================================
Log ""
Log "========== CLEANUP COMPLETE =========="
Log ""
Log "Deleted Items Summary:"
Log "Total items removed: $($deletedItems.Count)"
Log "Total space freed: $([math]::Round($totalSpace/1MB, 2)) MB"
Log ""

foreach ($item in $deletedItems) {
    Log "  - $($item.Path) ($([math]::Round($item.Size/1MB, 2)) MB) [Reason: $($item.Reason)]"
}

Log ""
Log "Files successfully archived to: $archiveFolder"
Log ""
Log "Next steps:"
Log "1. Review REPORT structure for consolidation"
Log "2. Update Obsidian vault configuration"
Log "3. Run Obsidian re-index"
Log ""
Log "Log saved to: $logFile"

Write-Host ""
Write-Host "✓ CLEANUP COMPLETE!" -ForegroundColor Green
Write-Host "Space freed: $([math]::Round($totalSpace/1MB, 2)) MB" -ForegroundColor Cyan
Write-Host "Log file: $logFile" -ForegroundColor Yellow
