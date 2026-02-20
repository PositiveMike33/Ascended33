# Outils OSINT — Arsenal HexStrike

> Tous les outils listés ici sont open source et légaux à utiliser pour l'OSINT passif.
> L'utilisation sur des cibles sans autorisation peut être illégale — voir [[Cadre Legal — Quebec Canada]].

---

## Infrastructure et Reconnaissance Réseau

### theHarvester
**Usage :** Collecte d'emails, sous-domaines, IPs, URLs depuis les moteurs de recherche publics.
```bash
# Installation
pip3 install theHarvester

# Usage de base
theHarvester -d target.com -b google,bing,linkedin,shodan -l 500

# Exporter les résultats
theHarvester -d target.com -b all -f rapport_output
```
**Sources disponibles :** Google, Bing, LinkedIn, Yahoo, Hunter, DuckDuckGo, Shodan

---

### Subfinder
**Usage :** Énumération passive de sous-domaines via sources publiques.
```bash
# Installation
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest

# Usage
subfinder -d target.com -o subdomains.txt

# Avec toutes les sources
subfinder -d target.com -all -recursive
```

---

### WHOIS / dig / nslookup
**Usage :** Informations d'enregistrement de domaine, DNS.
```bash
# WHOIS
whois target.com
whois 8.8.8.8

# DNS lookup
dig target.com ANY
dig +short MX target.com
nslookup target.com

# Reverse DNS
dig -x IP_ADDRESS
```

---

### DNSdumpster
**Usage :** Cartographie DNS complète (interface web).
- URL : [dnsdumpster.com](https://dnsdumpster.com)
- Fournit : sous-domaines, serveurs MX, NS, enregistrements A
- Exporte en format Excel

---

## Moteurs de Recherche Spécialisés

### Shodan
**Usage :** Découverte d'appareils connectés exposés (serveurs, caméras, IoT, etc.).
```
# Recherches Shodan (interface web ou API)
org:"Nom Organisation"
ssl.cert.subject.CN:"target.com"
hostname:"target.com"
net:192.168.1.0/24
port:22 country:CA
```
- Compte gratuit : 50 résultats par recherche
- API Python : `pip install shodan`

---

### Censys
**Usage :** Similaire à Shodan — scan de l'internet public.
- URL : [search.censys.io](https://search.censys.io)
- Gratuit pour la recherche de base

---

### OSINT Framework
**Usage :** Répertoire organisé de tous les outils OSINT par catégorie.
- URL : [osintframework.com](https://osintframework.com)
- Référence pour trouver l'outil adapté à chaque type de cible

---

## Réseaux Sociaux et Identité

### Sherlock
**Usage :** Recherche de username sur 300+ plateformes simultanément.
```bash
# Installation
pip3 install sherlock-project

# Usage
sherlock username_cible

# Sortie dans fichier
sherlock username_cible --output results.txt
```

---

### Maltego Community Edition
**Usage :** Cartographie visuelle de relations entre entités (personnes, organisations, domaines, IPs).
- Téléchargement : [maltego.com](https://www.maltego.com/downloads/)
- Gratuit en version Community (limité à 12 entités par graphe)
- Transforms disponibles : WHOIS, DNS, réseaux sociaux, Shodan

**Guide de démarrage :**
1. Créer un compte Maltego
2. Lancer un "New Graph"
3. Glisser un "Domain" depuis la palette
4. Clic droit → "Run Transforms" → "All Transforms"

---

### SpiderFoot HX
**Usage :** Automatisation OSINT multi-sources avec interface web.
```bash
# Installation
pip3 install spiderfoot

# Lancer l'interface web
spiderfoot -l 127.0.0.1:5001

# Accéder via navigateur : http://127.0.0.1:5001
```

---

## Fuites et Données Compromises

### Have I Been Pwned (HIBP)
**Usage :** Vérifier si des emails d'une organisation ont été compromis dans des fuites connues.
- URL : [haveibeenpwned.com](https://haveibeenpwned.com)
- API disponible pour recherches en masse (payante)
```bash
# Via curl (email unique)
curl https://haveibeenpwned.com/api/v3/breachedaccount/email@target.com \
  -H "hibp-api-key: VOTRE_CLE"
```

---

## Analyse de Métadonnées

### ExifTool
**Usage :** Extraction de métadonnées depuis des images, PDFs, documents.
```bash
# Installation (Linux)
apt install exiftool

# Analyser un fichier
exiftool document.pdf
exiftool image.jpg

# Extraire toutes les métadonnées en JSON
exiftool -json image.jpg
```

**Ce qu'on peut trouver :** Auteur du document, logiciel utilisé, GPS de la photo, date de création, nom d'utilisateur, chemin réseau interne.

---

## Archives Web

### Wayback Machine
**Usage :** Accéder à des versions archivées de sites web.
- URL : [web.archive.org](https://web.archive.org)
```bash
# API Wayback Machine
curl "http://archive.org/wayback/available?url=target.com"

# Lister toutes les captures disponibles
curl "http://web.archive.org/cdx/search/cdx?url=target.com/*&output=text&limit=50"
```

---

## Google Dorks — Cheatsheet

```
# Fichiers exposés
site:target.com filetype:pdf OR filetype:xlsx OR filetype:docx
site:target.com ext:sql OR ext:log OR ext:env

# Panneaux d'administration
site:target.com inurl:admin OR inurl:login OR inurl:dashboard
site:target.com intitle:"admin panel" OR intitle:"login"

# Informations sensibles
site:target.com "confidentiel" OR "internal use only" OR "ne pas diffuser"
site:target.com "mot de passe" OR "password" OR "credentials"

# Technologies et frameworks
site:target.com inurl:wp-admin
site:target.com inurl:.php?id=
site:target.com "powered by"

# Emails et contacts
"@target.com" site:linkedin.com
"@target.com" filetype:pdf
```

---

## Setup Recommandé HexStrike OSINT

**Environnement :** Kali Linux (VM isolée) ou Ubuntu + outils
**VPN :** Toujours actif pendant les recherches OSINT actives
**Navigateur :** Firefox avec uBlock Origin + aucune connexion à des comptes personnels

```bash
# Installation groupée des outils essentiels
pip3 install theHarvester sherlock-project spiderfoot
apt install exiftool whois dnsutils
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
```

---

*Arsenal HexStrike — Open Source, Légal, Efficace*
