Write-Host "=== DOCKER DIAGNOSTICS ===" -ForegroundColor Cyan
Write-Host ""

# Check Docker version
Write-Host "1. Checking Docker version..." -ForegroundColor Yellow
docker --version
Write-Host ""

# Check Docker daemon status
Write-Host "2. Checking Docker daemon status..." -ForegroundColor Yellow
docker ps | Out-Host
Write-Host ""

# Check running containers
Write-Host "3. Listing all containers..." -ForegroundColor Yellow
docker ps -a
Write-Host ""

# Check docker-compose status
Write-Host "4. Checking docker-compose status..." -ForegroundColor Yellow
docker-compose ps
Write-Host ""

# Check service logs
Write-Host "5. Checking Pieces Sync logs..." -ForegroundColor Yellow
docker logs pieces-sync --tail 20
Write-Host ""

Write-Host "6. Testing localhost connectivity..." -ForegroundColor Yellow
$ports = @(8003, 8004, 8005, 8006)
foreach ($port in $ports) {
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:$port/health" -TimeoutSec 2 -ErrorAction Stop
        Write-Host "Port $port: ONLINE - $($response.StatusCode)" -ForegroundColor Green
    } catch {
        Write-Host "Port $port: OFFLINE - $($_.Exception.Message)" -ForegroundColor Red
    }
}
