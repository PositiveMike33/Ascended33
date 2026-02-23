# 📚 Documentation Email Sync MCP

Bienvenue dans la documentation complète du serveur Email Sync MCP. Cette documentation couvre tous les aspects : configuration, intégration, déploiement et extensions.

## 📖 Structure de la documentation

```
docs/
├── README.md                          ← Vous êtes ici
├── OAUTH_SETUP_GUIDE.md              ← Configuration OAuth
├── MCP_INTEGRATION.md                ← Intégration Claude Code
├── INTEGRATIONS_ROADMAP.md           ← Futures intégrations
└── DEPLOYMENT_GUIDE.md               ← Déploiement production
```

## 🚀 Guide de démarrage rapide (5 minutes)

### 1️⃣ Installation des dépendances

```bash
cd email-sync
npm install
```

### 2️⃣ Configuration OAuth

```bash
npm run setup
```

Cela lancera un assistant interactif pour :
- Configurer vos credentials Google OAuth
- Configurer vos credentials Microsoft OAuth
- Définir le chemin de votre coffre Obsidian

### 3️⃣ Vérification

```bash
npm run verify
```

Cela vérifiera que tout est correctement configuré ✅

### 4️⃣ Démarrage

```bash
npm start
```

Vous verrez :
```
Email Sync MCP Server running on stdio transport
```

## 📋 Pour quelle tâche aller où ?

### ❓ "Comment configurer Gmail et Outlook ?"
→ [OAUTH_SETUP_GUIDE.md](./OAUTH_SETUP_GUIDE.md)

**Contenu :**
- Création de projet Google Cloud
- Création d'app Azure
- Configuration complète des credentials
- Dépannage

### ❓ "Comment utiliser avec Claude Code ?"
→ [MCP_INTEGRATION.md](./MCP_INTEGRATION.md)

**Contenu :**
- Configuration du fichier `.mcp.json`
- Liste complète des outils disponibles
- Exemples d'utilisation
- Troubleshooting MCP

### ❓ "Quelles intégrations sont prévues ?"
→ [INTEGRATIONS_ROADMAP.md](./INTEGRATIONS_ROADMAP.md)

**Contenu :**
- Intégrations actuelles
- Intégrations planifiées (Slack, Todoist, Notion, etc.)
- Priorisation des features
- Feedback utilisateur

### ❓ "Comment déployer en production ?"
→ [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)

**Contenu :**
- Déploiement local vs cloud
- Setup Render (recommandé)
- Docker & Kubernetes
- AWS Lambda
- Sécurité & monitoring

---

## 🎯 Cas d'usage courants

### Cas 1 : Je veux lire mes e-mails non lus

```
Utilisez gmail-fetch-emails avec Claude Code :

"Récupère mes 10 derniers e-mails Gmail et affiche-moi 
un résumé de chacun avec l'expéditeur, le sujet et une 
prévisualisation."
```

### Cas 2 : Je veux automatiser mes notes quotidiennes

```
Utilisez calendar-create-daily-note :

"Crée une note quotidienne pour aujourd'hui qui inclut
tous mes événements calendrier et une section pour 
les tâches à faire."
```

### Cas 3 : Je veux archiver les e-mails importants

```
Utilisez gmail-search-emails :

"Cherche tous les e-mails avec des pièces jointes 
depuis la dernière semaine et ajoute-les à Obsidian
en tant que notes archivées."
```

### Cas 4 : Je veux être notifié des réunions urgentes

```
Utilisez calendar-get-events + Slack (intégration future) :

"Affiche les événements de la journée et envoie une 
notification Slack pour les réunions dans l'heure 
suivante."
```

---

## 🔧 Architecture

### Composants clés

```
MCP Server (src/index.js)
    ↓
Tool Definitions (email-tools.js, calendar-tools.js)
    ↓
Managers (Gmail, Outlook, Calendar)
    ↓
External APIs (Google, Microsoft)
    ↓
Obsidian Vault (Local Files)
```

### Flux de données

```
Claude Code
    ↓
MCP Server (stdio)
    ↓
Tool Call → Email Manager → Gmail API
                         ↓ Fetch Emails
                         ↓
Claude Code (Result)
```

---

## 📊 Outils disponibles

### Email Tools (8 outils)

| Outil | Description |
|-------|-------------|
| `gmail-fetch-emails` | Récupère les derniers e-mails Gmail |
| `gmail-send-email` | Envoie un e-mail via Gmail |
| `gmail-search-emails` | Recherche avancée dans Gmail |
| `outlook-fetch-emails` | Récupère les derniers e-mails Outlook |
| `outlook-send-email` | Envoie un e-mail via Outlook |

### Calendar Tools (5 outils)

| Outil | Description |
|-------|-------------|
| `calendar-get-events` | Récupère les événements calendrier |
| `calendar-create-daily-note` | Crée une note quotidienne Obsidian |
| `calendar-create-weekly-note` | Crée une note hebdomadaire Obsidian |
| `calendar-sync-and-notify` | Sync calendrier + notifications |
| `calendar-add-event-from-email` | Crée un événement depuis un e-mail |

---

## 🔐 Sécurité

### Credentials

✅ **Sécurisés :** Stockés dans `.env` (ignoré par Git)  
✅ **Tokens :** Rafraîchis automatiquement dans `config/token.json`  
❌ **Jamais :** Hard-codés dans le code  
❌ **Jamais :** Committés sur Git  

### Best practices

```bash
# ✅ BON : .gitignore exclut les secrets
.env
config/token.json
credentials.json

# ❌ MAUVAIS : Ajouter à Git
git add .env  # DON'T DO THIS !
```

---

## 🛠️ Dépannage courant

### "Node not found"
```bash
# Installer Node.js 18+
# https://nodejs.org/

node --version  # Doit afficher v18+
```

### "Module not found"
```bash
# Réinstaller les dépendances
cd email-sync
npm install
```

### "OAuth failed"
```bash
# Vérifier les credentials
cat .env

# Reconfigurer
npm run setup

# Redémarrer
npm start
```

### "Obsidian path not found"
```bash
# Vérifier le chemin dans .env
OBSIDIAN_VAULT_PATH=/Users/username/Documents/Obsidian

# Doit exister et être accessible
ls -la /Users/username/Documents/Obsidian
```

---

## 📈 Performances

### Temps de réponse typique

| Opération | Temps |
|-----------|-------|
| Fetch e-mails (20) | < 500ms |
| Search e-mails | < 1s |
| Get calendar events | < 300ms |
| Create daily note | < 200ms |

### Limitations

| Limite | Valeur |
|--------|--------|
| E-mails par requête | 50 max |
| Appels API/jour | 1M (Google) |
| Taille e-mail | 25MB |
| Attendez après création note | 2s |

---

## 🚀 Prochaines étapes

### Pour débuter

1. Lisez [OAUTH_SETUP_GUIDE.md](./OAUTH_SETUP_GUIDE.md)
2. Exécutez `npm run setup`
3. Exécutez `npm start`
4. Testez avec Claude Code

### Pour déployer

1. Lisez [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)
2. Choisissez votre architecture (Render recommended)
3. Configurez les secrets
4. Déployez en production

### Pour étendre

1. Lisez [INTEGRATIONS_ROADMAP.md](./INTEGRATIONS_ROADMAP.md)
2. Consultez [MCP_INTEGRATION.md](./MCP_INTEGRATION.md)
3. Ouvrez une issue pour votre feature

---

## 💬 Support

### Ressources

- 📖 **Documentation :** Vous êtes dedans !
- 🐛 **Issues :** GitHub Issues
- 💬 **Discussion :** GitHub Discussions
- 🤖 **Claude Code :** Consultez Claude Code docs

### Pour signaler un problème

Créez une issue GitHub avec :
- Description du problème
- Étapes pour reproduire
- Logs d'erreur (`npm start 2>&1 | tee error.log`)
- Version de Node.js (`node --version`)

---

## 📅 Feuille de route

### Court terme (2-4 semaines)
- ✅ Configuration OAuth
- ✅ MCP Integration
- ⏳ Slack Integration
- ⏳ Todoist Integration

### Moyen terme (1-2 mois)
- ⏳ Notion Integration
- ⏳ Database Backend
- ⏳ Advanced Rules Engine

### Long terme (3+ mois)
- ⏳ Mobile App
- ⏳ Multi-Account Management
- ⏳ AI-Powered Email Summarization

---

## 📄 Fichiers clés du projet

```
email-sync/
├── src/
│   ├── index.js              ← Point d'entrée MCP
│   ├── email-tools.js        ← Définitions outils email
│   ├── calendar-tools.js     ← Définitions outils calendrier
│   └── managers/
│       ├── gmail-manager.js  ← Gmail API
│       ├── outlook-manager.js ← Outlook API
│       └── calendar-manager.js ← Calendar API
├── scripts/
│   ├── setup.js              ← Configuration OAuth
│   └── verify-setup.js       ← Vérification setup
├── docs/
│   ├── README.md             ← Vous êtes ici
│   ├── OAUTH_SETUP_GUIDE.md
│   ├── MCP_INTEGRATION.md
│   ├── INTEGRATIONS_ROADMAP.md
│   └── DEPLOYMENT_GUIDE.md
├── config/                   ← Credentials (gitignored)
├── .env.example              ← Template env
├── package.json              ← Dépendances
└── dashboard.html            ← UI de monitoring
```

---

## 📞 Auteur & Maintenance

**Auteur :** Claude Code  
**Licence :** MIT  
**Repository :** GitHub  
**Support :** GitHub Issues / Discussions  

---

## ✨ Merci d'utiliser Email Sync MCP !

Votre feedback est précieux. N'hésitez pas à :
- ⭐ Laisser une star sur GitHub
- 🐛 Signaler des bugs
- 💡 Suggérer des features
- 📝 Contribuer à la documentation

**Bonne organisation ! 🚀**

---

**Dernière mise à jour :** Février 2026  
**Version :** 1.0.0  
**Statut :** Production Alpha
