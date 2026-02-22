# HexStrike Docker Setup - Quick Start

## Problem Solved ✅

HexStrike now works **entirely with Docker containers**:
- ✅ th3-tor (Tor anonymity)
- ✅ th3-kali (OSINT tools)
- ✅ th3-hackergpt (Claude AI)
- ✅ th3-hexstrike (Main API)

## Step 1: First Time Setup (Build Images)

**Run as Administrator:**

```bash
.\DOCKER_SETUP_FIX.bat
```

This will:
1. Build all 4 Docker images locally
2. Start the complete stack
3. Verify services are running

**Expected output:**
```
[OK] Docker images built successfully
[OK] Docker services starting...
SERVICE STATUS
th3-tor          ... Up ...
th3-kali         ... Up ...
th3-hackergpt    ... Up ...
th3-hexstrike    ... Up ...
```

## Step 2: Daily Launch

**After first setup, simply run:**

```bash
.\LAUNCH_HEXSTRIKE_DOCKER.bat
```

Or via Docker directly:

```bash
docker-compose up -d
```

## Step 3: Verify Services

**Check everything is working:**

```bash
.\VERIFY_HEXSTRIKE.bat
```

## Access HexStrike

| Service | URL |
|---------|-----|
| **Dashboard** | http://localhost:8501 |
| **HackerGPT API** | http://localhost:8000 |
| **HexStrike API** | http://localhost:8001 |
| **Tor SOCKS5** | localhost:9050 |

## Common Tasks

### View Logs
```bash
docker-compose logs -f
docker-compose logs -f th3-hexstrike
```

### Stop Services
```bash
docker-compose down
```

### Restart Single Service
```bash
docker-compose restart th3-hexstrike
```

### Access Kali Terminal
```bash
docker exec -it th3-kali /bin/bash
```

### Rebuild Images (if issues)
```bash
docker-compose build --no-cache
docker-compose up -d
```

## Troubleshooting

### Docker Not Running?
Windows will start Docker automatically, but if not:
```powershell
start "" "C:\Program Files\Docker\Docker\Docker.exe"
```

### HexStrike API (8001) Not Responding?
```bash
# Check if container is running
docker ps | findstr th3-hexstrike

# View logs
docker-compose logs th3-hexstrike

# Restart
docker-compose restart th3-hexstrike
```

### Tor Connection Issues?
```bash
# Test Tor
docker exec th3-tor nc -z localhost 9050

# View Tor logs
docker-compose logs th3-tor
```

### Vault Sync Not Working?
```bash
# Verify mount
docker exec th3-kali ls -la /vault

# Check permissions
docker exec th3-hexstrike ls -la /vault
```

## File Structure

```
Ascended33/
├── DOCKER_SETUP_FIX.bat          ← First-time setup
├── LAUNCH_HEXSTRIKE_DOCKER.bat   ← Daily launch
├── VERIFY_HEXSTRIKE.bat          ← Verify services
├── docker-compose.yml            ← Stack configuration
├── dockerfiles/                  ← Custom Docker images
│   ├── Dockerfile.tor
│   ├── Dockerfile.kali
│   ├── Dockerfile.hackergpt
│   └── Dockerfile.hexstrike
├── HEXSTRIKE_DOCKER_GUIDE.md     ← Full documentation
└── [rest of project files...]
```

## Architecture

```
User Browser
    ↓
Streamlit Dashboard (8501)
    ↓
    ├─→ HexStrike API (8001) ←─┐
    │       ↓                   │
    │   th3-hexstrike          │
    │       ↓                   │
    ├─→ HackerGPT API (8000)    │
    │       ↓                   │
    │   th3-hackergpt          │
    │       ↓                   │
    ├─→ Kali OSINT (SSH:22)     │
    │       ↓                   │
    │   th3-kali               │
    │       ↓                   │
    └─→ Tor Proxy (9050)        │
            ↓                   │
        th3-tor ←───────────────┘
        (SOCKS5)

All connected to Obsidian Vault (/vault mount)
```

## Performance Notes

- **First build:** ~15-20 minutes (pulls base images)
- **Daily startup:** ~10-15 seconds
- **Memory usage:** ~3-4GB when running all 4 containers

## Next Steps

1. ✅ Run `DOCKER_SETUP_FIX.bat` to build images
2. ✅ Run `LAUNCH_HEXSTRIKE_DOCKER.bat` to start services
3. ✅ Run `VERIFY_HEXSTRIKE.bat` to confirm everything works
4. ✅ Open http://localhost:8501 for Streamlit dashboard
5. ✅ Check Vault sync is working properly

---

**For detailed configuration options, see:** `HEXSTRIKE_DOCKER_GUIDE.md`

**Last Updated:** 2026-02-20  
**Status:** Production Ready ✅
