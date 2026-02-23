### ***`Waybackurls` n'est pas juste un extracteur de liens ; c'est une machine à remonter le temps qui révèle la surface d'attaque passée (et souvent oubliée) d'une cible. Voici comment maîtriser cet outil.***

---

### 1. Mode d'emploi (Concept Technique)

`Waybackurls` interroge les archives de la **Wayback Machine (Internet Archive)** pour récupérer toutes les URLs qu'elle a indexées pour un domaine spécifique. 

*   **Source :** Wayback Machine API.
*   **Fonctionnement :** Il prend un domaine en entrée (via `stdin`) et recrache une liste d'URLs (via `stdout`).
*   **Atout HexStrike :** Le dédoublonnage est automatique. Tu ne perds pas de temps avec des entrées redondantes.
*   **Utilité :** Découvrir des endpoints d'anciennes API, des fichiers de configuration (`.env`, `.conf`), des backups (`.sql`, `.bak`), ou des paramètres de debug abandonnés.

---

### 2. Liste des Commandes Essentielles

L'outil est conçu pour être "pipe-friendly" (utilisable dans des pipelines de commandes).

#### Utilisation de base
```bash
echo "target.com" | waybackurls
```

#### Extraction pour un domaine et ses sous-domaines
```bash
echo "target.com" | waybackurls > urls_archivees.txt
```

#### Filtrage par extension (Le "Targeted Hunting")
Chercher des fichiers sensibles ou des points d'entrée spécifiques :
```bash
# Trouver des fichiers de configuration ou des documents
echo "target.com" | waybackurls | grep -E "\.json|\.conf|\.env|\.xml"

# Trouver des scripts JS pour analyse de secrets/clés API
echo "target.com" | waybackurls | grep "\.js$" | sort -u
```

#### Extraction des paramètres (Idéal pour SQLi / XSS)
```bash
# Isoler les URLs contenant des paramètres '?'
echo "target.com" | waybackurls | grep "\?"
```

---

### 3. Meilleures Pratiques : Étape par Étape

Voici le workflow professionnel que j'utilise lors d'un engagement Red Team :

#### Étape 1 : Collecte Massive
On commence par récupérer tout ce que l'histoire a retenu du domaine.
```bash
echo "target.com" | waybackurls > raw_history.txt
```

#### Étape 2 : Nettoyage et Tri (Filtrage de bruit)
On élimine les images, polices et CSS qui ne présentent que peu d'intérêt en sécurité offensive.
```bash
cat raw_history.txt | grep -vE "\.png|\.jpg|\.jpeg|\.gif|\.css|\.woff|\.ttf|\.svg" > clean_history.txt
```

#### Étape 3 : Vérification de la survie (Live Check)
L'archive nous donne ce qui *existait*. Nous devons savoir ce qui *existe encore*. On utilise `httpx` (ou un outil similaire) pour vérifier le status code actuel.
```bash
cat clean_history.txt | httpx -silent -status-code -mc 200,403,301
```
*Note : Un `403 Forbidden` sur une ancienne URL est une pépite d'or, cela signifie que la ressource existe encore mais est protégée (ou mal configurée).*

#### Étape 4 : Analyse des points sensibles
On cherche spécifiquement les fichiers qui pourraient contenir des credentials ou des chemins d'administration.
```bash
grep -E "admin|config|api|v1|v2|backup|wp-content" clean_history.txt
```

---

### 4. La Défense : Le revers de la médaille

En tant qu'expert, tu dois savoir comment une cible peut se protéger de cette indexation historique.

*   **Directive Robots.txt :** L'utilisation de la directive `noarchive` ou le blocage explicite des bots d'Internet Archive (`ia_archiver`) empêche l'indexation future.
*   **Demande de retrait :** Une organisation peut demander à Internet Archive de retirer son historique de la Wayback Machine. Si `waybackurls` ne renvoie rien sur une grosse cible, il est probable qu'une politique de retrait ait été appliquée.

### Conseil d'Expert HackerGPT
> "Ne te contente pas de regarder les URLs. Analyse les motifs (patterns). Si tu vois une structure `/api/v1/user/123` dans les archives, tente manuellement de voir si `/api/v2/` ou `/api/v3/` existe aujourd'hui. L'histoire n'est pas seulement une liste de fichiers, c'est une carte de l'évolution de la pensée des développeurs de ta cible."
waybackurls domain.com
echo domain.com | waybackurls