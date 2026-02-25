# Recommandations de plugins

Les plugins sont des collections installables de compétences, de commandes, d'agents et de crochets. Installez-les via `/plugin install`.

**Note** : Il s'agit de plugins provenant du dépôt officiel. Utilisez la recherche sur le web pour découvrir d'autres plugins de la communauté.

---

## Plugins officiels

### Développement et qualité du code

| Plugin de la société de gestion des droits d'auteur - Plugin de la société de gestion des droits d'auteur - Meilleur pour - Fonctionnalités clés
|--------|----------|--------------|
| **plugin-dev** | Construction de plugins Claude Code | Compétences pour la création de compétences, de crochets, de commandes, d'agents, etc.
| Les agents de révision spécialisés (code, tests, types) peuvent être utilisés pour la révision des articles de presse.
**code-review** | Revue de code automatisée | Revue multi-agents avec évaluation de la confiance | **code-simplifier** | Revue de code automatisée
| **code-simplifier** | Refactoring de code | Simplifier le code tout en préservant les fonctionnalités |
| **feature-dev** | Développement de fonctionnalités | Workflow de fonctionnalités de bout en bout avec des agents | **feature-dev** | Développement de fonctionnalités

### Git & Workflow

| Plugin Git & Workflow | Meilleur pour | Fonctionnalités clés
|--------|----------|--------------|
**commit-commands** | Git workflows | /commit, /commit-push-pr commands | **hookify** | Règles d'automatisation
| Le plugin Git est un outil de gestion de l'information qui permet de créer des hooks à partir d'un modèle de conversation.

### Frontend

| Plugin Git - Meilleur pour - Fonctionnalités principales - Plugin Git - Meilleur pour - Fonctionnalités principales - Plugin Git - Meilleur pour
|--------|----------|--------------|
| Développement de l'interface utilisateur | Interface utilisateur de niveau production, évite l'esthétique générique |

### Apprentissage et conseils

| Plugin pour la création de sites web - Plugin pour la création de sites web - Plugin pour la création de sites web - Plugin pour la création de sites web
|--------|----------|--------------|
| Le plugin d'apprentissage et d'orientation vous permet d'obtenir des informations sur les choix de code et sur la façon dont vous pouvez les utiliser.
| Apprentissage interactif | Demande de contributions aux points de décision |
| **sécurité-guidance** | Sensibilisation à la sécurité | Avertit des problèmes de sécurité lors de l'édition |

### Serveurs de langue (LSP)

| Plugin | Langue |
|--------|----------|
**typescript-lsp** | TypeScript/JavaScript | **pyright-lsp** | Python
| **pyright-lsp** | Python | **gopls-lsp** | Python
**gopls-lsp** | Go | **popls-lsp** | Python
| **gopls-lsp** | Go | **rust-analyzer-lsp** | Rust | **clangd-lsp** | Rust
| **clangd-lsp** | C/C++ | **jdtls-lsp** | Rust
| **jdtls-lsp** | Java | **kotlin-lsp** | Rust
**kotlin-lsp** | Kotlin | **swift-lsp** | Rust
| **swift-lsp** | Swift | **csharp-lsp** | Kotlin
| **csharp-lsp** | C# | **php-lsp** | Kotlin
**csharp-lsp** | C# | **php-lsp** | PHP | **lua-lsp** | Kotlin
| **lua-lsp** | Lua | **csharp-lsp** | C# | **php-lsp** | PHP

---

## Référence rapide : Codebase → Plugin

| Codebase Signal | Plugin recommandé
|-----------------|-------------------|
| Construire des plugins | plugin-dev |
| | flux de travail basé sur les PR | pr-review-toolkit | | flux de travail basé sur les PR
| Création de plugins : plugin-dev
| React/Vue/Angular | frontend-design |
| Projet TypeScript - typescript-impression - règles d'automatisation - hookify
Projet TypeScript | typescript-lsp | Projet Python | pyright-lsp
Projet Python | pyright-lsp | Projet Go | gopls-lsp
Projet Go | gopls-lsp | Projet Python | pyright-lsp
Code sensible à la sécurité | security-guidance | code sensible à la sécurité | security-guidance | code sensible à la sécurité
| Apprentissage/onboarding | explanatory-output-style |

---

## Gestion des plugins

```bash
# Installer un plugin
/plugin install <nom du plugin>

# Liste des plugins installés
/plugin list

# Afficher les détails du plugin
/plugin info <nom du plugin>
```

---

## Quand recommander des plugins

**Recommander l'installation d'un plugin lorsque:**
- L'utilisateur souhaite installer des automatismes Claude Code à partir du dépôt officiel d'Anthropic ou d'une autre place de marché partagée.
- L'utilisateur a besoin de plusieurs fonctionnalités connexes
- L'équipe veut des flux de travail standardisés
- Première installation de Claude Code