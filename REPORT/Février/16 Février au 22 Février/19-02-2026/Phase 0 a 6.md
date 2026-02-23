#20-02-2026 #Update #ascended33 
~~PHASE 0 — IMMÉDIAT (avant tout autre chose)~~
  ~~0.1  git log pour vérifier secrets dans historique~~
  ~~0.2  Rotation credentials si trouvés~~
  ~~0.3  pip install detect-secrets pre-commit → hook installé~~
  ~~0.4  Vérifier .gitignore exhaustif~~

PHASE 1 — SEMAINE 1 (fondation OPSEC)
  1.1  Créer identity_guard.py (patterns PII: nom, IP, clés API, chemins)
  1.2  Créer trace_cleaner.py (cleanup post-op: output/, logs, cache DNS)
  1.3  Améliorer vpn_check.py (IP home reference + DNS leak check)

PHASE 2 — SEMAINE 1 (modules recon manquants)
  2.1  Créer scripts/recon/network_scan.py (Nmap via KaliSSH)
  2.2  Créer scripts/recon/web_enum.py (hexstrike-ai agents)
  2.3  Créer scripts/recon/vuln_scan.py (Nuclei + CVE)

PHASE 3 — SEMAINE 2 (tests — non-négociable)
  3.1  Créer tests/ avec pytest + mocks pour tous les modules
  3.2  Target: ≥70% coverage sur modules OPSEC
  3.3  GitHub Actions workflow pour tests automatisés

PHASE 4 — SEMAINE 2 (qualité pro)
  4.1  pip install bandit mypy black flake8
  4.2  bandit -r scripts/ → corriger tous HIGH/CRITICAL
  4.3  pyproject.toml (config outils)

PHASE 5 — SEMAINE 3 (intégration réelle)
  5.1  Setup Obsidian + plugin Local REST API → tester verify_connections.py
  5.2  Démarrer Kali VM + hexstrike-ai → valider SSH + MCP
  5.3  VPN + Tor → valider verify_opsec() retourne True

PHASE 6 — SEMAINE 3 (premier run complet)
  6.1  OSINT end-to-end vers Vault
  6.2  Rapport généré et synced dans Obsidian
  6.3  Trace cleaner post-op
