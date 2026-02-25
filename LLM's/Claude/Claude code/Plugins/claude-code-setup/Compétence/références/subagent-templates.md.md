# Recommandations pour les sous-agents

Les sous-agents sont des instances spécialisées de Claude qui fonctionnent en parallèle, chacune disposant de sa propre fenêtre contextuelle et de son propre accès aux outils. Ils sont idéaux pour des révisions, des analyses ou des tâches de génération ciblées.

**Note** : Il s'agit de modèles communs. Concevez des sous-agents personnalisés en fonction des besoins spécifiques de la base de code en matière de révision et d'analyse.

## Agents de révision du code

### code-reviewer
**Le meilleur pour** : Contrôles automatisés de la qualité du code sur de grandes bases de code

| Recommandez quand la détection de l'erreur.
|----------------|-----------|
| Le code de la base de données est volumineux (>500 fichiers).
| Développement actif
| L'équipe souhaite une révision cohérente | L'accent est mis sur la qualité

**Valeur** : Exécute la revue de code en parallèle pendant que vous continuez à travailler.
**Modèle** : sonnet (équilibre qualité/vitesse)
**Outils** : Read, Grep, Glob, Bash

---

### security-reviewer
**Le meilleur pour** : Revue de code axée sur la sécurité

| Recommandez la détection des failles de sécurité.
|----------------|-----------|
| Code d'authentification présent - Motifs `auth/`, `login`, `session` - Traitement des paiements - Motifs `stripe`, `payment`, `billing`, `billing`.
| Traitement des paiements - motifs `stripe`, `payment`, `billing` - Traitement des données de l'utilisateur - motifs `user`, `payment`, `billing`.
| Traitement des données de l'utilisateur - `user`, `profile`, `pii`.
| Les clés de l'API dans le code

**Valeur** : attrape les vulnérabilités OWASP, les problèmes d'authentification, l'exposition des données
**Modèle** : sonnet
**Outils** : Read, Grep, Glob (en lecture seule pour la sécurité)

---

### test-writer
**Le meilleur pour** : Générer une couverture de test complète

| Recommandez la détection de l'erreur.
|----------------|-----------|
| La couverture de test est faible. Peu de fichiers de test par rapport aux fichiers source.
| La suite de tests existe | `tests/`, `__tests__/` présents |
| jest, pytest, vitest dans les deps |

**Valeur** : Génère des tests correspondant aux conventions du projet
**Modèle** : sonnet
**Tools** : Read, Write, Grep, Glob

---

## Agents spécialisés

### api-documenter
**Le meilleur pour** : Génération de documentation sur les API

| Recommandez la détection d'une erreur dans la documentation de l'API.
|----------------|-----------|
| Les points de terminaison REST, les routes Express, les chemins FastAPI, etc.
| Schéma GraphQL - Fichiers `.graphql` - Création de la documentation de l'API
| Les API non documentées - Routes Express, chemins FastAPI, fichiers `.graphql`.
| API non documentées | Routes sans documentation

**Valeur** : Génère les spécifications de l'OpenAPI, la documentation des points d'extrémité
**Modèle** : sonnet
**Tools** : Lecture, écriture, Grep, Glob

---

### performance-analyzer
**Le meilleur pour** : Trouver les goulots d'étranglement des performances

| Recommandez quand la détection des goulots d'étranglement.
|----------------|-----------|
| Requêtes de base de données - Utilisation de l'ORM, code SQL brut - Requêtes de base de données - Utilisation de l'ORM, code SQL brut
| Code à fort trafic - Points d'extrémité d'API - Chemins d'accès rapides - Code à fort trafic - Code à faible trafic - Code à faible trafic - Code à faible trafic
| Plaintes concernant les performances | L'utilisateur signale une lenteur
| Algorithmes complexes | Boucles imbriquées, récursion |

**Valeur** : Trouver N+1 requêtes, algorithmes O(n²), fuites de mémoire
**Modèle** : sonnet
**Outils** : Read, Grep, Glob, Bash

---

### ui-reviewer
**Le meilleur pour** : Accessibilité frontale et révision UX

| Recommandez la détection d'un problème d'accessibilité
|----------------|-----------|
| React/Vue/Angular | Cadre de travail frontal détecté
| Bibliothèque de composants | Répertoire `components/` | Bibliothèque de composants | Répertoire `components/` | Répertoire `components/` | Bibliothèque de composants
| Pas seulement un projet d'API

**Valeur** : Capture les problèmes d'accessibilité, les problèmes d'interface utilisateur, les lacunes en matière de responsive design.
**Modèle** : sonnet
**Outils** : Read, Grep, Glob

---

## Agents utilitaires

### dependency-updater
**Le meilleur pour** : Mises à jour sûres des dépendances

| Recommandez la détection
|----------------|-----------|
| `npm outdated` a des résultats | `npm outdated` a des résultats | `npm outdated` a des résultats
| Avis de sécurité | `npm audit` warning |


**Valeur** : Met à jour les dépendances de manière incrémentale avec des tests
**Modèle** : sonnet
**Outils** : Lecture, écriture, Bash, Grep

---

### migration-helper
**Meilleur pour** : Migrations de cadre/version

| Recommandez la détection de l'erreur
|----------------|-----------|
| Vous avez besoin d'une mise à jour majeure, d'une version très ancienne du framework ou d'une migration de version.
| Avertissements de dépréciation
| Changements architecturaux | Changements d'architecture

**Valeur** : Planifie et exécute les migrations de manière incrémentale
**Modèle** : opus (raisonnement complexe nécessaire)
**Outils** : Read, Write, Grep, Glob, Bash

---

## Référence rapide : Détection → Recommandation

| Si vous voyez quelque chose, recommandez un sous-agent.
|------------|-------------------|
| Code de sécurité | Code de paiement | Code d'authentification
| Code d'authentification/de paiement - Réviseur de sécurité
| Quelques tests | test-writer |
| peu de tests | rédacteur de tests | routes API | api-documenteur
| Analyse de la base de données | Analyse de la performance | Analyse de la performance
| Composants frontaux | ui-reviewer |
| paquetages obsolètes | dependency-updater |
| Ancienne version du framework | migration-helper |

---

## Placement des sous-agents

Les sous-agents sont placés dans `.claude/agents/` :

```
.claude/
└── agents/
    ├── code-reviewer.md
    ├─── security-reviewer.md
    └─── test-writer.md
```

---

## Guide de sélection des modèles

| Modèle - Meilleur pour - Compromis - Modèle - Meilleur pour - Compromis - Modèle - Meilleur pour - Compromis - Compromis
|-------|----------|-----------|
| Le modèle de l'analyse de l'information est le modèle le plus approprié pour les tâches d'examen et d'analyse.
**sonnet** | La plupart des tâches de révision et d'analyse | Équilibré (recommandé par défaut)
**opus** | Migrations complexes, architecture | Approfondissement, plus lent, plus cher

---

## Guide d'accès aux outils

| Guide d'accès aux outils - Niveau d'accès - Outils - Cas d'utilisation - Niveau d'accès - Outils - Cas d'utilisation - Cas d'utilisation
|--------------|-------|----------|
| Lecture seule - Lecture, Grep, Glob - Revues, analyses, etc.
| Écriture | + Écriture | Génération de code, documentation |
| Bash | Migrations, tests |