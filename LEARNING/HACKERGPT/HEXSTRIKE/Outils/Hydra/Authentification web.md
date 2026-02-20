## $`hydra -L users -P pass http-form-post://`
#authentifications_web
  
  **📝 Ce que fait cette commande  
La commande `hydra -L users -P pass http-form-post://` est une attaque par dictionnaire automatisée ciblant un formulaire de connexion Web (méthode POST).  
  
* **`hydra`** : L'outil de brute-force réseau ultra-rapide.  
* **`-L users`** : Charge une liste d'utilisateurs potentiels depuis un fichier nommé "users".  
* **`-P pass`** : Charge une liste de mots de passe depuis un fichier nommé "pass".  
* **`http-form-post://`** : Indique à Hydra d'utiliser le module spécifique aux formulaires HTTP POST (le type le plus courant pour les pages de login).  
  
*Note : Pour être complète, cette commande nécessite normalement des arguments supplémentaires (URL, paramètres du formulaire et message d'erreur).*  
  
## 🎯 Pourquoi on l'utilise  
On l'utilise pour vérifier la **résistance aux attaques par dictionnaire**. En tant qu'expert, cela nous permet de démontrer qu'un compte peut être compromis en quelques secondes si la politique de mot de passe est faible ou si aucune protection contre le brute-force (comme le bannissement d'IP ou le CAPTCHA) n'est en place.  
  
## 🔍 Scénarios appropriés  
1. **Audit de CMS (WordPress/Joomla) :** Tester les accès à l'interface `/wp-login.php` ou `/administrator/` pour s'assurer que l'administrateur n'utilise pas de couple identifiant/mot de passe par défaut.  
2. **Test de Portails Captifs :** Vérifier la sécurité des interfaces de connexion Wi-Fi d'entreprise ou d'hôtels.  
3. **Équipements IoT/Industriels :** Tester les interfaces web de routeurs ou de caméras IP qui utilisent souvent des identifiants prévisibles (admin/admin).  
  
## ⚠️ Précautions  
* **Légalité :** Ne lancez cette commande **que** sur des cibles pour lesquelles vous avez une autorisation écrite explicite (Scope de Pentest).  
* **Verrouillage de compte :** Attention ! Une attaque de ce type peut verrouiller les comptes des utilisateurs réels (Account Lockout Policy), perturbant ainsi la production.  
* **Bruit réseau :** Hydra génère énormément de logs. C'est une méthode "bruyante" facilement détectable par un IDS/IPS ou un WAF.  
  
## 💡 Variantes utiles  
**1. Cibler un utilisateur spécifique avec une liste de mots de passe :**  
`hydra -l admin -P passlist.txt 192.168.1.10 http-form-post "/login.php:user=^USER^&pass=^PASS^:F=Invalid"`  
*(Ici, on fixe l'utilisateur "admin" et on définit précisément le format du formulaire).*  
  
**2. Augmenter la vitesse (Threads) :**  
`hydra -L users -P pass -t 64 http-form-post://...`  
*(L'option `-t 64` lance 64 connexions en parallèle pour accélérer le processus).*  
  
**3. Utiliser le mode verbeux pour voir les tentatives en direct :**  
`hydra -V -L users -P pass http-form-post://...`  
*(L'option `-V` affiche chaque couple testé, utile pour le débogage).*  
  
---  
**Conseil d'expert :** Toujours analyser la requête POST avec l'inspecteur de votre navigateur (F12) ou Burp Suite avant de lancer Hydra pour identifier les noms exacts des champs `user` et `password`**