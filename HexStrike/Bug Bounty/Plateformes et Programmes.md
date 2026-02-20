# Plateformes et Programmes de Bug Bounty

> Le bug bounty est la voie légale la plus accessible pour débuter en recherche de vulnérabilités.
> Chaque programme définit son scope. Hors scope = hors-la-loi.

---

## Grandes Plateformes

### HackerOne
**URL :** [hackerone.com](https://www.hackerone.com)
**Type :** Bug bounty + Vulnerability Disclosure Programs (VDP)
**Volume :** Plus de 3 000 programmes actifs

**Commencer :**
1. Créer un compte hacker
2. Compléter le profil et la vérification d'identité
3. Commencer par les programmes VDP (sans bounty mais scope large)
4. Progresser vers les programmes privés après premiers rapports acceptés

**Programmes recommandés pour débuter :**
- US Department of Defense (VDP — large scope, pas de bounty mais good practice)
- GitLab (scope large, bon pour l'apprentissage)
- Shopify (scope défini, bonne réactivité)

---

### Bugcrowd
**URL :** [bugcrowd.com](https://www.bugcrowd.com)
**Type :** Bug bounty + pentest as a service
**Volume :** 1 000+ programmes

**Points forts :** Interface claire, bon système de triage, programmes enterprise

---

### Intigriti
**URL :** [intigriti.com](https://www.intigriti.com)
**Type :** Bug bounty — focus Europe
**Points forts :** Communauté européenne, scope de programmes souvent bien défini

---

### YesWeHack
**URL :** [yeswehack.com](https://www.yeswehack.com)
**Type :** Bug bounty — Francophone (France + Québec)
**Points forts :** Interface en français, bonne pour les chercheurs francophones

---

### Open Bug Bounty
**URL :** [openbugbounty.org](https://www.openbugbounty.org)
**Type :** Coordination de divulgation (pas de bounty monétaire)
**Points forts :** Aucune inscription requise, volume important, bon pour pratiquer la divulgation responsable

---

## Programmes Canadiens et Québécois

### Gouvernement du Canada
- Pas de programme officiel public actif (à vérifier régulièrement)
- Signalement via : [cyber.gc.ca](https://www.cyber.gc.ca/fr/signalement)

### Banques Canadiennes
Plusieurs grandes banques ont des programmes de VDP (non publics).
Contacter directement via leur page sécurité (security@bank.com ou via PSIRT).

### Entreprises Québécoises
La plupart n'ont pas encore de programme formel.
Pour les contacter : chercher `security@`, `psirt@`, ou la page "Responsible Disclosure" sur leur site.

---

## Comprendre un Programme Bug Bounty

### Anatomy d'un Programme

**In-Scope :**
- Domaines, IPs, applications explicitement inclus
- Ce que tu peux tester

**Out-of-Scope :**
- Domaines et applications exclus
- Types de tests interdits (DoS, phishing, social engineering)
- Tester hors scope annule le bounty et peut être illégal

**Règles Typiques :**
- Pas de DoS / DDoS
- Pas d'accès aux données d'autres utilisateurs
- Pas d'altération ou suppression de données
- Divulgation responsable (ne pas publier avant fix)

### Catégories de Bounty (CVSS-based)

| Criticité | Fourchette Bounty Typique |
|-----------|--------------------------|
| Critique (9.0–10.0) | 5 000$ – 50 000$+ |
| Élevée (7.0–8.9) | 1 000$ – 5 000$ |
| Moyenne (4.0–6.9) | 250$ – 1 000$ |
| Faible (0.1–3.9) | 50$ – 250$ |
| Informationnelle | 0$ (acknowledgement) |

---

## Vulnérabilités les Plus Recherchées en Bug Bounty

1. **XSS (Cross-Site Scripting)** — Facile à trouver, bon pour débuter
2. **IDOR (Insecure Direct Object Reference)** — Accès aux ressources d'autres utilisateurs
3. **SSRF (Server-Side Request Forgery)** — Critique si accès cloud interne
4. **SQLi (SQL Injection)** — Moins fréquent mais très bien payé
5. **Auth Bypass** — Contournement d'authentification
6. **Open Redirect** — Souvent faible mais combinable
7. **Business Logic Flaws** — Difficile à automatiser, bon pour les chasseurs manuels

---

## Workflow de Soumission d'un Bug

1. **Reproduire** le bug de manière fiable (3 fois minimum)
2. **Documenter :**
   - Étapes de reproduction exactes
   - Screenshot ou vidéo
   - Requête HTTP/réponse (depuis Burp)
   - Impact réel (ne pas exagérer)
3. **Rédiger le rapport** avec le template [[Templates/TPL — Rapport Bug Bounty]]
4. **Soumettre** via la plateforme (jamais directement au public)
5. **Attendre** le triage (5-15 jours en général)
6. **Collaborer** avec l'équipe de sécurité si demandes de clarification

---

## Erreurs Communes des Débutants

- Tester hors scope (risque légal)
- Soumettre sans reproduire de manière fiable
- Exagérer l'impact dans le rapport
- Divulguer publiquement avant le fix
- Copier des rapports existants (duplicates non payés)
- Utiliser des outils automatisés agressifs (bannissement)

---

*HexStrike Bug Bounty — Légal, éthique, et persistant*
