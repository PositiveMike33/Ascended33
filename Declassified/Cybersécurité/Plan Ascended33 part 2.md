## Contexte

Le dépôt `Ascended33` est une application template minimale de Streamlit qui rend une visualisation interactive en spirale. Il n'y a pas de fichier `CLAUDE.md` existant. La tâche consiste à en créer un qui documente la structure de la base de code, les flux de développement et les conventions de l'assistant d'intelligence artificielle.

## Résumé du dépôt

- Type** : Python Streamlit web app (modèle de visualisation de la spirale)
- Pile** : Python, Streamlit, Altair (graphiques), NumPy, Pandas
- Point d'entrée** : `streamlit_app.py`
- **Dépendances** : `requirements.txt` (altair, pandas, streamlit)
- Environnement de développement** : Conteneur de développement via `.devcontainer/devcontainer.json` utilisant `ghcr.io/streamlit/basic-template:latest`
- **CI** : `.github/workflows/devcontainer-build-and-push.yml` construit/pousse l'image du conteneur de développement vers GHCR sur les poussées vers `main`
- **Port** : 8501 (Streamlit par défaut)
- **Branch** : `claude/claude-md-mlt4a9w9zx36kf7g-AqS9u`

## Inventaire des fichiers

|Chemin d'accès|Objet|
|---|---|
|`streamlit_app.py`|Application principale - graphique en spirale avec curseurs interactifs|
|Requirements.txt`|Dépendances Python (altair, pandas, streamlit)
|`README.md`|Instructions d'utilisation de base|
|`.devcontainer/devcontainer.json`|Codespaces/configuration locale du conteneur de développement|
|.github/.devcontainer/devcontainer.json``Configuration de la construction de l'image du conteneur de développement
|`.github/workflows/devcontainer-build-and-push.yml`|CI : build & push container image|
|`LICENSE`|Licence MIT|

## Plan

### Action

Créez `/home/user/Ascended33/CLAUDE.md` avec les sections suivantes :

1. **Vue d'ensemble du projet** - ce qu'est ce repo, son but
2. **Structure de la base de code** - arbre des fichiers avec descriptions
3. **Configuration du développement** - instructions locales + devcontainer
4. **Exécution de l'application** - commande `streamlit run` (en anglais)
5. **Conventions clés** - style Python, gestion des dépendances
6. **CI/CD** - flux de construction de l'image devcontainer
7. **Guides de l'assistant IA** - ce qu'il faut faire/ne pas faire quand on modifie ce repo

### Fichiers critiques à créer

- `/home/user/Ascended33/CLAUDE.md` (nouveau fichier)

### Vérification

- Lisez le fichier après l'avoir écrit pour confirmer que le contenu est correct.
- Commit et push vers `claude/claude-md-mlt4a9w9zx36kf7g-AqS9u`
- Confirmez que le transfert a réussi