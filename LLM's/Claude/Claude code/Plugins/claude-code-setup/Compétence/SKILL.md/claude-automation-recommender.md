---
name: claude-automation-recommender
description: Analysez une base de code et recommandez des automatisations Claude Code (hooks, sous-agents, compétences, plugins, serveurs MCP). À utiliser lorsque l'utilisateur demande des recommandations d'automatisation, souhaite optimiser sa configuration Claude Code, mentionne l'amélioration des workflows Claude Code, demande comment configurer Claude Code pour un projet ou souhaite savoir quelles fonctionnalités Claude Code il devrait utiliser.
tools: Read, Glob, Grep, Bash
---

# Recommandateur Claude Automation

Analysez les modèles de base de code pour recommander des automatisations Claude Code adaptées à toutes les options d'extensibilité.

**Cette compétence est en lecture seule. Elle analyse la base de code et émet des recommandations. Elle ne crée ni ne modifie aucun fichier. Les utilisateurs mettent en oeuvre les recommandations eux-mêmes ou demandent à Claude Code de les aider à les construire.

## Directives de sortie

- Recommandez 1 à 2 automatismes de chaque type** : Ne vous laissez pas submerger - présentez les 1 à 2 automatismes les plus utiles par catégorie.
- Si l'utilisateur demande un type spécifique** : Si l'utilisateur demande un type spécifique** : concentrez-vous uniquement sur ce type et fournissez plus d'options (3-5 recommandations).
- Allez au-delà des listes de référence** : Les fichiers de référence contiennent des modèles communs, mais utilisez la recherche sur le web pour trouver des recommandations spécifiques aux outils, frameworks et bibliothèques de la base de code.
- Dites aux utilisateurs qu'ils peuvent en demander plus** : Terminez en indiquant que les utilisateurs peuvent demander plus de recommandations pour une catégorie spécifique.

## Aperçu des types d'automatisation

| Type d'automatisation
|------|----------|
| Les outils d'automatisation sont des outils qui permettent d'effectuer des actions automatiques sur les événements de l'outil (format sur l'enregistrement, lint, bloc d'édition).
| Les sous-groupes de travail **Sous-agents** | Réviseurs/analyseurs spécialisés qui fonctionnent en parallèle |
| Compétences : expertise, flux de travail et tâches répétables (invoqués par Claude ou l'utilisateur via `/skill-name`).
**Plugins** | Collections de compétences qui peuvent être installées sur votre ordinateur.
| Serveurs MCP** | Intégrations d'outils externes (bases de données, API, navigateurs, documents)

## Workflow

### Phase 1 : Analyse de la base de code

Recueillir le contexte du projet :

```bash
# Détecter le type de projet et les outils
ls -la package.json pyproject.toml Cargo.toml go.mod pom.xml 2>/dev/null
cat package.json 2>/dev/null | head -50

# Vérifier les dépendances pour les recommandations du serveur MCP
cat package.json 2>/dev/null | grep -E '"(react|vue|angular|next|express|fastapi|django|prisma|supabase|stripe)"'

# Vérifier la présence d'une configuration Claude Code existante
ls -la .claude/ CLAUDE.md 2>/dev/null

# Analyser la structure du projet
ls -la src/ app/ lib/ tests/ composants/ pages/ api/ 2>/dev/null
```

**Indices clés à capturer:**

| Les indicateurs clés à capturer sont les suivants : - Catégorie - Ce qu'il faut rechercher - Recommandations pour les catégories - Les indicateurs clés à capturer sont les suivants
|----------|------------------|----------------------------|
| Langue/Cadre de travail : package.json, pyproject.toml, modèles d'importation : Hooks, serveurs MCP, etc.
| MCP Playwright, compétences frontales | MCP Playwright, compétences frontales | MCP Playwright, compétences frontales | MCP Playwright, compétences frontales
| Express, FastAPI, Django | Outils de documentation d'API | Base de données
| Base de données | Prisma, Supabase, raw SQL | Serveurs MCP de base de données | API externes
| APIs externes | Stripe, OpenAI, AWS SDKs | context7 MCP pour les docs |
| Tests - Jest, pytest, Playwright configs - Testing hooks, subagents - CI/CD - GitHealth - GitHealth - GitHealth - GitHealth - GitHealth
| CI/CD | GitHub Actions, CircleCI | GitHub MCP server |
| Suivi d'incidents | Linéaire, références Jira | Suivi d'incidents MCP
| OpenAPI, JSDoc, docstrings | Compétences en matière de documentation

### Phase 2 : Générer des recommandations

Sur la base de l'analyse, générez des recommandations dans toutes les catégories :

#### A. Recommandations concernant le serveur MCP

Voir [references/mcp-servers.md](mcp-servers.md.md) pour des modèles détaillés.

| Vous pouvez également consulter la liste des serveurs MCP recommandés dans la base de données Codebase Signal.
|-----------------|------------------------|
| Le serveur MCP recommandé est Signal, qui utilise des bibliothèques populaires (React, Express, etc.).
| Les utilisateurs ont besoin de tester l'interface utilisateur de leur site web.
| Le système de gestion de la base de données utilise Supabase | **Supabase MCP** - Opérations directes sur la base de données
| Base de données PostgreSQL/MySQL **Database MCP** - Outils de requête et de schéma
| Dépôt GitHub **GitHub MCP** - Problèmes, PRs, actions
| MCP** - Gestion des problèmes - MCP**Linéaire - Gestion des problèmes - MCP**Linéaire
| MCP** AWS - Gestion des ressources du cloud
| Le système de gestion de l'espace de travail de Slack
| MCP** - Mémoire et persistance du contexte
| Gestion de l'espace de travail Slack - **Slack MCP** - Notifications d'équipe
| Gestion des conteneurs Docker | **Docker MCP** - Gestion des conteneurs

#### B. Recommandations en matière de compétences

Voir [references/skills-reference.md] (references/skills-reference.md) pour plus de détails.

Créez des compétences dans `.claude/skills/<nom>/SKILL.md`. Certaines sont également disponibles via des plugins :

| Vous pouvez également accéder à certaines d'entre elles via des plugins : - Codebase Signal - Skill - Plugin - Codebase Signal - Skill - Plugin
|-----------------|-------|--------|
| Construction de plugins | skill-development | plugin-dev |
| Git commits | commit | commands | commit-commands |
| React/Vue/Angular | frontend-design | frontend-design | React/Vue/Angular | React/Vue/Angular | frontend-design | frontend-design
| règles d'automatisation | règles d'écriture | hookify |
| Planification des fonctionnalités | Feature-dev | Feature-dev | Planification des fonctionnalités | Planification des fonctionnalités

**Compétences personnalisées à créer** (avec des modèles, des scripts, des exemples) :

| Les compétences personnalisées à créer** (avec des modèles, des scripts et des exemples) : - Signal de la base de code - Compétence à créer - Invocation de la base de code
|-----------------|-----------------|------------|
| Projet de base de données - **créer une base de données - **créer une base de données - **créer une base de données - **créer une base de données - **créer une base de données
| Projet de base de données | **créer-migration** (avec script de validation) | Utilisateurs seulement
| Suite de tests | **gen-test** (avec exemples de tests) | Réservé à l'utilisateur
| Bibliothèque de composants | **nouveau-composant** (avec modèles) | Réservé à l'utilisateur
| flux de travail PR | **pr-check** (avec liste de contrôle) | réservé à l'utilisateur
| Release | **release-notes** (avec contexte git) | Réservé à l'utilisateur |
| Style de code | **conventions de projet** | Réservé à Claude |
| Onboarding | **setup-dev** (avec prereq script) | Utilisateur uniquement |

#### C. Recommandations concernant les crochets

Voir [references/hooks-patterns.md](hooks-patterns.md.md) pour les configurations.

| Signal de la base de code | Accroche recommandée
|-----------------|------------------|
| Prettier configuré | PostToolUse : auto-format lors de l'édition
| ESLint/Ruff configuré | PostToolUse : auto-lint lors de l'édition |
| Projet TypeScript | PostToolUse : vérification de type lors de l'édition
| PostToolUse : exécuter les tests correspondants |
| PreToolUse : bloque les modifications de `.env` | PreToolUse : bloque les modifications de `.env` |
| PreToolUse : bloquer les modifications du fichier `.env`.
| Code sensible à la sécurité | PreToolUse : demande de confirmation |

#### D. Recommandations pour les sous-agents

Voir [references/subagent-templates.md](subagent-templates.md.md) pour les modèles.

| Si vous n'avez pas de modèle de sous-agent, vous pouvez utiliser la base de code Signal et le sous-agent recommandé.
|-----------------|---------------------|
| Vous avez besoin d'une base de code importante (>500 fichiers) ? **code-reviewer** - Parallel code review
| Vous avez besoin d'un code d'authentification et de paiement, d'un code d'authentification et de paiement, d'un code d'authentification et de paiement.
| Projet d'API **api-documenter** - Génération d'OpenAPI
| Projet d'API - **api-documenter** - Génération d'OpenAPI
| **ui-reviewer** - Examen de l'accessibilité | **test de l'interface utilisateur** - Test de l'interface utilisateur
**test-writer** - Génération de tests

#### E. Recommandations pour les plugins

Voir [references/plugins-reference.md](plugins-reference.md.md) pour les plugins disponibles.

| Vous pouvez également consulter la liste des plugins disponibles en cliquant sur le lien suivant : [YNXMTTRFKWDNDOUK].
|-----------------|-------------------|
| Productivité générale **anthropic-agent-skills** - Core skills bundle (ensemble de compétences de base)
| Installer les compétences docx, xlsx, pdf |
| Développement du front-end | **frontend-design** plugin
| Outils de construction d'IA | **mcp-builder** pour le développement de MCP | Outils de construction d'IA

### Phase 3 : Rapport sur les recommandations de sortie

Formulez clairement vos recommandations. **N'incluez que 1 à 2 recommandations par catégorie** - les plus valables pour cette base de code spécifique. Sautez les catégories qui ne sont pas pertinentes.

```markdown
## Recommandations d'automatisation du code Claude

J'ai analysé votre base de code et identifié les meilleures automatisations pour chaque catégorie. Voici mes 1 à 2 meilleures recommandations par type :

### Profil de la base de code
- Type** : [langage détecté/temps d'exécution]
- **Framework** : [framework détecté]
- **Bibliothèques clés** : [bibliothèques pertinentes détectées]

---

#### 🔌 MCP Servers

#### contexte7
**Why** : [raison spécifique basée sur les bibliothèques détectées]
**Installation** : `claude mcp add context7`

---

### 🎯 Compétences

#### [nom de la compétence]
**Pourquoi** : [raison spécifique]
**Créer** : `.claude/skills/[name]/SKILL.md`
**Invocation** : Utilisateur uniquement / Les deux / Claude uniquement
**Aussi disponible dans** : [nom du plugin] plugin (si applicable)
``yaml
---
name : [skill-name]
description : [ce qu'il fait]
disable-model-invocation : true # pour l'utilisateur uniquement
---
```

---

### ⚡ Crochets

#### [nom du crochet]
**Pourquoi** : [raison spécifique basée sur la configuration détectée]
**Où** : `.claude/settings.json`

---

### 🤖 Sous-agents

#### [nom de l'agent]
**Pourquoi** : [raison spécifique basée sur des modèles de base de code]
**Où** : `.claude/agents/[nom].md`

---

**Vous en voulez plus?** Demandez des recommandations supplémentaires pour une catégorie spécifique (par exemple, "montrez-moi plus d'options de serveur MCP" ou "quels autres crochets pourraient vous aider").

**Vous voulez de l'aide pour mettre en place l'une de ces recommandations ? Demandez et je vous aiderai à mettre en place l'une des recommandations ci-dessus.
```

## Cadre de décision

### Quand recommander les serveurs MCP
- Intégration de services externes nécessaire (bases de données, API)
- Recherche de documentation pour les bibliothèques/SDK
- Automatisation ou test du navigateur
- Intégration d'outils d'équipe (GitHub, Linear, Slack)
- Gestion de l'infrastructure en nuage

### Quand recommander des compétences

- Génération de documents (docx, xlsx, pptx, pdf - également dans les plugins)
- Invitations ou flux de travail fréquemment répétés
- Tâches spécifiques à un projet avec arguments
- Application de modèles ou de scripts aux tâches (les compétences peuvent regrouper des fichiers d'appui)
- Actions rapides invoquées avec `/nom de la compétence`.
- Les flux de travail qui doivent être exécutés de manière isolée (`contexte : fork`)

**Contrôle de l'invocation:**
- `disable-model-invocation : true` - Réservé à l'utilisateur (pour les effets de bord : deploy, commit, send)
- `user-invocable : false` - Claude uniquement (pour les connaissances de base)
- Défaut (omettre les deux) - Les deux peuvent invoquer

### Quand recommander les crochets
- Actions répétitives de post-édition (formatage, linting)
- Règles de protection (blocage des modifications de fichiers sensibles)
- Contrôles de validation (tests, contrôles de type)

### Quand recommander des sous-agents
- Expertise spécialisée nécessaire (sécurité, performance)
- Flux de travail de révision parallèles
- Contrôles de qualité des antécédents

### Quand recommander des plugins
- Vous avez besoin de plusieurs compétences connexes
- Vous voulez des ensembles d'automatisation pré-packagés
- Standardisation à l'échelle de l'équipe

---

## Conseils de configuration

### Configuration du serveur MCP

**Partage d'équipe** : Vérifiez `.mcp.json` dans le repo pour que toute l'équipe ait les mêmes serveurs MCP.

**Debugging** : Utilisez le drapeau `--mcp-debug` pour identifier les problèmes de configuration.

**Prérequis à recommander:**
- CLI GitHub (`gh`) - permet les opérations natives de GitHub
- Puppeteer/Playwright CLI - pour les serveurs MCP à navigateur

### Headless Mode (pour CI/Automation)

Recommandez headless Claude pour les pipelines automatisés :

```bash
# Exemple de crochet de pré-commission
claude -p "corriger les erreurs de lint dans src/" --allowedTools Edit,Write

# pipeline CI avec sortie structurée
claude -p "<prompt>" --output-format stream-json | votre_commande
```

### Permissions pour les Hooks

Configurez les outils autorisés dans `.claude/settings.json` :

``json
{
  "permissions" : {
    "allow" : ["Edit", "Write", "Bash(npm test:*)", "Bash(git commit:*)"].
  }
}
```