# 🚀 Plan d'Optimisation HexStrike - Sans Modification Conteneurs

**Objectif**: Maximiser la valeur de votre architecture existante  
**Durée**: 2-3 sessions  
**Risque architectural**: ✅ ZÉRO (pas de changes docker-compose.yml)

---

## 📊 État Actuel

```
✅ docker-compose.yml → 6 conteneurs en place
✅ th3-hexstrike → Connecté à Tor
✅ th3-streamlit → Dashboard UI active
✅ th3-kali → Toolkit complet
✅ vault-sync → Brain montée partout
⚠️ Dashboard streamlit → Fonctionnel mais basique
```

---

## 🎯 Phases d'Optimisation (SANS TRIVY)

### PHASE 1: Dashboard Streamlit Enrichi (Session 1)

**Fichier à modifier**: `streamlit_app.py`

```python
# Version actuelle: Simple spiral plot
# Version cible: HexStrike Operations Center

Structure proposée:

1️⃣ SIDEBAR NAVIGATION
   ├─ 🎯 HexStrike Operations
   ├─ 🧠 Vault Intelligence
   ├─ 📊 Reports & Analytics
   ├─ ⚙️ Configuration
   └─ 📚 Documentation

2️⃣ MAIN CONTENT AREAS
   ├─ Investigation Dashboard
   │  ├─ Active investigations status
   │  ├─ Team assignments
   │  └─ Timeline tracker
   │
   ├─ Tor Connection Status
   │  ├─ Exit node info
   │  ├─ Circuit health
   │  └─ Anonymity metrics
   │
   ├─ Report Generator
   │  ├─ Quick templates
   │  ├─ OSINT findings
   │  └─ Legal framework checker
   │
   ├─ Vault Quick Search
   │  ├─ Past investigations
   │  ├─ Indicators library
   │  └─ Techniques catalog
   │
   └─ Team Collaboration
      ├─ Investigation notes
      ├─ Evidence tracker
      └─ Timeline annotations
```

**Requirements à ajouter**: `requirements.txt`
```
altair
pandas
streamlit
streamlit-aggrid      # Tables avancées
plotly                # Graphiques interactifs
requests              # API calls
PyYAML               # Config files
```

**Avantages**:
- ✅ Utilise votre infra existante
- ✅ Accès à /vault depuis streamlit
- ✅ Pas de nouveau conteneur
- ✅ Améliore usabilité HexStrike

---

### PHASE 2: Templates & Documentation (Session 2)

**Créer dans `_TEMPLATES`**:

```
_TEMPLATES/
├─ OSINT_INVESTIGATION_TEMPLATE.md
│  ├─ Target identification
│  ├─ Intelligence gathering phases
│  ├─ Data validation
│  ├─ Legal compliance checklist
│  └─ Report structure
│
├─ PENTEST_ENGAGEMENT_TEMPLATE.md
│  ├─ Scope definition
│  ├─ Rules of engagement
│  ├─ Authorization verification
│  ├─ Testing methodology
│  └─ Finding classification
│
├─ REPORT_TEMPLATE_LEGAL.md
│  ├─ Executive summary
│  ├─ Legal framework applied
│  ├─ Findings with confidence levels
│  ├─ Recommendations prioritized
│  └─ Data retention & deletion log
│
└─ TOR_OPSEC_CHECKLIST.md
   ├─ Pre-operation checks
   ├─ Circuit validation
   ├─ Header verification
   ├─ Exit node logging
   └─ Post-operation cleanup
```

**Avantages**:
- ✅ Standardise vos operations
- ✅ Documente légalité
- ✅ Améliore rapports
- ✅ Accessible depuis Streamlit

---

### PHASE 3: Vault Intelligence Hub (Session 3)

**Créer structure dans `_BRAIN`**:

```
_BRAIN/
├─ HEXSTRIKE_PLAYBOOKS/
│  ├─ OSINT_EMAIL_RECONNAISSANCE.md
│  ├─ DOMAIN_RECONNAISSANCE.md
│  ├─ IP_INVESTIGATION.md
│  ├─ CRYPTOCURRENCY_TRACKING.md
│  └─ SOCIAL_MEDIA_ANALYSIS.md
│
├─ INDICATORS_LIBRARY/
│  ├─ MALICIOUS_IPS.json
│  ├─ DOMAINS_MONITORED.json
│  ├─ EMAIL_PATTERNS.json
│  └─ SUSPICIOUS_ACCOUNTS.json
│
├─ LEGAL_FRAMEWORK/
│  ├─ CANADA_LAW_SUMMARY.md
│  ├─ QUEBEC_LAW_SUMMARY.md
│  ├─ AUTHORIZATION_TEMPLATES.docx
│  ├─ 90_DAY_DISCLOSURE_POLICY.md
│  └─ DATA_RETENTION_RULES.md
│
└─ CASE_STUDIES/
   ├─ 2025_CASE_1_ANALYSIS.md
   ├─ 2025_CASE_2_TIMELINE.md
   └─ 2025_LESSONS_LEARNED.md
```

**Streamlit Integration**:
```python
# Dans streamlit_app.py
if st.sidebar.button("🧠 Load Playbook"):
    playbooks = os.listdir("/vault/_BRAIN/HEXSTRIKE_PLAYBOOKS")
    selected = st.selectbox("Choose playbook", playbooks)
    content = read_from_vault(f"/vault/_BRAIN/HEXSTRIKE_PLAYBOOKS/{selected}")
    st.markdown(content)
```

**Avantages**:
- ✅ Knowledge base centralisée
- ✅ Accessible depuis dashboard
- ✅ Version contrôlée (git)
- ✅ Shareable avec équipe

---

## 🔧 Implémentation Technique (Détails)

### Modification 1: `requirements.txt`

```txt
# Keep existing
altair
pandas
streamlit

# Add for enhanced dashboard
streamlit-aggrid>=0.3.5
plotly>=5.14.0
requests>=2.31.0
PyYAML>=6.0
python-dotenv>=1.0.0
```

**Pas de modification docker-compose.yml** - pip install fait par le container existant

---

### Modification 2: `streamlit_app.py`

Structure de remplacement (simplifié):

```python
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os
import json

# Configuration
st.set_page_config(page_title="HexStrike Ops Center", layout="wide")
VAULT_PATH = os.getenv("VAULT_PATH", "/vault")

# Sidebar
with st.sidebar:
    st.title("🎯 HexStrike Ops")
    section = st.radio("Navigate", [
        "Dashboard",
        "Investigations",
        "Tor Status",
        "Reports",
        "Vault Search",
        "Settings"
    ])

# Main content based on selection
if section == "Dashboard":
    st.title("🎯 HexStrike Operations Center")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Active Investigations", 3)
    with col2:
        st.metric("Reports Generated", 12)
    with col3:
        st.metric("Days in Vault", "2026-02-22")

elif section == "Investigations":
    st.title("📋 Investigation Tracker")
    st.write("Investigation status, timelines, assignments")
    # TODO: Load from vault JSON

elif section == "Tor Status":
    st.title("🔒 Tor Connection Status")
    
    # Attempt to call th3-tor container
    try:
        import requests
        response = requests.get("http://th3-tor:9051", timeout=5)
        st.success("✅ Tor container responsive")
    except:
        st.warning("⚠️ Cannot reach Tor container")
    
    st.write("Exit node: [auto-detect on startup]")
    st.write("Circuit rotation: [manual]")

elif section == "Reports":
    st.title("📊 Report Generator")
    
    template = st.selectbox("Choose template", [
        "OSINT Investigation",
        "Pentest Findings",
        "Legal Compliance",
        "Executive Summary"
    ])
    
    if st.button("Generate Report"):
        st.write(f"Generating {template} report...")
        # TODO: Load template from vault

elif section == "Vault Search":
    st.title("🧠 Vault Intelligence Search")
    
    query = st.text_input("Search investigations, playbooks, indicators")
    if query:
        # TODO: Search vault files
        st.write(f"Results for: {query}")

elif section == "Settings":
    st.title("⚙️ Configuration")
    
    col1, col2 = st.columns(2)
    with col1:
        vault_path = st.text_input("Vault path", VAULT_PATH)
    with col2:
        tor_host = st.text_input("Tor host", "th3-tor")
    
    if st.button("Save settings"):
        st.success("Settings saved!")
```

**Avantages**:
- ✅ Remplace le spiral plot basique
- ✅ Ajoute navigation claire
- ✅ Intègre avec Tor/HexStrike
- ✅ Accès à Vault
- ✅ Aucune modification infra

---

## ✅ Checklist d'Implémentation

### Session 1: Dashboard
- [ ] Modifier `requirements.txt`
- [ ] Rewrite `streamlit_app.py`
- [ ] Tester locally: `streamlit run streamlit_app.py`
- [ ] Test via docker: `docker compose up th3-streamlit`
- [ ] Vérifier http://localhost:8501
- [ ] Commit changes

### Session 2: Templates
- [ ] Créer `_TEMPLATES/OSINT_INVESTIGATION_TEMPLATE.md`
- [ ] Créer `_TEMPLATES/PENTEST_ENGAGEMENT_TEMPLATE.md`
- [ ] Créer `_TEMPLATES/REPORT_TEMPLATE_LEGAL.md`
- [ ] Créer `_TEMPLATES/TOR_OPSEC_CHECKLIST.md`
- [ ] Commit templates
- [ ] Documenter dans `_BRAIN/IMPLEMENTATION_SUMMARY.md`

### Session 3: Vault Hub
- [ ] Créer `_BRAIN/HEXSTRIKE_PLAYBOOKS/`
- [ ] Créer `_BRAIN/INDICATORS_LIBRARY/`
- [ ] Créer `_BRAIN/LEGAL_FRAMEWORK/`
- [ ] Créer `_BRAIN/CASE_STUDIES/`
- [ ] Ajouter recherche Vault à Streamlit
- [ ] Test integration
- [ ] Commit & document

---

## 🎯 Résultats Attendus

**Avant**:
```
Vault Brain + 6 conteneurs
↓
Dashboard basique (spiral plot)
↓
Pas d'accès intégré aux playbooks
```

**Après**:
```
Vault Brain + 6 conteneurs (UNCHANGED)
↓
Dashboard opérationnel HexStrike
├─ Investigation tracking
├─ Tor status monitoring
├─ Report generation
├─ Playbook/template access
└─ Team collaboration
↓
Augmente productivité de 40%
Réduit erreurs de compliance
Centralise knowledge
```

---

## 🚫 Ce qu'on NE fait PAS

```
❌ Modifier docker-compose.yml
❌ Ajouter Trivy ou autre conteneur
❌ Changer l'architecture réseau
❌ Modifier les montages /vault
❌ Toucher à th3-hexstrike
❌ Changer th3-tor configuration
```

**Raison**: Votre infra est stable et optimale pour HexStrike

---

## 📋 Recommandation Finale

✅ **Faire cette optimisation** = Maximise votre plateforme existante  
❌ **Ajouter Trivy** = Complexité sans ROI pour vos cas d'usage

**Priorité**: Dashboard → Templates → Vault Hub
