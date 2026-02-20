

Salut, ici **Wireshark Expert**. Bienvenue dans cette session de formation HexStrike. Aujourd'hui, nous maîtrisons la base de l'acquisition de données réseau en ligne de commande.  
  
Voici ta leçon sur l'utilisation de **Tshark**, le moteur de Wireshark sans interface graphique.  
  
---  
  
# 🎓 Leçon : Capture de trafic avec Tshark  
  
**📝 Ce que fait cette commande  
`tshark -i eth0 -w capture.pcap`  
  
* **`tshark`** : Lance l'outil de capture et d'analyse de paquets en ligne de commande.  
* **`-i eth0`** : Spécifie l'**interface** réseau à écouter (ici `eth0`, la première interface Ethernet).  
* **`-w capture.pcap`** : Indique à Tshark d'**écrire** (*write*) les données brutes dans un fichier nommé `capture.pcap` au lieu de les afficher à l'écran.  
  
## 🎯 Pourquoi on l'utilise  
En cybersécurité offensive et en administration système, on utilise cette commande pour :  
1. **Économiser les ressources** : Contrairement à l'interface graphique de Wireshark, Tshark consomme très peu de RAM et de CPU.  
2. **Capture à distance** : Idéal pour travailler via SSH sur un serveur distant ou une cible compromise.  
3. **Analyse différée** : On récupère le fichier `.pcap` pour l'analyser plus tard avec des outils plus puissants ou des scripts automatisés.  
  
## 🔍 Scénarios appropriés  
1. **Audit de serveur "Headless"** : Vous devez surveiller le trafic d'un serveur web qui ne possède pas d'interface graphique.  
2. **Investigation Forense** : Capturer le trafic réseau suspect pendant une attaque en cours pour conserver des preuves numériques non altérées.  
3. **Analyse de Malware** : Isoler une machine virtuelle infectée et enregistrer tout son trafic sortant pour identifier les serveurs C2 (Command & Control).  
  
## ⚠️ Précautions  
* **Privilèges** : L'accès aux interfaces réseau nécessite généralement les droits **root** (`sudo`).  
* **Espace Disque** : Sur un réseau à haut débit, un fichier `.pcap` peut saturer votre disque en quelques minutes. Surveillez la taille du fichier.  
* **Légalité** : Ne capturez jamais de trafic sur un réseau dont vous n'avez pas l'autorisation écrite explicite. L'interception de données privées est un délit pénal.  
  
## 💡 Variantes utiles  
  
### 1. Capturer uniquement un service spécifique (ex: HTTP)  
Ajoutez un filtre de capture pour ne pas polluer votre fichier :  
```bash  
sudo tshark -i eth0 -f "tcp port 80" -w http_only.pcap  
```  
  
### 2. Limiter la capture par nombre de paquets  
Utile pour un échantillonnage rapide (s'arrête après 1000 paquets) :  
```bash  
sudo tshark -i eth0 -c 1000 -w sample.pcap  
```  
  
### 3. Capturer sur toutes les interfaces simultanément  
Si vous ne savez pas par où passe le trafic :  
```bash  
sudo tshark -i any -w global_capture.pcap  
```  
  
---  
**Conseil d'expert :** Une fois ta capture terminée, utilise `tshark -r capture.pcap` pour relire le contenu ou ouvre-le dans l'interface graphique de Wireshark pour une analyse visuelle.  
  
Prêt pour la suite de ton entraînement sur Kali Linux ?**