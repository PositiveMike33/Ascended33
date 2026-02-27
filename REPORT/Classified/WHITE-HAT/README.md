# ⚪ WHITE-HAT — Defensive Audits & Compliance

> **Opérations défensives.** Ce dossier contient les audits de conformité, évaluations de vulnérabilités passives, et rapports de hardening produits par HexStrike en mode Blue Team.

---

## 1. Définition

Le chapeau blanc représente les **opérations de sécurité défensive** : audits de conformité (CIS, ISO 27001), évaluation des vulnérabilités sans exploitation active, et génération de recommandations de durcissement. L'objectif est d'améliorer la posture de sécurité sans causer d'interruption de service.

Différence clé : contrairement au Red Hat, le White Hat **n'exploite jamais** les vulnérabilités — il les identifie et propose des remèdes.

---

## 2. Cadre légal

| Exigence | Détail |
|----------|--------|
| **Autorisation** | Propriétaire du système ou responsable IT/CISO |
| **Mode** | Passif / safe-mode uniquement (pas de payloads actifs) |
| **Loi applicable** | Canada : LPRPDE / RGPD (données personnelles) |
| **Rapport** | Document confidentiel remis uniquement au commanditaire |
| **Divulgation** | Responsible disclosure si CVE public détecté |

---

## 3. Outils utilisés

| Script | Outils | Objectif |
|--------|--------|----------|
| `compliance_audit.py` | docker-bench-security, kube-bench, checkov, trivy | Conformité CIS + scan IaC/conteneurs |
| `vuln_assessment.py` | nuclei (safe), nikto, nmap --script vuln | Évaluation de vulnérabilités sans exploitation |
| `hardening_report.py` | commandes système (iptables, sshd, services) | Vérification de la configuration de sécurité |

---

## 4. Meilleures pratiques

1. **Mode safe uniquement** : tous les outils fonctionnent en mode "check" ou "assess" — jamais en mode "exploit" ou "attack".
2. **Aucun impact sur la production** : les scans doivent avoir un footprint minimal. Préférer les heures creuses.
3. **Rapport confidentiel** : les rapports White Hat contiennent des informations sensibles sur les failles — ne pas partager hors du circuit commanditaire + CISO.
4. **Responsible disclosure** : si un CVE 0-day est découvert, appliquer le processus de disclosure responsable (90 jours vendor → public).
5. **Validation de baseline** : chaque audit génère une baseline de sécurité. Re-auditer après 90 jours pour mesurer la progression.
6. **Trivy + checkov** : scanner les images Docker et les fichiers IaC (Terraform, Ansible) avant tout déploiement.

---

## 5. Résultats attendus

| Fichier | Contenu |
|---------|---------|
| `00_metadata.md` | Contexte, systèmes audités, fenêtre temporelle |
| `01_recon.md` | Inventaire des services, versions, configurations |
| `02_vulnerabilities.md` | CVEs trouvés, score CVSS, criticité |
| `03_exploitation.md` | *N/A pour White Hat* — vecteurs théoriques documentés |
| `04_analysis.md` | Analyse de conformité CIS, gaps identifiés |
| `05_countermeasures.md` | Recommandations priorisées (Critical/High/Medium/Low) |
| `06_validation.md` | Re-audit après application des recommandations |

---

## 6. Commandes de lancement

```bash
# Depuis C:/Users/th3th/th3-thirty3/hexstrike-ai/

# Audit de conformité Docker + Kubernetes + IaC
python scripts/hat_attack_runner.py --hat white --mode compliance_audit --target th3-hexstrike

# Évaluation de vulnérabilités (mode passif)
python scripts/hat_attack_runner.py --hat white --mode vuln_assessment --target th3-gemini

# Rapport de hardening (vérification config système)
python scripts/hat_attack_runner.py --hat white --mode hardening_report --target th3-kali

# Audit complet sur tous les conteneurs whitelistés
for target in th3-kali th3-gemini th3-streamlit; do
  python scripts/hat_attack_runner.py --hat white --mode compliance_audit --target $target
done
```

---

## 7. Navigation

- [[INDEX]] — Registre de toutes les opérations White Hat
- [[../../_BRAIN/PROTOCOLES_VAULT]] — Commandes globales HexStrike
- [[../RED-HAT/README]] — Contrepart offensive (red team)
