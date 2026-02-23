# Batch copy and enrich daily notes
$sourceDir = "D:\Vault\Vault\REPORT\Février"
$destDir = "D:\Vault\Vault\THIRTY3\daily"
$processedCount = 0

$mdFiles = Get-ChildItem -Path $sourceDir -Filter "*.md" -Recurse -File

foreach ($file in $mdFiles) {
    $pathSegments = $file.DirectoryName -split '\\'
    $dateFolder = $null
    
    foreach ($segment in $pathSegments) {
        if ($segment -match '^\d{2}-\d{2}-\d{4}$') {
            $dateFolder = $segment
            break
        }
    }
    
    if ($dateFolder) {
        $dateParts = $dateFolder -split '-'
        $day = $dateParts[0]
        $month = $dateParts[1]
        $year = $dateParts[2]
        
        $newFileName = "${year}-${month}-${day}_learning_progress.md"
        $destMonthDir = "$destDir\$year\$month"
        
        if (-not (Test-Path $destMonthDir)) {
            New-Item -ItemType Directory -Force -Path $destMonthDir | Out-Null
        }
        
        $originalContent = Get-Content -Path $file.FullName -Raw -Encoding UTF8
        
        $yamlFrontmatter = @"
---
date: $year-$month-$day
type: learning-progress
phase: [2]
tags: [learning, phase-2, development, security]
status: active
source: REPORT/Février
---

"@
        
        $enrichedContent = $yamlFrontmatter + $originalContent
        $destPath = Join-Path $destMonthDir $newFileName
        Set-Content -Path $destPath -Value $enrichedContent -Encoding UTF8 -Force
        
        $processedCount++
    }
}

Write-Output "Processed: $processedCount files"
