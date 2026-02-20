# HexStrike — Base de Connaissances Vulnérabilités

Ce dossier centralise les notes sur les vulnérabilités étudiées, reproduites en lab, ou identifiées lors d'engagements.

## Catégories

Créer des notes avec le préfixe correspondant :

| Préfixe | Catégorie |
|---------|-----------|
| `WEB-` | Vulnérabilités web (XSS, SQLi, IDOR, etc.) |
| `INFRA-` | Infrastructure (services exposés, configs) |
| `CVE-` | CVEs spécifiques étudiés |
| `MALWARE-` | Samples analysés en RE |
| `TECHNIQUE-` | Techniques d'attaque documentées |

## Format d'une Note de Vulnérabilité

```markdown
# [CATÉGORIE-XXX] — Nom de la Vulnérabilité

**Type :** XSS / SQLi / IDOR / SSRF / etc.
**CVSS :** X.X
**CVE :** CVE-XXXX-XXXXX (si applicable)
**Étudié le :** YYYY-MM-DD
**Source :** Lab HTB / Bug Bounty / CVE / Engagement

## Description
[Explication technique de la vulnérabilité]

## Conditions d'Exploitation
[Quand et comment cette vulnérabilité est exploitable]

## Payload / PoC
[Exemple de code ou commande — contexte lab uniquement]

## Détection (Blue Team)
[Comment détecter cette attaque dans les logs]

## Remédiation
[Comment corriger]

## Références
[Links vers CVE, OWASP, writeups]
```

## Ressources Vulnérabilités

- **NVD (National Vulnerability Database)** : [nvd.nist.gov](https://nvd.nist.gov)
- **OWASP** : [owasp.org](https://owasp.org)
- **Exploit-DB** : [exploit-db.com](https://www.exploit-db.com)
- **CVE Details** : [cvedetails.com](https://www.cvedetails.com)
- **Rapid7 Vulndb** : [vulndb.cyberark.com](https://vulndb.cyberark.com)
