---
date: 2026-02-19
type: learning-progress
phase: [2]
tags: [learning, phase-2, development, security, hacking]
status: active
source: REPORT/Février
---

## Contexte
#19-02-2026  #Context_Précédent 
Michael demande une analyse réaliste et minutieuse du projet Ascended33 dans les meilleures pratiques de cybersécurité, avec un compte-rendu étape par étape de ce qui manque et ce qui doit absolument être fait pour contribuer à des projets cybersécurité de manière professionnelle.

---

## État Réel du Projet (2026-02-19)

### Ce qui EXISTE et FONCTIONNE

|Module|Fichier|Lignes|Statut|
|---|---|---|---|
|Dashboard Streamlit|streamlit_app.py|506|✅ Complet|
|Client hexstrike-ai|mcp/hexstrike_client.py|124|✅ Complet|
|Client SSH Kali|mcp/kali_ssh_client.py|189|✅ Complet|
|Registre d'outils|mcp/tool_registry.py|213|✅ Complet|
|Vérification OPSEC|scripts/opsec/vpn_check.py|94|✅ Partiel|
|Reconnaissance DNS|scripts/osint/domain_recon.py|393|✅ Complet|
|Vérif. fuites|scripts/osint/breach_check.py|289|✅ Complet|
|Empreinte sociale|scripts/osint/social_footprint.py|280|✅ Complet|
|Dark Web Monitor|scripts/osint/dark_web_monitor.py|290|✅ Complet|
|Générateur rapports|scripts/reporting/report_generator.py|131|✅ Complet|
|Client Obsidian|vault_sync/vault_api.py|140|✅ Complet|
|Constructeur notes|vault_sync/note_builder.py|212|✅ Complet|
|Sync Vault|vault_sync/sync.py|273|✅ Complet|
|Vérif. connexions|verify_connections.py|161|✅ Complet|
|Templates rapports|templates/ (4 fichiers)|338|✅ Complet|
|Launcher Windows|setup.ps1 / .bat / .ps1|260|✅ Complet|

### Ce qui MANQUE

|Module|Fichier prévu|Priorité|
|---|---|---|
|Recon active|scripts/recon/network_scan.py|HAUTE|
|Recon web|scripts/recon/web_enum.py|HAUTE|
|Scan vulnérabilités|scripts/recon/vuln_scan.py|HAUTE|
|Nettoyage traces|scripts/opsec/trace_cleaner.py|HAUTE|
|Protection PII|scripts/opsec/identity_guard.py|CRITIQUE|
|Formatter rapports|scripts/reporting/formatter.py|MOYENNE|
|Sync Vault writer|scripts/reporting/vault_writer.py|MOYENNE|
|Registre outils|mcp/tool_registry.py|✅ Déjà fait|
|Tests unitaires|tests/ (directory entier)|CRITIQUE|
|Documentation API|—|MOYENNE|

---

## PROBLÈMES DE SÉCURITÉ IDENTIFIÉS (par ordre de criticité)

### 🔴 CRITIQUE — Action immédiate requise

**P1 — Secrets dans l'historique Git**

- `config/config.yaml` contient: clé API Obsidian (64 chars), IP Kali (192.168.157.128), chemin SSH (C:/Users/th3th/.ssh/kali_lab_key), username `th3th`
- **Le fichier est gitignored MAINTENANT mais a possiblement été commité avant**
- Risque: Si jamais poussé sur un remote public, tous ces credentials sont compromis
- **Action**: Vérifier `git log --all -- config/config.yaml`, si trouvé: rotation immédiate de TOUTES les credentials

**P2 — Pas de module identity_guard.py**

- CLAUDE.md §7.4 stipule: "Run scripts/opsec/identity_guard.py before committing to detect PII leaks"
- Ce module N'EXISTE PAS — la protection PII pré-commit est donc absente
- **Action**: Créer ce module en priorité absolue

**P3 — Pas de git hook pre-commit**

- Aucun hook pre-commit qui vérifie les secrets avant de commiter
- Aucun outil type `detect-secrets`, `gitleaks`, ou `trufflehog` configuré
- **Action**: Installer un hook pre-commit pour détecter les secrets

### 🟠 HAUTE — À traiter dans les 48h

**P4 — OPSEC check incomplet dans vpn_check.py**

- Logique actuelle: vérifie si VPN actif via l'IP publique courante
- Faiblesse: Compare seulement à httpbin.org, pas à une IP de référence connue
- Possible faux positif: Si VPN est down mais IP publique a changé, check peut passer
- **Action**: Stocker l'IP "de base" (sans VPN) dans config, comparer à chaque run

**P5 — paramiko AutoAddPolicy pour SSH Kali**

- `kali_ssh_client.py` utilise `AutoAddPolicy()` (accepte toute clé d'hôte)
- Vulnérabilité MITM si le réseau est compromis
- **Action**: Utiliser `RejectPolicy` + stocker fingerprint Kali dans config

**P6 — Pas de rate limiting dans les modules OSINT**

- Requêtes illimitées vers: crt.sh, Wayback Machine, ipinfo.io, GitHub
- Risk: IP bannée par ces services
- **Action**: Ajouter backoff exponentiel + respect des rate limits APIs

### 🟡 MOYENNE — À traiter sous 2 semaines

**P7 — SHA-1 dans breach_check.py (k-anonymity)**

- Ligne 185: `hashlib.sha1(password.encode()).hexdigest()` — SHA-1 déprécié
- Mitigé par la nature de k-anonymity (seul le préfixe est envoyé)
- **Note**: HIBP API exige spécifiquement SHA-1 pour la compatibilité — donc impossible à changer

**P8 — Pas de validation des réponses API**

- Les réponses JSON des APIs externes ne sont pas validées (Pydantic ou schema check)
- Données malformées pourraient causer des erreurs non gérées
- **Action**: Ajouter validation de schema basique

**P9 — Gestion des erreurs trop large**

- Plusieurs `except Exception as e:` au lieu d'exceptions spécifiques
- Peut masquer des erreurs importantes
- **Action**: Affiner les blocs except progressivement

---

## FEUILLE DE ROUTE ÉTAPE PAR ÉTAPE

### PHASE 0 — Sécurité Immédiate (Faire MAINTENANT, avant tout)

**Étape 0.1 — Audit de l'historique Git pour les secrets**

bash

```bash
# Vérifier si config.yaml a jamais été commité
git log --all --full-history -- config/config.yaml
git log --all --full-history -- "*.yaml" "*.json" "*.key" "*.env"

# Scanner l'historique complet pour les secrets
# Installer gitleaks et scanner
gitleaks detect --source . --log-opts="--all"
```

**Étape 0.2 — Rotation des credentials SI compromis**

- Régénérer la clé API Obsidian Local REST API
- Regénérer/changer la clé SSH Kali
- Mettre à jour config.yaml avec nouveaux credentials

**Étape 0.3 — Installer un hook pre-commit anti-secrets**

bash

```bash
pip install detect-secrets pre-commit
# Créer .pre-commit-config.yaml avec detect-secrets hook
# Générer baseline: detect-secrets scan > .secrets.baseline
pre-commit install
```

**Étape 0.4 — Vérifier .gitignore est correct**

- Confirmer que config/config.yaml, *.log, output/, vault_sync/cache/ sont bien ignorés
- Tester: `git status` ne doit PAS montrer config.yaml

---

### PHASE 1 — Modules OPSEC Manquants (Fondation de sécurité)

**Étape 1.1 — Créer scripts/opsec/identity_guard.py** Objectif: Détecter les PII avant tout commit ou publication

python

```python
# Doit détecter:
# - Noms réels (Michael Gauthier Guillet + variantes)
# - IPs de targets réels
# - Noms de clients
# - Clés API (patterns regex: sk-, ghp_, etc.)
# - Chemins de fichiers personnels (C:/Users/th3th/)
# - Emails personnels
```

**Étape 1.2 — Créer scripts/opsec/trace_cleaner.py** Objectif: Nettoyer les artefacts post-opération

python

```python
# Doit nettoyer:
# - output/ (fichiers temporaires)
# - Logs d'outils OSINT
# - Cache DNS local
# - Historique shell (fichiers .history créés)
# - Fichiers temporaires de scan Nmap
```

**Étape 1.3 — Améliorer vpn_check.py**

- Ajouter IP de référence "home" dans config.yaml
- Comparer IP courante à la référence (plus fiable qu'un check binaire)
- Ajouter vérification de DNS leak (dnsleak.com API)

---

### PHASE 2 — Module Recon Active (Le cœur manquant)

**Étape 2.1 — Créer scripts/recon/network_scan.py** Wrapper Python pour Nmap via kali_ssh_client:

python

```python
# Fonctionnalités:
# - SYN scan (-sS) — requiert root sur Kali
# - Service detection (-sV)
# - OS fingerprinting (-O)
# - Script scan (-sC pour scripts NSE)
# - Output XML → parsing automatique → dict Python
# - OPSEC gate: verify_opsec(require_vpn=True) avant tout scan
# - Limitation: scan uniquement dans le scope autorisé
```

**Étape 2.2 — Créer scripts/recon/web_enum.py** Wrapper pour outils web via hexstrike-ai:

python

```python
# Fonctionnalités:
# - Directory bruteforce (Gobuster/FFuf via hexstrike)
# - CMS detection (WPScan, etc.)
# - HTTP headers analysis
# - SSL/TLS certificate inspection
# - CORS misconfiguration detection
# - Robots.txt + sitemap analysis (passif)
```

**Étape 2.3 — Créer scripts/recon/vuln_scan.py**

python

````python
# Fonctionnalités:
# - Nuclei templates via hexstrike-ai
# - CVE correlation via hexstrike CVE agent
# - CVSS scoring
# - Severity bucketing: Critical/High/Medium/Low/Info
```

---

### PHASE 3 — Tests (Non-négociable en cybersécurité pro)

**Étape 3.1 — Créer la structure de tests**
```
tests/
├── __init__.py
├── test_osint/
│   ├── test_domain_recon.py      # Mock crt.sh, Wayback, WHOIS
│   ├── test_breach_check.py      # Mock HIBP API
│   ├── test_social_footprint.py  # Mock HTTP responses
│   └── test_dark_web_monitor.py  # Mock Tor + paste sites
├── test_opsec/
│   ├── test_vpn_check.py         # Mock httpbin + torcheck
│   ├── test_identity_guard.py    # Test PII detection accuracy
│   └── test_trace_cleaner.py     # Test cleanup functions
├── test_reporting/
│   └── test_report_generator.py  # Test template rendering
└── test_vault/
    ├── test_vault_api.py         # Mock Obsidian REST API
    └── test_note_builder.py      # Test note construction
````

**Étape 3.2 — Configurer pytest + coverage**

bash

```bash
pip install pytest pytest-cov pytest-mock
# Créer pytest.ini avec paramètres de couverture
# Target: > 70% de couverture sur les modules OPSEC (critique)
```

**Étape 3.3 — Ajouter GitHub Actions pour les tests**

yaml

```yaml
# .github/workflows/tests.yml
# Runner: ubuntu-latest
# Steps: pip install, pytest --cov, upload coverage
```

---

### PHASE 4 — Qualité & Conformité Professionnelle

**Étape 4.1 — Configurer le linting**

bash

```bash
pip install flake8 black mypy bandit
# flake8: style PEP8
# black: formatage automatique
# mypy: type checking strict
# bandit: analyse statique de sécurité
```

**Étape 4.2 — Audit Bandit (sécurité statique)**

bash

```bash
bandit -r scripts/ mcp/ vault_sync/ -f json -o bandit_report.json
# Focus sur: B105/B106 (hardcoded passwords), B201 (flask debug), B301 (pickle)
# Analyser chaque finding et corriger ou justifier
```

**Étape 4.3 — Ajouter pyproject.toml**

toml

````toml
[tool.bandit]
exclude_dirs = ["tests/"]
skips = ["B324"]  # SHA-1 for HIBP k-anonymity (justified)

[tool.mypy]
strict = true
ignore_missing_imports = true
```

---

### PHASE 5 — Intégration & Déploiement (Setup sur Windows)

**Étape 5.1 — Valider setup Obsidian**
```
1. Ouvrir Obsidian → Settings → Community plugins
2. Installer "Local REST API" plugin
3. Activer et noter le port (27123) et générer une clé API
4. Mettre la clé dans config/config.yaml (obsidian.api_key)
5. Tester: python3 verify_connections.py
```

**Étape 5.2 — Valider setup Kali VM**
```
1. Démarrer la VM Kali
2. Vérifier l'IP: ip a (doit correspondre à config.yaml kali.host)
3. Tester SSH: ssh -i ~/.ssh/kali_lab_key kali@192.168.157.128
4. Démarrer hexstrike-ai: cd ~/hexstrike-ai && python3 hexstrike_server.py
5. Tester: curl http://localhost:8888/health (depuis Kali)
6. Vérifier: verify_connections.py montre ✅ pour tous
```

**Étape 5.3 — Valider le VPN + Tor pour dark web**
```
1. Activer VPN sur Windows host
2. Démarrer Tor Browser ou le service Tor
3. Tester: python3 -c "from scripts.opsec.vpn_check import verify_opsec; print(verify_opsec())"
4. Vérifier que status.safe == True avant tout dark web monitoring
````

---

### PHASE 6 — Workflows Opérationnels

**Étape 6.1 — Premier run OSINT complet**

bash

```bash
# Lancer le dashboard
streamlit run streamlit_app.py

# Ou en ligne de commande directe:
python3 scripts/osint/domain_recon.py example.com --output vault
python3 scripts/osint/social_footprint.py targetuser --output vault
```

**Étape 6.2 — Valider le pipeline de rapport**

bash

```bash
python3 scripts/reporting/report_generator.py \
  --type osint \
  --target "test-target.com" \
  --output local  # tester en local d'abord, puis vault
```

**Étape 6.3 — Valider le sync Vault**

python

````python
from vault_sync.vault_api import ObsidianVaultClient
vault = ObsidianVaultClient.from_config()
print(vault.is_reachable())  # Doit être True
```

---

## PRIORITÉS ABSOLUES (ordre d'exécution recommandé)
```
1. [IMMÉDIAT]  Audit git history pour secrets exposés → rotation si nécessaire
2. [IMMÉDIAT]  Créer scripts/opsec/identity_guard.py (protection PII)
3. [IMMÉDIAT]  Installer pre-commit hook detect-secrets
4. [SEMAINE 1] Créer scripts/opsec/trace_cleaner.py
5. [SEMAINE 1] Créer scripts/recon/network_scan.py (wrapper Nmap)
6. [SEMAINE 1] Créer scripts/recon/web_enum.py (wrapper hexstrike)
7. [SEMAINE 1] Créer scripts/recon/vuln_scan.py (Nuclei/CVE)
8. [SEMAINE 2] Créer tests/ avec pytest (couverture ≥70% OPSEC)
9. [SEMAINE 2] Configurer bandit + mypy + flake8
10. [SEMAINE 2] GitHub Actions pour tests automatisés
11. [SEMAINE 3] Setup complet Obsidian + hexstrike + Tor
12. [SEMAINE 3] Premier pentest lab complet de bout en bout
````

---

## STANDARDS PROFESSIONNELS MANQUANTS

Pour contribuer à des projets cybersécurité dans les règles de l'art:

|Standard|Statut|Action requise|
|---|---|---|
|OWASP Secure Coding|⚠️ Partiel|Audit bandit + corriger findings|
|Gestion des secrets|❌ Manquant|detect-secrets + rotation credentials|
|Tests automatisés|❌ Absent|Créer suite pytest complète|
|CI/CD tests|❌ Absent|GitHub Actions tests workflow|
|Type checking strict|⚠️ Partiel|mypy --strict sur tous les modules|
|Documentation API|⚠️ Partiel|Compléter docstrings|
|Revue OPSEC|⚠️ Partiel|Améliorer vpn_check + ajouter DNS leak|
|Logging structuré|⚠️ Partiel|Ajouter contexte opération dans logs|
|Authorization gates|✅ Présent|Bon, maintenir et renforcer|
|Rapport de vulnérabilités|✅ Templates|Complets et professionnels|

---

## FICHIERS CRITIQUES À MODIFIER/CRÉER

**Créer (nouveaux fichiers)**:

- `scripts/opsec/identity_guard.py` — Protection PII
- `scripts/opsec/trace_cleaner.py` — Nettoyage post-op
- `scripts/recon/network_scan.py` — Recon active Nmap
- `scripts/recon/web_enum.py` — Enumération web
- `scripts/recon/vuln_scan.py` — Scan vulnérabilités
- `tests/` — Suite de tests complète
- `.pre-commit-config.yaml` — Hooks de sécurité
- `pyproject.toml` — Config bandit/mypy/black

**Modifier (fichiers existants)**:

- `scripts/opsec/vpn_check.py` — Ajouter IP home reference + DNS leak check
- `mcp/kali_ssh_client.py` — Remplacer AutoAddPolicy par RejectPolicy + fingerprint
- `requirements.txt` — Ajouter pytest, detect-secrets, bandit, mypy, black
- `.gitignore` — Vérifier exhaustivité

---

## VÉRIFICATION FINALE (Definition of Done)

Le projet sera "production-ready" cybersécurité quand:

- [ ]  `git log --all -- config/` ne montre aucun secret commité
- [ ]  `detect-secrets scan` retourne 0 findings
- [ ]  `bandit -r scripts/ mcp/ vault_sync/` retourne 0 HIGH/CRITICAL
- [ ]  `pytest tests/ --cov` retourne ≥70% coverage
- [ ]  `mypy scripts/ mcp/ vault_sync/` retourne 0 erreurs
- [ ]  `python3 verify_connections.py` retourne ✅ pour tous
- [ ]  Un run OSINT complet fonctionne de bout en bout vers le Vault
- [ ]  Le pre-commit hook bloque si secrets détectés
