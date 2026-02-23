 `masscan -p80,443 10.0.0.0/8 --rate 10000`  
  
---  
  
**📝 Ce que fait cette commande  
  
Cette commande lance un **scan de ports asynchrone** (SYN scan) à haute vitesse. Voici la décomposition technique :  
* **`-p80,443`** : Cible uniquement les ports standards Web (HTTP et HTTPS).  
* **`10.0.0.0/8`** : Définit la cible. Il s'agit d'un réseau privé de classe A complet, contenant **16 777 216 adresses IP**.  
* **`--rate 10000`** : Force l'envoi de **10 000 paquets par seconde**.  
  
Contrairement à un scanner classique, Masscan utilise sa propre pile TCP (bypassant celle de l'OS), ce qui lui permet de scanner ce volume massif d'IPs en un temps record sans saturer les ressources locales de la machine attaquante.  
  
## 🎯 Pourquoi on l'utilise  
  
On utilise cette configuration spécifique pour la **découverte rapide de surface d'attaque Web** sur une infrastructure gigantesque.  
  
* **Vitesse :** Scanner un `/8` avec Nmap prendrait des semaines. Avec Masscan à ce débit, cela se fait en un temps raisonnable (quelques heures).  
* **Ciblage précis :** En se limitant aux ports 80/443, on cherche spécifiquement des serveurs web, des interfaces d'administration ou des services exposés.  
* **Efficacité :** C'est l'outil idéal pour la phase de reconnaissance initiale ("Recon") avant de lancer des outils plus lourds (comme Nuclei ou Nmap) sur les hôtes vivants identifiés.  
  
## 🔍 Scénarios appropriés  
  
1. **Audit interne d'une multinationale :**  
Vous êtes connecté au réseau interne d'une très grande entreprise et devez identifier tous les serveurs web internes (Intranet, outils RH, Shadow IT) sur l'ensemble du réseau privé 10.x.x.x.  
2. **Détection de "Shadow IT" :**  
L'équipe sécurité veut recenser toutes les interfaces web non déclarées qui tournent sur le réseau corporate pour vérifier si elles respectent les politiques de sécurité (HTTPS, authentification).  
3. **Vérification de segmentation réseau :**  
Depuis une zone critique, vous lancez ce scan pour vérifier si le pare-feu laisse passer le trafic web vers l'ensemble du réseau bureautique (ce qui ne devrait peut-être pas être le cas).  
  
## ⚠️ Précautions  
  
* **Saturation Réseau (DoS) :** 10 000 paquets/seconde peuvent saturer de vieux pare-feux, des commutateurs bas de gamme ou des liaisons VPN fragiles. Surveillez la latence du réseau.  
* **Bruit et Détection :** Ce scan est **extrêmement bruyant**. Il déclenchera instantanément n'importe quel IDS/IPS (Snort, Suricata) ou SOC. Ce n'est pas une commande pour une approche furtive (Red Teaming discret).  
* **Exactitude :** Si le taux (`--rate`) est supérieur à ce que votre bande passante peut supporter, vous aurez des pertes de paquets et des faux négatifs (des serveurs existants ne seront pas vus).  
* **Légalité :** Scanner un `/8` entier n'est légal que si vous possédez ce réseau ou avez une autorisation explicite pour **toute** la plage.  
  
## 💡 Variantes utiles  
  
**1. Sauvegarde des résultats (Indispensable pour l'automatisation) :**  
```bash  
masscan -p80,443 10.0.0.0/8 --rate 10000 -oJ resultats_web.json  
```  
*Ajoute `-oJ` pour sortir les données en format JSON, facilement ingérable par HexStrike ou des scripts Python.*  
  
**2. Scan plus large mais plus lent (Tous les ports) :**  
```bash  
masscan -p0-65535 10.0.0.0/16 --rate 50000  
```  
*Scanne tous les ports sur un réseau plus petit (`/16`), en augmentant le débit pour compenser le nombre de ports.*  
  
**3. Spécifier l'interface réseau et la source :**  
```bash  
masscan -p80 10.0.0.0/8 --rate 1000 -e eth0 --router-mac 66:55:44:33:22:11  
```  
*Utile si Masscan n'arrive pas à détecter automatiquement la passerelle ou l'interface de sortie (`-e`).*  
  
---  
*Fin de la leçon. Prêt pour l'exécution ou l'analyse.***