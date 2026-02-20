
$`john --wordlist=rockyou.txt hash.txt`
  
---  
  
# 🎓 Leçon : Attaque par Dictionnaire avec John the Ripper  
  
**📝 Ce que fait cette commande  
`john --wordlist=rockyou.txt hash.txt`  
  
Cette commande lance **John the Ripper** pour effectuer une **attaque par dictionnaire** sur un fichier de condensats (hashes).  
- `john` : Appelle l'exécutable.  
- `--wordlist=rockyou.txt` : Indique à l'outil d'utiliser une liste de mots pré-existante (ici, le célèbre fichier *RockYou* contenant des millions de mots de passe fuités).  
- `hash.txt` : Le fichier cible contenant les empreintes numériques à casser. John tentera d'identifier automatiquement le type de hash (MD5, SHA-1, bcrypt, etc.) avant de commencer.  
  
## 🎯 Pourquoi on l'utilise  
En cybersécurité offensive, on ne devine pas les mots de passe caractère par caractère (brute-force pur) si l'on peut l'éviter, car c'est trop lent. On utilise cette commande pour **tester la résistance des mots de passe** face à des fuites de données connues. Si un mot de passe est dans *RockYou*, il est considéré comme compromis instantanément.  
  
## 🔍 Scénarios appropriés  
1. **Audit de conformité interne :** Vérifier si les employés d'une entreprise utilisent des mots de passe trop simples ou présents dans les bases de données de fuites mondiales.  
2. **Post-exploitation (Privilege Escalation) :** Après avoir extrait le fichier `/etc/shadow` d'un serveur Linux, pour tenter d'obtenir les accès "root" ou d'autres utilisateurs.  
3. **Capture The Flag (CTF) :** Identifier rapidement un hash trouvé dans une base de données web mal sécurisée lors d'un exercice de pénétration.  
  
## ⚠️ Précautions  
- **Cadre Légal :** N'utilisez cette commande que sur des fichiers dont vous êtes le propriétaire ou pour lesquels vous avez une autorisation écrite explicite (Mandat de Pentest).  
- **Ressources Système :** Le cassage de hash est intensif pour le CPU. Sur des algorithmes complexes (comme Argon2 ou bcrypt avec un coût élevé), cela peut faire chauffer votre machine de test.  
- **Stockage :** John stocke les mots de passe trouvés dans son fichier `john.pot`. Ne le supprimez pas par erreur.  
  
## 💡 Variantes utiles  
  
**1. Spécifier le format (Gain de temps massif) :**  
Si vous savez que le hash est du MD5, forcez le format pour éviter que John ne perde du temps à deviner.  
```bash  
john --format=Raw-MD5 --wordlist=rockyou.txt hash.txt  
```  
  
**2. Utiliser les règles de transformation (Mangles) :**  
Cette variante applique des règles (ex: ajouter "123" à la fin ou transformer "e" en "3") aux mots du dictionnaire.  
```bash  
john --wordlist=rockyou.txt --rules hash.txt  
```  
  
**3. Afficher les résultats :**  
Une fois l'attaque terminée, pour voir les mots de passe découverts :  
```bash  
john --show hash.txt  
```  
  
---  
*Fin de la leçon. Pratiquez avec éthique et rigueur. Des questions sur l'optimisation des règles de transformation ?***