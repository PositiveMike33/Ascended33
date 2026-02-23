# Guide de Déploiement - Email Sync MCP

Guide complet pour déployer Email Sync MCP en production.

## 📊 Architectures de déploiement

### Option 1 : Local (Développement)
- **Coût :** $0
- **Uptime :** Dépend de votre machine
- **Idéal pour :** Tests, développement
- **Limitation :** Pas de redondance

### Option 2 : Serveur cloud (Production)
- **Coût :** $20-50/mois
- **Uptime :** 99.9%
- **Idéal pour :** Production
- **Options :** Heroku, Railway, Render

### Option 3 : Conteneur Docker (Scalable)
- **Coût :** $50-200/mois
- **Uptime :** 99.99%
- **Idéal pour :** Équipes, high-volume
- **Options :** Docker Hub, Kubernetes, AWS ECS

---

## 🚀 Déploiement sur Render (Recommandé)

### Avantages
✅ Gratuit le premier mois  
✅ Déploiement facile depuis GitHub  
✅ Support PostgreSQL inclus  
✅ Logs centralisés  

### Étape 1 : Préparer le code pour Render

```bash
# À la racine du projet
touch render.yaml
```

**Contenu de `render.yaml` :**

```yaml
services:
  - type: web
    name: email-sync-mcp
    runtime: node
    startCommand: cd email-sync && npm start
    env:
      - key: GOOGLE_CLIENT_ID
        value: ${GOOGLE_CLIENT_ID}
      - key: GOOGLE_CLIENT_SECRET
        value: ${GOOGLE_CLIENT_SECRET}
      - key: MICROSOFT_CLIENT_ID
        value: ${MICROSOFT_CLIENT_ID}
      - key: MICROSOFT_CLIENT_SECRET
        value: ${MICROSOFT_CLIENT_SECRET}
      - key: MCP_HOST
        value: 0.0.0.0
      - key: MCP_PORT
        value: 3000
    disk:
      name: data
      mountPath: /data
```

### Étape 2 : Créer un compte Render

1. Allez sur [render.com](https://render.com)
2. Cliquez "Sign up"
3. Connectez-vous avec GitHub

### Étape 3 : Connecter votre repository

1. Cliquez sur "New+" → "Web Service"
2. Sélectionnez votre repository
3. Remplissez les informations :
   - **Name:** `email-sync-mcp`
   - **Runtime:** Node
   - **Build command:** `cd email-sync && npm install`
   - **Start command:** `cd email-sync && npm start`

### Étape 4 : Configurer les variables d'environnement

1. Allez dans "Environment"
2. Ajoutez :
   - `GOOGLE_CLIENT_ID`
   - `GOOGLE_CLIENT_SECRET`
   - `MICROSOFT_CLIENT_ID`
   - `MICROSOFT_CLIENT_SECRET`
   - `OBSIDIAN_VAULT_PATH` (optionnel)

3. Cliquez "Create Web Service"

### Étape 5 : Déploiement automatique

Chaque fois que vous pushez sur la branche :

```bash
git push origin main
```

Render redéploie automatiquement ! ✨

---

## 🐳 Déploiement avec Docker

### Étape 1 : Créer le Dockerfile

```dockerfile
# email-sync/Dockerfile
FROM node:18-alpine

WORKDIR /app

# Installer les dépendances
COPY package*.json ./
RUN npm install

# Copier le code
COPY . .

# Exposer le port
EXPOSE 3000

# Santé du conteneur
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
  CMD node -e "require('http').get('http://localhost:3000/health', (r) => {if (r.statusCode !== 200) throw new Error(r.statusCode)})"

# Démarrer le serveur
CMD ["npm", "start"]
```

### Étape 2 : Créer docker-compose.yml

```yaml
version: '3.9'

services:
  email-sync:
    build: ./email-sync
    ports:
      - "3000:3000"
    environment:
      - GOOGLE_CLIENT_ID=${GOOGLE_CLIENT_ID}
      - GOOGLE_CLIENT_SECRET=${GOOGLE_CLIENT_SECRET}
      - MICROSOFT_CLIENT_ID=${MICROSOFT_CLIENT_ID}
      - MICROSOFT_CLIENT_SECRET=${MICROSOFT_CLIENT_SECRET}
      - MCP_HOST=0.0.0.0
      - MCP_PORT=3000
    volumes:
      - ./email-sync/config:/app/config
      - ./email-sync/.env:/app/.env
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "node", "-e", "require('http').get('http://localhost:3000/health')"]
      interval: 30s
      timeout: 3s
      retries: 3
```

### Étape 3 : Déployer avec Docker

```bash
# Build l'image
docker-compose build

# Lance le conteneur
docker-compose up -d

# Vérifier le statut
docker-compose ps

# Voir les logs
docker-compose logs -f email-sync

# Arrêter
docker-compose down
```

---

## ☁️ Déploiement sur AWS Lambda (Serverless)

### Avantages
✅ Pay-as-you-go (~$1/mois si usage modéré)  
✅ Scalabilité automatique  
✅ Pas de serveur à gérer  

### Limitations
❌ Cold start (~3s)  
❌ Timeout max 15 minutes  

### Setup

```bash
# 1. Installer Serverless Framework
npm install -g serverless

# 2. Créer serverless.yml
touch email-sync/serverless.yml
```

**serverless.yml :**

```yaml
service: email-sync-mcp

provider:
  name: aws
  runtime: nodejs18.x
  region: eu-west-1
  environment:
    GOOGLE_CLIENT_ID: ${env:GOOGLE_CLIENT_ID}
    GOOGLE_CLIENT_SECRET: ${env:GOOGLE_CLIENT_SECRET}

functions:
  sync:
    handler: src/index.handler
    events:
      - http:
          path: /sync
          method: post
    timeout: 300
    memorySize: 512

plugins:
  - serverless-plugin-tracing

package:
  individually: true
  exclude:
    - node_modules/**
```

### Déployer

```bash
cd email-sync
serverless deploy
```

---

## 🔐 Sécurité - Checklist pré-production

### Variables d'environnement

- [ ] Aucun secret hard-codé dans le code
- [ ] Tous les secrets dans `.env` (ignoré par Git)
- [ ] Credentials stockés dans les secrets du serveur
- [ ] Tokens OAuth rafraîchis régulièrement

### Code

- [ ] Validation des entrées utilisateur
- [ ] Rate limiting activé
- [ ] CORS configuré correctement
- [ ] Headers de sécurité définis

### Infrastructure

- [ ] HTTPS/SSL activé
- [ ] Firewall configuré
- [ ] Backups réguliers activés
- [ ] Logs d'audit centralisés

### Monitoring

- [ ] Alertes pour erreurs
- [ ] Monitoring de l'uptime
- [ ] Logs d'authentification
- [ ] Dashboard de performance

---

## 📈 Performance - Optimisations

### Caching

```javascript
// Ajouter au src/index.js
const NodeCache = require('node-cache');
const cache = new NodeCache({ stdTTL: 300 }); // 5 min

async function fetchEmailsCached(limit) {
  const cacheKey = `emails_${limit}`;
  const cached = cache.get(cacheKey);
  
  if (cached) return cached;
  
  const emails = await gmailManager.fetchEmails(limit);
  cache.set(cacheKey, emails);
  
  return emails;
}
```

### Compression

```bash
# Dans package.json
"compression": "^1.7.4"

// Dans src/index.js
import compression from 'compression';
app.use(compression());
```

### Connection pooling

```javascript
// Pour les connexions DB
const pool = new Pool({
  max: 20,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
});
```

---

## 🔍 Monitoring et Alertes

### Outils recommandés

| Outil | Fonction | Coût |
|-------|----------|------|
| **Sentry** | Error tracking | $0-70/mois |
| **DataDog** | Full-stack monitoring | $15-100/mois |
| **New Relic** | Performance APM | $30-100/mois |
| **Uptime Robot** | Uptime monitoring | $0-50/mois |

### Setup Sentry

```bash
# Installer
npm install @sentry/node

# Dans src/index.js
import * as Sentry from "@sentry/node";

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  tracesSampleRate: 1.0,
});

// Capturer les erreurs automatiquement
app.use(Sentry.Handlers.errorHandler());
```

---

## 📊 Scaling pour haute charge

### Charge estimée

| Métrique | Valeur |
|----------|--------|
| Concurrent users | 1 user = 1 process |
| E-mails/jour | 1M = 100 requêtes API |
| Calendrier sync/jour | 1K = 50 requêtes API |

### Stratégies de scaling

**Vertically (Plus puissant) :**
- Augmenter la RAM : 512MB → 2GB
- Augmenter le CPU : 0.5vCPU → 2vCPU
- ⚡ Rapide, mais coûteux

**Horizontally (Plus de serveurs) :**
- Ajouter plusieurs instances
- Load balancer pour distribuer
- Redis pour session sharing
- ⚡ Meilleur pour haute charge

### Exemple avec Kubernetes

```yaml
# email-sync-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: email-sync
spec:
  replicas: 3  # 3 instances
  selector:
    matchLabels:
      app: email-sync
  template:
    metadata:
      labels:
        app: email-sync
    spec:
      containers:
      - name: email-sync
        image: email-sync:latest
        ports:
        - containerPort: 3000
        env:
        - name: REDIS_URL
          value: redis://redis-service:6379
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
```

---

## 🔄 Backup et Disaster Recovery

### Stratégie de backup

```bash
# Backup quotidien
0 2 * * * /scripts/backup-db.sh
0 3 * * * /scripts/backup-credentials.sh
```

### Restauration

```bash
# Restaurer depuis backup
./scripts/restore-db.sh backup_2026-02-23.tar.gz
```

### Plan de récupération

| Scénario | Temps de récupération |
|----------|----------------------|
| Perte de fichier | < 1 heure (restore backup) |
| Base de données corrompue | < 4 heures (restore + replay logs) |
| Perte complète du serveur | < 1 jour (nouveau serveur) |

---

## 📝 Checklist de déploiement

Avant de déployer en production :

- [ ] Tous les tests passent (`npm test`)
- [ ] Version bump dans package.json
- [ ] CHANGELOG.md à jour
- [ ] Variables d'environnement configurées
- [ ] Secrets sécurisés (pas en clair)
- [ ] SSL/HTTPS activé
- [ ] Firewall configuré
- [ ] Backups testés
- [ ] Monitoring en place
- [ ] Alertes configurées
- [ ] Documentation à jour
- [ ] Runbook créé (procédures d'urgence)
- [ ] Équipe formée à la maintenance

---

## 🎓 Exemples de déploiement

### Déploiement minimal (Gratuit)

```bash
# Sur votre machine
npm start
# URL locale : http://localhost:3000
```

### Déploiement léger ($5/mois - Render)

```bash
git push origin main
# Auto-deployed par Render
# URL : https://email-sync-mcp.onrender.com
```

### Déploiement production ($50/mois - AWS)

```bash
serverless deploy --stage prod
# Auto-scaling, haute disponibilité
# URL : https://api.yourdomain.com/sync
```

---

## 📞 Support et incidents

### Procédure d'incident

1. **Détection** (Sentry/Uptime Robot)
2. **Alerte** (Slack/Email)
3. **Investigation** (Logs + Monitoring)
4. **Mitigation** (Rollback ou Fix)
5. **Débriefing** (Post-mortem)

### Contacts escalade

```
Niveau 1 : Alert → Vérifier Sentry/Logs
Niveau 2 : Pas résolu → Redémarrer le serveur
Niveau 3 : Toujours pas → Rollback version précédente
Niveau 4 : Critique → Activer équipe on-call
```

---

## 🎯 Prochaines étapes

1. ✅ Configuration OAuth
2. ✅ MCP Integration
3. ⏭️ **Choisir architecture** (Local/Render/Docker/AWS)
4. ⏭️ **Configurer monitoring**
5. ⏭️ **Lancer en production**

---

**Dernière mise à jour :** Février 2026  
**Mainteneur :** Claude Code Team  
**Support :** GitHub Issues / Discord
