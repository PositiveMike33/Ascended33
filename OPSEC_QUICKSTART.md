# OPSEC Quick Start — Ascended33 Complete Security Setup

**Bienvenue dans le système OPSEC complet d'Ascended33!**

Ce guide montre comment démarrer une session de test de sécurité complètement anonyme avec:
- ✅ VPN + fallback automatique (NordVPN → Mullvad → ProtonVPN)
- ✅ Tor toujours actif (container Docker th3-tor)
- ✅ Isolation de sécurité (container Kali)
- ✅ Auto-logging dans la Vault Obsidian
- ✅ Nettoyage automatique des traces

---

## 📋 Pré-requis

Avant de commencer, assurez-vous que vous avez:

1. **Docker & Docker Compose** installés
   ```bash
   docker --version
   docker-compose --version
   ```

2. **Un client VPN installé** (au moins un):
   ```bash
   # NordVPN (recommandé)
   nordvpn status
   
   # OU Mullvad
   mullvad status
   
   # OU ProtonVPN
   which protonvpn
   ```

3. **Python 3.11+**
   ```bash
   python3 --version
   ```

4. **Obsidian avec le plugin REST API** activé
   - Settings → Local REST API → Activer
   - Copier l'API key

---

## 🚀 Démarrage Rapide (5 minutes)

### Étape 1: Démarrer une session OPSEC sécurisée

```bash
# Rendre le script exécutable
chmod +x launch-opsec-session.sh

# Lancer une session OSINT
./launch-opsec-session.sh "OSINT Investigation" "self" "osint"
```

**Sortie attendue:**
```
[1/4] Starting Docker containers (th3-kali + th3-tor)...
✓ Containers started

[2/4] Verifying Tor connectivity...
✓ Tor online

[3/4] Checking VPN protection...
✓ NordVPN active

[4/4] Initializing OPSEC manager and logging to Vault...
✓ Operation logged to Vault

╔════════════════════════════════════════════════════════════════════╗
║  ✓ OPSEC INITIALIZED SAFELY                                       ║
╚════════════════════════════════════════════════════════════════════╝

✓ Session ready for operations.
```

### Étape 2: Accéder au container Kali

```bash
docker exec -it th3-kali bash
```

Vous êtes maintenant dans une environment complètement anonyme:
- ✓ Trafic via VPN
- ✓ Sortie via Tor
- ✓ IP masquée (45.88.190.23)
- ✓ Session loggée dans la Vault

### Étape 3: Vérifier votre anonymat

```bash
# À l'intérieur th3-kali:

# Vérifier IP directe
curl https://httpbin.org/ip

# Vérifier via Tor
curl -x socks5://th3-tor:9050 https://check.torproject.org

# Test DNS (ne doit pas révéler votre IP réelle)
nslookup google.com
```

### Étape 4: Exécuter vos outils de sécurité

```bash
# À l'intérieur th3-kali - tous vos outils favoris:

# Reconnaissance
nmap -sV target.com
amass enum -d target.com

# Web scanning
nuclei -t vulnerability-checks -u https://target.com

# OSINT
whois target.com
dig target.com

# Tor-routed requests
curl -x socks5://th3-tor:9050 https://onion-site.onion
```

### Étape 5: Quitter et nettoyer

```bash
# Quitter le container Kali
exit

# Nettoyer les traces (important!)
python3 scripts/opsec/trace_cleaner.py --scope full

# Arrêter les containers
docker-compose -f docker-compose-opsec.yml down
```

---

## 📊 Vérifier vos Logs dans la Vault

Tous vos opérations sont auto-loggées à:
```
D:\Vault\Security\Operations\2026-02-19\
├── 20260219_150330-OSINT-Investigation.md
├── 20260219_151045-Pentesting-Session.md
└── 20260219_152100-Dark-Web-Monitoring.md
```

Chaque log contient:
- ✓ Timestamp de début
- ✓ Statut OPSEC (VPN/Tor/IP)
- ✓ Findings découverts
- ✓ Timeline d'exécution
- ✓ Statut final

---

## 🔧 Workflows Courants

### Workflow 1: OSINT Investigation

```bash
./launch-opsec-session.sh "OSINT - Target Investigation" "self" "osint"
docker exec -it th3-kali bash

# Inside th3-kali:
python3 /opt/scripts/osint/domain_recon.py --target self
python3 /opt/scripts/osint/breach_check.py --email your@email.com
python3 /opt/scripts/osint/social_footprint.py --username username

exit
python3 scripts/opsec/trace_cleaner.py --scope full
```

### Workflow 2: Penetration Testing

```bash
./launch-opsec-session.sh "Pentesting - Self Lab" "self" "pentest"
docker exec -it th3-kali bash

# Inside th3-kali:
nmap -sV -p- 192.168.1.1
nuclei -t cves -u http://target
sqlmap -u "http://target?id=1" --dbs

exit
python3 scripts/opsec/trace_cleaner.py --scope full
```

### Workflow 3: Dark Web Monitoring

```bash
./launch-opsec-session.sh "Dark Web Threat Intel" "self" "threat_intel"
docker exec -it th3-kali bash

# Inside th3-kali:
# All requests automatically routed through Tor

curl -x socks5://th3-tor:9050 http://search7g5l43xy.onion
# (Tor search engine)

exit
python3 scripts/opsec/trace_cleaner.py --scope full
```

---

## 🛡️ Checklist de Sécurité

Avant chaque opération sensible, vérifiez:

- [ ] VPN actif → `nordvpn status` ou `mullvad status`
- [ ] Tor actif → `docker ps | grep th3-tor`
- [ ] IP masquée → `curl https://httpbin.org/ip`
- [ ] Pas de compte personnel loggé
- [ ] Domaine d'application: `self` (self-testing)
- [ ] Opération loggée dans Vault

---

## 🚨 Troubleshooting

### "Tor won't start"
```bash
docker logs th3-tor
docker-compose -f docker-compose-opsec.yml restart th3-tor
```

### "VPN connection failed"
```bash
# Vérifier le statut
nordvpn status

# Redémarrer NordVPN
nordvpn disconnect
nordvpn connect

# Essayer Mullvad (fallback)
mullvad connect
```

### "Docker command not found"
```bash
# Vérifier que Docker daemon tourne
sudo systemctl start docker
docker ps
```

### "Port 9050 already in use"
```bash
# Port Tor SOCKS5 déjà pris
lsof -i :9050
kill -9 <PID>
```

---

## 📚 Documentation Complète

Pour plus de détails, consultez:
- `OPSEC_GUIDE.md` — Guide complet du système OPSEC
- `OPSEC_EXAMPLES.py` — Exemples d'intégration
- `config/config.yaml` — Configuration des paramètres OPSEC
- `scripts/opsec/` — Code source des modules

---

## 🔐 Philosophie de Sécurité

Le système Ascended33 OPSEC repose sur:

1. **Defense in Depth** — Plusieurs couches (VPN + Tor)
2. **Automation** — Tout est auto-orchestré (pas d'ajustement manuel)
3. **Audit Trail** — Tout est loggé pour l'accountability
4. **Cleanup** — Les traces sont automatiquement nettoyées
5. **Self-Testing Only** — Cible toujours `self` (pas de cibles non-autorisées)

---

## 🎯 Prochaines Étapes

1. **Lancer votre première session**
   ```bash
   ./launch-opsec-session.sh "First Test" "self" "osint"
   ```

2. **Consulter les logs dans la Vault**
   - Ouvrir Obsidian
   - Aller à `Security/Operations/2026-02-19/`

3. **Intégrer avec hexstrike-ai** (optionnel)
   - Démarrer sur la même machine
   - Accessible à `localhost:8888` depuis th3-kali

---

**Bienvenue dans le monde de Ascended33 — La sécurité complètement automatisée.**

*Version 2.0 — Février 2026*
