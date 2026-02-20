=================================================
  ASCENDED33 DOCKER IMAGE BUILDER
=================================================
  Building all required Docker images for HexStrike integration
=================================================

# Configuration
$SCRIPT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path
$DOCKERFILE_DIR = "$SCRIPT_DIR\dockerfiles"

# Create Dockerfile directory if it doesn't exist
if (-not (Test-Path $DOCKERFILE_DIR)) {
    Write-Host "[*] Creating Dockerfile directory..." -ForegroundColor Cyan
    New-Item -ItemType Directory -Path $DOCKERFILE_DIR -Force | Out-Null
}

# Check if docker daemon is running
Write-Host "[*] Checking Docker daemon..." -ForegroundColor Yellow
$docker_check = docker ps 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "[!] Docker daemon not running. Starting Docker..." -ForegroundColor Red
    Start-Process "C:\Program Files\Docker\Docker\Docker.exe"
    Start-Sleep -Seconds 10
}

# Build th3-tor image
Write-Host "`n[*] Building th3-tor image..." -ForegroundColor Cyan
@"
FROM alpine:latest

RUN apk add --no-cache \
    tor \
    curl \
    netcat-openbsd

COPY config/torrc /etc/tor/torrc

EXPOSE 9050 9051

HEALTHCHECK --interval=10s --timeout=5s --retries=3 \
    CMD nc -z localhost 9050 || exit 1

CMD ["tor", "-f", "/etc/tor/torrc"]
"@ | Out-File -FilePath "$DOCKERFILE_DIR\Dockerfile.tor" -Encoding UTF8

docker build -f "$DOCKERFILE_DIR\Dockerfile.tor" -t th3-tor:latest "$SCRIPT_DIR"
if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] th3-tor image built successfully" -ForegroundColor Green
} else {
    Write-Host "[!] Failed to build th3-tor image" -ForegroundColor Red
}

# Build th3-kali image
Write-Host "`n[*] Building th3-kali image..." -ForegroundColor Cyan
@"
FROM kalilinux/kali:latest

RUN apt-get update && apt-get install -y \
    curl \
    wget \
    git \
    python3 \
    python3-pip \
    openssh-server \
    nmap \
    metasploit-framework \
    hashcat

RUN mkdir -p /workspace /vault
WORKDIR /workspace

EXPOSE 22

HEALTHCHECK --interval=15s --timeout=10s --retries=3 \
    CMD test -d /workspace || exit 1

CMD ["/bin/bash"]
"@ | Out-File -FilePath "$DOCKERFILE_DIR\Dockerfile.kali" -Encoding UTF8

docker build -f "$DOCKERFILE_DIR\Dockerfile.kali" -t th3-kali:latest "$SCRIPT_DIR"
if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] th3-kali image built successfully" -ForegroundColor Green
} else {
    Write-Host "[!] Failed to build th3-kali image" -ForegroundColor Red
}

# Build th3-hackergpt image
Write-Host "`n[*] Building th3-hackergpt image..." -ForegroundColor Cyan
@"
FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    curl \
    git \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip install --no-cache-dir \
    fastapi \
    uvicorn \
    aiohttp \
    requests \
    anthropic

COPY mcp/ /app/mcp/
COPY scripts/ /app/scripts/

EXPOSE 8000

HEALTHCHECK --interval=20s --timeout=10s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "mcp.hexstrike_client:app", "--host", "0.0.0.0", "--port", "8000"]
"@ | Out-File -FilePath "$DOCKERFILE_DIR\Dockerfile.hackergpt" -Encoding UTF8

docker build -f "$DOCKERFILE_DIR\Dockerfile.hackergpt" -t th3-hackergpt:latest "$SCRIPT_DIR"
if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] th3-hackergpt image built successfully" -ForegroundColor Green
} else {
    Write-Host "[!] Failed to build th3-hackergpt image" -ForegroundColor Red
}

# Build th3-hexstrike image
Write-Host "`n[*] Building th3-hexstrike image..." -ForegroundColor Cyan
@"
FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    curl \
    git \
    gcc \
    nmap \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip install --no-cache-dir \
    fastapi \
    uvicorn \
    aiohttp \
    requests \
    paramiko \
    anthropic

COPY mcp/ /app/mcp/
COPY scripts/ /app/scripts/
COPY workers/ /app/workers/
COPY core/ /app/core/

EXPOSE 8001

HEALTHCHECK --interval=20s --timeout=10s --retries=3 \
    CMD curl -f http://localhost:8001/status || exit 1

CMD ["python3", "-m", "uvicorn", "workers.hexstrike_worker:app", "--host", "0.0.0.0", "--port", "8001"]
"@ | Out-File -FilePath "$DOCKERFILE_DIR\Dockerfile.hexstrike" -Encoding UTF8

docker build -f "$DOCKERFILE_DIR\Dockerfile.hexstrike" -t th3-hexstrike:latest "$SCRIPT_DIR"
if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] th3-hexstrike image built successfully" -ForegroundColor Green
} else {
    Write-Host "[!] Failed to build th3-hexstrike image" -ForegroundColor Red
}

=================================================
  IMAGE VERIFICATION
=================================================

Write-Host "`n[*] Verifying built images..." -ForegroundColor Yellow
docker images | Select-String "th3-"
Write-Host "[OK] Docker images ready" -ForegroundColor Green

=================================================
  STARTING DOCKER COMPOSE
=================================================

Write-Host "`n[*] Starting Docker Compose stack..." -ForegroundColor Cyan
Set-Location $SCRIPT_DIR
docker-compose up -d

Write-Host "[OK] Waiting for services to start..." -ForegroundColor Green
Start-Sleep -Seconds 15

=================================================
  HEALTH CHECK
=================================================

docker-compose ps
Write-Host "[OK] Docker setup complete!" -ForegroundColor Green
