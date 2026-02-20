# Module 04 — Sécurité Web — OWASP Top 10

**Phase :** 2 — Sécurité Web + Bug Bounty
**Durée estimée :** 4–6 semaines
**Prérequis :** [[01 — Fondamentaux Reseaux TCP-IP]], [[02 — Linux pour la Securite]]

---

## L'OWASP Top 10

L'OWASP (Open Web Application Security Project) publie la liste des 10 vulnérabilités web les plus critiques.
C'est la référence mondiale pour la sécurité des applications web.

**Ressource principale :** [PortSwigger Web Security Academy](https://portswigger.net/web-security) — gratuit et excellent.

---

## A01 — Broken Access Control

**C'est quoi :** Les utilisateurs peuvent accéder à des ressources qui ne leur sont pas destinées.

**Exemple concret :**
```
# Utilisateur A accède à son profil
GET /user/profile?id=12345

# Il modifie l'ID et accède au profil d'un autre utilisateur
GET /user/profile?id=12346   ← IDOR (Insecure Direct Object Reference)
```

**Tester :**
- Changer les IDs dans les URLs et paramètres
- Accéder à des pages admin quand on est utilisateur
- Tester les méthodes HTTP (GET → POST → DELETE)

**Protéger :**
- Vérifier les autorisations côté serveur pour chaque requête
- Ne pas exposer les IDs internes directement

---

## A02 — Cryptographic Failures

**C'est quoi :** Données sensibles transmises ou stockées sans chiffrement.

**Exemples :**
- Mots de passe stockés en clair (ou hashés avec MD5)
- HTTP au lieu de HTTPS
- Cookies sensibles sans flag `Secure` et `HttpOnly`

**Tester :**
```bash
# Vérifier SSL/TLS
sslscan target.com
testssl.sh target.com

# Vérifier les cookies dans Burp
# Chercher : Secure flag? HttpOnly flag?
```

---

## A03 — Injection

**C'est quoi :** Des données non validées sont interprétées comme du code.

### SQL Injection
```sql
-- URL normale : /search?q=python
-- Payload : /search?q=python' OR '1'='1

-- La requête SQL devient :
SELECT * FROM books WHERE title = 'python' OR '1'='1'
-- Retourne TOUS les livres
```

**Tester avec SQLMap :**
```bash
sqlmap -u "https://target.com/search?q=test" --level=3
```

### Cross-Site Scripting (XSS)
```html
<!-- Payload injecté dans un champ de recherche -->
<script>alert(document.cookie)</script>

<!-- Si réfléchi dans la page HTML sans échappement : -->
<h1>Résultats pour : <script>alert(document.cookie)</script></h1>
```

**Types de XSS :**
- **Reflected :** payload dans la requête, reflété dans la réponse
- **Stored :** payload sauvegardé en base, affiché à tous
- **DOM-based :** manipulation du DOM sans aller au serveur

**Tester :**
```html
<!-- Payloads de base -->
<script>alert(1)</script>
"><script>alert(1)</script>
<img src=x onerror=alert(1)>
<svg onload=alert(1)>
```

---

## A04 — Insecure Design

**C'est quoi :** La logique métier elle-même est mal conçue.

**Exemple :**
- Un coupon de réduction applicable en boucle
- Un mot de passe réinitialisé sans vérifier l'identité
- Un paiement validable sans finaliser la transaction

**Tester :** Réfléchir à "que se passe-t-il si je fais X en dehors du flux normal ?"

---

## A05 — Security Misconfiguration

**C'est quoi :** Mauvaise configuration des serveurs, frameworks, ou services.

**Exemples communs :**
- Pages de debug/erreur activées en production
- Comptes par défaut non changés (admin/admin)
- Répertoires non protégés avec listing activé
- Versions de logiciels exposées dans les en-têtes

**Tester :**
```bash
# Énumération de répertoires
gobuster dir -u https://target.com -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt

# En-têtes HTTP (versions exposées)
curl -I https://target.com

# Nikto
nikto -h https://target.com
```

---

## A06 — Vulnerable and Outdated Components

**C'est quoi :** Utilisation de bibliothèques ou composants avec des vulnérabilités connues.

**Tester :**
```bash
# Identifier les technologies et versions
whatweb https://target.com
wappalyzer (extension navigateur)

# Vérifier les CVEs
# searchsploit nom_logiciel version
searchsploit wordpress 5.8
searchsploit apache 2.4.49
```

---

## A07 — Identification and Authentication Failures

**C'est quoi :** Failles dans les mécanismes d'authentification.

**Exemples :**
- Pas de protection contre le bruteforce
- Tokens de session prévisibles
- Fonctionnalité "Se souvenir de moi" mal implémentée
- Réinitialisation de mot de passe par email sans expiration

**Tester :**
```bash
# Bruteforce login (SEULEMENT si autorisé)
hydra -l admin -P /usr/share/wordlists/rockyou.txt target.com http-post-form "/login:user=^USER^&pass=^PASS^:Invalid"

# JWT (JSON Web Tokens)
# Aller sur jwt.io — décoder et analyser le token
# Tester : alg:none, HS256 avec secret faible
```

---

## A08 — Software and Data Integrity Failures

**C'est quoi :** Manque de vérification d'intégrité des mises à jour ou données.

**Exemple :** Update automatique d'un package sans vérification de signature → supply chain attack

---

## A09 — Security Logging and Monitoring Failures

**C'est quoi :** Absence de journalisation des événements de sécurité.

**Impact :** Les attaques passent inaperçues pendant des mois.

**Recommandation :** Vérifier dans le rapport si le client a des logs, alertes, et un SIEM.

---

## A10 — Server-Side Request Forgery (SSRF)

**C'est quoi :** Le serveur fait des requêtes HTTP pour toi vers des destinations que tu contrôles.

**Exemple :**
```
# Fonctionnalité normale : charger une image depuis une URL
POST /api/fetch-image
{"url": "https://example.com/image.jpg"}

# Payload SSRF
{"url": "http://169.254.169.254/latest/meta-data/"}  ← Metadata AWS
{"url": "http://localhost/admin"}  ← Accès réseau interne
{"url": "file:///etc/passwd"}  ← Fichiers locaux
```

---

## Setup Pratique — Burp Suite

**Burp Suite Community Edition — Configuration de base :**

1. **Ouvrir Burp** → Proxy → Options → Proxy Listeners : 127.0.0.1:8080
2. **Configurer Firefox :**
   - Settings → Network Settings → Manual proxy
   - HTTP Proxy : 127.0.0.1, Port : 8080
3. **Installer le certificat CA Burp :**
   - Dans Firefox, visiter : http://burp
   - CA Certificate → Télécharger
   - Firefox → Settings → Privacy → Certificates → Import

**Fonctionnalités clés :**
- **Proxy** : Intercepter et modifier les requêtes
- **Repeater** : Rejouer et modifier des requêtes individuelles
- **Intruder** : Fuzzing automatisé (limité en version gratuite)
- **Decoder** : Encoder/décoder (base64, URL, HTML, etc.)

---

## Environnements de Practice

### DVWA (Damn Vulnerable Web Application)
```bash
# Installation Docker (plus simple)
docker run --rm -it -p 80:80 vulnerables/web-dvwa

# Accéder via : http://localhost
# Login : admin / password
# Mettre le niveau de difficulté à "Low" pour commencer
```

### PortSwigger Web Security Academy
- URL : [portswigger.net/web-security](https://portswigger.net/web-security)
- 100% gratuit
- Labs interactifs pour chaque catégorie OWASP
- **Le meilleur endroit pour apprendre la sécurité web**

---

## Checklist de Validation

- [ ] Je comprends les 10 catégories OWASP
- [ ] J'ai testé XSS, SQLi, et IDOR sur DVWA
- [ ] J'ai configuré Burp Suite et intercepté des requêtes
- [ ] J'ai complété 5 labs PortSwigger Academy
- [ ] Je peux expliquer la différence entre XSS reflété et stocké
- [ ] Je sais ce qu'est un IDOR et comment le tester

**Quand toutes les cases sont cochées → Module 04 : Complété**

---

*Module 04 — Parcours HexStrike | Retour vers [[Parcours HexStrike]]*
