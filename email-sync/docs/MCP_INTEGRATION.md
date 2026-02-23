# Intégration MCP - Email Sync avec Claude Code

Guide complet pour intégrer le serveur Email Sync MCP dans Claude Code.

## 📋 Prérequis

- Claude Code installé et fonctionnel
- Node.js 18+
- Email Sync MCP configuré avec OAuth (voir [OAUTH_SETUP_GUIDE.md](./OAUTH_SETUP_GUIDE.md))
- Fichier `.env` rempli et testé avec `npm run verify`

---

## 1️⃣ Configuration du fichier `.mcp.json`

Le fichier `.mcp.json` se trouve à la racine du worktree et configure les serveurs MCP accessibles.

### Localisation

```
D:\Vault\Vault\.claude\worktrees\nostalgic-chandrasekhar\.mcp.json
```

### Configuration Email Sync

```json
{
  "mcpServers": {
    "email-sync": {
      "command": "node",
      "args": ["email-sync/src/index.js"],
      "env": {
        "NODE_PATH": "./email-sync",
        "DOTENV_PATH": "./email-sync/.env"
      }
    }
  }
}
```

### Explication des champs

| Champ | Description |
|-------|-------------|
| `command` | Exécutable à lancer (node pour JS) |
| `args` | Arguments passés à node (chemin du script MCP) |
| `env` | Variables d'environnement pour le processus |

---

## 2️⃣ Structure du projet pour MCP

Assurez-vous que la structure suit ce pattern :

```
email-sync/
├── src/
│   ├── index.js          ← Point d'entrée MCP
│   ├── email-tools.js
│   ├── calendar-tools.js
│   └── managers/
├── config/
│   ├── credentials.json  ← OAuth credentials
│   └── token.json        ← Tokens d'accès
├── .env                  ← Variables configurées
├── .env.example
├── package.json
└── dashboard.html
```

---

## 3️⃣ Démarrer le serveur MCP

### Option 1 : Ligne de commande Claude Code

```bash
claude mcp start email-sync
```

### Option 2 : Depuis le répertoire email-sync

```bash
cd email-sync
npm start
```

**Output attendu :**
```
Email Sync MCP Server running on stdio transport
Listening for tool calls...
```

---

## 4️⃣ Vérifier la connexion MCP

### Dans Claude Code

Utilisez la commande intégrée :

```
/mcp email-sync status
```

Ou testez directement avec un prompt :

```
Que puis-je faire avec le serveur Email Sync MCP ?
```

Claude répondra avec les outils disponibles.

---

## 5️⃣ Outils disponibles dans MCP

Une fois connecté, ces outils sont disponibles pour Claude Code :

### Email Tools

#### `gmail-fetch-emails`
Récupère les derniers e-mails Gmail

```javascript
{
  "limit": 20  // Nombre d'e-mails (max 50)
}
```

**Réponse :**
```json
{
  "emails": [
    {
      "id": "email_id",
      "from": "user@example.com",
      "subject": "Subject",
      "preview": "First 100 chars...",
      "date": "2026-02-23T10:30:00Z",
      "unread": true
    }
  ]
}
```

#### `gmail-send-email`
Envoie un e-mail via Gmail

```javascript
{
  "to": "recipient@example.com",
  "subject": "Test Subject",
  "body": "E-mail body",
  "cc": "cc@example.com",      // Optionnel
  "bcc": "bcc@example.com"     // Optionnel
}
```

#### `gmail-search-emails`
Recherche avancée dans Gmail

```javascript
{
  "query": "from:sender@example.com subject:urgent",
  "limit": 10
}
```

**Syntaxe de recherche :**
- `from:address@example.com` - Par expéditeur
- `subject:text` - Par sujet
- `has:attachment` - Avec pièce jointe
- `is:unread` - E-mails non lus
- `before:2026-02-20` - Avant une date
- `after:2026-02-20` - Après une date

#### `outlook-fetch-emails`
Récupère les e-mails Outlook

```javascript
{
  "limit": 20
}
```

#### `outlook-send-email`
Envoie un e-mail via Outlook

```javascript
{
  "to": "recipient@example.com",
  "subject": "Test Subject",
  "body": "E-mail body"
}
```

### Calendar Tools

#### `calendar-get-events`
Récupère les événements calendrier

```javascript
{
  "days": 7,           // Nombre de jours à l'avance
  "account": "google"  // "google" ou "microsoft"
}
```

#### `calendar-create-daily-note`
Crée une note quotidienne dans Obsidian

```javascript
{
  "date": "2026-02-23",     // Format YYYY-MM-DD
  "account": "google"
}
```

Génère un fichier markdown :
```
2026-02-23 - Daily Note.md
├── Événements
├── Tasks
└── Notes
```

#### `calendar-create-weekly-note`
Crée une note hebdomadaire

```javascript
{
  "weekStart": "2026-02-23",  // Lundi de la semaine
  "account": "google"
}
```

---

## 6️⃣ Exemples d'utilisation dans Claude Code

### Exemple 1 : Récupérer et résumer les e-mails non lus

```
Utilise gmail-fetch-emails pour récupérer les 10 derniers e-mails non lus.
Ensuite, créé un résumé formaté en markdown avec :
- L'expéditeur
- Le sujet
- Un aperçu du contenu
```

### Exemple 2 : Automatiser les notes quotidiennes

```
Crée une note quotidienne pour aujourd'hui en utilisant calendar-create-daily-note.
Récupère aussi les 5 prochains événements avec calendar-get-events.
Ajoute ces événements à la note créée.
```

### Exemple 3 : Recherche et tri d'e-mails

```
Cherche tous les e-mails contenant "invoice" depuis la dernière semaine.
Trie-les par date décroissante.
Génère une table markdown avec : date, expéditeur, sujet.
```

---

## 7️⃣ Dépannage MCP

### Problème : "MCP server not found"

**Solution :**
1. Vérifiez que `.mcp.json` existe dans le worktree
2. Vérifiez la syntaxe JSON (pas de virgules manquantes)
3. Vérifiez le chemin vers `email-sync/src/index.js`

### Problème : "Node not found"

**Solution :**
```bash
# Vérifiez que Node.js est installé
node --version

# Vérifiez que npm a installé les dépendances
cd email-sync && npm install
```

### Problème : "Tools not available"

**Solution :**
1. Vérifiez que `npm run verify` passe tous les tests
2. Redémarrez le serveur MCP : `npm start`
3. Vérifiez le fichier `.env` est correctement configuré

### Problème : "Authentication failed"

**Solution :**
1. Supprimez `config/token.json`
2. Relancez `npm run setup`
3. Autorisez l'accès OAuth
4. Redémarrez le serveur MCP

---

## 8️⃣ Gestion des credentials en MCP

### Stockage sécurisé

Les credentials sont stockés dans :
- `.env` - Variables de configuration (ignoré par Git)
- `config/token.json` - Tokens d'accès (ignoré par Git)

### Best practices

```bash
# ✅ BON : Committer la structure, pas les secrets
git add .
git rm --cached .env config/
git commit -m "Add email-sync structure"

# ❌ MAUVAIS : Committer les secrets
git add .env config/token.json
git commit -m "Add config"  # DANGER !
```

### Rotation des tokens

```bash
# Si un token est compromis
rm config/token.json
npm run setup
# Sélectionnez "Re-authorize" pour obtenir un nouveau token
```

---

## 9️⃣ Performance et limitations MCP

### Limitations

| Limite | Valeur |
|--------|--------|
| E-mails par requête | 50 |
| Caractères par e-mail | 10,000 |
| Appels API Gmail/jour | 1,000,000 (rate limit Google) |
| Délai réponse MCP | < 5s |

### Optimisation

```javascript
// ❌ Lent : Récupère tous les e-mails
const emails = await client.fetchEmails(1000);

// ✅ Rapide : Récupère par lots de 50
for (let i = 0; i < 1000; i += 50) {
  const batch = await client.fetchEmails(50);
  processEmails(batch);
}
```

---

## 🔟 Monitoring et logs

### Activer les logs détaillés

```bash
# Dans le terminal
DEBUG=email-sync:* npm start
```

### Fichier log (optionnel)

```javascript
// Dans src/index.js
const fs = require('fs');
const logStream = fs.createWriteStream('mcp.log', { flags: 'a' });

console.log = (...args) => {
  logStream.write(args.join(' ') + '\n');
};
```

### Vérifier l'état du serveur

```bash
# Dans un autre terminal
curl http://localhost:3000/status

# Réponse
{
  "status": "running",
  "tools": 8,
  "uptime": 3600
}
```

---

## 1️⃣1️⃣ Tests MCP

### Test simple

```
Récupère 5 e-mails Gmail.
Affiche le premier e-mail complet (from, subject, body).
```

### Test d'authentification

```
Crée une note quotidienne pour aujourd'hui.
Si ça fonctionne, l'authentification OAuth est valide.
```

### Test de performance

```
Récupère 50 e-mails et mesure le temps.
Devrait prendre < 2 secondes.
```

---

## 1️⃣2️⃣ Intégration avancée : Hooks

Vous pouvez créer des hooks Claude Code qui utilisent Email Sync automatiquement.

### Exemple : Hook post-commit

```json
{
  "hooks": {
    "post-commit": {
      "pattern": "^feat:|^fix:",
      "commands": [
        "claude mcp call email-sync gmail-send-email",
        "to=team@example.com subject=Commit from=notifications@example.com"
      ]
    }
  }
}
```

---

## 1️⃣3️⃣ Prochaines étapes

1. ✅ Configuration OAuth complète
2. ✅ Lancement du serveur MCP
3. ✅ Vérification de la connexion
4. ⏭️ **Prochaines :** Consulter [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)

---

**Besoin d'aide ?**
- Consultez [OAUTH_SETUP_GUIDE.md](./OAUTH_SETUP_GUIDE.md) pour les problèmes d'authentification
- Consultez [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) pour le déploiement en production
- Consultez [INTEGRATIONS_ROADMAP.md](./INTEGRATIONS_ROADMAP.md) pour les futures intégrations
