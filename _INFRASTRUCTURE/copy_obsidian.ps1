$source = "C:\Users\th3th\OneDrive\Documents\Obsidian Vault"
$destination = "D:\Vault\Vault\EXTERNAL\External Vault"

Write-Host "Source: $source"
Write-Host "Destination: $destination"
Write-Host ""

# Vérifier que la source existe
if (Test-Path $source) {
    Write-Host "✓ Source trouvée"
} else {
    Write-Host "✗ Source non trouvée"
    exit 1
}

# Copier le contenu
Write-Host "Copie en cours..."
Copy-Item -Path "$source\*" -Destination $destination -Recurse -Force

# Vérifier le résultat
$files = @(Get-ChildItem -Path $destination -Recurse)
$totalSize = ($files | Measure-Object -Property Length -Sum).Sum

Write-Host ""
Write-Host "✓ Copie terminée"
Write-Host "Fichiers copiés: $($files.Count)"
Write-Host "Taille totale: $('{0:F2}' -f ($totalSize / 1MB)) MB"
