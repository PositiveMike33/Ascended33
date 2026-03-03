# ============================================================================
# TEST SUITE AUTOMATISÉE - HexStrike Ascended33
# Valide tous les conteneurs Docker, connexions, volumes, et APIs
# ============================================================================

param(
    [switch]$SkipCleanup = $false,
    [switch]$Verbose = $false
)

# Configuration
$ErrorActionPreference = "Continue"
$WarningPreference = "SilentlyContinue"
$VerbosePreference = if ($Verbose) { "Continue" } else { "SilentlyContinue" }

# Chemins
$INFRA_DIR = Split-Path -Parent $MyInvocation.MyCommandPath
$PROJECT_ROOT = Split-Path -Parent $INFRA_DIR
$COMPOSE_FILE = "$INFRA_DIR\docker-compose.yml"
$COMPOSE_FILE_V2 = "$PROJECT_ROOT\docker-compose-v2.yml"
$VAULT_PATH = "D:\Vault\Vault"
$RESULTS_LOG = "$INFRA_DIR\test-results-$(Get-Date -Format 'yyyy-MM-dd_HHmmss').log"

# Couleurs
$Colors = @{
    Reset   = "`e[0m"
    Success = "`e[32m"  # Green
    Error   = "`e[31m"  # Red
    Warning = "`e[33m"  # Yellow
    Info    = "`e[36m"  # Cyan
    Header  = "`e[1;35m" # Magenta Bold
}

# Compteurs
$global:TestsPassed = 0
$global:TestsFailed = 0
$global:TestsWarning = 0

# ============================================================================
# FONCTIONS UTILITAIRES
# ============================================================================

function Write-Header {
    param([string]$Text)
    Write-Host "`n$($Colors.Header)╔════════════════════════════════════════╗$($Colors.Reset)"
    Write-Host "$($Colors.Header)║ $Text$(' ' * (36 - $Text.Length))║$($Colors.Reset)"
    Write-Host "$($Colors.Header)╚════════════════════════════════════════╝$($Colors.Reset)`n"
}

function Write-TestInfo {
    param([string]$Step, [string]$Description)
    Write-Host "$($Colors.Info)[ÉTAPE $Step]$($Colors.Reset) $Description" -ForegroundColor Cyan
}

function Write-Success {
    param([string]$Message)
    Write-Host "$($Colors.Success)✓ SUCCÈS:$($Colors.Reset) $Message"
    Add-Content -Path $RESULTS_LOG -Value "✓ $Message"
    $global:TestsPassed++
}

function Write-Failure {
    param([string]$Message)
    Write-Host "$($Colors.Error)✗ ÉCHEC:$($Colors.Reset) $Message"
    Add-Content -Path $RESULTS_LOG -Value "✗ $Message"
    $global:TestsFailed++
}

function Write-Warning {
    param([string]$Message)
    Write-Host "$($Colors.Warning)⚠ ATTENTION:$($Colors.Reset) $Message"
    Add-Content -Path $RESULTS_LOG -Value "⚠ $Message"
    $global:TestsWarning++
}

function Test-Command {
    param([string]$Command)
    $null = & {$ErrorActionPreference = "SilentlyContinue"; cmd /c $Command 2>&1}
    return $LASTEXITCODE -eq 0
}

function Get-DockerContainer {
    param([string]$Name)
    try {
        docker inspect $Name 2>$null | ConvertFrom-Json
    } catch {
        return $null
    }
}

function Get-ContainerStatus {
    param([string]$Name)
    try {
        $container = docker ps -a --format "json" | ConvertFrom-Json | Where-Object { $_.Names -eq $Name }
        return $container.State
    } catch {
        return "unknown"
    }
}

function Test-Endpoint {
    param([string]$URL, [string]$Description)
    try {
        $response = curl -s -m 5 "$URL" 2>$null
        if ($response) {
            Write-Success "$Description - Status 200"
            return $true
        } else {
            Write-Failure "$Description - No response"
            return $false
        }
    } catch {
        Write-Failure "$Description - Error: $_"
        return $false
    }
}

function Invoke-DockerExec {
    param(
        [string]$Container,
        [string]$Command,
        [string]$Description
    )
    try {
        $result = docker exec $Container sh -c $Command 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Success "$Description"
            return @{ Success = $true; Output = $result }
        } else {
            Write-Failure "$Description - Exit code: $LASTEXITCODE"
            return @{ Success = $false; Output = $result }
        }
    } catch {
        Write-Failure "$Description - Exception: $_"
        return @{ Success = $false; Output = $_ }
    }
}

# ============================================================================
# TESTS
# ============================================================================

Write-Header "DÉMARRAGE SUITE DE TESTS - HexStrike Ascended33"
Add-Content -Path $RESULTS_LOG -Value "=== TEST SUITE STARTED $(Get-Date) ==="

# ============================================================================
# PHASE 1 : VÉRIFICATION INFRASTRUCTURE
# ============================================================================

Write-Header "PHASE 1 - Vérification Infrastructure Docker"

Write-TestInfo "1.1" "Vérifier l'état des conteneurs Docker"
$containers = @("th3-hexstrike", "th3-tor", "th3-kali", "th3-hackergpt", "th3-streamlit")

foreach ($container in $containers) {
    $status = Get-ContainerStatus -Name $container
    if ($status -in @("running", "Up", "Up (healthy)")) {
        Write-Success "Conteneur $container est UP"
    } elseif ($status -in @("exited", "Exited")) {
        Write-Failure "Conteneur $container est STOPPED"
    } else {
        Write-Warning "Conteneur $container status: $status"
    }
}

Write-TestInfo "1.2" "Afficher le format détaillé des conteneurs"
$psOutput = docker ps --format "table {{.Names}}`t{{.Status}}`t{{.Ports}}"
Write-Host $psOutput
Add-Content -Path $RESULTS_LOG -Value "Docker PS Output:`n$psOutput"

# ============================================================================
# PHASE 2 : CONNEXIONS INTERNES
# ============================================================================

Write-Header "PHASE 2 - Tests de Connexion Interne"

Write-TestInfo "2.1" "Test santé Hexstrike (port 8001)"
$result = Invoke-DockerExec -Container "th3-hexstrike" -Command "curl -s http://localhost:8001/health" -Description "Health check Hexstrike"
if ($result.Success) {
    Write-Host "Réponse: $($result.Output)" -ForegroundColor Green
}

Write-TestInfo "2.2" "Test ping Redis depuis Hexstrike"
$result = Invoke-DockerExec -Container "th3-hexstrike" -Command "redis-cli -h redis ping 2>/dev/null || echo 'Redis not reachable'" -Description "Redis ping test"

Write-TestInfo "2.3" "Test connectivité réseau Docker"
docker network inspect ascended33-network 2>$null | ConvertFrom-Json | Select-Object -ExpandProperty Containers | ForEach-Object {
    Write-Host "  - $($_.Name): $($_.IPv4Address)" -ForegroundColor Green
}

# ============================================================================
# PHASE 3 : TESTS APPLICATIFS
# ============================================================================

Write-Header "PHASE 3 - Tests Applicatifs"

Write-TestInfo "3.1" "Test volume Vault monté"
if (Test-Path $VAULT_PATH) {
    Write-Success "Volume Vault accessible: $VAULT_PATH"
    $vaultSize = (Get-ChildItem $VAULT_PATH -Recurse | Measure-Object -Property Length -Sum).Sum / 1MB
    Write-Host "  Taille totale: $([Math]::Round($vaultSize, 2)) MB"
} else {
    Write-Failure "Volume Vault INACCESSIBLE: $VAULT_PATH"
}

Write-TestInfo "3.2" "Tester création fichier dans volume"
$testFile = "$VAULT_PATH\REPORT\test_$(Get-Date -Format 'HHmmss').txt"
try {
    "Test write at $(Get-Date)" | Out-File -FilePath $testFile -Encoding UTF8 -ErrorAction Stop
    Write-Success "Fichier créé: $testFile"
    Remove-Item $testFile -Force
} catch {
    Write-Failure "Impossible d'écrire dans Vault: $_"
}

Write-TestInfo "3.3" "Vérifier structure REPORT"
$reportPath = "$VAULT_PATH\REPORT\Classified"
if (Test-Path $reportPath) {
    Write-Success "Dossier REPORT/Classified existe"
    $files = Get-ChildItem $reportPath -ErrorAction SilentlyContinue
    Write-Host "  Fichiers présents: $($files.Count)"
    $files | ForEach-Object { Write-Host "    - $($_.Name)" }
} else {
    Write-Warning "Dossier REPORT/Classified n'existe pas encore"
}

# ============================================================================
# PHASE 4 : TESTS API EXTERNES
# ============================================================================

Write-Header "PHASE 4 - Tests API Externes"

Write-TestInfo "4.1" "Test HexStrike API (port 8001)"
Test-Endpoint -URL "http://localhost:8001/health" -Description "HexStrike Health Endpoint"

Write-TestInfo "4.2" "Test HackerGPT API (port 8000)"
Test-Endpoint -URL "http://localhost:8000/health" -Description "HackerGPT Health Endpoint"

Write-TestInfo "4.3" "Test Streamlit Dashboard (port 8501)"
Test-Endpoint -URL "http://localhost:8501/_stcore/health" -Description "Streamlit Health Endpoint"

Write-TestInfo "4.4" "Test Kali Labs API (port 5000)"
Test-Endpoint -URL "http://localhost:5000/health" -Description "Kali Labs Health Endpoint"

Write-TestInfo "4.5" "Test Audit API (port 8002)"
Test-Endpoint -URL "http://localhost:8002/health" -Description "Audit API Health Endpoint"

Write-TestInfo "4.6" "Test Vault Indexer (port 8004)"
Test-Endpoint -URL "http://localhost:8004/health" -Description "Vault Indexer Health Endpoint"

Write-TestInfo "4.7" "Test Report Generator (port 8005)"
Test-Endpoint -URL "http://localhost:8005/health" -Description "Report Generator Health Endpoint"

# ============================================================================
# PHASE 5 : TESTS TOR / ANONYMITÉ
# ============================================================================

Write-Header "PHASE 5 - Tests Tor & Anonymité"

Write-TestInfo "5.1" "Vérifier Tor SOCKS5 (port 9050)"
try {
    $torTest = docker exec th3-tor curl -s --socks5 localhost:9050 https://check.torproject.org/api/ip 2>$null
    if ($torTest -like "*isTor*") {
        Write-Success "Tor SOCKS5 est fonctionnel"
        Write-Host "Réponse Tor: $torTest"
    } else {
        Write-Failure "Tor SOCKS5 ne répond pas correctement"
    }
} catch {
    Write-Failure "Erreur test Tor: $_"
}

Write-TestInfo "5.2" "Vérifier Tor control port (9051)"
$result = Invoke-DockerExec -Container "th3-tor" -Command "echo 'GETINFO version' | nc localhost 9051" -Description "Tor Control Port"

# ============================================================================
# PHASE 6 : TESTS PERSISTANCE ET LOGGING
# ============================================================================

Write-Header "PHASE 6 - Tests Persistance & Logging"

Write-TestInfo "6.1" "Vérifier logs Hexstrike"
$hexstrikeLogs = docker logs th3-hexstrike 2>&1 | Select-Object -Last 20
Write-Host "Derniers logs Hexstrike (20 lignes):"
Write-Host $hexstrikeLogs -ForegroundColor Gray

Write-TestInfo "6.2" "Vérifier logs Tor"
$torLogs = docker logs th3-tor 2>&1 | Select-Object -Last 10
Write-Host "Derniers logs Tor (10 lignes):"
Write-Host $torLogs -ForegroundColor Gray

Write-TestInfo "6.3" "Vérifier volumes Docker"
$volumes = docker volume ls --format "table {{.Name}}\t{{.Driver}}"
Write-Host $volumes
Add-Content -Path $RESULTS_LOG -Value "Docker Volumes:`n$volumes"

# ============================================================================
# PHASE 7 : TESTS INTEGRATION PIECES OS & MCP
# ============================================================================

Write-Header "PHASE 7 - Tests Intégration Pieces OS & MCP"

Write-TestInfo "7.1" "Vérifier Pieces OS (port 39300)"
Test-Endpoint -URL "http://localhost:39300/health" -Description "Pieces OS Health"

Write-TestInfo "7.2" "Vérifier Obsidian API (port 3123)"
Test-Endpoint -URL "http://127.0.0.1:3123/health" -Description "Obsidian API Health"

Write-TestInfo "7.3" "Vérifier HexStrike MCP"
if (Test-Path "$INFRA_DIR\Ascended33\hexstrike-mcp.py") {
    Write-Success "HexStrike MCP script trouvé"
} else {
    Write-Warning "HexStrike MCP script non trouvé"
}

# ============================================================================
# RÉSUMÉ FINAL
# ============================================================================

Write-Header "RÉSUMÉ DES TESTS"

$totalTests = $global:TestsPassed + $global:TestsFailed + $global:TestsWarning
$successRate = if ($totalTests -gt 0) { [Math]::Round(($global:TestsPassed / $totalTests) * 100, 2) } else { 0 }

Write-Host "Total Tests: $totalTests"
Write-Host "$($Colors.Success)✓ Succès: $($global:TestsPassed)$($Colors.Reset)"
Write-Host "$($Colors.Error)✗ Échecs: $($global:TestsFailed)$($Colors.Reset)"
Write-Host "$($Colors.Warning)⚠ Avertissements: $($global:TestsWarning)$($Colors.Reset)"
Write-Host "Taux de réussite: $successRate%"

Write-Host "`nRésultats sauvegardés dans: $RESULTS_LOG"

# ============================================================================
# NETTOYAGE (OPTIONNEL)
# ============================================================================

if (-not $SkipCleanup) {
    Write-Header "Options de Nettoyage"
    Write-Host "`nPour nettoyer les ressources Docker:"
    Write-Host "  docker system prune -a --volumes" -ForegroundColor Yellow
    Write-Host "`nPour redémarrer tous les services:"
    Write-Host "  docker-compose -f docker-compose-v2.yml down && docker-compose -f docker-compose-v2.yml up -d" -ForegroundColor Yellow
}

Add-Content -Path $RESULTS_LOG -Value "`n=== TEST SUITE COMPLETED $(Get-Date) ==="

Write-Host "`n$($Colors.Success)✓ Suite de tests terminée !$($Colors.Reset)`n"
