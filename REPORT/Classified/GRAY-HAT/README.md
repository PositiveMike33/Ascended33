# 🩶 GRAY-HAT — OSINT, Bug Bounty & Passive Reconnaissance

> **Reconnaissance passive.** Ce dossier contient les opérations OSINT, les reconnaissances pour bug bounty, et les analyses passives de la surface d'attaque externe.

---

## 1. Définition

Le chapeau gris représente les **opérations d'intelligence passive** : OSINT (Open Source Intelligence), bug bounty, et reconnaissance sans exploitation active. Ces opérations ciblent des informations **publiquement accessibles** ou dans le cadre d'un programme bug bounty avec scope défini.

Spectre Gray Hat :
- **OSINT pur** : sources publiques uniquement (DNS, WHOIS, Shodan, GitHub, LinkedIn)
- **Bug Bounty** : dans le scope défini par le programme (HackerOne, Bugcrowd, programme privé)
- **Recon passive** : pas d'envoi de payloads, pas d'exploitation, pas de DoS

---

## 2. Cadre légal

| Exigence | Détail |
|----------|--------|
| **OSINT** | Sources publiques uniquement — aucun accès non autorisé |
| **Bug Bounty** | Scope du programme obligatoire — out-of-scope interdit même si vulnérable |
| **Données personnelles** | RGPD/LPRPDE : minimisation des données, pas de stockage inutile |
| **Tor** | Obligatoire pour toutes cibles externes (protège l'identité de l'opérateur) |
| **Canada / US** | CFAA §1030 et CC §342.1 s'appliquent même à la reconnaissance passive |
| **Divulgation** | Bug Bounty : rapport via la plateforme officielle uniquement |

---

## 3. Outils utilisés

| Script | Outils | Objectif |
|--------|--------|----------|
| `osint_recon.py` | amass, subfinder, theharvester, shodan-cli, httpx | Énumération DNS + footprinting externe |
| `bug_bounty_recon.py` | /api/bugbounty/* (6 phases HexStrike) | Workflow complet bug bounty |

### Pipeline OSINT
```
amass (passive) → subfinder → theharvester → httpx → shodan
                                    ↓
                            Rapport GRAY-HAT/
```

---

## 4. Meilleures pratiques

1. **Tor obligatoire** : toutes les requêtes vers des cibles externes doivent passer par `th3-tor` (SOCKS5). Le runner vérifie la présence du proxy avant de lancer les outils.
2. **Sources passives uniquement** : amass et subfinder en mode `-passive`. Pas de brute-force DNS en OSINT pur.
3. **Minimisation des données** : ne collecter que ce qui est pertinent au scope. Pas de stockage de PII (emails personnels, numéros de téléphone) au-delà du nécessaire.
4. **Respect du scope bug bounty** : vérifier `scope.txt` avant chaque phase. Un subdomain hors scope ne doit jamais être testé même s'il apparaît dans les résultats.
5. **Rate limiting Shodan** : API key requise — respecter les limites de l'API (1 requête/seconde en plan gratuit).
6. **Documentation Shodan** : toujours inclure la requête exacte (`query`) dans le rapport pour reproductibilité.

---

## 5. Résultats attendus

| Fichier | Contenu |
|---------|---------|
| `00_metadata.md` | Cible, scope bug bounty, méthode Tor, timestamp |
| `01_recon.md` | Subdomains découverts, IPs, ports, services exposés |
| `02_vulnerabilities.md` | Findings passifs (configs exposées, buckets S3 ouverts, etc.) |
| `03_exploitation.md` | *N/A pour Gray Hat* — vecteurs documentés seulement |
| `04_analysis.md` | Surface d'attaque mappée, priorités pour pentest (si scope élargi) |
| `05_countermeasures.md` | Recommendations de réduction de surface |
| `06_validation.md` | Vérification post-fix (si bug bounty accepté) |

---

## 6. Commandes de lancement

```bash
# Depuis C:/Users/th3th/th3-thirty3/hexstrike-ai/

# OSINT complet sur un domaine externe (via Tor automatique)
python scripts/hat_attack_runner.py --hat gray --mode osint_recon --target example.com

# Cible de test officielle nmap (toujours valide)
python scripts/hat_attack_runner.py --hat gray --mode osint_recon --target scanme.nmap.org

# Workflow bug bounty complet (6 phases HexStrike)
python scripts/hat_attack_runner.py --hat gray --mode bug_bounty_recon --target bugbounty-target.com

# OSINT avec job ID pour tracking
python scripts/hat_attack_runner.py --hat gray --mode osint_recon --target target.com --job-id bb-2026-042
```

---

## 7. Navigation

- [[INDEX]] — Registre de toutes les opérations Gray Hat
- [[../../ENQUETES_OSINT/INDEX_OSINT]] — Hub OSINT centralisé
- [[../../_BRAIN/PROTOCOLES_VAULT]] — Commandes globales HexStrike
- [[../BLACK-HAT/README]] — Simulation TTP avancée
