# 🚀 HexStrike Claude Workflow — Complete Setup

**Status:** ✅ READY TO USE  
**Last Updated:** 2026-02-20  
**Integration Level:** Full (Desktop + Vault + MCP)

---

## 📋 What's Been Set Up

### 1️⃣ **Desktop Launcher** ✅
- **File:** `HexStrike.lnk` (on your Desktop)
- **What it does:** One-click launch of Docker container + Streamlit UI
- **Ports:**
  - 8001 → HexStrike API backend
  - 8501 → Streamlit web interface
  - 8000 → HackerGPT (if enabled)
  - 9050 → Tor SOCKS5 proxy

### 2️⃣ **Code Fixes Applied** ✅
- **Port mismatch corrected:** Client now connects to 8001 (was 8888)
- **UI errors fixed:**
  - Status display: "HexStrike CONNECTED" ✅
  - Tool retrieval: 150+ tools fallback enabled
  - Server health: Three-state indicator (Healthy/Ready/Initializing)

### 3️⃣ **Documentation Created** ✅
- `LAUNCH_HEXSTRIKE.bat` → Docker orchestration
- `HEXSTRIKE_QUICK_START.txt` → User guide (230 lines)
- `HEXSTRIKE_FIXES_COMPLETED.md` → Technical details (370 lines)
- `HEXSTRIKE_INTEGRATION_SUMMARY.md` → Complete overview (499 lines)
- `DASHBOARD.md` → Added HexStrike section

### 4️⃣ **Vault Integration** ✅
- HexStrike added to DASHBOARD.md
- Cross-linked to KALI_PROJECT and ETHICAL_HACKING_NOTE
- Docker management documented in DOCS/

---

## 🎯 How to Use HexStrike

### **Method 1: Desktop Launcher (Recommended)**
```
1. Double-click HexStrike.lnk on desktop
2. Wait 30-60 seconds for Docker to start
3. Browser automatically opens http://localhost:8501
4. Select tool from dashboard
5. Run investigation/scan
```

### **Method 2: Manual Launch**
```powershell
# From PowerShell in Ascended33 directory
cd D:\Vault\Vault\Ascended33
docker-compose up -d
# Wait 30 seconds, then navigate to http://localhost:8501
```

### **Method 3: Batch File**
```
Double-click LAUNCH_HEXSTRIKE.bat
(Same as Method 1, with verbose output)
```

---

## 🛠️ 150+ Available Tools

### **Reconnaissance (Gathering)**
- nmap, masscan, shodan, censys, hunter.io, dnsdumpster
- whois, dig, host, nslookup, fierce, subfinder, assetfinder

### **Vulnerability Scanning**
- nuclei, nessus, openvas, trivy, grype, container-diff
- bandit (Python), semgrep, sonarqube

### **Web Application Testing**
- burpsuite, owasp-zap, sqlmap, nikto, w3af, acunetix
- wpscan (WordPress), droopescan, joomscan

### **Exploitation Frameworks**
- metasploit, searchsploit, beef, cobalt-strike
- shellcode generators, payload encoders

### **Network Analysis**
- wireshark, tcpdump, netcat, socat, nping
- mtr, iftop, nethogs

### **Malware Analysis**
- cuckoo, yara, volatility, binwalk, radare2, ghidra
- upx, strings, objdump

### **OSINT & Intelligence**
- maltego, shodan, hunter.io, linkedin-enum
- creepy (geolocation), theHarvester

### **Defensive Security**
- snort, suricata, zeek, ossec, osquery
- fail2ban, crowdsec

### **Container & Cloud**
- docker, kubernetes, helm, terraform, cloudmapper
- prowler (AWS auditing)

### **Cryptography**
- hashcat, john-the-ripper, hydra (brute force)
- hashpumpy, rosslin (certificate analysis)

### **And 40+ more specialized tools...**

---

## 📊 Learning Path with HexStrike

### **Phase 1: Reconnaissance (Week 1-2)**
- Learn: nmap, masscan, shodan
- Tasks: Map target infrastructure, enumerate services
- Tools: nmap scripting, service enumeration

### **Phase 2: Vulnerability Discovery (Week 3-4)**
- Learn: nuclei, nessus, burpsuite
- Tasks: Find CVEs, web vulnerabilities
- Tools: Template customization, API integration

### **Phase 3: Exploitation (Week 5-6)**
- Learn: metasploit, searchsploit, SQL injection
- Tasks: Gain access, post-exploitation
- Tools: Custom payloads, lateral movement

### **Phase 4: Advanced (Week 7+)**
- Learn: Custom tool development, automation
- Tasks: Build CI/CD security, advanced persistence
- Tools: Python scripting, full stack integration

**Certifications to target:**
- CEH (Certified Ethical Hacker) → Foundational
- OSCP (Offensive Security Certified Professional) → Advanced
- GPEN (GIAC Penetration Tester) → Industry recognized

---

## 🔍 MCP Integration with Claude

HexStrike is integrated with Claude's MCP server for AI-powered analysis:

### **Trigger Claude Workflows:**
```
"hexstrike : [action]" 
→ Launch investigation with AI enhancement

Examples:
- "hexstrike : scan target 192.168.1.1"
- "hexstrike : analyze results from nuclei scan"
- "hexstrike : generate exploitation report"
```

### **Available MCP Commands:**
- `launch_hexstrike` → Start environment
- `run_tool [name] [args]` → Execute tool
- `analyze_results [output]` → AI analysis
- `generate_report [investigation_id]` → Create PDF

---

## ✅ Verification Checklist

**Before first use:**
- [ ] Desktop shortcut HexStrike.lnk exists
- [ ] LAUNCH_HEXSTRIKE.bat is executable
- [ ] Docker Desktop is installed and running
- [ ] docker-compose.yml configured correctly
- [ ] Port 8001 available (HexStrike backend)
- [ ] Port 8501 available (Streamlit UI)

**After first launch:**
- [ ] Browser opens to http://localhost:8501
- [ ] "HexStrike CONNECTED" appears in header
- [ ] Tool list loads (150+ tools visible)
- [ ] Can select and run a tool
- [ ] Results appear in dashboard

---

## 🐛 Troubleshooting

### **Issue: "HexStrike Offline" or connection refused**
**Solution:**
1. Check Docker Desktop is running
2. Open PowerShell in Ascended33 directory
3. Run: `docker-compose ps`
4. If th3-hexstrike not running, run: `docker-compose up -d`
5. Wait 30 seconds and refresh browser

### **Issue: Port 8501 already in use**
**Solution:**
```powershell
# Find process using port 8501
Get-NetTCPConnection -LocalPort 8501 | Select-Object OwningProcess
# Kill process (replace 12345 with PID)
Stop-Process -Id 12345 -Force
```

### **Issue: Tools not loading**
**Solution:**
1. Check hexstrike_wrapper.py port is 8001
2. Verify in hexstrike_tools.py fallback is active
3. Check firewall isn't blocking localhost:8001
4. Try clearing browser cache (Ctrl+Shift+Delete)

### **Issue: Docker container crashes**
**Solution:**
```powershell
# View logs
docker-compose logs th3-hexstrike
# Rebuild container
docker-compose down
docker-compose up -d --build
```

---

## 🎓 Next Steps (Recommended Order)

1. **Launch HexStrike** using desktop shortcut
2. **Explore UI** — Click through tools, read descriptions
3. **Run first scan** — Try nmap on localhost (safe practice)
4. **Analyze results** — Use HexStrike's analysis features
5. **Read Phase 1 materials** — Start KALI_PROJECT learning path
6. **Setup training environment** — Create VM for safe testing
7. **Begin CTF challenges** — Practice with HackTheBox, TryHackMe
8. **Document findings** — Create investigation notes in Vault

---

## 📚 Related Documentation

- **Main integration:** [[HEXSTRIKE_INTEGRATION_SUMMARY.md]]
- **Quick start:** [[HEXSTRIKE_QUICK_START.txt]]
- **Technical fixes:** [[HEXSTRIKE_FIXES_COMPLETED.md]]
- **Learning path:** [[🐧_KALI_INTEGRATION_PROJECT/README_KALI_PROJECT]]
- **Ethical hacking template:** [[_TEMPLATES/ETHICAL_HACKING_NOTE.md]]
- **Docker management:** [[DOCKER_INTEGRATION_GUIDE.md]]

---

**Ready to launch? Click HexStrike.lnk on your desktop! 🚀**
