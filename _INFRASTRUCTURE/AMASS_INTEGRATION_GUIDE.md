# 🔍 AMASS Integration Guide for HexStrike

**Status**: ✅ Configured & Ready  
**Date**: 2025-02-25  
**Version**: 1.0

---

## 📋 Vue d'ensemble

AMASS est un outil puissant de reconnaissance OSINT (Open Source Intelligence) qui découvre les sous-domaines, adresses IP et autres informations sur vos cibles.

**Fonctionnalités principales:**
- ✓ Énumération DNS complète
- ✓ Recherche de certificats (CT Logs)
- ✓ Brute force de sous-domaines
- ✓ Requêtes API multiples sources
- ✓ Reconnaissance active (facultatif)
- ✓ Intégration Tor anonyme
- ✓ Export multiformats (JSON, CSV, HTML)

---

## 🚀 Démarrage Rapide

### **Configuration Simple**

```yaml
# Dans amass_config.yaml:
scope:
  domains:
    - target.com
    - example.com
  include_subdomains: true
  ports: [80, 443, 8080, 8443]
```

### **Lancer AMASS via HexStrike**

```python
python3 _INFRASTRUCTURE/amass_orchestrator.py \
  --domains target.com example.com \
  --brute-force \
  --output-dir /vault/REPORT/Classified/amass
```

### **Avec Tor (Anonyme)**

```python
python3 _INFRASTRUCTURE/amass_orchestrator.py \
  --domains target.com \
  --tor-proxy socks5://th3-tor:9050 \
  --brute-force
```

---

## ⚙️ Configuration Détaillée

### **1. Fichier de Configuration**

**Emplacement**: `_INFRASTRUCTURE/amass_config.yaml`

#### **Domaines à Scanner**
```yaml
scope:
  domains:
    - monentreprise.com
    - api.monentreprise.com
    - staging.monentreprise.com
  
  # Inclure les sous-domaines
  include_subdomains: true
  
  # Ports à vérifier
  ports:
    - 80
    - 443
    - 8080
    - 8443
    - 3000
    - 5000
```

#### **Résolveurs DNS**
```yaml
dns:
  resolvers:
    - 8.8.8.8           # Google
    - 8.8.4.4           # Google  
    - 1.1.1.1           # Cloudflare
    - 1.0.0.1           # Cloudflare
    - 9.9.9.9           # Quad9
    - 208.67.222.123    # OpenDNS
```

#### **Brute Force**
```yaml
brute_force:
  enabled: true
  wordlist: /usr/share/amass/wordlists/subdomains-top1million-5000.txt
  max_workers: 100
  recursive: true
```

#### **Sources de Données**
```yaml
sources:
  enabled:
    - certdb          # Certificate database
    - crtsh           # CT search
    - censys          # Censys
    - baidu           # Baidu
    - bing            # Bing
    - google          # Google
    - shodan          # Shodan
    - virustotal      # VirusTotal
    - threatcrowd     # ThreatCrowd
```

---

## 🔧 Utilisation Avancée

### **Option 1: Configuration Fichier YAML**

```bash
# Éditer la configuration
nano _INFRASTRUCTURE/amass_config.yaml

# Lancer avec la config
python3 _INFRASTRUCTURE/amass_orchestrator.py --config amass_config.yaml
```

### **Option 2: Paramètres CLI**

```bash
# Énumération simple
python3 _INFRASTRUCTURE/amass_orchestrator.py \
  --domains example.com \
  --output-dir /vault/REPORT/amass

# Énumération complète (brute force + Tor)
python3 _INFRASTRUCTURE/amass_orchestrator.py \
  --domains example.com target.com \
  --brute-force \
  --tor-proxy socks5://th3-tor:9050 \
  --output-dir /vault/REPORT/Classified/amass \
  --verbose
```

### **Option 3: Via HexStrike Tools**

Dans la GUI HexStrike Tools:

```
1. Select Tool: AMASS
2. Configuration: {
     "domains": ["example.com"],
     "brute_force": true,
     "output_dir": "/vault/REPORT/amass"
   }
3. Click "Launch Task"
```

---

## 📊 Résultats et Sorties

### **Format de Sortie**

Les résultats sont générés dans:
```
/vault/REPORT/Classified/amass/
├── example.com_subdomains.txt     ← Liste brute
├── amass_results_*.json           ← Résultats structurés
├── amass_report_*.md              ← Rapport markdown
└── amass.log                      ← Logs
```

### **Exemple de Résultat JSON**

```json
{
  "timestamp": "2025-02-25T14:45:30.123456",
  "total_domains": 1,
  "domains": [
    {
      "domain": "example.com",
      "status": "success",
      "subdomains_found": 42,
      "subdomains": [
        "www.example.com",
        "api.example.com",
        "mail.example.com",
        "staging.example.com",
        ...
      ],
      "output_file": "/vault/REPORT/amass/example.com_subdomains.txt"
    }
  ]
}
```

### **Rapport Markdown Généré**

```markdown
# AMASS Reconnaissance Report

**Generated**: 2025-02-25T14:45:30.123456

## Domain: example.com
**Status**: success
**Subdomains Found**: 42

- www.example.com
- api.example.com
- mail.example.com
- staging.example.com
- dev.example.com
...

--- 

## Domain: target.com
**Status**: success
...
```

---

## 🌐 Intégration Tor (Anonymité)

### **Configurer Tor dans AMASS**

```yaml
# amass_config.yaml
integration:
  tor_enabled: true
  tor_socks5: socks5://th3-tor:9050
  tor_proxy: http://th3-tor:8118
```

### **Lancer avec Tor**

```bash
python3 _INFRASTRUCTURE/amass_orchestrator.py \
  --domains target.com \
  --tor-proxy socks5://th3-tor:9050
```

**Vérifier que Tor fonctionne:**

```bash
# Vérifier si on est derrière Tor
curl -s --socks5 th3-tor:9050 https://check.torproject.org/api/ip
# Devrait retourner: {"isTor": true, "ip": "..."}
```

---

## 🔐 Clés API (Optionnel)

Pour utiliser les sources payantes/premium:

```yaml
# amass_config.yaml
sources:
  credentials:
    # Shodan
    shodan_key: "YOUR_SHODAN_API_KEY"
    
    # VirusTotal
    virustotal_key: "YOUR_VT_API_KEY"
    
    # PassiveTotal
    passivetotal_user: "YOUR_PT_USER"
    passivetotal_key: "YOUR_PT_KEY"
    
    # WhoisXML
    whoisxml_key: "YOUR_WHOISXML_KEY"
```

**Obtenir les clés:**
- Shodan: https://shodan.io/account/profile
- VirusTotal: https://www.virustotal.com/gui/home/upload
- PassiveTotal: https://www.passivetotal.org
- WhoisXML: https://www.whoisxmlapi.com

---

## 📈 Cas d'Usage

### **1. Audit Interne**

```bash
python3 _INFRASTRUCTURE/amass_orchestrator.py \
  --domains monentreprise.com \
  --brute-force \
  --output-dir /vault/REPORT/Classified/amass
```

**Résultats**: Liste complète des sous-domaines découverts en ligne.

### **2. Reconnaissance Complète (Brute Force + Sources)**

```bash
python3 _INFRASTRUCTURE/amass_orchestrator.py \
  --domains target.com target-cdn.com \
  --brute-force \
  --verbose \
  --output-dir /vault/REPORT/amass
```

**Résultats**: 
- Tous les sous-domaines publics
- Adresses IP
- Certificats SSL
- Informations MX

### **3. Scan Anonyme via Tor**

```bash
python3 _INFRASTRUCTURE/amass_orchestrator.py \
  --domains sensitive-target.com \
  --tor-proxy socks5://th3-tor:9050 \
  --brute-force \
  --output-dir /vault/REPORT/Classified/amass
```

**Protection**: Tout routé via Tor, IP masquée.

### **4. Reconnaissance Passive (Sans Brute Force)**

```python
config = AmassConfig(
  domains=["example.com"],
  brute_force=False,
  output_dir="/vault/REPORT/amass"
)
```

**Durée**: Plus rapide, données publiques uniquement.

---

## ⚡ Commandes Rapides

```bash
# Scan simple
amass enum -d example.com

# Avec brute force
amass enum -d example.com -brute -w /path/to/wordlist.txt

# Avec résolveurs DNS personnalisés
amass enum -d example.com -r 8.8.8.8,1.1.1.1,9.9.9.9

# Avec proxy Tor
amass enum -d example.com -proxy socks5://th3-tor:9050

# Verbose
amass enum -d example.com -v

# JSON output
amass enum -d example.com -o results.json

# Complet
amass enum -d example.com \
  -brute \
  -r 8.8.8.8,1.1.1.1 \
  -proxy socks5://th3-tor:9050 \
  -o /vault/REPORT/amass_results.json \
  -v
```

---

## 🔍 Vérifier les Résultats

```bash
# Voir les sous-domaines trouvés
cat /vault/REPORT/Classified/amass/example.com_subdomains.txt

# Nombre de sous-domaines
wc -l /vault/REPORT/Classified/amass/example.com_subdomains.txt

# Résultats JSON
cat /vault/REPORT/Classified/amass/amass_results_*.json | jq '.domains[0].subdomains_found'

# Rapport markdown
cat /vault/REPORT/Classified/amass/amass_report_*.md
```

---

## 📊 Intégration HexStrike

### **Dans HexStrike Tools GUI**

```
Available Tools: [amass ▼]

AMASS Configuration:
{
  "custom": "parameters"
}

Options:
- Priority: Normal
- Cache to Obsidian: ✓
- Send notification when complete: ☐

[Launch Task]
```

### **Résultats dans Vault**

```
/vault/REPORT/Classified/amass/
├── 2025-02-25_amass_results.json
├── 2025-02-25_amass_report.md
├── example.com_subdomains.txt
└── target.com_subdomains.txt
```

---

## 🚨 Limitations & Considérations

### **Performance**
- ⚠️ Le brute force peut prendre 10-30 minutes
- ⚠️ Peut générer beaucoup de trafic DNS
- ⚠️ Certaines sources ont des limites de requêtes

### **Légalité**
- ✓ La reconnaissance passive est légale
- ⚠️ Le brute force peut être détecté
- ⚠️ Vérifier les règles légales de votre juridiction
- ⚠️ Avoir l'autorisation du propriétaire du domaine

### **Faux Positifs**
- Les sous-domaines trouvés peuvent être:
  - Inactifs
  - Arrêtés
  - Mal configurés
  - De tiers (CDN, etc.)

---

## 📚 Ressources

- **AMASS GitHub**: https://github.com/OWASP/Amass
- **Documentation AMASS**: https://owasp.org/www-project-amass/
- **Tutoriels**: https://www.youtube.com/results?search_query=amass+tutorial
- **Wordlists**: https://github.com/OWASP/Amass/releases

---

## 🛠️ Dépannage

### **"amass: command not found"**
```bash
# Installer AMASS
apt-get install amass        # Linux
brew install amass           # macOS
docker run owasp/amass       # Docker
```

### **"Proxy connection failed"**
```bash
# Vérifier que Tor tourne
docker ps | grep th3-tor

# Vérifier la connectivité
curl -s --socks5 th3-tor:9050 https://check.torproject.org/api/ip
```

### **"No subdomains found"**
- Vérifier la cible est publique
- Vérifier les résolveurs DNS
- Essayer sans Tor d'abord
- Augmenter le timeout

---

## 📝 Fichiers

| Fichier | Description |
|---------|-------------|
| `amass_config.yaml` | Configuration complète (9.4 KB) |
| `amass_orchestrator.py` | Script orchestration (12.8 KB) |
| `AMASS_INTEGRATION_GUIDE.md` | Ce guide |

---

## ✅ Checklist de Configuration

- [ ] Lire ce guide
- [ ] Éditer `amass_config.yaml`
- [ ] Définir les domaines cibles
- [ ] Activer/désactiver brute force
- [ ] (Optionnel) Ajouter clés API
- [ ] (Optionnel) Configurer Tor
- [ ] Tester avec: `python3 amass_orchestrator.py --domains example.com`
- [ ] Vérifier les résultats dans `/vault/REPORT/Classified/amass/`

---

**Version**: 1.0  
**Status**: ✅ Ready to use  
**Last Updated**: 2025-02-25
