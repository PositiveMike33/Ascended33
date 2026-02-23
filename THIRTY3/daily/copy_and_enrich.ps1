# Define source and destination paths
$sourceDir = "D:\Vault\Vault\REPORT\Février"
$destDir = "D:\Vault\Vault\THIRTY3\daily"

# Get all markdown files from source
$mdFiles = Get-ChildItem -Path $sourceDir -Filter "*.md" -Recurse -File

# Counter for processing
$processedCount = 0
$copyErrorCount = 0

Write-Host "Found $($mdFiles.Count) markdown files to process" -ForegroundColor Green

foreach ($file in $mdFiles) {
    try {
        # Extract date from file path (format: DD-MM-YYYY or similar)
        $pathSegments = $file.DirectoryName -split '\\'
        $dateFolder = $null
        
        # Look for date folder (format: DD-MM-YYYY)
        foreach ($segment in $pathSegments) {
            if ($segment -match '^\d{2}-\d{2}-\d{4}$') {
                $dateFolder = $segment
                break
            }
        }
        
        if ($dateFolder) {
            # Parse the date
            $dateParts = $dateFolder -split '-'
            $day = $dateParts[0]
            $month = $dateParts[1]
            $year = $dateParts[2]
            
            # Create new filename
            $newFileName = "${year}-${month}-${day}_learning_progress.md"
            
            # Ensure destination directory exists
            $destMonthDir = "$destDir\$year\$month"
            if (-not (Test-Path $destMonthDir)) {
                New-Item -ItemType Directory -Force -Path $destMonthDir | Out-Null
            }
            
            # Read the original file
            $originalContent = Get-Content -Path $file.FullName -Raw -Encoding UTF8
            
            # Create YAML frontmatter based on content analysis
            $phase = 2  # Default to phase 2 based on learning progression
            
            # Infer tags from filename and content
            $tags = @("learning", "phase-2", "development")
            if ($file.Name -like "*OSINT*" -or $originalContent -like "*OSINT*") { $tags += "osint" }
            if ($file.Name -like "*CTF*" -or $originalContent -like "*CTF*") { $tags += "ctf" }
            if ($file.Name -like "*Docker*" -or $originalContent -like "*Docker*") { $tags += "docker" }
            if ($file.Name -like "*API*" -or $originalContent -like "*API*") { $tags += "api" }
            if ($file.Name -like "*Security*" -or $originalContent -like "*Security*") { $tags += "security" }
            
            $tagsString = "[" + ($tags | Select-Object -Unique | ForEach-Object { "`"$_`"" }) -join ", " + "]"
            
            # Create YAML frontmatter
            $yamlFrontmatter = @"
---
date: $year-$month-$day
type: learning-progress
phase: [$phase]
tags: $tagsString
status: active
source: REPORT/Février
---

"@
            
            # Combine frontmatter with original content
            $enrichedContent = $yamlFrontmatter + $originalContent
            
            # Write to destination
            $destPath = Join-Path $destMonthDir $newFileName
            Set-Content -Path $destPath -Value $enrichedContent -Encoding UTF8 -Force
            
            $processedCount++
            Write-Host "✓ $year-$month-$day" -ForegroundColor Green
        }
        else {
            Write-Host "⚠ Skipped (no date): $($file.Name)" -ForegroundColor Yellow
            $copyErrorCount++
        }
    }
    catch {
        Write-Host "✗ Error: $($file.Name) - $_" -ForegroundColor Red
        $copyErrorCount++
    }
}

Write-Host "`n=== SUMMARY ===" -ForegroundColor Cyan
Write-Host "✓ Processed: $processedCount" -ForegroundColor Green
Write-Host "⚠ Skipped: $copyErrorCount" -ForegroundColor Yellow
Write-Host "Total: $($mdFiles.Count)" -ForegroundColor White
