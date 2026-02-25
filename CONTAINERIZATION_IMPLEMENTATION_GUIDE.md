# 🚀 CONTAINERIZATION IMPLEMENTATION GUIDE

**Date:** 2026-02-22  
**Status:** 🟢 READY TO IMPLEMENT  
**Timeline:** 5 phases over 2-3 weeks

---

## 📋 WHAT'S BEEN CREATED

### ✅ Dockerfiles Created (5 NEW)
```
✅ Dockerfile.kali-labs          → _PROJECTS/🐧_KALI_INTEGRATION_PROJECT/
✅ Dockerfile.audit-api          → _PROJECTS/🔐_SECURITY_AUDIT_PROJECT/
✅ Dockerfile.pieces-sync        → _PROJECTS/🤖_PIECES_OS_INTEGRATION/
✅ Dockerfile.vault-indexer      → _INFRASTRUCTURE/
✅ Dockerfile.report-generator   → _INFRASTRUCTURE/
```

### ✅ Requirements Files Created (5 NEW)
```
✅ requirements.txt              → _PROJECTS/🐧_KALI_INTEGRATION_PROJECT/
✅ requirements.txt              → _PROJECTS/🔐_SECURITY_AUDIT_PROJECT/
✅ requirements.txt              → _PROJECTS/🤖_PIECES_OS_INTEGRATION/
✅ requirements-indexer.txt      → _INFRASTRUCTURE/
✅ requirements-report-generator.txt → _INFRASTRUCTURE/
```

### ✅ Documentation Created
```
✅ CONTAINERIZATION_ANALYSIS.md
✅ CONTAINERIZATION_IMPLEMENTATION_GUIDE.md (THIS FILE)
✅ docker-compose-v2.yml (Complete updated compose file)
```

---

## 🎯 PHASE-BY-PHASE IMPLEMENTATION

### PHASE 1: BUILD ALL IMAGES (Week 1 — 2-3 hours)

#### Step 1.1: Build Kali Labs Image
```bash
cd D:/Vault/Vault

docker build \
  -f _PROJECTS/🐧_KALI_INTEGRATION_PROJECT/Dockerfile.kali-labs \
  -t kali-labs:latest \
  _PROJECTS/🐧_KALI_INTEGRATION_PROJECT/

# Expected output:
# Successfully built [hash]
# Successfully tagged kali-labs:latest
```

**Verify:**
```bash
docker image ls | grep kali-labs
# Should show: kali-labs:latest
```

#### Step 1.2: Build Audit API Image
```bash
docker build \
  -f _PROJECTS/🔐_SECURITY_AUDIT_PROJECT/Dockerfile.audit-api \
  -t audit-api:latest \
  _PROJECTS/🔐_SECURITY_AUDIT_PROJECT/

# Expected output:
# Successfully built [hash]
# Successfully tagged audit-api:latest
```

#### Step 1.3: Build Pieces Sync Image
```bash
docker build \
  -f _PROJECTS/🤖_PIECES_OS_INTEGRATION/Dockerfile.pieces-sync \
  -t pieces-sync:latest \
  _PROJECTS/🤖_PIECES_OS_INTEGRATION/

# Expected output:
# Successfully built [hash]
# Successfully tagged pieces-sync:latest
```

#### Step 1.4: Build Vault Indexer Image
```bash
docker build \
  -f _INFRASTRUCTURE/Dockerfile.vault-indexer \
  -t vault-indexer:latest \
  _INFRASTRUCTURE/

# Expected output:
# Successfully built [hash]
# Successfully tagged vault-indexer:latest
```

#### Step 1.5: Build Report Generator Image
```bash
docker build \
  -f _INFRASTRUCTURE/Dockerfile.report-generator \
  -t report-generator:latest \
  _INFRASTRUCTURE/

# Expected output:
# Successfully built [hash]
# Successfully tagged report-generator:latest
```

#### Step 1.6: Verify all images built
```bash
docker image ls | grep -E 'kali-labs|audit-api|pieces-sync|vault-indexer|report-generator'

# Should show:
# kali-labs               latest    [hash]    123MB
# audit-api              latest    [hash]    456MB
# pieces-sync            latest    [hash]    234MB
# vault-indexer          latest    [hash]    345MB
# report-generator       latest    [hash]    567MB
```

---

### PHASE 2: TEST INDIVIDUAL CONTAINERS (Week 1 — 2 hours)

#### Step 2.1: Test Kali Labs Container
```bash
docker run -it --rm \
  --name test-kali-labs \
  -v D:/Vault/Vault:/vault:rw \
  kali-labs:latest \
  python --version

# Expected output:
# Python 3.11.x
```

#### Step 2.2: Test Audit API Container
```bash
docker run -d --rm \
  --name test-audit-api \
  -p 8002:8002 \
  audit-api:latest

# Wait 5 seconds
sleep 5

# Test endpoint
curl http://localhost:8002/health

# Expected output:
# {"status":"healthy"}

# Stop container
docker stop test-audit-api
```

#### Step 2.3: Test Pieces Sync Container
```bash
docker run -d --rm \
  --name test-pieces-sync \
  -p 8003:8003 \
  pieces-sync:latest

# Wait 5 seconds
sleep 5

# Test endpoint
curl http://localhost:8003/health

# Expected output:
# {"status":"ready"}

# Stop container
docker stop test-pieces-sync
```

#### Step 2.4: Test Vault Indexer Container
```bash
docker run -d --rm \
  --name test-vault-indexer \
  -p 8004:8004 \
  -v D:/Vault/Vault:/vault:ro \
  vault-indexer:latest

# Wait 5 seconds
sleep 5

# Test endpoint
curl http://localhost:8004/health

# Expected output:
# {"status":"initialized"}

# Stop container
docker stop test-vault-indexer
```

#### Step 2.5: Test Report Generator Container
```bash
docker run -d --rm \
  --name test-report-generator \
  -p 8005:8005 \
  report-generator:latest

# Wait 5 seconds
sleep 5

# Test endpoint
curl http://localhost:8005/health

# Expected output:
# {"status":"ready"}

# Stop container
docker stop test-report-generator
```

---

### PHASE 3: BACKUP & REPLACE DOCKER-COMPOSE (Week 2 — 15 min)

#### Step 3.1: Backup current docker-compose.yml
```bash
cd D:/Vault/Vault/_INFRASTRUCTURE

# Backup existing file
cp docker-compose.yml docker-compose.yml.backup-2026-02-22

# List backup
ls -la docker-compose.yml*

# Should show:
# docker-compose.yml              (original)
# docker-compose.yml.backup-2026-02-22  (backup)
```

#### Step 3.2: Copy new docker-compose.yml
```bash
cd D:/Vault/Vault

# First review the differences
diff _INFRASTRUCTURE/docker-compose.yml docker-compose-v2.yml | head -50

# Copy new version to main location
cp docker-compose-v2.yml _INFRASTRUCTURE/docker-compose.yml

# Verify
cat _INFRASTRUCTURE/docker-compose.yml | head -20
```

---

### PHASE 4: START FULL STACK (Week 2 — 5-10 min)

#### Step 4.1: Start all services
```bash
cd D:/Vault/Vault/_INFRASTRUCTURE

# Pull all images and start services
docker compose up -d

# Expected output:
# Creating network "ascended33-network"...
# Creating th3-tor... ✓
# Creating th3-kali... ✓
# Creating th3-hackergpt... ✓
# Creating th3-hexstrike... ✓
# Creating th3-streamlit... ✓
# Creating kali-labs... ✓
# Creating audit-api... ✓
# Creating pieces-sync... ✓
# Creating vault-indexer... ✓
# Creating report-generator... ✓
```

#### Step 4.2: Verify all services running
```bash
docker compose ps

# Expected output:
# CONTAINER ID  IMAGE                    STATUS        PORTS
# [hash]        th3-tor:latest          Up 30s        9050->9050/tcp
# [hash]        th3-kali:latest         Up 25s        
# [hash]        th3-hackergpt:latest    Up 20s        8000->8000/tcp
# [hash]        th3-hexstrike:latest    Up 15s        8001->8001/tcp
# [hash]        th3-streamlit:latest    Up 10s        8501->8501/tcp
# [hash]        kali-labs:latest        Up 5s         5000->5000/tcp
# [hash]        audit-api:latest        Up 5s         8002->8002/tcp
# [hash]        pieces-sync:latest      Up 5s         8003->8003/tcp
# [hash]        vault-indexer:latest    Up 5s         8004->8004/tcp
# [hash]        report-generator:latest Up 5s         8005->8005/tcp
```

#### Step 4.3: Check health status
```bash
# Check each service health
for port in 5000 8002 8003 8004 8005 8501; do
  echo "Testing port $port..."
  curl -s http://localhost:$port/health || echo "Not responding yet"
done
```

---

### PHASE 5: INTEGRATION TESTING (Week 2-3 — 2-3 hours)

#### Step 5.1: Test Streamlit Dashboard
```bash
# Open browser
# http://localhost:8501

# Verify:
✓ Dashboard loads
✓ Menu items visible
✓ All 5 new services accessible from dashboard
✓ No error messages in logs
```

#### Step 5.2: Test Kali Labs Service
```bash
# From Streamlit or via curl
curl http://localhost:5000/

# Verify:
✓ Service responds
✓ Labs initialized
✓ SQLite databases present
```

#### Step 5.3: Test Audit API Service
```bash
curl -X GET http://localhost:8002/api/audits

# Verify:
✓ API responds
✓ Database initialized
✓ No connection errors
```

#### Step 5.4: Test Pieces Sync Service
```bash
curl http://localhost:8003/status

# Verify:
✓ Webhook handler ready
✓ Pieces API reachable (host.docker.internal:39300)
✓ Sync service healthy
```

#### Step 5.5: Test Vault Indexer Service
```bash
curl -X GET http://localhost:8004/search?q=test

# Verify:
✓ Search API responds
✓ Indexer initialized
✓ /vault mounted and accessible
```

#### Step 5.6: Test Report Generator Service
```bash
curl -X POST http://localhost:8005/generate \
  -H "Content-Type: application/json" \
  -d '{"template":"audit","title":"Test"}'

# Verify:
✓ API responds
✓ Report generation engine ready
✓ PDF support working
```

#### Step 5.7: View logs for any errors
```bash
# Check logs for all services
docker compose logs

# Check specific service
docker compose logs kali-labs
docker compose logs audit-api
docker compose logs pieces-sync
docker compose logs vault-indexer
docker compose logs report-generator

# Expected: No ERROR messages
```

---

## 🔄 COMMON TROUBLESHOOTING

### Issue 1: Build fails due to missing dependencies

**Symptom:**
```
ERROR: couldn't find requirements.txt
```

**Fix:**
```bash
# Verify files exist
ls -la _PROJECTS/🐧_KALI_INTEGRATION_PROJECT/requirements.txt
ls -la _PROJECTS/🔐_SECURITY_AUDIT_PROJECT/requirements.txt
ls -la _PROJECTS/🤖_PIECES_OS_INTEGRATION/requirements.txt

# If missing, recreate from CONTAINERIZATION_ANALYSIS.md
```

### Issue 2: Port already in use

**Symptom:**
```
ERROR: bind: address already in use :::8002
```

**Fix:**
```bash
# Find what's using the port
lsof -i :8002

# Either:
# 1. Stop the other service
# 2. Change port in docker-compose.yml
# 3. Kill the process (careful!)
```

### Issue 3: Container exits immediately

**Symptom:**
```
docker ps shows container as "Exited (1)"
```

**Fix:**
```bash
# Check logs
docker logs <container-name>

# Common causes:
# - Missing volumes
# - Bad environment variables
# - Python import errors
# - Missing dependencies

# Fix the error in Dockerfile or requirements.txt
# Rebuild image
docker build ...
```

### Issue 4: Pieces Sync can't reach Pieces API

**Symptom:**
```
ConnectionError: Cannot reach http://host.docker.internal:39300
```

**Fix:**
```bash
# Verify Pieces running on port 39300
netstat -an | grep 39300

# If Pieces not running, start it
# Update docker-compose.yml:
# Change PIECES_API_URL to actual IP/hostname if needed
```

---

## 📊 VERIFICATION CHECKLIST

Before considering containerization complete:

```
✅ All 5 images built successfully
   [ ] kali-labs:latest
   [ ] audit-api:latest
   [ ] pieces-sync:latest
   [ ] vault-indexer:latest
   [ ] report-generator:latest

✅ All 10 containers running
   [ ] th3-tor
   [ ] th3-kali
   [ ] th3-hackergpt
   [ ] th3-hexstrike
   [ ] th3-streamlit
   [ ] kali-labs
   [ ] audit-api
   [ ] pieces-sync
   [ ] vault-indexer
   [ ] report-generator

✅ All health checks passing
   [ ] docker compose ps shows all "Up"
   [ ] All /health endpoints respond
   [ ] No ERROR in docker compose logs

✅ Volumes mounted correctly
   [ ] /vault accessible from all containers
   [ ] Data persisted in named volumes
   [ ] No permission errors

✅ Networking working
   [ ] Services communicate via docker network
   [ ] Ports correctly mapped
   [ ] host.docker.internal accessible from containers

✅ Integration working
   [ ] Streamlit dashboard sees all services
   [ ] API endpoints accessible
   [ ] Data flows between containers
```

---

## 🚀 NEXT STEPS AFTER CONTAINERIZATION

### Week 3: Create Missing APIs

1. **Kali Labs API** (`kali-labs/api.py`)
   - GET /labs → List available labs
   - POST /labs/{lab}/run → Execute lab
   - GET /labs/{lab}/status → Check status

2. **Audit API** (`audit-api/api.py`)
   - POST /audits → Create new audit
   - GET /audits/{id} → Retrieve audit
   - GET /audits → List all audits

3. **Pieces Sync API** (`pieces-sync/webhook_handler.py`)
   - POST /webhook → Handle sync events
   - GET /status → Sync status
   - POST /sync → Trigger manual sync

4. **Vault Indexer API** (`vault-indexer/search_api.py`)
   - GET /search → Full-text search
   - POST /index → Rebuild index
   - GET /categories → List content categories

5. **Report Generator API** (`report-generator/report_api.py`)
   - POST /generate → Generate report
   - GET /templates → List templates
   - POST /validate → Validate for legal compliance

### Week 4: Connect via Streamlit Dashboard

- Add UI panels for each new service
- Create workflows combining services
- Build monitoring dashboard
- Add service management controls

---

## 📁 FILES CREATED SUMMARY

```
D:/Vault/Vault/
├── CONTAINERIZATION_ANALYSIS.md
├── CONTAINERIZATION_IMPLEMENTATION_GUIDE.md (THIS FILE)
├── docker-compose-v2.yml
│
├── _PROJECTS/🐧_KALI_INTEGRATION_PROJECT/
│   ├── Dockerfile.kali-labs ✨ NEW
│   └── requirements.txt ✨ NEW
│
├── _PROJECTS/🔐_SECURITY_AUDIT_PROJECT/
│   ├── Dockerfile.audit-api ✨ NEW
│   └── requirements.txt ✨ NEW
│
├── _PROJECTS/🤖_PIECES_OS_INTEGRATION/
│   ├── Dockerfile.pieces-sync ✨ NEW
│   └── requirements.txt ✨ NEW
│
└── _INFRASTRUCTURE/
    ├── Dockerfile.vault-indexer ✨ NEW
    ├── requirements-indexer.txt ✨ NEW
    ├── Dockerfile.report-generator ✨ NEW
    └── requirements-report-generator.txt ✨ NEW
```

---

## ⏰ ESTIMATED TIMELINE

| Phase | Task | Duration | Status |
|-------|------|----------|--------|
| 1 | Build all 5 images | 2-3 hours | Ready |
| 2 | Test individual containers | 2 hours | Ready |
| 3 | Backup & replace docker-compose.yml | 15 min | Ready |
| 4 | Start full stack | 5-10 min | Ready |
| 5 | Integration testing | 2-3 hours | Ready |
| **Total** | **Complete containerization** | **~8-10 hours** | **Ready to start** |

---

## 🎯 SUCCESS CRITERIA

✅ All files created (10 Dockerfiles + 5 requirements files)  
✅ All containers build without errors  
✅ All containers run and pass health checks  
✅ All services accessible on correct ports  
✅ Streamlit dashboard sees all new services  
✅ Data persists in volumes  
✅ Services communicate via docker network  

**Current Status: 🟢 READY FOR IMPLEMENTATION**

---

**Created:** 2026-02-22  
**Ready to start:** YES ✅  
**Estimated completion:** 2026-02-27 (3-5 days)
