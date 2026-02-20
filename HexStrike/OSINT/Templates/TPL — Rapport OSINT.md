# Rapport OSINT — [NOM CLIENT]
**HexStrike | Confidentiel**

---

## En-tête du Rapport

| Champ | Valeur |
|-------|--------|
| **Client** | [Nom de l'organisation] |
| **Demandeur** | [Nom, titre] |
| **Date de début** | YYYY-MM-DD |
| **Date de fin** | YYYY-MM-DD |
| **Analyste** | Michael — HexStrike |
| **Classification** | CONFIDENTIEL — Réservé au client |
| **Version** | 1.0 |

---

## 1. Résumé Exécutif

*[2-3 paragraphes, langage non technique, lisible par un dirigeant.]*
*[Répondre à : Qu'est-ce qui a été trouvé ? Quel est le niveau de risque ? Que faut-il faire en premier ?]*

**Niveau de risque global :** FAIBLE / MOYEN / ÉLEVÉ / CRITIQUE

**Points critiques identifiés :**
- [Point 1]
- [Point 2]

**Recommandation prioritaire :**
> [Une phrase — l'action la plus urgente]

---

## 2. Périmètre de l'Investigation

### Cibles analysées
| Type | Identifiant | Inclus dans scope |
|------|-------------|-------------------|
| Domaine principal | example.com | Oui |
| Sous-domaines | *.example.com | Oui |
| Adresses IP | x.x.x.x/24 | Oui |
| Réseaux sociaux | @handle | Oui/Non |

### Hors scope (non analysé)
- [Éléments explicitement exclus]

### Méthodologie utilisée
- OSINT passif uniquement (aucune interaction directe avec les systèmes cibles)
- Sources : moteurs de recherche, WHOIS, DNS, Shodan, réseaux sociaux publics

---

## 3. Infrastructure Exposée

### Domaines et Sous-domaines
| Sous-domaine | IP | Service | Statut |
|-------------|-----|---------|--------|
| target.com | x.x.x.x | HTTPS | Actif |
| mail.target.com | x.x.x.x | SMTP | Actif |
| admin.target.com | x.x.x.x | HTTP | **Exposé** |

### Ports et Services Exposés (Shodan)
| IP | Port | Service | Version | Risque |
|----|------|---------|---------|--------|
| x.x.x.x | 22 | SSH | OpenSSH 7.4 | Moyen |
| x.x.x.x | 3306 | MySQL | 5.7 | Critique |

### Fournisseurs et Technologies Identifiés
- Hébergeur : [Cloudflare / OVH / AWS / etc.]
- CMS : [WordPress / Drupal / etc.]
- Frameworks : [React / Laravel / etc.]
- Email : [GSuite / Office365 / etc.]

---

## 4. Fuites et Données Exposées

### Emails Compromis (Have I Been Pwned)
| Email | Fuites identifiées | Données exposées |
|-------|-------------------|-----------------|
| user@target.com | LinkedIn 2021, Adobe 2013 | Email, mot de passe hashé |

### Documents Sensibles Trouvés
| Fichier | Source | Contenu sensible |
|---------|--------|-----------------|
| rapport-interne.pdf | Google | Noms d'employés, structure org |

### Informations sur les Employés (Sources Publiques)
| Nom | Poste | Source | Informations exposées |
|-----|-------|--------|----------------------|
| [Prénom Nom] | CTO | LinkedIn | Email professionnel, stack technique |

---

## 5. Analyse des Risques

### Matrice de Risques

| Risque identifié | Probabilité | Impact | Priorité |
|-----------------|-------------|--------|---------|
| [Description] | Faible/Moyen/Élevé | Faible/Moyen/Élevé | P1/P2/P3 |

### Scénarios d'Attaque Potentiels

**Scénario 1 — [Titre]**
> *[Description de comment un attaquant pourrait utiliser les informations trouvées]*
> *Probabilité : [Faible/Moyen/Élevé]*

**Scénario 2 — [Titre]**
> *[Description]*

---

## 6. Recommandations

### Priorité 1 — Actions Immédiates (< 48h)
- [ ] [Action spécifique] — *[Raison et impact]*
- [ ] [Action spécifique]

### Priorité 2 — Court Terme (< 30 jours)
- [ ] [Action spécifique]
- [ ] [Action spécifique]

### Priorité 3 — Long Terme (< 90 jours)
- [ ] [Action spécifique]

---

## 7. Annexes Techniques

### Annexe A — Commandes Exécutées
```bash
# Sous-domaines
theHarvester -d target.com -b google,bing -l 500

# DNS
dig target.com ANY
whois target.com

# Shodan (interface web)
org:"Nom Organisation"
```

### Annexe B — Sources de Données Consultées
| Source | Type | Date consultation |
|--------|------|------------------|
| Shodan | Infrastructure | YYYY-MM-DD |
| LinkedIn | Employés | YYYY-MM-DD |
| HIBP | Fuites | YYYY-MM-DD |
| WHOIS | Domaines | YYYY-MM-DD |

### Annexe C — Indicateurs Clés (IOCs)
```
Domaines identifiés :
- example.com
- sub.example.com

IPs identifiées :
- x.x.x.x
```

---

## Déclaration Légale

Ce rapport a été produit dans le cadre d'une investigation OSINT passive, basée exclusivement sur des données publiquement accessibles. Aucune intrusion, authentification non autorisée, ou interception de communications n'a été effectuée.

Ce rapport est confidentiel et destiné exclusivement au client nommé ci-dessus. Toute divulgation non autorisée est interdite.

**HexStrike opère conformément au Code criminel du Canada (art. 342.1) et à la Loi 25 du Québec.**

---

*Rapport généré par HexStrike | [Date] | Contact : [email]*
