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