

Salut, ici **Nikto Expert**. En tant que spécialiste HexStrike, je vais t'apprendre à maîtriser l'un des paramètres les plus puissants de Nikto pour affiner tes scans de serveurs web.  
  
Voici ta leçon sur l'optimisation des scans avec l'option de **Tuning**.  
  
---  
  
# 🎓 Leçon : Maîtriser le scan sélectif avec Nikto  
  
**📝 Ce que fait cette commande  
La commande `nikto -h url -Tuning x` permet de scanner un hôte (`-h`) en filtrant spécifiquement les types de tests de vulnérabilités à exécuter.  
  
Le paramètre `-Tuning` suivi d'une valeur (chiffre ou lettre) indique à Nikto de ne lancer que certaines catégories de tests (ou d'en exclure si on utilise le préfixe `x`). Les catégories vont de **1** (Fichiers intéressants) à **c** (Inclusion de fichiers distants).  
  
## 🎯 Pourquoi on l'utilise  
Nikto est extrêmement bruyant et génère des milliers de requêtes. On utilise le **Tuning** pour :  
1. **Gagner du temps :** Ne tester que ce qui est pertinent pour la cible.  
2. **Discrétion relative :** Réduire le nombre de requêtes pour éviter de saturer les logs (même si Nikto reste peu discret).  
3. **Précision :** Se focaliser sur un vecteur d'attaque spécifique (ex: SQLi uniquement).  
  
## 🔍 Scénarios appropriés  
  
1. **Audit de configuration rapide :**  
Si tu suspectes uniquement des erreurs de configuration serveur ou des fichiers par défaut oubliés, tu utiliseras `-Tuning 2`. C'est idéal pour un check rapide après un déploiement.  
  
2. **Test ciblé sur les injections (XSS/SQLi) :**  
Sur une application web riche en formulaires, tu utiliseras `-Tuning 49` (4 pour le XSS, 9 pour le SQL Injection) pour ignorer les tests de fichiers serveurs et te concentrer sur les failles applicatives.  
  
3. **Éviter le déni de service (DoS) :**  
Lors d'un test sur un serveur de production fragile, tu utiliseras `-Tuning x6`. Le `x` indique une **exclusion**, et le `6` correspond aux tests de DoS. Cela permet de scanner sans risquer de faire tomber le service.  
  
## ⚠️ Précautions  
- **Autorisation obligatoire :** Comme tout outil de scan actif, ne l'utilise que sur des systèmes dont tu as l'autorisation écrite (ROE - Rules of Engagement).  
- **Bruit sur le réseau :** Nikto n'est pas fait pour la furtivité. Ses signatures sont connues de tous les IDS/IPS (Systèmes de détection d'intrusion).  
- **Faux positifs :** Nikto peut parfois signaler des fichiers "sensibles" qui sont en réalité des leurres ou des pages 404 mal configurées.  
  
## 💡 Variantes utiles  
  
* **Scanner uniquement l'injection SQL et l'exécution de commandes :**  
```bash  
nikto -h http://mon-serveur.com -Tuning 89  
```  
*(8 = Command Execution, 9 = SQL Injection)*  
  
* **Tout tester SAUF les tentatives de bruteforce d'authentification :**  
```bash  
nikto -h http://mon-serveur.com -Tuning xa  
```  
*(x = exclure, a = Authentication Bypass)*  
  
* **Scanner avec un format de sortie propre pour ton rapport :**  
```bash  
nikto -h url -Tuning 123 -Format htm -o rapport_scan.html  
```  
  
---  
**Note de l'expert :** Le Tuning est la différence entre un "script kiddie" qui lance un scan aveugle et un Pentester qui sait exactement ce qu'il cherche. Utilise-le pour rendre tes audits plus professionnels.  
  
Quelle est la prochaine étape de ton apprentissage ?**