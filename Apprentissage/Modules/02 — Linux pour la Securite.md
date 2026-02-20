# Module 02 — Linux pour la Sécurité

**Phase :** 0 — Fondations
**Durée estimée :** 1–2 semaines
**Prérequis :** [[01 — Fondamentaux Reseaux TCP-IP]]

---

## Pourquoi Linux ?

Kali Linux, REMnux, Parrot OS — tous les outils de cybersécurité sont sur Linux.
Les serveurs cibles tournent à 80% sur Linux.
La ligne de commande est ta interface principale.
Maîtriser Linux = maîtriser ton environnement de travail.

---

## Commandes Essentielles

### Navigation et Fichiers
```bash
pwd               # Où suis-je ?
ls -la            # Lister les fichiers (avec cachés et permissions)
cd /chemin        # Changer de répertoire
cd ~              # Aller dans le home
cd ..             # Remonter d'un niveau

# Créer, copier, déplacer, supprimer
mkdir dossier           # Créer un dossier
touch fichier.txt       # Créer un fichier vide
cp source dest          # Copier
mv source dest          # Déplacer / renommer
rm fichier.txt          # Supprimer un fichier
rm -rf dossier/         # Supprimer un dossier (avec tout son contenu — attention!)

# Lire et éditer
cat fichier.txt         # Afficher le contenu
less fichier.txt        # Afficher page par page (q pour quitter)
nano fichier.txt        # Éditeur simple
vim fichier.txt         # Éditeur puissant (i pour insérer, :wq pour sauvegarder)
```

### Recherche
```bash
# Chercher un fichier
find / -name "passwd" 2>/dev/null
find /home -name "*.txt" -size +1k

# Chercher dans un fichier
grep "erreur" fichier.log
grep -r "password" /etc/    # Recherche récursive
grep -i "admin" fichier.txt # Insensible à la casse

# Combiner les commandes (pipe)
cat /etc/passwd | grep "bash"
ls -la | grep ".conf"
```

### Permissions
```bash
# Format des permissions
# -rwxr-xr--  1  user  group  size  date  nom
#  |||||||
#  |||||||  --- Autres (r--)
#  ||||--- Groupe (r-x)
#  |--- Propriétaire (rwx)
#  --- Type (- = fichier, d = dossier, l = lien)

# Changer les permissions
chmod 755 script.sh      # rwxr-xr-x
chmod +x script.sh       # Ajouter l'exécution
chmod 600 id_rsa         # Clé SSH — lecture propriétaire seulement

# Changer le propriétaire
chown user:group fichier
sudo chown root:root /etc/important

# Voir les permissions
ls -la fichier
stat fichier
```

### Processus et Services
```bash
# Voir les processus
ps aux                   # Tous les processus
ps aux | grep python     # Filtrer
top / htop               # Vue temps réel

# Tuer un processus
kill PID
kill -9 PID              # Force kill
pkill -f "nom_programme"

# Services (systemd)
systemctl start service    # Démarrer
systemctl stop service     # Arrêter
systemctl status service   # Voir le statut
systemctl enable service   # Activer au démarrage

# Réseau
netstat -tulnp           # Ports écoutés
ss -tulnp               # Alternative moderne
```

### Gestion des Paquets (Kali/Ubuntu/Debian)
```bash
# APT (Debian/Ubuntu/Kali)
sudo apt update                    # Mettre à jour la liste
sudo apt upgrade                   # Mettre à jour les paquets
sudo apt install nom-paquet        # Installer
sudo apt remove nom-paquet         # Désinstaller
sudo apt search mot-clé            # Chercher un paquet

# pip (Python)
pip install theHarvester
pip3 install requests

# Go
go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
```

---

## Scripting Bash de Base

```bash
#!/bin/bash
# Mon premier script de recon

TARGET=$1   # Premier argument passé au script

if [ -z "$TARGET" ]; then
    echo "Usage: $0 <domain>"
    exit 1
fi

echo "=== Recon sur $TARGET ==="

echo "[*] WHOIS..."
whois $TARGET | grep -i "registrant\|name\|email" | head -10

echo "[*] DNS..."
dig $TARGET A +short
dig $TARGET MX +short

echo "[*] Sous-domaines rapides..."
subfinder -d $TARGET -silent | head -20

echo "[+] Recon terminée"
```

```bash
# Rendre le script exécutable
chmod +x recon.sh

# Exécuter
./recon.sh target.com
```

---

## Fichiers Importants en Linux (pour la cybersécurité)

```bash
# Utilisateurs et authentification
/etc/passwd        # Liste des utilisateurs (pas les mots de passe)
/etc/shadow        # Hashes des mots de passe (root seulement)
/etc/group         # Groupes

# Configuration réseau
/etc/hosts         # Résolution DNS locale
/etc/resolv.conf   # Serveurs DNS configurés
/etc/network/interfaces  # Config réseau (Debian)

# Logs (précieux pour la forensique)
/var/log/auth.log  # Authentifications
/var/log/syslog    # Logs système généraux
/var/log/apache2/  # Logs Apache
/var/log/nginx/    # Logs Nginx

# Crontabs (persistance de processus)
/etc/crontab
/etc/cron.d/
crontab -l         # Voir les tâches planifiées de l'utilisateur courant
```

---

## Setup Kali Linux

```bash
# Télécharger Kali : kali.org/get-kali
# Installer en VM (VirtualBox ou VMware recommandé)

# Premier démarrage — mise à jour
sudo apt update && sudo apt full-upgrade -y
sudo apt install -y kali-linux-everything  # Tous les outils (optionnel, ~15GB)

# Outils essentiels si pas déjà installés
sudo apt install -y \
    nmap \
    nikto \
    gobuster \
    hydra \
    sqlmap \
    wireshark \
    burpsuite \
    metasploit-framework \
    theHarvester \
    maltego \
    exiftool

# Configuration Metasploit (première fois)
sudo msfdb init
msfconsole
```

---

## Exercices Pratiques

```bash
# Exercice 1 — Exploration du système
find / -name "*.conf" 2>/dev/null | head -20
cat /etc/passwd | cut -d: -f1  # Lister les utilisateurs

# Exercice 2 — Scripting
# Créer un script qui prend un domaine en paramètre
# et exécute whois + dig + theHarvester
# Sauvegarder les résultats dans un fichier daté

# Exercice 3 — Kali
# Installer Kali en VM
# Faire un nmap sur 127.0.0.1
# Faire un nmap sur le réseau local (192.168.x.0/24)
# Ouvrir Burp Suite et configurer le proxy
```

---

## Ressources

| Ressource | Lien | Gratuit |
|-----------|------|---------|
| TryHackMe — Linux Fundamentals (1,2,3) | tryhackme.com | Oui |
| OverTheWire — Bandit | overthewire.org/wargames/bandit | Oui |
| Kali Linux Revealed (livre officiel) | kali.org/docs | Oui |
| Explainshell.com | explainshell.com | Oui |

---

## Checklist de Validation

- [ ] Je navigue dans le filesystem sans me perdre
- [ ] Je comprends les permissions Unix (rwx)
- [ ] Je peux installer des outils avec apt et pip
- [ ] Je peux écrire un script bash simple
- [ ] J'ai installé Kali Linux en VM
- [ ] Je sais utiliser grep, find, et les pipes
- [ ] Je connais les fichiers système importants

**Quand toutes les cases sont cochées → Module 02 : Complété**

---

*Module 02 — Parcours HexStrike | Retour vers [[Parcours HexStrike]]*
