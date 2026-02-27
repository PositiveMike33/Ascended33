# 🔴 RED-HAT — Offensive Penetration Testing

> **Authorization mandatory.** Every operation in this folder targets a system explicitly listed in `ATTACK_WHITELIST` or covered by a signed scope-of-work document.

---

## 1. Définition

Le chapeau rouge représente les **tests d'intrusion offensifs** : simulation d'un attaquant réel dans le but d'identifier et d'exploiter des vulnérabilités avant qu'un adversaire ne le fasse. Le Red Team agit sans restrictions (sauf celles du scope) et documente chaque vecteur utilisé.

Différence clé : contrairement au Gray Hat, le Red Hat **exploite activement** les failles ; il ne se contente pas de les identifier.

---

## 2. Cadre légal

| Exigence | Détail |
|----------|--------|
| **Autorisation écrite** | Scope-of-work signé OU cible dans `ATTACK_WHITELIST` |
| **Scope défini** | IPs/hostnames, ports, fenêtre temporelle |
| **Loi applicable** | Canada : CC §342.1 / US : CFAA 18 U.S.C. §1030 |
| **Responsabilité** | L'opérateur HexStrike assume la responsabilité légale si scope débordé |
| **Cibles interdites** | Tout ce qui est dans `PROTECTED_CONTAINERS` → rejet 403 automatique |

---

## 3. Outils utilisés

| Script | Outils | Objectif |
|--------|--------|----------|
| `network_pentest.py` | nmap, masscan, nuclei, metasploit | Découverte réseau + exploitation |
| `web_pentest.py` | ffuf, nuclei, sqlmap, dalfox | Attaque applicative web |
| `password_attack.py` | hydra, hashcat, john | Attaque par force brute + cracking |

---

## 4. Meilleures pratiques (OPSEC Red Team)

1. **Vérifier la whitelist** avant chaque lancement — `is_authorized_target(target)` retourne `(True, "authorized")` obligatoirement.
2. **Rate limiting** : `password_attack.py` est plafonné à 5 tentatives/service + délai 2 s entre chaque tentative. Ne jamais lever cette limite en production.
3. **Tor pour les cibles externes** : toute cible hors du réseau Docker interne doit transiter par `th3-tor` (SOCKS5 `127.0.0.1:9050`). Le runner vérifie automatiquement.
4. **Documenter chaque étape** : l'output brut de chaque outil est préservé dans `raw/`. Ne jamais supprimer ces fichiers avant validation (06_validation.md signé).
5. **Cleanup obligatoire** : supprimer shells, cron jobs, ou fichiers déposés après chaque engagement. Documenter le cleanup dans `06_validation.md`.
6. **Chain of custody** : l'horodatage UTC est automatique ; ne pas modifier manuellement `00_metadata.md`.

---

## 5. Résultats attendus

Chaque opération génère un dossier `YYYY-MM-DD_HH-MM_<type>_<cible>/` avec :

| Fichier | Contenu |
|---------|---------|
| `00_metadata.md` | Contexte, scope, chapeau, routing, job ID |
| `01_recon.md` | Ports ouverts, services, OS, bannières |
| `02_vulnerabilities.md` | CVEs avec score CVSS, composants affectés |
| `03_exploitation.md` | Vecteurs utilisés, succès/échec, proof-of-concept |
| `04_analysis.md` | Cause racine, timeline, pourquoi ça fonctionne |
| `05_countermeasures.md` | Mesures défensives, règles iptables, patches |
| `06_validation.md` | Re-test post-remediation, verdict final |
| `raw/*.txt` | Output brut de chaque outil |

---

## 6. Commandes de lancement

```bash
# Depuis C:/Users/th3th/th3-thirty3/hexstrike-ai/

# Pentest réseau complet (nmap + masscan + nuclei + metasploit)
python scripts/hat_attack_runner.py --hat red --mode network_pentest --target th3-kali

# Pentest web (ffuf + nuclei + sqlmap + dalfox)
python scripts/hat_attack_runner.py --hat red --mode web_pentest --target th3-kali

# Attaque password (hydra + hashcat + john)
python scripts/hat_attack_runner.py --hat red --mode password_attack --target th3-kali

# Avec options avancées
python scripts/hat_attack_runner.py --hat red --mode network_pentest --target th3-gemini --job-id op-2026-001
```

---

## 7. Navigation

- [[INDEX]] — Registre de toutes les opérations Red Hat
- [[../../_BRAIN/PROTOCOLES_VAULT]] — Commandes globales HexStrike
- [[../WHITE-HAT/README]] — Contrepart défensive (blue team)
