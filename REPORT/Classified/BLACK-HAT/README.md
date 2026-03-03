# ⚫ BLACK-HAT — TTP Simulation & Advanced Red Team

> **USAGE STRICTEMENT INTERNE — WHITELIST ONLY.**
> Toute tentative sur une cible hors `ATTACK_WHITELIST` est bloquée automatiquement (erreur 403). Ces opérations simulent des TTPs (Tactics, Techniques, Procedures) d'acteurs malveillants réels dans un environnement contrôlé à des fins éducatives et de red team avancé.

---

## 1. Définition

Le Black-Hat (usage simulé) représente les **émulations d'acteurs de menace** : reproduction fidèle des TTPs documentés dans le framework MITRE ATT&CK pour entraîner les équipes de défense, tester les capacités de détection SIEM/EDR, et valider les playbooks de réponse à incident.

**Ce n'est PAS du hacking malveillant** — c'est de la simulation contrôlée dans un lab isolé.

Cas d'usage légitimes :
- Entraînement Red Team / Purple Team
- Test de détection SIEM (alertes manquées → amélioration des règles)
- Validation des playbooks SOC (temps de réponse, escalade)
- Exercices CTF internes

---

## 2. Cadre légal & Contraintes techniques

| Contrainte | Valeur |
|------------|--------|
| **Cibles autorisées** | `th3-kali`, `th3-gemini`, `th3-streamlit` uniquement |
| **Cibles interdites** | Tout ce qui n'est pas dans `ATTACK_WHITELIST` → 403 immédiat |
| **Réseau** | Docker-internal uniquement — pas de trafic externe en Black Hat |
| **Tor** | Non utilisé (réseau interne). Tor requis si simulation d'exfiltration externe. |
| **Loi applicable** | Canada CC §342.1 — autorisation explicite du propriétaire du lab |
| **Enregistrement** | Chaque TTP doit être taggé avec son ID MITRE ATT&CK |
| **Cleanup** | Suppression obligatoire de tous les artefacts après l'opération |

---

## 3. Outils utilisés & TTPs simulés

| Script | TTPs MITRE | Outils |
|--------|-----------|--------|
| `ttp_simulation.py` | T1595, T1046, T1110, T1083 | nmap, masscan, hydra, gobuster |
| `full_exploit_chain.py` | T1595→T1046→T1110→T1078→T1083→T1041 | Chaîne complète recon→exploit→post-ex→cleanup |

### Mapping MITRE ATT&CK

| TTP ID | Nom | Simulation |
|--------|-----|-----------|
| **T1595** | Active Scanning | nmap `-sV -sC` sur la cible |
| **T1046** | Network Service Discovery | masscan top-1000 ports |
| **T1110** | Brute Force | hydra SSH/HTTP (5 tentatives max) |
| **T1083** | File and Directory Discovery | gobuster sur services web détectés |
| **T1078** | Valid Accounts | Test avec credentials communs |
| **T1041** | Exfiltration Over C2 Channel | Simulation log uniquement (pas de vraie exfil) |

---

## 4. Meilleures pratiques

1. **Whitelist stricte** : `full_exploit_chain.py` vérifie `ATTACK_WHITELIST` avant chaque action. La liste ne peut être modifiée qu'en éditant `vault_report_writer.py` directement — pas d'override CLI.
2. **Tagging MITRE obligatoire** : chaque phase de l'opération est annotée avec l'ID TTP correspondant dans `03_exploitation.md`.
3. **Rate limiting inchangeable** : hydra est limité à 5 tentatives/service + délai 2 s. Ne pas modifier ces valeurs même en lab.
4. **Purple Team** : idéalement, une équipe défensive monitore le SIEM pendant l'opération pour mesurer le temps de détection.
5. **Cleanup documenté** : `06_validation.md` doit lister chaque artefact déposé ET confirmer sa suppression.
6. **Isolation réseau** : les simulations Black Hat ne doivent jamais sortir du réseau Docker. Vérifier les règles iptables avant de commencer.
7. **Débriefing** : après chaque simulation, organiser un debriefing avec l'équipe défensive pour analyser ce qui a été détecté / manqué.

---

## 5. Résultats attendus

| Fichier | Contenu |
|---------|---------|
| `00_metadata.md` | Cible, TTPs simulés, routing interne, autorisation |
| `01_recon.md` | Résultats de la phase T1595 + T1046 |
| `02_vulnerabilities.md` | Surfaces exploitées (T1110 + T1083) |
| `03_exploitation.md` | **Chaque TTP taggé** avec ID MITRE, vecteur, résultat |
| `04_analysis.md` | Analyse gap détection (SIEM aurait-il vu ça ?) |
| `05_countermeasures.md` | Règles de détection proposées (Sigma rules, etc.) |
| `06_validation.md` | Confirmation cleanup + rapport purple team |

---

## 6. Commandes de lancement

```bash
# Depuis C:/Users/th3th/th3-thirty3/hexstrike-ai/

# Simulation TTP séquentielle (T1595 → T1046 → T1110 → T1083)
python scripts/hat_attack_runner.py --hat black --mode ttp_simulation --target th3-kali

# Chaîne complète recon → exploit → post-ex → cleanup
python scripts/hat_attack_runner.py --hat black --mode full_exploit_chain --target th3-gemini

# Test de blocage (doit retourner erreur 403)
python scripts/hat_attack_runner.py --hat black --mode ttp_simulation --target th3-redis
# → Expected: "Target 'th3-redis' is in the protected-containers blocklist."

# Simulation avec job ID pour corrélation SIEM
python scripts/hat_attack_runner.py --hat black --mode ttp_simulation --target th3-kali --job-id rt-2026-007
```

---

## 7. Navigation

- [[INDEX]] — Registre de toutes les opérations Black Hat
- [[../../_BRAIN/PROTOCOLES_VAULT]] — Commandes globales HexStrike
- [[../RED-HAT/README]] — Pentest offensif standard
- [[../../LEARNING/HACKERGPT/HEXSTRIKE]] — Documentation hexstrike-ai
