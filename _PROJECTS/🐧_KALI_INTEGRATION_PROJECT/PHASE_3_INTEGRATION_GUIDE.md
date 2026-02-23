# 🚀 PHASE 3: PIECES + KALI SYNC — COMPLETE GUIDE

**Date:** 2026-02-18
**Status:** READY TO EXECUTE ✅
**Time to complete:** 10-15 minutes

---

## 📋 What you're getting

```
✅ Automated sync script (KALI_PIECES_SYNC_SCRIPT.py)
✅ SQL injection testing lab
✅ XSS testing environment
✅ Python automation utilities
✅ Complete documentation & index
✅ Quick reference commands
```

---

## 🎯 Step-by-Step Execution

### **STEP 1: Copy script to Kali**

From Windows (or transfer via shared folder):

```bash
# Copy KALI_PIECES_SYNC_SCRIPT.py to Kali VM
# Location: /tmp/claude_workspace/python_scripts/KALI_PIECES_SYNC_SCRIPT.py
```

Or in Kali, download directly:

```bash
# In Kali terminal (with venv activated)
cd /tmp/claude_workspace/python_scripts/
# Paste the script here
```

---

### **STEP 2: Run the sync script**

**In Kali terminal (venv activated):**

```bash
# Navigate to workspace
cd /tmp/claude_workspace

# Run the sync script
python3 python_scripts/KALI_PIECES_SYNC_SCRIPT.py
```

**Expected output:**

```
[2026-02-18 19:00:00] ✅ Verifying environment...
[2026-02-18 19:00:00] ✅ PHASE 1: Setting up directory structure...
[2026-02-18 19:00:01] ✅ PHASE 2: Creating hacking labs...
[2026-02-18 19:00:02] ✅ PHASE 3: Creating Python scripts...
[2026-02-18 19:00:03] ✅ PHASE 4: Creating documentation...

✅ All components ready!
Workspace location: /tmp/claude_workspace
Next step: Copy Pieces snippets to /tmp/claude_workspace/pieces_sync/
```

---

### **STEP 3: Verify structure created**

```bash
# Verify directories
ls -R /tmp/claude_workspace/

# Should show:
# /tmp/claude_workspace/
# ├── pieces_sync/
# │   ├── hacking-exploits/
# │   ├── revenue-prompts/
# │   ├── audit-templates/
# │   └── claude-workflows/
# ├── hacking_labs/
# │   ├── sql-injection-lab/
# │   └── xss-lab/
# └── python_scripts/
#     ├── test_runner.py
#     └── KALI_PIECES_SYNC_SCRIPT.py
```

---

### **STEP 4: Test SQL injection lab**

```bash
# Navigate to SQL injection lab
cd /tmp/claude_workspace/hacking_labs/sql-injection-lab

# Run setup (creates test database)
bash setup.sh

# Expected output:
# [*] Setting up SQL injection lab...
# [+] Database created: /tmp/claude_workspace/hacking_labs/sql-injection-lab/vulnerable.db
# [+] Test credentials:
#     admin / admin123
#     user1 / password1
#     user2 / password2

# Connect to database
sqlite3 vulnerable.db

# Inside sqlite3, test SQL injection:
sqlite> SELECT * FROM users WHERE id=1' OR '1'='1;
# Should return all users (vulnerability demonstrated!)

# Test safe query:
sqlite> SELECT * FROM users WHERE id=1;
# Returns only user with id=1 (correct behavior)
```

---

### **STEP 5: Copy Pieces snippets**

Now that the structure is ready, you need to add your actual Pieces snippets.

**For Hacking Exploits:**
- Copy each snippet from Pieces
- Save as `.sql`, `.js`, or `.txt` files in `/tmp/claude_workspace/pieces_sync/hacking-exploits/`
- Example: `sql-injection-union-based.sql`, `xss-basic.js`

**For Revenue Prompts:**
- Copy each prompt from Pieces
- Save as `.txt` or `.md` files in `/tmp/claude_workspace/pieces_sync/revenue-prompts/`
- Example: `service-ideation-prompt.txt`, `pricing-strategy-prompt.txt`

**For Audit Templates:**
- Copy templates from Pieces
- Save as `.md` or `.html` files in `/tmp/claude_workspace/pieces_sync/audit-templates/`

**For Claude Workflows:**
- Copy automation scripts
- Save as `.py` files in `/tmp/claude_workspace/pieces_sync/claude-workflows/`

---

## 🧪 Testing the integration

### **Run automated tests:**

```bash
# Activate venv first
source /tmp/claude_workspace/venv/bin/activate

# Run test suite
python3 /tmp/claude_workspace/python_scripts/test_runner.py
```

### **Manual SQL injection testing:**

```bash
# Start SQLite with test database
sqlite3 /tmp/claude_workspace/hacking_labs/sql-injection-lab/vulnerable.db

# Try these payloads:
SELECT * FROM users;                          # Normal query
SELECT * FROM users WHERE id=1;               # Safe

SELECT * FROM users WHERE id=1' OR '1'='1;   # VULNERABLE - returns all
SELECT * FROM users WHERE username='admin' -- ; # VULNERABLE - auth bypass
SELECT * FROM users UNION SELECT 1,2,3;      # VULNERABLE - data extraction
```

### **Manual XSS testing:**

```bash
# Open the XSS lab in a browser
firefox /tmp/claude_workspace/hacking_labs/xss-lab/index.html

# Try these payloads in the "Vulnerable" input field:
<script>alert('XSS')</script>
<img src=x onerror=alert('XSS')>
<svg onload=alert('XSS')>

# Notice:
# - Vulnerable version: Payloads execute (red background)
# - Safe version: Payloads displayed as text (green background)
```

---

## 📚 Directory structure created

```
/tmp/claude_workspace/
├── venv/                          # Python virtual environment
├── pieces_sync/                   # Synced Pieces snippets
│   ├── hacking-exploits/          # SQL injection, XSS, XXE, auth bypass
│   ├── revenue-prompts/           # Service ideation, pricing, leads, etc.
│   ├── audit-templates/           # Report templates, checklists
│   ├── claude-workflows/          # Automation scripts
│   └── SYNC_INDEX.md              # Index of all synced items
├── hacking_labs/                  # Learning environments
│   ├── sql-injection-lab/
│   │   ├── setup.sh               # Database setup script
│   │   └── vulnerable.db          # SQLite test database
│   └── xss-lab/
│       └── index.html             # XSS testing playground
└── python_scripts/                # Automation utilities
    ├── test_runner.py             # Automated test suite
    └── KALI_PIECES_SYNC_SCRIPT.py # This sync script

```

---

## ✅ Verification checklist

After running the sync script:

- [ ] All 4 collections directories created
- [ ] SQL injection lab set up (setup.sh exists)
- [ ] XSS lab created (index.html exists)
- [ ] test_runner.py script created
- [ ] SYNC_INDEX.md documentation created
- [ ] Python venv still activated

---

## 🔐 Safety notes

✅ **Safe to run:**
- No system modifications
- No root operations required
- All changes in /tmp (auto-cleanup on reboot)
- Educational purposes only

❌ **Never run these on production:**
- The SQL injection lab is INTENTIONALLY vulnerable
- The XSS lab demonstrates exploits
- Only use for learning in isolated environment

---

## 🚀 Quick reference commands

```bash
# Activate environment
source /tmp/claude_workspace/venv/bin/activate

# Run sync script
python3 /tmp/claude_workspace/python_scripts/KALI_PIECES_SYNC_SCRIPT.py

# Test SQL injection lab
cd /tmp/claude_workspace/hacking_labs/sql-injection-lab
bash setup.sh
sqlite3 vulnerable.db

# Run tests
python3 /tmp/claude_workspace/python_scripts/test_runner.py

# View documentation
cat /tmp/claude_workspace/pieces_sync/SYNC_INDEX.md
cat /tmp/claude_workspace/KALI_INTEGRATION_README.md

# List all synced snippets
find /tmp/claude_workspace/pieces_sync -type f | wc -l

# Clean up (if needed)
rm -rf /tmp/claude_workspace  # WARNING: Deletes everything!
```

---

## 📖 Next Steps (PHASE 4)

Once this Phase 3 is complete, you'll have:

1. ✅ Kali integration complete
2. ✅ Pieces sync structure ready
3. ✅ Learning labs initialized
4. ✅ Python automation framework

**Phase 4 (Coming next):**
- Populate labs with real Pieces snippets
- Run automated tests
- Start Phase 2 OWASP learning
- Document learnings in Vault

---

## 🎓 Learning path after integration

### **Week 1-2: SQL Injection mastery**
1. Understand UNION-based injection
2. Practice on local lab
3. Test against TryHackMe
4. Document walkthrough in Vault

### **Week 2-3: XSS exploitation**
1. Learn DOM-based vs Reflected
2. Practice WAF bypasses
3. Test on PortSwigger Academy
4. Document payloads in Pieces

### **Week 3-4: XXE & other OWASP Top 10**
1. Follow similar pattern
2. Build labs as needed
3. Document learnings

---

## 📝 Support & troubleshooting

**If script fails:**
1. Check venv is activated: `echo $VIRTUAL_ENV`
2. Check workspace exists: `ls -la /tmp/claude_workspace/`
3. Check permissions: `ls -la /tmp/claude_workspace/venv/bin/activate`
4. Run with verbose: `python3 -u KALI_PIECES_SYNC_SCRIPT.py`

**If labs don't work:**
1. Verify setup.sh ran: `ls -la /tmp/claude_workspace/hacking_labs/sql-injection-lab/`
2. Check database created: `file vulnerable.db`
3. Test SQLite: `sqlite3 :memory: "SELECT 1"`

---

## 🎉 Success criteria

Phase 3 is complete when:

- ✅ Script runs without errors
- ✅ All directories created
- ✅ SQL injection lab functional
- ✅ XSS lab accessible
- ✅ Test runner works
- ✅ Documentation in place

---

*Created: 2026-02-18 | Status: PRODUCTION READY | Next: Phase 4 Population*
