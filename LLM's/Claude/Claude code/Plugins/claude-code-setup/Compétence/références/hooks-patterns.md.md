# Recommandations concernant les crochets

Les crochets exécutent automatiquement des commandes en réponse à des événements du code Claude. Ils sont idéaux pour l'application et l'automatisation qui doivent se produire de manière cohérente.

**Note** : Il s'agit de modèles courants. Utilisez la recherche sur le web pour trouver des hooks pour des outils/frameworks non listés ici afin de recommander les meilleurs hooks pour l'utilisateur.

## Crochets de formatage automatique

### Prettier (JavaScript/TypeScript)
| Détection d'un fichier existant - Détection d'un fichier existant - Détection d'un fichier existant - Détection d'un fichier existant
|-----------|-------------|
| `.prettierrc`, `.prettierrc.json`, `prettier.config.js` | ✓ |

**Recommandé** : PostToolUse hook sur Edit/Write pour l'auto-formatage
**Valeur** : Le code reste formaté sans y penser

### ESLint (JavaScript/TypeScript)
| Détection d'un fichier existant
|-----------|-------------|
| `.eslintrc`, `.eslintrc.json`, `eslint.config.js` | ✓ |

**Recommend** : PostToolUse hook on Edit/Write to auto-fix
**Valeur** : Les erreurs de Lint sont corrigées automatiquement

### Black/isort (Python)
| Détection d'un fichier existant
|-----------|-------------|
| `pyproject.toml` avec black/isort, `.black`, `setup.cfg` | ✓ | |

**Recommend** : PostToolUse hook pour formater les fichiers Python
**Valeur** : Formatage cohérent de Python

### Ruff (Python - Moderne)
| Détection d'un fichier existant
|-----------|-------------|
| `ruff.toml`, `pyproject.toml` avec `[tool.ruff]` | ✓ |

**Recommend** : PostToolUse hook for lint + format
**Valeur** : Linting rapide et complet de Python

### gofmt (Go)
| Détection d'un fichier existant
|-----------|-------------|
| `go.mod` | ✓ |

**Recommandé** : PostToolUse hook pour lancer gofmt
**Valeur** : Formatage standard de Go

### rustfmt (Rust)
| Détection d'un fichier existant
|-----------|-------------|
| `Cargo.toml` | | ✓ | |

**Recommandé** : PostToolUse hook pour lancer rustfmt
**Valeur** : Formatage Rust standard

---

## Crochets de vérification de type

### TypeScript
| Détection d'un fichier existant
|-----------|-------------|
| `tsconfig.json` | ✓ |

**Recommend** : PostToolUse hook pour exécuter tsc --noEmit
**Valeur** : Capturez les erreurs de type immédiatement

### mypy/pyright (Python)
| Détection d'un fichier existant
|-----------|-------------|
| `mypy.ini`, `pyrightconfig.json`, pyproject.toml with mypy | ✓ | |

**Recommend** : PostToolUse hook for type checking (crochet PostToolUse pour la vérification des types)
**Valeur** : Attraper les erreurs de type en Python

---

## Crochets de protection

### Bloquer les modifications de fichiers sensibles
| Détection de la présence d'un fichier
|-----------|-------------|
| `.env`, `.env.local`, `.env.production` | Fichiers d'environnement | `credentials.json`, `secrets.json`, `.env.production`.
| `credentials.json`, `secrets.yaml` | Fichiers secrets | `.git/`, `.git/`, `.git/`, `.git/`.
| Répertoire `.git/` | Git internals |

**Recommandé** : Crochet PreToolUse qui bloque l'édition/écriture dans ces chemins
**Valeur** : Prévenir l'exposition accidentelle d'un secret ou la corruption de Git

### Bloquer les éditions de fichiers verrouillés
| Détection de la présence d'un chemin d'accès
|-----------|-------------|
| `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml` | Fichiers de verrouillage JS | `Cargo.lock`, `poetry.lock`, `pnpm-lock.yaml`
| `Cargo.lock`, `poetry.lock`, `Pipfile.lock` | Autres fichiers de verrouillage |

**Recommandé** : Crochet PreToolUse qui bloque les éditions directes
**Valeur** : Les fichiers de verrouillage ne doivent être modifiés que par le gestionnaire de paquets

---

## Crochets du Test Runner

### Jest (JavaScript/TypeScript)
| Détection de la présence de
|-----------|-------------|
| `jest.config.js`, `jest` dans package.json | Jest configuré | `__tests__/`, `*.jest` dans package.json
| `__tests__/`, `*.test.ts`, `*.spec.ts` | Les fichiers de test existent |

**Recommandé** : PostToolUse hook pour exécuter les tests associés après l'édition.
**Valeur** : Retour d'information immédiat sur les modifications

### pytest (Python)
| Détection de la présence de
|-----------|-------------|
| `pytest.ini`, `pyproject.toml` avec pytest | pytest configuré | `tests/`, `test_*.py`, `pytest_*.py` avec pytest
| `tests/`, `test_*.py` | Les fichiers de test existent |

**Recommandé** : PostToolUse hook pour lancer pytest sur les fichiers modifiés
**Valeur** : Retour d'information immédiat sur les tests

---

## Référence rapide : Détection → Recommandation

| Si vous voyez ce crochet, recommandez-le.
|------------|-------------------|
| Configuration de Prettier | Formatage automatique lors de l'édition et de l'écriture
| ESLint config | Auto-lint sur Edit/Write |
| Ruff/Black config | Auto-format Python |
| tsconfig.json | Vérification du type lors de l'édition / écriture
| Répertoire de test - Exécutez les tests correspondants lors de l'édition.
| Blocage des fichiers .env | Blocage des modifications de fichiers .env
| Blocage de l'édition des fichiers .env
Projet Go | gofmt sur Edit | Projet Rust | rustfmt sur Edit | Projet Rust | rustfmt sur Edit
| Projet Rust | rustfmt sur Edit |

---

## Crochets de notification

Les crochets de notification s'exécutent lorsque Claude Code envoie des notifications. Utilisez les filtres de correspondance pour filtrer par type de notification.

### Permission Alerts
| Matcher | Cas d'utilisation |
|---------|----------|
Alerte lorsque Claude demande des permissions | `permission_prompt` | Alerte lorsque Claude demande des permissions |

**Recommandé** : Jouer un son, envoyer une notification sur le bureau, ou enregistrer les demandes de permission.
**Valeur** : Ne manquez jamais les invites de permission lorsque vous êtes multitâches.

### Notifications d'inactivité
| Matcher | Cas d'utilisation |
|---------|----------|
| `idle_prompt` | Alerte lorsque Claude est en attente d'une entrée (60+ secondes d'inactivité) |

**Recommandé** : Jouer un son ou envoyer une notification lorsque Claude a besoin d'attention
**Valeur** : Sachez quand Claude est prêt à recevoir vos commentaires

### Exemple de configuration

```json
{
  "hooks" : {
    "Notification" : [
      {
        "matcher" : "permission_prompt",
        "hooks" : [
          {
            "type" : "command",
            "command" : "afplay /System/Library/Sounds/Ping.aiff"
          }
        ]
      },
      {
        "matcher" : "idle_prompt",
        "hooks" : [
          {
            "type" : "command",
            "commande" : "osascript -e 'afficher la notification "Claude attend" avec le titre "Claude Code"".
          }
        ]
      }
    ]
  }
}
```

### Correspondances disponibles

| Déclencheurs Quand |
|---------|---------------|
| Claude a besoin d'une permission pour un outil.
| Claude attend une entrée (60+ secondes) | `auth_success` | Claude attend une entrée (60+ secondes) | `auth_success` | Claude attend une entrée (60+ secondes)
| `auth_success` | L'authentification a réussi
| `elicitation_dialog` | L'outil MCP a besoin d'une entrée |

---

## Référence rapide : Détection → Recommandation

| Si vous voyez ce crochet, recommandez-le.
|------------|-------------------|
| Configuration de Prettier | Formatage automatique lors de l'édition et de l'écriture
| ESLint config | Auto-lint sur Edit/Write |
| Ruff/Black config | Auto-format Python |
| tsconfig.json | Vérification du type lors de l'édition / écriture
| Répertoire de test - Exécutez les tests correspondants lors de l'édition.
| Blocage des fichiers .env | Blocage des modifications de fichiers .env
| Blocage de l'édition des fichiers .env
Projet Go | gofmt sur Edit | Projet Rust | rustfmt sur Edit | Projet Rust | rustfmt sur Edit
| Projet Rust | rustfmt sur Edit |
| Projet Rust - rustfmt sur Edit - Projet Rust - rustfmt sur Edit - Projet Rust - rustfmt sur Edit

---

## Placement des crochets

Les crochets sont placés dans `.claude/settings.json` :

```
.claude/
└── settings.json ← Configurations de crochets ici
```

Nous vous recommandons de créer le répertoire `.claude/` s'il n'existe pas.