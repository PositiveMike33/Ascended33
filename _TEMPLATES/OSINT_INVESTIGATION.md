---
title: "OSINT Investigation: [INVESTIGATION_NAME]"
date: 2026-02-19
status: ACTIVE | CLOSED | ARCHIVED
investigation_id: "OSI-2026-[XXX]"
classification: CONFIDENTIAL | PUBLIC | LEGAL
authorization_type: "Pentesting | CTF | Bug Bounty | Law Enforcement Coordination"
confidence_level: HIGH | MEDIUM | LOW
target_type: "Cybercriminal | Phishing Campaign | Malware Distribution | Data Breach | Ransomware Gang"
priority: P1 | P2 | P3
---

# OSINT Investigation: [INVESTIGATION_NAME]

**Investigation ID:** OSI-2026-[XXX]  
**Status:** ACTIVE | CLOSED  
**Started:** [DATE]  
**Last Updated:** [DATE]  
**Classification:** CONFIDENTIAL | PUBLIC  
**Authorization:** [AUTHORIZATION_TYPE]  

---

## 🎯 Executive Summary

[2-3 sentence overview of the investigation, key findings, and impact]

**Key Metrics:**
- Total targets/victims: [NUMBER]
- IOCs identified: [NUMBER] (domains, IPs, hashes, emails)
- Confidence attribution: [HIGH/MEDIUM/LOW] - [PERCENTAGE]%
- Timeline span: [START DATE] → [END DATE]

---

## 📋 Target Profile

### Primary Target
- **Name/Alias:** [NAME or "UNKNOWN"]
- **Type:** Individual | Group | Organization | Campaign
- **Known as:** [ALTERNATE NAMES/ALIASES]
- **Suspected Location:** [COUNTRY/REGION]
- **Sophistication Level:** Novice | Amateur | Professional | State-Sponsored

### Background
[Detailed description of target history, previous campaigns, known affiliations]

### Capabilities & Tactics
- **Primary Attack Vector:** [PHISHING/MALWARE/RDP BRUTE FORCE/etc]
- **Malware Family:** [IF APPLICABLE]
- **Infrastructure:** [HOSTING PROVIDER/ISP/BULLETPROOF HOSTER]
- **TTPs (Tactics, Techniques, Procedures):**
  - [TTP 1]
  - [TTP 2]
  - [TTP 3]

---

## 🔍 Phase 1: Target Intelligence Gathering

### Data Sources Consulted
- [ ] WHOIS/Domain Registry
- [ ] DNS Records
- [ ] SSL Certificates
- [ ] Social Media Profiles
- [ ] Email Intelligence
- [ ] Dark Web Monitoring
- [ ] Public Breach Databases
- [ ] Security Research Reports
- [ ] Government Databases (if authorized)

### Intelligence Collected
[Document all findings from passive intelligence gathering]

**Key Findings:**
- [Finding 1 with source]
- [Finding 2 with source]
- [Finding 3 with source]

---

## 📊 Phase 2: Data Structuring

### Investigation Framework

| Category | Details | Confidence |
|----------|---------|------------|
| **Infrastructure** | [Shared nameservers, hosting providers, IP ranges] | HIGH/MEDIUM/LOW |
| **Malware** | [Family, variants, C2 protocols] | HIGH/MEDIUM/LOW |
| **Timeline** | [Campaign phases with dates] | HIGH/MEDIUM/LOW |
| **Attribution** | [Suspected actor(s)] | HIGH/MEDIUM/LOW |
| **Impact** | [Number of victims, damage] | HIGH/MEDIUM/LOW |

### Data Quality Assessment
- Completeness: [PERCENTAGE]%
- Reliability: HIGH | MEDIUM | LOW
- Sources Verified: [COUNT]
- Data Gaps: [LIST]

---

## 🏷️ Phase 3: IOC Tracking

### Indicators of Compromise

#### Domains
| Domain | Registrar | Hosting | Detection Ratio | First Seen | Last Seen | Status |
|--------|-----------|---------|-----------------|-----------|-----------|--------|
| [domain1.com] | [Registrar] | [IP/Hosting] | 38/87 | [DATE] | [DATE] | Active/Sinkholed |
| [domain2.com] | [Registrar] | [IP/Hosting] | 42/87 | [DATE] | [DATE] | Active/Sinkholed |

#### IP Addresses
| IP Address | Country | ASN | Hosting Provider | First Seen | Last Seen | Services |
|-----------|---------|-----|------------------|-----------|-----------|----------|
| [1.2.3.4] | [COUNTRY] | AS12345 | [PROVIDER] | [DATE] | [DATE] | HTTP/HTTPS/DNS |
| [5.6.7.8] | [COUNTRY] | AS54321 | [PROVIDER] | [DATE] | [DATE] | SMTP/SSH |

#### File Hashes
| Hash (SHA256) | Type | Family | Detection Ratio | Analysis | First Seen |
|---------------|------|--------|-----------------|----------|-----------|
| [HASH] | [EXE/DLL/PDF] | [MALWARE_FAMILY] | 45/87 | [Link to analysis] | [DATE] |
| [HASH] | [EXE/DLL/DOC] | [MALWARE_FAMILY] | 52/87 | [Link to analysis] | [DATE] |

#### Email Addresses
| Email | Domain | First Seen | Breaches | Associated | Status |
|-------|--------|-----------|----------|-----------|--------|
| [email@domain.com] | [DOMAIN] | [DATE] | [BREACH_DB] | [OTHER_IOCs] | Active |

### Infrastructure Correlation
[Describe shared infrastructure patterns indicating centralized control]

**Confidence Level:** HIGH | MEDIUM | LOW  
**Reasoning:** [Explain correlation confidence]

---

## ⏱️ Phase 4: Timeline Construction

### Campaign Timeline

**Phase 1: [PHASE_NAME]** ([START_DATE] - [END_DATE])
- [Key activity 1]
- [Key activity 2]
- [Key activity 3]

**Phase 2: [PHASE_NAME]** ([START_DATE] - [END_DATE])
- [Key activity 1]
- [Key activity 2]

**Phase 3: [PHASE_NAME]** ([START_DATE] - [END_DATE])
- [Key activity 1]
- [Key activity 2]

### Timeline Evidence Sources
- [ ] Email headers with timestamps
- [ ] Domain registration dates
- [ ] Certificate transparency logs
- [ ] Malware compilation timestamps
- [ ] Victim reports/dates
- [ ] Security research publication dates

---

## 🔗 Phase 5: Connection Mapping

### Relationship Matrix

```
[TARGET] → [MALWARE FAMILY] → [C2 INFRASTRUCTURE]
    ↓            ↓                    ↓
[PHISHING] → [IOCs] → [SHARED HOSTING] → [ASN]
    ↓
[VICTIMS]
```

### Actor Relationships
- **Confirmed Connections:** [List confirmed relationships]
- **Suspected Connections:** [List suspected relationships with confidence]
- **Alternative Hypotheses:** [List alternative attribution scenarios]

### Tool & Malware Correlations
- **Custom Malware:** [Indicates [HIGH/MEDIUM/LOW] sophistication]
- **Off-the-shelf Tools:** [Name tools used]
- **Code Similarity:** [SSDEEP/Imphash matches indicating variants]

---

## 🎖️ Phase 6: Attribution & Expert Reporting

### Attribution Assessment

**Primary Attribution:**
- **Suspected Actor(s):** [NAME]
- **Confidence Level:** HIGH (90%+) | MEDIUM (50-90%) | LOW (10-50%)
- **Confidence Percentage:** [X]%

### Evidence Supporting Attribution

#### Technical Evidence
- [Evidence 1 - e.g., custom malware variant]
- [Evidence 2 - e.g., infrastructure preferences]
- [Evidence 3 - e.g., C2 protocol implementation]

#### Behavioral Evidence
- [Behavior 1 - e.g., timing patterns]
- [Behavior 2 - e.g., targeting preferences]
- [Behavior 3 - e.g., operational security patterns]

#### Contextual Evidence
- [Context 1 - e.g., geopolitical motivations]
- [Context 2 - e.g., known tool usage]
- [Context 3 - e.g., victim targeting]

### Alternative Hypotheses
[Describe why attribution might be incorrect or alternative actors]

**Reasoning for Rejection:** [Explain why alternatives are less likely]

### Known Unknowns
- [Unknown 1]
- [Unknown 2]
- [Unknown 3]

---

## 📄 Expert Report Components

### Legal Compliance
- ✅ Authorization Verified: [YES/NO]
- ✅ Chain of Custody Maintained: [YES/NO]
- ✅ Victim Data Separated: [YES/NO]
- ✅ Evidence Admissibility: [VERIFIED/QUESTIONABLE/NOT_VERIFIED]

### Recommendations

#### For Law Enforcement
- [Recommendation 1]
- [Recommendation 2]
- [Recommendation 3]

#### For Incident Response
- [Recommendation 1]
- [Recommendation 2]

#### For Network Defense
- [Detection rule/signature]
- [Blocking recommendation]

---

## 🔐 Appendices

### Appendix A: Detailed IOC Analysis
[Full IOC extraction and enrichment data]

### Appendix B: Malware Analysis Details
[Behavioral, static, and code analysis details]

### Appendix C: Infrastructure Mapping
[Detailed hosting provider, ASN, and network topology analysis]

### Appendix D: Attribution Methodology
[Detailed explanation of attribution process and evidence weighting]

### Appendix E: Detection & Defense Rules
```yara
rule [MALWARE_FAMILY] {
    strings:
        $string1 = "[STRING]"
        $string2 = "[STRING]"
    condition:
        all of them
}
```

---

## 📌 Investigation Metadata

| Field | Value |
|-------|-------|
| **Investigation ID** | OSI-2026-[XXX] |
| **Created** | [DATE] |
| **Last Modified** | [DATE] |
| **Modified By** | [NAME/CLAUDE] |
| **Status** | ACTIVE \| CLOSED \| ARCHIVED |
| **Classification** | CONFIDENTIAL \| PUBLIC \| LEGAL |
| **Authorization** | [TYPE] |
| **Total IOCs** | [NUMBER] |
| **Confidence** | HIGH \| MEDIUM \| LOW |
| **Exported Reports** | [LINK1], [LINK2] |
| **Related Investigations** | [[OSI-2026-XXX]], [[OSI-2026-YYY]] |

---

## 🔗 Links & References

**Related Investigations:**
- [[OSI-2026-XXX - Similar Campaign]]
- [[OSI-2026-YYY - Same Actor]]

**Vault Integration:**
- [[ENQUETES_OSINT/ACTIVES - Active investigations hub]]
- [[ENQUETES_OSINT/IOCs_LIBRARY - IOC correlation database]]
- [[_BRAIN/DASHBOARD - Main dashboard]]

**External References:**
- [Security Research Report]
- [Malware Analysis Blog]
- [Threat Intelligence Report]

---

## 📋 Checklist

- [ ] All IOCs validated and normalized
- [ ] Timeline verified with source documentation
- [ ] Attribution confidence justified
- [ ] Legal compliance verified
- [ ] Victim data properly segmented
- [ ] Chain of custody maintained
- [ ] Report exported to PDF
- [ ] Law enforcement notified (if applicable)
- [ ] Evidence archived securely
- [ ] Investigation status updated

---

**Tags:** #osint #ioc #timeline #profiling #attribution #[TARGET_TYPE] #[classification]
