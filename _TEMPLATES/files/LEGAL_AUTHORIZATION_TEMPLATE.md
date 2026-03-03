---
type: LEGAL
tags: [LEGAL, authorization, compliance]
version: "1.0"
created: 2026-03-03
---

# ▣ Legal Authorization Document Template

> **⚠ MANDATORY:** This document MUST be completed and signed before any investigation or penetration test begins.

---

## AUTHORIZATION DETAILS

**Document Reference:** AUTH-{{YEAR}}-{{SEQ}}
**Date Issued:** {{DATE}}
**Valid Until:** {{EXPIRY_DATE}}

**Authorized Operator:** TH3_THIRTY3 / Michael Gauthier Guillet
**Organization:** HEXSTRIKE Operations

---

## CLIENT / TARGET INFORMATION

**Client Name:** {{CLIENT_NAME}}
**Client Contact:** {{CONTACT_NAME}} — {{CONTACT_EMAIL}}
**Organization Type:** {{ORG_TYPE}}

---

## SCOPE OF AUTHORIZATION

### Authorized Activities
- [ ] Passive OSINT reconnaissance
- [ ] Active network scanning
- [ ] Web application testing
- [ ] Social engineering (with explicit written consent)
- [ ] Physical security assessment
- [ ] Wireless security assessment

### Target Assets (In Scope)
```
Domains:   {{DOMAINS}}
IP Ranges: {{IP_RANGES}}
Systems:   {{SYSTEMS}}
```

### Explicitly Out of Scope
```
{{OUT_OF_SCOPE_LIST}}
```

### Prohibited Actions
- Denial of Service (DoS/DDoS) attacks
- Destruction or modification of production data
- Actions affecting third-party systems
- Social engineering of personal (non-employee) individuals
- Physical intrusion (unless explicitly authorized)

---

## LEGAL FRAMEWORK

**Jurisdiction:** Quebec, Canada
**Applicable Laws:**
- Criminal Code of Canada — Section 342.1 (Unauthorized use of computer)
- PIPEDA / Law 25 (Quebec) — Personal data protection
- Computer Fraud and Abuse Act (if US systems involved)

**Data Handling:**
- All collected data classified as: {{DATA_CLASSIFICATION}}
- Retention period: {{RETENTION_PERIOD}}
- Data destruction method: {{DESTRUCTION_METHOD}}

---

## SIGNATURES

**Client Representative:**
Name: _____________________ Title: _____________________
Signature: _________________ Date: _____________________

**Authorized Operator:**
Name: TH3_THIRTY3            Title: Security Researcher
Signature: _________________ Date: _____________________

---

**Emergency Stop Contact:** {{EMERGENCY_CONTACT}}
**Incident Notification:** Within {{NOTIFICATION_WINDOW}} hours

---
*HexStrike Legal Framework — 2026-03-03*
