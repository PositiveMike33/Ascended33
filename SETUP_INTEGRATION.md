# 🚀 Ascended33 ↔ Obsidian Vault Integration Setup Guide

**Status**: Configuration file created ✅  
**Next**: Complete authentication and test connectivity

---

## Quick Setup (5 minutes)

### Step 1: Get Obsidian API Key (2 minutes)

1. **Open Obsidian** on your Windows machine (the one with D:\Vault\Vault)
2. Go to **Settings** → **Community plugins**
3. Find **"Local REST API"** plugin
4. Click **Settings** icon for the plugin
5. Copy the **API Key** (long string starting with `obs_`)
6. Open `D:\Vault\Vault\Ascended33\config\config.yaml`
7. Paste the key after `api_key: ` on line 9:
   ```yaml
   api_key: "obs_YOUR_COPIED_KEY_HERE"
   ```
8. **Save the file**

### Step 2: Test Vault Connectivity (2 minutes)

Open PowerShell in `D:\Vault\Vault\Ascended33\` and run:

```powershell
python verify_connections.py
```

Expected output:
```
[INFO] Obsidian REST API at localhost:27123... [PASS]
[INFO] Test write note to Vault... [PASS]
[INFO] hexstrike-ai at localhost:8888... [FAIL] (expected if not running)
[INFO] SSH connection to Kali VM... [FAIL] (expected if SSH not set up yet)
```

✅ **If Obsidian tests pass, integration is working!**

### Step 3: Verify Vault Note Creation (1 minute)

After running `verify_connections.py`, check Obsidian:
- Look for new folder: `Claude-Michael/Sessions/`
- Look for new file: `_connection_test.md`
- If it exists with content "Ascended33 connected successfully" → **YOU'RE GOOD!**

---

## Full Setup (for Kali Integration)

### Step 4: Configure Kali SSH (if using Kali VM)

**On your Kali Linux VM**:

```bash
# Generate SSH key if you don't have one
ssh-keygen -t rsa -b 4096 -f ~/.ssh/kali_lab_key -N ""

# Get your Kali IP address
hostname -I
# Output: 192.168.x.x (remember this)
```

**On Windows** (update config.yaml):

```yaml
kali_vm:
  host: "192.168.x.x"                # Replace with your Kali IP
  user: "kali"
  key_file: "~/.ssh/kali_lab_key"   # If Windows SSH is configured
```

Or use Windows 10/11 built-in SSH:
- Copy Kali public key to Windows: `~/.ssh/authorized_keys`
- Update `key_file` path

### Step 5: Start hexstrike-ai on Kali

**On Kali VM**:

```bash
cd ~/hexstrike-ai
python3 hexstrike_server.py
# Should output: "MCP Server running at http://localhost:8888"
```

### Step 6: Run Full Verification

```powershell
python verify_connections.py
```

Expected output (all systems):
```
[PASS] Obsidian REST API at localhost:27123
[PASS] Test write note to Vault
[PASS] hexstrike-ai at localhost:8888
[PASS] SSH connection to Kali VM
[PASS] hexstrike-ai running on Kali VM
[PASS] nmap installed on Kali
[PASS] Get Kali IP address

All 7 checks passed — Ascended33 fully operational!
```

---

## Testing the Integration

### Test 1: Create a Test Note from Dashboard

```powershell
cd D:\Vault\Vault\Ascended33
streamlit run streamlit_app.py
```

Open browser → http://localhost:8501

**Expected**:
- Dashboard loads with dark theme
- Status panel shows "Obsidian: ONLINE" (green)
- No errors in console

### Test 2: Manual Note Creation

```powershell
python -c "
from vault_sync.vault_api import ObsidianVaultClient
from vault_sync.note_builder import NoteBuilder

vault = ObsidianVaultClient.from_config()
note = NoteBuilder.security_note(
    title='Integration Test — example.com',
    target='example.com',
    note_type='osint',
    body='## Test\\nThis note was created via Python integration.\\n',
    tags=['osint', 'test', '2026'],
    severity='Low'
)
vault.create_note('HACKERGPT/OSINT_Profilage/2026-02-19-integration-test.md', note)
print('✅ Note created successfully!')
"
```

**Check Obsidian**:
- Open vault folder in Obsidian
- Navigate to: `HACKERGPT/OSINT_Profilage/`
- Look for `2026-02-19-integration-test.md`
- Verify frontmatter is parsed correctly

### Test 3: Vault Search

```powershell
python -c "
from vault_sync.sync import VaultSync

sync = VaultSync()
results = sync.search_notes('integration')
for result in results:
    print(f'  📄 {result.path}')
    print(f'     Tags: {result.tags}')
"
```

---

## Architecture After Setup

```
┌─────────────────────────────────────────┐
│   Ascended33 Dashboard (Streamlit)      │
│   http://localhost:8501                 │
└──────────────────┬──────────────────────┘
                   │
        ┌──────────┼──────────┐
        ▼          ▼          ▼
   ┌────────┐ ┌────────┐ ┌────────┐
   │ Vault  │ │hexstrike│ │ OPSEC  │
   │ Sync   │ │ MCP    │ │ Check  │
   └───┬────┘ └───┬────┘ └────────┘
       │          │
       ▼          ▼
   ┌──────────────────────────────────┐
   │    Obsidian Vault (D:\Vault)     │
   │    REST API :27123               │
   │                                  │
   │  HACKERGPT/                      │
   │  ├── OSINT_Profilage/      ◄──┐  │
   │  ├── HEXSTRIKE/            ◄──┤  │
   │  └── CTF/                  ◄──┤  │
   │                                │  │
   │  ENQUETES_OSINT/           ◄──┤  │
   │  Claude-Michael/Sessions/  ◄──┘  │
   │                                  │
   └──────────────────────────────────┘
```

---

## Workflow: OSINT → Vault

```
User clicks "Launch OSINT" in Ascended33
         ↓
Dashboard calls hexstrike-ai API
         ↓
hexstrike finds: domains, IPs, emails, etc.
         ↓
NoteBuilder structures findings with metadata
         ↓
VaultSync pushes to Obsidian via REST API
         ↓
Note appears in Vault with:
  • YAML frontmatter (date, type, severity, tags)
  • Wikilinks for cross-references
  • Section headings (Findings, Analysis, etc.)
  • Related note backlinks
         ↓
Claude can now reference findings in future sessions
         ↓
Vault index auto-updates for search/filtering
```

---

## Troubleshooting

### "Cannot reach Obsidian REST API"

**Check**:
1. Is Obsidian running? (look for window)
2. Is Local REST API plugin enabled? (Settings → Community plugins)
3. Check API key is correct in `config.yaml`

**Fix**:
```powershell
# Test direct connection
curl http://localhost:27123/
# Should return HTML (not "Connection refused")
```

### "SSH connection failed to Kali"

**Check**:
1. Is Kali VM running?
2. Is SSH service running on Kali? `sudo systemctl start ssh`
3. Is IP address correct in `config.yaml`?
4. Can you ping Kali? `ping 192.168.x.x`

**Fix**:
```bash
# On Kali
sudo systemctl enable ssh
sudo systemctl start ssh
hostname -I  # Get correct IP
```

### "hexstrike-ai not responding"

**Check**:
1. Is hexstrike-ai running on Kali? `ps aux | grep hexstrike`
2. Is it on correct port 8888?
3. Can you reach it from Windows? `curl http://kali-ip:8888/`

**Fix**:
```bash
# On Kali
cd ~/hexstrike-ai
python3 hexstrike_server.py
# Wait for "MCP Server running..." message
```

---

## Configuration File Reference

**Location**: `D:\Vault\Vault\Ascended33\config\config.yaml`

```yaml
vault:
  mode: "rest_api"                   # Use REST API (better than filesystem)
  base_url: "http://localhost:27123" # Obsidian REST API endpoint
  api_key: "obs_..."                 # Get from Obsidian settings
  vault_path: "D:/Vault"             # Fallback for filesystem mode

hexstrike:
  mcp_url: "http://localhost:8888"   # hexstrike-ai MCP server
  timeout_seconds: 30                # Request timeout

kali_vm:
  host: "192.168.x.x"                # Your Kali IP
  user: "kali"                       # SSH username
  key_file: "~/.ssh/kali_lab_key"    # SSH private key
  mcp_port: 8888                     # hexstrike-ai port on Kali

opsec:
  require_vpn: true                  # Enforce VPN for operations
  require_tor_for_darkweb: true      # Require TOR for dark web
  vpn_check_url: "..."               # TOR project check API

reporting:
  default_output: "vault"            # Save findings to Vault
  local_output_dir: "./output/"      # Fallback local directory
  vault_base_path: "HACKERGPT"       # Root folder for findings
```

---

## Files Modified/Created

| File | Status | Purpose |
|------|--------|---------|
| `config/config.yaml` | ✅ Created | Main configuration file |
| `INTEGRATION_VERIFICATION_REPORT.md` | ✅ Created | Comprehensive analysis |
| `verify_connections.py` | ✅ Existing | Connection test script |
| `SETUP_INTEGRATION.md` | ✅ Created | This guide |

---

## Next Steps

1. **Get API key** from Obsidian Local REST API plugin
2. **Update config.yaml** with the API key
3. **Run `verify_connections.py`** to test
4. **Check Obsidian** for connection test note
5. **(Optional) Set up Kali** for hexstrike-ai integration
6. **Launch dashboard**: `streamlit run streamlit_app.py`

---

**You're ready to integrate hexstrike-ai findings into your Obsidian knowledge base!** 🎯

For detailed technical information, see: `INTEGRATION_VERIFICATION_REPORT.md`