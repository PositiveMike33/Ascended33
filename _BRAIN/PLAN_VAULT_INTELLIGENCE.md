---
date: 2026-02-14
type: plan-fondateur
statut: complété
tags: [_brain, plan, vault-intelligence]
---

# 📐 PLAN FONDATEUR — Vault Intelligence System

> **Ce fichier est la référence absolue pour comprendre pourquoi ce système existe et comment il est structuré.**
> Claude doit le lire quand il a besoin de se réaligner sur l'objectif fondamental.

---

## Contexte

Michaël G. Guillet utilise un vault Obsidian de 608 notes comme base de connaissance personnelle couvrant : cybersécurité, IA/LLM, astrologie, neuroscience, freelance, finance et journaux quotidiens. Il veut que Claude devienne un **agent actif** dans ce vault — capable de créer, optimiser, analyser et gérer ses notes via les outils MCP disponibles.

**Problème actuel :** Le vault est riche mais passif. Il n'existe pas de système structuré pour la planification quotidienne, le suivi budgétaire, les rappels, la génération automatique de rapports, ni de protocole de maintenance.

**Résultat attendu :** Un "second cerveau" où Claude peut être invoqué pour exécuter des opérations concrètes sur le vault : créer des notes sur mesure, auditer le contenu, synthétiser des informations cross-domaines, et maintenir la santé du vault.

---

## Infrastructure existante à exploiter

| Outil | Rôle dans le système |
|-------|---------------------|
| `Desktop Commander` MCP | Lecture/écriture/recherche de fichiers — outil principal de Claude Code |
| `mcp-tools` plugin Obsidian | Connexion Claude Desktop ↔ vault (semantic search, file ops) |
| `obsidian-local-rest-api` | HTTP API vers le vault pour automatisation externe |
| `Cannoli` plugin | Workflows LLM automatisés sur Canvas (Gemini configuré) |
| `RAPPORT QUOTIDIEN/` | Pattern existant de journaux quotidiens à standardiser |
| `Prompts/System Prompt/` | Système prompt VAULT existant à enrichir |

---

## Phase 1 — Fondations ✅ COMPLÉTÉ

### Structure créée
```
D:\Vault\Vault\
├── _BRAIN/
│   ├── DASHBOARD.md        ← Hub central
│   ├── MEMOIRE.md          ← Contexte persistant
│   ├── INDEX.md            ← Index du vault
│   ├── AUDIT.md            ← Santé & maintenance
│   └── PLAN_VAULT_INTELLIGENCE.md  ← Ce fichier
├── _TEMPLATES/
│   ├── RAPPORT_QUOTIDIEN.md
│   ├── PLANNING_HEBDO.md
│   ├── TODO.md
│   ├── BUDGET.md
│   ├── PROJET.md
│   ├── RECHERCHE.md
│   └── CAPTURE_RAPIDE.md
├── PLANNING/
│   ├── TODO_ACTIF.md
│   ├── PROJETS_ACTIFS.md
│   └── BUDGET_2026.md
└── ARCHIVE/
```

### System prompt enrichi
Fichier : `Prompts/System Prompt/SYSTEM PROMPT — Assistant Personnel Agentique Multi-Tâche.md`
Section §10 PROTOCOLES VAULT ajoutée avec 13 commandes déclencheurs.

---

## Phase 2 — Agent VAULT Enrichi ✅ COMPLÉTÉ

### Commandes déclencheurs actives

| Trigger | Action |
|---------|--------|
| `"rapport de ce soir"` | Créer rapport dans `RAPPORT QUOTIDIEN/{{date}}/` |
| `"ajoute à mon todo : X"` | Ajouter dans `PLANNING/TODO_ACTIF.md` |
| `"capture ça : X"` | Créer depuis `_TEMPLATES/CAPTURE_RAPIDE.md` |
| `"état du vault"` | Lire `_BRAIN/AUDIT.md` |
| `"synthèse sur [sujet]"` | Recherche cross-notes → `_TEMPLATES/RECHERCHE.md` |
| `"mon budget"` | Lire `PLANNING/BUDGET_2026.md` |
| `"mise à jour mémoire"` | Mettre à jour `_BRAIN/MEMOIRE.md` |
| `"nouveau projet : X"` | Créer depuis `_TEMPLATES/PROJET.md` |
| `"planning semaine"` | Créer depuis `_TEMPLATES/PLANNING_HEBDO.md` |
| `"mes projets"` | Lire `PLANNING/PROJETS_ACTIFS.md` |
| `"audit complet"` | Scan deep : liens brisés, orphelins, sans frontmatter |
| `"archive les vieux rapports"` | Archiver RAPPORT QUOTIDIEN > 90 jours |
| `"mise à jour index"` | Régénérer `_BRAIN/INDEX.md` |

---

## Phase 3 — Intelligence Cross-Notes (à venir)

### 3.1 Workflow de synthèse
Claude utilise Desktop Commander pour :
1. Rechercher par mot-clé dans tout le vault (`start_search` avec `searchType: content`)
2. Lire les notes pertinentes
3. Créer une note de synthèse depuis `_TEMPLATES/RECHERCHE.md`
4. Ajouter des backlinks dans les notes sources

### 3.2 INDEX.md auto-généré
- Index par domaine (Cybersécurité, IA, Finance, Astrologie, etc.)
- Index par type de note (projet, recherche, capture, rapport)
- Notes orphelines à traiter
- Notes à enrichir (sans tags, sans frontmatter)

### 3.3 Cannoli Canvas (automatisation Gemini) — À configurer
Fichier cible : `_BRAIN/CANNOLI_WORKFLOWS.canvas`
- **Workflow A :** Générer rapport quotidien automatique depuis todo du jour
- **Workflow B :** Synthèse hebdomadaire des rapports quotidiens
- **Workflow C :** Alerte budget si dépenses > seuil configuré

---

## Vérification (checklist de validation)

- [x] Dossiers `_BRAIN/` et `_TEMPLATES/` créés et visibles dans Obsidian
- [x] `DASHBOARD.md` — tous les liens cliquables
- [ ] Tester `"rapport de ce soir"` → note créée au bon endroit
- [ ] Tester `"état du vault"` → Claude lit AUDIT.md
- [ ] Tester `"mon budget"` → Claude lit BUDGET_2026.md
- [ ] Tester `"capture ça : idée X"` → note créée dans bon dossier
- [ ] Configurer Cannoli workflows (Phase 3)

---

*Plan fondateur archivé le 2026-02-14 | [[_BRAIN/DASHBOARD]]*
