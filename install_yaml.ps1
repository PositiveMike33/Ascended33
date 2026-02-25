$pythonPath = "D:\Vault\Vault\.env\Scripts\python.exe"
$pipPath = "D:\Vault\Vault\.env\Scripts\pip.exe"

Write-Host "Installation de pyyaml..."
& $pipPath install pyyaml

Write-Host "Vérification..."
& $pythonPath -c "import yaml; print('✓ yaml installé avec succès')"

pause
