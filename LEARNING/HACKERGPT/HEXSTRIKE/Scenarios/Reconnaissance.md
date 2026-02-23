C'est l'étape la plus cruciale. Plus on passe de temps ici, moins on en perdra en phase d'exploitation. On va diviser ça en deux types : la **Passive** (discrète) et l'**Active** (plus bruyante). Voici la roadmap stratégique que nous allons suivre. 
---
### 1. Quelles données récolter ? (La Target List) Avant de lancer les scripts, on doit savoir ce qu'on cherche :
* **Infrastructure réseau :** Adresses IP (IPv4/v6), plages d'IP (Netblocks), ASNs (Autonomous System Numbers). 
* **Noms de domaine :** Sous-domaines (souvent les moins sécurisés), domaines associés, enregistrements DNS (MX, TXT, SPF). 
* **Technologies :** Serveurs web (Nginx, Apache), CMS (WordPress, Drupal), Frameworks (React, PHP), Bases de données.
* **Données Humaines/OSINT :** Emails d'employés, organigrammes, fuites de credentials (leaks), documents exposés (PDF/Docx avec métadonnées).
---
### 2. Étape par Étape : Le Protocole de Récolte 
#### Étape 1 : Reconnaissance Passive (OSINT) *Objectif : Collecter sans jamais toucher directement l'infrastructure de la cible.
* 1. **WHOIS & DNS :** Identifier le propriétaire et les serveurs de noms. ```bash whois target.com dig target.com ANY ``` 2. **Moteurs de recherche spécialisés :** Utiliser Shodan ou Censys pour voir ce qui est déjà indexé sur le web sans scanner soi-même. 
* *Outil :* [Shodan.io](https://www.shodan.io) 3. **Recherche de sous-domaines (Passive) :** Utiliser des agrégateurs de certificats SSL. * *Outil :* `subfinder -d target.com -silent`

#### Étape 2 : Énumération de Sous-Domaines (Active) *Objectif : Découvrir la surface d'attaque cachée (dev.target.com, staging.target.com).
1. **Brute-force DNS :** Tester des milliers de noms pour voir lesquels répondent. ```bash # Utilisation de subfinder combiné à httpx pour vérifier ce qui est vivant subfinder -d target.com | httpx -title -tech-detect -status-code ``` 
2. **DNS Zone Transfer (Si mal configuré) :** Tenter de récupérer toute la zone DNS. ```bash dig axfr @ns1.target.com target.com ```

#### Étape 3 : Fingerprinting des Services (Scanning) *Objectif : Identifier les versions des logiciels pour chercher des CVE (failles).* 
1. **Scan de ports intelligent :** On ne scanne pas tout d'un coup pour éviter les IDS (systèmes de détection). ```bash # Scan des 1000 ports les plus communs avec détection de version et d'OS nmap -sV -sC -T4 target.com ``` 
2. **Analyse des technos Web :** * *Outil :* `whatweb target.com` ou l'extension Wappalyzer.

#### Étape 4 : Énumération de Répertoires et Fichiers *Objectif : Trouver des fichiers sensibles (.env, .git, /admin, /config).
* 1. **Fuzzing de chemins :** ```bash gobuster dir -u https://target.com -w /usr/share/wordlists/dirb/common.txt ``` 

#### Étape 5 : OSINT & Data Leaks *Objectif : Trouver des points d'entrée via l'humain.
1. **Récolte d'emails :** * *Outil :* `theHarvester -d target.com -l 500 -b google`
2. **Recherche de credentials fuyés :** Consulter des bases comme *Have I Been Pwned* (API) ou des dumps de bases de données sur le Dark Web.---

### 3. Tableau de synthèse des outils
| Phase             | Outil Favori          | Utilité                                 |     |     |     |     |     |     |     |     |     |     |     |     |
| :---------------- | :-------------------- | :-------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **Sous-domaines** | **Amass / Subfinder** | Le top pour cartographier les domaines. |     |     |     |     |     |     |     |     |     |     |     |     |
|                   |                       |                                         |     |     |     |     |     |     |     |     |     |     |     |     |
|                   |                       |                                         |     |     |     |     |     |     |     |     |     |     |     |     |

### ⚠️ Avertissement de sécurité Michael, rappelle-toi : la reconnaissance **active** (Nmap, Gobuster) peut être détectée par les pare-feux et les SOC. Elle ne doit être pratiquée que sur des systèmes dont tu as l'autorisation écrite (contrat de pentest ou Bug Bounty).
### 🎯 Prochaine étape ?
On a une belle liste de sous-domaines et de ports ouverts. 
On regarde comment **analyser les vulnérabilités** sur un service spécifique qu'on aurait trouvé (ex: un serveur web avec une version obsolète) .

📊 **Mémoire mise à jour** | 
🎯 **Prochaine action : Analyse de vulnérabilités ou exploitation.**