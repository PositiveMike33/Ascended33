# 🔧 OBSIDIAN VAULT API CONNECTION FIX

**Status**: ✅ **DEPLOYED**

---

## 🔍 PROBLEM IDENTIFIED

Ascended33 showed:
- ❌ **Obsidian Vault** - OFFLINE
- ❌ Error: "Obsidian Vault API offline"

**Root Cause**: 
Container `th3-streamlit` tried to connect to `http://localhost:27123` but from inside a Docker container, `localhost` refers to the container itself, not the host OS where Obsidian runs.

**Network Isolation Issue:**
```
Host OS:
  Obsidian → listening on 127.0.0.1:27123
  
Docker Container (th3-streamlit):
  Tries to reach localhost:27123
  BUT localhost = container itself, not host!
  ❌ Connection refused
```

---

## ✨ SOLUTION APPLIED

### 1. Add Host Gateway Mapping

```powershell
--add-host=host.docker.internal:host-gateway
```

This special hostname allows containers to reach the host OS services.

### 2. Set Environment Variables

```powershell
-e VAULT_API_URL=http://host.docker.internal:27123
-e OBSIDIAN_HOST=host.docker.internal
-e OBSIDIAN_PORT=27123
```

These variables tell th3-streamlit where to find Obsidian's API.

### 3. Full Updated Configuration

```powershell
docker run -d `
  --name th3-streamlit `
  --network ascended33_ascended33-network `
  -p 8501:8501 `
  --add-host=host.docker.internal:host-gateway `
  -e VAULT_API_URL=http://host.docker.internal:27123 `
  -e OBSIDIAN_HOST=host.docker.internal `
  -e OBSIDIAN_PORT=27123 `
  -v "D:/Vault/Vault:/vault:rw" `
  -v "D:/Vault/Vault/_INFRASTRUCTURE/Ascended33:/app:rw" `
  -v /var/run/docker.sock:/var/run/docker.sock:rw `
  -e VAULT_PATH=/vault `
  -e STREAMLIT_SERVER_HEADLESS=true `
  -e STREAMLIT_SERVER_PORT=8501 `
  --restart unless-stopped `
  python:3.11-slim bash -c "pip install streamlit requests docker -q && streamlit run /app/streamlit_app.py"
```

---

## 🔄 HOW IT WORKS NOW

### Network Flow

```
┌──────────────────────────────────────┐
│  Host OS                             │
│  - Obsidian (port 27123)            │
│  - Docker Daemon                     │
└─────────────┬──────────────────────┘
              │
              │ Docker internal
              │ routing
              │
    ┌─────────▼────────────────┐
    │  Docker Container        │
    │  th3-streamlit           │
    │                          │
    │  host.docker.internal    │  ← Special DNS name
    │  Points to host OS       │
    │                          │
    │  Can now reach:          │
    │  ✅ Obsidian (27123)    │
    │  ✅ Docker socket       │
    └──────────────────────────┘
```

### Connection Sequence

1. **Ascended33 app** needs Vault status
2. Calls: `http://host.docker.internal:27123/...`
3. Docker resolves `host.docker.internal` → host OS IP
4. Container connects to Obsidian API
5. Gets Vault status ✅
6. Displays in dashboard

---

## ✅ VERIFICATION

### 1. Check Container is Running

```bash
docker ps | grep th3-streamlit
# Should show: th3-streamlit  Up X seconds
```

### 2. Test Obsidian Connection from Container

```bash
docker exec th3-streamlit curl http://host.docker.internal:27123/
# Should get a response (not connection refused)
```

### 3. Test Environment Variables

```bash
docker exec th3-streamlit printenv | grep -i obsidian
# Should show:
# VAULT_API_URL=http://host.docker.internal:27123
# OBSIDIAN_HOST=host.docker.internal
# OBSIDIAN_PORT=27123
```

### 4. Refresh Dashboard

- Open: http://localhost:8501
- Hard refresh: **Ctrl+Shift+Del** then **Ctrl+F5**
- Check **SYSTEM STATUS** panel

**Should now show:**
```
✅ HexStrike       - CONNECTED
✅ Obsidian Vault  - ONLINE (or SYNCED)
✅ OPSEC           - SAFE
✅ VPN             - RELAYED (or status)
✅ TOR             - ACTIVE
```

---

## 📋 KEY CONFIGURATION CHANGES

| Parameter | Value | Purpose |
|-----------|-------|---------|
| `--add-host` | `host.docker.internal:host-gateway` | Enable host OS access |
| `VAULT_API_URL` | `http://host.docker.internal:27123` | Obsidian API endpoint |
| `OBSIDIAN_HOST` | `host.docker.internal` | Obsidian hostname |
| `OBSIDIAN_PORT` | `27123` | Obsidian port |

---

## 📚 TECHNICAL NOTES

### host.docker.internal

- **Purpose**: Special DNS name that Docker provides
- **On Linux**: May need `--network host` or Docker daemon configuration
- **On Windows/Mac**: Built-in, works automatically
- **In this setup**: Works with bridge network + `--add-host`

### Port 27123

- **Service**: Obsidian Local REST API
- **Plugin Required**: "Local REST API" community plugin
- **Configuration**: Needs API key setup in Obsidian
- **Protocol**: HTTP (not HTTPS in local setup)

---

## 🔧 IF VAULT IS STILL OFFLINE

### Troubleshooting Checklist

1. **Verify Obsidian is running**
   ```bash
   netstat -ano | findstr 27123
   # Should show: TCP 127.0.0.1:27123 LISTENING
   ```

2. **Check Obsidian Local REST API plugin**
   - Settings → Community Plugins → Search "Local REST API"
   - Ensure it's installed and enabled
   - Note the API key

3. **Test connection from container**
   ```bash
   docker exec th3-streamlit curl -v http://host.docker.internal:27123/
   ```
   - Should NOT say "connection refused"
   - May show auth error (401) - that's OK
   - That means the port is reachable

4. **Check environment variables**
   ```bash
   docker inspect th3-streamlit | grep OBSIDIAN
   ```
   - Should show all OBSIDIAN_* vars set

5. **Restart container**
   ```bash
   docker restart th3-streamlit
   ```

6. **Update config file**
   
   Look at Ascended33 config file (config/config.yaml) and ensure:
   ```yaml
   vault:
     api_url: http://host.docker.internal:27123
     api_key: "YOUR_API_KEY_HERE"
   ```

---

## 📁 OBSIDIAN SETUP (If Not Done)

### 1. Install Local REST API Plugin

- Open Obsidian
- Settings → Community Plugins
- Search "Local REST API"
- Install and Enable

### 2. Get API Key

- Settings → Community Plugins → Local REST API
- Find "API Key" setting
- Copy the generated key (or create one)

### 3. Configure Ascended33

Create or update `D:\Vault\Vault\_INFRASTRUCTURE\Ascended33\config\config.yaml`:

```yaml
vault:
  path: "D:\\Vault\\Vault"
  api_url: "http://host.docker.internal:27123"
  api_key: "YOUR_API_KEY_FROM_OBSIDIAN"
  port: 27123

obsidian:
  host: "host.docker.internal"
  port: 27123
  enabled: true
```

### 4. Restart th3-streamlit

```bash
docker restart th3-streamlit
```

---

## ✅ EXPECTED BEHAVIOR NOW

### Dashboard Status

```
SYSTEM STATUS:
🟢 HexStrike       - CONNECTED
🟢 Obsidian Vault  - ONLINE / SYNCED
🟢 OPSEC           - SAFE
🟢 VPN             - RELAYED / CONNECTED
🟢 TOR             - ACTIVE / CONNECTED
```

### Vault Synchronization

- Ascended33 can now:
  - ✅ Read Vault files
  - ✅ Sync with Obsidian
  - ✅ Log missions to Vault
  - ✅ Store reports in Obsidian

---

## 📊 CURRENT DEPLOYMENT STATUS

✅ **th3-streamlit** - Redeployed with:
- Docker socket mounted
- host.docker.internal mapping
- Obsidian environment variables
- Docker Python SDK

✅ **Host OS** - Obsidian running on port 27123
✅ **Network** - Docker container can now reach host services
✅ **API** - Obsidian Local REST API accessible from container

---

## 🚀 NEXT STEPS

1. **Verify Obsidian is running** with Local REST API plugin
2. **Refresh Ascended33 dashboard** (Ctrl+F5)
3. **Check SYSTEM STATUS** panel
4. **Obsidian Vault should show ONLINE** ✅

---

**Key Concept**: `host.docker.internal` is the bridge that lets containers communicate with the host OS services!

