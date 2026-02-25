# Recommandations en matière de compétences

Les compétences sont des expertises packagées avec des flux de travail, des documents de référence et des meilleures pratiques. Créez-les dans `.claude/skills/<nom>/SKILL.md`. Les compétences peuvent être invoquées automatiquement par Claude lorsqu'elles sont pertinentes, ou par les utilisateurs directement avec `/skill-name`.

Certaines compétences pré-construites sont disponibles via des plugins officiels (à installer via `/plugin install`).

**Note** : Il s'agit de modèles courants. Utilisez une recherche sur le web pour trouver des idées de compétences spécifiques aux outils et frameworks de la base de code.

---

## Disponible sur Official Plugins

### Développement du plugin (plugin-dev)

| Compétences - Meilleur pour - Meilleur pour - Meilleur pour - Meilleur pour
|-------|----------|
| Développement de compétences **Développement de compétences** | Création de nouvelles compétences avec une structure adéquate
| Développement d'une nouvelle compétence avec une structure adéquate.
| Développement de commandes**** Création de commandes de type slash
| Développement d'agents*** - Création de sous-agents spécialisés
| Intégration des serveurs MCP dans les plugins
| Développement de sousagents spécialisés **mcp-integration** | Intégration des serveurs MCP dans les plugins

### Flux de travail Git (commandes de validation)

| Compétences - Meilleures pour - Les compétences - Les compétences - Les compétences - Les compétences - Les compétences - Les compétences - Les compétences - Les compétences - Les compétences
|-------|----------|
**commit** | Créer des commits git avec les messages appropriés
**commit-push-pr** | Flux de travail complet pour le commit, le push et le PR

### Frontend (frontend-design)

| Compétences - Meilleur pour - Les compétences - Les compétences - Les compétences - Les compétences - Les compétences - Les compétences - Les compétences - Les compétences - Les compétences
|-------|----------|
| Création de composants d'interface utilisateur soignés |

**Valeur** : Créez des interfaces utilisateur distinctives et de haute qualité au lieu d'une esthétique générique de l'IA.

### Règles d'automatisation (hookify)

| Compétences - Meilleur pour - Les compétences - Les compétences - Les compétences - Les compétences - Les compétences - Les compétences - Les compétences - Les compétences - Les compétences
|-------|----------|
| Création de règles hookify pour l'automatisation |

### Développement de fonctionnalités (feature-dev)

| Compétences : Meilleur pour
|-------|----------|
| **feature-dev** | Flux de travail de bout en bout pour le développement de fonctionnalités |

---

## Référence rapide : Compétences officielles des plugins

| Codebase Signal | Compétence | Plugin |
|-----------------|-------|--------|
| compétences de développement | plugin-dev | construction de plugins | compétences de développement | plugin-dev | construction de plugins
| Le développement d'un plugin est un processus complexe et complexe qui nécessite de nombreuses compétences.
| React/Vue/Angular | frontend-design | frontend-design | React/Vue/Angular | React/Vue/Angular | frontend-design | frontend-design
| règles d'automatisation | règles d'écriture | hookify |
| Planification des fonctionnalités | Feature-dev | Feature-dev | Planification des fonctionnalités | Planification des fonctionnalités

---

## Compétences du projet personnalisé

Créez des compétences spécifiques à un projet dans `.claude/skills/<name>/SKILL.md`.

### Structure des compétences

```
.claude/skills/
└── my-skill/
    ├── SKILL.md # Instructions principales (obligatoires)
    ├── template.yaml # Modèle à appliquer
    ├── scripts/
    │ └── validate.sh # Script à exécuter
    └── exemples/ # Exemples de référence
```

### Référence Frontmatter

```yaml
---
name : nom-de-la-compétence
description : Ce que fait cette compétence et quand l'utiliser
disable-model-invocation : true # Seul l'utilisateur peut l'invoquer (pour les effets de bord)
user-invocable : false # Seul Claude peut invoquer (pour les connaissances de base)
allowed-tools : Read, Grep, Glob # Restreint l'accès aux outils
context : fork # Exécuter dans un sous-agent isolé
agent : Explore # Quel type d'agent lors du forkage
---
```

### Contrôle de l'invocation

| Paramètre | Utilisateur | Claude | Utilisation pour |
|---------|------|--------|---------|
| (par défaut) | ✓ | ✓ | Compétences d'usage général |
| `disable-model-invocation : true` | ✓ | ✗ | Effets secondaires (déploiement, envoi) |
| `invocable par l'utilisateur : false` | ✗ | ✓ | Connaissances de base |

---

## Exemples de compétences personnalisées

### Documentation API avec OpenAPI Template

Appliquez un modèle YAML pour générer des documents d'API cohérents :

```
.claude/skills/api-doc/
├── SKILL.md
└── openapi-template.yaml
```

**SKILL.md:**
``yaml
---
name : api-doc
description : Générer de la documentation OpenAPI pour un point d'accès. A utiliser pour documenter les routes de l'API.
---

Génère la documentation OpenAPI pour le point de terminaison à $ARGUMENTS.

Utilisez le modèle dans [openapi-template.yaml](openapi-template.yaml) comme structure.

1. Lisez le code du point d'accès
2. Extraire le chemin, la méthode, les paramètres, les schémas de requête/réponse
3. Remplir le modèle avec les valeurs réelles
4. Produisez le YAML complété
```

**openapi-template.yaml:**
``yaml
paths :
  /{chemin} :
    {méthode} :
      summary : ""
      description : ""
      paramètres : []
      requestBody :
        content :
          application/json :
            schema : {}
      responses :
        "200" :
          description : ""
          content :
            application/json :
              schema : {}
```

---

### Générateur de migration de base de données avec script

Générez et validez des migrations à l'aide d'un script intégré :

```
.claude/skills/create-migration/
├── SKILL.md
└── scripts/
    └── validate-migration.sh
```

**SKILL.md:**
```yaml
---
name : create-migration
description : Créer un fichier de migration de base de données
disable-model-invocation : true
allowed-tools : Read, Write, Bash
---

Créer une migration pour : $ARGUMENTS

1. Générer un fichier de migration dans `migrations/` avec un préfixe d'horodatage
2. Inclure les fonctions de montée et de descente
3. Lancez la validation : `bash ~/.claude/skills/create-migration/scripts/validate-migration.sh`
4. Signalez les problèmes trouvés
```

**scripts/validate-migration.sh:**
```bash
#!/bin/bash
# Validez la syntaxe de la migration
npx prisma validate 2>&1 || echo "Validation failed"
```

---

### Générateur de tests avec exemples

Générez des tests en suivant les modèles du projet :

```
.claude/skills/gen-test/
├── SKILL.md
└── exemples/
    ├── unit-test.ts
    └── integration-test.ts
```

**SKILL.md:**
```yaml
---
name : gen-test
description : Génère des tests pour un fichier en suivant les conventions du projet
disable-model-invocation : true
---

Générer des tests pour : $ARGUMENTS

Référez-vous à ces exemples pour connaître les modèles attendus :
- Tests unitaires : [examples/unit-test.ts](examples/unit-test.ts)
- Tests d'intégration : [examples/integration-test.ts](examples/integration-test.ts)

1. Analysez le fichier source
2. Identifiez les fonctions/méthodes à tester
3. Générer des tests correspondant aux conventions du projet
4. Placez-les dans le répertoire de test approprié
```

---

### Générateur de composants avec modèle

Échafaudez de nouveaux composants à partir d'un modèle :

```
.claude/skills/new-component/
├── SKILL.md
└── templates/
    ├── component.tsx.template
    ├── component.test.tsx.template
    └── component.stories.tsx.template
```

**SKILL.md:**
``yaml
---
name : new-component
description : Échafaudage d'un nouveau composant React avec des tests et des histoires.
disable-model-invocation : true
---

Créer un composant : $ARGUMENTS

Utilisez les modèles du répertoire [templates/](templates/) :
1. Générer le composant à partir de component.tsx.template
2. Générer des tests à partir de component.test.tsx.template
3. Générer l'histoire Storybook à partir de component.stories.tsx.template

Remplacez {{Nom du composant}} par le nom en PascalCase.
Remplacez {{nom-composant}} par le nom de l'affaire kebab.
```

---

### Revue des RP avec liste de contrôle

Examinez les RP à l'aide d'une liste de contrôle spécifique au projet :

```
.claude/skills/pr-check/
├── SKILL.md
└── checklist.md
```

**SKILL.md:**
``yaml
---
name : pr-check
description : Vérifier les RP par rapport à la liste de contrôle du projet
disable-model-invocation : true
context : fork
---

## Contexte du PR
- Diffusion : !`gh pr diff`
- Description : !`gh pr view`

Révision par rapport à [checklist.md](checklist.md).

Pour chaque élément, marquer ✅ ou ❌ avec une explication.
```

**checklist.md:**
```markdown
## Liste de contrôle des RP

- Tests ajoutés pour les nouvelles fonctionnalités
- Aucune déclaration console.log
- La gestion des erreurs inclut des messages destinés à l'utilisateur
- Les changements d'API sont rétrocompatibles
- Les migrations de bases de données sont réversibles
```

---

### Notes de version Générateur

Génère des notes de version à partir de l'historique git :

**SKILL.md:**
```yaml
---
name : release-notes
description : Génère les notes de version à partir des commits depuis le dernier tag
disable-model-invocation : true
---

## Changements récents
- Commits depuis la dernière balise : !`git log $(git describe --tags --abbrev=0)..HEAD --oneline`
- Dernière balise : !`git describe --tags --abbrev=0`

Générer les notes de version :
1. Regrouper les commits par type (feat, fix, docs, etc.)
2. Rédiger des descriptions conviviales
3. Mettre en évidence les changements de rupture
4. Formatage en markdown
```

---

### Conventions du projet (Claude uniquement)

Connaissances de base que Claude applique automatiquement :

**SKILL.md:**
```yaml
---
name : projet-conventions
description : Style et modèles de code pour ce projet. A appliquer lors de l'écriture ou de la révision du code.
invocable par l'utilisateur : false
---

## Conventions de nommage
- Composants React : PascalCase
- Utilitaires : camelCase
- Constantes : UPPER_SNAKE_CASE
- Fichiers : kebab-case

## Modèles
- Utiliser `Result<T, E>` pour les opérations faillibles, pas pour les exceptions
- Préférez la composition à l'héritage
- Toutes les réponses de l'API utilisent la forme `{ data, error, meta }`.

## Interdit
- Pas de types `any
- Pas de `console.log` dans le code de production
- Pas d'entrées/sorties synchrones de fichiers
```

---

### Configuration de l'environnement

Embarquez les nouveaux développeurs avec un script d'installation :

```
.claude/skills/setup-dev/
├── SKILL.md
└── scripts/
    └── check-prerequisites.sh
```

**SKILL.md:**
```yaml
---
name : setup-dev
description : Mise en place d'un environnement de développement pour les nouveaux contributeurs
disable-model-invocation : true
---

Mise en place d'un environnement de développement :

1. Vérifier les prérequis : `bash scripts/check-prerequisites.sh`
2. Installez les dépendances : `npm install`
3. Copier le modèle d'environnement : `cp .env.example .env`
4. Configurez la base de données : `npm run db:setup`
5. Vérifiez l'installation : `npm test`

Signalez tout problème rencontré.
```

---

## Argument Patterns

| Modèle | Signification | Exemple |
|---------|---------|---------|
| `$ARGUMENTS` | Tous les arguments sous forme de chaîne | `/deploy staging` → "staging" |

Les arguments sont ajoutés comme `ARGUMENTS : <valeur>` si `$ARGUMENTS` n'est pas dans la compétence.

## Injection dynamique de contexte

Utilisez `!`command`` pour injecter des données dynamiques avant que la compétence ne s'exécute :

``yaml
## État actuel
- Branche : !`git branch --show-current`
- Etat : !`git status --short`
```

La sortie de la commande remplace l'espace réservé avant que Claude ne voie le contenu de la compétence.