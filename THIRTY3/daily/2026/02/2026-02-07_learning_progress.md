---
date: 2026-02-07
type: learning-progress
phase: [2]
tags: [learning, phase-2, development, security, hacking]
status: active
source: REPORT/Février
---

## Contexte

L'utilisateur dispose d'un script bash de base GHOST-PROTOCOL qui réalise l'usurpation de MAC, la randomisation de noms d'hôtes et l'effacement de l'historique bash. La demande consiste à l'améliorer. Le champ d'application a été réduit à **l'anonymisation du réseau** - renforcement défensif de la vie privée pour la recherche de sécurité autorisée sur Kali Linux.

Aucun script ghost-protocol ou répertoire `scripts/` n'existe actuellement dans le projet HexStrike AI.

## Scope - Ce que nous construisons

Un script bash autonome axé sur le **renforcement de la confidentialité des réseaux** :

1. **Confidentialité DNS** - Passez à des résolveurs DNS axés sur la confidentialité (Quad9, Cloudflare, etc.), sauvegardez/restaurez la configuration d'origine.
2. **IPv6 Leak Prevention** - Désactivez IPv6 pour prévenir les fuites, avec restauration
3. **ARP Cache Flush** - Effacez la table ARP du noyau
4. **DNS Cache Flush** - Efface le cache résolu par le système
5. **Vérification de l'état du proxy/SOCKS** - Détecte et signale les variables d'environnement du proxy.
6. **Test de fuite DNS** - Vérification simple par rapport à un point d'extrémité connu
7. **Durcissement de l'empreinte TCP** - Ajustez le TTL et la taille de la fenêtre TCP via sysctl afin de masquer l'empreinte du système d'exploitation.
8. **MAC Spoofing** (conservé de l'original) - Amélioré avec des préfixes spécifiques aux fournisseurs (Apple, Dell, etc.)
9. **Hostname Randomization** (conservé de l'original) - Amélioré avec des modèles contextuels (style Windows, style Mac)

**Non inclus** : Destruction des logs, timestomping, suppression par déchiquetage, persistance/cron, services systemd.

## Fichiers à créer

|Fichier|Description|
|---|---|
|scripts/ghost-protocol.sh`|Script principal amélioré (~400-500 lignes)

## Fichiers à modifier

|Fichier|Changement|
|---|---|
|Ajouter `macchanger` à la liste d'installation d'apt-get, COPIER le répertoire `scripts/`.

## Architecture des scripts

**Shell Snippet**
```
scripts/ghost-protocol.sh (~450 lignes)

 ┌─ SECTION 1 : Shebang, mode strict, constantes
 ├─ SECTION 2 : Palette de couleurs (thème ANSI HexStrike)
 ├─ SECTION 3 : Fonctions d'affichage (bannière, print_status, print_success, etc.)
 ├─ SECTION 4 : Fonctions utilitaires (check_root, check_deps, detect_interface, safe_exec)
 ├─ SECTION 5 : Gestion des états (save_state, load_state - JSON via python3 one-liners)
 ├─ SECTION 6 : MAC spoofing (vendor prefixes, generate, spoof, restore)
 ├─ SECTION 7 : Usurpation de nom d'hôte (motifs, générer, usurper, restaurer)
 ├─ SECTION 8 : Anonymisation du réseau (DNS, IPv6, ARP, empreinte digitale, test de fuite)
 ├─ SECTION 9 : Restauration (restore_all from saved state)
 ├─ SECTION 10 : Analyse des arguments (case/shift pour les options longues)
 └─ SECTION 11 : Menu d'aide + envoi principal
```




**Links:**
- [Create command](<HACKERGPT/HEXSTRIKE/Outils/Nmap/Create command.md>)
- [Commande](<HACKERGPT/HEXSTRIKE/Outils/Trivy/Commande.md>)
- [reconnaissance historique](<HACKERGPT/HEXSTRIKE/Outils/Waybackcurls/reconnaissance historique.md>)
- [La structure d'un site web expliquée](<Notes et Mémos Importants/Notes rapide/HTML/La structure d'un site web expliquée.md>)
- [Explication étape par étape](<HACKERGPT/HEXSTRIKE/Outils/Dalfox/Explication étape par étape.md>)

## Interface CLI

```
ghost-protocol.sh [MODE] [OPTIONS]

Modes :
  --full Exécute tout : MAC spoof + nom d'hôte + anonymisation du réseau
  --spoof Usurpation de MAC + nom d'hôte uniquement
  --anonymize Anonymisation du réseau uniquement (DNS, IPv6, ARP, empreinte)
  --restore Rétablir tous les changements à l'état pré-fantôme
  --status Affiche l'état actuel de la machine fantôme
  --help Affiche l'aide

Options :
  --interface <iface> Interface réseau (par défaut : détection automatique)
  --vendor <nom> Préfixe du fournisseur MAC : apple, dell, lenovo, samsung, hp, random
  --dry-run Prévisualisation des actions sans les exécuter
  --verbose Sortie détaillée
  --quiet Suppression de la sortie de non-erreur
  --no-confirm Ignorer les demandes de confirmation
```

## Détails de l'implémentation

### Fichier d'état (`$HOME/.ghost-protocol/state.json`)

json

```json
{
  "timestamp" : "2026-02-07T12:00:00Z",
  "original_mac" : "aa:bb:cc:dd:ee:ff",
  "original_hostname" : "kali",
  "original_dns" : "nameserver 8.8.8.8",
  "original_ipv6" : "0",
  "interface" : "eth0"
}
```

Lecture/écriture JSON via `python3 -c` (garanti disponible dans Kali).

### Préfixes MAC des vendeurs (tableau associatif)

bash

```bash
declare -A VENDOR_PREFIXES=(
  ["apple"]="00:CD:FE" ["dell"]="00:14:22" ["lenovo"]="00:06:1B"
  ["samsung"]="00:07:AB" ["hp"]="00:1E:0B" ["microsoft"]="00:50:F2"
)
```

### Résolveurs de confidentialité DNS

bash

````bash
PRIVACY_DNS=("9.9.9.9" "149.112.112.112" # Quad9
             "1.1.1.1" "1.0.0.1") # Cloudflare
```

### Modèles de sécurité
- `safe_exec()` - enveloppe chaque commande système, respecte `--dry-run`, enregistre les actions
- `confirm_action()` - invite colorée Y/n, ignorée avec `--no-confirm`
- `check_root()` - quitte immédiatement si l'utilisateur n'est pas root
- `check_dependencies()` - vérifie que macchanger, ip, python3 sont disponibles ; repli gracieux si macchanger est absent (utiliser `ip link set`)
- Détection Docker via `/.dockerenv` - sauter les opérations qui nécessitent un accès au niveau de l'hôte
- Trap on EXIT/SIGINT/SIGTERM - imprime les instructions de restauration si l'exécution est interrompue à mi-parcours
- Détection des liens symboliques `/etc/resolv.conf` - gérer les fichiers résolus par le système par rapport aux fichiers directs

### Flux d'exécution : `--full`
```
1. check_root → check_deps → detect_interface
2. save_state (backup MAC, hostname, DNS, IPv6)
3. MAC spoof (fournisseur ou aléatoire)
4. Nom d'hôte aléatoire
5. DNS → résolveurs de confidentialité
6. Désactivation de l'IPv6
7. Vidage du cache ARP
8. Vider le cache DNS
9. Durcissement de l'empreinte TCP (TTL, taille de la fenêtre)
10. Résumé de l'état
```

### Flux d'exécution : `--restore`
```
1. load_state → fail s'il n'y a pas d'état sauvegardé
2. Restore original MAC
3. Restore original hostname
4. Restaurer le DNS d'origine (/etc/resolv.conf)
5. Restaurez l'IPv6
6. Effacez le fichier d'état
````

## Dockerfile Change

Ligne 34-67 de `Dockerfile` - ajoutez `macchanger` à la liste d'installation d'apt-get :

diff

``diff
     wafw00f \N- + macchanger \N
+ macchanger \N- && apt-get clean \N
     && apt-get clean \N
```

Ligne 82 - ajoutez COPY pour les scripts :

diff

```diff
 COPY hexstrike_server.py hexstrike_mcp.py tasks.py ./
+COPY scripts/ ./scripts/
+RUN chmod +x ./scripts/*.sh
```

## Vérification

1. **Vérification de la syntaxe** : `bash -n scripts/ghost-protocol.sh`
2. **Menu d'aide** : `sudo bash scripts/ghost-protocol.sh --help`
3. **Exécution à sec complète** : `sudo bash scripts/ghost-protocol.sh --full --dry-run` - devrait afficher toutes les actions planifiées sans les exécuter.
4. **Status** : `sudo bash scripts/ghost-protocol.sh --status` - montre l'état actuel du MAC, du nom d'hôte, du DNS et de l'IPv6.
5. **Construction du docker** : `docker build -t hexstrike-ai:full -f Dockerfile .` - vérifie qu'il n'y a pas d'erreur de construction