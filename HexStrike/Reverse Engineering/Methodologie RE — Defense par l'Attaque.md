# Reverse Engineering — Défense par l'Attaque

> *Comprendre comment une attaque est construite pour mieux s'en défendre.*
> *Le RE défensif n'attaque pas — il analyse pour protéger.*

---

## Principe Fondamental HexStrike

Le reverse engineering dans le contexte HexStrike est **défensif** :
- Analyser des malwares pour comprendre leur fonctionnement
- Étudier des exploits publiés pour conseiller les clients sur les patches
- Comprendre les techniques d'attaque pour mieux les détecter
- Former les équipes de sécurité à reconnaître les IOCs (Indicateurs de Compromission)

**Ce qui est légal :**
- Analyser des samples de malware dans un environnement isolé
- Étudier des exploits publiés (CVE) pour du patching
- Désassembler des logiciels pour lesquels tu as l'autorisation ou qui sont open source
- Analyser du trafic réseau capturé sur tes propres systèmes

**Ce qui est illégal :**
- Cracker des licences logicielles propriétaires
- Contourner des DRM sans autorisation
- Analyser des systèmes tiers sans accord

---

## Environnement d'Analyse Sécurisé

**Règle absolue : Toujours analyser dans un environnement isolé.**

```bash
# Setup VM isolée (REMnux — distribution dédiée au RE défensif)
# Téléchargement : remnux.org

# Ou Flare-VM (Windows) — pour analyser malware Windows
# github.com/mandiant/flare-vm

# Configuration réseau : Mode "Host-Only" ou "Réseau interne"
# JAMAIS en mode "NAT" ou "Bridged" lors de l'analyse de malware
```

**Outils de base à installer dans la VM :**
```bash
# Sur REMnux (pré-installé pour la plupart)
file, strings, xxd    # Analyse initiale
strace, ltrace        # Tracing système
Wireshark             # Analyse réseau
Ghidra, Radare2       # Désassembleurs
x64dbg, GDB           # Debuggers
```

---

## Phase 1 — Analyse Statique (sans exécuter le fichier)

**Objectif :** Comprendre le fichier sans l'exécuter.

```bash
# Identifier le type de fichier
file suspicious.exe
file suspicious.bin

# Strings lisibles dans le binaire
strings suspicious.exe | grep -i "http\|url\|password\|cmd\|powershell"

# Hashes pour identification
md5sum suspicious.exe
sha256sum suspicious.exe
# Vérifier sur VirusTotal : virustotal.com

# Analyse d'entête PE (Windows)
pecheck suspicious.exe  # ou PE Studio (GUI)
exiftool suspicious.exe

# Détecter le packer/obfuscateur
PEiD (GUI) ou Detect-It-Easy
```

---

## Phase 2 — Analyse Dynamique (exécution contrôlée)

**SEULEMENT dans la VM isolée, réseau désactivé ou simulé.**

```bash
# Surveiller les appels système (Linux)
strace -f -e trace=all ./suspicious_elf 2>&1 | tee strace_output.txt

# Surveiller les connexions réseau (même VM)
# Lancer Wireshark avant d'exécuter
wireshark -i eth0

# Sur Windows (Flare-VM) — Process Monitor
# Filtrer par nom du processus pour voir :
# - Fichiers créés/modifiés
# - Clés de registre
# - Connexions réseau

# Autoruns — persistance
autoruns.exe  # Voir ce qui se lance au démarrage après exécution
```

---

## Phase 3 — Désassemblage et Décompilation

```bash
# Ghidra (NSA open source — excellent pour débutant)
# Téléchargement : ghidra-sre.org
# Importer le binaire → CodeBrowser → Analyse automatique
# Utiliser le décompilateur intégré

# Radare2 (CLI — puissant)
r2 suspicious.exe
> aaa           # Analyse complète
> afl           # Lister les fonctions
> pdf @ main    # Désassembler main()
> axt @ sym.import.CreateFileW  # Trouver les appels vers une API

# Binary Ninja (payant, essai gratuit)
# IDA Free (gratuit pour usage non-commercial)
```

---

## Phase 4 — Identification des IOCs

**Indicateurs de Compromission à extraire :**

```
Réseau :
- IPs de C2 (Command & Control)
- Domaines de C2
- URLs de téléchargement
- User-Agents inhabituels
- Ports non-standard

Fichiers :
- Hashes (MD5, SHA1, SHA256)
- Chemins de fichiers créés
- Noms de fichiers déposés

Registre (Windows) :
- Clés de persistance
- Valeurs modifiées

Comportement :
- Processus créés
- Services installés
- Comptes créés
```

---

## Ressources d'Apprentissage RE

### Samples de Malware Légaux (pour étude)
- **MalwareBazaar** : [bazaar.abuse.ch](https://bazaar.abuse.ch) — samples de malware réels pour chercheurs
- **VirusTotal** : [virustotal.com](https://www.virustotal.com) — analyse et accès aux samples
- **Hybrid Analysis** : [hybrid-analysis.com](https://www.hybrid-analysis.com) — analyse dynamique cloud

### Plateformes de Practice RE
- **Crackmes.one** : challenges RE légaux
- **Reversing.kr** : challenges progressifs
- **Malware Traffic Analysis** : [malware-traffic-analysis.net](https://malware-traffic-analysis.net) — PCAP à analyser

### Cours et Formations
- **OpenSecurityTraining2** : cours gratuits en profondeur
- **TCM Security — Practical Malware Analysis** : formation payante mais solide
- **Livre : "Practical Malware Analysis"** (Sikorski & Honig) — référence absolue

---

## Template de Rapport d'Analyse RE

Pour chaque sample analysé, documenter dans `HexStrike/Vulnerabilites/` :

```markdown
# Analyse RE — [Nom/Hash du Sample]

**Date d'analyse :** YYYY-MM-DD
**Hash SHA256 :** [hash]
**Type identifié :** Ransomware / RAT / Dropper / etc.
**Source :** MalwareBazaar / VirusTotal / Client

## Analyse Statique
- Packer : [Oui/Non — lequel]
- Strings notables : [liste]
- Imports suspects : [liste]

## Analyse Dynamique
- Connexions réseau : [IPs, domaines]
- Fichiers créés : [chemins]
- Persistance : [mécanisme]

## IOCs
[Liste des indicateurs de compromission]

## Recommandations Défensives
[Ce que les clients doivent détecter/bloquer]
```

---

*Reverse Engineering défensif HexStrike — Comprendre pour protéger*
