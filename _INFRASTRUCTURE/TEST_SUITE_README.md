# 🧪 HexStrike Ascended33 - Test Suite Automatisée

Orchestration, validation et troubleshooting complet de tous les conteneurs Docker, connexions réseau et APIs.

---

## 📋 Vue d'ensemble

Cette suite de tests automatisée valide **7 phases** de votre infrastructure HexStrike :

1. **PHASE 1** - Vérification Infrastructure Docker
2. **PHASE 2** - Tests de Connexion Interne
3. **PHASE 3** - Tests Applicatifs (Volumes, REPORT)
4. **PHASE 4** - Tests API Externes (tous les endpoints)
5. **PHASE 5** - Tests Tor & Anonymité
6. **PHASE 6** - Tests Persistance & Logging
7. **PHASE 7** - Tests Intégration Pieces OS & MCP

---

## 🚀 Démarrage Rapide

### **Option 1 : Python (Recommandé - Multiplateforme)**

```bash
# Windows (PowerShell)
python .\_INFRASTRUCTURE\test_orchestrator.py

# Linux/Mac
python3 ./_INFRASTRUCTURE/test_orchestrator.py

# Ou avec make (si disponible)
make test
```

**Avantages:**
- ✓ Multiplateforme (Windows/Mac/Linux)
- ✓ Sorties en JSON + console
- ✓ Gestion élégante des erreurs
- ✓ Timeouts configurables

---

### **Option 2 : PowerShell (Windows Only)**

```powershell
# Terminal PowerShell (Admin recommandé)
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
.\_INFRASTRUCTURE\TEST_SUITE_WINDOWS.ps1

# Ou avec options
.\_INFRASTRUCTURE\TEST_SUITE_WINDOWS.ps1 -Verbose
.\_INFRASTRUCTURE\TEST_SUITE_WINDOWS.ps1 -SkipCleanup
```

**Avantages:**
- ✓ Interface native Windows
- ✓ Logs colorisés
- ✓ Gestion des chemins Windows

---

### **Option 3 : Bash (Linux/Mac)**

```bash
# Rendre le script exécutable
chmod +x ./_INFRASTRUCTURE/TEST_SUITE_LINUX.sh

# Exécuter
./_INFRASTRUCTURE/TEST_SUITE_LINUX.sh

# Avec variables d'environnement
VAULT_PATH=/mnt/vault ./_INFRASTRUCTURE/TEST_SUITE_LINUX.sh
```

**Avantages:**
- ✓ Léger et rapide
- ✓ Pas de dépendances externes
- ✓ Compatible avec tous les shells Unix

---

## 📊 Phases de Test Détaillées

### **PHASE 1 - Vérification Infrastructure Docker**

Vérifie que tous les conteneurs sont UP et accessibles.

```bash
# Manuellement
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# Conteneurs attendus
th3-hexstrike     ✓ UP
th3-tor           ✓ UP
th3-kali          ✓ UP
th3-hackergpt     ✓ UP
th3-streamlit     ✓ UP
```

---

### **PHASE 2 - Tests de Connexion Interne**

Valide les connexions inter-conteneurs sur le réseau Docker.

```bash
# 2.1 - HexStrike Health
curl -s http://localhost:8001/health | python3 -m json.tool
# Attendu: {"status": "healthy", "version": "..."}

# 2.2 - Redis depuis HexStrike
docker exec th3-hexstrike redis-cli -h redis ping
# Attendu: PONG

# 2.3 - Réseau ascended33-network
docker network inspect ascended33-network
```

---

### **PHASE 3 - Tests Applicatifs**

Teste les volumes montés et la structure des rapports.

```bash
# 3.1 - Volume Vault accessible
ls -la "D:\Vault\Vault" (Windows)
ls -la "/mnt/vault" (Linux/Mac)

# 3.2 - Écriture dans Vault
echo "test" > "D:\Vault\Vault\test.txt"

# 3.3 - Structure REPORT
ls -la "D:\Vault\Vault\REPORT\Classified"
```

---

### **PHASE 4 - Tests API Externes**

Teste tous les endpoints HTTP des services.

```bash
PORT    SERVICE                 ENDPOINT
----    -------                 --------
8001    HexStrike AI           /health
8000    HackerGPT              /health
8501    Streamlit Dashboard    /_stcore/health
5000    Kali Labs              /health
8002    Audit API              /health
8004    Vault Indexer          /health
8005    Report Generator       /health
```

---

### **PHASE 5 - Tests Tor & Anonymité**

Valide la configuration Tor SOCKS5.

```bash
# 5.1 - Test Tor SOCKS5 (9050)
curl -s --socks5 localhost:9050 https://check.torproject.org/api/ip
# Attendu: {"isTor": true, "ip": "..."}

# 5.2 - Tor Control Port (9051)
echo "GETINFO version" | nc localhost 9051
```

---

### **PHASE 6 - Tests Persistance & Logging**

Récupère les logs et vérifie les volumes.

```bash
# 6.1 - Logs HexStrike
docker logs th3-hexstrike | tail -20

# 6.2 - Logs Tor
docker logs th3-tor | tail -10

# 6.3 - Volumes Docker
docker volume ls
```

---

### **PHASE 7 - Tests Intégration Pieces OS & MCP**

Valide les intégrations externes.

```bash
ENDPOINT                    PORT    SERVICE
---------                   ----    -------
/health                     39300   Pieces OS
/health                     3123    Obsidian API
(MCP Script)                N/A     HexStrike MCP
```

---

## 📁 Résultats

Les résultats sont sauvegardés dans :

```
_INFRASTRUCTURE/test-results/
├── test-2025-02-25_144530.log     (PowerShell)
├── test-2025-02-25_144530.txt     (Bash)
└── test-2025-02-25_144530.json    (Python - Format complet)
```

### **Format JSON (Python)**

```json
{
  "timestamp": "2025-02-25T14:45:30.123456",
  "total_time_seconds": 15.47,
  "summary": {
    "total": 42,
    "success": 38,
    "failure": 2,
    "warning": 2,
    "success_rate_percent": 90.5
  },
  "tests": [
    {
      "name": "Container th3-hexstrike",
      "status": "SUCCESS",
      "message": "Is RUNNING",
      "duration_seconds": 0.12,
      "details": null
    }
  ]
}
```

---

## 🔧 Troubleshooting Guide

### **Si un test échoue :**

| Étape | Symptôme | Solution |
|-------|----------|----------|
| 1 | Conteneur absent | `docker compose up -d` |
| 2 | Connection refused | Vérifier que le conteneur est UP : `docker ps` |
| 3 | Timeout | Augmenter le timeout dans le script |
| 4 | API non accessible | Vérifier les port mappings : `docker port <container>` |
| 5 | Tor inaccessible | Vérifier `docker logs th3-tor` |
| 6 | Logs vides | Conteneur peut être neuf - `docker logs --since 5m <container>` |
| 7 | Volume non monté | Vérifier `docker inspect <container>` sous Mounts |

---

### **Diagnostics Rapides**

```bash
# Vérifier tous les conteneurs
docker ps -a

# Vérifier un conteneur spécifique
docker inspect th3-hexstrike

# Voir les logs en temps réel
docker logs -f th3-hexstrike

# Vérifier la connectivité réseau
docker network inspect ascended33-network

# Test port disponible
netstat -an | grep LISTEN

# Vérifier les volumes
docker volume inspect <volume-name>

# Nettoyer les ressources orphelines
docker system prune -a --volumes
```

---

## ⚙️ Options Avancées

### **Variables d'Environnement**

```bash
# Définir le chemin Vault
export VAULT_PATH=/custom/vault/path
python3 test_orchestrator.py

# Logging verbose
export DEBUG=1
./_INFRASTRUCTURE/TEST_SUITE_LINUX.sh
```

### **Redémarrer les Services**

```bash
# Restart all services
docker-compose -f docker-compose-v2.yml down
docker-compose -f docker-compose-v2.yml up -d

# Restart specific service
docker-compose restart th3-hexstrike

# Rebuild and restart
docker-compose up -d --build th3-hexstrike
```

### **Nettoyer Complètement**

```bash
# Remove all containers and volumes (⚠️ ATTENTION)
docker-compose down -v

# Clean system
docker system prune -a --volumes

# Remove specific volume
docker volume rm <volume-name>
```

---

## 🔐 Sécurité

- ✓ Aucune donnée sensible n'est loggée
- ✓ Les mots de passe/tokens ne sont jamais affichés
- ✓ Les tests ne modifient pas les configurations critiques
- ✓ Les fichiers de test sont nettoyés après exécution

---

## 📊 Interprétation des Résultats

### **Taux de Réussite**

- **90-100%** : Infrastructure saine ✓
- **70-90%** : Quelques services inactifs (optionnel?)
- **50-70%** : Problèmes majeurs - vérifier les logs
- **< 50%** : Infrastructure non prête - rebuild recommandé

### **Symboles**

```
✓  SUCCESS  - Test passé sans problème
✗  FAILURE  - Test échoué - action requise
⚠  WARNING  - Test passé mais comportement inattendu
ℹ  INFO     - Informations importantes
```

---

## 🎯 Cas d'Usage Courants

### **Setup Initial**

```bash
# 1. Build les images
docker-compose build

# 2. Lancer les services
docker-compose up -d

# 3. Attendre ~30s pour les health checks
sleep 30

# 4. Tester
python3 test_orchestrator.py
```

### **Vérification Avant Déploiement**

```bash
# 1. Exécuter la suite complète
python3 test_orchestrator.py

# 2. Vérifier le JSON
cat _INFRASTRUCTURE/test-results/test-*.json

# 3. Valider le taux de réussite > 90%
jq '.summary.success_rate_percent' _INFRASTRUCTURE/test-results/test-*.json
```

### **Debugging Rapide**

```bash
# 1. Tests uniquement
./_INFRASTRUCTURE/TEST_SUITE_LINUX.sh

# 2. Logs détaillés
docker logs th3-hexstrike | tail -50 | grep -i error

# 3. État du système
docker system df

# 4. Réseau
docker network inspect ascended33-network
```

---

## 📝 Logs

Les logs sont disponibles dans :

```bash
# PowerShell
_INFRASTRUCTURE/test-results/*.log

# Bash
_INFRASTRUCTURE/test-results/*.log

# Python (JSON complet)
_INFRASTRUCTURE/test-results/*.json
```

---

## 🤝 Support

Si une étape échoue :

1. **Vérifier les logs** : `docker logs <container>`
2. **Vérifier l'état** : `docker ps -a`
3. **Vérifier le réseau** : `docker network inspect ascended33-network`
4. **Redémarrer** : `docker-compose restart <service>`

---

## 📚 Ressources

- [Docker Documentation](https://docs.docker.com)
- [Docker Compose Reference](https://docs.docker.com/compose/reference/)
- [Tor Project](https://www.torproject.org)
- [HexStrike Docs](./HEXSTRIKE_TOR_SETUP_COMPLETE.md)

---

**Dernière mise à jour:** 2025-02-25  
**Version:** 1.0.0
