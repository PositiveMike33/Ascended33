
$`tshark -r file.pcap -Y "http.request"`

---  
  La commande `tshark -r file.pcap -Y "http.request"` est le scalpel du pentester pour isoler les interactions client-serveur.  
  
**📝 Ce que fait cette commande  
Cette commande utilise **Tshark** (la version CLI de Wireshark) pour traiter un fichier de capture de paquets (`.pcap`).  
- `-r file.pcap` : (Read) Lit le fichier spécifié au lieu de capturer en direct.  
- `-Y "http.request"` : Applique un **filtre d'affichage** (Display Filter). Elle ordonne à Tshark de ne montrer que les paquets qui sont des requêtes HTTP (GET, POST, PUT, etc.), en ignorant les réponses du serveur (200 OK, 404, etc.) et tout le trafic non-HTTP (TCP, DNS, etc.).  
  
## 🎯 Pourquoi on l'utilise  
En analyse forensique ou en audit, un fichier PCAP peut contenir des millions de paquets. Ouvrir un fichier de 2 Go dans l'interface graphique de Wireshark est souvent lent, voire impossible.  
On utilise cette commande pour :  
1. **Extraire rapidement l'intention de l'attaquant** (quelles pages a-t-il consultées ?).  
2. **Automatiser l'analyse** via des scripts Bash.  
3. **Isoler les indicateurs de compromission (IoC)** liés au protocole HTTP.  
  
## 🔍 Scénarios appropriés  
1. **Analyse de Directory Bruteforce :** Identifier si un attaquant a tenté de deviner des dossiers cachés (ex: `/admin`, `/.env`) en observant la succession rapide de requêtes.  
2. **Détection d'Exfiltration de Données :** Repérer des requêtes `POST` suspectes vers des domaines inconnus ou des requêtes `GET` contenant de longues chaînes de caractères encodées en Base64.  
3. **Recherche de Web Shells :** Traquer les interactions avec un fichier `.php` ou `.jsp` récemment uploadé sur un serveur web compromis.  
  
## ⚠️ Précautions  
- **Données Sensibles :** Les requêtes HTTP circulent souvent en clair (si ce n'est pas du HTTPS). Elles peuvent contenir des mots de passe (Basic Auth), des cookies de session ou des données personnelles. Manipule ces fichiers avec la plus grande confidentialité.  
- **Limitation TLS/SSL :** Cette commande ne fonctionnera pas sur du trafic HTTPS (port 443) à moins que tu ne fournisses les clés de déchiffrement à Tshark.  
- **Légalité :** N'analyse que des captures réseaux pour lesquelles tu as une autorisation explicite. L'interception de trafic tiers est un délit.  
  
## 💡 Variantes utiles  
  
**1. Extraire uniquement les domaines et les URIs (format propre) :**  
```bash  
tshark -r file.pcap -Y "http.request" -T fields -e http.host -e http.request.uri  
```  
*Idéal pour générer une liste de liens visités sans le surplus de texte.*  
  
**2. Isoler uniquement les méthodes POST (souvent là où se trouvent les identifiants) :**  
```bash  
tshark -r file.pcap -Y "http.request.method == POST"  
```  
  
**3. Chercher des User-Agents spécifiques (ex: détection de scanners comme Nmap ou SQLMap) :**  
```bash  
tshark -r file.pcap -Y "http.user_agent contains \"sqlmap\""  
```  
  
---  
**Conseil d'expert :** "Le bruit est l'ennemi de l'analyste. Apprends à filtrer avant de chercher à comprendre."  
  
Tu as une capture sous la main pour tester ?**