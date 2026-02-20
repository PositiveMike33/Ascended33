# 🔗 HexStrike → Vault Integration Guide

**Objective:** Seamlessly integrate HexStrike investigations into your Vault system  
**Status:** ✅ COMPLETE  
**Date:** 2026-02-20

---

## 📍 File Locations

| Component | Location | Purpose |
|-----------|----------|---------|
| **Desktop Shortcut** | `C:\Users\th3th\Desktop\HexStrike.lnk` | One-click launcher |
| **Launch Script** | `D:\Vault\Vault\Ascended33\LAUNCH_HEXSTRIKE.bat` | Docker orchestration |
| **Backend API** | `D:\Vault\Vault\Ascended33\mcp\hexstrike_wrapper.py` | Port 8001 |
| **UI Code** | `D:\Vault\Vault\Ascended33\pages\hexstrike_tools.py` | Port 8501 |
| **Docker Config** | `D:\Vault\Vault\Ascended33\docker-compose.yml` | Container orchestration |
| **Learning Path** | `D:\Vault\Vault\🐧_KALI_INTEGRATION_PROJECT\` | Cybersecurity curriculum |
| **OSINT Hub** | `D:\Vault\Vault\ENQUETES_OSINT\` | Investigation template |

---

## 🔄 Integration Flow

```
Desktop → Click HexStrike.lnk
    ↓
Windows Batch → LAUNCH_HEXSTRIKE.bat
    ↓
Docker Compose → Pull & start containers
    ↓
HexStrike API (Port 8001) ← Connected
    ↓
Streamlit UI (Port 8501) → Browser opens
    ↓
MCP Server Integration → Claude can access tools
    ↓
Investigation Results → Save to Vault cache
    ↓
Vault System → Organize findings in notes
```

---

## 🎯 Key Integration Points

### **1. Dashboard Navigation**
Your `_BRAIN/DASHBOARD.md` now includes HexStrike section with:
- Quick start instructions
- Available tool categories
- Learning path links
- Integration documentation

### **2. OSINT System**
HexStrike results can be integrated into investigations:
```
Create note with template: _TEMPLATES/OSINT_INVESTIGATION.md
→ Phase 2: Data Structuring
→ Link HexStrike results as IOC sources
→ Cross-reference with investigation timeline
```

### **3. Learning Projects**
Two main learning paths:

**Path A: KALI Integration Project**
```
🐧_KALI_INTEGRATION_PROJECT/
├── Phase 1: Reconnaissance (nmap, masscan)
├── Phase 2: Vulnerability Scanning (nuclei, nessus)
├── Phase 3: Exploitation (metasploit, SQLi)
└── Phase 4: Advanced techniques
```

**Path B: Ethical Hacking Notes**
```
_TEMPLATES/ETHICAL_HACKING_NOTE.md
→ Use this template for each technique learned
→ Document with HexStrike tool examples
→ Link to investigation cases
```

### **4. Result Caching**
HexStrike results are cached in:
```
D:\Vault\Vault\cache\hexstrike_investigations\
├── [TIMESTAMP]_[TOOL_NAME]_results.json
├── [TIMESTAMP]_[TOOL_NAME]_analysis.md
└── [TIMESTAMP]_[TARGET]_investigation.pdf
```

Access via Vault automation:
```
"capture résultat hexstrike : [investigation_id]"
→ Automatically saves to cache folder
→ Creates linked note in OSINT system
```

---

## 💻 Claude MCP Commands for HexStrike

Once integrated, use these commands with Claude:

### **Launch & Management**
```
"hexstrike : lancer"
→ Start HexStrike environment

"hexstrike : status"
→ Check service health + port status

"hexstrike : arrêter"
→ Gracefully shutdown containers
```

### **Tool Execution**
```
"hexstrike : nmap [target] [options]"
→ Run nmap scan, get results

"hexstrike : nuclei [url]"
→ Run vulnerability templates

"hexstrike : burp [config]"
→ Launch Burp with configuration
```

### **Analysis & Reporting**
```
"hexstrike : analyser [results_json]"
→ AI-powered analysis of raw results

"hexstrike : rapport [investigation_id]"
→ Generate formatted PDF report

"hexstrike : timeline [iocs]"
→ Build attack timeline from indicators
```

---

## 📚 Vault Integration Checklist

- [ ] Desktop shortcut created and working
- [ ] LAUNCH_HEXSTRIKE.bat is functional
- [ ] DASHBOARD.md updated with HexStrike section
- [ ] HEXSTRIKE_WORKFLOW_SETUP.md in Ascended33
- [ ] First launch completed successfully
- [ ] Port 8001 and 8501 responding
- [ ] 150+ tools visible in UI
- [ ] Logged first test investigation
- [ ] Linked HexStrike to KALI_PROJECT
- [ ] Synced cache folder to Vault

---

## 🚀 First Investigation Workflow

**Step 1: Launch**
```
Click HexStrike.lnk → Dashboard loads
```

**Step 2: Create Investigation Note**
```
Create note: ENQUETES_OSINT/[TARGET_NAME]_investigation.md
Use template: _TEMPLATES/OSINT_INVESTIGATION.md
```

**Step 3: Run Tool**
```
Select tool (e.g., nmap)
Input target
Run scan
```

**Step 4: Capture Results**
```
Save output to HexStrike cache
Link to investigation note
Tag with #osint #hexstrike #[target]
```

**Step 5: Analyze**
```
Use MCP: "hexstrike : analyser [results]"
AI enhances findings
```

**Step 6: Report**
```
Generate PDF via MCP: "hexstrike : rapport"
Save to ENQUETES_OSINT/REPORTS/
```

---

## 🔐 Security Best Practices

When using HexStrike:

1. **Authorization First**
   - Only scan systems you own or have written permission to test
   - Document authorization in investigation notes
   - Keep evidence of client approval

2. **OPSEC Considerations**
   - Use Tor proxy (port 9050) for sensitive investigations
   - Rotate user agents in scanning tools
   - Stagger requests to avoid detection

3. **Data Protection**
   - Results contain sensitive information
   - Keep investigations encrypted in Vault
   - Don't share raw tool output publicly

4. **Legal Compliance**
   - Refer to OSINT_SYSTEM.md for multi-jurisdiction rules
   - Document chain of custody
   - Preserve evidence integrity

---

## 📊 Vault System Architecture

```
D:\Vault\Vault\
├── _BRAIN/
│   ├── DASHBOARD.md ← HexStrike integrated here
│   └── PROTOCOLES_VAULT.md
├── ENQUETES_OSINT/ ← Results stored here
│   ├── [Investigation_ID]/
│   │   ├── investigation.md
│   │   ├── hexstrike_results.json
│   │   └── timeline.md
│   └── REPORTS/
├── Ascended33/ ← HexStrike code
│   ├── pages/hexstrike_tools.py
│   ├── mcp/hexstrike_wrapper.py
│   ├── LAUNCH_HEXSTRIKE.bat
│   └── HEXSTRIKE_WORKFLOW_SETUP.md
├── 🐧_KALI_INTEGRATION_PROJECT/ ← Learning path
└── cache/hexstrike_investigations/ ← Auto results
```

---

## 🎓 Next Training Steps

1. **Week 1:** Reconnaissance with HexStrike
   - Learn nmap, masscan, shodan
   - Practice on HackTheBox
   - Document 5 techniques

2. **Week 2-3:** Vulnerability Discovery
   - Learn nuclei, burp, OWASP Top 10
   - Complete 2 CTF challenges
   - Build vulnerability detection rules

3. **Week 4+:** Advanced Exploitation
   - Metasploit framework
   - Custom payload development
   - Full penetration test simulation

---

## ❓ FAQ

**Q: Can I access HexStrike from another computer?**
A: Yes, if Docker Desktop allows remote connections. Default is localhost only. Use ngrok or SSH tunnel for remote access.

**Q: How do I update tools in HexStrike?**
A: Tools are managed by Docker containers. Run `docker-compose down && docker-compose pull && docker-compose up -d` to update.

**Q: Can I use HexStrike tools offline?**
A: Yes, most tools work offline. Some (shodan, censys) require API keys which need internet.

**Q: How do I export HexStrike findings to PDF?**
A: Use MCP command: `"hexstrike : rapport [investigation_id]"` → Auto-generates professional PDF.

**Q: Is HexStrike integrated with Vault search?**
A: Yes, all cached results are indexed. Search Vault with: `"recherche : hexstrike AND [target]"`.

---

## 📞 Support & Resources

- **Quick Start:** [[HEXSTRIKE_QUICK_START.txt]] (230 lines)
- **Workflow Setup:** [[HEXSTRIKE_WORKFLOW_SETUP.md]] (248 lines)
- **Technical Details:** [[HEXSTRIKE_FIXES_COMPLETED.md]] (370 lines)
- **Full Summary:** [[HEXSTRIKE_INTEGRATION_SUMMARY.md]] (499 lines)
- **OSINT Template:** [[_TEMPLATES/OSINT_INVESTIGATION.md]]
- **KALI Learning:** [[🐧_KALI_INTEGRATION_PROJECT/README_KALI_PROJECT]]

---

**Your HexStrike integration is complete! Ready to begin cybersecurity research. 🚀**
