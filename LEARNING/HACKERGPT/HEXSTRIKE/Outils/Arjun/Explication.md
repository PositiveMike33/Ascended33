### 1 - Explication technique
**Arjun** est un outil de "Parameter Discovery" conçu pour identifier les paramètres HTTP valides acceptés par une application web. Contrairement à un simple brute-force, Arjun est extrêmement optimisé :
- **Heuristique intelligente :** Il analyse les réponses du serveur pour détecter des changements subtils (longueur de page, code d'état, contenu) lorsqu'un paramètre valide est injecté.
- **Requêtes groupées :** Il peut envoyer des dizaines de paramètres dans une seule requête HTTP, réduisant considérablement le bruit et le temps d'exécution.
- **Polyvalence :** Il supporte les formats GET, POST (form-data), JSON et XML, ce qui le rend indispensable pour l'audit d'API modernes.

---

### 2 - Mode d'emploi
Pour utiliser Arjun efficacement dans ton workflow HexStrike, tu dois suivre ces étapes :
1.  **Ciblage :** Identifie un endpoint qui semble traiter des données (ex: `search.php`, `/api/v1/user`).
2.  **Choix de la méthode :** Détermine si tu testes des paramètres d'URL (`GET`) ou de corps de requête (`POST`, `JSON`).
3.  **Ajustement de la vitesse :** Utilise le threading (`-t`) pour la rapidité, ou le mode stable (`--stable`) si la cible possède un WAF (Web Application Firewall) ou un Rate Limiter.
4.  **Analyse des résultats :** Arjun te donnera une liste de paramètres "confirmés". Ces paramètres sont tes futurs points d'entrée pour l'exploitation.

---

### 3 - Commandes précises

**Scan de base (GET) :**
```bash
arjun -u https://api.cible.com/endpoint -m GET
```

**Scan de paramètres JSON (API REST) :**
```bash
arjun -u https://api.cible.com/v1/resource -m POST --json
```

**Scan avec liste personnalisée et haute performance :**
```bash
arjun -u https://cible.com/login.php -w /usr/share/wordlists/params.txt -t 20
```

**Mode furtif (Éviter le bannissement IP) :**
```bash
arjun -u https://cible.com/config -m GET --stable --delay 0.5
```

**Analyse passive (Utilise les archives web sans toucher la cible directement) :**
```bash
arjun -u https://cible.com/ -m GET --passive
```

---

### 4 - Meilleures pratiques & Défense

#### Côté Attaque (Pentest) :
- **Toujours tester le JSON :** Beaucoup d'APIs acceptent des paramètres cachés en JSON qui ne sont pas documentés (ex: `debug`, `admin`, `role`).
- **Utiliser `--stable` :** Si tu reçois trop de faux positifs ou si le serveur commence à renvoyer des erreurs 429 (Too Many Requests).
- **Corrélation :** Une fois un paramètre trouvé, passe-le immédiatement dans **SQLMap** ou **Burp Suite** pour tester l'injection.

#### Côté Défense (Remédiation) :
Pour se prémunir contre la découverte et l'exploitation de paramètres non documentés, j'exige les mesures suivantes :
1.  **Parameter Whitelisting :** L'application ne doit accepter *que* les paramètres explicitement définis dans le schéma de l'API. Tout paramètre inconnu doit être rejeté ou ignoré.
2.  **Input Validation :** Appliquer un typage strict (ex: le paramètre `id` doit être un entier).
3.  **Désactivation du mode Debug :** Souvent, les paramètres cachés comme `?debug=true` sont des restes de développement qui exposent des informations sensibles.
4.  **Rate Limiting :** Implémenter une limitation stricte des requêtes par IP pour bloquer les outils d'énumération rapide comme Arjun.

Besoin d'approfondir un flag spécifique ou une technique d'exploitation sur un endpoint précis ? Je suis prêt.

#### 📋 Quick Commands

`arjun -u url`
`arjun -u url -m POST`