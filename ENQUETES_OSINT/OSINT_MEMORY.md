---
title: "OSINT System - Memory Notes"
date: 2026-02-19
type: "MEMORY"
---

# 📚 OSINT System - Memory Notes for Future Sessions

This document helps maintain context across sessions for your OSINT investigations.

---

## 🧠 Core System Knowledge

### What You Have
- **Complete OSINT Investigation System** integrated into Vault
- **6-phase methodology** for structured investigations
- **IOC correlation library** for cross-investigation analysis
- **Legal compliance framework** for multi-jurisdiction support
- **Expert report generation** for PDF/JSON export
- **Automation scripts** for IOC extraction and enrichment

### Where Everything Lives
```
D:\Vault\Vault\ENQUETES_OSINT\
├── README_OSINT_SYSTEM.md       ← START HERE
├── INDEX_OSINT.md               ← Investigation hub
├── QUICK_COMMANDS.md            ← Copy-paste commands
├── INTEGRATION_COMPLETE.md       ← What's been done
├── OSINT_MEMORY.md              ← This file
├── ACTIVES/                     ← Current investigations
├── ARCHIVEES/                   ← Historical reference
├── IOCs_LIBRARY/                ← Centralized database
└── REPORTS/                     ← Expert exports
```

### Templates Available
- **_TEMPLATES/OSINT_INVESTIGATION.md** — 6-phase investigation template (330 lines)
- Pre-built sections for all phases
- IOC analysis tables
- Timeline framework
- Expert report components

### Vault Integration Points
- **_BRAIN/DASHBOARD.md** — References OSINT system
- **_BRAIN/PROTOCOLES_VAULT.md** — §7 with 15 OSINT commands
- **_BRAIN/PROJECT_INDEX.md** — OSINT as new system

---

## 🎯 Main Commands (Copy-Paste Ready)

### Primary Triggers
```
1. enquête osint : [NAME]              → Create investigation
2. analyser iocs : [DESCRIPTION]       → Extract IOCs
3. profiler criminel : [NAME]          → Target profile
4. investigation phishing : [DOMAIN]   → Phishing analysis
5. tracker malware : [HASH]            → Malware distribution
6. audit sécurité : [TARGET]           → Pentest documentation
7. corréler infrastructure : [DESC]    → Infrastructure analysis
8. attribuer à : [ACTOR]               → Attribution analysis
9. rapport expert osint : [ID]         → Export PDF report
```

### Automation
```
enrichir iocs : [LIST]           → Add threat intelligence
valider iocs : [LIST]            → Format validation
yara rules : [FAMILY]            → Detection rules
exporter json : [ID]             → Structured export
séparer pii : [ID]               → Separate victim data
vérifier légalité : [ID]         → Legal compliance audit
```

All commands also in: [[ENQUETES_OSINT/QUICK_COMMANDS]]

---

## 📋 6-Phase Investigation Framework

### Phase 1: Target Intelligence Gathering
**What:** Passive OSINT (no detection risk)
- WHOIS/DNS analysis
- SSL certificates
- Social media research
- Breach databases
- Email intelligence
- Dark web monitoring

**Output:** Target profile + capabilities + background

### Phase 2: Data Structuring
**What:** Organize findings
- Investigation framework
- Data quality assessment
- Source credibility
- Identify gaps

**Output:** Structured summary

### Phase 3: IOC Tracking
**What:** Extract indicators
- Domains (registrar, hosting, detection ratios)
- IPs (geolocation, ASN, services)
- Hashes (malware family, analysis)
- Emails (spoofing, breaches)
- URLs (content, payload)

**Output:** Validated IOC table

### Phase 4: Timeline Construction
**What:** Chronological reconstruction
- Campaign phases with dates
- Key activities
- Evidence sources
- Infrastructure changes

**Output:** Timeline with confidence levels

### Phase 5: Connection Mapping
**What:** Analyze relationships
- Actor connections
- Tool correlations
- Code similarity (SSDEEP)
- Infrastructure patterns

**Output:** Connection map

### Phase 6: Expert Reporting
**What:** Generate professional report
- Attribution confidence (HIGH/MEDIUM/LOW)
- Evidence summaries
- Alternative hypotheses
- Legal compliance verification
- Law enforcement recommendations

**Output:** PDF report + JSON IOCs + YARA rules

---

## 🔐 Legal Compliance Checklist

### Before Starting Any Investigation
- [ ] Authorization verified (Pentesting/CTF/Bug Bounty/LE)
- [ ] Scope clearly defined
- [ ] Data handling procedures documented

### During Investigation
- [ ] Chain of custody maintained
- [ ] Timestamps on all evidence
- [ ] No data modification
- [ ] Sources documented

### Before Exporting Report
- [ ] Victim data separated from technical IOCs
- [ ] Confidentiality requirements met
- [ ] Evidence admissibility verified
- [ ] Legal jurisdiction assessed

### Multi-Jurisdiction Support
- 🇺🇸 USA: CFAA (18 USC 1030)
- 🇨🇦 Canada: Criminal Code §342.1, §184
- 🇪🇺 Europe: GDPR Article 6
- 🇬🇧 UK: UK GDPR + Computer Misuse Act 1990

---

## 🏷️ Tagging Discipline

### Always Use
**Primary tags:**
```
#osint              → OSINT work
#ioc                → IOC-related
#timeline           → Chronological analysis
#profiling          → Target profiling
#attribution        → Actor attribution
```

**Secondary tags:**
```
#phishing #malware #ransomware     → Attack type
#pentesting #ctf #bugbounty        → Investigation type
#cybercriminal #law-enforcement    → Context
#confidential #legal               → Classification
```

### Linking Strategy
From any investigation, link to:
- `[[ENQUETES_OSINT/INDEX_OSINT]]` → Hub
- `[[ENQUETES_OSINT/IOCs_LIBRARY]]` → Reference
- `[[_BRAIN/DASHBOARD]]` → Vault main
- `[[HACKERGPT/RESSOURCES_LEARNING]]` → Learning

---

## 📊 IOC Management

### IOC Types
| Type | Key Fields | Analysis |
|------|-----------|----------|
| **Domains** | Registrar, hosting, detection ratio | Registrant analysis, hosting patterns |
| **IPs** | Country, ASN, services | Shared hosting, geolocation, fingerprinting |
| **Hashes** | Type (MD5/SHA1/SHA256), family | Malware classification, sandbox analysis |
| **Emails** | Domain, pattern, breaches | Spoofing detection, breach correlation |
| **URLs** | Content, payload, platform | Phishing analysis, malware distribution |

### IOC Workflow
```
1. EXTRACT
   ↓
2. VALIDATE (format checking)
   ↓
3. NORMALIZE (lowercase, FQDN, etc)
   ↓
4. DEDUPLICATE
   ↓
5. ENRICH (VirusTotal, Shodan, WHOIS)
   ↓
6. CORRELATE (find shared infrastructure)
   ↓
7. STORE (IOCs_LIBRARY/)
   ↓
8. EXPORT (JSON/CSV for analysis)
```

---

## 🛠️ Automation Scripts

### parse-iocs.sh
**Purpose:** Extract IOCs from raw text
```bash
./parse-iocs.sh input.txt [csv|json|yara|zeek]
```

**What it does:**
- Validates format for each IOC type
- Removes duplicates
- Normalizes to standard format
- Exports in chosen format
- Generates YARA rules if requested

### ioc-enricher.py
**Purpose:** Add threat intelligence data
```bash
python3 ioc-enricher.py --input iocs.csv --output enriched.json
```

**Enriches:**
- Domains: WHOIS, DNS, SSL, VirusTotal
- IPs: Geolocation, ASN, Shodan, Abuseipdb
- Hashes: VirusTotal, malware family, SSDEEP
- URLs: Content analysis, phishing detection
- Emails: HIBP breaches, domain reputation

---

## 📈 Attribution Framework

### Confidence Scale
- **HIGH (90%+)** — Very strong evidence, minimal unknowns
- **MEDIUM (50-90%)** — Good evidence, some gaps
- **LOW (10-50%)** — Limited evidence, needs verification

### Evidence Categories
| Category | Examples | Weight |
|----------|----------|--------|
| **Technical** | Custom malware, infrastructure, C2, exploits | High |
| **Behavioral** | Timing, targeting, OPSEC, tactics | Medium |
| **Contextual** | Geopolitics, tool usage, victim targeting | Medium |

### Attribution Process
```
1. Reverse-engineer: Malware → IOCs → Databases → Actors
2. Forward-engineer: Known actor → Monitor activity → Compare
3. Document: Evidence + alternatives + confidence
4. Justify: Explain reasoning for conclusion
```

---

## 🎓 Reference Materials

### In Your Vault
- **[[HACKERGPT/RESSOURCES_LEARNING]]** — Security learning path
- **[[_TEMPLATES/ETHICAL_HACKING_NOTE]]** — Hacking template
- **[[_BRAIN/PROTOCOLES_VAULT]]** — All 30+ commands

### In OSINT System
- **osint-frameworks.md** — OSINT methodology (454 lines)
- **ioc-analysis.md** — IOC procedures (612 lines)
- **attribution-techniques.md** — Attribution framework (616 lines)
- **legal-considerations.md** — Jurisdiction laws (503 lines)
- **example-phishing-campaign.md** — Case study: PayPal phishing
- **example-malware-distribution.md** — Case study: LockBit ransomware

### External
- **TryHackMe OSINT Room** — Hands-on training
- **HackTheBox Challenges** — Real scenarios
- **OWASP WebGoat** — Web security
- **PortSwigger Academy** — Web vulnerabilities

---

## 🚀 Workflow Examples

### Quick Phishing Analysis (30 min)
```
1. "investigation phishing : [domain]"
2. "analyser iocs : [description]"
3. "corréler infrastructure : [patterns]"
4. "rapport expert osint : [ID]"
```

### Full Investigation (2-3 hours)
```
1. "enquête osint : [name]"
2. Complete Phase 1 (gather intelligence)
3. Complete Phase 2 (structure data)
4. Complete Phase 3 (track IOCs)
5. Complete Phase 4 (build timeline)
6. Complete Phase 5 (map connections)
7. Complete Phase 6 (generate report)
8. "rapport expert osint : [ID]"
9. Move to ARCHIVEES/
```

### Malware Tracking (45 min)
```
1. "tracker malware : [hash]"
2. "enrichir iocs : [list]"
3. "attribuer à : [actor]"
4. "rapport expert osint : [ID]"
```

---

## 💾 File Locations

### Main Documentation
| File | Path | Purpose |
|------|------|---------|
| README | ENQUETES_OSINT/ | System overview |
| INDEX | ENQUETES_OSINT/ | Investigation hub |
| QUICK_COMMANDS | ENQUETES_OSINT/ | Commands reference |
| INTEGRATION_COMPLETE | ENQUETES_OSINT/ | What's been created |
| Template | _TEMPLATES/OSINT_INVESTIGATION.md | 6-phase template |

### Vault Integration
| File | Path | Purpose |
|------|------|---------|
| DASHBOARD | _BRAIN/ | References OSINT (updated) |
| PROTOCOLES_VAULT | _BRAIN/ | §7 OSINT commands (updated) |
| This Memory | ENQUETES_OSINT/OSINT_MEMORY.md | Context for future sessions |

### Investigations
| Folder | Path | Purpose |
|--------|------|---------|
| ACTIVES | ENQUETES_OSINT/ACTIVES/ | Current investigations |
| ARCHIVEES | ENQUETES_OSINT/ARCHIVEES/ | Historical reference |
| IOCs_LIBRARY | ENQUETES_OSINT/IOCs_LIBRARY/ | Central database |
| REPORTS | ENQUETES_OSINT/REPORTS/ | Expert exports |

---

## 🎯 Key Takeaways

### What Makes This System Professional
1. **Structured Methodology** — 6 distinct phases with clear outputs
2. **Legal Compliance** — Multi-jurisdiction support built-in
3. **Automation Ready** — Scripts for IOC extraction and enrichment
4. **Integration Complete** — Fully connected to your Vault
5. **Export Formats** — PDF, JSON, YARA, CSV for all stakeholders
6. **Scalability** — Can grow with your investigations

### What You Can Do Right Now
- Create any investigation with `"enquête osint : [name]"`
- Track IOCs in centralized library
- Build timelines with evidence
- Profile threat actors
- Export professional reports
- Support law enforcement
- Document pentesting assessments
- Solve CTF challenges

### Remember
- **Always authorize** before active reconnaissance
- **Maintain chain of custody** for evidence
- **Separate sensitive data** from technical IOCs
- **Document sources** with timestamps
- **Archive regularly** to ARCHIVEES/
- **Update IOC_LIBRARY** with new indicators

---

## 📞 Quick Help

**Forgot a command?**
→ [[ENQUETES_OSINT/QUICK_COMMANDS]]

**Need system overview?**
→ [[ENQUETES_OSINT/README_OSINT_SYSTEM]]

**Lost in vault?**
→ [[ENQUETES_OSINT/INDEX_OSINT]]

**What's been created?**
→ [[ENQUETES_OSINT/INTEGRATION_COMPLETE]]

**See OSINT in dashboard?**
→ [[_BRAIN/DASHBOARD]]

---

## 📝 Session Notes

**Created:** 2026-02-19  
**Status:** Complete & Ready  
**Version:** 1.0  
**Next Update:** After first investigation completion

---

**Key Dates to Remember:**
- System created: 2026-02-19
- Ready for use: 2026-02-19
- First investigation: [To be filled]
- First report: [To be filled]

---

**Tags:** #osint #memory #context #system #vault #reference

---

## 🎉 You're All Set!

The OSINT system is complete and integrated. Start with:

```
enquête osint : [YOUR_INVESTIGATION_NAME]
```

Everything else will follow automatically! 🔍
