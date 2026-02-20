# Cadre Légal HexStrike — Québec & Canada

> *Ce document est la fondation légale de toute opération HexStrike.*
> *À lire avant le premier engagement. À relire régulièrement.*

---

## Lois Applicables

### Code Criminel du Canada — Art. 342.1 : Utilisation non autorisée d'ordinateur

**Ce qui est criminel :**
> Quiconque, frauduleusement et sans apparence de droit, obtient directement ou indirectement un service ordinateur est coupable d'une infraction.

En termes simples : accéder à un système informatique **sans autorisation explicite du propriétaire** est un acte criminel, peu importe l'intention.

**Peine maximale :** Jusqu'à 10 ans d'emprisonnement pour les cas graves.

### Art. 342.2 : Possession d'outils informatiques pour commettre une infraction

La simple possession d'outils conçus pour commettre des infractions (si l'intention criminelle peut être prouvée) est un crime.

**Protection HexStrike :** Toujours avoir une documentation d'autorisation qui prouve la légitimité de l'utilisation des outils.

### Loi sur la Protection des Renseignements Personnels et les Documents Électroniques (LPRPDE — fédérale)

- Toute collecte de données personnelles doit avoir un but légitime
- Les données personnelles collectées lors d'un engagement doivent être sécurisées et détruites après l'engagement
- Rapport de confidentialité des données à inclure dans tout rapport client

### Loi 25 du Québec (Loi modernisant des dispositions législatives en matière de protection des renseignements personnels)

- Entrée en vigueur progressive 2022–2023
- Les organisations québécoises doivent gérer les incidents de confidentialité
- Un rapport HexStrike qui identifie une fuite de données doit recommander une notification à la Commission d'accès à l'information (CAI)

---

## Ce Qui Est Légal

| Activité | Conditions légales |
|----------|-------------------|
| OSINT sur données publiques | Données accessibles au public, pas d'authentification requise |
| Bug bounty | Dans le scope défini par le programme, programme actif et public |
| Pentest | Autorisation écrite signée du propriétaire du système |
| Recherche en lab | Systèmes propres ou VMs isolées, sans connexion aux systèmes tiers |
| Reverse engineering | Sur logiciels dont tu es propriétaire, ou avec autorisation |
| Divulgation de vulnérabilité | Via divulgation responsable, délai minimum 90 jours |

---

## Ce Qui Est Criminel

| Activité | Risque légal |
|----------|-------------|
| Scanner un réseau sans autorisation | Art. 342.1 — accès non autorisé |
| Accéder à un compte avec des credentials trouvés | Art. 342.1 + vol d'identité |
| Intercepter des communications | Art. 184 Code criminel |
| Installer un keylogger sans consentement | Art. 342.1 + espionnage |
| Vendre des données volées | Multiples chefs criminels |
| Menacer de divulguer une vuln sans délai | Extorsion — Art. 346 |

---

## Formulaire d'Autorisation HexStrike

*Ce formulaire doit être signé avant tout engagement (pentest, audit, OSINT ciblé).*

```
AUTORISATION D'ENGAGEMENT HexStrike
====================================

Client : ________________________________
Représentant autorisé : _________________
Titre : _________________________________
Date : __________________________________

Systèmes inclus dans le scope :
- Domaines : ____________________________
- Plages IP : ___________________________
- Applications : ________________________

Systèmes EXCLUS du scope (ne pas tester) :
- _______________________________________

Durée de l'engagement :
Du : ___________________ Au : ___________

Types de tests autorisés :
[ ] OSINT passif
[ ] Scan de vulnérabilités (non-destructif)
[ ] Tests d'intrusion (avec précautions)
[ ] Ingénierie sociale (si explicitement coché)
[ ] Tests physiques (si explicitement coché)

Restrictions particulières :
_________________________________________

Contact d'urgence (disponible 24/7 pendant l'engagement) :
Nom : _________________________ Tél : _______________

En signant ce document, je certifie être propriétaire ou avoir l'autorité légale
pour autoriser les tests sur les systèmes listés ci-dessus.

Signature client : ___________________________ Date : ________
Signature HexStrike : ________________________ Date : ________
```

---

## Règles d'Or OSINT

1. **Données publiques uniquement** — Si un compte/login est requis pour accéder à l'info, stop.
2. **Pas de social engineering actif** — Observer est légal. Contacter en se faisant passer pour quelqu'un d'autre ne l'est pas.
3. **Pas de scraping massif qui surcharge les serveurs** — Peut être interprété comme une DoS.
4. **Documenter les sources** — Chaque information dans le rapport doit avoir une source vérifiable.

---

## Règles d'Or Bug Bounty

1. **Lire le scope complet avant de commencer** — Les domaines hors scope sont off-limits.
2. **Pas de DoS, pas de spam** — Même pour tester une vulnérabilité.
3. **Pas d'accès aux données d'autres utilisateurs** — Trouver la vulnérabilité suffit. Extraire des données réelles est criminel.
4. **Divulgation uniquement via la plateforme** — Jamais directement à la presse ou public.
5. **Respecter le délai de réponse du programme** avant d'escalader.

---

## Divulgation Responsable — Standard HexStrike

1. **Jour 0** : Découverte de la vulnérabilité. Documenter avec preuves minimales.
2. **Jour 1** : Notifier le responsable sécurité de l'organisation (via email sécurisé ou formulaire officiel).
3. **Jours 1–14** : Attendre accusé de réception.
4. **Jour 14** : Si pas de réponse, relance et notification que le délai court.
5. **Jour 90** : Si pas de correction ou communication, divulgation publique partielle (sans exploit fonctionnel).
6. **Après correction** : Divulgation complète avec credit au chercheur (si désiré).

---

## Ressources Légales Québec/Canada

- [CRTC — Cybersécurité](https://www.crtc.gc.ca)
- [Centre canadien pour la cybersécurité](https://www.cyber.gc.ca)
- [Commission d'accès à l'information du Québec](https://www.cai.gouv.qc.ca)
- [Code criminel du Canada — Partie IX](https://laws-lois.justice.gc.ca/fra/lois/C-46/)

---

*Document fondateur HexStrike — Révisé le 2026-02-20*
