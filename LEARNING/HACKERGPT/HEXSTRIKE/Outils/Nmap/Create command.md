✅ Response from Nmap Master

```json
{
    "action": "configure_tool",
    "tool": "nmap",
    "params": {
        "role": "expert_master",
        "mode": "cli_generation",
        "context": "waiting_for_target"
    },
    "reason": "Initialisation du module expert Nmap. En attente de la cible spécifique et des contraintes documentaires pour générer la commande exacte."
}
```

En tant qu'**Expert Nmap Master** au sein de HexStrike, j'ai analysé votre demande. Vous avez fourni le protocole de génération (le "système") mais pas la tâche spécifique ni la cible (le "contexte" est vide `{}`).

Pour démontrer ma maîtrise absolue et répondre à votre instruction finale ("commandes précises et explications techniques"), voici les **3 archétypes de commandes** que je génère pour des engagements professionnels, selon le niveau de discrétion et l'objectif.

### 1. L'Audit Complet (Infrastructure Mapping)
Cette commande est utilisée pour cartographier totalement une cible lorsqu'on a peu de contraintes de bruit (Whitebox/Greybox).

```bash
nmap -sS -sU -p T:1-65535,U:53,161,123 -sV -O --script="default,discovery,vuln" -T4 --min-rate 1000 -oA /tmp/hexstrike_full_audit <TARGET>
```

**Analyse Technique :**
*   `-sS` (TCP SYN) + `-sU` (UDP) : Scan hybride. Le SYN est rapide et furtif (demi-ouverture), l'UDP cible des services critiques souvent oubliés (DNS, SNMP, NTP).
*   `-p T:1-65535...` : Scan complet des ports TCP, et ciblage chirurgical des ports UDP courants pour gagner du temps.
*   `--script="default,discovery,vuln"` : Utilisation massive du moteur NSE pour la découverte, la versioning et les vulnérabilités connues (CVE).
*   `--min-rate 1000` : Force Nmap à envoyer au moins 1000 paquets/sec. Risqué pour la congestion, mais excellent pour la vitesse sur réseau stable.

### 2. Le Fantôme (Firewall/IDS Evasion)
Cette commande est conçue pour contourner les règles de filtrage simples et éviter la détection par les IDS basés sur des signatures de scan volumétriques.

```bash
nmap -sS -T2 -f -D RND:10 --source-port 53 --data-length 25 --randomize-hosts -n -oN /tmp/hexstrike_stealth <TARGET>
```

**Analyse Technique :**
*   `-T2` (Polite) : Ralentit le scan pour ne pas saturer les seuils de détection temporels.
*   `-f` (Fragment) : Fragmente les paquets IP, rendant difficile pour les pare-feu sans réassemblage de paquets de lire l'en-tête TCP.
*   `-D RND:10` (Decoy) : Masque votre IP parmi 10 adresses IP aléatoires. L'IDS verra 11 sources scanner simultanément.
*   `--source-port 53` : Impersonne le trafic DNS (souvent autorisé par les pare-feu mal configurés).
*   `--data-length 25` : Ajoute des données aléatoires pour modifier la taille par défaut des paquets Nmap (signature statique souvent bloquée).

### 3. L'Exploitant (Targeted Vulnerability)
Focalisé sur une vulnérabilité spécifique ou un service web, utilisant les scripts NSE avancés.

```bash
nmap -sV --script="http-enum,http-sql-injection,http-waf-detect" --script-args="http-useragent='Mozilla/5.0 (Windows NT 10.0; Win64; x64)'" -p 80,443,8080 -Pn -oX /tmp/hexstrike_web <TARGET>
```

**Analyse Technique :**
*   `-Pn` : Suppose que l'hôte est actif (saute le ping). Crucial si la cible bloque ICMP.
*   `--script-args` : Modifie le User-Agent pour ressembler à un navigateur légitime et éviter le blocage par WAF basique.
*   Script Selection : Ne charge que les scripts pertinents pour le web (énumération, SQLi, détection WAF) pour réduire le bruit et le temps de scan.

---

**INSTRUCTION :** Pour que je génère la commande CLI *unique et parfaite* selon votre prompt initial, veuillez me fournir :
1.  La **Cible** (IP, Plage ou Domaine).
2.  L'**Objectif** précis (ex: "Découverte rapide", "Scan complet silencieux", "Recherche de vulnérabilité SMB").


nmap -sS -sV -O
nmap -sC -sV
nmap -p- -T4
nmap --script vuln