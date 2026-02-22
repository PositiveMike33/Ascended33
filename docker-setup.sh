#!/bin/bash

=================================================
  ASCENDED33 DOCKER SETUP - BUILD & LAUNCH
=================================================

cd "$(dirname "$0")"

echo "[*] Checking Docker daemon..."
if ! docker ps &>/dev/null; then
    echo "[!] Docker daemon not running"
    echo "[*] Please start Docker Desktop manually"
    exit 1
fi

echo "[OK] Docker daemon running"
echo ""
echo "[*] Building Docker images (10-20 minutes)..."
echo ""

docker-compose build --no-cache

if [ $? -ne 0 ]; then
    echo ""
    echo "[!] Docker build failed"
    exit 1
fi

echo ""
echo "[OK] Images built successfully!"
echo ""
echo "[*] Starting Docker Compose services..."
echo ""

docker-compose up -d

if [ $? -ne 0 ]; then
    echo "[!] Docker Compose startup failed"
    exit 1
fi

echo ""
echo "[*] Waiting for services to initialize..."
sleep 15

echo ""
echo "================================================="
echo "  SERVICE STATUS"
echo "================================================="
docker-compose ps

echo ""
echo "[OK] ASCENDED33 Docker setup complete!"
echo ""
echo "Available endpoints:"
echo "  - Streamlit Dashboard: http://localhost:8501"
echo "  - HackerGPT API:       http://localhost:8000"
echo "  - HexStrike API:       http://localhost:8001"
echo "  - Tor SOCKS5:          localhost:9050"
echo ""
