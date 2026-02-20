---
title: "OSINT Intelligence System - README"
date: 2026-02-19
status: ACTIVE
version: 1.0
---

# 🔍 OSINT Intelligence System — README

**Professional Open Source Intelligence investigations integrated with your Vault**

Welcome to your OSINT investigation system! This is your **virtual brain** for managing authorized security investigations including pentesting, CTF challenges, bug bounty work, and law enforcement coordination against cybercriminals.

---

## 🎯 What You Can Do

✅ **Pentesting Engagements** — Document authorized security assessments  
✅ **CTF Challenges** — Solve and document walkthroughs  
✅ **Bug Bounty Research** — Track vulnerabilities and impact analysis  
✅ **Malware Investigations** — Track distribution, C2, victims  
✅ **Phishing Campaigns** — Analyze email infrastructure and IOCs  
✅ **Ransomware Tracking** — Profile gangs, infrastructure, victims  
✅ **Law Enforcement Support** — Create expert reports for authorities  
✅ **Criminal Profiling** — Build threat actor profiles with TTPs  

---

## 📁 System Structure

```
ENQUETES_OSINT/
├── README_OSINT_SYSTEM.md          ← You are here
├── INDEX_OSINT.md                  ← Hub for all investigations
├── QUICK_COMMANDS.md               ← Copy-paste commands for Claude
│
├── ACTIVES/                        ← Currently active investigations
│   ├── [OSI-2026-001]/
│   │   ├── investigation.md        (OSINT_INVESTIGATION template)
│   │   ├── iocs.json              (Extracted & enriched IOCs)
│   │   └── timeline.md            (Chronological events)
│   └── [OSI-2026-002]/
│       └── ...
│
├── ARCHIVEES/                      ← Closed investigations (reference)
│   ├── [OSI-2025-001]/
│   │   ├── investigation_final.md
│   │   ├── expert_report.pdf
│   │   └── iocs_final.json
│   └── [OSI-2025-002]/
│       └── ...
│
├── IOCs_LIBRARY/                   ← Central IOC correlation database
│   ├── all_iocs_enriched.json     (Master IOC list)
│   ├── infrastructure_map.csv     (IP/Domain clustering)
│   ├── malware_hashes.txt         (SHA256 list)
│   └── threat_actors.json         (Known actors + TTPs)
│
└── REPORTS/                        ← Expert reports for export
    ├── 2026-02/
    │   ├── OSI-2026-001_expert_report.pdf
    │   └── OSI-2026-001_iocs_export.json
    └── 2026-01/
        └── ...
```

---

## 🚀 Quick Start (5 minutes)

### Step 1: Understand the system (2 min)
Read: [[ENQUETES_OSINT/INDEX_OSINT]]

### Step 2: Learn commands (1 min)
See: [[ENQUETES_OSINT/QUICK_COMMANDS]]

### Step 3: Start your first investigation (2 min)
Pick a command and tell Claude:

```
enquête osint : [YOUR_INVESTIGATION_NAME]
```

**Examples:**
```
enquête osint : Emotet phishing campaign
enquête osint : LockBit ransomware distribution
enquête osint : PayPal domain spoofing
```

That's it! Claude will create a complete `OSINT_INVESTIGATION.md` template with all 6 phases.

---

## 🔄 Investigation Workflow

### Phase 1: Target Intelligence Gathering
**Passive OSINT** (no detection risk)
- WHOIS/DNS lookups
- SSL certificate analysis
- Social media research
- Public breach databases
- Email intelligence
- Dark web monitoring

**Output:** Target profile + background + capabilities

### Phase 2: Data Structuring
**Organize findings**
- Create investigation framework
- Data quality assessment
- Source credibility evaluation
- Identify gaps

**Output:** Structured intelligence summary

### Phase 3: IOC Tracking
**Extract & analyze indicators**
- Domains (registrar, hosting, detection ratios)
- IP addresses (geolocation, ASN, services)
- File hashes (malware family, analysis)
- Email addresses (spoofing, breaches)
- URLs (content, payload)

**Output:** Validated IOC table with enrichment data

### Phase 4: Timeline Construction
**Reconstruct chronologically**
- Campaign phases with dates
- Key activities
- Evidence sources (timestamps)
- Infrastructure changes

**Output:** Chronological timeline with confidence levels

### Phase 5: Connection Mapping
**Analyze relationships**
- Relationship matrix
- Actor connections
- Tool/malware correlations
- Code similarity (SSDEEP)

**Output:** Visual connection map

### Phase 6: Expert Reporting
**Generate professional report**
- Attribution assessment (HIGH/MEDIUM/LOW confidence)
- Evidence summaries (technical/behavioral/contextual)
- Alternative hypotheses
- Legal compliance verification
- Recommendations for LE/IR

**Output:** PDF expert report + structured IOC export

---

## ⚡ Common Commands

### For Phishing Investigations
```
investigation phishing : [DOMAIN]
```
→ Email header analysis + IOC extraction + victim count

### For Malware Tracking
```
tracker malware : [HASH_OR_FAMILY]
```
→ C2 infrastructure + distribution + victims + attribution

### For Target Profiling
```
profiler criminel : [NAME_OR_ALIAS]
```
→ Background + capabilities + TTPs + known infrastructure

### For IOC Analysis
```
analyser iocs : [DESCRIPTION]
```
→ Extraction + validation + normalization + enrichment

### For Expert Reports
```
rapport expert osint : [INVESTIGATION_ID]
```
→ PDF export with legal compliance + evidence chain

See full list: [[ENQUETES_OSINT/QUICK_COMMANDS]]

---

## 🛠️ Automation Scripts

### Parse IOCs from raw data
```bash
cd /path/to/scripts
./parse-iocs.sh input_file.txt [csv|json|yara|zeek]
```
**Output:** Validated, normalized IOCs in chosen format

**Features:**
- Format validation (domains, IPs, hashes, emails, URLs)
- Deduplication
- Normalization (lowercase, standard format)
- YARA rule generation
- Zeek intelligence framework export

### Enrich IOCs with threat intelligence
```bash
python3 ioc-enricher.py --input iocs.csv --output enriched.json
```
**Output:** IOCs with enrichment data (VirusTotal, Shodan, WHOIS, etc.)

**Features:**
- Domain enrichment (WHOIS, DNS, SSL, VirusTotal)
- IP enrichment (geolocation, ASN, Shodan, Abuseipdb)
- Hash enrichment (VirusTotal, malware family, SSDEEP)
- URL enrichment (content analysis, phishing detection)
- Email enrichment (HIBP breaches, domain reputation)

---

## 🔐 Legal & Compliance Framework

### ✅ Authorized OSINT Activities
- **Pentesting:** With written authorization from target organization
- **Bug Bounty:** Following platform rules and scope
- **CTF:** Official competitions (TryHackMe, HackTheBox, etc.)
- **Law Enforcement:** Supporting authorized investigations
- **Public Research:** Using only public, freely available data

### ⚠️ Critical Compliance Points
- ✅ Get explicit authorization before any active reconnaissance
- ✅ Maintain chain of custody for evidence
- ✅ Separate victim data (PII) from technical IOCs
- ✅ Document all sources and timestamps
- ✅ Verify evidence admissibility for legal proceedings
- ✅ Follow jurisdiction-specific laws (CFAA, GDPR, Criminal Code, etc.)

### 🔒 Supported Jurisdictions
- 🇺🇸 **USA:** CFAA (18 USC 1030), wiretapping laws
- 🇨🇦 **Canada:** Criminal Code §342.1, §184
- 🇪🇺 **Europe:** GDPR Article 6 (lawful basis)
- 🇬🇧 **UK:** UK GDPR + Computer Misuse Act 1990

Full details: See reference files (legal-considerations.md)

---

## 📊 Vault Integration

### Navigation Structure
```
_BRAIN/DASHBOARD (main hub)
    ↓
ENQUETES_OSINT/INDEX_OSINT (you are here)
    ├── ACTIVES/ (current investigations)
    ├── ARCHIVEES/ (historical reference)
    ├── IOCs_LIBRARY/ (central database)
    └── REPORTS/ (expert exports)
```

### Linking Strategy
From any investigation, link to:
- `[[ENQUETES_OSINT/INDEX_OSINT]]` — Navigation hub
- `[[ENQUETES_OSINT/IOCs_LIBRARY]]` — IOC references
- `[[_BRAIN/DASHBOARD]]` — Main dashboard
- `[[HACKERGPT/RESSOURCES_LEARNING]]` — Learning path

### Tagging Discipline
Always add to investigation notes:

**Primary tags:**
```
#osint            → General OSINT work
#ioc              → Indicator of Compromise
#timeline         → Chronological reconstruction
#profiling        → Target profiling
#attribution      → Actor attribution
```

**Secondary tags:**
```
#phishing #malware #ransomware    → Attack type
#pentesting #ctf #bugbounty       → Investigation type
#cybercriminal #law-enforcement   → Context
#confidential #legal              → Classification
```

**Project tags:**
```
#project/name     → Link to project
```

---

## 📈 Progress Tracking

### Investigation Status Levels
- **ACTIVE** — Currently under investigation
- **PAUSED** — Awaiting more data
- **CLOSED** — Investigation complete, ready for archive
- **ARCHIVED** — Historical reference only

### Confidence Levels
- **HIGH (90%+)** — Very strong evidence for attribution/finding
- **MEDIUM (50-90%)** — Good evidence, some unknowns
- **LOW (10-50%)** — Limited evidence, needs verification

### IOC Management
- **Total IOCs:** Count of all indicators found
- **Validated IOCs:** Count after format/format verification
- **Enriched IOCs:** Count with threat intelligence data
- **Dedup Rate:** Percentage of duplicates removed

---

## 🎓 Learning Resources

### This System
- [[ENQUETES_OSINT/INDEX_OSINT]] — Full documentation
- [[ENQUETES_OSINT/QUICK_COMMANDS]] — Command reference
- [[_TEMPLATES/OSINT_INVESTIGATION]] — Template

### Security Learning
- [[HACKERGPT/RESSOURCES_LEARNING]] — Phase 1-4 learning path
- [[_TEMPLATES/ETHICAL_HACKING_NOTE]] — Hacking template
- [[_BRAIN/PROTOCOLES_VAULT]] — 30+ automation commands

### External Resources
- **TryHackMe** — OSINT rooms + CTF training
- **HackTheBox** — Hands-on labs + real scenarios
- **PortSwigger** — OWASP Top 10 + web security
- **OWASP** — Web application security standards

---

## 🔗 Example Investigations

### Example 1: Phishing Campaign Analysis
**Scenario:** Analyze a PayPal phishing campaign targeting 5,000 users

**What you'll get:**
- Email header analysis (SPF/DKIM/DMARC failures)
- 5 malicious domains identified
- Infrastructure correlation (shared nameserver)
- Emotet malware payload analysis
- MEDIUM-HIGH confidence attribution (70-75%)
- IOC export for security vendors
- YARA detection rules

**See:** `references/example-phishing-campaign.md`

### Example 2: Ransomware Infrastructure Tracking
**Scenario:** Track LockBit 3.0 ransomware distribution network

**What you'll get:**
- Malware sample analysis (cryptography, obfuscation)
- 5 C2 server mapping (across 3 countries)
- Distribution methods breakdown (60% email, 25% watering hole, 15% RDP)
- Victim profiling (47 confirmed + $25M ransom)
- HIGH confidence attribution (80-85%)
- Payment infrastructure analysis (Bitcoin/Monero)
- Defense recommendations

**See:** `references/example-malware-distribution.md`

---

## 📋 Getting Started Checklist

- [ ] Read this README (10 min)
- [ ] Review [[ENQUETES_OSINT/INDEX_OSINT]] (15 min)
- [ ] Copy a command from [[ENQUETES_OSINT/QUICK_COMMANDS]]
- [ ] Tell Claude: `"enquête osint : [name]"`
- [ ] Fill in Phase 1: Target Intelligence Gathering
- [ ] Continue through Phase 6: Expert Reporting
- [ ] Export PDF report when complete
- [ ] Move to ARCHIVEES/ when closed
- [ ] Update [[ENQUETES_OSINT/IOCs_LIBRARY]] with IOCs

---

## 🆘 Troubleshooting

### "How do I start?"
→ Pick a command from [[ENQUETES_OSINT/QUICK_COMMANDS]] and tell Claude

### "Is this legal?"
→ Check [[references/legal-considerations.md]] for your jurisdiction

### "How do I enrich IOCs?"
→ Use script: `python3 ioc-enricher.py --input iocs.csv --output enriched.json`

### "How do I export a report?"
→ Command: `"rapport expert osint : [INVESTIGATION_ID]"`

### "How do I correlate across investigations?"
→ Command: `"corréler enquêtes : [ID1] vs [ID2]"`

---

## 📞 Quick Links

| Link | Purpose |
|------|---------|
| [[ENQUETES_OSINT/INDEX_OSINT]] | Full system documentation |
| [[ENQUETES_OSINT/QUICK_COMMANDS]] | Copy-paste commands |
| [[_TEMPLATES/OSINT_INVESTIGATION]] | Investigation template |
| [[_BRAIN/DASHBOARD]] | Main Vault hub |
| [[_BRAIN/PROTOCOLES_VAULT]] | All 30+ commands |
| [[HACKERGPT/RESSOURCES_LEARNING]] | Security learning path |

---

## 🎯 Success Criteria

**First week:**
- ✅ Understand system structure
- ✅ Create 1 test investigation
- ✅ Extract and validate IOCs
- ✅ Build timeline

**First month:**
- ✅ Complete 3+ investigations
- ✅ Generate 2+ expert reports
- ✅ Establish IOC library (50+ indicators)
- ✅ Document attribution methodology

**Ongoing:**
- ✅ Maintain chain of custody
- ✅ Update legal compliance
- ✅ Enrich IOCs with threat intelligence
- ✅ Archive completed investigations

---

## 📝 System Notes

**Version:** 1.0  
**Created:** 2026-02-19  
**Status:** ACTIVE ✅  
**Last Updated:** 2026-02-19

**Next Steps:**
1. Read [[ENQUETES_OSINT/INDEX_OSINT]]
2. Choose a command from [[ENQUETES_OSINT/QUICK_COMMANDS]]
3. Tell Claude the command
4. Follow the 6-phase workflow
5. Export and archive when complete

---

**You have everything you need to conduct professional OSINT investigations!**

🔍 Start with: `"enquête osint : [name]"`

---

**Tags:** #osint #readme #system #investigations #vault
