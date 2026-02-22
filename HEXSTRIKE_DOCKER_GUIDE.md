# HexStrike Docker Integration Guide

## Overview

HexStrike now runs entirely within Docker containers with full Tor integration and Claude/OSINT capabilities.

### Architecture

```
┌─────────────────────────────────────────────┐
│           Streamlit Dashboard               │
│          (http://localhost:8501)             │
└──────────────────┬──────────────────────────┘
                   │
    ┌──────────────┼──────────────┐
    │              │              │
┌───▼───┐  ┌──────▼──────┐  ┌───▼─────────┐
│th3-tor│  │ th3-kali    │  │th3-hackergpt│
│       │  │  (OSINT)    │  │ (Claude AI) │
│SOCKS5 │  │ SSH:22      │  │  API:8000   │
│:9050  │  │ workspace   │  │ Vault sync  │
└────┬──┘  └──────┬──────┘  └────┬────────┘
     │            │              │
     └────────────┼──────────────┘
                  │
            ┌─────▼──────┐
            │th3-hexstrike
            │ (Main API)
            │ API:8001
            │ Reports
            └────────────┘
```

## Quick Start

### 1. Build & Launch (First Time)

```bash
# Run setup script (Administrator required)
.\DOCKER_SETUP_FIX.bat
```

This will:
- Build all 4 Docker images locally
- Start the complete stack
- Verify all services

### 2. Daily Launch

```bash
# Simple launch script
.\LAUNCH_HEXSTRIKE_DOCKER.bat
```

Or use Docker commands directly:

```bash
docker-compose up -d
docker-compose ps
```

## Services & Endpoints

| Service | Container | Port | Health Check |
|---------|-----------|------|--------------|
| Tor | th3-tor | 9050 | nc -z localhost 9050 |
| Kali (OSINT) | th3-kali | 22 | workspace dir exists |
| HackerGPT (Claude) | th3-hackergpt | 8000 | /health endpoint |
| HexStrike (Main) | th3-hexstrike | 8001 | /status endpoint |
| Streamlit Dashboard | localhost | 8501 | Browser access |

## Common Commands

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f th3-hexstrike
docker-compose logs -f th3-hackergpt
```

### Stop Services
```bash
docker-compose down
```

### Restart Single Service
```bash
docker-compose restart th3-hexstrike
```

### Access Kali Container
```bash
docker exec -it th3-kali /bin/bash
```

### Check Service Status
```bash
docker-compose ps
docker-compose health-check
```

## Troubleshooting

### Docker Daemon Not Running
```powershell
# Start Docker manually
start "" "C:\Program Files\Docker\Docker\Docker.exe"
```

### HexStrike API (8001) Not Responding

1. Check if container is running:
```bash
docker ps | findstr th3-hexstrike
```

2. Check logs:
```bash
docker-compose logs th3-hexstrike
```

3. Verify dependencies:
```bash
docker-compose ps
# All 4 containers should show "Up"
```

4. Restart service:
```bash
docker-compose restart th3-hexstrike
```

### HackerGPT API (8000) Connection Failed

1. Verify Claude API key in environment
2. Check network connectivity:
```bash
docker exec th3-hackergpt curl -f http://localhost:8000/health
```

3. Rebuild container:
```bash
docker-compose build --no-cache th3-hackergpt
docker-compose up -d th3-hackergpt
```

### Tor Connection Issues

1. Check Tor service:
```bash
docker exec th3-tor nc -z localhost 9050
```

2. View Tor logs:
```bash
docker-compose logs th3-tor
```

3. Verify torrc config:
```
cat config/torrc
```

### Vault Sync Not Working

1. Verify mount point:
```bash
docker exec th3-kali ls -la /vault
```

2. Check permissions:
```bash
docker exec th3-hexstrike ls -la /vault
```

3. Verify volume in compose file:
```yaml
volumes:
  - D:/Vault/Vault:/vault:rw
```

## Performance Optimization

### Reduce Memory Usage
```yaml
# In docker-compose.yml, add to service:
deploy:
  resources:
    limits:
      memory: 2G
    reservations:
      memory: 1G
```

### Improve Build Speed
```bash
# Build with cache:
docker-compose build

# Build without cache (slower):
docker-compose build --no-cache
```

### Network Optimization
```bash
# Increase Tor circuit renewal
docker exec th3-tor tor-control NEWIDENTITY
```

## Environment Variables

Services read from environment:

| Variable | Value | Purpose |
|----------|-------|---------|
| TOR_PROXY | socks5://th3-tor:9050 | Tor routing |
| VAULT_PATH | /vault | Obsidian sync |
| WORKSPACE | /workspace | Kali workspace |
| CLAUDE_ENABLED | true | Claude integration |
| ANONYMITY_MODE | enabled | Secure operations |

## Data Persistence

Volumes mounted:
- `tor-data`: Tor circuits & caches
- `kali-tools`: Installed tools
- `kali-workspace`: Work files
- `hackergpt-data`: AI models
- `hexstrike-data`: Reports & results
- `D:/Vault/Vault`: Obsidian Vault (RW)

## Maintenance

### Weekly
```bash
# Check disk usage
docker system df

# Prune unused images/networks
docker system prune -a
```

### Monthly
```bash
# Rebuild images
docker-compose build --no-cache

# Update base images
docker pull alpine:latest
docker pull kalilinux/kali:latest
docker pull python:3.11-slim
```

## Advanced Configuration

### Custom Tor Exit Nodes
Edit `config/torrc`:
```
ExitNodes {fr},{de},{nl}
StrictNodes 1
```

Then restart:
```bash
docker-compose restart th3-tor
```

### Enable VPN Over Tor
In `docker-compose.yml`, add to th3-kali:
```yaml
environment:
  - USE_VPN=true
  - VPN_PROVIDER=protonvpn
```

### Multi-User Sessions
Use Kali container user management:
```bash
docker exec th3-kali useradd -m newuser
docker exec th3-kali passwd newuser
```

## Support & Debugging

### Generate Debug Report
```bash
docker-compose config
docker-compose logs > debug.log
docker ps -a
docker images | grep th3
```

### Performance Monitoring
```bash
# Real-time stats
docker stats

# Container details
docker inspect th3-hexstrike
```

---

**Last Updated:** 2026-02-20  
**HexStrike Version:** Docker-integrated  
**Status:** Production Ready ✅
