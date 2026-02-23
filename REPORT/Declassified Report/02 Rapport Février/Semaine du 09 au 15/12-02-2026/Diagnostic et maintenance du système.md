#12-02-2026 
### Diagnostic et maintenance du système

- Lancement d'un bilan de santé à l'aide de Microsoft PC Manager, qui a identifié un état "Réseau déconnecté" et des problèmes de service DNS.
- Nettoyage du système via PC Manager, libérant 248,8 Mo d'espace de stockage et nettoyant 21 traces d'utilisation.
- Utilisation de la fonction "PC boost" de PC Manager.

### Dépannage du réseau

- Exécution des commandes `ipconfig` dans PowerShell pour inspecter les configurations des adaptateurs réseau, observation de plusieurs statuts "Média déconnecté" et d'une connexion VPN NordLynx active.
- Tentative de renouvellement des adresses IP à l'aide de `ipconfig /renew`, ce qui a entraîné une erreur de dépassement de délai DHCP pour l'adaptateur Npcap Loopback, indiquant une incapacité à contacter le serveur DHCP.
- Consultation de l'application Windows "Get Help" pour le diagnostic du réseau, qui a indiqué de manière contradictoire être connecté à l'internet.
- Vous avez observé que le statut Wi-Fi était "Non connecté" (not connected) dans les paramètres rapides, ce qui corrobore les problèmes de déconnexion du réseau.

### Référence et gestion des connaissances

- Examen d'une note personnelle Obsidian intitulée "40 commandes Windows", détaillant divers utilitaires de ligne de commande Windows, notamment `ipconfig`, `findstr`, `ipconfig /release`, `ipconfig /renew`, `ipconfig /displaydns`, `clip`, `ipconfig /flushdns`, `nslookup`, `cls`, `getmac`, `powercfg /energy`, `powercfg /batteryreport`, et `assoc`. Cet examen a directement soutenu les activités de dépannage du réseau.
