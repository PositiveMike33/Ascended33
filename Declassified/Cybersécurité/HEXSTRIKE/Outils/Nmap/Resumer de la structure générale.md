La vidéo est un guide complet d’environ 1 h 24 sur **Nmap**, qui part des bases jusqu’aux usages avancés sur Kali Linux et autres systèmes.[[youtube](https://www.youtube.com/watch?v=JHAMj2vN2oU)]​

## Structure générale

- Présentation de Nmap, de son histoire, de la famille d’outils associée (Ncrack, Ncat, Nping, Zenmap, NSE) et des avertissements légaux/éthiques sur le scanning non autorisé.[[youtube](https://www.youtube.com/watch?v=JHAMj2vN2oU)]​
    
- Installation de Nmap depuis le code source sur Kali (dépendances, compilation, résolution d’erreurs), mention des paquets précompilés Windows et Linux et de la branche expérimentale `nmap-exp`.[[youtube](https://www.youtube.com/watch?v=JHAMj2vN2oU)]​
    
- Parcours progressif: Nmap basique, gestion de cibles (IP, ranges, CIDR, fichiers de cibles, exclusions, choix d’interface, IPv6, cibles aléatoires).[[youtube](https://www.youtube.com/watch?v=JHAMj2vN2oU)]​
    

## Scans et options de base

- États de ports (open, closed, filtered, unfiltered, open|filtered, closed|filtered) et option `--reason` pour comprendre pourquoi un port est dans un état donné.[[youtube](https://www.youtube.com/watch?v=JHAMj2vN2oU)]​
    
- Scans simples: `nmap <target>`, scan de plusieurs hôtes, sous-réseaux (`/CIDR`), plages d’IP, fichiers de cibles (`-iL`), exclusions (`--exclude`, `--excludefile`).[[youtube](https://www.youtube.com/watch?v=JHAMj2vN2oU)]​
    
- Options de découverte (ping): `-Pn` (pas de ping), `-sn` (ping sweep), ARP scan local, TCP SYN ping (`-PS`), ACK ping (`-PA`), UDP ping (`-PU`), SCTP, ICMP echo (`-PE`), timestamp (`-PP`), address mask (`-PM`), IP protocol ping (`-PO`), ARP (`-PR`).[[youtube](https://www.youtube.com/watch?v=JHAMj2vN2oU)]​
    

## Port scanning et techniques avancées

- Focalisation sur les ports: `-F` (top 100), `-p` (ports précis, ranges, noms, wildcard `"*"` pour tous les 65535 ports), combinaison TCP/UDP (`-sU`/`-sT`/`-sS` avec `-p`).[[youtube](https://www.youtube.com/watch?v=JHAMj2vN2oU)]​
    
- Types de scan:
    
    - TCP SYN (`-sS`), connect (`-sT`), UDP (`-sU`).[[youtube](https://www.youtube.com/watch?v=JHAMj2vN2oU)]​
        
    - Scans “stealth”: NULL (`-sN`), FIN (`-sF`), Xmas (`-sX`).[[youtube](https://www.youtube.com/watch?v=JHAMj2vN2oU)]​
        
    - ACK scan (`-sA`) pour distinguer filtré / non filtré.[[youtube](https://www.youtube.com/watch?v=JHAMj2vN2oU)]​
        
    - Scan de protocoles IP (`-sO`), scan avec flags personnalisés (`--scanflags`).[[youtube](https://www.youtube.com/watch?v=JHAMj2vN2oU)]​
        
- Contrôle de l’ordre: scan séquentiel (`-r`), randomisation des hôtes (`--randomize-hosts`).[[youtube](https://www.youtube.com/watch?v=JHAMj2vN2oU)]​
    

## Détection d’OS, de services et DNS

- Détection de l’OS avec `-O`, options `--osscan-limit` et `--osscan-guess`/`--fuzzy` pour forcer les guesses.[[youtube](https://www.youtube.com/watch?v=JHAMj2vN2oU)]​
    
- Détection de versions de services `-sV` et `--version-trace` pour voir le détail du fingerprinting applicatif.[[youtube](https://www.youtube.com/watch?v=JHAMj2vN2oU)]​
    
- Gestion DNS: `-n` (pas de reverse DNS), `-R` (reverse forcé), `--system-dns`, `--dns-servers <srv1,srv2>` pour contrôler les résolveurs.[[youtube](https://www.youtube.com/watch?v=JHAMj2vN2oU)]​
    

## Timing, performance et fiabilité

- Templates de timing `-T0` à `-T5` (paranoïaque à insensé) avec exemples d’adaptation selon réseau rapide/lent.[[youtube](https://www.youtube.com/watch?v=JHAMj2vN2oU)]​
    
- Contrôles fins:
    
    - Parallélisme de ports `--min-parallelism` / `--max-parallelism`.[[youtube](https://www.youtube.com/watch?v=JHAMj2vN2oU)]​
        
    - Groupes d’hôtes `--min-hostgroup` / `--max-hostgroup`.[[youtube](https://www.youtube.com/watch?v=JHAMj2vN2oU)]​
        
    - RTT: `--initial-rtt-timeout`, `--max-rtt-timeout`.[[youtube](https://www.youtube.com/watch?v=JHAMj2vN2oU)]​
        
    - `--max-retries`, `--host-timeout`, `--scan-delay`, `--max-scan-delay`, `--min-rate`, `--max-rate`, `--ttl` pour adapter vitesse, discrétion et précision.[[youtube](https://www.youtube.com/watch?v=JHAMj2vN2oU)]​
        

## Contournement de firewalls et évasion

- Fragmentation et MTU personnalisé (`--mtu`), envoi en raw Ethernet (`--send-eth`) ou en IP (`--send-ip`).[[youtube](https://www.youtube.com/watch?v=JHAMj2vN2oU)]​
    
- Décoys (`-D` avec IPs ou `RND`) pour diluer l’origine réelle du scan.[[youtube](https://www.youtube.com/watch?v=JHAMj2vN2oU)]​
    
- Idle/zombie scan (`-sI`) en utilisant un hôte tiers avec IP ID prédictible.[[youtube](https://www.youtube.com/watch?v=JHAMj2vN2oU)]​
    
- `--source-port` / `-g` pour forcer le port source (20, 53, 67, etc.), `--data-length` pour ajouter des données et casser les signatures, `--spoof-mac`, `--badsum` pour checksums incorrects.[[youtube](https://www.youtube.com/watch?v=JHAMj2vN2oU)]​
    

## Nmap Scripting Engine (NSE)

- Présentation de NSE: scripts en Lua pour vulnérabilité, découverte, whois, géoloc, etc., avec dépôt officiel des scripts.[[youtube](https://www.youtube.com/watch?v=JHAMj2vN2oU)]​
    
- Utilisation basique: `--script <nom>` sur une cible, exemple avec scripts `whois-*` combinés à `-sn`.[[youtube](https://www.youtube.com/watch?v=JHAMj2vN2oU)]​
    
- Exemple de script `traceroute-geolocation` pour traceroute + géolocalisation, output KML pour visualisation dans Google Maps/Earth, et recommandation d’explorer la bibliothèque de scripts NSE sur le site Nmap.[[youtube](https://www.youtube.com/watch?v=JHAMj2vN2oU)]​
    

## Sortie et Zenmap

- Options de sortie: `-oN` (texte normal), `-oX` (XML), `-oG` (grepable), `-oA` (tous formats à la fois), ainsi que `--stats-every` pour afficher périodiquement les stats pendant un long scan.[[youtube](https://www.youtube.com/watch?v=JHAMj2vN2oU)]​
    
- Présentation de Zenmap comme GUI multi‑plateforme pour composer, sauvegarder et rejouer des commandes Nmap visuellement, utile sous Windows, macOS et Linux.[[youtube](https://www.youtube.com/watch?v=JHAMj2vN2oU)]​
    

En résumé, la vidéo est une “masterclass” qui couvre l’installation, les scans basiques et avancés, le tuning de performance, les techniques d’évasion, NSE et les options d’output, avec un fort accent sur l’usage responsable et légal de Nmap.[[youtube](https://www.youtube.com/watch?v=JHAMj2vN2oU)]​