# 🚀 DÉMARRAGE RAPIDE - Test Suite HexStrike

## 📌 Fichiers de Test Créés

```
_INFRASTRUCTURE/
├── TEST_SUITE_WINDOWS.ps1          ← PowerShell (Windows)
├── TEST_SUITE_LINUX.sh             ← Bash (Linux/Mac)
├── test_orchestrator.py            ← Python (Multiplateforme - Recommandé)
├── RUN_TESTS.bat                   ← Launcher Windows
├── run-tests.sh                    ← Launcher Linux/Mac
├── TEST_SUITE_README.md            ← Documentation complète
└── test-results/                   ← Dossier des résultats
    ├── test-2025-02-25_*.log       ← Logs
    └── test-2025-02-25_*.json      ← Résultats JSON (Python)
```

---

## ⚡ Démarrage en 30 Secondes

### **🪟 Windows**

**Option 1 : Double-clic (le plus simple)**
```
Double-cliquez sur : _INFRASTRUCTURE\RUN_TESTS.bat
→ Menu interactif s'ouvre
→ Choisir option [1] ou [2]
```

**Option 2 : PowerShell (si Python installé)**
```powershell
cd _INFRASTRUCTURE
python test_orchestrator.py
```

**Option 3 : PowerShell direct**
```powershell
cd _INFRASTRUCTURE
..\RUN_TESTS.bat
```

---

### **🐧 Linux/Mac**

**Option 1 : Launcher interactif**
```bash
chmod +x _INFRASTRUCTURE/run-tests.sh
./_INFRASTRUCTURE/run-tests.sh
```

**Option 2 : Python (Recommandé)**
```bash
python3 _INFRASTRUCTURE/test_orchestrator.py
```

**Option 3 : Bash direct**
```bash
bash _INFRASTRUCTURE/TEST_SUITE_LINUX.sh
```

---

## 📊 Résultats Attendus

### **Succès (✓)**
```
✓ SUCCÈS: Container th3-hexstrike is RUNNING
✓ SUCCÈS: HexStrike Health Check
✓ SUCCÈS: Vault Volume Mounted at D:\Vault\Vault
✓ SUCCÈS: HexStrike API (8001) Responding
```

### **Avertissement (⚠)**
```
⚠ ATTENTION: Redis not reachable (optional)
⚠ ATTENTION: Pieces OS (39300) not accessible yet
```

### **Échec (✗)**
```
✗ ÉCHEC: Container th3-tor is STOPPED
✗ ÉCHEC: Vault Volume INACCESSIBLE at D:\Vault\Vault
```

---

## 🎯 What Each Phase Tests

| Phase | Test | Expected Result |
|-------|------|-----------------|
| 1️⃣ **Infrastructure** | Conteneurs UP | th3-hexstrike, th3-tor, th3-kali... |
| 2️⃣ **Connexions** | HexStrike health | `{"status": "healthy"}` |
| 3️⃣ **Volumes** | Vault accessible | Fichiers lisibles/écrivables |
| 4️⃣ **APIs** | Tous les endpoints | HTTP 200 OK |
| 5️⃣ **Tor** | SOCKS5 proxy | `{"isTor": true}` |
| 6️⃣ **Logging** | Logs disponibles | Dernières 20 lignes |
| 7️⃣ **Intégrations** | Pieces OS + MCP | Endpoints responding |

---

## 🔧 If a Test Fails

### **Exemple: "Container th3-hexstrike is STOPPED"**

```bash
# 1. Vérifier le status
docker ps -a | grep th3-hexstrike

# 2. Vérifier les logs
docker logs th3-hexstrike | tail -50

# 3. Redémarrer
docker-compose -f docker-compose-v2.yml restart th3-hexstrike

# 4. Ou rebuild + restart
docker-compose -f docker-compose-v2.yml up -d --build th3-hexstrike

# 5. Relancer les tests
python3 _INFRASTRUCTURE/test_orchestrator.py
```

---

## 📈 Success Rate Interpretation

| Rate | Status | Action |
|------|--------|--------|
| **90-100%** | ✓ Excellent | Production-ready |
| **70-90%** | ⚠ Good | Some optional services down |
| **50-70%** | ✗ Poor | Major issues - check logs |
| **< 50%** | ✗ Critical | Rebuild needed |

---

## 📂 Output Locations

### **PowerShell**
```
_INFRASTRUCTURE/test-results/test-2025-02-25_144530.log
```

### **Bash**
```
_INFRASTRUCTURE/test-results/test-2025-02-25_144530.log
```

### **Python (JSON - Recommended)**
```
_INFRASTRUCTURE/test-results/test-2025-02-25_144530.json

# Voir le taux de réussite
cat _INFRASTRUCTURE/test-results/test-*.json | grep success_rate
```

---

## 🎮 Interactive Menu (Launcher)

```
[1] Python - Full featured (recommended)    ← Complète + JSON
[2] PowerShell - Windows native             ← Windows seulement
[3] Docker PS - Quick check                 ← Container status
[4] Docker Logs - View logs                 ← Logs detaillés
[5] System Cleanup - Clean resources        ← Docker prune
[6] Exit
```

---

## ⚙️ Common Commands

```bash
# Voir tous les conteneurs
docker ps -a

# Voir les logs en temps réel
docker logs -f th3-hexstrike

# Vérifier le réseau
docker network inspect ascended33-network

# Vérifier les ports
docker port th3-hexstrike

# Redémarrer tous les services
docker-compose -f docker-compose-v2.yml restart

# Voir l'utilisation disque
docker system df

# Nettoyer les ressources orphelines
docker system prune -a --volumes
```

---

## 📝 Fichiers Importants

| Fichier | Purpose |
|---------|---------|
| `docker-compose-v2.yml` | Configuration complète des services |
| `TEST_SUITE_README.md` | Documentation détaillée |
| `test-results/*.json` | Résultats structurés (Python) |
| `test-results/*.log` | Logs texte (PowerShell/Bash) |

---

## 🆘 Support

**Les tests échouent?**

1. **Vérifier Docker est running**
   ```bash
   docker ps
   ```

2. **Vérifier les logs des services**
   ```bash
   docker logs th3-hexstrike | grep -i error
   docker logs th3-tor | grep -i error
   ```

3. **Redémarrer les services**
   ```bash
   docker-compose down
   docker-compose up -d
   sleep 30
   python3 test_orchestrator.py
   ```

4. **Cleanup et rebuild complet**
   ```bash
   docker system prune -a --volumes
   docker-compose build
   docker-compose up -d
   python3 test_orchestrator.py
   ```

---

## 📚 Documentation

- **Complète**: `TEST_SUITE_README.md` (9.4 KB)
- **JSON Format**: `test-results/test-*.json`
- **Docker Logs**: `docker logs <container>`
- **Network**: `docker network inspect ascended33-network`

---

## ✨ Tips & Tricks

### **Exécution automatique au démarrage**

**Windows (Task Scheduler)**
```
Tâche: Run Tests
Programme: python _INFRASTRUCTURE\test_orchestrator.py
Fréquence: Au démarrage
```

**Linux (cron)**
```bash
# Chaque jour à 6h
0 6 * * * python3 ~/projects/HexStrike/_INFRASTRUCTURE/test_orchestrator.py
```

### **Monitoring continu**

```bash
# Loop tests toutes les 5 minutes
watch -n 300 'python3 _INFRASTRUCTURE/test_orchestrator.py'
```

### **Export JSON vers fichier**

```bash
# Python output to file
python3 test_orchestrator.py > test-results/last-run.json 2>&1

# Afficher le résumé
cat test-results/last-run.json | grep -A 5 summary
```

---

## 🎯 Next Steps

**Après les tests :**

1. ✓ Tous les tests passent → Ready for deployment
2. ⚠ Quelques avertissements → Vérifier les services optionnels
3. ✗ Échecs → Vérifier `TEST_SUITE_README.md` section Troubleshooting

---

**Version**: 1.0  
**Last Updated**: 2025-02-25  
**Support**: See TEST_SUITE_README.md for full documentation
