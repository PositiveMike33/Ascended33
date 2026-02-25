# Test Script - Simplified Version
$SourcePath = "D:/Vault/Vault/THIRTY3/daily"
$DestinationBasePath = "D:/Vault/Vault/REPORT/declassified report/02 Rapport Février/Semaine du 16 au 22 VACANCE"

Write-Host "====== TEST: Organize Daily Reports ======" -ForegroundColor Cyan
Write-Host "Source: $SourcePath"
Write-Host "Destination: $DestinationBasePath"
Write-Host "==========================================`n"

# Check source path
if (-not (Test-Path $SourcePath)) {
    Write-Host "ERROR: Source path not found!" -ForegroundColor Red
    exit 1
}

Write-Host "✓ Source path exists" -ForegroundColor Green

# Find files matching pattern
$files = Get-ChildItem -Path $SourcePath -Filter "(????-??-??)*" -File

Write-Host "Found $($files.Count) files matching pattern:`n"
foreach ($file in $files) {
    Write-Host "  - $($file.Name)" -ForegroundColor Yellow
}

# Check destination
if (-not (Test-Path $DestinationBasePath)) {
    Write-Host "`n❌ Destination path does not exist!" -ForegroundColor Red
    Write-Host "Path: $DestinationBasePath" -ForegroundColor Red
}
else {
    Write-Host "`n✓ Destination path exists" -ForegroundColor Green
    Write-Host "Sub-directories:" -ForegroundColor Cyan
    $subdirs = Get-ChildItem -Path $DestinationBasePath -Directory
    foreach ($dir in $subdirs) {
        Write-Host "  - $($dir.Name)" -ForegroundColor Green
    }
}

Write-Host "`n==========================================`n"
