Si Nmap est un scalpel chirurgical, **Masscan** est un fusil à pompe à dispersion : c'est l'outil de reconnaissance de masse par excellence. Sa force réside dans son architecture **asynchrone**, lui permettant d'atteindre des vitesses théoriques de 10 millions de paquets par seconde (10M pps), ce qui permet de scanner l'Internet entier en moins de 6 minutes.

Voici l'explication technique détaillée et les commandes pour maîtriser ce monstre de performance.

---

### 1. L'Architecture Asynchrone
Contrairement aux scanners classiques qui attendent une réponse avant d'envoyer le paquet suivant (synchrone), Masscan envoie des paquets de manière continue et traite les réponses entrantes de façon indépendante. Il utilise sa propre pile TCP/IP pour outrepasser les limitations du noyau de l'OS.

### 2. Commande Maîtresse : Scan de Large Envergure
Voici une commande type pour scanner un réseau `/16` sur les ports web les plus communs avec une capture de bannières :

```bash
sudo masscan 192.168.0.0/16 -p80,443,8080 \
    --rate 100000 \
    --banners \
    --excludefile exclude.txt \
    --adapter-ip 192.168.1.50 \
    --wait 10 \
    -oJ results.json
```

### 3. Analyse Technique des Options

#### A. La Vitesse (`--rate`)
C'est le paramètre le plus critique. 
- `--rate 100000` : Envoie 100 000 paquets par seconde. 
- **Expert Tip :** Pour atteindre 1M ou 10M pps, tu auras besoin de pilotes spécifiques comme **PF_RING**. Attention : un `rate` trop élevé sur une connexion instable causera des faux négatifs (paquets perdus).

#### B. Capture de Bannières (`--banners`)
Par défaut, Masscan ne fait qu'un "SYN scan" (port ouvert/fermé). Avec `--banners`, il complète le handshake TCP pour récupérer les informations d'identification du service (ex: version du serveur Apache, type de SSH).
- **Note :** Cela ralentit le scan car cela nécessite une gestion d'état TCP.

#### C. Gestion des Cibles (`--excludefile`)
En Red Team, il est vital de ne pas toucher à certains segments (systèmes critiques, honeypots connus, IP gouvernementales). 
- Utilise `--excludefile exclude.txt` pour ignorer les ranges IP listés dans ce fichier.

#### D. Configuration Réseau (`--adapter-ip`)
Masscan utilise son propre stack. Pour recevoir les réponses, il a parfois besoin que tu spécifies l'IP de ton interface réseau avec `--adapter-ip`. Cela permet aussi de faire du "source IP spoofing" dans certains contextes d'audit de pare-feu.

#### E. Le Délai de Finition (`--wait`)
Puisque le scan est asynchrone, des paquets de réponse peuvent arriver après que le dernier paquet d'envoi a été expédié. `--wait 10` dit à Masscan d'attendre 10 secondes supplémentaires avant de s'arrêter pour capturer les réponses tardives.

### 4. Formats de Sortie (Output)
Le post-traitement est essentiel dans HexStrike. Masscan propose plusieurs formats :
- `-oL <file>` : Liste simple (List format).
- `-oX <file>` : Format XML (idéal pour l'import dans d'autres outils).
- `-oG <file>` : Format Grepable (pour les fans de `awk` et `sed`).
- `-oJ <file>` : **Format JSON** (Recommandé pour l'intégration Python/NoSQL).

### 5. Défense et Limitations
*   **Traffic Shaping / Rate Limiting :** Si tu scannes trop vite, les IPS/IDS cibles (ou même ton propre FAI) vont te blacklister ou "dropper" tes paquets. 
*   **Blackholing :** Un scan trop agressif peut saturer la table d'état de ton propre routeur, provoquant un déni de service local. Surveille toujours ton infrastructure.

---

**Conseil d'HackerGPT :** 
Commence toujours par un `--rate 1000` pour tester la stabilité du lien, puis augmente progressivement. N'oublie pas : la vitesse est inutile si la précision est sacrifiée.

Besoin d'une commande spécifique pour un scénario d'évasion d'IDS ou une intégration avec un script Python ? Je suis là.

#### 📋 Quick Commands

`masscan -p80,443 0.0.0.0/0 --rate 10000``masscan --banners`