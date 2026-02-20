

Salut, ici **Radare2 Expert**. Bienvenue dans cette session HexStrike. Aujourd'hui, nous décomposons la "Sainte Trinité" du reverse engineering statique sous `r2`.  
  
Voici ta leçon sur l'enchaînement de commandes : `aaa; afl; pdf @ main`  
  
---  
  
**📝 Ce que fait cette commande  
Cette séquence automatise les premières étapes cruciales de l'analyse d'un binaire :  
  
1. **`aaa` (Analyze All) :** Analyse en profondeur le binaire. Radare2 cherche les symboles, les références de cordes (strings), les sauts d'appels et construit le graphe de contrôle de flux.  
2. **`afl` (Analyze Functions List) :** Affiche la liste de toutes les fonctions identifiées lors de l'analyse. Elle donne une vue d'ensemble de la structure du programme (adresses, taille, noms).  
3. **`pdf @ main` (Print Disassembly Function) :** Désassemble et affiche le code assembleur de la fonction spécifiée (ici `main`). Le `@` agit comme un pointeur temporaire.  
  
## 🎯 Pourquoi on l'utilise  
On l'utilise pour passer instantanément d'un fichier binaire brut à une **compréhension logique du code**. C'est le point d'entrée standard de tout "reverser" : on analyse tout, on liste les capacités, et on plonge directement dans le cœur du programme (`main`) pour comprendre son comportement initial.  
  
## 🔍 Scénarios appropriés  
1. **Analyse de Malware :** Identifier rapidement si le `main` appelle des fonctions suspectes (connexions réseau, chiffrement de fichiers, persistance).  
2. **Challenge CTF (pwn/reverse) :** Localiser des vulnérabilités classiques comme `gets()` ou `strcpy()` au sein de la fonction principale pour préparer un exploit.  
3. **Vérification de compilation :** S'assurer qu'un binaire critique a été compilé avec les bonnes protections ou vérifier l'implémentation d'un algorithme spécifique sans accès au code source.  
  
## ⚠️ Précautions  
* **Légalité :** N'analyse que des binaires pour lesquels tu possèdes une autorisation explicite. Le reverse engineering de logiciels propriétaires peut violer les Conditions Générales d'Utilisation (EULA).  
* **Analyse statique vs dynamique :** Bien que `aaa` soit une analyse statique, sois prudent. Dans un environnement de production, analyse toujours les binaires suspects dans une machine virtuelle isolée (Kali Linux en Sandbox).  
* **Faux positifs :** `aaa` peut parfois mal interpréter des données comme du code sur des binaires obfusqués.  
  
## 💡 Variantes utiles  
* **`aa; afl`** : Une analyse plus rapide (`aa` au lieu de `aaa`) si le binaire est massif et que tu n'as pas besoin d'une analyse exhaustive des références croisées.  
* **`pdf @ sym.main`** : Si le binaire possède des symboles de débogage, le point d'entrée sera souvent préfixé par `sym.`.  
* **`VV @ main`** : Remplace `pdf` par `VV` pour passer en **mode graphique visuel** (ASCII Art). Cela permet de visualiser les branchements (if/else, boucles) de manière beaucoup plus intuitive.  
  
---  
**Conseil d'expert :** L'analyse est la base de tout. Si `aaa` échoue à trouver `main`, utilise la commande `iE` pour chercher le "Entry Point" réel du binaire.  
  
Bon hacking éthique !**