---
name: launch-vault
description: Lance 100% du projet Vault — Docker containers, Obsidian, Streamlit HexStrike, VS Code. Utiliser quand l'utilisateur dit "lance le vault", "démarre tout", "ouvre le projet".
disable-model-invocation: true
---

Lance le script maître du Vault qui démarre tout le projet en séquence :

1. Docker Compose (th3-tor, th3-kali, th3-hackergpt, th3-hexstrike)
2. Obsidian → D:\Vault\Vault
3. Streamlit HexStrike → http://localhost:8501
4. VS Code → D:\Vault\Vault
5. Navigateur → http://localhost:8501

Commande à exécuter :
```
PowerShell -NoProfile -ExecutionPolicy Bypass -File "D:\Vault\Vault\LAUNCH_VAULT.ps1"
```

Le raccourci bureau "VAULT LAUNCH.lnk" fait la même chose en double-clic.
