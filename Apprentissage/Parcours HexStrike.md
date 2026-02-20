# Parcours HexStrike — De Débutant à Opérationnel

> *Ce parcours est ta roadmap. Pas un horaire rigide — une direction.*
> *Chaque module complété est une preuve THIRTY3.*

---

## Vision du Parcours

**Point de départ :** Débutant en cybersécurité
**Point d'arrivée :** Praticien HexStrike opérationnel — OSINT, Bug Bounty, Pentest, RE défensif

**Durée estimée :** 12–18 mois à cadence soutenue
**Engagement requis :** 1–2 heures par jour minimum

---

## Vue d'Ensemble

```
Phase 0 (Semaines 1-4)    : Fondations — Réseaux + Linux
Phase 1 (Semaines 5-12)   : OSINT Passif — Observer sans toucher
Phase 2 (Semaines 13-24)  : Sécurité Web — OWASP + Bug Bounty
Phase 3 (Semaines 25-52)  : Pentest — Kali + Labs + Certification
Phase 4 (An 2+)           : Opérationnel — Clients, OSCP, HexStrike
```

---

## Phase 0 — Fondations (Semaines 1–4)

**Objectif :** Comprendre le langage de la cybersécurité.

### Module 01 — Réseaux TCP/IP
Voir [[Modules/01 — Fondamentaux Reseaux TCP-IP]]

**Compétences à acquérir :**
- [ ] Modèle OSI — 7 couches, rôle de chacune
- [ ] TCP/IP — handshake, ports, protocoles courants
- [ ] DNS — comment ça fonctionne réellement
- [ ] HTTP/HTTPS — requêtes, réponses, en-têtes
- [ ] Subnetting de base (CIDR, plages IP)

**Ressources :**
- TryHackMe : Pre-Security Path (gratuit)
- YouTube : "Professor Messer Network+" (gratuit)

### Module 02 — Linux pour la Sécurité
Voir [[Modules/02 — Linux pour la Securite]]

**Compétences à acquérir :**
- [ ] Navigation filesystem, permissions
- [ ] Commandes essentielles (ls, grep, find, chmod, etc.)
- [ ] Scripting bash de base
- [ ] Gestion des processus et services
- [ ] Installation et configuration d'outils

**Ressources :**
- TryHackMe : Linux Fundamentals (3 parties, gratuit)
- OverTheWire : Bandit (wargame Linux, gratuit)

### Milestone Phase 0
> Compléter les 25 premières salles TryHackMe du Pre-Security Path
> Documenter dans `THIRTY3/Preuves/` quand c'est fait

---

## Phase 1 — OSINT Passif (Semaines 5–12)

**Objectif :** Maîtriser la collecte d'information légale et éthique.

### Module 03 — Introduction OSINT
Voir [[Modules/03 — Introduction OSINT]]

**Compétences à acquérir :**
- [ ] OSINT Framework — navigation et usage
- [ ] Google Dorks — maîtrise des opérateurs avancés
- [ ] theHarvester — collecte d'emails et sous-domaines
- [ ] Shodan — recherche d'infrastructure exposée
- [ ] Maltego CE — cartographie de relations
- [ ] Produire un rapport OSINT complet

**Practice :**
- Faire une investigation OSINT sur ta propre organisation / ton propre nom
- TryHackMe : OSINT rooms (Shodan.io, Google Dorking)

### Milestone Phase 1
> Compléter une investigation OSINT complète sur une cible autorisée
> Livrer un rapport au format [[HexStrike/OSINT/Templates/TPL — Rapport OSINT|Template OSINT]]

---

## Phase 2 — Sécurité Web + Bug Bounty (Semaines 13–24)

**Objectif :** Comprendre les vulnérabilités web et soumettre les premiers rapports.

### Module 04 — Sécurité Web — OWASP Top 10
Voir [[Modules/04 — Securite Web — OWASP Top 10]]

**Compétences à acquérir :**
- [ ] OWASP Top 10 — comprendre chaque catégorie
- [ ] XSS — reflété, stocké, DOM-based
- [ ] SQL Injection — détection et exploitation basique
- [ ] IDOR — identifier et exploiter les références directes
- [ ] Authentification — sessions, tokens, cookies
- [ ] Burp Suite — proxy, repeater, intruder basics

**Practice :**
- DVWA (Damn Vulnerable Web Application) en local
- HackTheBox — Web challenges (gratuit)
- TryHackMe — OWASP Top 10 room
- PortSwigger Web Security Academy (gratuit, excellent)

### Début Bug Bounty
- Créer un compte HackerOne et Bugcrowd
- Lire 20 rapports public "Disclosed" pour comprendre les standards
- Choisir 1 programme VDP avec large scope
- Soumettre les premiers rapports (même si low severity)

### Milestone Phase 2
> Soumettre 5 rapports de bug bounty (acceptés ou non — l'apprentissage compte)
> Obtenir au moins 1 rapport accepté (tout niveau)

---

## Phase 3 — Pentest + Certification (Semaines 25–52)

**Objectif :** Maîtriser la méthodologie pentest et obtenir une première certification.

### Module 05 — Introduction au Pentest
Voir [[Modules/05 — Introduction au Pentest]]

**Compétences à acquérir :**
- [ ] Kali Linux — setup et configuration
- [ ] Nmap — scanning avancé
- [ ] Metasploit — bases de l'exploitation
- [ ] Methodology PTES — les 6 phases
- [ ] Rédaction de rapport professionnel
- [ ] Post-exploitation de base

**Practice :**
- HackTheBox — Machines "Easy" (au moins 10)
- TryHackMe — Jr Penetration Tester Path
- VulnHub — machines locales

### Certification Cible : CompTIA Security+
Voir [[Certifications/CompTIA Security+]]

- Durée de préparation : 3–4 mois
- Contenu : Fondamentaux sécurité, cryptographie, gestion des risques
- Valeur : Reconnaissance internationale, porte d'entrée dans l'industrie

### Milestone Phase 3
> Compléter 10 machines HTB "Easy"
> Passer et réussir CompTIA Security+
> Livrer un premier pentest sur un système d'entraînement (Metasploitable) avec rapport complet

---

## Phase 4 — Opérationnel HexStrike (An 2+)

**Objectif :** Premiers clients, OSCP, développement de l'outil Ascended33.

### Activités
- [ ] Premiers engagements clients (commencer par l'entourage proche)
- [ ] Progression Bug Bounty — viser Medium et High
- [ ] Préparer OSCP (6–12 mois)
- [ ] Contribuer au développement d'Ascended33
- [ ] Construire la réputation HexStrike au Québec

### Certifications Phase 4
- [[Certifications/CEH — Certified Ethical Hacker|CEH]]
- [[Certifications/OSCP — Offensive Security|OSCP]] (objectif principal)

---

## Suivi de Progression — Dataview

```dataview
TABLE file.mtime AS "Modifié", status AS "Statut"
FROM "Apprentissage"
WHERE status != null
SORT file.mtime DESC
```

---

## Ressources Gratuites Essentielles

| Ressource | Type | Lien |
|-----------|------|------|
| TryHackMe | Labs guidés | tryhackme.com |
| HackTheBox | Labs/CTF | hackthebox.com |
| PortSwigger Academy | Web security | portswigger.net/web-security |
| OWASP | Référence | owasp.org |
| VulnHub | VMs locales | vulnhub.com |
| OverTheWire | Wargames | overthewire.org |
| PentesterLab | Web | pentesterlab.com |
| Cybrary | Cours vidéo | cybrary.it |

---

*Parcours HexStrike — THIRTY3 en action dans le monde cyber*
