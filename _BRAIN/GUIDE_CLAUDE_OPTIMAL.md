# 🚀 Guide Ultime — Travailler avec Claude à Plein Potentiel
**Date :** 14-02-2026

---

## 🎯 VUE D'ENSEMBLE

Ce guide couvre les **3 piliers** pour maximiser ta collaboration avec Claude :
1. **Skills personnalisés** — Donner à Claude tes propres workflows
2. **MCP (Model Context Protocol)** — Connecter Claude à tes outils
3. **Prompt Engineering** — Communiquer parfaitement avec Claude

---

## 🧩 PILIER 1 — SKILLS PERSONNALISÉS

### C'est quoi un Skill ?
Un **Skill** = un dossier avec un fichier `Skill.md` qui donne à Claude des connaissances spécialisées + des workflows spécifiques à **ton** style de travail.

> ✅ Disponible sur les plans : Pro, Max, Team, Enterprise + Claude Code

---

### Structure d'un Skill (fichier requis)

```
mon-skill/
├── Skill.md          ← OBLIGATOIRE (cœur du skill)
├── REFERENCE.md      ← docs supplémentaires (optionnel)
├── scripts/          ← code exécutable (optionnel)
│   └── script.py
├── references/       ← fichiers de référence (optionnel)
└── assets/           ← templates, images, données (optionnel)
```

---

### Template Skill.md — Copier/Coller

```yaml
---
name: nom-du-skill
description: |
  Ce que fait le skill et QUAND l'utiliser.
  Ex: Applique mes directives de marque à tous mes documents.
  Utilise quand je crée une présentation ou un rapport.
---

## Vue d'ensemble
[Explique le but du skill en 2-3 phrases]

## Instructions
1. Étape 1...
2. Étape 2...
3. Étape 3...

## Exemples
**Input :** [exemple de requête]
**Output :** [exemple de résultat attendu]

## Quand utiliser ce skill
- Cas d'usage 1
- Cas d'usage 2

## Ressources
Voir [REFERENCE.md](references/REFERENCE.md) pour les détails.
```

---

### Règles d'or pour les Skills

| Règle | Pourquoi |
|-------|----------|
| **Nom en minuscules** avec tirets | Ex: `code-review` pas `Code Review` |
| **Description précise** (max 1024 car.) | Claude l'utilise pour décider d'activer le skill |
| **Un skill = une tâche** | Plusieurs petits skills > un gros skill |
| **Commence simple** | Markdown d'abord, code ensuite |
| **< 500 lignes** dans Skill.md | Mettre le reste dans des fichiers référencés |

---

### Packaging & Upload

1. Zippe le dossier : `mon-skill.zip > mon-skill/ > Skill.md`
2. Va dans **Claude > Paramètres > Capacités**
3. Upload le ZIP
4. Active le skill
5. Teste avec plusieurs prompts pour vérifier l'activation

---

### Checklist avant upload

- [ ] Le nom du dossier = le nom dans le YAML
- [ ] La description dit QUOI + QUAND
- [ ] Tous les fichiers référencés existent
- [ ] Pas de clés API ou mots de passe dans le code
- [ ] Testé avec des exemples de prompts

---

## 🔌 PILIER 2 — MCP (MODEL CONTEXT PROTOCOL)

### C'est quoi le MCP ?
Le MCP = une prise **USB-C universelle** pour connecter Claude à n'importe quel outil externe.

```
Claude (MCP Host)
    ↓
MCP Client (connection manager)
    ↓
MCP Server (ton outil : fichiers, API, DB, apps...)
```

---

### Les 3 Primitives MCP (ce que tu peux exposer)

| Primitive | Quoi | Exemple |
|-----------|------|---------|
| **Tools** | Fonctions que Claude peut appeler | Rechercher dans ta DB, créer un fichier |
| **Resources** | Données/contexte que Claude peut lire | Contenu de fichiers, schéma DB |
| **Prompts** | Templates réutilisables | Prompts système, few-shot examples |

---

### Types de MCP Servers

**Local (STDIO)** — Tourne sur ta machine
- Communication via stdin/stdout
- Idéal : accès fichiers locaux, apps desktop
- Ex: serveur filesystem, git, sqlite

**Remote (HTTP)** — Tourne sur le cloud
- Communication via HTTP + Server-Sent Events
- Idéal : APIs externes, services web
- Ex: GitHub MCP, Notion MCP, Google Calendar MCP

---

### MCP Servers Essentiels à Installer

| Serveur | Ce que ça fait | Priorité |
|---------|---------------|----------|
| **filesystem** | Lire/écrire tes fichiers locaux | ⭐⭐⭐ |
| **git** | Gérer tes repos Git | ⭐⭐⭐ |
| **fetch** | Faire des requêtes web | ⭐⭐⭐ |
| **sqlite** | Interroger des bases SQLite | ⭐⭐ |
| **github** | GitHub API complet | ⭐⭐ |
| **notion** | Lire/écrire dans Notion | ⭐⭐ |
| **google-calendar** | Gérer ton calendrier | ⭐⭐ |
| **obsidian** | Lire/écrire dans Obsidian | ⭐⭐⭐ |

---

### Step-by-Step : Créer ton premier MCP Server (Python)

**Structure minimale :**
```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("mon-serveur")

@mcp.tool()
def ma_fonction(parametre: str) -> str:
    """Description claire de ce que fait l'outil."""
    return f"Résultat: {parametre}"

if __name__ == "__main__":
    mcp.run()
```

**Connecter à Claude Desktop :**
```json
// ~/Library/Application Support/Claude/claude_desktop_config.json
{
  "mcpServers": {
    "mon-serveur": {
      "command": "python",
      "args": ["/chemin/vers/mon_serveur.py"]
    }
  }
}
```

---

### Bonnes Pratiques MCP

- **Valider toutes les entrées** côté serveur
- **Rate limiting** pour éviter les abus
- **Logs** pour auditer les appels d'outils
- **Timeout** sur tous les appels (évite les blocages)
- **Descriptions claires** : Claude utilise la description pour décider d'utiliser l'outil
- **Noms explicites** : `get_weather_data` > `weather`
- **Output Schema** : définir la structure de sortie pour validation

---

### Découverte de MCP Servers Existants

- 🌐 **mcp.so** — Répertoire officiel de serveurs MCP
- 🔍 **smithery.ai** — Marketplace MCP
- 📦 **GitHub Anthropic** — Serveurs officiels

---

## ✍️ PILIER 3 — PROMPT ENGINEERING (PARLER À CLAUDE)

### Les 6 Techniques Fondamentales

#### 1. Sois Clair et Direct
> Claude = nouvel employé brillant sans contexte. Donne-lui **tout** le contexte.

```
❌ "Améliore mon email"
✅ "Tu es un copywriter expert B2B. Réécris cet email de prospection 
   pour un PDG de PME tech. Objectif : obtenir un meeting de 30min. 
   Ton : professionnel mais humain. Max 150 mots."
```

#### 2. Utilise les Balises XML
Sépare clairement les parties de ton prompt :
```xml
<instructions>
  Analyse ce contrat et identifie les risques critiques.
</instructions>

<context>
  Je suis directeur juridique d'une startup SaaS.
</context>

<document>
  [contenu du contrat]
</document>

<format>
  Liste numérotée par ordre de sévérité.
</format>
```

#### 3. Donne un Rôle à Claude (System Prompt)
```
"Tu es un data scientist senior spécialisé en analyse client 
pour des entreprises Fortune 500. Tu parles français, 
tu vas droit au but, tu fournis des insights actionnables."
```

#### 4. Multishot (Exemples)
Montre 2-3 exemples input/output pour calibrer le style :
```
Input: [exemple 1] → Output: [résultat 1]
Input: [exemple 2] → Output: [résultat 2]
Input: [ton vrai input]
```

#### 5. Chain of Thought (Laisse Réfléchir)
```
"Avant de répondre, réfléchis étape par étape dans des balises 
<thinking>, puis donne ta réponse finale dans <answer>."
```

#### 6. Chaîner les Prompts
Décompose les tâches complexes en étapes :
```
Step 1 : "Analyse ce problème et liste les sous-tâches"
Step 2 : "Pour chaque sous-tâche, propose une solution"  
Step 3 : "Synthétise en plan d'action prioritaire"
```

---

### Template de Prompt Universel

```
[RÔLE] Tu es [expert en quoi].

[CONTEXTE] Je suis [qui tu es]. J'ai besoin de [quoi] parce que [pourquoi].

[TÂCHE] [Instruction claire et spécifique, étapes si nécessaire]

[EXEMPLES] (si pertinent)
Input: ... → Output: ...

[FORMAT] Réponds en [format : liste / tableau / texte / code].
[CONTRAINTES] Max [longueur]. Ton : [formel/décontracté/technique].
```

---

## ⚡ WORKFLOW RECOMMANDÉ — TON SETUP OPTIMAL

### Setup en 3 Phases

**Phase 1 — Fondations (Semaine 1)**
- [ ] Installer Claude Desktop
- [ ] Activer l'exécution de code (Paramètres > Capacités)
- [ ] Installer MCP filesystem + fetch
- [ ] Créer ton premier skill simple (ex: "Mon style d'écriture")

**Phase 2 — Expansion (Semaine 2-3)**
- [ ] Installer MCP Obsidian (pour notes bidirectionnelles)
- [ ] Installer MCP GitHub (pour tes projets code)
- [ ] Créer 3-5 skills pour tes workflows récurrents
- [ ] Maîtriser les balises XML dans tes prompts

**Phase 3 — Maîtrise (Semaine 4+)**
- [ ] Créer des MCP servers custom pour tes besoins uniques
- [ ] Composer des skills entre eux
- [ ] Utiliser Claude Code pour les projets tech
- [ ] Documenter tes prompts qui marchent dans Obsidian

---

## 🔒 SÉCURITÉ — Les Règles Immuables

- ❌ Ne jamais coder en dur des clés API dans les Skills/MCP
- ❌ Ne jamais activer un Skill téléchargé sans l'avoir lu
- ✅ Utiliser des variables d'environnement pour les credentials
- ✅ Toujours vérifier les permissions des MCP servers
- ✅ Un humain doit valider les actions sensibles (suppression, envoi)

---

## 📚 RESSOURCES OFFICIELLES

| Ressource | URL | Pour quoi |
|-----------|-----|-----------|
| Support Claude | support.claude.com | Skills officiels |
| Docs Anthropic | docs.anthropic.com | API + Prompt Engineering |
| MCP Officiel | modelcontextprotocol.io | Architecture MCP |
| Agent Skills Spec | agentskills.io | Standard ouvert Skills |
| Skills GitHub | github.com/anthropics/skills | Exemples de Skills |
| MCP Registry | registry.smithery.ai | Serveurs MCP disponibles |

---

## 💡 TIPS RAPIDES

> **La description du Skill est CRITIQUE** — C'est ce que Claude lit pour décider d'activer ton skill. Sois très spécifique sur le QUAND.

> **Commence par un skill Markdown pur** — Pas besoin de code pour 80% des cas d'usage. Ajoute du code seulement si nécessaire.

> **Les Skills se composent** — Claude peut utiliser plusieurs skills automatiquement ensemble. Crée des skills focalisés et laisse Claude les combiner.

> **Teste avec des variantes de prompt** — Si Claude n'active pas ton skill, ajuste la description. Elle doit contenir les mots-clés que tu utilises naturellement.

> **MCP + Skills = combo puissant** — Tes Skills donnent le COMMENT faire, tes MCP servers donnent l'ACCÈS aux données et outils.

---

## 🔗 LIENS CONNEXES

- [[CLAUDE_WORKFLOW]] — Workflows Claude avec code
- [[PROTOCOLES_VAULT]] — Commandes déclencheurs (30+)
- [[COMPETENCES_CLAUDE_OBSIDIAN]] — Compétences avancées
- [[MEMORY]] — Système mémoire persistant
- [[DASHBOARD]] — Hub central du Vault

---

**Guide créé le 14-02-2026**  
**Sources :** support.claude.com · docs.anthropic.com · modelcontextprotocol.io · agentskills.io

---

#claude #skills #mcp #prompt-engineering #workflow #automation #guide #14-02-2026