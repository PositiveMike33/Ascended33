
## 1. Introduction : La Boîte Noire Démasquée

Bienvenue dans ce parcours d'apprentissage dédié à l'analyse de micrologiciels (firmwares). Pour un chercheur en cybersécurité débutant, un système CCTV — comme les modèles **Sidenav** ou **Identiv Vision** — ressemble souvent à une "boîte noire" impénétrable. Pourtant, ces appareils sont les sentinelles de nos infrastructures. Comprendre leur fonctionnement interne n'est pas seulement une curiosité technique, c'est une nécessité pour garantir que ces protecteurs ne deviennent pas des traîtres.

L'expert Benjamin Tamási nous enseigne une philosophie précieuse : l'analyse logique prime sur l'ouverture physique. Pourquoi s'épuiser à dessouder des puces EEPROM quand le "cerveau" de l'appareil est souvent accessible via une simple mise à jour logicielle ?

"La curiosité technique consiste à ne pas accepter qu'une porte soit fermée simplement parce qu'on n'a pas la clé, mais à comprendre comment le verrou a été forgé pour en fabriquer une nouvelle."

Dans ce guide, nous allons transformer un bloc de données binaires illisible en un système de fichiers clair en utilisant deux outils piliers : **Binwalk** pour l'extraction chirurgicale et **John the Ripper** pour le décodage des secrets. Avant de disséquer le cerveau de l'appareil, notre première mission est de localiser ses points de contact sur le réseau.

## 2. Phase 1 : Reconnaissance et Identification des Portes d'Entrée

Pour identifier votre cible, nous utilisons **Nmap** (ou sa version graphique **Zenmap**). Un scan "intense" révélera les services qui écoutent silencieusement. Ne vous laissez pas tromper par la "sécurité par l'obscurité" : les constructeurs cachent souvent des services sur des ports non standard pour échapper aux regards indiscrets.

### Cartographie des Ports Critiques

|   |   |   |
|---|---|---|
|Port|Service|Implication pour l'Analyse|
|**80 / 8085**|HTTP|Interface web. Souvent truffée de bugs (ex: accès direct après plusieurs échecs).|
|**23**|**Telnet**|Le Graal. Un accès shell (ligne de commande) souvent non documenté et caché.|
|**554 / 8554**|RTSP|Flux vidéo. Souvent utilisé comme protocole de "fallback" non sécurisé.|
|**8000**|Propriétaire|Port de gestion spécifique (souvent utilisé par Hikvision/Dahooa).|

**Le conseil du professeur :** Pour bien comprendre la diffusion vidéo, retenez cette analogie. Le protocole **RTSP** est comme votre télécommande (il met en pause, joue ou arrête le flux), tandis que le **RTP** est la diffusion elle-même (le signal qui arrive sur l'écran). Notez que même si l'interface Web est protégée, le flux RTSP est parfois accessible sans authentification via une simple adresse URI.

Une fois que nous avons confirmé que l'appareil est "vivant" et bavard, nous devons récupérer son micrologiciel pour l'analyser hors ligne.

## 3. Phase 2 : Acquisition et Analyse Initiale de l'Archive

Inutile de sortir le fer à souder. Les firmwares sont généralement disponibles sur les sites de support des constructeurs ou des distributeurs (comme LDS). Ces fichiers, bien qu'étiquetés `.bin`, sont des poupées russes numériques.

En utilisant la commande `file` sous Linux, vous découvrirez souvent que le fichier binaire est en réalité un **uboot PPC boot image** ou une archive compressée. Une fois décompressé manuellement (si c'est un simple ZIP), on découvre une structure de fichiers fascinante.

**Structure typique d'un firmware extrait :**

```bash
/firmware_data
  ├── install_desc.txt  # Scripts d'installation en texte clair (ASCII)
  ├── logo.img          # L'image de démarrage du constructeur
  ├── romfs.img         # Le système de fichiers compressé (Notre cible !)
  └── sophia.exe        # Une curiosité : un exécutable Windows sur un système Linux ?
```

La présence de fichiers comme `sophia.exe` montre parfois que les constructeurs mélangent des environnements de développement, créant des "anomalies" qui sont autant de pistes pour nous. Mais pour l'instant, notre priorité est de monter l'image `romfs.img`.

## 4. Phase 3 : Extraction — La Puissance de Binwalk

L'analyse de `romfs.img` avec un éditeur hexadécimal révèle souvent un **uImage header** de 64 octets. Ce petit bloc de données empêche le système Linux de reconnaître le système de fichiers.

### La méthode manuelle vs l'automatisme magique

1. **La méthode "artisanale" :** Utiliser `dd if=romfs.img of=romfs_clean.img skip=64 bs=1` pour supprimer chirurgicalement l'en-tête de 64 octets.
2. **La méthode "Master" :** Utiliser **Binwalk**.

**L'Astuce d'Expert :** La commande `binwalk -Me [fichier]` est votre meilleure amie. Le paramètre **-M** signifie **Matryoshka** (Poupées Russes). Il indique à Binwalk d'extraire récursivement chaque fichier trouvé à l'intérieur d'un autre fichier, automatisant ainsi des heures de travail manuel.

Binwalk identifiera l'en-tête uImage et extraira automatiquement le système de fichiers, qu'il s'agisse de **SquashFS** ou de **ROMFS**. Vous transformez ainsi un bloc binaire indigeste en une arborescence Linux standard, prête à livrer ses secrets.

## 5. Phase 4 : Exploration du Système de Fichiers Embarqué

Une fois le système extrait, vous naviguez dans les entrailles de l'appareil. Votre cible prioritaire est le dossier `/etc/` pour trouver les fichiers d'authentification.

### Le chemin critique vers les secrets :

1. **Localisation de** `**/etc/passwd**` **:** Sur la plupart des systèmes embarqués, il n'y a pas de fichier `shadow`. Les hachages des mots de passe sont stockés **directement** dans `passwd`.
2. **La faille Dahooa (Bypass 127.0.0.1) :** Gardez en tête que certains systèmes ont des "portes dérobées" logiques. Par exemple, une vulnérabilité connue permet de contourner l'authentification si la requête semble provenir de l'adresse locale `127.0.0.1`.
3. **Le "God's Eye" :** C'est le concept d'un accès universel intégré par les constructeurs pour la maintenance, souvent laissé actif par négligence.

**Le Hack Actionnable :** Si vous analysez un DVR et que vous souhaitez réinitialiser l'accès, cherchez le dossier `/mnt/mtd/config/`. La suppression du fichier `**account1**` force souvent l'appareil à revenir aux réglages d'usine, supprimant le mot de passe administrateur au prochain redémarrage.

## 6. Phase 5 : Décryptage avec John the Ripper

Vous avez extrait une chaîne de caractères comme `root:ab9f8...`. C'est un hachage (souvent de type **DES** traditionnel). Pour le briser, nous utilisons **John the Ripper**.

### Performance et Outils

- **John the Ripper (CPU) :** Sur un ordinateur portable standard, casser un hachage DES peut prendre environ **3 heures**.
- **OCL-Hashcat (GPU) :** Si vous utilisez la puissance de votre carte graphique, ce même hachage peut être brisé en seulement **17 secondes**.

**Commande type :** `john --format=desc hashlist.txt`

Une fois le mot de passe root obtenu (souvent une suite simple comme `12345` ou un mot de passe maître constructeur), vous avez un contrôle total via le port **Telnet (23)**. En tant que `root`, vous pouvez non seulement visionner les flux, mais aussi **effacer les journaux de connexion (logs)** ou même formater le disque dur pour supprimer toute preuve vidéo.

## 7. Conclusion : Vers une Meilleure Hygiène de Sécurité

Cette immersion nous montre que la sécurité des systèmes CCTV repose souvent sur des fondations fragiles. Entre les mots de passe par défaut et les comptes de maintenance cachés, la "boîte noire" est en réalité pleine de courants d'air.

### Checklist de sécurisation (Hygiène Cyber) :

- [ ] **Bannir les mots de passe par défaut :** Changez immédiatement `admin/12345`.
- [ ] **Désactiver Telnet :** Si l'accès shell n'est pas nécessaire, fermez le port 23.
- [ ] **Isolation Réseau :** Ne placez jamais vos caméras sur l'Internet public. Utilisez un VLAN dédié et isolé.
- [ ] **Mises à jour :** Appliquez les correctifs pour fermer les vulnérabilités de type "bypass" (comme le bypass 127.0.0.1).

**Note de fin :** La rétro-ingénierie est une discipline noble qui sert à renforcer nos défenses. Utilisez ces connaissances avec éthique et rigueur. En comprenant comment les systèmes sont brisés, vous devenez capable de construire des architectures véritablement résilientes. Bon hacking éthique !