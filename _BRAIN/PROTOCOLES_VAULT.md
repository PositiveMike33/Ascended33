---
date: 2026-02-14
type: protocoles
tags: [vault, automation, commands, claude]
status: active
---

# 🎯 PROTOCOLES VAULT — Commandes déclencheurs

> **Référence complète des commandes pour opérer le système VAULT avec Claude.**
> Dire simplement la commande → Claude exécute l'action correspondante.

---

## 📋 Vue d'ensemble

| Domaine | Commandes clés | Voir section |
|---------|----------------|--------------|
| **Rapports** | rapport de ce soir, audit, synthèse | §1 |
| **Productivité** | ajoute à mon todo, capture ça, planning | §2 |
| **Productive Revenue** | idée revenu, pricing, brainstorm | §3 |
| **Ethical Hacking** | hacking, CTF, audit sécurité | §4 |
| **Claude Workflows** | workflow claude, API, automation | §5 |
| **Vault Management** | état du vault, mise à jour mémoire, maintenance | §6 |

---

---

## §1 — RAPPORTS & SYNTHÈSES

### 1️⃣ "rapport de ce soir"

**Trigger :**
```
Claude, rapport de ce soir
```

**Action :**
- Crée fichier : `RAPPORT_QUOTIDIEN/[YYYY-MM-DD].md`
- Format : Template RAPPORT_QUOTIDIEN
- Contient : Résumé jour + accomplissements + prochaines étapes

**Template utilisé :** `_TEMPLATES/RAPPORT_QUOTIDIEN.md`

**Example output :**
```markdown
# 📋 RAPPORT QUOTIDIEN — 2026-02-14

## ✨ Résumé du jour
1. Créé 3 templates productifs (revenu, hacking, workflow)
2. Enrichi MEMORY.md avec compétences avancées
3. Documenté protocoles VAULT complètement

## 🎯 Priorités de demain
1. Tester API Claude pour automation
2. Créer 3 notes PRODUCTIVE_REVENU réelles
3. Documenter 1 CTF walkthrough

## 💡 Notes personnelles
...
```

---

### 2️⃣ "état du vault"

**Trigger :**
```
Claude, état du vault
Claude, audit
```

**Action :**
- Lit : `_BRAIN/AUDIT.md`
- Affiche : Santé vault + problèmes + recommendations

**Génère :**
- Nombre total notes
- Notes récentes
- Liens cassés (si détectables)
- Templates non-utilisés
- Dossiers vides
- Recommendations nettoyage

---

### 3️⃣ "synthèse sur [sujet]"

**Trigger :**
```
Claude, synthèse sur Claude + Obsidian
Claude, résumé : ethical hacking
Claude, overview : HexStrike-AI
```

**Action :**
- Recherche cross-vault sur sujet
- Synthétise notes liées
- Crée outline : Concepts clés → Connections → Gaps → Next steps

**Template utilisé :** `_TEMPLATES/RECHERCHE.md`

---

### 4️⃣ "mon budget" / "état financier"

**Trigger :**
```
Claude, mon budget
Claude, état financier 2026
Claude, revenu ce mois
```

**Action :**
- Lit : `PLANNING/BUDGET_2026.md`
- Affiche : Résumé mensualisé + tracking dépenses + projections

---

---

## §2 — PRODUCTIVITÉ & PLANNING

### 1️⃣ "ajoute à mon todo : [tâche]"

**Trigger :**
```
Claude, ajoute à mon todo : créer landing page portfolio
Claude, add task : review HexStrike code
```

**Action :**
- Ajoute dans : `PLANNING/TODO_ACTIF.md`
- Section appropriée (priorité détectée automatiquement)
- Format : Checkbox + description claire + liens si pertinent

**Workflow :**
```
User input → Parse tâche → Déterminer priorité → Ajouter dans TODO → Confirmer
```

---

### 2️⃣ "capture ça : [idée]"

**Trigger :**
```
Claude, capture ça : idée pour service IA
Claude, quick note : bug dans Clawdbot à fixer
```

**Action :**
- Crée : `CAPTURE_RAPIDE/[timestamp].md`
- Format : Template CAPTURE_RAPIDE
- Quick inbox — à traiter/organiser après

**Structure :**
```markdown
---
date: [now]
type: capture
inbox: true  # À organiser
---

# Capture — [titre auto-généré]

[Contenu exact saisi]

---
**À classer dans :** [suggestion]
**Peut créer note :** [note type suggestion]
```

---

### 3️⃣ "planning semaine"

**Trigger :**
```
Claude, planning semaine
Claude, weekly planning
```

**Action :**
- Crée : `PLANNING/PLANNING_SEMAINE_[YYYY-W##].md`
- Analyse TODO_ACTIF
- Distribue tâches par jour
- Identifie blockers

---

### 4️⃣ "nouveau projet : [nom]"

**Trigger :**
```
Claude, nouveau projet : Portfolio freelance
Claude, create project : CTF mastery
```

**Action :**
- Crée dossier : `PROJETS/[nom]/`
- Initialise : Template PROJET.md
- Ajoute à : PROJETS_ACTIFS.md

---

---

## §3 — PRODUCTIVE REVENUE & MONÉTISATION

### 1️⃣ "idée revenu : [description]"

**Trigger :**
```
Claude, idée revenu : service de security audit
Claude, revenu : IA automation pour PME
```

**Action :**
- Crée : `NOTE_PRODUCTIVE_REVENU.md`
- Sections : Problème → Solution → Effort vs. Revenu → Action plan
- Auto-analyse viabilité

**Contenu généré :**
- Pitch client
- Stack requis
- Pricing estimate
- Lead gen strategy

---

### 2️⃣ "pricing : [service]"

**Trigger :**
```
Claude, pricing : security audit service
Claude, calculator : freelance IA rate
```

**Action :**
- Analyse marché
- Génère 3 modèles pricing (hourly, project, value-based)
- Provide ICP (Ideal Customer Profile)
- Competitive positioning

**Output :**
```markdown
## Pricing Analysis — [Service]

### Model 1 : Time-based
$X/h | Rationale | Market comparison

### Model 2 : Project-based
$X flat | Project scope | ROI calculation

### Model 3 : Value-based
X% of savings / $X base | When to use

### Recommended
[Best fit pour votre profil] — Reasoning
```

---

### 3️⃣ "brainstorm revenu"

**Trigger :**
```
Claude, brainstorm revenu
Claude, 10 idées pour monétiser mes compétences
```

**Action :**
- Génère 10 idées originales
- Chacune avec : description + revenu potentiel + effort + timeline
- Ranking par score viabilité/effort

---

### 4️⃣ "service : [service]"

**Trigger :**
```
Claude, service : définir offre IA automation
Claude, create service : ethical hacking training
```

**Action :**
- Crée fiche complète
- Includes : Pitch → Livrables → Pricing → ICP → Differentiators
- Prêt pour portfolio/pitching

---

---

## §4 — ETHICAL HACKING & SECURITY

### 1️⃣ "hacking : [concept/CTF]"

**Trigger :**
```
Claude, hacking : SQL injection exploitation
Claude, ethical hacking : XSS techniques
```

**Action :**
- Crée : `ETHICAL_HACKING_NOTE.md`
- Contient : Theory → Practical → Walkthrough → Defense
- Tags : educational context + level

---

### 2️⃣ "CTF : [challenge]"

**Trigger :**
```
Claude, CTF : HackTheBox — Lame machine
Claude, walkthrough : PicoCTF reverse engineering
```

**Action :**
- Crée : `HACKERGPT/CTF-Walkthroughs/[platform]/[challenge].md`
- Documented step-by-step
- Includes : recon → exploitation → proof → lessons

---

### 3️⃣ "audit sécurité : [système/code]"

**Trigger :**
```
Claude, audit sécurité : HexStrike API
Claude, security review : Clawdbot codebase
```

**Action :**
- Analyse code/architecture fourni
- Génère rapport : Vulnerabilities → Severity → Fix recommendations
- Format : PDF/markdown compatible

---

### 4️⃣ "learning next : ethical hacking"

**Trigger :**
```
Claude, prochain step : ethical hacking
Claude, what's next : after OWASP Top 10
```

**Action :**
- Évalue level courant
- Suggère phase suivante
- Recommande : resources + timeline + CTF practice

---

---

## §5 — CLAUDE WORKFLOWS & AUTOMATION

### 1️⃣ "workflow claude : [description]"

**Trigger :**
```
Claude, workflow claude : créer contenu monétisable
Claude, create workflow : lead generation automation
```

**Action :**
- Crée : `CLAUDE_WORKFLOW.md`
- Documents : Input → Process → Output
- Includes : Prompt template + code examples + metrics

---

### 2️⃣ "API : [tâche]"

**Trigger :**
```
Claude, API : générer rapport quotidien automatiquement
Claude, code : Python script pour synthèse vault
```

**Action :**
- Fournit code Python complet utilisant Claude API
- Explique : Authentication → Request → Processing → Output
- Includes : Error handling + rate limits

---

### 3️⃣ "automation : [process]"

**Trigger :**
```
Claude, automation : capture note → parsing → TODO
Claude, zapier : create lead → contact → CRM
```

**Action :**
- Designs workflow automation
- Tools : Zapier, Make, or custom script
- Includes : trigger → action → logging

---

---

## §6 — VAULT MANAGEMENT & MAINTENANCE

### 1️⃣ "mise à jour mémoire"

**Trigger :**
```
Claude, mise à jour mémoire
Claude, update MEMORY.md
```

**Action :**
- Lit contexte conversation actuelle
- Met à jour : `MEMORY.md`
- Ajoute : patterns éprouvés, découvertes, corrections
- Max 200 lignes — garder concis

---

### 2️⃣ "maintenance vault"

**Trigger :**
```
Claude, maintenance vault
Claude, vault cleanup
```

**Action :**
- Audit complet
- Identifie : notes orphelines, dossiers vides, liens cassés
- Suggestions : archivage, regroupement, tags manquants

---

### 3️⃣ "index : mettre à jour"

**Trigger :**
```
Claude, index : mettre à jour
Claude, rebuild index
```

**Action :**
- Rafraîchit : `_BRAIN/INDEX.md`
- Inclut : Toutes notes + tags + backlinks
- Organized par : Dossier → Date → Type

---

### 4️⃣ "template : [domaine]"

**Trigger :**
```
Claude, template : créer pour notes de meeting
Claude, new template : project review
```

**Action :**
- Crée template markdown réutilisable
- Includes : Front-matter + sections + guidance
- Saved : `_TEMPLATES/[NOUVEAU].md`

---

---

## 📚 Commandes composées (Advanced)

### Multi-step workflows

#### 1️⃣ "idée complète : [concept]"
```
1. Crée NOTE_PRODUCTIVE_REVENU
2. Calcule pricing + ICP
3. Génère pitch client
4. Ajoute to TODO_ACTIF avec deadline
```

---

#### 2️⃣ "CTF mastery : [domaine]"
```
1. Détecte level courant
2. Recommande phase learning
3. Crée checklist + resources
4. Plan walkthroughs à faire
```

---

#### 3️⃣ "portfolio ready : [service]"
```
1. Définit service complètement
2. Crée case study template
3. Génère marketing copy
4. Pricing + ICP documented
5. Ready for outreach
```

---

---

## ⚙️ Configuration requise

### In your system prompt (Prompts/System Prompt/...):
```markdown
## §10 PROTOCOLES VAULT

When user mentions ANY command from this document:
1. Recognize the trigger pattern
2. Execute the action specified
3. Create files in correct location
4. Update DASHBOARD.md if new content
5. Confirm action taken

Use templates from _TEMPLATES/ — never create from scratch.
Update MEMORY.md quarterly with new patterns.
```

---

## §7 — OSINT INVESTIGATIONS (NEW!)

### 1️⃣ "enquête osint : [NOM_CAMPAGNE]"

**Trigger :**
```
enquête osint : PayPal phishing campaign
```

**Action :**
- Crée : `ENQUETES_OSINT/ACTIVES/[OSI-2026-XXX]/investigation.md`
- Format : Template OSINT_INVESTIGATION.md (6 phases complètes)
- Contient : Target profile + IOC tracking + timeline + attribution

**Phases couvertes :**
1. Target Intelligence Gathering (passive OSINT)
2. Data Structuring (framework)
3. IOC Tracking (domains, IPs, hashes, emails)
4. Timeline Construction (chronological reconstruction)
5. Connection Mapping (relationships + infrastructure)
6. Expert Reporting (PDF + legal compliance)

---

### 2️⃣ "analyser iocs : [DESCRIPTION]"

**Trigger :**
```
analyser iocs : 5 domains, 2 IPs, malware hash from phishing campaign
```

**Action :**
- Extrait + valide + normalise IOCs
- Génère JSON enrichi avec threat intelligence
- Crée CSV pour spreadsheet analysis
- Génère règles YARA pour détection

**Output :**
- `ENQUETES_OSINT/IOCs_LIBRARY/iocs_[TIMESTAMP].json`
- `ENQUETES_OSINT/IOCs_LIBRARY/iocs_[TIMESTAMP].csv`
- `ENQUETES_OSINT/REPORTS/yara_rules_[TIMESTAMP].yar`

---

### 3️⃣ "profiler criminel : [NOM_OU_ALIAS]"

**Trigger :**
```
profiler criminel : Emotet gang
```

**Action :**
- Crée profil complet avec background
- Documente capabilities + TTPs (Tactics, Techniques, Procedures)
- Liste infrastructure connue
- Mappe MITRE ATT&CK techniques

**Output :** Section complète dans investigation.md

---

### 4️⃣ "investigation phishing : [DOMAINE]"

**Trigger :**
```
investigation phishing : paypal-security-verify.com
```

**Action :**
- Analyse email headers (SPF/DKIM/DMARC)
- Extrait payload + malware
- Corrèle infrastructure
- Estime nombre de victims

**Output :** Complete phishing investigation with IOCs

---

### 5️⃣ "tracker malware : [HASH_OU_FAMILLE]"

**Trigger :**
```
tracker malware : LockBit 3.0 ransomware
```

**Action :**
- Analyse comportement + code
- Mappe C2 infrastructure
- Documente distribution methods
- Identifie victims

**Output :** Malware distribution network analysis

---

### 6️⃣ "rapport expert osint : [INVESTIGATION_ID]"

**Trigger :**
```
rapport expert osint : OSI-2026-001
```

**Action :**
- Génère PDF professionnel
- Exporte IOCs en JSON structuré
- Vérifie legal compliance (chain of custody, admissibility)
- Recommandations pour law enforcement

**Output :**
- `ENQUETES_OSINT/REPORTS/OSI-2026-001_expert_report.pdf`
- `ENQUETES_OSINT/REPORTS/OSI-2026-001_iocs_export.json`

---

### 7️⃣ "audit sécurité : [CIBLE]" (Pentest)

**Trigger :**
```
audit sécurité : Company X network infrastructure
```

**Action :**
- Documente vulnerabilités trouvées
- Crée chain of custody
- Vérifie authorization
- Recommandations de remédiation

**Output :** Security audit report avec evidence + recommendations

---

### 8️⃣ "corréler infrastructure : [DESCRIPTION]"

**Trigger :**
```
corréler infrastructure : 3 domains with shared nameserver
```

**Action :**
- Analyse shared hosting/nameservers
- Mappe ASN + IP ranges
- Identifie patterns d'infrastructure
- Assigne confidence level (HIGH/MEDIUM/LOW)

**Output :** Infrastructure clustering analysis

---

### 9️⃣ "attribuer à : [ACTOR_NAME]"

**Trigger :**
```
attribuer à : Emotet gang - analyze confidence level
```

**Action :**
- Évalue evidence (technical/behavioral/contextual)
- Documente alternative hypotheses
- Assigne confidence percentage (10-100%)
- Justifie attribution

**Output :** Attribution analysis section

---

### Additional Commands:

**Enrichir IOCs :**
```
enrichir iocs : [CSV_FILE_OU_LISTE]
```
→ Ajoute VirusTotal, Shodan, WHOIS, SSL certs, URLhaus, HIBP data

**Valider IOCs :**
```
valider iocs : [LISTE]
```
→ Format validation + normalization + deduplication

**Créer règles de détection :**
```
yara rules : [MALWARE_FAMILLE]
```
→ Génère règles YARA pour scanners

**Exporter en JSON :**
```
exporter json : [INVESTIGATION_ID]
```
→ IOCs + timeline + attribution en JSON structuré

**Séparer données confidentielles :**
```
séparer pii : [INVESTIGATION_ID]
```
→ Crée 2 fichiers : Technical IOCs + Victim PII (séparé)

**Vérifier conformité légale :**
```
vérifier légalité : [INVESTIGATION_ID]
```
→ Audit : authorization + chain of custody + evidence admissibility

---

### OSINT Resources:

**Full Documentation:**
- [[ENQUETES_OSINT/README_OSINT_SYSTEM]] — System overview
- [[ENQUETES_OSINT/INDEX_OSINT]] — Complete hub
- [[ENQUETES_OSINT/QUICK_COMMANDS]] — Copy-paste reference

**Template:**
- [[_TEMPLATES/OSINT_INVESTIGATION]] — Investigation template (6 phases)

**Reference Files (in plugin skill):**
- `osint-frameworks.md` — OSINT methodology
- `ioc-analysis.md` — IOC handling procedures
- `attribution-techniques.md` — Attribution framework
- `legal-considerations.md` — Jurisdiction-specific laws

**Example Investigations:**
- `example-phishing-campaign.md` — PayPal phishing case (OSI-2025-001)
- `example-malware-distribution.md` — LockBit ransomware case (OSI-2025-002)

**Automation Scripts:**
- `parse-iocs.sh` — Extract + validate IOCs
- `ioc-enricher.py` — Enrich with threat intelligence

---

## 🔍 Quick reference

**Want to create :**
- Revenue idea? → "idée revenu : [desc]"
- Hacking note? → "hacking : [concept]"
- Claude workflow? → "workflow claude : [desc]"
- Project? → "nouveau projet : [nom]"

**Want to analyze :**
- Vault health? → "état du vault"
- Finances? → "mon budget"
- Topic? → "synthèse sur [sujet]"

**Want to organize :**
- Add task? → "ajoute à mon todo : [task]"
- Quick capture? → "capture ça : [idée]"
- Plan week? → "planning semaine"

**Want to develop :**
- Learning path? → "prochain step : [domain]"
- Service? → "pricing : [service]"
- Automation? → "workflow claude : [desc]"

---

## 📞 Support

**Unclear command?** Ask Claude to clarify.
**New need?** Create custom command in PROTOCOLES_VAULT.md.
**Command not working?** Check if template exists in _TEMPLATES/.

---

*Document créé : 2026-02-14*
*Dernière révision : 2026-02-14*
*Version : 1.0*
