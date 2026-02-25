# Organize Daily Reports Script
# Purpose: Move (YYYY-MM-DD) formatted files to destination folders with date-based subfolder creation
# Author: Claude Code
# Date: 2026-02-22

param(
    [string]$SourcePath = "D:/Vault/Vault/THIRTY3/daily",
    [string]$DestinationBasePath = "D:/Vault/Vault/REPORT/declassified report/02 Rapport Février/Semaine du 16 au 22 VACANCE",
    [switch]$DryRun = $false,
    [switch]$Verbose = $false
)

# ===== CONFIGURATION =====
# Week mapping for February 2026
$weekMapping = @{
    # Week: "Semaine du 16 au 22 VACANCE"
    16 = "16-02-2026"
    17 = "17-02-2026"
    18 = "18-02-2026"
    19 = "19-02-2026"
    20 = "20-02-2026"
    21 = "21-02-2026"
    22 = "22-02-2026"
}

$reportTypes = @("Bilan du jour", "Bilan du soir")
$datePattern = "^\(\d{4}-\d{2}-\d{2}\)"

# ===== FUNCTIONS =====

function Get-DateFromFilename {
    param([string]$Filename)
    
    if ($Filename -match $datePattern) {
        $dateStr = $Filename -replace "^\(|\)", ""
        try {
            $date = [DateTime]::ParseExact($dateStr, "yyyy-MM-dd", $null)
            return $date
        }
        catch {
            return $null
        }
    }
    return $null
}

function Get-DestinationFolder {
    param([DateTime]$Date)
    
    $day = $Date.Day
    $month = $Date.Month
    $year = $Date.Year
    
    if ($month -eq 2 -and $year -eq 2026 -and $weekMapping.ContainsKey($day)) {
        return $weekMapping[$day]
    }
    
    return $null
}

function Test-DuplicateFile {
    param(
        [string]$DestinationPath,
        [string]$Filename
    )
    
    $fullPath = Join-Path $DestinationPath $Filename
    return Test-Path $fullPath
}

function Get-UniqueFilename {
    param(
        [string]$DestinationPath,
        [string]$Filename
    )
    
    $counter = 1
    $baseName = [System.IO.Path]::GetFileNameWithoutExtension($Filename)
    $extension = [System.IO.Path]::GetExtension($Filename)
    
    while (Test-Path (Join-Path $DestinationPath "$baseName`_$counter$extension")) {
        $counter++
    }
    
    return "$baseName`_$counter$extension"
}

function Process-ReportFile {
    param(
        [string]$SourceFile,
        [string]$DestinationBasePath
    )
    
    $filename = Split-Path $SourceFile -Leaf
    $date = Get-DateFromFilename $filename
    
    if ($null -eq $date) {
        if ($Verbose) { Write-Host "SKIP: Invalid date format in $filename" -ForegroundColor Yellow }
        return @{ Status = "SKIPPED"; Reason = "Invalid date format"; File = $filename }
    }
    
    $destSubfolder = Get-DestinationFolder $date
    if ($null -eq $destSubfolder) {
        if ($Verbose) { Write-Host "SKIP: Date $($date.ToString('yyyy-MM-dd')) not in week mapping for $filename" -ForegroundColor Yellow }
        return @{ Status = "SKIPPED"; Reason = "Date not in week mapping"; File = $filename }
    }
    
    $destinationPath = Join-Path $DestinationBasePath $destSubfolder
    
    # Create destination folder if it doesn't exist
    if (-not (Test-Path $destinationPath)) {
        if ($Verbose) { Write-Host "CREATE: Folder $destinationPath" -ForegroundColor Green }
        if (-not $DryRun) {
            New-Item -ItemType Directory -Path $destinationPath -Force | Out-Null
        }
    }
    
    # Check for duplicates
    if (Test-DuplicateFile $destinationPath $filename) {
        $newFilename = Get-UniqueFilename $destinationPath $filename
        if ($Verbose) { Write-Host "RENAME: Duplicate detected. Renaming to $newFilename" -ForegroundColor Yellow }
        if (-not $DryRun) {
            Move-Item -Path $SourceFile -Destination (Join-Path $destinationPath $newFilename) -Force
        }
        return @{ Status = "MOVED_RENAMED"; OriginalFile = $filename; NewFile = $newFilename; Destination = $destSubfolder; Note = "DUPLICATE - MANUAL REVIEW NEEDED" }
    }
    else {
        if ($Verbose) { Write-Host "MOVE: $filename -> $destSubfolder" -ForegroundColor Green }
        if (-not $DryRun) {
            Move-Item -Path $SourceFile -Destination (Join-Path $destinationPath $filename) -Force
        }
        return @{ Status = "MOVED"; File = $filename; Destination = $destSubfolder }
    }
}

# ===== MAIN EXECUTION =====

Write-Host "====== Organize Daily Reports ======" -ForegroundColor Cyan
Write-Host "Source: $SourcePath"
Write-Host "Destination Base: $DestinationBasePath"
Write-Host "Mode: $(if ($DryRun) { 'DRY RUN' } else { 'EXECUTION' })"
Write-Host "======================================`n"

# Verify paths exist
if (-not (Test-Path $SourcePath)) {
    Write-Host "ERROR: Source path not found: $SourcePath" -ForegroundColor Red
    exit 1
}

if (-not (Test-Path $DestinationBasePath)) {
    Write-Host "ERROR: Destination base path not found: $DestinationBasePath" -ForegroundColor Red
    exit 1
}

# Find and process files
$results = @()
$sourceFiles = Get-ChildItem -Path $SourcePath -Filter "(????-??-??)*" -File

if ($sourceFiles.Count -eq 0) {
    Write-Host "INFO: No files matching pattern found in source path" -ForegroundColor Yellow
}
else {
    foreach ($file in $sourceFiles) {
        $result = Process-ReportFile -SourceFile $file.FullName -DestinationBasePath $DestinationBasePath
        $results += $result
    }
}

# Generate report
Write-Host "`n====== OPERATION REPORT ======" -ForegroundColor Cyan
Write-Host "Total files processed: $($results.Count)"
Write-Host "Moved: $($results | Where-Object { $_.Status -eq 'MOVED' } | Measure-Object).Count"
Write-Host "Moved and Renamed (Duplicates): $($results | Where-Object { $_.Status -eq 'MOVED_RENAMED' } | Measure-Object).Count"
Write-Host "Skipped: $($results | Where-Object { $_.Status -eq 'SKIPPED' } | Measure-Object).Count"

$duplicates = $results | Where-Object { $_.Status -eq 'MOVED_RENAMED' }
if ($duplicates.Count -gt 0) {
    Write-Host "`n*** ATTENTION: DUPLICATES DETECTED (Manual review needed) ***" -ForegroundColor Yellow
    foreach ($dup in $duplicates) {
        Write-Host "  • $($dup.OriginalFile) -> $($dup.NewFile) in $($dup.Destination)" -ForegroundColor Yellow
    }
}

Write-Host "====================================`n"

# Return results for logging
return $results
