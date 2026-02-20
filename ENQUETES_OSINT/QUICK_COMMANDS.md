---
title: "OSINT Quick Commands"
date: 2026-02-19
type: "REFERENCE"
---

# ⚡ OSINT Quick Commands — Déclenche investigation avec Claude

**Copie-colle une commande → Claude créera la note automatiquement**

---

## 🚀 Commandes Principales

### 1️⃣ Créer une enquête OSINT
```
enquête osint : [NOM_CAMPAGNE]
```
**Exemple :**
```
enquête osint : PayPal phishing campaign Jan 2026
```
**Résultat :** `OSINT_INVESTIGATION.md` avec tous les sections (6 phases)

---

### 2️⃣ Analyser des IOCs
```
analyser iocs : [DESCRIPTION_CAMPAGNE]
```
**Exemple :**
```
analyser iocs : 5 domains, 2 IPs, malware hash from phishing
```
**Résultat :** Extrait + valide + normalise + enrichit IOCs

---

### 3️⃣ Profiler un criminel
```
profiler criminel : [NOM_OU_ALIAS]
```
**Exemple :**
```
profiler criminel : Emotet gang
```
**Résultat :** Background + capabilities + TTPs + known infrastructure

---

### 4️⃣ Construire une timeline
```
timeline : [NOM_CAMPAGNE]
```
**Exemple :**
```
timeline : Emotet botnet distribution 2024-2025
```
**Résultat :** Chronologie avec phases, dates, evidence sources

---

### 5️⃣ Générer un rapport expert
```
rapport expert osint : [INVESTIGATION_ID]
```
**Exemple :**
```
rapport expert osint : OSI-2026-001
```
**Résultat :** PDF professionnel avec legal compliance + evidence

---

### 6️⃣ Tracker un malware
```
tracker malware : [HASH_OU_FAMILLE]
```
**Exemple :**
```
tracker malware : LockBit 3.0 ransomware
```
**Résultat :** Analyse C2 + distribution + victims + attribution

---

### 7️⃣ Investigation phishing
```
investigation phishing : [DOMAINE_OU_EMAIL]
```
**Exemple :**
```
investigation phishing : paypal-security-verify.com
```
**Résultat :** Email analysis + IOCs + infrastructure + victims

---

### 8️⃣ Audit sécurité (Pentest)
```
audit sécurité : [CIBLE]
```
**Exemple :**
```
audit sécurité : Company X network infrastructure
```
**Résultat :** Vulnérabilités + evidence + recommendations

---

### 9️⃣ Corréler infrastructure
```
corréler infrastructure : [DESCRIPTION]
```
**Exemple :**
```
corréler infrastructure : 3 domains with shared nameserver ns1.attacker-dns.ru
```
**Résultat :** Clustering analysis + HIGH confidence linking

---

### 🔟 Attribution analysis
```
attribuer à : [ACTOR_NAME]
```
**Exemple :**
```
attribuer à : Emotet gang - analyze confidence level
```
**Résultat :** Evidence evaluation + alternative hypotheses + confidence justification

---

## 📊 Commandes Secondaires

### Enrichir IOCs
```
enrichir iocs : [CSV_FILE_OU_LISTE]
```
Utilise VirusTotal, Shodan, WHOIS, SSL certs, URLhaus, HIBP

---

### Valider IOCs
```
valider iocs : [LISTE_IOCs]
```
Vérifie format + normalise + déduplique

---

### Créer règles de détection
```
yara rules : [MALWARE_FAMILLE]
```
Génère règles YARA pour Suricata/YARA scanners

---

### Exporter en JSON
```
exporter json : [INVESTIGATION_ID]
```
Exporte tous IOCs + timeline + attribution en JSON structuré

---

### Séparer données confidentielles
```
séparer pii : [INVESTIGATION_ID]
```
Crée 2 fichiers : Technical IOCs + Victim PII (séparé)

---

### Vérifier conformité légale
```
vérifier légalité : [INVESTIGATION_ID]
```
Audit : authorization + chain of custody + evidence admissibility

---

## 🔗 Commandes Avancées

### Corréler multi-enquêtes
```
corréler enquêtes : [ID1] vs [ID2]
```
Trouvent IOCs communs ou patterns similaires

---

### Générer rapport comparatif
```
comparer acteurs : [ACTOR1] vs [ACTOR2]
```
Infrastructure + TTPs + victims + timeline overlap

---

### Timeline visuelle
```
créer timeline visuelle : [INVESTIGATION_ID]
```
Génère canvas/diagram Obsidian avec phases colorées

---

### Dashboard enquête
```
dashboard enquête : [INVESTIGATION_ID]
```
Crée vue Dataview avec stats + IOCs + timeline

---

## 🛠️ Automation Scripts

### Parse IOCs from file
```bash
./parse-iocs.sh input.txt csv
# Output: iocs_[TIMESTAMP].csv
```

### Enrichir IOCs
```bash
python3 ioc-enricher.py --input iocs.csv --output enriched.json
# Ajoute : VirusTotal, Shodan, WHOIS, etc.
```

---

## 📋 Patterns d'utilisation

### Workflow 1: Nouvelle campagne phishing
```
1. investigation phishing : [DOMAINE]
2. analyser iocs : [description des IOCs trouvés]
3. corréler infrastructure : [patterns détectés]
4. attribuer à : [suspected actor]
5. rapport expert osint : [ID généré]
```

### Workflow 2: Tracker malware
```
1. tracker malware : [HASH/FAMILLE]
2. enrichir iocs : [IOCs from analysis]
3. créer timeline : [campaign phases]
4. comparer acteurs : [known variants]
5. yara rules : [generate detection rules]
```

### Workflow 3: Pentest autorisé
```
1. audit sécurité : [TARGET]
2. profiler criminel : [infrastructure owner]
3. analyser iocs : [IOCs discovered during pentest]
4. vérifier légalité : [ensure authorization]
5. rapport expert osint : [export for client]
```

---

## ✨ Pro Tips

### Tip 1: Dense linking
```
Après chaque commande, ajoute :
[[ENQUETES_OSINT/INDEX_OSINT]]  → Hub central
[[ENQUETES_OSINT/IOCs_LIBRARY]] → Reference
```

### Tip 2: Tagging discipline
```
Toujours ajouter :
#osint #ioc #[target_type] #[classification]
#phishing #malware #ransomware
#pentesting #ctf #bugbounty
```

### Tip 3: Versioning
```
Chaque mise à jour :
- Update date: [DATE]
- Status: ACTIVE → CLOSED
- IOC count: [NUMBER]
- Confidence: [LEVEL]
```

### Tip 4: Evidence backup
```
Toujours télécharger :
- Investigation PDF (expert report)
- IOCs JSON (structured data)
- Screenshots (evidence)
```

---

## 🔐 Checklist avant export

- [ ] Authorization vérifiée
- [ ] Chain of custody documentée
- [ ] Victim data séparé des IOCs
- [ ] Attribution confidence justifiée
- [ ] Legal compliance vérifié
- [ ] Sources documentées (timestamps)
- [ ] IOCs validés + dédupliqués
- [ ] Timeline chronologique vérifiée
- [ ] TTPs mappés à MITRE ATT&CK
- [ ] Rapport formaté profesionnellement

---

## 📞 Quick Reference Links

**Vault Hub:** [[ENQUETES_OSINT/INDEX_OSINT]]  
**Dashboard:** [[_BRAIN/DASHBOARD]]  
**Hacking Learning:** [[HACKERGPT/RESSOURCES_LEARNING]]  
**All Commands:** [[_BRAIN/PROTOCOLES_VAULT]]

---

## 📝 Notes

**Dernière mise à jour:** 2026-02-19  
**Format:** Copy-paste ready commands  
**Status:** ACTIVE ✅

**À chaque enquête :**
1. Copie commande pertinente
2. Dis à Claude
3. Claude crée note automatiquement
4. Développe avec 6 phases du framework OSINT

---

**Tags:** #osint #quick-reference #commands #automation #vault
