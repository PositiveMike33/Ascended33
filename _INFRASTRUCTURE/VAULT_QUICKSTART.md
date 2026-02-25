# 🚀 Vault Brain - Quick Start Guide

## ✅ Current Status

All 6 th3 containers are **UP and RUNNING** with D:\Vault\Vault integrated:

```
🟢 th3-security-tools    (3000, 8080)
🟢 th3-kali              (22 SSH)
🟢 th3-tor               (9050, 9051)
🟢 th3-hexstrike         (8001)
🟢 th3-hackergpt         (8000)
🟢 th3-streamlit         (8501)
```

---

## 🧠 What is the Vault Brain?

Your Obsidian vault at **D:\Vault\Vault** is now a **shared virtual brain** accessible to all containers at `/vault`.

Every container can:
- ✅ **Read** your notes, knowledge base, planning documents
- ✅ **Write** analysis, reports, findings
- ✅ **Update** brain context with AI discoveries
- ✅ **Access** as a unified knowledge source for Claude Code

---

## 📊 Container Access Points

| Service | Port | Access URL | Purpose |
|---------|------|-----------|---------|
| **Security Tools** | 8080 | http://localhost:8080 | Web UI for tools |
| **Streamlit** | 8501 | http://localhost:8501 | Dashboard interface |
| **HexStrike** | 8001 | http://localhost:8001 | Security scanning |
| **HackerGPT** | 8000 | http://localhost:8000 | AI security analysis |
| **Tor SOCKS** | 9050 | 127.0.0.1:9050 | Anonymous proxy |
| **Kali SSH** | 22 | ssh://localhost:22 | Shell access |

---

## 🔧 Common Tasks

### 1. Access Vault from a Container

```bash
docker exec -it th3-kali bash
# Inside container:
ls /vault
cat /vault/KNOWLEDGE/index.md
```

### 2. Write a Report from Container

```bash
docker exec th3-security-tools bash -c "
  echo 'Security Report - $(date)' > /vault/RAPPORT\ QUOTIDIEN/$(date +%Y-%m-%d).md
  echo '## Findings' >> /vault/RAPPORT\ QUOTIDIEN/$(date +%Y-%m-%d).md
"
```

### 3. Read from Vault in Python (th3-streamlit)

```python
import json
import os

# Read knowledge database
vault_path = os.getenv('VAULT_PATH', '/vault')
with open(f'{vault_path}/piecesdb.json', 'r') as f:
    knowledge = json.load(f)

# Write analysis results
with open(f'{vault_path}/_BRAIN/latest_analysis.json', 'w') as f:
    json.dump(results, f, indent=2)
```

### 4. Inter-Container Communication

```bash
# From th3-hackergpt, call th3-hexstrike API:
docker exec th3-hackergpt curl http://th3-hexstrike:8001/api/status

# From th3-tor, route traffic through Tor:
docker exec th3-security-tools curl --socks5 th3-tor:9050 http://example.com
```

### 5. Monitor Vault Changes

```bash
watch -n 1 'ls -ltr /vault/_BRAIN/ | tail -10'
```

---

## 📁 Vault Directory Structure (Accessible in All Containers)

```
/vault/
├── THIRTY3/                    # Main project files
├── KNOWLEDGE/                  # Knowledge base & reference
├── LEARNING/                   # Learning materials & courses
├── PLANNING/                   # Plans, roadmaps, strategies
├── RAPPORT QUOTIDIEN/          # Daily reports & findings
├── Notes et Mémos Importants/  # Critical notes & memos
├── _INFRASTRUCTURE/            # Deployment configs
│   └── Ascended33/             # Streamlit app code
├── _PROJECTS/                  # Active projects
├── _BRAIN/                     # AI analysis & context
│   ├── latest_analysis.json
│   ├── claude_context.md
│   └── findings.md
├── _TEMPLATES/                 # Document templates
├── METADATA/                   # Metadata & indexes
├── LLM's/                      # LLM configurations
├── Security/                   # Security policies & docs
├── EXTERNAL/                   # External resources
├── piecesdb.json              # Main knowledge database
└── docker-compose.yml         # Orchestration file
```

---

## 🚀 Start/Stop Commands

### Start all containers (from D:\Vault\Vault):
```bash
docker compose up -d
```

### Stop all containers:
```bash
docker compose down
```

### Restart a specific container:
```bash
docker restart th3-hackergpt
```

### View logs:
```bash
# All containers:
docker compose logs -f

# Specific container:
docker logs th3-security-tools -f --tail 50

# Last 5 minutes:
docker logs th3-kali --since 5m -f
```

---

## 🔍 Verify Integration

Run verification script:
```powershell
.\verify-vault-integration.ps1
```

Or manually check:
```bash
# Check all containers running
docker ps --format "table {{.Names}}\t{{.Status}}"

# Verify Vault mount in container
docker exec th3-kali test -d /vault && echo "✅ Vault accessible" || echo "❌ Vault not found"

# List Vault contents
docker exec th3-hackergpt ls -la /vault/
```

---

## 📊 Monitoring

### Health Check Status:
```bash
docker ps --format "table {{.Names}}\t{{.Status}}"
```

### Resource Usage:
```bash
docker stats --no-stream
```

### Network Status:
```bash
docker network ls
docker network inspect th3-brain-network
```

---

## 🔐 Security Notes

- ✅ Vault is mounted as **read-write** to all containers
- ✅ Tor container provides anonymous proxy access
- ✅ SSH available on kali container (port 22)
- ✅ All containers on internal Docker networks
- ⚠️ Ensure D:\Vault\Vault permissions allow Docker access
- ⚠️ Backup Vault data regularly

---

## 🛠️ Advanced: Accessing External Disk Mounts

To mount additional external disk paths to containers, edit `docker-compose.yml`:

```yaml
volumes:
  - D:/Vault/PDF:/vault/PDF:ro          # Read-only
  - D:/Vault/PNG:/vault/PNG:ro          # Read-only
```

Then restart:
```bash
docker compose up -d
```

---

## 🐛 Troubleshooting

### Container stuck restarting?
```bash
docker logs <container-name> --tail 50
docker restart <container-name>
```

### Can't access /vault from container?
```bash
# Check mount exists
docker inspect <container-name> | grep -A10 "Mounts"

# If missing, stop and update docker-compose.yml, then:
docker compose down
docker compose up -d
```

### Vault not accessible on host?
```bash
# Verify external disk is mounted
Get-PSDrive | Select-Object Name, Root
# Should show D: drive

# Check Docker can read it:
docker run --rm -v D:/:/host:ro alpine ls /host/Vault
```

---

## 📞 Support

For Docker issues:
```bash
docker compose logs -f
docker inspect <container-name>
```

For more details, see:
- `VAULT_INTEGRATION_REPORT.md` - Full technical integration details
- `docker-compose.yml` - Container orchestration configuration

---

**Status**: ✅ Ready for use  
**Last Updated**: 2026-02-19  
**All Containers**: 🟢 Running
