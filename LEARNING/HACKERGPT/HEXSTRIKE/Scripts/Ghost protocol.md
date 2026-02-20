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
