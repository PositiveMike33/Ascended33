# 🎓 Leçon : Maîtriser `prowler aws`  
  
**📝 Ce que fait cette commande  
La commande `prowler aws` est le point d'entrée pour l'audit de sécurité d'une infrastructure AWS. Elle lance un scan complet de ton environnement (ou d'un compte spécifique) en vérifiant plus de 250 contrôles de sécurité basés sur le **CIS Benchmark (Center for Internet Security)** et d'autres frameworks de conformité (PCI-DSS, ISO27001, HIPAA). Elle analyse les configurations de l'IAM, du réseau (VPC), du stockage (S3), des bases de données (RDS), et bien plus.  
  
## 🎯 Pourquoi on l'utilise  
Dans le Cloud, la **mauvaise configuration** est la menace n°1. On utilise `prowler aws` pour :  
* **Identifier les "Low Hanging Fruits"** : Trouver instantanément les buckets S3 ouverts au public ou les groupes de sécurité autorisant le SSH (port 22) depuis `0.0.0.0/0`.  
* **Vérifier la conformité** : S'assurer que l'infrastructure respecte les standards légaux ou industriels.  
* **Hardening (Durcissement)** : Obtenir une liste précise d'actions correctives pour réduire la surface d'attaque.  
  
## 🔍 Scénarios appropriés  
1. **Audit Initial (Shadow IT/Legacy)** : Tu récupères la gestion d'un compte AWS dont tu ignores l'historique. Prowler te donne une vue d'ensemble immédiate des failles héritées.  
2. **Pré-Audit de Certification** : Avant un audit formel (type SOC2 ou PCI), tu lances Prowler pour corriger les non-conformités en amont.  
3. **Surveillance de la Dérive (Config Drift)** : Intégré dans une pipeline CI/CD ou un cron job, il permet de détecter si un développeur a modifié une règle de sécurité de manière non sécurisée après le déploiement.  
  
## ⚠️ Précautions  
* **Permissions IAM** : Prowler nécessite un utilisateur ou un rôle IAM avec des permissions de lecture (généralement `SecurityAudit` et `ViewOnlyAccess`). N'utilise jamais un utilisateur `Root`.  
* **API Throttling** : Sur des environnements massifs, Prowler peut générer un grand nombre d'appels API, ce qui peut déclencher un bridage (throttling) de la part d'AWS.  
* **Autorisation** : Même si c'est un outil de scan passif (lecture), assure-toi d'avoir l'autorisation explicite du propriétaire du compte avant de scanner.  
  
## 💡 Variantes utiles  
  
### 1. Cibler un service spécifique  
Si tu ne veux scanner que le stockage pour trouver des fuites de données :  
```bash  
prowler aws --services s3  
```  
  
### 2. Filtrer par sévérité  
Pour ne voir que les vulnérabilités critiques qui nécessitent une intervention immédiate :  
```bash  
prowler aws --severity critical  
```  
  
### 3. Générer un rapport HTML exploitable  
Idéal pour présenter tes résultats à un client ou à ta direction :  
```bash  
prowler aws -M html  
```  
*(Le rapport sera généré dans le dossier `output` avec des graphiques et des détails par ressource).*  
  
---  
**Conseil d'expert :** En tant que Pentester, commence toujours par un scan `critical` et `high` pour identifier les chemins d'exploitation rapides (comme des clés d'accès IAM trop permissives).  
  
Prêt pour la prochaine commande ?**