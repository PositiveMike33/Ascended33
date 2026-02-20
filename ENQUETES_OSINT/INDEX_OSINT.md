---
title: "Index des Enquêtes OSINT"
date: 2026-02-19
last_updated: 2026-02-19
type: "INDEX"
---

# 📊 Index des Enquêtes OSINT

**Bienvenue dans le système d'enquêtes OSINT du Vault !**

Ce document sert de hub central pour naviguer toutes vos investigations. Utilise les commandes Claude déclencheurs pour créer et gérer les enquêtes.

---

## ⚡ Commandes Déclencheurs Rapides

### Créer une nouvelle enquête
```
"enquête osint : [NOM_CAMPAGNE]"
→ Crée OSINT_INVESTIGATION.md automatiquement
```

### Analyser des IOCs
```
"analyser iocs : [DESCRIPTION]"
→ Structure et enrichit les IOCs
```

### Profiler un criminel
```
"profiler criminel : [NOM/ALIAS]"
→ Crée profil cible avec TTPs
```

### Générer un rapport expert
```
"rapport expert osint : [INVESTIGATION_ID]"
→ Exporte rapport PDF complet
```

### Tracker un malware
```
"tracker malware : [HASH/FAMILLE]"
→ Corrèle infrastructure + C2
```

### Enquête phishing
```
"investigation phishing : [DOMAINE]"
→ Analyse campagne email + IOCs
```

### Audit sécurité (pentest)
```
"audit sécurité : [CIBLE]"
→ Documente vulnérabilités + fixes
```

---

## 📁 Structure des Dossiers

### ACTIVES/
Enquêtes en cours d'investigation
- **Statut:** ACTIVE
- **Accès rapide:** Démarrage immédiat
- **Format:** OSINT_INVESTIGATION.md
- **Liens:** Mises à jour quotidiennes

### ARCHIVEES/
Enquêtes fermées ou anciennes
- **Statut:** CLOSED ou ARCHIVED
- **Archivage:** Post-rapport expert
- **Conservation:** 2 ans minimum
- **Accès:** Référence historique

### IOCs_LIBRARY/
Bibliothèque centrale d'IOCs corrélés
- **Format:** CSV + JSON enrichi
- **Contenu:** Tous IOCs validés/dédupliqués
- **Mise à jour:** Temps réel
- **Utilisation:** Cross-investigation correlation

### REPORTS/
Rapports experts exportés
- **Format:** PDF professionnel
- **Classification:** CONFIDENTIAL | PUBLIC
- **Destinataire:** Experts, journalistes, enquêteurs
- **Archivage:** Hiérarchie par date

---

## 🔍 Enquêtes Actives

*Aucune enquête active actuellement. Démarre avec :*

```
"enquête osint : [nom_campagne]"
```

---

## 📋 Enquêtes Archivées

### OSI-2025-001: PayPal Phishing Campaign
- **Status:** CLOSED
- **Type:** Phishing → Emotet
- **Résultat:** 5,000+ emails, 200-400 compromises
- **Attribution:** Emotet gang (MEDIUM-HIGH - 70-75%)
- **Lien:** [[ENQUETES_OSINT/ARCHIVEES/OSI-2025-001]]

### OSI-2025-002: LockBit 3.0 Ransomware
- **Status:** CLOSED
- **Type:** Ransomware-as-a-Service
- **Résultat:** 47 victims, 847 BTC (~$25M)
- **Attribution:** LockBit gang (HIGH - 80-85%)
- **Lien:** [[ENQUETES_OSINT/ARCHIVEES/OSI-2025-002]]

---

## 🔗 IOC Statistics

| IOC Type | Total | Validated | Deduplicated | Last Updated |
|----------|-------|-----------|--------------|--------------|
| Domains | 0 | 0 | 0 | N/A |
| IP Addresses | 0 | 0 | 0 | N/A |
| File Hashes | 0 | 0 | 0 | N/A |
| Email Addresses | 0 | 0 | 0 | N/A |
| URLs | 0 | 0 | 0 | N/A |

---

## 📊 Attribution Summary

| Actor/Campaign | Confidence | Evidence | Last Seen |
|---|---|---|---|
| [À remplir] | HIGH/MEDIUM/LOW | [Technical/Behavioral/Contextual] | [DATE] |

---

## 🎯 Investigation Workflow

```
1. GATHER INTELLIGENCE
   ↓ (Passive OSINT)
   
2. STRUCTURE DATA
   ↓ (Normalize IOCs)
   
3. TRACK IOCs
   ↓ (Correlate infrastructure)
   
4. BUILD TIMELINE
   ↓ (Chronological reconstruction)
   
5. MAP CONNECTIONS
   ↓ (Relationship analysis)
   
6. GENERATE REPORT
   ↓ (Export PDF + legal compliance)
   
7. ARCHIVE
   ✅ (Move to ARCHIVEES/)
```

---

## 🛠️ Automation Scripts

Utilisables pour extraire et enrichir IOCs :

### parse-iocs.sh
```bash
./parse-iocs.sh <input_file> [output_format]
# Formats: csv, json, yara, zeek
```

### ioc-enricher.py
```bash
python3 ioc-enricher.py --input iocs.csv --output enriched.json
# Enrichit: domains, IPs, hashes, emails, URLs
```

---

## 📚 Documentation Technique

### References Disponibles
- **osint-frameworks.md** - Méthodologie OSINT complète
- **ioc-analysis.md** - Analyse détaillée des IOCs
- **attribution-techniques.md** - Framework d'attribution
- **legal-considerations.md** - Compliance juridique

### Examples Complets
- **example-phishing-campaign.md** - Cas PayPal phishing
- **example-malware-distribution.md** - Cas LockBit RaaS

---

## ⚖️ Conformité Légale

### ✅ Avant chaque enquête
- [ ] Authorization vérifiée (Pentesting/CTF/Bug Bounty/Legal)
- [ ] Victimes identifiées et confidentialité assurée
- [ ] Chain of custody établie
- [ ] Données séparées (PII ≠ Technical IOCs)

### 📋 Jurisdictions Supportées
- 🇺🇸 United States (CFAA - 18 USC 1030)
- 🇨🇦 Canada (Criminal Code §342.1, §184)
- 🇪🇺 Europe (GDPR Article 6)
- 🇬🇧 UK (UK GDPR + Computer Misuse Act 1990)

### 👮 Law Enforcement Coordination
- FBI Cyber Division
- RCMP (Canada)
- Europol

---

## 🏷️ Tagging System

### Primary Tags
```
#osint              — Enquête OSINT générale
#ioc                — Indicator of Compromise
#timeline           — Reconstruction chronologique
#profiling          — Profilage de cible
#attribution        — Attribution analysis
#phishing           — Campagne phishing
#malware            — Malware distribution
#ransomware         — Ransomware campaign
#pentesting         — Authorized pentest
#ctf                — Capture The Flag
#bugbounty          — Bug bounty investigation
#confidential        — Données confidentielles
#legal              — Dossier pour tribunal
```

### Secondary Tags
```
#cybercriminal      — Criminel cyber ciblé
#law-enforcement    — Coordination police
#evidence           — Chaîne de preuve
#infrastructure     — Corrélation infrastructure
#c2                 — Command & Control
#exploit            — Exploitation technique
```

---

## 📈 Metrics & KPIs

### Investigation Progress
- IOCs collected: [X]/Total
- Timeline coverage: [X]%
- Attribution confidence: [HIGH/MEDIUM/LOW]
- Report readiness: [%]

### Team Activity
- Active investigations: [X]
- Closed investigations: [X]
- Total evidence collected: [X] IOCs
- Reports generated: [X]

---

## 🔐 Security Best Practices

### Data Handling
1. **Validation** - Tous les IOCs validés avant corrélation
2. **Normalization** - Format standardisé (lowercase, FQDN, etc)
3. **Deduplication** - Suppression des doublons
4. **Enrichment** - APIs threat intelligence (VirusTotal, etc)
5. **Correlation** - Clustering par infrastructure/behavioral patterns

### Evidence Integrity
- ✅ Cryptographic hashing (SHA256)
- ✅ Write-blocking pour disques
- ✅ No modification of evidence
- ✅ Audit trail documentation
- ✅ Timestamp verification

### Confidentiality
- 🔐 Victim data separated from IOCs
- 🔐 Classification markers (CONFIDENTIAL/PUBLIC)
- 🔐 Limited distribution (experts, LE only)
- 🔐 Secure archival post-investigation

---

## 🔗 Vault Integration

### Linking Strategy
```
_BRAIN/DASHBOARD
    ↓
ENQUETES_OSINT/INDEX_OSINT (vous êtes ici)
    ├─ ACTIVES/[OSI-2026-XXX]
    ├─ ARCHIVEES/[OSI-2025-XXX]
    ├─ IOCs_LIBRARY/[iocs_enriched.json]
    └─ REPORTS/[rapport_expert.pdf]

Connections:
ENQUETES_OSINT ↔ HACKERGPT/OSINT Profilage
ENQUETES_OSINT ↔ REPORT/Classified Report
ENQUETES_OSINT ↔ 🔐_SECURITY_AUDIT_PROJECT
```

### Related Notes
- [[_BRAIN/DASHBOARD]] - Main hub
- [[_BRAIN/PROTOCOLES_VAULT]] - 30+ commandes
- [[HACKERGPT/RESSOURCES_LEARNING]] - Hacking learning path
- [[_TEMPLATES/OSINT_INVESTIGATION]] - Template d'enquête
- [[_TEMPLATES/ETHICAL_HACKING_NOTE]] - Hacking notes

---

## 📞 Contact & Support

### Pour enquêtes légales
- FBI Cyber Division: ic3.gov
- RCMP: cybercrime.rcmp.gc.ca
- Europol: europol.europa.eu

### For pentesting & bug bounty
- HackerOne, Bugcrowd, Intigriti
- Responsible disclosure guidelines

### For CTF & learning
- TryHackMe, HackTheBox, PicoCTF
- OWASP WebGoat, PortSwigger labs

---

## 📝 Notes

**Dernière mise à jour:** 2026-02-19  
**Version:** 1.0  
**Statut:** ACTIF ✅

Pour démarrer une enquête, utilise l'une des commandes déclencheurs ci-dessus !

---

**Tags:** #osint #index #enquetes #ioc #attribution #vault-hub
