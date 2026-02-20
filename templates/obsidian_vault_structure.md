# 📁 Obsidian Vault Structure - Ascended33 OSINT Platform

**Version:** 1.0.0  
**Status:** Production Ready  
**Purpose:** Recommended folder structure and conventions for your OSINT vault

---

## 📋 Quick Start Folder Structure

Create these folders in your Obsidian vault root:

```
Your-Obsidian-Vault/
├── Investigations/          # Investigation projects
├── IOCs/                    # Indicator of Compromise database
├── Actors/                  # Threat actor profiles
├── Campaigns/               # Campaign tracking
├── Tools/                   # Tool notes and commands
├── Resources/               # Reference materials
├── Templates/               # Note templates
└── Archive/                 # Completed investigations
```

---

## 🔍 Detailed Structure

### 1. **Investigations/** - Investigation Projects

Store investigation notes organized by case ID or name.

```
Investigations/
├── inv_001_emotet/
│   ├── index.md                    # Investigation overview
│   ├── timeline.md                 # Chronological events
│   ├── ioc_summary.md             # Summary of IOCs found
│   ├── actors.md                  # Involved threat actors
│   ├── findings.md                # Key findings
│   └── recommendations.md         # Remediation steps
├── inv_002_phishing/
│   ├── index.md
│   ├── email_analysis.md
│   └── ...
```

**index.md Frontmatter Example:**
```yaml
---
case_of_use: incident-response
status: active
investigation_id: inv_001
tags: [emotet, malware, banking, incident]
created_date: 2026-02-20T10:00:00Z
modified_date: 2026-02-20T10:00:00Z
source: Internal reporting
confidence: high
---
```

### 2. **IOCs/** - Indicator of Compromise Database

Organized by IOC type for easy reference.

```
IOCs/
├── domain/
│   ├── c2.emotet.com.md           # One IOC per file
│   ├── phishing.example.com.md
│   └── ...
├── ip/
│   ├── 192.168.1.100.md
│   ├── 10.0.0.50.md
│   └── ...
├── hash/
│   ├── md5_abc123def456.md
│   ├── sha256_xyz789.md
│   └── ...
├── email/
│   ├── attacker@domain.com.md
│   └── ...
└── bitcoin/
    ├── 1A1z7agoat.md
    └── ...
```

**IOC Note Frontmatter:**
```yaml
---
case_of_use: incident-response
ioc_type: domain
ioc_value: c2.emotet.com
confidence: high
first_seen: 2026-01-15
source: URLhaus
investigation_id: inv_001
tags: [ioc-domain, case-incident, emotet, c2]
status: active
---
```

### 3. **Actors/** - Threat Actor Profiles

Profile each threat actor or group you encounter.

```
Actors/
├── WIZARD_SPIDER.md               # Ransomware group
├── WIZARD_SPIDER/
│   ├── campaigns.md               # Campaigns by this group
│   ├── iocs.md                    # All IOCs linked
│   ├── tools.md                   # Tools they use
│   └── timeline.md                # Timeline of activity
├── APT28.md
└── ...
```

**Actor Profile Frontmatter:**
```yaml
---
case_of_use: threat-intelligence
actor_type: group
actor_name: WIZARD_SPIDER
aliases: [TEMP_TRIDENT, UNC1878]
country: Russia (suspected)
tags: [ransomware, financially-motivated, active]
confidence: high
campaigns: [inv_001, inv_003]
---
```

### 4. **Campaigns/** - Campaign Tracking

Track multi-incident campaigns.

```
Campaigns/
├── emotet_2026.md                 # Campaign overview
├── emotet_2026/
│   ├── timeline.md                # Campaign timeline
│   ├── affected_targets.md        # Organizations hit
│   ├── ioc_summary.md            # All campaign IOCs
│   └── actors.md                 # Groups involved
├── lazarus_campaign_q1.md
└── ...
```

**Campaign Frontmatter:**
```yaml
---
case_of_use: incident-response
campaign_name: Emotet Wave Q1 2026
campaign_id: camp_emotet_q1_2026
status: active
start_date: 2026-01-01
end_date: null
actors: [WIZARD_SPIDER, TA542]
tags: [campaign, emotet, banking-trojan]
estimated_victims: 200+
---
```

### 5. **Tools/** - Tool Notes and Commands

Store tool documentation and useful commands.

```
Tools/
├── OSINT/
│   ├── shodan_queries.md
│   ├── censys_techniques.md
│   └── intelx_notes.md
├── Malware_Analysis/
│   ├── ghidra_tips.md
│   ├── strings_techniques.md
│   └── yara_rules.md
├── Network/
│   ├── nmap_commands.md
│   ├── wireshark_filters.md
│   └── zeek_queries.md
└── ...
```

### 6. **Resources/** - Reference Materials

External links and reference documentation.

```
Resources/
├── MITRE_ATT&CK.md                # Techniques reference
├── CVE_Database.md                # CVE lookup references
├── RegEx_Patterns.md              # Useful regex patterns
├── External_Feeds.md              # IOC feed sources
└── Documentation/
    ├── RGPD.md
    ├── Legal_Framework.md
    └── Ethics_Guidelines.md
```

### 7. **Templates/** - Note Templates

Reusable templates for consistency.

```
Templates/
├── Investigation_Template.md       # Blank investigation
├── IOC_Template.md                # Blank IOC note
├── Actor_Template.md              # Blank actor profile
├── Campaign_Template.md            # Blank campaign
└── Incident_Report_Template.md    # Report template
```

### 8. **Archive/** - Completed Investigations

Move completed investigations here for archival.

```
Archive/
├── 2025/
│   ├── inv_099_resolved.md
│   └── ...
├── 2026_q1/
│   ├── inv_001_emotet_completed.md
│   └── ...
```

---

## 🏷️ Tagging System

Use consistent tags for organization and filtering.

### Investigation Tags
```
#investigation
#incident-response
#bug-bounty
#journalisme
#personnel
#active
#resolved
#archived
```

### IOC Type Tags
```
#ioc-domain
#ioc-ip
#ioc-hash
#ioc-email
#ioc-bitcoin
#ioc-url
```

### Severity Tags
```
#severity-critical
#severity-high
#severity-medium
#severity-low
```

### Status Tags
```
#status-active
#status-review
#status-archived
```

### Case of Use Tags
```
#case-incident
#case-bounty
#case-journalisme
#case-personnel
```

---

## 📝 Naming Conventions

### Investigation Notes
- Format: `inv_{id}_{short_name}.md`
- Example: `inv_001_emotet_botnet.md`

### IOC Notes
- Format: `{ioc_type}_{identifier}.md`
- Examples:
  - `domain_c2.emotet.com.md`
  - `ip_192.168.1.100.md`
  - `hash_abc123def456.md`

### Actor Notes
- Format: `{actor_name_uppercase}.md`
- Example: `WIZARD_SPIDER.md`

### Campaign Notes
- Format: `{campaign_name}_{year_quarter}.md`
- Example: `emotet_2026_q1.md`

---

## 📌 Frontmatter Template

Every note should have this frontmatter:

```yaml
---
case_of_use: [incident-response | bug-bounty | journalisme | personnel]
source: [Where information came from]
created_date: [ISO 8601 format]
modified_date: [ISO 8601 format]
tags: [relevant, tags]
confidence: [low | medium | high]
investigation_id: [inv_xxx if applicable]
status: [active | archived | review]
---
```

---

## 🔗 Cross-Linking Best Practices

### Link to Investigations
```markdown
See also: [[Investigations/inv_001_emotet/index|Emotet Investigation]]
```

### Link to IOCs
```markdown
Related IOC: [[IOCs/domain/c2.emotet.com|c2.emotet.com]]
```

### Link to Actors
```markdown
Attribution: [[Actors/WIZARD_SPIDER|WIZARD SPIDER Group]]
```

### Link to Campaigns
```markdown
Part of: [[Campaigns/emotet_2026_q1|Emotet Q1 2026 Campaign]]
```

---

## 📊 Useful Dataview Queries

### View all active investigations
```
TABLE case_of_use, status, confidence
FROM "Investigations"
WHERE status = "active"
SORT modified_date DESC
```

### View all IOCs by type
```
TABLE ioc_type, confidence, investigation_id
FROM "IOCs"
SORT ioc_type, confidence DESC
```

### View investigation timeline
```
TABLE created_date as "Created", modified_date as "Modified", status
FROM "Investigations"
SORT modified_date DESC
```

---

## 🎯 Folder Setup Script

Run this to create the full structure:

```bash
# From your Obsidian vault root directory
mkdir -p Investigations IOCs/domain IOCs/ip IOCs/hash IOCs/email IOCs/bitcoin
mkdir -p Actors Campaigns Tools/OSINT Tools/Malware_Analysis Tools/Network
mkdir -p Resources/Documentation Templates Archive/{2025,2026_q1,2026_q2}
```

---

## 💡 Pro Tips

1. **Consistency**: Use the exact folder structure and naming conventions
2. **Tagging**: Tag everything - it's faster to filter later
3. **Backlinks**: Create backlinks between related notes for graph visualization
4. **Templates**: Create notes from templates to ensure proper structure
5. **Regular Cleanup**: Archive old investigations monthly
6. **Daily Journal**: Maintain a daily investigation log in your vault
7. **Obsidian Plugins**: Install Dataview for powerful queries
8. **Graph View**: Use graph view to visualize investigation connections

---

## 🔐 Privacy & Compliance

- ✅ Store only information you're authorized to keep
- ✅ Use `#personnel` tag for personal notes
- ✅ Encrypt vault if storing sensitive data
- ✅ Respect RGPD/CEDH when storing personal data
- ✅ Mark sensitive investigations with `#confidential`

---

**Last Updated:** 2026-02-20  
**Maintained by:** Ascended33 OSINT Platform  
**Version:** 1.0.0
