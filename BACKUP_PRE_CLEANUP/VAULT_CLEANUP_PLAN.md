# 🧹 Plan de Nettoyage du Vault — Organisation Complète

**Status:** 📋 Plan créé | ⏳ À exécuter
**Date:** 2026-02-20
**Objectif:** Structure propre, identifiable et optimisée

---

## 🔴 Problèmes Identifiés

### 1. **DOUBLONS MAJEURS**

| Dossier | Type | Action |
|---------|------|--------|
| `HACKERGPT/` & `Declassified/Cybersécurité/` | Duplicate complet | ❌ Supprimer `Declassified/` |
| `Notes et Mémos Importants/` & `Classified Report/` | Duplicate complet | ❌ Supprimer `Classified Report/` |
| `LLM's/Gemini/Gemini 1/` | Nested duplicate | ❌ Supprimer sous-dossier `Gemini 1/` |
| `Index.md` (racine) | Config Obsidian | ✅ Keeper si utilisé |

### 2. **STRUCTURE CONFUSE**

```
D:\Vault\Vault\
├── Declassified/              ❌ Doublons de HACKERGPT
├── Classified Report/         ❌ Doublons de Notes et Mémos
├── HACKERGPT/                 ❌ À renommer
├── LLM's/                     ❌ Structure bizarre
├── Notes et Mémos Importants/ ❌ Nom trop long
├── HexStrike/                 ✅ NEW - Keeper
├── Security/                  ✅ NEW - Keeper
├── THIRTY3/                   ✅ NEW - Keeper
├── _BRAIN/                    ✅ Core - Keeper
└── [d'autres...]              ⚠️ À nettoyer
```

### 3. **FICHIERS NON-ORGANISÉS**
- `.devcontainer/` — Devrais être en `_INFRASTRUCTURE/`
- `.github/` — Devrais être en `_INFRASTRUCTURE/`
- `Apprentissage/` — Doublons de `THIRTY3/`
- `HexStrike/` — Bon, mais besoin de documentation
- Security files éparpillés

---

## ✨ NOUVELLE STRUCTURE PROPOSÉE

```
D:\Vault\Vault\
│
├── 📚 _BRAIN/                    [HUB CENTRAL]
│   ├── DASHBOARD.md              ← Point d'entrée
│   ├── PROJECT_INDEX.md
│   ├── PROTOCOLES_VAULT.md
│   ├── MASTERCLASS/
│   ├── MEMOIRE/
│   └── AUDIT.md
│
├── 🎯 _PROJECTS/                 [4 PROJETS ACTIFS]
│   ├── 🔐_SECURITY_AUDIT/        Revenue project
│   ├── 🤖_PIECES_INTEGRATION/    Memory system
│   ├── 🐧_KALI_LEARNING/         Hacking labs
│   └── 🧠_CLAUDE_MASTERY/        Automation
│
├── 🔧 _INFRASTRUCTURE/           [TECH SETUP]
│   ├── .devcontainer/
│   ├── .github/
│   ├── Ascended33/               Git submodule
│   ├── docker-compose.yml
│   └── HEXSTRIKE_DOCKER_GUIDE.md
│
├── 📋 PLANNING/                  [ORGANISATION]
│   ├── TODO_ACTIF.md
│   ├── BUDGET_2026.md
│   ├── PROJETS_ACTIFS.md
│   └── CALENDRIER_HEBDO.md
│
├── 🔍 SECURITY/                  [OSINT + HACKING]
│   ├── OSINT/                    Investigations
│   ├── OPERATIONS/               Security ops
│   ├── TOOLS/                    HexStrike tools
│   └── LEARNING/                 Phase 1-4 curriculum
│
├── 📚 LEARNING/                  [RESSOURCES EDUCA]
│   ├── PHASE_1_FUNDAMENTALS/     Basics
│   ├── PHASE_2_INTERMEDIATE/     Tools
│   ├── PHASE_3_ADVANCED/         Exploitation
│   ├── PHASE_4_CERTIFICATION/    OSCP prep
│   └── CTF_WALKTHROUGHS/         Solutions
│
├── 💡 KNOWLEDGE/                 [REFERENCE]
│   ├── CLAUDE_WORKFLOWS/         Automation docs
│   ├── HACKING_METHODS/          OWASP + techniques
│   ├── OSINT_METHODS/            Investigation patterns
│   ├── REVENUE_TEMPLATES/        Business models
│   └── CODING_SNIPPETS/          Reusable code
│
├── 📊 REPORTS/                   [DOCUMENTATION]
│   ├── DAILY/                    Rapports quotidiens
│   ├── WEEKLY/                   Rapports hebdomadaires
│   ├── MONTHLY/                  Rapports mensuels
│   └── INVESTIGATIONS/           OSINT reports
│
├── 🎬 THIRTY3/                   [DAILY TRACKER]
│   ├── daily/2026/02/            Learning progress
│   ├── Constitution/             Framework
│   ├── Protocoles/               Procedures
│   └── Templates/                Templates
│
├── 🌐 EXTERNAL/                  [INTEGRATIONS]
│   ├── PIECES_SNIPPETS/          Code library
│   ├── ZAPIER_WORKFLOWS/         Automation
│   └── API_CONNECTIONS/          External services
│
└── 📄 [ROOT FILES]
    ├── README.md                 ← Nouvelle doc
    ├── CLAUDE.md                 ← Instructions Claude
    ├── .claude/memory/           ← Auto memory
    └── VAULT_STRUCTURE.md        ← Cette structure
```

---

## 📋 ÉTAPES DE NETTOYAGE

### Phase 1: Supprimer les Doublons (20 min)
```bash
# 1. Vérifier contenu et fusionner si besoin
diff -r Declassified/ HACKERGPT/
diff -r "Classified Report/" "Notes et Mémos Importants/"
diff -r LLM\'s/Gemini/Gemini\ 1/ LLM\'s/Gemini/

# 2. Supprimer les doublons
rm -rf Declassified/
rm -rf "Classified Report/"
rm -rf LLM\'s/Gemini/Gemini\ 1/
rm -rf Apprentissage/
```

### Phase 2: Reorganiser (30 min)
```bash
# 1. Créer structure principale
mkdir -p _INFRASTRUCTURE _PROJECTS PLANNING SECURITY LEARNING KNOWLEDGE REPORTS EXTERNAL

# 2. Déplacer fichiers de configuration
mv .devcontainer/ _INFRASTRUCTURE/
mv .github/ _INFRASTRUCTURE/
mv Ascended33 _INFRASTRUCTURE/

# 3. Déplacer projets
mv 🔐_SECURITY_AUDIT_PROJECT _PROJECTS/
mv 🤖_PIECES_OS_INTEGRATION _PROJECTS/
mv 🐧_KALI_INTEGRATION_PROJECT _PROJECTS/
mv 🧠_CLAUDE_MASTERY _PROJECTS/

# 4. Déplacer planning
mkdir -p PLANNING
mv "Notes et Mémos Importants/Notes rapide/PLANNING/"* PLANNING/

# 5. Fusionner Security
mv HexStrike SECURITY/TOOLS
mv Security/OSINT SECURITY/
mv Security/Operations SECURITY/

# 6. Reorganiser Learning
mkdir -p LEARNING
mv HACKERGPT/HEXSTRIKE LEARNING/TOOLS (ou dans SECURITY)
# Créer structure Phase 1-4
```

### Phase 3: Documenter (15 min)
```bash
# Créer fichiers de navigation
README.md                    ← Guide d'utilisation
VAULT_STRUCTURE.md          ← Cette structure
NAVIGATION.md               ← Liens rapides
```

### Phase 4: Updater Liens (15 min)
- Mettre à jour DASHBOARD.md
- Mettre à jour tous les [[liens]] internes
- Vérifier les références de fichiers

---

## 🎯 RÈGLES DE STRUCTURE

### Noms de Dossiers
✅ **À FAIRE:**
- `_BRAIN/` — Underscore = Core system
- `PLANNING/` — CAPS = Main categories
- `SECURITY/TOOLS/` — Nested = Related items
- `2026/02/` — Dates = Time-based

❌ **À ÉVITER:**
- Noms avec espaces (utiliser underscores)
- Doublons même partiels
- Acronymes confus (HACKERGPT → LEARNING/HACKING)
- Niveaux de nesting > 4

### Noms de Fichiers
✅ **À FAIRE:**
- `2026-02-20-investigation.md` — Date prefix
- `INDEX_OSINT.md` — CAPS pour index
- `README_PROJECT.md` — README en caps
- `_TEMPLATE_NOTE.md` — Underscore = Templates

❌ **À ÉVITER:**
- Espaces et caractères spéciaux
- Noms génériques (Note1.md, Doc.md)
- Majuscules irrégulières

---

## 📊 IMPACT DU NETTOYAGE

### Avant
- 650+ notes dispersées
- 8+ dossiers avec doublons
- Navigation confuse
- ~500MB de fichiers dupliqués

### Après
- 650+ notes organisées
- Structure claire et hiérarchique
- Navigation unifiée
- ~50MB gain (doublons supprimés)
- **100% identifiable**

---

## ✅ CHECKLIST DE VALIDATION

Après nettoyage:
- [ ] Aucun dossier dupliqué
- [ ] Structure cohérente (max 4 niveaux)
- [ ] Tous les liens [[...]] fonctionnent
- [ ] DASHBOARD.md à jour
- [ ] README.md présent
- [ ] VAULT_STRUCTURE.md actuel
- [ ] 0 fichiers orphelins
- [ ] git diff propre (doublons disparus)
- [ ] Obsidian graph visuel et lisible
- [ ] Tous les projets accessibles

---

## 🚀 Commandes Résumées

```bash
# 1. Supprimer doublons
rm -rf Declassified/ "Classified Report/" LLM\'s/Gemini/Gemini\ 1/ Apprentissage/

# 2. Créer structure
mkdir -p _INFRASTRUCTURE _PROJECTS PLANNING SECURITY LEARNING KNOWLEDGE REPORTS EXTERNAL

# 3. Déplacer .devcontainer et .github
mv .devcontainer/ _INFRASTRUCTURE/
mv .github/ _INFRASTRUCTURE/

# 4. Déplacer Ascended33
mv Ascended33 _INFRASTRUCTURE/

# 5. Déplacer projets (si nommés avec emoji)
# mv 🔐_SECURITY_AUDIT_PROJECT _PROJECTS/
# mv 🤖_PIECES_OS_INTEGRATION _PROJECTS/
# mv 🐧_KALI_INTEGRATION_PROJECT _PROJECTS/
# mv 🧠_CLAUDE_MASTERY _PROJECTS/

# 6. Réorganiser contenu principal
# mkdir -p PLANNING && mv Notes\ et\ Mémos*/Notes\ rapide/PLANNING/* PLANNING/

# 7. Nettoyage final
rm -rf LLM\'s/ "Notes et Mémos Importants/" Index.md (si seulement config Obsidian)

# 8. Commit
git add -A
git commit -m "vault: comprehensive cleanup and reorganization"
```

---

## 📌 Priorisation

**URGENTS** (À faire immédiatement):
1. Supprimer Declassified/ (doublons HACKERGPT)
2. Supprimer Classified Report/ (doublons Notes)
3. Supprimer doublons LLM's/Gemini 1/

**IMPORTANTS** (Cette semaine):
4. Réorganiser en structure _PROJECTS, PLANNING, SECURITY
5. Mettre à jour tous les liens
6. Créer README.md et VAULT_STRUCTURE.md

**OPTIONNELS** (Prochaine semaine):
7. Renommer HACKERGPT en nom plus clair
8. Compléter la structure LEARNING/PHASE_1-4
9. Fusionner HexStrike docs en une seule location

---

**Prêt pour nettoyage! 🧹✨**

