---
description: Créer et configurer une nouvelle application Claude Agent SDK
argument-hint:
  - project-name
tags:
  - "#skills"
  - "#claude"
  - "#agent_sdk"
---

Vous devez aider l'utilisateur à créer une nouvelle application Claude Agent SDK. Suivez attentivement les étapes suivantes :

## Documentation de référence

Avant de commencer, consultez la documentation officielle pour vous assurer que vous fournissez des conseils précis et à jour. Utilisez WebFetch pour lire ces pages :

1. **Débutez par la vue d'ensemble** : https://docs.claude.com/en/api/agent-sdk/overview
2. **En fonction du langage choisi par l'utilisateur, lisez la référence SDK appropriée** :
   - TypeScript : https://docs.claude.com/en/api/agent-sdk/typescript
   - Python : https://docs.claude.com/en/api/agent-sdk/python
3. **Lisez les guides pertinents mentionnés dans la vue d'ensemble** tels que :
   - Streaming vs Single Mode
   - Permissions
   - Outils personnalisés
   - Intégration MCP
   - Sous-agents
   - Sessions
   - Tout autre guide pertinent en fonction des besoins de l'utilisateur

**IMPORTANT** : Vérifiez toujours les dernières versions des paquets et utilisez-les. Utilisez WebSearch ou WebFetch pour vérifier les versions actuelles avant l'installation.

## Rassembler les exigences

IMPORTANT : Posez ces questions une à la fois. Attendez la réponse de l'utilisateur avant de poser la question suivante. Il est ainsi plus facile pour l'utilisateur de répondre.

Posez les questions dans l'ordre suivant (ignorez celles que l'utilisateur a déjà fournies sous forme d'arguments) :

1. **Langue** (à poser en premier) : "Souhaitez-vous utiliser TypeScript ou Python ?"

   - Attendez la réponse avant de poursuivre

2. **Nom du projet** (deuxième question) : "Quel nom aimeriez-vous donner à votre projet ?"

   - Si $ARGUMENTS est fourni, utilisez-le comme nom de projet et sautez cette question.
   - Attendez la réponse avant de continuer

3. **Type d'agent** (poser la troisième question, mais passer si la question 2 était suffisamment détaillée) : "Quel type d'agent construisez-vous ? Quelques exemples :

   - Agent de codage (SRE, examen de la sécurité, examen du code)
   - Agent commercial (support client, création de contenu)
   - Agent personnalisé (décrivez votre cas d'utilisation)"
   - Attendez la réponse avant de poursuivre

4. **Point de départ** (quatrième question) : "Aimeriez-vous.. :

   - Un exemple minimal de 'Hello World' pour commencer
   - Un agent de base avec des caractéristiques communes
   - Un exemple spécifique basé sur votre cas d'utilisation".
   - Attendez la réponse avant de continuer

5. **Choix des outils** (demandez le cinquième) : Indiquez à l'utilisateur les outils que vous utiliserez et confirmez avec lui qu'il s'agit des outils qu'il souhaite utiliser (par exemple, il peut préférer pnpm ou bun à npm). Respectez les préférences de l'utilisateur lors de l'exécution des exigences.

Une fois que vous avez répondu à toutes les questions, passez à la création du plan d'installation.

## Plan d'installation

Sur la base des réponses de l'utilisateur, créez un plan qui comprend :

1. **Initialisation du projet** :

   - Créer le répertoire du projet (s'il n'existe pas)
   - Initialiser le gestionnaire de paquets :
     - TypeScript : `npm init -y` et configurer `package.json` avec type : "module" et des scripts (inclure un script "typecheck")
     - Python : Créez `requirements.txt` ou utilisez `poetry init`.
   - Ajoutez les fichiers de configuration nécessaires :
     - TypeScript : TypeScript : Créez `tsconfig.json` avec les paramètres appropriés pour le SDK
     - Python : Créez optionnellement des fichiers de configuration si nécessaire

2. **Vérifiez les dernières versions** :

   - AVANT l'installation, utilisez WebSearch ou vérifiez npm/PyPI pour trouver la dernière version.
   - Pour TypeScript : Vérifiez https://www.npmjs.com/package/@anthropic-ai/claude-agent-sdk
   - Pour Python : Consultez https://pypi.org/project/claude-agent-sdk/
   - Informez l'utilisateur de la version que vous installez

3. **Installation du SDK** :

   - TypeScript : `npm install @anthropic-ai/claude-agent-sdk@latest` (ou spécifiez la dernière version)
   - Python : `pip install claude-agent-sdk` (pip installe la dernière version par défaut)
   - Après l'installation, vérifiez la version installée :
     - TypeScript : Vérifiez le package.json ou exécutez `npm list @anthropic-ai/claude-agent-sdk`
     - Python : Exécutez `pip show claude-agent-sdk`

4. **Créer les fichiers de démarrage** :

   - TypeScript : Créez un `index.ts` ou `src/index.ts` avec un exemple de requête basique
   - Python : Créez un `main.py` avec un exemple de requête basique.
   - Incluez les importations appropriées et la gestion des erreurs de base
   - Utilisez une syntaxe et des modèles modernes et actualisés à partir de la dernière version du SDK.

5. **Configuration de l'environnement** :

   - Créez un fichier `.env.example` avec `ANTHROPIC_API_KEY=votre_clé_api_ici`
   - Ajoutez `.env` à `.gitignore`
   - Expliquez comment obtenir une clé d'API à partir de https://console.anthropic.com/

6. **En option : Créez la structure du répertoire .claude** :
   - Proposez de créer un répertoire `.claude/` pour les agents, les commandes et les paramètres.
   - Demandez-lui s'il souhaite des exemples de sous-agents ou de commandes slash.

## Mise en œuvre

Après avoir recueilli les besoins et obtenu la confirmation du plan par l'utilisateur :

1. Vérifier les dernières versions des paquets à l'aide de WebSearch ou de WebFetch
2. Exécutez les étapes de configuration
3. Créez tous les fichiers nécessaires
4. Installez les dépendances (utilisez toujours les dernières versions stables)
5. Vérifier les versions installées et informer l'utilisateur
6. Créez un exemple de travail basé sur leur type d'agent
7. Ajoutez des commentaires utiles dans le code pour expliquer ce que fait chaque partie.
8. **VÉRIFIEZ QUE LE CODE FONCTIONNE AVANT DE TERMINER** :
   - Pour TypeScript :
     - Exécutez `npx tsc --noEmit` pour vérifier les erreurs de type.
     - Corrigez TOUTES les erreurs de type jusqu'à ce que les types passent complètement
     - Assurez-vous que les importations et les types sont corrects
     - Ne continuez que lorsque la vérification des types est réussie sans erreur
   - Pour Python :
     - Vérifiez que les importations sont correctes
     - Vérifiez les erreurs de syntaxe de base
   - Ne considérez pas l'installation comme terminée tant que le code n'a pas été vérifié avec succès.

## Vérification

Une fois tous les fichiers créés et les dépendances installées, utilisez l'agent vérificateur approprié pour valider que l'application Agent SDK est correctement configurée et prête à être utilisée :

1. **Pour les projets TypeScript** : Lancez l'agent **agent-sdk-verifier-ts** pour valider la configuration.
2. **Pour les projets Python** : Lancez l'agent **agent-sdk-verifier-py** pour valider la configuration.
3. L'agent vérifiera l'utilisation du SDK, la configuration, les fonctionnalités et le respect de la documentation officielle.
4. Examinez le rapport de vérification et résolvez les problèmes éventuels.

## Guide de démarrage

Une fois l'installation terminée et vérifiée, fournissez à l'utilisateur :

1. **Prochaines étapes** :

   - Comment définir sa clé API
   - Comment exécuter leur agent :
     - TypeScript : `npm start` ou `node --loader ts-node/esm index.ts`
     - Python : `python main.py`

2. **Ressources utiles** :

   - Lien vers la référence du SDK TypeScript : https://docs.claude.com/en/api/agent-sdk/typescript
   - Lien vers la référence du SDK Python : https://docs.claude.com/en/api/agent-sdk/python
   - Expliquez les concepts clés : invites du système, permissions, outils, serveurs MCP.

3. **Étapes suivantes courantes** :
   - Comment personnaliser l'invite système
   - Comment ajouter des outils personnalisés via MCP
   - Comment configurer les autorisations
   - Comment créer des sous-agents

## Notes importantes

- UTILISEZ TOUJOURS LES DERNIÈRES VERSIONS** : Avant d'installer un paquet, vérifiez les dernières versions en utilisant WebSearch ou en consultant directement npm/PyPI.
- **VÉRIFIEZ QUE LE CODE S'EXÉCUTE CORRECTEMENT** :
  - Pour TypeScript : Exécutez `npx tsc --noEmit` et corrigez TOUTES les erreurs de type avant de terminer.
  - Pour Python : Vérifiez que la syntaxe et les importations sont correctes
  - Ne considérez PAS la tâche comme terminée tant que le code n'a pas passé la vérification.
- Vérifiez la version installée après l'installation et informez-en l'utilisateur.
- Consultez la documentation officielle pour toute exigence spécifique à une version (version de Node.js, version de Python, etc.)
- Vérifiez toujours si des répertoires/fichiers existent déjà avant de les créer.
- Utilisez le gestionnaire de paquets préféré de l'utilisateur (npm, yarn, pnpm pour TypeScript ; pip, poetry pour Python)
- Assurez-vous que tous les exemples de code sont fonctionnels et incluent une gestion appropriée des erreurs
- Utiliser une syntaxe et des modèles modernes compatibles avec la dernière version du SDK
- Rendez l'expérience interactive et éducative
- Posez les questions une par une** - Ne posez pas plusieurs questions dans une même réponse.

Commencez par poser uniquement la PREMIÈRE question. Attendez la réponse de l'utilisateur avant de passer à la question suivante.