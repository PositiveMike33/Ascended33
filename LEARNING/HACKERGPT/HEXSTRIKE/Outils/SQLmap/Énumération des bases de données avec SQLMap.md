$`sqlmap -u "url?id=1" --dbs`

Salut, ici ton expert **HexStrike**. Aujourd'hui, nous allons disséquer l'une des commandes fondamentales de l'arsenal SQLMap. Cette commande est souvent le point de bascule entre une suspicion de faille et une preuve d'exploitation concrète.  
  
Voici ta leçon sur l'énumération initiale.  
  
---  
  
# 🎓 Leçon : Énumération des bases de données avec SQLMap  
  
**📝 Ce que fait cette commande  
`sqlmap -u "url?id=1" --dbs`  
  
Cette commande automatise trois étapes critiques :  
1. **Analyse de la cible (`-u`)** : Elle teste le paramètre `id` dans l'URL pour détecter des vulnérabilités d'injection SQL (Boolean-based, Error-based, Union-based, etc.).  
2. **Fingerprinting** : Elle identifie le Système de Gestion de Base de Données (SGBD) utilisé (MySQL, PostgreSQL, MSSQL, Oracle, etc.).  
3. **Énumération (`--dbs`)** : Une fois l'injection confirmée, elle extrait les noms de toutes les bases de données (schémas) auxquelles l'utilisateur de la base de données a accès.  
  
## 🎯 Pourquoi on l'utilise  
On l'utilise pour la **cartographie des données**. Savoir quelles bases de données existent permet de :  
* Confirmer l'impact réel de la vulnérabilité.  
* Identifier les cibles prioritaires (ex: une base nommée `client_db` est plus critique que `test_db`).  
* Préparer les étapes suivantes de l'extraction (tables, colonnes, données).  
  
## 🔍 Scénarios appropriés  
1. **Audit de site Web dynamique** : Lors du test d'une application utilisant des paramètres de requête (comme un catalogue de produits ou un profil utilisateur) pour s'assurer que les entrées sont correctement sanitisées.  
2. **Validation de rapports Bug Bounty** : Pour prouver qu'une injection SQL est exploitable en fournissant la liste des bases de données comme preuve de concept (PoC).  
3. **Évaluation post-intrusion** : Dans un cadre de Red Team, pour identifier où sont stockées les informations sensibles (identifiants, données financières) une fois un point d'entrée trouvé.  
  
## ⚠️ Précautions  
* **Légalité** : Ne lance jamais cette commande sur un domaine sans autorisation écrite préalable (contrat de pentest).  
* **Bruit (Stealth)** : SQLMap est extrêmement bruyant par défaut. Les pare-feu applicatifs (WAF) et les IDS/IPS détecteront rapidement les centaines de requêtes générées.  
* **Intégrité** : Bien que `--dbs` soit une opération de lecture, des tests d'injection agressifs peuvent parfois ralentir ou faire planter des bases de données mal configurées.  
  
## 💡 Variantes utiles  
  
* **Mode Automatique (Batch) :**  
```bash  
sqlmap -u "url?id=1" --dbs --batch  
```  
*Utilise les réponses par défaut de SQLMap sans interrompre l'utilisateur.*  
  
* **Cibler la base actuelle uniquement :**  
```bash  
sqlmap -u "url?id=1" --current-db  
```  
*Plus rapide et discret si tu ne veux que le nom de la base de données utilisée par l'application actuelle.*  
  
* **Augmenter la discrétion :**  
```bash  
sqlmap -u "url?id=1" --dbs --random-agent --tamper=space2comment  
```  
*Utilise un User-Agent de navigateur aléatoire et un script de "tampering" pour tenter de contourner certains filtres de sécurité basiques.*  
  
---  
**Rappel de l'expert :** L'outil est puissant, mais ta méthodologie doit l'être encore plus. Utilise toujours le flag `--dbs` comme une étape de reconnaissance avant de plonger dans l'extraction de données spécifiques.**