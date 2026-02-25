# Recommandations pour le serveur MCP

Les serveurs MCP (Model Context Protocol) étendent les capacités de Claude en se connectant à des outils et services externes.

**Note** : Il s'agit de serveurs MCP courants. Utilisez une recherche sur le web pour trouver des serveurs MCP spécifiques aux services et intégrations de la base de code.

## Configuration et partage d'équipe

**Méthodes de connexion:**
1. **Configuration du projet** (`.mcp.json`) - Disponible uniquement dans ce répertoire
2. **Config globale** (`~/.claude.json`) - Disponible dans tous les projets
3. **Checked-in `.mcp.json`** - Disponible pour toute l'équipe (recommandé !)

**Astuce** : Vérifiez `.mcp.json` dans git pour que toute l'équipe ait les mêmes serveurs MCP.

**Débogage** : Utilisez `claude --mcp-debug` pour identifier les problèmes de configuration.

## Documentation et connaissances

### contexte7
**Le meilleur pour** : Projets utilisant des bibliothèques/SDK populaires pour lesquels vous souhaitez que Claude code avec une documentation à jour.

| Recommandez quand, quand, quand, quand, quand, quand...
|----------------|----------|
| Vous utilisez React, Vue, Angular | Cadres frontaux |
| Utilisation de Express, FastAPI, Django | Cadres backend |
| Utilisation de Prisma, Drizzle | ORMs |
| Utilisation de Stripe, Twilio, SendGrid | API tierces
| Utilisation de AWS SDK, Google Cloud | SDKs Cloud | Utilisation de LangChain, OpenAI
| Utilisation de LangChain, OpenAI SDK | Bibliothèques AI/ML

**Valeur** : Claude récupère la documentation en direct au lieu de s'appuyer sur des données d'entraînement, ce qui réduit les API hallucinées et les modèles obsolètes.

---

## Navigateur et interface

### Playwright MCP
**Le meilleur pour** : Projets frontaux nécessitant une automatisation du navigateur, des tests ou des captures d'écran

| Recommandez quand, exemples, etc.
|----------------|----------|
| Vous avez besoin d'une application React/Vue/Angular pour tester les composants de l'interface utilisateur.
| Test des composants de l'interface utilisateur (UI)
| Test des composants de l'interface utilisateur - Tests E2E nécessaires - Validation du flux utilisateur - Test de régression visuelle - Comparaison des captures d'écran
| Test de l'interface utilisateur (UI) | Débogage des problèmes d'UI | Voir ce que l'utilisateur voit
Tests de formulaires | Flux de travail en plusieurs étapes | Tests de composants d'interface utilisateur | Tests de régression visuelle | Comparaisons de captures d'écran

**Valeur** : Claude peut interagir avec votre application en cours, prendre des captures d'écran, remplir des formulaires et vérifier le comportement de l'interface utilisateur.

### Puppeteer MCP
**Le meilleur pour** : Automatisation d'un navigateur sans tête, scraping web

| Recommandez quand - Exemples - Recommandez quand - Recommandez quand - Exemples - Recommandez quand - Recommandez quand - Exemples
|----------------|----------|
| Génération de PDF à partir de HTML | Génération de rapports
| Tâches de web scraping | Extraction de données
| Tests sans tête | Environnements de CI

---

## Bases de données

### Supabase MCP
**Meilleur pour** : Les projets utilisant Supabase comme backend/base de données

| Recommandez quand, exemples, etc...
|----------------|----------|
| Le projet Supabase a été détecté | `@supabase/supabase-js` dans le deps
| Auth + base de données | Applications de gestion des utilisateurs
| Fonctionnalités en temps réel | Synchronisation des données en temps réel

**Valeur** : Claude peut interroger les tables, gérer l'authentification et interagir directement avec le stockage de Supabase.

### PostgreSQL MCP
**Le meilleur pour** : Accès direct à la base de données PostgreSQL

| Recommandez quand, exemples, etc.
|----------------|----------|
| Utilisation brute de PostgreSQL - Pas de couche ORM - Pas de couche ORM
| Migration de bases de données | Gestion des schémas
| Tâches d'analyse de données | Requêtes complexes |
| Débogage des problèmes de données | Inspection des données réelles |

### Neon MCP
**Le meilleur pour** : Les utilisateurs de Neon Postgres sans serveur

### Turso MCP
**Le meilleur pour** : Utilisateurs de bases de données de pointe Turso/libSQL

---

## Contrôle de version et DevOps

### GitHub MCP
**Le meilleur pour** : Les dépôts hébergés par GitHub qui ont besoin d'une intégration des problèmes et des rapports.

| Recommandez quand, exemples, etc.
|----------------|----------|
| Référentiel GitHub - `.git` avec GitHub remote - `.git` avec GitHub remote - `.git` avec GitHub remote - `.git`.
| Développement axé sur les problèmes - Référencement des problèmes dans les commits
| Révision, fusion | Actions GitHub
| Actions GitHub | Accès au pipeline CI/CD | Gestion des mises à jour
| Gestion des versions | Automatisation des balises et des versions

**Valeur** : Claude peut créer des problèmes, réviser des RP, vérifier l'exécution des flux de travail et gérer les versions.

### GitLab MCP
**Le meilleur pour** : Les dépôts hébergés par GitLab

### Linear MCP
**Le meilleur pour** : Les équipes qui utilisent Linear pour le suivi des problèmes

| Recommandez quand - Exemples - Recommandez quand - Recommandez quand - Exemples - Recommandez quand - Recommandez quand - Exemples
|----------------|----------|
| L'espace de travail linéaire - Les références des problèmes comme `ABC-123` - La planification des sprints - La gestion du carnet de commandes - La planification des sprints - La gestion du carnet de commandes
| Planification de sprint | Gestion du carnet de commandes | Création d'un numéro à partir du code
| Création de problèmes à partir du code | Création automatique de problèmes pour les TODOs |

---

## Infrastructure en nuage

### AWS MCP
**Le meilleur pour** : Gestion de l'infrastructure AWS

| Recommandez-nous quand, exemples, etc.
|----------------|----------|
AWS SDK dans les dépendances | Paquets `@aws-sdk/*` | Infrastructure en tant que code | Terraform, CDK, SAM
| Développement de l'infrastructure en tant que code - Terraform, CDK, SAM - Développement de Lambda - Fonctions sans serveur - Gestion de l'infrastructure AWS
| Développement Lambda | Fonctions sans serveur
| Utilisation de S3, DynamoDB | Services de données en nuage |

### Cloudflare MCP
**Meilleur pour** : Cloudflare Workers, Pages, R2, D1

| Recommandez quand | Exemples |
|----------------|----------|
| Cloudflare Workers | Fonctions de périphérie
| Déploiement de pages - Hébergement de sites statiques - Stockage R2 - Stockage d'objets - Stockage D1
| Stockage R2 - Stockage d'objets - Stockage d'objets - Stockage d'objets
| Base de données D1 | Base de données SQL Edge

### Vercel MCP
**Le meilleur pour** : Déploiement et configuration de Vercel

---

## Surveillance et observation

### Sentry MCP
**Le meilleur pour** : Suivi des erreurs et débogage

| Recommandez quand, exemples, etc.
|----------------|----------|
| La configuration de Sentry | `@sentry/*` dans le deps
| Débogage de la production | Recherche d'erreurs
| Groupement de problèmes similaires | Suivi des mises à jour
| Suivi des versions | Corrélation entre les déploiements et les erreurs

**Valeur** : Claude peut enquêter sur les problèmes liés à Sentry, en trouver les causes profondes et proposer des solutions.

### Datadog MCP
**Le meilleur pour** : APM, logs et métriques

---

## Communication

### Slack MCP
**Le meilleur pour** : Intégration de l'espace de travail Slack

| Recommandez-nous quand, quand, quand, quand, quand, quand, quand...
|----------------|----------|
| L'équipe utilise Slack | Envoyez des notifications
| Notifications de déploiement | Canaux d'alerte | Réponse aux incidents
| L'équipe utilise Slack pour envoyer des notifications, déployer des canaux d'alerte, répondre aux incidents et publier des mises à jour.

### Notion MCP
**Le meilleur pour** : Espace de travail Notion pour la documentation

| Recommandez quand - Exemples - Recommandez quand - Recommandez quand - Exemples - Recommandez quand - Recommandez quand - Exemples
|----------------|----------|
| Notion d'espace de travail pour la documentation
| Base de connaissances | Recherche dans la documentation
| Notes de réunion | Créer des résumés

---

## Fichiers et données

### Système de fichiers MCP
**Le meilleur pour** : Opérations de fichiers améliorées au-delà des outils intégrés

| Recommandez quand, exemples, etc.
|----------------|----------|
| Opérations complexes sur les fichiers | Traitement par lots
| Recherche avancée | Modèles personnalisés | Surveillance des changements
| Recherche avancée | Modèles personnalisés

### Memory MCP
**Le meilleur pour** : Mémoire persistante entre les sessions

| Recommandez quand, exemples, etc.
|----------------|----------|
| Les projets de longue haleine - Souvenez-vous du contexte - Les préférences de l'utilisateur - Stockez les paramètres - Les préférences de l'utilisateur
| Préférences de l'utilisateur | Mémoriser les paramètres
| Apprendre des modèles d'apprentissage | Construire des connaissances |

**Valeur** : Claude se souvient du contexte du projet, des décisions et des modèles au fil des conversations.

---

## Conteneurs et DevOps

### Docker MCP
**Le meilleur pour** : Gestion des conteneurs

| Recommandez quand - Exemples - Docker MCP
|----------------|----------|
Fichier Docker Compose | Orchestration de conteneurs | Fichier Docker Compose présent | Construction d'images
| Dockerfile présent | Construction d'images
| Débogage du conteneur | Inspecter les logs, exécuter le fichier Docker

### Kubernetes MCP
**Le meilleur pour** : Gestion des clusters Kubernetes

| Recommandez quand, exemples, etc.
|----------------|----------|
| K8s manifests | Déploiement, mise à l'échelle des pods |
| Déploiement, mise à l'échelle des pods | Graphiques Helm | Gestion des paquets
| Débogage de cluster | Journaux de pods, état |

---

## AI & ML

### Exa MCP
**Le meilleur pour** : Recherche sur le web et recherche

| Recommandez quand | Exemples |
|----------------|----------|
| Recherche d'informations sur le web
| Analyse concurrentielle | Étude de marché
| Documentation manquante | Recherche d'exemples

---

## Référence rapide : Modèles de détection

| Rechercher | Suggère un serveur MCP |
|----------|-------------------|
| Paquets npm populaires | context7 | React/Vue/Next.js | Playwright MCP
| React/Vue/Next.js | Playwright MCP | `@supabase/supabase-js` | Supabase
| MCP Playwright - `@supabase/supabase-js` - Supabase MCP - `@supabase-js` - `@supabase-js` - Supabase MCP
`pg` ou `postgres` | PostgreSQL MCP | `@supabase/supabase-js` | Supabase MCP
GitHub remote | GitHub MCP | GitHub remote | GitHub MCP | GitHub MCP
`.linear` ou Linear refs | Linear MCP | `@@aws-sdk` ou `.linear` ou Linear refs | Linear MCP
`@aws-sdk/*` | AWS MCP | `@sentry/*` | AWS MCP | `@sentry/*` | AWS MCP
`@sentry/*` | Sentry MCP | `@sentry/*` | Sentry MCP | `@sentry/*` | AWS MCP
`@aws-sdk/*` | AWS MCP | `@sentry/*` | Sentry MCP | `@docker-compose.yml` | Docker MCP
URLs des webhooks de Slack | Slack MCP | `@@anthropic-*` | `@@sentry/*` | Sentry MCP
| `@anthropic-ai/sdk` | context7 for Anthropic docs |