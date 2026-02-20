# Outils Reverse Engineering — Arsenal HexStrike

---

## Distributions Dédiées

### REMnux
**Usage :** Distribution Linux spécialisée pour l'analyse de malware.
- URL : [remnux.org](https://remnux.org)
- Contient 100+ outils pré-installés
- Recommandé pour l'analyse de samples Linux/PDF/Office

### Flare-VM
**Usage :** Windows VM configurée pour l'analyse de malware Windows.
- URL : [github.com/mandiant/flare-vm](https://github.com/mandiant/flare-vm)
- Installation sur Windows 10 propre en VM
```powershell
# Installation
(New-Object net.webclient).DownloadFile('https://raw.githubusercontent.com/mandiant/flare-vm/main/install.ps1', "$env:temp\install.ps1")
.\install.ps1
```

---

## Analyse Statique

| Outil | OS | Usage | Gratuit |
|-------|-----|-------|---------|
| **Ghidra** | Linux/Win/Mac | Désassembleur + décompilateur complet | Oui |
| **Radare2** | Linux/Win/Mac | Framework RE CLI | Oui |
| **Binary Ninja** | Linux/Win/Mac | Désassembleur professionnel | Essai gratuit |
| **IDA Free** | Linux/Win/Mac | Version gratuite limitée d'IDA | Oui |
| **Cutter** | Linux/Win/Mac | Interface graphique pour Radare2 | Oui |
| **PE Studio** | Windows | Analyse rapide binaires PE | Oui |
| **Detect It Easy** | Linux/Win | Détection de packers | Oui |
| **exiftool** | Linux/Win/Mac | Métadonnées de fichiers | Oui |

---

## Analyse Dynamique

| Outil | OS | Usage | Gratuit |
|-------|-----|-------|---------|
| **x64dbg** | Windows | Debugger Windows | Oui |
| **GDB + pwndbg** | Linux | Debugger Linux | Oui |
| **Process Monitor** | Windows | Monitoring fichiers/réseau/registre | Oui |
| **Process Hacker** | Windows | Gestionnaire de processus avancé | Oui |
| **Autoruns** | Windows | Persistance au démarrage | Oui |
| **Wireshark** | Linux/Win | Capture et analyse réseau | Oui |
| **FakeNet-NG** | Windows | Simulation réseau pour malware | Oui |
| **INetSim** | Linux | Simulation services réseau | Oui |

---

## Ghidra — Guide Rapide

```bash
# Installation
# Télécharger depuis https://ghidra-sre.org
# Requis : Java 17+
sudo apt install openjdk-17-jdk
# Décompresser et lancer
./ghidraRun

# Workflow de base
# 1. File → New Project → Non-Shared Project
# 2. File → Import File → [sélectionner le binaire]
# 3. Double-clic sur le fichier importé
# 4. "Analyze" → Yes (analyse automatique)
# 5. Dans CodeBrowser :
#    - Ctrl+G : Aller à une adresse
#    - F → Functions window : voir toutes les fonctions
#    - Décompilateur : fenêtre à droite automatique
```

---

## Radare2 — Commandes Essentielles

```bash
# Ouvrir un binaire
r2 suspicious.exe
r2 -A suspicious.exe  # Avec analyse automatique

# Commandes de base
?           # Aide
aaa         # Analyse complète
afl         # Liste des fonctions
pdf @ main  # Désassembler la fonction main
s main      # Seek vers main
VV          # Mode visuel graphe de flux
q           # Quitter

# Chercher des strings
iz          # Strings dans les sections data
iz~http     # Filtrer les strings contenant "http"

# Cross-references
axt @ [adresse]  # Qui appelle cette adresse
axf @ [adresse]  # Que cette adresse appelle
```

---

## x64dbg — Debugger Windows

**Commandes clés :**
- `F2` : Poser un breakpoint
- `F7` : Step into (rentrer dans les fonctions)
- `F8` : Step over (passer par-dessus)
- `F9` : Run jusqu'au prochain breakpoint
- `Ctrl+G` : Aller à une adresse

**Workflow typique :**
1. Ouvrir le binaire en mode "suspend on entry"
2. Analyser les imports (onglet "Imports")
3. Poser des breakpoints sur les fonctions réseau (WS2_32.dll)
4. Exécuter et observer les appels réseau
5. Poser des breakpoints sur les fichiers créés (kernel32.CreateFile)

---

## Analyse de Documents Malveillants

```bash
# PDF
pdfid malicious.pdf       # Analyse rapide
pdf-parser malicious.pdf  # Analyse détaillée

# Office (macros)
olevba malicious.docm     # Extraire les macros VBA
oletools (suite complète)

# JavaScript obfusqué
js-beautify script.js     # Désobfusquer
node script.js 2>&1       # Exécuter dans sandbox
# Ou : JSTool dans Firefox DevTools

# Archives et packed
file archive.bin          # Identifier le format
binwalk archive.bin       # Analyser les contenus embarqués
7z x archive.bin          # Extraire
```

---

## Plateformes d'Analyse Cloud (Sandboxes)

| Plateforme | Usage | Gratuit |
|------------|-------|---------|
| [any.run](https://any.run) | Sandbox interactive | Oui (limité) |
| [Hybrid Analysis](https://hybrid-analysis.com) | Sandbox automatisée | Oui |
| [VirusTotal](https://virustotal.com) | Multi-AV + comportement | Oui |
| [Joe Sandbox](https://www.joesandbox.com) | Analyse approfondie | Essai gratuit |

**Note :** Les fichiers soumis à ces plateformes deviennent publics (sauf offres payantes). Ne jamais soumettre de fichiers confidentiels client.

---

*Arsenal RE Défensif HexStrike — Comprendre l'attaque pour renforcer la défense*
