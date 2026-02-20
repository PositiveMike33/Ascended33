# Méthodologie OSINT — HexStrike

> *OSINT = Open Source Intelligence — renseignement à partir de sources publiques uniquement.*
> *Aucune authentification. Aucune intrusion. Aucune violation de la vie privée.*

---

## Cadre Légal Rappel

Avant toute investigation OSINT ciblée sur une personne ou organisation :
- **OSINT passif sur données publiques** = légal
- **OSINT ciblé sur individu** sans mandat ou autorisation = zone grise selon le contexte
- **Social engineering actif** = illégal sans autorisation
- Voir [[Cadre Legal — Quebec Canada]] pour le détail complet

---

## Les 5 Phases OSINT

### Phase 1 — Définition de la Cible et du Scope

**Avant de commencer, documenter :**
- Qui/quoi est la cible (organisation, domaine, personne publique)
- Quel est l'objectif (surface d'attaque, réputation, infrastructure)
- Quelles sont les limites légales applicables
- Qui a demandé l'investigation et avec quelle autorisation

**Livrables :** Brief d'engagement signé, note dans `HexStrike/Engagements/`

---

### Phase 2 — Collecte Passive (Reconnaissance)

Collecte de données sans interaction directe avec la cible.

#### Sous-domaines et Infrastructure
```
# theHarvester — emails, sous-domaines, IPs
theHarvester -d target.com -b google,bing,linkedin

# Subfinder — énumération de sous-domaines
subfinder -d target.com -o subdomains.txt

# WHOIS — propriétaire du domaine
whois target.com

# DNSdumpster — cartographie DNS
# Via interface web : dnsdumpster.com
```

#### Métadonnées et Contenus Publics
```
# Google Dorks (recherche avancée)
site:target.com filetype:pdf
site:target.com inurl:admin
site:target.com "confidentiel" OR "internal"
"@target.com" site:linkedin.com
target.com ext:xlsx OR ext:docx

# Shodan — appareils connectés exposés
# Via interface web ou API : shodan.io
# Recherche : org:"Nom de l'organisation"

# Wayback Machine — pages archivées
# Via interface web : web.archive.org
```

#### Réseaux Sociaux et Présence en Ligne
```
# Sherlock — username across platforms
sherlock username_cible

# Maltego CE — cartographie de relations
# Interface graphique — voir documentation Maltego

# LinkedIn, Twitter/X, GitHub public
# SpiderFoot HX — automatisation multi-sources
spiderfoot -t target.com -m sfp_whois,sfp_dnsresolve
```

---

### Phase 3 — Analyse et Corrélation

**Organiser les données :**
1. Cartographier l'infrastructure (domaines, IPs, ASN)
2. Identifier les technologies utilisées (Wappalyzer, BuiltWith)
3. Lister les employés/contacts identifiés (sources publiques)
4. Identifier les fuites potentielles (Have I Been Pwned pour emails)
5. Corréler les informations entre sources

**Niveau de confiance :** Attribuer A/B/C à chaque information
- A = Confirmé par sources multiples
- B = Source unique fiable
- C = Non confirmé, à vérifier

---

### Phase 4 — Rapport OSINT

Utiliser le template [[Templates/TPL — Rapport OSINT]].

**Structure minimale :**
1. Résumé exécutif (non-technique)
2. Méthodologie utilisée
3. Surface d'attaque identifiée
4. Fuites et expositions
5. Recommandations prioritaires
6. Annexes techniques

---

### Phase 5 — Livraison et Clôture

- Présentation au client (oral + rapport écrit)
- Suppression des données collectées (selon accord)
- Archive du rapport dans `HexStrike/Engagements/[nom-client]/`
- Bilan THIRTY3 de l'engagement

---

## Outils OSINT par Catégorie

Voir [[Outils OSINT — Arsenal]] pour la liste complète avec installation et usage.

---

## Checklist OSINT Rapide

```
PRE-ENGAGEMENT
[ ] Autorisation vérifiée (si cible organisationnelle)
[ ] Scope défini et documenté
[ ] Note dans Engagements/ créée

COLLECTE
[ ] WHOIS + DNS
[ ] Sous-domaines (theHarvester, Subfinder)
[ ] Google Dorks
[ ] Shodan (si infrastructure)
[ ] Réseaux sociaux (si pertinent)
[ ] Fuites d'emails (HIBP)
[ ] Métadonnées documents publics
[ ] Wayback Machine

ANALYSE
[ ] Cartographie infrastructure
[ ] Corrélation des données
[ ] Niveau de confiance attribué
[ ] Risques identifiés et priorisés

RAPPORT
[ ] Template complété
[ ] Résumé exécutif rédigé
[ ] Recommandations priorisées
[ ] Sources documentées
[ ] Relecture et validation
```

---

*Méthodologie HexStrike — Légalement alignée avec le [[Cadre Legal — Quebec Canada]]*
