# $`ffuf -u url -X POST -d "param=FUZZ"`

  
Aujourd'hui, nous allons décortiquer une commande fondamentale pour tester la robustesse des formulaires et des API : l'utilisation du fuzzing via la méthode POST.  
  
---  

  
La commande cible :  
`ffuf -u https://cible.com/endpoint -X POST -d "param=FUZZ" -w wordlist.txt`  
  
**📝 Ce que fait cette commande  
Cette commande effectue un test de force brute (fuzzing) sur le **corps** d'une requête HTTP.  
- **`-u`** : Définit l'URL cible (l'endpoint qui reçoit les données).  
- **`-X POST`** : Force l'utilisation de la méthode HTTP POST (au lieu du GET par défaut).  
- **`-d "param=FUZZ"`** : Définit les données envoyées dans le corps de la requête. Le mot-clé **`FUZZ`** est l'endroit exact où `ffuf` injectera chaque ligne de ton dictionnaire.  
  
## 🎯 Pourquoi on l'utilise  
En cybersécurité offensive, de nombreuses vulnérabilités ne sont pas visibles dans l'URL (GET). Elles se cachent dans les données envoyées via des formulaires ou des appels API (POST). Utiliser `ffuf` ici permet d'automatiser la recherche de valeurs valides, de paramètres cachés ou de tester des injections sans manipulation manuelle répétitive.  
  
## 🔍 Scénarios appropriés  
1. **Brute-force de formulaire d'authentification** : Tester une liste de mots de passe sur un paramètre `password=FUZZ` pour identifier un compte vulnérable.  
2. **Recherche d'ID de session ou de jetons** : Tester si un paramètre (ex: `id=FUZZ`) renvoie des données différentes, ce qui pourrait indiquer une IDOR (Insecure Direct Object Reference).  
3. **Test d'injection (SQL/NoSQL)** : Envoyer des payloads spécifiques (ex: `' OR 1=1--`) via le paramètre pour observer les erreurs de base de données ou les changements de comportement de l'application.  
  
## ⚠️ Précautions  
* **Autorisation** : Ne lance jamais cette commande sur un système sans accord écrit (ROE). Le fuzzing génère beaucoup de logs.  
* **Déni de Service (DoS)** : Par défaut, `ffuf` est extrêmement rapide. Une cadence trop élevée peut faire tomber un serveur fragile. Utilise `-p 0.1` pour ajouter un délai si nécessaire.  
* **Altération des données** : Le fuzzing POST peut créer des milliers d'entrées inutiles dans la base de données de la cible (ex: création de comptes fictifs).  
  
## 💡 Variantes utiles  
  
**1. Filtrer les réponses inutiles (La plus importante) :**  
Si toutes les requêtes renvoient une page de 1240 octets, utilise `-fs` pour masquer ce bruit et ne voir que ce qui sort de l'ordinaire.  
```bash  
ffuf -u url -X POST -d "param=FUZZ" -w wordlist.txt -fs 1240  
```  
  
**2. Fuzzer le nom du paramètre lui-même :**  
Utile pour découvrir des paramètres cachés ou de debug (ex: `debug=true`).  
```bash  
ffuf -u url -X POST -d "FUZZ=test" -w params_list.txt  
```  
  
**3. Ajouter des Headers (JSON API) :**  
Si tu travailles sur une API moderne, tu dois souvent préciser le Content-Type.  
```bash  
ffuf -u url -X POST -H "Content-Type: application/json" -d '{"username": "admin", "password": "FUZZ"}' -w wordlist.txt  
```  
  
---  
**Conseil d'expert :** Analyse toujours une requête légitime avec Burp Suite avant de lancer `ffuf` afin de copier exactement la structure des données POST attendue par le serveur.  
  
Besoin d'approfondir un point spécifique sur le fuzzing d'API ? Mutons la commande !**