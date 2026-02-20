# Module 03 — Introduction OSINT

**Phase :** 1 — OSINT Passif
**Durée estimée :** 3–4 semaines
**Prérequis :** [[01 — Fondamentaux Reseaux TCP-IP]], [[02 — Linux pour la Securite]]

---

## OSINT — L'Art de la Visibilité

L'OSINT (Open Source Intelligence) consiste à collecter des informations depuis des sources publiques.

**La règle d'or :** Si tu as besoin d'un login pour accéder à l'information — ce n'est plus de l'OSINT passif.

**Ce module te donne la base pour :**
- Conduire une investigation OSINT éthique et légale
- Cartographier la surface d'attaque d'une organisation
- Produire un rapport OSINT professionnel

---

## Semaine 1 — Google Dorking

### Opérateurs Google Avancés

```
site:          Limiter à un domaine
               site:example.com

intitle:       Dans le titre de la page
               intitle:"index of"

inurl:         Dans l'URL
               inurl:admin

filetype:      Type de fichier
               filetype:pdf site:example.com

intext:        Dans le corps du texte
               intext:"mot de passe"

cache:         Version cachée
               cache:example.com

-              Exclure
               site:example.com -blog

"..."          Phrase exacte
               "confidentiel internal use only"
```

### Dorks Utiles à Pratiquer

```
# Trouver des fichiers sensibles
site:target.com filetype:pdf OR filetype:xlsx OR filetype:docx
site:target.com filetype:sql OR filetype:log OR filetype:env
site:target.com filetype:bak OR filetype:old

# Panneaux d'administration exposés
site:target.com inurl:admin
site:target.com inurl:login OR inurl:signin
intitle:"phpMyAdmin" site:target.com

# Informations sur l'organisation
"@target.com" site:linkedin.com
site:target.com "confidentiel" OR "internal"
site:github.com "target.com" "api_key" OR "password"
```

**Exercice :** Faire 10 recherches Google Dorks sur un domaine que tu contrôles (ton propre site, ou un domaine de test).

---

## Semaine 2 — Reconnaissance DNS et Infrastructure

### theHarvester — Collecte Automatisée

```bash
# Installation
pip3 install theHarvester

# Collecte de base (Google + Bing)
theHarvester -d target.com -b google,bing -l 500

# Toutes les sources disponibles
theHarvester -d target.com -b all -l 500

# Sauvegarder les résultats
theHarvester -d target.com -b all -f resultats_target

# Sources principales
# google, bing, linkedin, yahoo, duckduckgo
# hunter, shodan, censys, virustotal
```

### WHOIS et DNS

```bash
# WHOIS — propriétaire et dates
whois target.com
whois 192.168.1.1  # Reverse WHOIS sur IP

# DNS complet
dig target.com ANY
dig target.com A        # IPv4
dig target.com MX       # Email
dig target.com NS       # Serveurs de noms
dig target.com TXT      # SPF, DKIM, autres

# Énumération de sous-domaines
subfinder -d target.com -silent
subfinder -d target.com -all -recursive

# DNSdumpster (interface web)
# dnsdumpster.com — très complet, exporte en Excel
```

---

## Semaine 3 — Shodan et Infrastructure Exposée

### Shodan — Moteur de Recherche IoT

```
# Recherches Shodan (interface web : shodan.io)

# Par organisation
org:"Nom Organisation"
org:"Nom Organisation" port:22

# Par domaine
hostname:"target.com"
hostname:".target.com"

# Par technologie
ssl.cert.subject.CN:"target.com"
http.title:"Login"
http.html:"powered by WordPress"

# Infrastructures exposées
port:3306 country:CA  # MySQL exposé au Canada
port:22 org:"Nom Organisation"  # SSH
port:3389 country:CA  # RDP exposé

# API Shodan (Python)
pip install shodan
```

```python
import shodan

api = shodan.Shodan("VOTRE_CLE_API")
results = api.search("org:'Nom Organisation'")

for result in results['matches']:
    print(f"IP: {result['ip_str']}")
    print(f"Port: {result['port']}")
    print(f"Organisation: {result.get('org', 'N/A')}")
```

---

## Semaine 4 — Maltego et Rapport

### Maltego Community Edition

**Téléchargement :** [maltego.com/downloads](https://www.maltego.com/downloads/)

**Workflow de base :**
1. Créer un compte Maltego (gratuit)
2. "New Graph"
3. Glisser "Domain" depuis la palette d'entités
4. Taper `target.com`
5. Clic droit → Run Transforms → All Transforms
6. Observer le graphe se construire (sous-domaines, IPs, emails)
7. Explorer les entités trouvées avec de nouveaux transforms

**Entités utiles :**
- Domain → To DNS Names
- Domain → To Email Addresses
- Person → To Social Networks
- IP Address → To Organization

**Limite Community Edition :** 12 entités par graphe — travailler par couches.

### Rédiger le Rapport OSINT

Utiliser [[HexStrike/OSINT/Templates/TPL — Rapport OSINT|Template Rapport OSINT]].

**Exercice final de ce module :**
Faire une investigation OSINT complète sur ton propre nom / organisation personnelle :
1. Google Dorks
2. theHarvester
3. WHOIS + DNS
4. Shodan (si applicable)
5. Maltego
6. Rédiger un rapport complet avec le template

---

## Ressources

| Ressource | Lien | Gratuit |
|-----------|------|---------|
| OSINT Framework | osintframework.com | Oui |
| TryHackMe — Shodan.io | tryhackme.com | Oui |
| TryHackMe — Google Dorking | tryhackme.com | Oui |
| Maltego Documentation | docs.maltego.com | Oui |
| Bellingcat Guides OSINT | bellingcat.com | Oui |

---

## Checklist de Validation

- [ ] Je maîtrise 10 opérateurs Google avancés
- [ ] J'ai utilisé theHarvester sur un domaine test
- [ ] Je sais interpréter les résultats WHOIS et DNS
- [ ] J'ai fait une recherche Shodan sur une organisation
- [ ] J'ai créé et navigué un graphe Maltego
- [ ] J'ai produit un rapport OSINT complet avec le template HexStrike

**Quand toutes les cases sont cochées → Module 03 : Complété**

---

*Module 03 — Parcours HexStrike | Retour vers [[Parcours HexStrike]]*
