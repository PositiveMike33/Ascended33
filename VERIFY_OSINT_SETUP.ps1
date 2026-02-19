#!/usr/bin/env powershell
<#
.SYNOPSIS
    Vérification pré-lancement - Infrastructure OSINT Légale
.DESCRIPTION
    Vérifie que tous les composants sont correctement installés
    avant le lancement de la session d'investigation.
.NOTES
    Exécuter: powershell -ExecutionPolicy Bypass -File "VERIFY_OSINT_SETUP.ps1"
#>

param(
    [switch]$Verbose = $false
)

$ErrorActionPreference = "Continue"
$ProgressPreference = "SilentlyContinue"

function Write-Status {
    param(
        [string]$Component,
        [bool]$Status,
        [string]$Message
    )
    
    if ($Status) {
        Write-Host "✅ $Component" -ForegroundColor Green
    } else {
        Write-Host "❌ $Component" -ForegroundColor Red
    }
    
    if ($Message) {
        Write-Host "   $Message" -ForegroundColor Gray
    }
}

function Write-Header {
    param([string]$Title)
    Write-Host ""
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
    Write-Host "  $Title" -ForegroundColor Cyan
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
}

function Check-Docker {
    Write-Header "1. VÉRIFICATION DOCKER"
    
    try {
        $version = docker --version
        Write-Status "Docker installé" $true "Version: $version"
        
        $daemon = docker ps -q
        Write-Status "Daemon Docker actif" $true
        return $true
    } catch {
        Write-Status "Docker NOT FOUND" $false "À installer: https://docker.com"
        return $false
    }
}

function Check-DockerCompose {
    Write-Header "2. VÉRIFICATION DOCKER COMPOSE"
    
    try {
        $version = docker-compose --version
        Write-Status "Docker Compose installé" $true "Version: $version"
        return $true
    } catch {
        Write-Status "Docker Compose NOT FOUND" $false "Installez via: docker app plugin install compose"
        return $false
    }
}

function Check-Files {
    Write-Header "3. VÉRIFICATION FICHIERS"
    
    $requiredFiles = @(
        "docker-compose-osint.yml",
        "osint_legal_engine.py",
        "legal_report_generator.py",
        "docker_orchestrator_osint.py",
        "OSINT_LEGAL_GUIDE.md",
        "OSINT_INTEGRATION_SUMMARY.md"
    )
    
    $allPresent = $true
    foreach ($file in $requiredFiles) {
        $exists = Test-Path $file
        Write-Status "Fichier: $file" $exists
        if (-not $exists) { $allPresent = $false }
    }
    
    return $allPresent
}

function Check-Python {
    Write-Header "4. VÉRIFICATION PYTHON"
    
    try {
        $version = python --version 2>&1
        Write-Status "Python installé" $true "Version: $version"
        
        # Vérifier version >= 3.9
        $major = [int]($version -split "Python ")[1] -split "\." | Select-Object -First 1
        $minor = [int]($version -split "\." | Select-Object -Index 1)
        
        if ($major -eq 3 -and $minor -ge 9) {
            Write-Status "Python 3.9+" $true
            return $true
        } else {
            Write-Status "Python version insuffisante" $false "Requis: 3.9+, Installé: $version"
            return $false
        }
    } catch {
        Write-Status "Python NOT FOUND" $false "À installer: https://python.org"
        return $false
    }
}

function Check-PythonPackages {
    Write-Header "5. VÉRIFICATION PACKAGES PYTHON"
    
    $packages = @(
        "cryptography",
        "docker",
        "requests",
        "pathlib"
    )
    
    $allInstalled = $true
    foreach ($package in $packages) {
        try {
            $out = python -c "import $package" 2>&1
            Write-Status "Package: $package" $true
        } catch {
            Write-Status "Package: $package" $false "À installer: pip install $package"
            $allInstalled = $false
        }
    }
    
    return $allInstalled
}

function Check-Directories {
    Write-Header "6. VÉRIFICATION RÉPERTOIRES"
    
    $requiredDirs = @(
        "config",
        "scripts",
        "osint_reports",
        "output"
    )
    
    $allPresent = $true
    foreach ($dir in $requiredDirs) {
        $exists = Test-Path $dir -PathType Container
        
        if (-not $exists) {
            New-Item -ItemType Directory -Path $dir -Force > $null
            Write-Status "Répertoire créé: $dir" $true
        } else {
            Write-Status "Répertoire: $dir" $true
        }
    }
    
    return $allPresent
}

function Check-DiskSpace {
    Write-Header "7. VÉRIFICATION ESPACE DISQUE"
    
    try {
        $drive = (Get-Location).Drive.Name
        $disk = Get-Volume -DriveLetter $drive
        $freeGB = [math]::Round($disk.SizeRemaining / 1GB, 2)
        
        $hasSoace = $disk.SizeRemaining -gt 5GB
        
        Write-Status "Espace disque" $hasSpace "$freeGB GB libre (Requis: 5GB+)"
        return $hasSpace
    } catch {
        Write-Status "Vérification espace" $false "Vérification manuelle: dir c:"
        return $true
    }
}

function Check-Memory {
    Write-Header "8. VÉRIFICATION MÉMOIRE"
    
    try {
        $mem = Get-WmiObject Win32_ComputerSystem
        $totalMemory = [math]::Round($mem.TotalPhysicalMemory / 1GB, 2)
        $availableMemory = [math]::Round((Get-WmiObject Win32_OperatingSystem).FreePhysicalMemory / 1MB, 2)
        
        $sufficient = $totalMemory -ge 4
        
        Write-Status "RAM" $sufficient "Total: $totalMemory GB, Libre: $availableMemory MB"
        return $sufficient
    } catch {
        Write-Status "Vérification RAM" $false "Vérification manuelle requise"
        return $true
    }
}

function Check-Network {
    Write-Header "9. VÉRIFICATION RÉSEAU"
    
    try {
        $dns = Resolve-DnsName -Name 8.8.8.8 -ErrorAction Stop
        Write-Status "Connectivité réseau" $true
        
        # Vérifier port 9050 disponible
        $socket = New-Object System.Net.Sockets.TcpClient
        try {
            $socket.Connect("localhost", 9050)
            Write-Status "Port Tor (9050)" $false "Déjà utilisé (normal si Tor lancé)"
            $socket.Close()
        } catch {
            Write-Status "Port Tor (9050)" $true "Disponible"
        }
        
        return $true
    } catch {
        Write-Status "Réseau" $false "Pas de connexion internet"
        return $false
    }
}

function Check-DockerImage {
    Write-Header "10. VÉRIFICATION IMAGES DOCKER"
    
    Write-Host ""
    Write-Host "⚠️  Images Docker nécessaires:" -ForegroundColor Yellow
    Write-Host "  - kalilinux/kali-rolling" -ForegroundColor Gray
    Write-Host "  - custom/hackergpt:latest (à build)" -ForegroundColor Gray
    Write-Host "  - custom/hexstrike:latest (à build)" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Commandes de pull:" -ForegroundColor Yellow
    Write-Host "  docker pull kalilinux/kali-rolling" -ForegroundColor Gray
    Write-Host ""
    
    $hasKali = docker images | Select-String "kalilinux"
    if ($hasKali) {
        Write-Status "Image Kali" $true
    } else {
        Write-Status "Image Kali" $false "À télécharger: docker pull kalilinux/kali-rolling"
    }
    
    return $hasKali
}

function Check-Keys {
    Write-Header "11. VÉRIFICATION CLÉS CRYPTOGRAPHIQUES"
    
    $privateKey = Test-Path "osint_private.pem"
    $publicKey = Test-Path "osint_public.pem"
    
    if (-not $privateKey) {
        Write-Host "ℹ️  Clés cryptographiques seront générées au premier lancement" -ForegroundColor Cyan
    } else {
        Write-Status "Clé privée (PROTÉGER!)" $privateKey
        Write-Status "Clé publique" $publicKey
    }
    
    return $true
}

function Show-Summary {
    Write-Header "RÉSUMÉ DE VÉRIFICATION"
    
    Write-Host ""
    Write-Host "✅ = Composant prêt" -ForegroundColor Green
    Write-Host "❌ = Composant manquant" -ForegroundColor Red
    Write-Host "⚠️  = Action recommandée" -ForegroundColor Yellow
    Write-Host ""
    
    Write-Host "Prochaines étapes:" -ForegroundColor Cyan
    Write-Host "  1. Corriger les ❌ en rouge ci-dessus" -ForegroundColor Gray
    Write-Host "  2. python docker_orchestrator_osint.py" -ForegroundColor Gray
    Write-Host "  3. Attendre ~40 secondes pour démarrage" -ForegroundColor Gray
    Write-Host "  4. Accéder: http://localhost:8001 (Hexstrike)" -ForegroundColor Gray
    Write-Host ""
}

# ====== EXÉCUTION PRINCIPALE ======
Write-Host ""
Write-Host "🕵️  VÉRIFICATION INFRASTRUCTURE OSINT LÉGALE" -ForegroundColor Cyan
Write-Host "Anonymité Opérationnelle + Auditabilité Légale" -ForegroundColor Cyan
Write-Host ""

# Collecte résultats
$results = @()

$results += @{ name = "Docker"; passed = Check-Docker }
$results += @{ name = "Docker Compose"; passed = Check-DockerCompose }
$results += @{ name = "Fichiers"; passed = Check-Files }
$results += @{ name = "Python"; passed = Check-Python }
$results += @{ name = "Packages Python"; passed = Check-PythonPackages }
$results += @{ name = "Répertoires"; passed = Check-Directories }
$results += @{ name = "Espace Disque"; passed = Check-DiskSpace }
$results += @{ name = "Mémoire"; passed = Check-Memory }
$results += @{ name = "Réseau"; passed = Check-Network }
$results += @{ name = "Images Docker"; passed = Check-DockerImage }
$results += @{ name = "Clés Crypto"; passed = Check-Keys }

# Affiche résumé
Show-Summary

# Compte résultats
$passed = ($results | Where-Object { $_.passed }).Count
$total = $results.Count

Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "Résultats: $passed/$total composants prêts" -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host ""

# Recommandations finales
if ($passed -eq $total) {
    Write-Host "✅ SYSTÈME PRÊT POUR OPÉRATIONS OSINT!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Commande de lancement:" -ForegroundColor Cyan
    Write-Host "  python docker_orchestrator_osint.py" -ForegroundColor Yellow
    Write-Host ""
} else {
    Write-Host "⚠️  Merci de corriger les $($total - $passed) élément(s) manquant(s) avant lancement" -ForegroundColor Yellow
    Write-Host ""
}

# Pause
if ($Verbose) {
    Read-Host "Appuyez sur Entrée pour fermer"
}
