

Salut, ici ton expert **Amass** de chez HexStrike. Aujourd'hui, nous allons disséquer une commande fondamentale de la phase d'intelligence (OSINT) avec OWASP Amass.  
  
---  
  
# 🎓 Leçon : Reconnaissance d'Organisation avec Amass  
  
La commande du jour :  
```bash  
amass intel -whois -d domain.com  
```  
  
**📝 Ce que fait cette commande  
Cette commande utilise le sous-module **`intel`** (Intelligence) d'Amass pour effectuer une **recherche WHOIS inversée**.  
  
Au lieu de simplement lister les sous-domaines, elle va :  
1. Consulter les informations d'enregistrement (WHOIS) du domaine cible (`domain.com`).  
2. Identifier le nom de l'organisation ou l'adresse e-mail de l'enregistreur.  
3. Rechercher **tous les autres domaines** enregistrés par cette même entité sur Internet.  
  
## 🎯 Pourquoi on l'utilise  
En tant que Red Teamer ou Pentester, ton objectif est de définir le **périmètre d'attaque (Attack Surface)** complet.  
Souvent, une entreprise possède plusieurs domaines racines (ex: `entreprise.com`, `entreprise-services.fr`, `acme-marketing.net`). Cette commande permet de découvrir ces domaines "frères" que tu n'aurais pas trouvés avec une simple énumération de sous-domaines.  
  
## 🔍 Scénarios appropriés  
1. **Audit de Shadow IT :** Identifier des domaines oubliés par les équipes techniques qui pointent vers des infrastructures obsolètes ou non sécurisées.  
2. **Fusions et Acquisitions :** Mapper rapidement l'infrastructure d'une entreprise qui vient d'en racheter une autre.  
3. **Reconnaissance Initiale (Black Box) :** Quand tu n'as qu'un nom de domaine et que tu dois trouver tous les points d'entrée potentiels appartenant à la même organisation.  
  
## ⚠️ Précautions  
* **RGPD / Privacy :** Depuis la mise en place du RGPD, beaucoup d'informations WHOIS sont masquées ("Redacted for Privacy"). La commande peut donc être moins efficace sur les domaines européens récents.  
* **Faux Positifs :** Si l'organisation utilise un prête-nom ou un registraire générique (comme "Domains By Proxy"), Amass pourrait renvoyer des milliers de domaines n'appartenant pas à ta cible. Vérifie toujours manuellement les résultats.  
* **Autorisation :** Bien que ce soit de l'OSINT (passif), assure-toi que la portée de ton contrat autorise l'inclusion de domaines connexes découverts lors de la reconnaissance.  
  
## 💡 Variantes utiles  
  
**1. Rechercher par plage d'IP (ASN) :**  
Si tu veux trouver les domaines associés à une infrastructure spécifique :  
```bash  
amass intel -asn 12345  
```  
  
**2. Trouver l'organisation via une IP :**  
Utile si tu tombes sur un serveur et que tu veux savoir ce qui l'entoure :  
```bash  
amass intel -addr 192.168.1.1  
```  
  
**3. Mode Actif (Plus précis mais moins discret) :**  
Pour tenter de récupérer des certificats SSL et affiner la découverte :  
```bash  
amass intel -active -whois -d domain.com  
```  
  
---  
*Entraîne-toi sur des domaines dont tu as la gestion pour observer la corrélation des données. La maîtrise de l'information est la première étape d'une intrusion réussie. Des questions sur la sortie des résultats ?***