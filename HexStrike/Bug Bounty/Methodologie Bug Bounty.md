# Méthodologie Bug Bounty — HexStrike

> La chasse aux bugs est une discipline. Pas un jeu de hasard.
> Méthode + persistance + rapports de qualité = succès.

---

## Mindset du Bug Hunter HexStrike

1. **Lire le programme à fond** avant de commencer — scope, règles, priorités
2. **Comprendre l'application** avant de l'attaquer — comment elle est censée fonctionner
3. **Chercher les anomalies** — là où la logique s'écarte du comportement attendu
4. **Documenter au fur et à mesure** — ne pas recompter sur sa mémoire
5. **Qualité > Quantité** — un bon rapport est 10x plus utile que 10 rapports médiocres

---

## Phase 1 — Sélection du Programme

**Critères de sélection pour débutant :**
- Scope large (plus de cibles = plus d'opportunités)
- Bonne réactivité (regarder les temps de réponse sur la plateforme)
- Pas de limite sur les types de vulnérabilités
- Préférer les VDP au début (moins de pression, apprentissage)

**Sources pour trouver des programmes :**
- [bugbounty.guide/list-of-bug-bounty-programs](https://bugbounty.guide)
- [chaos.projectdiscovery.io](https://chaos.projectdiscovery.io) — listes de sous-domaines in-scope

---

## Phase 2 — Reconnaissance du Programme

```bash
# Lister tous les sous-domaines in-scope
subfinder -d target.com | tee subdomains.txt

# Vérifier lesquels sont actifs
cat subdomains.txt | httpx -status-code -title -tech-detect

# Identifier les technologies
whatweb https://target.com
wappalyzer (extension navigateur)

# Chercher les endpoints API
# Regarder les fichiers JS pour des routes cachées
```

**Questions à se poser :**
- Quelle est la fonctionnalité principale de l'application ?
- Y a-t-il des zones d'upload de fichiers ?
- Y a-t-il des fonctionnalités de partage entre utilisateurs ?
- Y a-t-il une API ? De la documentation publique ?

---

## Phase 3 — Test Manuel (OWASP Top 10)

### XSS — Cross-Site Scripting
```
# Payloads de base à tester dans les champs de saisie
<script>alert(1)</script>
"><script>alert(1)</script>
<img src=x onerror=alert(1)>
javascript:alert(1)
```

**Où chercher :**
- Champs de recherche
- Formulaires de commentaires/profil
- Paramètres GET dans l'URL
- En-têtes HTTP reflétés dans la page

### IDOR — Insecure Direct Object Reference
```
# Exemple : changer l'ID dans l'URL
GET /user/profile?id=12345
→ Essayer id=12346, id=1, id=99999

# Dans les API
GET /api/users/12345/orders
→ Essayer avec d'autres IDs
```

### SQLi — Injection SQL
```sql
-- Payloads de base
' OR '1'='1
' OR 1=1--
'; DROP TABLE users--  (ne jamais utiliser en prod réelle)
' UNION SELECT 1,2,3--
```

### SSRF — Server-Side Request Forgery
```
# Tester des paramètres d'URL dans l'application
url=http://169.254.169.254/latest/meta-data/  (AWS metadata)
url=http://localhost/admin
url=file:///etc/passwd
```

### Open Redirect
```
# Dans les paramètres de redirection
?redirect=https://evil.com
?next=//evil.com
?url=javascript:alert(1)
```

---

## Phase 4 — Reproduction et Documentation

**Standard de documentation HexStrike :**

Pour chaque bug trouvé :
1. Créer une note dans `HexStrike/Vulnerabilites/`
2. Documenter :
   - URL exacte
   - Méthode HTTP (GET/POST/etc.)
   - Paramètre vulnérable
   - Payload utilisé
   - Réponse reçue (screenshot)
   - Impact réel démontré

**Reproduire 3 fois** avant de considérer le bug confirmé.

---

## Phase 5 — Rapport de Qualité

Utiliser le template [[Templates/TPL — Rapport Bug Bounty]].

**Ce qui fait un bon rapport :**
- Titre clair et précis (pas "XSS trouvé" mais "XSS reflected dans le paramètre `q` de search.php")
- Étapes de reproduction numérotées et précises
- Preuve concrète (screenshot, vidéo, requête Burp)
- Impact réel (ne pas dire "potentiellement critique" sans démontrer pourquoi)
- Suggestion de correction (optionnel mais apprécié)

**Ce qui fait rejeter un rapport :**
- "Potentiellement vulnérable à..."  (non reproduit)
- Impact exagéré par rapport à la réalité
- Duplicate (déjà reporté)
- Hors scope

---

## Outils Bug Bounty Spécifiques

```bash
# httpx — vérifier les sous-domaines actifs
httpx -l subdomains.txt -status-code -title

# nuclei — scanner de templates de vulnérabilités
nuclei -u https://target.com -t ~/nuclei-templates/

# gau — récupérer les URLs connues (Wayback + Common Crawl)
gau target.com | tee urls.txt

# waybackurls
waybackurls target.com | tee wayback.txt

# Parametres exposés
cat urls.txt | grep "?" | qsreplace "FUZZ"
```

---

## Suivi des Soumissions

Créer une note dans `HexStrike/Engagements/` pour chaque programme actif :

```markdown
# [Nom Programme] — Bug Bounty Tracker

**Plateforme :** HackerOne / Bugcrowd / etc.
**Date de début :** YYYY-MM-DD
**Statut :** Actif / Pause / Terminé

## Soumissions

| ID | Titre | Criticité | Statut | Bounty |
|----|-------|-----------|--------|--------|
| #001 | XSS in search | Moyen | Accepté | 250$ |
| #002 | IDOR in API | Élevé | En triage | - |

## Notes Reconnaissance
[Observations sur l'application, technologies, patterns]
```

---

*Méthodologie Bug Bounty HexStrike — Légale, méthodique, persistante*
