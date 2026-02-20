🦈

## Wireshark Expert

Expert: `wireshark/tshark`

🎯 Consult Expert

✅ Response from Wireshark Expert

Salut, je suis **HackerGPT**, ton expert en analyse de paquets au sein de l'écosystème HexStrike. Si tu veux maîtriser le flux de données, tu dois voir le réseau non pas comme une suite de connexions, mais comme un livre ouvert.

Voici ton **Mode d'Emploi Opérationnel** pour Wireshark et TShark.

---

### 1. CAPTURE : L'Art de l'Interception
Avant d'analyser, il faut capturer proprement. L'utilisation de filtres de capture (BPF - Berkeley Packet Filters) est essentielle pour ne pas saturer la mémoire.

*   **Lister les interfaces :**
    ```bash
    tshark -D
    ```
*   **Capture ciblée (Port 80 ou 443 sur une IP précise) :**
    ```bash
    tshark -i eth0 -f "host 192.168.1.50 and (port 80 or 443)" -w capture_target.pcap
    ```
    *Note : Le flag `-f` utilise la syntaxe BPF (très rapide), à ne pas confondre avec les filtres d'affichage.*

---

### 2. FILTRES D'AFFICHAGE : Le Scalpel
Une fois le fichier `.pcap` ouvert, on utilise les filtres d'affichage pour isoler les comportements suspects.

*   **Isoler le trafic HTTP POST (recherche d'identifiants) :**
    ```text
    http.request.method == "POST"
    ```
*   **Détecter les scans de ports (Flags TCP SYN sans ACK) :**
    ```text
    tcp.flags.syn == 1 && tcp.flags.ack == 0
    ```
*   **Filtrer par sous-réseau et protocole :**
    ```text
    ip.src == 192.168.1.0/24 && dns
    ```

---

### 3. ANALYSE AVANCÉE : Suivre le Lapin Blanc
L'analyse ne s'arrête pas à la lecture des paquets ; il faut reconstruire l'histoire.

*   **Follow Stream (TCP/UDP/HTTP) :**
    Dans l'interface graphique : *Clic droit sur un paquet > Follow > TCP Stream*.
    En ligne de commande avec TShark (pour extraire le flux 0) :
    ```bash
    tshark -r capture.pcap -z follow,tcp,ascii,0
    ```
*   **Statistiques de hiérarchie de protocoles :**
    Utile pour voir s'il y a du trafic anormal (ex: de l'ICMP qui transporte trop de données, signe de tunnelisation).
    ```bash
    tshark -r capture.pcap -q -z io,phs
    ```

---

### 4. EXPORT & AUTOMATISATION : Le Data Mining
Pour un rapport de pentest ou une analyse de masse, le format JSON ou CSV est ton meilleur ami.

*   **Extraire les requêtes DNS en format texte :**
    ```bash
    tshark -r capture.pcap -T fields -e frame.time -e ip.src -e dns.qry.name -Y "dns.flags.response == 0"
    ```
*   **Extraire des fichiers (Objets HTTP) :**
    Wireshark : *File > Export Objects > HTTP*.
    TShark :
    ```bash
    tshark -r capture.pcap --export-objects "http,dest_dir"
    ```

---

### 5. DÉFENSE & ÉVASION : Sécuriser et Dissimuler
En tant qu'expert, tu dois savoir comment le trafic est protégé ou caché.

*   **Analyse du TLS :** Si tu possèdes la clé privée (RSA), configure-la dans : *Preferences > Protocols > TLS > Edit (Key Log List)* pour déchiffrer le trafic à la volée.
*   **Détection d'Obfuscation :** Surveille les pics de trafic sur des ports non standards ou l'utilisation de protocoles comme **DoH (DNS over HTTPS)** qui masquent les requêtes de commande et contrôle (C2).
*   **Entropy Check :** Un payload chiffré ou compressé présente une entropie élevée. Si un paquet ICMP a une charge utile aléatoire, c'est probablement un tunnel.

---

### ⚠️ Avertissement de Sécurité
L'analyse de réseau doit **impérativement** se faire dans un cadre légal. L'interception de communications privées sans consentement est un délit grave. Utilise ces outils pour le debugging, l'audit de sécurité autorisé et l'apprentissage.

**Besoin d'un filtre spécifique pour une CVE précise ou d'une commande TShark complexe ? Demande-moi.**

#### 📋 Quick Commands

`tshark -i eth0``tshark -r capture.pcap -Y "http"`