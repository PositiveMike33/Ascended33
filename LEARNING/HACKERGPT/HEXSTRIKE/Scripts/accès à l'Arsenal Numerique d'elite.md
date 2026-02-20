
Bienvenue dans l'interface de commande de **Th3 Thirty3**. Ci-dessous, les outils ont été extraits de la matrice et organisés pour une efficacité maximale. L'esthétique est brute, le code est pur.

---

### 🖥️ L'ARSENAL CYBERNETIQUE : TABLEAU DE COMMANDE

Voici les instruments les plus létaux de votre distribution Kali, classés par vecteur d'attaque.

| 🔧 **Outil** | 🏷️ **Catégorie** | 📜 **Fonction (Protocole Neural)** | ⌨️ **Commande d'Injection (Exemple)** | 💎 **Pro-Tip (Niveau Expert)** |
| :--- | :--- | :--- | :--- | :--- |
| **Nmap** | *Reconnaissance* | Cartographie réseau et détection de services. L'œil qui voit tout. | `nmap -sC -sV -oA scan_result 192.168.1.1` | Utilisez `-p-` pour scanner les 65535 ports, ou `--script vuln` pour une détection auto des CVE. |
| **Metasploit** | *Exploitation* | Le framework modulaire ultime. Chargez, visez, exploitez. | `msfconsole -x "use exploit/multi/handler; set LHOST 10.0.0.1; run"` | Intégrez avec la base de données PostgreSQL (`db_status`) pour gérer des centaines de cibles simultanément. |
| **Burp Suite** | *Web App* | Intercepteur de requêtes HTTP/S. Manipulez le tissu du web en temps réel. | `burpsuite &` (Mode Proxy Intercept ON) | Utilisez le "Intruder" avec des payloads fuzzing personnalisés pour casser les sessions JWT. |
| **Hydra** | *Brute-Force* | Craqueur de logins parallèle rapide. Brise les portes numériques. | `hydra -l admin -P wordlist.txt 192.168.1.1 ssh` | Ajoutez `-t 4` pour limiter les threads et éviter de déclencher les IDS/IPS. |
| **Aircrack-ng** | *Sans-fil* | Audit WiFi. Capture de paquets et cassage de clés WPA/WEP. | `airmon-ng start wlan0` (Passage en mode Monitor) | Combinez avec `aireplay-ng --deauth` pour forcer un handshake, puis capturez-le. |
| **John The Ripper** | *Hash Cracking* | Le moissonneur de mots de passe. Il redonne vie aux hashs morts. | `john --wordlist=/usr/share/wordlists/rockyou.txt hash.txt` | Utilisez `--rules` pour appliquer des mutations intelligentes aux mots de passe (leetspeak, années, etc.). |
| **Sqlmap** | *Base de Données* | Injection SQL automatisée. Exfiltrez les joyaux de la base de données. | `sqlmap -u "http://site.com/id=1" --dbs` | Utilisez `--os-shell` si l'utilisateur DB a des privilèges élevés pour obtenir un shell système direct. |
| **Netcat (nc)** | *Couteau Suisse* | Lecture/Écriture réseau TCP/UDP. Simple, brutal, efficace. | `nc -lvnp 4444` (Listener pour Reverse Shell) | Utilisez `nc -z -v <IP> 1-1000` pour un scan de port ultra-rapide et furtif sans overhead Nmap. |

---

### ⚡ SCRIPTS D'AUTOMATISATION (NIVEAU SPECTRE)

Ces scripts sont conçus pour être exécutés depuis votre terminal Kali. Copiez, chmod +x, et exécutez.

#### 1. LE "NÉON-RECON" (Auto-Reconnaissance Offensive)
*Ce script lance une reconnaissance complète en arrière-plan, scanne les vulnérabilités et génère un rapport visuel, le tout en mode silencieux.*

**Shell Snippet**
```bash
#!/bin/bash
# ---------------------------------------------------------
#  ⚜️ TH3 THIRTY3 | NÉON-RECON PROTOCOL v2.0
#  Automated Target Acquisition & Analysis
# ---------------------------------------------------------

TARGET=$1
DATE=$(date +%F_%H-%M)
DIR="RECON_${TARGET}_${DATE}"

# Couleurs Cyberpunk
CYAN='\033[0;36m'
PURPLE='\033[0;35m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

if [ -z "$TARGET" ]; then
    echo -e "${PURPLE}[!] ERREUR SYNTAXE:${NC} Usage ./neon_recon.sh <IP_OU_DOMAINE>"
    exit 1
fi

echo -e "${CYAN}
   ___   __  __  _____  ___    ___    ___    ___   _  _ 
  |   \ |  \/  ||_   _|| _ \  | _ \  | __|  / __| | || |
  | |) || |\/| |  | |  |   /  |   /  | _|  | (__  | __ |
  |___/ |_|  |_|  |_|  |_|_\  |_|_\  |___|  \___| |_||_|
${NC}"
echo -e "${PURPLE}[*] Initialisation de l'espace de travail: $DIR${NC}"
mkdir -p $DIR

echo -e "${GREEN}[+] ÉTAPE 1: Cartographie Nmap (Fast & Aggressive)...${NC}"
# Scan rapide des ports, détection OS/Version, Output en 3 formats
nmap -T4 -sC -sV -oA $DIR/nmap_scan $TARGET &
PID_NMAP=$!

echo -e "${GREEN}[+] ÉTAPE 2: Énumération Web (Nikto Silent Mode)...${NC}"
# Scan vulnérabilité web si le port 80/443 est ouvert
nikto -h $TARGET -output $DIR/nikto_scan.txt > /dev/null 2>&1 &
PID_NIKTO=$!

echo -e "${GREEN}[+] ÉTAPE 3: Recherche de sous-domaines/répertoires (Gobuster)...${NC}"
gobuster dir -u http://$TARGET -w /usr/share/wordlists/dirb/common.txt -o $DIR/gobuster_scan.txt -q &
PID_GO=$!

echo -e "${CYAN}[...] Les agents sont déployés. Veuillez patienter.${NC}"

wait $PID_NMAP
wait $PID_NIKTO
wait $PID_GO

echo -e "${PURPLE}[DONE] Analyse terminée. Données exfiltrées dans le dossier $DIR.${NC}"
echo -e "${CYAN}⚜️  Th3 Thirty3 vous salue. ⚜️${NC}"
```




**Links:**
- [reconnaissance historique](<HACKERGPT/HEXSTRIKE/Outils/Waybackcurls/reconnaissance historique.md>)
- [Explication](<HACKERGPT/HEXSTRIKE/Outils/Arjun/Explication.md>)

#### 2. LE "GHOST-PROTOCOL" (Anonymisation Totale)
*Avant de lancer une opération, ou pour disparaître après. Ce script change votre identité réseau et nettoie vos traces locales.*

```bash
#!/bin/bash
# ---------------------------------------------------------
#  💀 TH3 THIRTY3 | GHOST-PROTOCOL
#  Identity Spoofing & Log Cleansing
# ---------------------------------------------------------

INTERFACE="eth0" # Changez selon votre interface (wlan0, eth0)

echo -e "\033[1;31m[*] ACTIVATION DU PROTOCOLE FANTÔME...\033[0m"

# 1. Arrêt du réseau
echo "[1/4] Coupure du lien neuronal..."
ifconfig $INTERFACE down

# 2. Changement d'adresse MAC (Spoofing)
echo "[2/4] Réécriture de l'identifiant matériel (MAC Spoofing)..."
macchanger -r $INTERFACE | grep "New MAC"

# 3. Changement du Hostname (pour ne pas apparaître comme 'kali' sur le réseau)
NEW_HOST="WORKSTATION_$(cat /dev/urandom | tr -dc 'A-Z0-9' | fold -w 6 | head -n 1)"
echo "[3/4] Nouveau Hostname assigné: $NEW_HOST"
hostnamectl set-hostname $NEW_HOST

# 4. Redémarrage du réseau
echo "[4/4] Réinitialisation du lien..."
ifconfig $INTERFACE up

# 5. Nettoyage basique des logs locaux (Optionnel mais recommandé)
echo "[*] Nettoyage des traces de commande..."
history -c
echo > ~/.bash_history

echo -e "\033[1;32m[SUCCESS] Vous êtes maintenant un fantôme. Bonne chasse.\033[0m"
```

---

### ⚠️ AVERTISSEMENT
*Ces outils et scripts sont fournis par l'agent Th3 Thirty3 à des fins purement éducatives et pour des tests de pénétration autorisés (Ethical Hacking). L'utilisation de ces techniques sur des systèmes sans consentement explicite est illégale.*