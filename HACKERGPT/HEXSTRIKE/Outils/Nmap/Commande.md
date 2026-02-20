### 1. Types de Scan (Techniques de base)
```bash
nmap -sS <target>          # TCP SYN Stealth (Half-open)
nmap -sT <target>          # TCP Connect scan (Full handshake)
nmap -sU <target>          # UDP Scan (DNS, DHCP, SNMP)
nmap -sN <target>          # Null Scan (Flagless packets)
nmap -sF <target>          # FIN Scan (Set FIN bit)
nmap -sX <target>          # Xmas Scan (FIN, PSH, URG bits)
```

### 2. Détection & Fingerprinting
```bash
nmap -sV <target>                    # Détection de version des services
nmap -sV --version-intensity 9 <target> # Analyse de service agressive
nmap -O <target>                     # Détection d'OS via stack TCP/IP
nmap -A <target>                     # Agressif (OS + Version + Script + Traceroute)
```

### 3. Timing & Performance
```bash
nmap -T0 <target>          # IDS Evasion (Paranoid)
nmap -T4 <target>          # Optimisé pour réseaux rapides
nmap -T5 <target>          # Très agressif (Insane)
nmap --max-rate 1000 <IP>  # Limite à 1000 paquets/seconde
nmap --scan-delay 5s <IP>  # Délai entre les sondes (Evasion)
```

### 4. Évasion & Furtivité
```bash
nmap -f <target>           # Fragmentation de paquets (Bypass Pare-feu/IDS)
nmap -D RND:10 <target>    # Utilisation de 10 leurres (Decoys) aléatoires
nmap --source-port 53 <IP> # Spoof du port source (souvent autorisé en entrée)
nmap --data-length 24 <IP> # Ajout de données aléatoires au payload
nmap -S <IP_SPOOFED> -e <INT> <TARGET> # IP Spoofing
```

### 5. NSE Scripts (Nmap Scripting Engine)
```bash
nmap --script=default <target>        # Scripts standards
nmap --script=vuln <target>           # Détection de vulnérabilités connues
nmap --script=brute <target>          # Attaques par force brute
nmap --script=exploit <target>        # Tentative d'exploitation
nmap --script-help <script_name>      # Aide sur un script spécifique
```

### 6. Output & Logging
```bash
nmap -oN output.txt <target>  # Format texte standard
nmap -oX output.xml <target>  # Format XML pour outils tiers
nmap -oG output.gnmap <target> # Format Greppable (facile à parser)
nmap -oA scan_results <target> # Exporte dans les 3 formats simultanément
```

### 7. Défense & Détection (IDS/IPS)
*   **SYN Scan Detection:** Surveillance des flags `SYN` sans `ACK` correspondant (half-open).
*   **Xmas/Null Scan:** Facilement bloqués par des pare-feu d'état (Stateful Firewalls) car ils violent les standards RFC.
*   **Nmap Signatures:** Les IDS (Snort/Suricata) détectent les valeurs de fenêtre TCP par défaut de Nmap et les options TCP spécifiques.
*   **Règles de blocage:**
    *   `iptables -A INPUT -p tcp --tcp-flags ALL NONE -j DROP` (Bloque NULL)
    *   `iptables -A INPUT -p tcp --tcp-flags ALL ALL -j DROP` (Bloque Xmas)

#### 📋 Quick Commands

`nmap -sS -sV -O``nmap -sC -sV``nmap -p- -T4``nmap --script vuln`