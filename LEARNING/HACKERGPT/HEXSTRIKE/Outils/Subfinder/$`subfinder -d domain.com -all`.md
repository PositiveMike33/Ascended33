
Salut, ici **HackerGPT**, ton expert HexStrike. Aujourd'hui, nous allons disséquer une commande fondamentale de la phase de reconnaissance (Recon) avec **Subfinder**, l'un des outils de découverte de sous-domaines les plus performants du toolkit ProjectDiscovery.  
  
---  
  
# 🎓 Leçon : Énumération Exhaustive avec Subfinder  
  
La commande du jour :  
```bash  
subfinder -d domain.com -all  
```  
  
**📝 Ce que fait cette commande  
Cette commande lance une recherche de sous-domaines pour une cible spécifique (`-d domain.com`).  
Le flag crucial ici est **`-all`**. Par défaut, Subfinder utilise une sélection de sources rapides. En ajoutant `-all`, tu forces l'outil à interroger **toutes les sources passives disponibles** (plus de 30 sources comme BinaryEdge, Crtsh, Censys, etc.), même celles qui sont plus lentes ou qui demandent une configuration plus poussée.  
  
*Note : C'est une méthode **passive**, ce qui signifie que tu n'envoies aucun paquet directement aux serveurs de la cible.*  
  
## 🎯 Pourquoi on l'utilise  
En cybersécurité offensive, on ne peut pas protéger (ou attaquer) ce qu'on ne voit pas. On utilise cette commande pour :  
1. **Maximiser la couverture** : Trouver des sous-domaines que des scans rapides ignoreraient.  
2. **Discrétion totale** : Comme la recherche est passive (interrogation de bases de données tierces), la cible ne voit aucune activité dans ses logs.  
3. **Gain de temps** : Obtenir une liste massive de cibles potentielles en quelques secondes avant de passer à l'analyse active.  
  
## 🔍 Scénarios appropriés  
1. **Reconnaissance Initiale (Bug Bounty) :** Avant de lancer des outils de brute-force, tu récupères tout ce qui est déjà connu publiquement pour identifier des serveurs de staging (`dev.domain.com`) ou des interfaces d'administration oubliées.  
2. **Cartographie de l'empreinte numérique :** Pour un audit Red Team, afin de comprendre l'étendue de l'infrastructure exposée d'une entreprise.  
3. **Shadow IT :** Identifier des services mis en ligne par des employés sans l'aval du département sécurité (souvent moins sécurisés).  
  
## ⚠️ Précautions  
- **Sources API :** Pour que `-all` soit réellement efficace, tu dois configurer tes clés API dans le fichier `provider-config.yaml` de Subfinder (ex: Shodan, Chaos, GitHub). Sans ces clés, de nombreuses sources resteront muettes.  
- **Données obsolètes :** Les sources passives peuvent parfois lister des sous-domaines qui n'existent plus (DNS records historiques).  
- **Légalité :** Bien que passif, assure-toi d'avoir l'autorisation d'inclure ces domaines dans ton périmètre d'audit.  
  
## 💡 Variantes utiles  
  
**1. Pour le piping (automatisation) :**  
```bash  
subfinder -d domain.com -all -silent  
```  
*Le flag `-silent` n'affiche que les résultats bruts, idéal pour envoyer la sortie vers un autre outil comme `httpx`.*  
  
**2. Sortie structurée pour rapport :**  
```bash  
subfinder -d domain.com -all -o results.txt  
```  
*Enregistre tous les résultats dans un fichier texte pour une analyse ultérieure.*  
  
**3. Recherche sur plusieurs domaines :**  
```bash  
subfinder -dL list_of_domains.txt -all  
```  
*Si tu as une liste de domaines cibles, utilise `-dL` pour les traiter à la chaîne.*  
  
---  
**Conseil d'expert :** Combine toujours Subfinder avec un résolveur DNS actif (comme `puredns` ou `shuffledns`) pour vérifier lesquels de ces sous-domaines sont encore "vivants" après ta récolte passive.  
  
Prêt à passer à la suite de ton apprentissage ?**

Reconnaissance3DNS & Subdomain2Web Reconnaissance4Web Discovery4Parameter Discovery3Vulnerability Scanning4Exploitation2Password Attacks3Network Analysis2OSINT2Cloud Security2Binary Analysis3Cryptography1

🔬

### Nmap Master

`nmap`

⚡

### Masscan Expert

`masscan`

🦀

### RustScan Expert

`rustscan`

⚡

## Masscan Expert

Expert: `masscan`

🎯 Consult Expert

✅ Response from Masscan Expert

Salut. Ici **HackerGPT**, ton expert Masscan au sein de l'écosystème HexStrike. Si tu cherches la vitesse pure et l'efficacité à l'échelle d'Internet, tu es au bon endroit. Masscan n'est pas un scanner de ports ordinaire : c'est un moteur asynchrone capable de scanner l'intégralité d'Internet en moins de 6 minutes si ton interface réseau le permet.

Voici ton guide d'utilisation expert pour maîtriser la bête.

---

### 1. Fondamentaux : La Syntaxe de Base
Contrairement à Nmap, Masscan est asynchrone. Il n'attend pas de réponse avant d'envoyer le paquet suivant.

```bash
# Scan simple d'un réseau sur le port 80 à une vitesse modérée
masscan 192.168.1.0/24 -p80 --rate 1000
```

### 2. La Puissance de Frappe : `--rate` et Performance
C'est ici que Masscan brille. Avec les bons pilotes (comme PF_RING), tu peux atteindre **10 millions de paquets par seconde (10M pps)**.

*   **Attention :** À ces vitesses, tu peux saturer ton propre routeur ou être banni par ton FAI (Blackholing).
*   **Recommandation :** Commence bas et augmente progressivement.

```bash
# Scan massif à 100 000 paquets/sec (nécessite une bande passante solide)
masscan 10.0.0.0/8 -p443 --rate 100000
```

### 3. Maîtrise de l'Infrastructure : `--adapter-ip` et Évasion
Si tu as plusieurs interfaces ou si tu veux spécifier ton IP source pour éviter la détection ou gérer le routage :

```bash
# Utiliser une IP source spécifique pour le scan
masscan 0.0.0.0/0 -p80 --rate 10000 --adapter-ip 192.168.1.50
```

### 4. Sécurité et Éthique : `--excludefile`
En Red Team, ne pas scanner les infrastructures critiques ou hors-périmètre est vital. Utilise toujours un fichier d'exclusion.

```bash
# Exclure les plages IP sensibles (gouvernement, DoD, etc.)
masscan 0.0.0.0/0 -p80 --excludefile exclude.txt
```

### 5. Capture de Bannières : `--banners`
Masscan ne se contente pas de dire si un port est ouvert. Il peut interagir avec le service pour récupérer des informations (bannières). Note qu'il utilise sa propre pile TCP/IP pour cela.

```bash
# Capture de bannières avec un temps d'attente (wait) pour les réponses
masscan 192.168.1.0/24 -p80,443,22 --banners --wait 10
```
*Le paramètre `--wait` est crucial ici pour laisser le temps aux connexions TCP de s'établir après le SYN initial.*

### 6. Gestion des Sorties (Outputs)
Pour intégrer Masscan dans ton pipeline HexStrike, le format de sortie est essentiel :

*   **-oX (XML) :** Idéal pour l'import dans d'autres outils.
*   **-oJ (JSON) :** Le meilleur pour le post-traitement (Python, jq).
*   **-oL (List) :** Simple liste d'IP/Ports.
*   **-oG (Grepable) :** Pour les fans de la ligne de commande.

```bash
# Export en JSON pour analyse ultérieure
masscan 172.16.0.0/16 -p1-1024 --rate 5000 -oJ results.json
```

---

### Le Pack Expert : La Commande "Full Recon"
Voici la commande que j'utilise pour une reconnaissance rapide et exhaustive sur un large périmètre :

```bash
masscan -iL cibles.txt -p1-65535 --rate 50000 --banners --wait 5 -oX scan_complet.xml --excludefile hors_pente.txt
```

### ⚠️ Avertissements de l'Expert
1.  **Traffic Shaping :** Ton ISP peut limiter ton trafic s'il détecte un pic massif de paquets SYN. Utilise `--rate` avec discernement.
2.  **IP Stack :** Masscan utilise sa propre pile TCP. Si tu scannes ton propre réseau local, ton OS peut envoyer des paquets RST pour fermer les connexions que Masscan essaie d'ouvrir. Utilise des règles `iptables` pour bloquer les RST sortants si nécessaire.
3.  **Légalité :** Un scan à 10M pps ressemble à s'y méprendre à une attaque DoS. Assure-toi d'avoir l'autorisation écrite (ROE) avant d'allumer les moteurs.

Besoin d'approfondir une option spécifique ou de parser les résultats JSON ? Je suis là.

#### 📋 Quick Commands

`masscan -p80,443 0.0.0.0/0 --rate 10000``masscan --banners`