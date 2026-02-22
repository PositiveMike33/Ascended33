# ============================================================================
# ASCENDED33 DOCKER LAUNCHER - Ultra-Fast Multi-Container Orchestration
# Launches all Docker containers in parallel with optimized startup
# ============================================================================

param(
    [switch]$Shutdown = $false,
    [switch]$Status = $false,
    [switch]$Debug = $false
)

$ErrorActionPreference = "SilentlyContinue"
$WarningPreference = "SilentlyContinue"

$VAULT_PATH = "D:\Vault\Vault"
$ASCENDED33_PATH = "$VAULT_PATH\Ascended33"
$LOGS_PATH = "$ASCENDED33_PATH\logs"
$TIMESTAMP = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

# Ensure logs directory exists
if (-not (Test-Path $LOGS_PATH)) {
    New-Item -ItemType Directory -Path $LOGS_PATH -Force | Out-Null
}

function Write-Log {
    param([string]$Message, [string]$Level = "INFO")
    $log_message = "[$TIMESTAMP] [$Level] $Message"
    Add-Content -Path "$LOGS_PATH\launcher.log" -Value $log_message
    
    $color = @{
        "INFO"    = "Cyan"
        "SUCCESS" = "Green"
        "WARNING" = "Yellow"
        "ERROR"   = "Red"
    }[$Level]
    
    Write-Host $log_message -ForegroundColor $color
}

function Test-DockerRunning {
    Write-Log "🔍 Checking Docker daemon..." "INFO"
    try {
        $result = docker info 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Log "✓ Docker daemon is running" "SUCCESS"
            return $true
        }
    } catch { }
    
    Write-Log "❌ Docker daemon not available - attempting to start..." "ERROR"
    try {
        Start-Service Docker -ErrorAction Stop
        Start-Sleep -Seconds 5
        return (docker info 2>&1 | $null) -and $LASTEXITCODE -eq 0
    } catch {
        Write-Log "❌ Failed to start Docker service" "ERROR"
        return $false
    }
}

function Check-DockerCompose {
    Write-Log "🔍 Checking Docker Compose..." "INFO"
    $compose_file = "$ASCENDED33_PATH\docker-compose.yml"
    
    if (-not (Test-Path $compose_file)) {
        Write-Log "❌ docker-compose.yml not found at $compose_file" "ERROR"
        return $false
    }
    
    Write-Log "✓ docker-compose.yml found" "SUCCESS"
    return $true
}

function Start-AllContainers {
    Write-Log "======================================" "INFO"
    Write-Log "🚀 STARTING ASCENDED33 DOCKER STACK" "INFO"
    Write-Log "======================================" "INFO"
    
    $start_time = Get-Date
    
    # Test Docker
    if (-not (Test-DockerRunning)) {
        Write-Log "❌ Cannot start - Docker not available" "ERROR"
        return $false
    }
    
    # Check docker-compose.yml
    if (-not (Check-DockerCompose)) {
        return $false
    }
    
    try {
        Write-Log "📦 Starting containers via Docker Compose..." "INFO"
        
        # Parallel startup - Docker Compose handles dependencies
        Set-Location -Path $ASCENDED33_PATH
        $output = & docker-compose up -d 2>&1
        
        if ($LASTEXITCODE -ne 0) {
            Write-Log "❌ Docker Compose failed: $output" "ERROR"
            return $false
        }
        
        Write-Log "✓ Docker Compose initiated" "SUCCESS"
        
        # Wait for health checks in parallel
        Write-Log "⏳ Waiting for container health checks (30-60 seconds)..." "INFO"
        $health_timeout = 120  # seconds
        $health_start = Get-Date
        
        $containers = @("th3-tor", "th3-kali", "th3-hackergpt", "th3-hexstrike")
        $healthy = @()
        
        while ((Get-Date) - $health_start -lt [timespan]::FromSeconds($health_timeout)) {
            foreach ($container in $containers) {
                if ($healthy -contains $container) { continue }
                
                $health = & docker inspect --format='{{.State.Health.Status}}' $container 2>&1
                
                if ($health -eq "healthy") {
                    Write-Log "✓ $container is healthy" "SUCCESS"
                    $healthy += $container
                } elseif ($health -eq "starting") {
                    Write-Log "  ⏳ $container is starting..." "INFO"
                }
            }
            
            if ($healthy.Count -eq 4) {
                Write-Log "✅ All 4 containers are healthy!" "SUCCESS"
                break
            }
            
            Start-Sleep -Seconds 5
        }
        
        if ($healthy.Count -lt 4) {
            Write-Log "⚠ Some containers may not be fully healthy yet" "WARNING"
        }
        
        # Check inter-container connectivity
        Write-Log "🔗 Verifying inter-container connectivity..." "INFO"
        $kali_tor_check = & docker exec th3-kali nc -z th3-tor 9050 2>&1
        
        if ($LASTEXITCODE -eq 0) {
            Write-Log "✓ Kali → Tor connectivity verified" "SUCCESS"
        } else {
            Write-Log "⚠ Network connectivity check inconclusive (non-critical)" "WARNING"
        }
        
        $elapsed = ((Get-Date) - $start_time).TotalSeconds
        Write-Log "======================================" "INFO"
        Write-Log "✅ ASCENDED33 DOCKER STACK READY" "SUCCESS"
        Write-Log "Startup completed in $([math]::Round($elapsed, 1)) seconds" "SUCCESS"
        Write-Log "======================================" "INFO"
        Write-Log "" "INFO"
        Write-Log "🌐 Service URLs:" "INFO"
        Write-Log "   • HackerGPT Dashboard: http://localhost:8000" "INFO"
        Write-Log "   • Hexstrike AI: http://localhost:8001" "INFO"
        Write-Log "   • Tor Proxy: localhost:9050" "INFO"
        Write-Log "" "INFO"
        Write-Log "📊 Starting auto-reporting system..." "INFO"
        
        # Start Python orchestrator in background
        Start-Process -FilePath "python.exe" -ArgumentList "$ASCENDED33_PATH\docker_orchestrator.py" `
            -WindowStyle Hidden -ErrorAction SilentlyContinue
        
        Write-Log "✓ Auto-reporting system started" "SUCCESS"
        
        return $true
        
    } catch {
        Write-Log "❌ Fatal error: $_" "ERROR"
        return $false
    }
}

function Stop-AllContainers {
    Write-Log "======================================" "INFO"
    Write-Log "🛑 SHUTTING DOWN ASCENDED33 DOCKER STACK" "INFO"
    Write-Log "======================================" "INFO"
    
    try {
        Set-Location -Path $ASCENDED33_PATH
        Write-Log "Stopping containers..." "INFO"
        
        $output = & docker-compose down 2>&1
        
        if ($LASTEXITCODE -eq 0) {
            Write-Log "✅ All containers shut down successfully" "SUCCESS"
            return $true
        } else {
            Write-Log "⚠ Partial shutdown completed" "WARNING"
            return $true
        }
    } catch {
        Write-Log "❌ Shutdown error: $_" "ERROR"
        return $false
    }
}

function Get-ContainerStatus {
    Write-Log "======================================" "INFO"
    Write-Log "📊 DOCKER CONTAINER STATUS" "INFO"
    Write-Log "======================================" "INFO"
    
    $containers = @("th3-tor", "th3-kali", "th3-hackergpt", "th3-hexstrike")
    
    foreach ($container in $containers) {
        $status = & docker inspect --format='{{.State.Status}}' $container 2>&1
        $health = & docker inspect --format='{{.State.Health.Status}}' $container 2>&1
        
        if ($health -eq "healthy") {
            Write-Log "✓ $container - $status (healthy)" "SUCCESS"
        } elseif ($status -eq "running") {
            Write-Log "⚠ $container - $status (checking...)" "WARNING"
        } else {
            Write-Log "✗ $container - $status" "ERROR"
        }
    }
    
    Write-Log "======================================" "INFO"
}

# Main execution
if ($Shutdown) {
    Stop-AllContainers
    exit
}

if ($Status) {
    Get-ContainerStatus
    exit
}

# Start all containers
$success = Start-AllContainers

if (-not $success) {
    Write-Log "💥 STARTUP FAILED - Check logs above" "ERROR"
    Write-Log "📋 Troubleshooting:" "INFO"
    Write-Log "   1. Ensure Docker Desktop is installed and running" "INFO"
    Write-Log "   2. Check Docker daemon status: docker info" "INFO"
    Write-Log "   3. Verify docker-compose.yml is present and valid" "INFO"
    Write-Log "   4. Check Docker images are built: docker images" "INFO"
    exit 1
}

Write-Log "🎯 Ascended33 is fully operational!" "SUCCESS"
Write-Log "Press any key to exit (containers continue running)..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
