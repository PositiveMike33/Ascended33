✅ Response from X8 Expert

Salut, ici l'expert **X8** de la suite HexStrike. Si tu cherches à débusquer des paramètres cachés ou non documentés avec une efficacité chirurgicale, tu es au bon endroit. 

**X8** est l'outil ultime de "Parameter Discovery" écrit en Rust. Sa force réside dans sa capacité à détecter des variations infimes dans les réponses HTTP (taille, temps de réponse, structure) pour identifier des vecteurs d'attaque invisibles à l'œil nu (IDOR, Debug modes, RCE via des paramètres cachés).

Voici le mode d'emploi avancé pour dominer tes engagements de Pentest.

---

### 1. Fondamentaux : Découverte de paramètres GET
C'est l'utilisation la plus courante. On cherche des variables comme `?debug=true`, `?admin=1`, etc.

```bash
x8 -u "https://api.target.com/v1/user" -w /usr/share/seclists/Discovery/Web-Content/burp-parameter-names.txt
```
*   **Technique :** X8 envoie des requêtes avec plusieurs paramètres simultanément pour gagner du temps, puis isole ceux qui provoquent un changement dans la réponse.

### 2. Paramètres POST (Formulaire & JSON)
Souvent, les développeurs cachent des fonctionnalités dans le corps de la requête.

**Pour du POST standard (x-www-form-urlencoded) :**
```bash
x8 -u "https://target.com/login" -m POST -w custom_params.txt
```

**Pour du JSON (Crucial pour les API modernes) :**
```bash
x8 -u "https://api.target.com/update" -m POST -X JSON -w parameters.txt
```
*   **Explication :** Le flag `-X JSON` instruit X8 d'injecter les paramètres dans une structure de dictionnaire JSON.

### 3. Techniques Avancées : Comparaison & Timing

#### A. Analyse par Timing (Blind Detection)
Si le serveur ne renvoie pas de différence de taille de page mais exécute une logique différente en arrière-plan (ex: recherche SQL lourde), on utilise le timing.
```bash
x8 -u "https://target.com/search" -w params.txt --check-time
```

#### B. Custom Headers & Cookies
Pour tester des zones authentifiées (indispensable en Pentest) :
```bash
x8 -u "https://target.com/admin/settings" -H "Authorization: Bearer <TOKEN>" -b "session=12345" -w params.txt
```

### 4. Stratégie de Wordlists (L'arsenal HexStrike)
Le choix de la liste détermine 90% du succès.
*   **SecLists :** `Discovery/Web-Content/burp-parameter-names.txt` (La base).
*   **Custom :** Crée des listes basées sur le contexte (ex: si c'est du Java, ajoute `debug`, `source`, `inspect`).

### 5. Optimisation et Performance
X8 est extrêmement rapide, mais tu peux ajuster son agressivité :
*   `--concurrency 10` : Nombre de threads (augmente pour la vitesse, baisse pour la discrétion).
*   `-p 100` : Nombre de paramètres par requête (X8 combine les tests pour optimiser le nombre de paquets).

---

### ANALYSE DE DÉFENSE (Blue Team Perspective)

Pour contrer ce type d'énumération, voici les recommandations que tu dois inclure dans tes rapports :

1.  **Parameter Hardening :** Implémenter une validation stricte (Allow-list). Tout paramètre non attendu par le schéma de l'API doit être rejeté ou ignoré silencieusement.
2.  **Logging & Monitoring :** Surveiller les pics de requêtes HTTP avec un grand nombre de paramètres inhabituels. Les outils comme X8 laissent une empreinte caractéristique si le nombre de paramètres par requête est élevé.
3.  **WAF (Web Application Firewall) :** Configurer des règles pour limiter le nombre de paramètres autorisés dans une seule requête GET ou POST.
4.  **Uniform Responses :** S'assurer que les erreurs renvoyées pour des paramètres invalides sont identiques en taille et en temps de réponse pour éviter les attaques par canal auxiliaire (side-channel).

---

**Un conseil d'expert :** Utilise toujours le flag `--output` pour sauvegarder tes découvertes. Une fois qu'un paramètre caché est trouvé (ex: `admin_mode`), passe immédiatement à l'étape suivante avec **Burp Suite** ou **ffuf** pour tester les valeurs de ce paramètre.

Besoin d'une commande spécifique pour un scénario particulier ? Dis-le moi.

#### 📋 Quick Commands

`x8 -u url -w wordlist``x8 -u url --json`