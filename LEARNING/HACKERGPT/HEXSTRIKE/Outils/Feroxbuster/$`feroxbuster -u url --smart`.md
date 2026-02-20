---  
  # 🎓 Leçon HexStrike : Le Mode Smart de Feroxbuster  
  
`feroxbuster -u https://cible.com --smart`  

**📝 Ce que fait cette commande  
Cette commande lance une énumération de fichiers et répertoires sur une URL cible en activant le **"Smart Mode"**.  
  
En mode normal, un outil de brute-force se base uniquement sur les codes d'état HTTP (ex: 200 OK, 404 Not Found). Le mode `--smart` va plus loin : il analyse les réponses du serveur pour détecter les **faux positifs**. Il envoie des requêtes vers des chemins inexistants (ex: `/al3atoire_12345`) pour observer comment le serveur réagit (longueur de page, nombre de mots, redirections) et filtre automatiquement les résultats similaires qui pollueraient ton scan.  
  
## 🎯 Pourquoi on l'utilise  
On l'utilise pour **éliminer le bruit**.  
De nombreux serveurs modernes sont configurés pour renvoyer un code `200 OK` ou une redirection même si la page n'existe pas (Soft 404). Sans le flag `--smart`, Feroxbuster pourrait t'afficher des milliers de résultats inutiles. Ce mode permet de gagner un temps précieux en ne montrant que ce qui est réellement "différent" et potentiellement intéressant.  
  
## 🔍 Scénarios appropriés  
1. **Applications Single Page (SPA) :** Les frameworks comme React ou Angular redirigent souvent toutes les erreurs vers `index.html`. Le mode smart identifie cette redondance et cache les doublons.  
2. **Serveurs avec Wildcard DNS :** Si n'importe quel sous-répertoire ou fichier renvoie vers une page de garde personnalisée.  
3. **WAF (Web Application Firewalls) :** Certains pare-feux modifient les réponses HTTP pour tromper les scanners. Le mode smart s'adapte à ces réponses spécifiques.  
  
## ⚠️ Précautions  
* **Bruit réseau :** Au démarrage, le mode `--smart` effectue plusieurs requêtes de calibration. C'est minime, mais à savoir.  
* **Faux négatifs rares :** Dans des cas très spécifiques, si une page légitime a exactement la même structure (taille/mots) qu'une page d'erreur, elle pourrait être masquée.  
* **Légalité :** Comme toujours, n'utilise cet outil que sur des périmètres où tu détiens une autorisation écrite (ROE).  
  
## 💡 Variantes utiles  
* **Avec extensions spécifiques :**  
`feroxbuster -u https://cible.com --smart -x php,txt,pdf`  
*(Cherche des fichiers spécifiques tout en filtrant les faux positifs)*  
* **Scan récursif limité :**  
`feroxbuster -u https://cible.com --smart -d 2`  
*(Active le mode intelligent mais limite la profondeur de recherche à 2 niveaux pour éviter de s'y perdre)*  
* **Mode silencieux pour scripts :**  
`feroxbuster -u https://cible.com --smart -q`  
*(N'affiche que les résultats finaux, idéal pour piper vers un autre outil)*  
  
---  
**Conseil d'expert :** En phase de reconnaissance, commence toujours par un scan `--smart`. Si tu vois que le serveur est "propre" (vraies 404), tu peux t'en passer, mais c'est ton meilleur bouclier contre l'infobésité en pentest.  
  
