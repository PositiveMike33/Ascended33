[[CCTV]]
[[CAM_IP]]
[[Hexstrike]]
[[Claude_code]]
[[08-02-2026]]
Audit de sécurité réseau local — 7 Février 2026

---

## 📌 CONTEXTE

**Objectif** : Scanner le réseau local pour identifier tous les ports ouverts et localiser 2 caméras personnelles connectées, en utilisant le framework HexStrike AI.

**Environnement** :

- PC : MSI (192.168.1.162) — Windows
- HexStrike AI : Docker container `th3-hexstrike` sur port 8888 (healthy)
- Réseau : 192.168.1.0/24 via routeur SmartRG
- Outils utilisés : Nmap (via HexStrike API), PowerShell (scans natifs), Python (probes STUN/API)

---

## PHASE 1 — DÉCOUVERTE DU RÉSEAU

### 1.1 Découverte des hôtes (ARP + Nmap)

**Méthode** : Table ARP Windows + Nmap ping sweep via HexStrike (`/api/tools/nmap`)

**Résultat — 6 appareils réels détectés** :

|#|IP|MAC|Fabricant (OUI Lookup)|Type identifié|
|---|---|---|---|---|
|1|192.168.1.1|e8:2c:6d:d5:de:81|**SmartRG Inc.** (Vancouver, WA)|🌐 Routeur/Box Internet|
|2|192.168.1.115|fe:7a:bf:aa:f8:10|MAC randomisée (bit LAA)|📱 Smartphone/Tablette|
|3|192.168.1.162|—|**MSI (Micro-Star)**|💻 Votre PC (nous)|
|4|192.168.1.165|98:a8:29:80:0f:68|**AltoBeam Inc.** (Beijing, CN)|📷 **CAMÉRA 1**|
|5|192.168.1.166|a0:d0:5b:b6:8e:e2|**Samsung**|📺 TV Samsung Smart|
|6|192.168.1.235|20:98:ed:92:07:b9|**AltoBeam Inc.** (Beijing, CN)|📷 **CAMÉRA 2**|

**Sources de vérification MAC** : maclookup.app (confirmé AltoBeam pour 98:A8:29 et 20:98:ED)

### 1.2 Scan des ports — Routeur (192.168.1.1)

**Commande HexStrike** : `nmap -sV -p 80,443,8080 -T4 --open -O 192.168.1.1`

|Port|État|Service|Version|
|---|---|---|---|
|80/tcp|OPEN|HTTP|lighttpd 1.4.53|
|443/tcp|OPEN|HTTPS|lighttpd 1.4.53|
|8080/tcp|OPEN|HTTP|lighttpd 1.4.53|

OS fingerprint : Cisco SG 500 switch (88%) ou Cisco SF300/SG300 (86%)

### 1.3 Scan des ports — TV Samsung (192.168.1.166)

**Commande HexStrike** : `nmap -sV -sC -p 1-10000 -T4 --open -Pn 192.168.1.166`

|Port|État|Service|Version|
|---|---|---|---|
|7678/tcp|OPEN|UPnP|Samsung AllShare upnpd 1.0|
|8001/tcp|OPEN|HTTP|(SmartViewSDK — 403 Forbidden)|
|8002/tcp|OPEN|SSL/HTTP|SmartViewSDK (certificat CN=SmartViewSDK, KR)|
|8080/tcp|OPEN|HTTP|lighttpd (WebServer)|
|8187/tcp|OPEN|UPnP|Samsung AllShare upnpd 1.0|
|9080/tcp|OPEN|HTTP|Mongoose httpd (JSON)|
|9197/tcp|OPEN|UPnP|Samsung AllShare upnpd 1.0|

---

## PHASE 2 — SCAN APPROFONDI DES 2 CAMÉRAS

### 2.1 Scan TCP complet (ports 1–65535)

**Méthode** : Script PowerShell `cam_fullscan.ps1` exécuté depuis Windows (pas Docker) — scan asynchrone par batch de 500 ports, timeout 300ms/port.

|Caméra|IP|Ports TCP ouverts|
|---|---|---|
|**Caméra 1**|192.168.1.165|**0 / 65535** ❌|
|**Caméra 2**|192.168.1.235|**0 / 65535** ❌|

**Conclusion** : Les deux caméras n'ont AUCUN port TCP ouvert sur toute la plage 1-65535.

### 2.2 Scan UDP (RTSP/SSDP/mDNS/STUN)

**Méthode** : Nmap UDP via HexStrike + probes PowerShell

**Via HexStrike (nmap -sU)** :

- Ports testés : 554, 8554, 5353, 1900, 3478, 3702, 6970, 10554, 67, 68
- Résultat : Tous en `open|filtered` (typique UDP à travers Docker bridge)

**Via PowerShell (probes directs)** :

|Test|Caméra 1 (165)|Caméra 2 (235)|
|---|---|---|
|RTSP UDP 554|❌ Pas de réponse|❌ Pas de réponse|
|RTSP UDP 8554|❌ Pas de réponse|❌ Pas de réponse|
|RTSP UDP 10554|❌ Pas de réponse|❌ Pas de réponse|
|PPCS/TUTK 32100|❌ Pas de réponse|❌ Pas de réponse|
|PPCS/TUTK 32761|❌ Pas de réponse|❌ Pas de réponse|
|P2P 12300/20000/56789|❌ Pas de réponse|❌ Pas de réponse|

### 2.3 Découverte ONVIF (WS-Discovery)

**Méthode** : Envoi SOAP Probe multicast UDP 239.255.255.250:3702

**Résultat** : ❌ Aucune réponse — Les caméras ne supportent pas ONVIF.

### 2.4 Découverte SSDP/UPnP

**Méthode** : M-SEARCH multicast UDP 239.255.255.250:1900

**Résultat** : ❌ Aucune réponse des caméras (la TV Samsung non plus depuis le script).

### 2.5 Connectivité confirmée

|Test|Caméra 1|Caméra 2|
|---|---|---|
|**Ping ICMP**|✅ 5ms TTL=64|✅ 5ms TTL=64|
|**ARP**|✅ Présente|✅ Présente|

**Conclusion** : Les caméras sont vivantes et accessibles au niveau réseau, mais ne répondent à AUCUN protocole standard (HTTP, RTSP, ONVIF, SSDP, Telnet, SSH).

---

## PHASE 3 — IDENTIFICATION DU FABRICANT & MODÈLE

### 3.1 Application mobile

- **Nom** : Ease Life (EaseLife)
- **Package Android** : `com.vitec.easelifeEn`
- **Développeur** : Hangzhou Vision Insight Technology Co., Ltd.
- **Site** : ehomeease.com / easelife.app
- **Aussi connu sous** : Marque **blurams** (même fabricant)

### 3.2 FCC ID

- **Grantee Code** : 2ASAQ
- **Titulaire** : Hangzhou Vision Insight Technology Co., Ltd.
- **20+ modèles enregistrés** dont : A10C, A11, A11C, A20, A21C, A22C, A30, A30C, A31, A31P, A31S, A3XX, D10C, D10C, E20C, S15F, S20, S21, S21C

### 3.3 Chipset WiFi

- **Fabricant** : AltoBeam Inc. (Beijing, Chine)
- **Modèle probable** : ATBM6012B (SoC WiFi 802.11 b/g/n, utilisé dans les caméras IoT)
- **Utilisé aussi dans** : TP-Link Tapo C110 (variante SSC333)

### 3.4 Modèles Ease Life documentés

- **Y104** : Wi-Fi Smart Camera
- **V2-2401** : Smart WiFi Camera
- **D112 (Y108)** : 1080P HD, PTZ 360°, vision nocturne couleur, audio bidirectionnel
- **D115** : Smart Wi-Fi Camera
- **D100** : Smart Camera

---

## PHASE 4 — ANALYSE DU PROTOCOLE P2P

### 4.1 Infrastructure cloud découverte

**Méthode** : Résolution DNS des sous-domaines ehomeease.com

|Domaine|IP|Rôle|Status|
|---|---|---|---|
|`ehomeease.com`|129.146.119.184|Site web principal|✅ Résolu|
|`easelife.app`|172.64.80.1|Site vitrine (Cloudflare)|✅ Résolu|
|`api.ehomeease.com`|129.146.61.229|**API REST backend**|✅ **ACTIF — Répond en JSON**|
|`stun.ehomeease.com`|129.146.78.10|**Serveur STUN (NAT traversal)**|✅ Résolu|
|`p2p.ehomeease.com`|—|P2P relay|❌ NXDOMAIN|
|`cloud.ehomeease.com`|—|Cloud|❌ NXDOMAIN|
|`turn.ehomeease.com`|—|TURN relay|❌ NXDOMAIN|
|`relay.ehomeease.com`|—|Relay|❌ NXDOMAIN|
|`iot.ehomeease.com`|—|IoT|❌ NXDOMAIN|

**Hébergement** : Oracle Cloud Infrastructure (plage 129.146.x.x)

### 4.2 Test de l'API cloud

**Méthode** : Python urllib depuis le container Docker

|Endpoint|Méthode|Réponse|
|---|---|---|
|`api.ehomeease.com/`|GET|`{"failflag":500,"failmsg":""}`|
|`api.ehomeease.com/api/v1/`|GET|`{"failflag":500,"failmsg":""}`|
|`api.ehomeease.com/health`|GET|`You don't have permission to access on this server`|
|30+ autres endpoints|GET/POST|Tous `failflag:500`|

**Conclusion** : L'API est active mais nécessite les tokens/signatures propriétaires de l'app mobile.

### 4.3 Test STUN

- Le serveur STUN `stun.ehomeease.com:3478` ne répond pas aux requêtes STUN standard (RFC 5389) depuis Docker (bridge réseau isolé)
- **Interprétation** : Il pourrait utiliser un protocole STUN modifié ou propriétaire

### 4.4 Routeur NAT-PMP

- Le routeur SmartRG (192.168.1.1:5351) **répond au NAT-PMP**
- Réponse brute : `00 80 00 00 00 32 41 E0 C0 DE BF F3`
- Octets 8-11 (`C0 DE BF F3`) = IP publique **192.222.191.243**

### 4.5 Architecture P2P déduite

```
┌──────────────┐        UDP (propriétaire)       ┌────────────────────┐
│  Caméra 1    │ ──────────────────────────────► │ stun.ehomeease.com │
│ 192.168.1.165│                                  │   129.146.78.10    │
└──────────────┘                                  └────────┬───────────┘
                                                           │
┌──────────────┐        UDP (propriétaire)                 │  Relay P2P
│  Caméra 2    │ ──────────────────────────────►           │
│ 192.168.1.235│                                  ┌────────▼───────────┐
└──────────────┘                                  │ api.ehomeease.com  │
                                                  │  129.146.61.229    │
┌──────────────┐        HTTPS (app ↔ cloud)       └────────┬───────────┘
│ 📱 App Ease  │ ◄────────────────────────────────         │
│   Life       │                                           │
└──────────────┘        UDP P2P (flux vidéo)    ◄──────────┘
```

**Résumé** : Les caméras n'acceptent AUCUNE connexion entrante. Elles initient elles-mêmes une connexion sortante UDP vers le cloud d'ehomeease.com, qui sert de relais P2P vers l'app mobile.

---

## PHASE 5 — MÉTHODOLOGIE D'ATTAQUE APPLIQUÉE

### Application de la méthodologie CCTV en 6 étapes :

|Étape|Technique|Résultat|Statut|
|---|---|---|---|
|**1. Reconnaissance passive (OSINT)**|Shodan, MAC lookup, FCC, DNS|Fabricant identifié, infra cloud cartographiée|✅ Terminé|
|**2. Identifiants par défaut**|Test admin/admin, root/root sur HTTP/RTSP/Telnet/SSH|**NON APPLICABLE** — Aucun service n'écoute|❌ Bloqué|
|**3. Brute-force RTSP**|Cameradar / dictionnaire sur port 554|**NON APPLICABLE** — Port 554 fermé|❌ Bloqué|
|**4. CVE / Vulnérabilités**|CVE-2021-32934 (TUTK), CVE-2021-28372 (Kalay)|Possiblement vulnérable si SDK TUTK < v3.3|⚠️ Non vérifié|
|**5. Rétro-ingénierie firmware**|Binwalk sur firmware .bin|Firmware non disponible publiquement|❌ Bloqué|
|**6. Accès physique (UART)**|Ports debug sur PCB|Non tenté (nécessite ouverture physique)|🔲 Non tenté|

**Blocage principal** : Les étapes 2, 3 et 5 de la méthodologie classique sont **inapplicables** car les caméras n'exposent aucun service réseau local.

---

## PHASE 6 — ÉVALUATION DE SÉCURITÉ

### Score de sécurité LAN : 🟢 92/100 (ÉLEVÉ)

|Critère|Score|Détail|
|---|---|---|
|Surface d'attaque TCP|10/10|0 ports ouverts sur 65535|
|Surface d'attaque UDP|9/10|Aucun service UDP détecté localement|
|RTSP exposé|10/10|Pas de flux interceptable|
|Interface Web|10/10|Absente|
|Telnet/SSH|10/10|Fermés|
|ONVIF|10/10|Non implémenté|
|UPnP/SSDP|10/10|Non détecté|
|Chiffrement P2P|7/10|Non vérifiable sans reverse APK|
|Dépendance cloud|6/10|Tout passe par Oracle Cloud (Chine)|
|Mise à jour firmware|10/10|OTA via app (non exposé)|

### Risques identifiés

|Niveau|Risque|Description|
|---|---|---|
|🟡 MOYEN|Dépendance cloud totale|Si ehomeease.com tombe, les caméras sont inutilisables|
|🟡 MOYEN|Chiffrement P2P inconnu|Possiblement vulnérable à CVE-2021-32934 si TUTK < v3.3|
|🟡 MOYEN|API propriétaire|Impossible d'auditer la sécurité de l'API sans reverse engineering|
|🟢 FAIBLE|Pas d'accès local|Impossible d'enregistrer localement (pas de NVR)|

---

## SCRIPTS PRODUITS PENDANT L'AUDIT

|Fichier|Rôle|
|---|---|
|`C:\Users\th3th\cam_scan.ps1`|Scan ports IoT + RTSP UDP + ONVIF WS-Discovery|
|`C:\Users\th3th\cam_fullscan.ps1`|Scan TCP full-range 1-65535 (async batches)|
|`C:\Users\th3th\cam_traffic_capture.ps1`|Analyseur trafic : ARP, DNS, ports IoT, probes P2P, NAT-PMP|
|`C:\Users\th3th\stun_test.py`|Test STUN RFC 5389 + probing API ehomeease.com|
|`C:\Users\th3th\api_probe.py`|Fuzzing 35+ endpoints API ehomeease.com|

---

# 🚀 PROCHAINES ÉTAPES — PLAN D'ACTION

## Étape 7 — Reverse Engineering APK (PRIORITÉ HAUTE)

**Objectif** : Décompiler l'APK Ease Life pour identifier le protocole P2P exact

**Actions** :

1. Télécharger l'APK `com.vitec.easelifeEn` depuis le téléphone Android (via `adb pull`)
2. Décompiler avec **jadx** ou **apktool** (disponibles dans HexStrike)
3. Rechercher dans le code décompilé :
    - Bibliothèques natives `.so` (libTUTK, libPPCS, libP2P, etc.)
    - Clés de chiffrement hardcodées
    - URLs d'API complètes et endpoints
    - Format du Device UID (identifiant P2P unique)
    - Certificats SSL pinning
4. **Fichiers critiques à extraire** :
    - `lib/arm64-v8a/*.so` → bibliothèques P2P natives
    - `assets/` → fichiers de configuration
    - `res/raw/` → certificats, configs
    - `AndroidManifest.xml` → permissions et composants

**Outils HexStrike** : Binwalk, strings, jadx (si installé dans le container)

## Étape 8 — Capture Wireshark du trafic caméra

**Objectif** : Intercepter les paquets UDP des caméras vers le cloud

**Actions** :

1. Configurer le routeur SmartRG en mode **port mirroring** (miroir de port) sur les IPs 192.168.1.165 et 192.168.1.235
2. Ou utiliser **ARP spoofing** (via ettercap dans HexStrike) pour intercepter le trafic
3. Capturer avec **tcpdump/tshark** dans HexStrike
4. Analyser les paquets UDP pour identifier :
    - Le protocole P2P (TUTK Kalay, PPCS, ou propriétaire)
    - Les serveurs relais contactés
    - Si le flux vidéo est chiffré ou en clair
    - Le format des Device UIDs

**Commande HexStrike prévue** :

```
POST /api/command
{"command": "timeout 60 tcpdump -i eth0 host 192.168.1.165 or host 192.168.1.235 -w /tmp/camera_capture.pcap"}
```

## Étape 9 — Test CVE-2021-32934 / CVE-2021-28372

**Objectif** : Vérifier si le SDK P2P est vulnérable

**Actions** (après identification du protocole en étape 7/8) :

1. Si TUTK identifié → tester avec les outils de Nozomi Networks
2. Si Kalay identifié → vérifier la version du SDK
3. Tester l'interception du flux P2P non chiffré
4. Vérifier si l'AuthKey/DTLS est activé

## Étape 10 — Tentative d'accès au firmware OTA

**Objectif** : Récupérer le firmware pour analyse Binwalk

**Actions** :

1. Depuis l'APK décompilé, extraire l'URL de mise à jour OTA
2. Télécharger le firmware .bin
3. Analyser avec Binwalk dans HexStrike :

```
   POST /api/tools/binwalk
   {"target": "/tmp/firmware.bin", "options": "-Me"}
```

4. Extraire le système de fichiers et chercher :
    - `/etc/passwd` et `/etc/shadow`
    - Fichiers de configuration avec mots de passe en dur
    - Scripts de démarrage réseau
    - Configuration du service P2P

## Étape 11 — Rapport final enrichi

**Objectif** : Compiler toutes les découvertes dans un rapport PDF professionnel

**Livrables** :

- Rapport PDF avec toutes les phases documentées
- Schéma d'architecture réseau
- Matrice de risques
- Recommandations de sécurité détaillées