$`nmap --script vuln target`

Salut, ici **Nmap Master**, ton expert HexStrike. Prêt à monter en compétence sur l'automatisation de la détection de failles ? Aujourd'hui, on décortique une commande pilier du moteur de script de Nmap (NSE).  
  
---  
  
# 🎓 Leçon : Détection de vulnérabilités avec NSE  
  
La commande : `nmap --script vuln `  
  
**📝 Ce que fait cette commande  
Cette commande active le **Nmap Scripting Engine (NSE)** en ciblant spécifiquement la catégorie de scripts nommée `vuln`.  
Au lieu de simplement vérifier si un port est ouvert, Nmap va interroger les services détectés (HTTP, SMB, FTP, etc.) pour vérifier s'ils sont affectés par des vulnérabilités connues (CVE), des configurations par défaut dangereuses ou des failles critiques répertoriées dans la base de données de scripts de Nmap.  
  
## 🎯 Pourquoi on l'utilise  
On l'utilise pour automatiser la phase de **Vulnerability Assessment**. C'est un gain de temps massif : au lieu de chercher manuellement chaque version de service sur Google ou Exploit-DB, Nmap fait la corrélation instantanément et te remonte si une cible est potentiellement exploitable (ex: EternalBlue, Heartbleed, vulnérabilités WordPress, etc.).  
  
## 🔍 Scénarios appropriés  
1. **Audit de périmètre interne :** Identifier rapidement les machines non patchées sur un réseau d'entreprise après avoir obtenu un accès initial.  
2. **Vérification de remédiation :** Après qu'un administrateur système a affirmé avoir patché une faille, tu lances ce scan pour confirmer que la vulnérabilité n'est plus détectable.  
3. **Reconnaissance pré-exploitation :** Lors d'un CTF ou d'un pentest, pour prioriser tes vecteurs d'attaque sur les services les plus "fragiles".  
  
## ⚠️ Précautions  
* **Bruit (Stealth) :** Cette commande est extrêmement **bruyante**. Elle génère beaucoup de trafic et sera immédiatement repérée par un IDS/IPS (Système de Détection d'Intrusion).  
* **Stabilité :** Bien que les scripts `vuln` soient généralement sûrs, certains peuvent provoquer des instabilités ou des dénis de service (DoS) sur des services très anciens ou fragiles.  
* **Légalité :** Ne lance jamais cette commande sur une cible sans une autorisation écrite (ROE - Rules of Engagement). C'est une action offensive claire.  
  
## 💡 Variantes utiles  
  
### 1. Le combo précision (Version + Vuln)  
Ajouter `-sV` permet à Nmap de détecter les versions exactes des services, ce qui aide les scripts `vuln` à être beaucoup plus précis.  
```bash  
nmap -sV --script vuln  
```  
  
### 2. Ciblage spécifique par port  
Inutile de scanner 1000 ports si tu ne t'intéresses qu'au serveur Web. On gagne en vitesse et en discrétion relative.  
```bash  
nmap -p 80,443 --script vuln  
```  
  
### 3. Utiliser une base de données étendue (Vulners)  
Si tu as installé le script tiers `http-vulners-paths.nse`, tu peux obtenir des résultats encore plus complets liés aux CVE récentes.  
```bash  
nmap -sV --script vulners  
```  
  
---  
**Conseil d'expert :** Toujours analyser les résultats avec un esprit critique. Un script peut indiquer une vulnérabilité parce qu'il détecte un numéro de version, même si un "backport" de sécurité a été appliqué par l'administrateur. **Vérifie toujours manuellement avant de conclure !**  
  
Des questions sur l'implémentation, Hacker ?**