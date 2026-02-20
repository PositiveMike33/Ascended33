# Module 01 — Fondamentaux Réseaux TCP/IP

**Phase :** 0 — Fondations
**Durée estimée :** 1–2 semaines
**Statut :** pending / in-progress / completed

---

## Pourquoi les Réseaux ?

Toute la cybersécurité repose sur les réseaux.
Un pentest commence par le scan de ports.
Un OSINT commence par la reconnaissance DNS.
Une attaque passe par le réseau.
Sans comprendre le réseau — tu travailles dans le noir.

---

## Concepts Clés

### Le Modèle OSI (7 Couches)

| Couche | Nom | Protocoles | Ce qui t'intéresse |
|--------|-----|-----------|-------------------|
| 7 | Application | HTTP, FTP, DNS, SMTP | Les données applicatives |
| 6 | Présentation | TLS/SSL, JPEG | Chiffrement |
| 5 | Session | NetBIOS | Sessions |
| 4 | Transport | TCP, UDP | Ports, connexions |
| 3 | Réseau | IP, ICMP, ARP | Adresses IP, routing |
| 2 | Liaison | Ethernet, WiFi | MACs, switches |
| 1 | Physique | Câbles, WiFi | Le hardware |

**Pour la cybersécurité, maîtriser les couches 3, 4, 7 en priorité.**

---

### TCP vs UDP

**TCP (Transmission Control Protocol) :**
- Connexion établie avant envoi de données (3-way handshake)
- Fiable — accusé de réception pour chaque paquet
- Utilisé par : HTTP, HTTPS, SSH, FTP, SMTP

**3-way handshake TCP :**
```
Client → Serveur : SYN (je veux me connecter)
Serveur → Client : SYN-ACK (d'accord, prêt)
Client → Serveur : ACK (compris, on commence)
```

**UDP (User Datagram Protocol) :**
- Pas de connexion établie
- Rapide mais non fiable (pas d'accusé de réception)
- Utilisé par : DNS, DHCP, VoIP, streaming, jeux en ligne

**Nmap scanne TCP par défaut — ajouter `-sU` pour UDP**

---

### Ports Importants en Cybersécurité

| Port | Protocole | Service | Intérêt |
|------|-----------|---------|---------|
| 21 | TCP | FTP | Transfert fichiers — souvent mal configuré |
| 22 | TCP | SSH | Administration distante |
| 23 | TCP | Telnet | Non chiffré — vulnérable |
| 25 | TCP | SMTP | Email — vecteur phishing |
| 53 | TCP/UDP | DNS | Zone transfer, DNS recon |
| 80 | TCP | HTTP | Web non chiffré |
| 443 | TCP | HTTPS | Web chiffré |
| 445 | TCP | SMB | Partage fichiers Windows — EternalBlue |
| 3306 | TCP | MySQL | Base de données |
| 3389 | TCP | RDP | Bureau distant Windows |
| 8080 | TCP | HTTP alt | Panels admin, APIs |

**À mémoriser : si tu vois un de ces ports ouvert dans Nmap, tu sais quoi chercher.**

---

### Adressage IP et Subnetting

```
# IPv4 — 4 octets de 0 à 255
192.168.1.100

# Classes d'adresses privées (non-routables sur internet)
10.0.0.0/8       → 10.x.x.x
172.16.0.0/12    → 172.16.x.x à 172.31.x.x
192.168.0.0/16   → 192.168.x.x

# Notation CIDR
192.168.1.0/24   → 256 adresses (192.168.1.0 à 192.168.1.255)
192.168.1.0/16   → 65536 adresses
192.168.1.0/32   → 1 adresse (hôte unique)

# Commandes utiles
ip a                          # Voir ses propres IPs (Linux)
ipconfig /all                 # Windows
ping 192.168.1.1              # Tester la connectivité
traceroute 8.8.8.8            # Tracer la route
```

---

### DNS — Domain Name System

**Comment ça fonctionne :**
```
1. Tu tapes "google.com" dans ton navigateur
2. Ton OS demande au serveur DNS configuré (ex: 8.8.8.8)
3. Le DNS résout "google.com" → 142.250.x.x
4. Ton navigateur se connecte à 142.250.x.x
```

**Types d'enregistrements DNS importants :**

| Type | Signification | Exemple |
|------|--------------|---------|
| A | IPv4 de l'hôte | google.com → 142.250.x.x |
| AAAA | IPv6 de l'hôte | google.com → 2607:... |
| MX | Serveur email | mail.google.com |
| NS | Serveur de noms | ns1.google.com |
| CNAME | Alias | www → site.com |
| TXT | Texte (SPF, DKIM) | "v=spf1 include:..." |
| PTR | Reverse DNS | IP → nom |

```bash
# Requêtes DNS depuis le terminal
dig google.com A          # IPv4
dig google.com MX         # Serveurs email
dig google.com NS         # Serveurs de noms
dig google.com TXT        # Enregistrements texte
dig google.com ANY        # Tout

# Reverse DNS
dig -x 8.8.8.8

# Zone transfer (si mal configuré — vulnérabilité)
dig @ns1.target.com target.com AXFR
```

---

### HTTP/HTTPS

**Structure d'une requête HTTP :**
```http
GET /page.html HTTP/1.1
Host: example.com
User-Agent: Mozilla/5.0
Accept: text/html
Cookie: session=abc123

[Corps vide pour GET]
```

**Structure d'une réponse HTTP :**
```http
HTTP/1.1 200 OK
Content-Type: text/html
Set-Cookie: session=xyz789

<html>...</html>
```

**Codes de statut HTTP :**
| Code | Signification |
|------|--------------|
| 200 | OK |
| 301/302 | Redirection |
| 403 | Forbidden (accès refusé) |
| 404 | Not Found |
| 500 | Erreur serveur |

**HTTPS = HTTP + TLS**
- Le trafic est chiffré entre le navigateur et le serveur
- Burp Suite agit comme proxy MITM pour intercepter HTTPS

---

## Exercices Pratiques

```bash
# Exercice 1 — Explorer le réseau local
ip a                           # Voir son IP
ip route                       # Voir la passerelle (gateway)
nmap -sP 192.168.1.0/24       # Scanner le réseau local (légal sur son propre réseau)

# Exercice 2 — Analyse DNS
dig google.com ANY
dig amazon.com MX
dig @8.8.8.8 youtube.com A

# Exercice 3 — Capture réseau
# Lancer Wireshark, ouvrir un navigateur, visiter http://example.com
# Observer les paquets TCP SYN, SYN-ACK, ACK
# Observer la requête GET HTTP

# Exercice 4 — Ports et services
nmap -sV localhost             # Scanner ses propres services
netstat -tulnp                 # Voir les ports ouverts localement
ss -tulnp                      # Alternative moderne à netstat
```

---

## Ressources

| Ressource | Lien | Gratuit |
|-----------|------|---------|
| TryHackMe — Pre-Security | tryhackme.com | Oui |
| TryHackMe — Network Fundamentals | tryhackme.com | Oui |
| Professor Messer Network+ | professormesser.com | Oui |
| Practical Networking (YouTube) | youtube.com | Oui |
| Wireshark Sample PCAPs | wiki.wireshark.org/SampleCaptures | Oui |

---

## Checklist de Validation

- [ ] Je comprends les 7 couches OSI et leur rôle
- [ ] Je sais expliquer le 3-way handshake TCP
- [ ] Je connais les 10 ports les plus importants en cybersécurité
- [ ] Je sais lire une adresse IP en notation CIDR
- [ ] Je peux faire une requête DNS avec `dig`
- [ ] Je comprends la structure d'une requête HTTP
- [ ] J'ai capturé et analysé du trafic réseau avec Wireshark

**Quand toutes les cases sont cochées → Module 01 : Complété**

---

*Module 01 — Parcours HexStrike | Retour vers [[Parcours HexStrike]]*
