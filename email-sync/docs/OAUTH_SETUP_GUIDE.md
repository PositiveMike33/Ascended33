# Guide de Configuration OAuth - Email Sync MCP

Ce guide détaille la configuration complète des credentials OAuth pour Gmail, Outlook et Google Calendar.

## Table des matières
1. [Configuration Google OAuth](#configuration-google-oauth)
2. [Configuration Microsoft OAuth](#configuration-microsoft-oauth)
3. [Vérification et Activation](#vérification-et-activation)
4. [Dépannage](#dépannage)

---

## Configuration Google OAuth

### Étape 1 : Créer un projet Google Cloud

1. Allez sur [Google Cloud Console](https://console.cloud.google.com/)
2. Connectez-vous avec votre compte Google
3. Cliquez sur le sélecteur de projet en haut
4. Cliquez sur "NOUVEAU PROJET"
5. Entrez le nom : `Email Sync MCP`
6. Cliquez sur "CRÉER"

**Attendez 1-2 minutes** que le projet soit créé.

### Étape 2 : Activer les APIs requises

1. Dans la barre de recherche, tapez `Gmail API`
2. Cliquez sur "Gmail API"
3. Cliquez sur "ACTIVER"
4. Répétez pour `Google Calendar API`

### Étape 3 : Créer les credentials OAuth

1. Accédez à **Identifiants** (Credentials) dans le menu de gauche
2. Cliquez sur "CRÉER DES IDENTIFIANTS"
3. Sélectionnez "ID client OAuth"
4. Choisissez le type d'application : **Application de bureau**
5. Cliquez sur "CRÉER"

### Étape 4 : Configurer l'écran de consentement OAuth

Si vous voyez un message "Vous devez d'abord configurer l'écran de consentement OAuth" :

1. Cliquez sur "CONFIGURER L'ÉCRAN DE CONSENTEMENT"
2. Choisissez le type d'utilisateur : **Personnel** (ou votre préférence)
3. Cliquez sur "CRÉER"
4. Remplissez les informations :
   - **Nom de l'application** : Email Sync MCP
   - **Email d'assistance** : Votre email
   - **Contacts pour les questions relatives à la confidentialité** : Votre email
5. Cliquez sur "ENREGISTRER ET CONTINUER"
6. Cliquez sur "AJOUTER OU SUPPRIMER DES CHAMPS" et sélectionnez :
   - `gmail.readonly` - Lire les e-mails Gmail
   - `gmail.send` - Envoyer des e-mails Gmail
   - `calendar.readonly` - Lire le calendrier
7. Cliquez sur "ENREGISTRER ET CONTINUER"
8. Cliquez sur "RETOUR AU TABLEAU DE BORD"

### Étape 5 : Obtenir vos credentials

1. Retournez à **Identifiants**
2. Sous "ID client OAuth 2.0", cliquez sur votre application créée
3. Vous verrez :
   - **ID client** : Copiez cette valeur
   - **Clé secrète client** : Cliquez sur l'icône d'œil et copiez cette valeur
4. Conservez ces valeurs pour l'étape de configuration

**Format :**
```
CLIENT_ID: 123456789-abc...xyz.apps.googleusercontent.com
CLIENT_SECRET: GOCSPX-...
```

---

## Configuration Microsoft OAuth

### Étape 1 : Accéder à Azure Portal

1. Allez sur [Azure Portal](https://portal.azure.com/)
2. Connectez-vous avec votre compte Microsoft
3. Cherchez "Inscriptions d'applications" dans la barre de recherche
4. Cliquez sur "Inscriptions d'applications"

### Étape 2 : Créer une nouvelle application

1. Cliquez sur "Nouvelle inscription"
2. Entrez le nom : `Email Sync MCP`
3. Sélectionnez "Comptes dans un répertoire d'organisation et comptes Microsoft personnels"
4. Cliquez sur "Inscrire"

### Étape 3 : Configurer l'URI de redirection

1. Dans le menu de gauche, cliquez sur "Authentification"
2. Sous "URI de redirection", cliquez sur "Ajouter une plateforme"
3. Sélectionnez "Mobile and desktop applications"
4. Ajoutez l'URI : `http://localhost:3000/auth/callback`
5. Cliquez sur "Configurer"

### Étape 4 : Créer un secret client

1. Dans le menu de gauche, cliquez sur "Certificats et secrets"
2. Cliquez sur "Nouveau secret client"
3. Description : `Email Sync MCP Secret`
4. Expires in : `24 mois`
5. Cliquez sur "Ajouter"
6. Copiez la **Valeur** du secret créé (pas l'ID)

### Étape 5 : Obtenir l'ID d'application

1. Allez dans l'onglet "Vue d'ensemble"
2. Copiez l'**ID d'application (client)**

**Format :**
```
MICROSOFT_CLIENT_ID: 12345678-abcd-1234-abcd-123456789012
MICROSOFT_CLIENT_SECRET: abcd~123...XYZ
```

### Étape 6 : Configurer les permissions d'API

1. Cliquez sur "Autorisations de l'API" dans le menu de gauche
2. Cliquez sur "Ajouter une autorisation"
3. Sélectionnez "Microsoft Graph"
4. Cliquez sur "Autorisations déléguées"
5. Recherchez et sélectionnez :
   - `Mail.Read` - Lire les e-mails
   - `Mail.Send` - Envoyer des e-mails
   - `Calendar.Read` - Lire le calendrier
6. Cliquez sur "Ajouter des autorisations"

---

## Vérification et Activation

### Étape 1 : Créer le fichier .env

```bash
cd email-sync
npm run setup
```

Le script interactif vous demandera :
1. Les credentials Google (CLIENT_ID, CLIENT_SECRET)
2. Les credentials Microsoft
3. Le chemin de votre coffre Obsidian

### Étape 2 : Vérifier la configuration

```bash
npm run verify
```

Ce script vérifie :
- ✅ Node.js version 18+
- ✅ Fichier .env créé
- ✅ Tous les fichiers source présents
- ✅ Dossier config/ créé
- ✅ Permissions Obsidian

### Étape 3 : Démarrer le serveur

```bash
npm start
```

Vous verrez :
```
Email Sync MCP Server running on stdio transport
```

---

## Dépannage

### Problème : "Invalid Client ID"
**Solution :** 
- Vérifiez que vous copiez exactement l'ID client depuis Google Cloud Console
- Assurez-vous qu'il n'y a pas d'espaces au début ou à la fin

### Problème : "Redirect URI mismatch"
**Solution :**
- Vérifiez que l'URI de redirection dans Azure Portal correspond à celle du script setup
- Par défaut : `http://localhost:3000/auth/callback`

### Problème : "Permission denied for Calendar API"
**Solution :**
- Revenez à Google Cloud Console
- Vérifiez que Google Calendar API est activée
- Attendez 5-10 minutes après l'activation

### Problème : "Token refresh failed"
**Solution :**
- Supprimez le fichier `config/token.json`
- Réexécutez `npm run setup`
- Le script vous demandera une nouvelle autorisation

### Problème : ".env file not found"
**Solution :**
```bash
npm run setup
# Suivi de
npm run verify
```

---

## Variables d'environnement requises

```env
# Google OAuth
GOOGLE_CLIENT_ID=your_client_id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your_client_secret
GOOGLE_REDIRECT_URI=http://localhost:3000/auth/callback

# Microsoft OAuth
MICROSOFT_CLIENT_ID=your_app_id
MICROSOFT_CLIENT_SECRET=your_client_secret
MICROSOFT_REDIRECT_URI=http://localhost:3000/auth/microsoft/callback

# Obsidian
OBSIDIAN_VAULT_PATH=/path/to/your/vault
OBSIDIAN_DAILY_FOLDER=Daily Notes
OBSIDIAN_ARCHIVE_FOLDER=Archive

# MCP Server
MCP_PORT=3000
MCP_HOST=localhost
```

---

## Sécurité

⚠️ **IMPORTANT :**
- Ne commitez JAMAIS votre fichier `.env` sur Git
- Conservez vos credentials en lieu sûr
- Utilisez `npm run setup` pour configurer sur chaque machine
- Les tokens d'accès sont stockés dans `config/token.json` (ignoré par Git)

---

## Prochaines étapes

Une fois la configuration terminée :
1. Testez avec `npm start`
2. Consultez [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) pour déployer en production
3. Consultez [MCP_INTEGRATION.md](./MCP_INTEGRATION.md) pour intégrer avec Claude Code
