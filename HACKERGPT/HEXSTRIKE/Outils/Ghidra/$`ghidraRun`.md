# 🎓 LEÇON : Maîtriser le lancement avec `ghidraRun`  
  
**📝 Ce que fait cette commande  
`ghidraRun` est le script de lancement principal (shell script sur Linux/macOS, batch sur Windows) de la suite de reverse engineering **Ghidra**.  
  
Techniquement, ce script :  
1. Vérifie la présence et la version du **JDK (Java Development Kit)** requis.  
2. Configure les variables d'environnement et le *classpath* Java.  
3. Initialise l'interface graphique (GUI) de Ghidra.  
4. Charge les modules et extensions installés.  
  
## 🎯 Pourquoi on l'utilise  
C'est la méthode standard et recommandée pour démarrer Ghidra. Au lieu d'appeler manuellement la machine virtuelle Java avec des dizaines d'arguments complexes, `ghidraRun` automatise tout le processus pour garantir que l'outil dispose de la mémoire et des bibliothèques nécessaires pour fonctionner de manière stable.  
  
## 🔍 Scénarios appropriés  
  
1. **Analyse de Malware Statique :** Tu as récupéré un échantillon suspect et tu souhaites le désassembler pour comprendre son comportement sans l'exécuter.  
2. **Audit de Sécurité Logicielle :** Tu possèdes un binaire propriétaire (sans accès au code source) et tu dois chercher des vulnérabilités potentielles comme des buffer overflows.  
3. **Compétition CTF (Capture The Flag) :** Tu es face à un challenge de "Reverse" et tu dois rapidement identifier la logique de vérification d'un flag dans un exécutable compilé.  
  
## ⚠️ Précautions  
* **Environnement Isolé :** Ne lance jamais Ghidra via `ghidraRun` pour analyser un malware sur ton système hôte. Utilise toujours une machine virtuelle (VM) isolée (type Kali Linux ou Flare-VM).  
* **Version du JDK :** Ghidra est exigeant. Si `ghidraRun` échoue, vérifie que tu utilises la version exacte du JDK requise (actuellement JDK 17+ pour les versions récentes).  
* **Ressources :** Ghidra est gourmand en RAM. Assure-toi d'avoir au moins 4Go à 8Go de RAM disponibles pour les gros projets.  
  
## 💡 Variantes utiles  
  
Bien que `ghidraRun` soit le point d'entrée GUI, voici les alternatives critiques :  
  
* **`./support/analyzeHeadless` :**  
La version "sans tête" (ligne de commande uniquement). Utilisée pour automatiser l'analyse de centaines de fichiers via des scripts sans ouvrir l'interface graphique.  
```bash  
./support/analyzeHeadless ~/Documents/Projets MonProjet -import ~/Malware/sample.exe  
```  
  
* **Modification de `launch.properties` :**  
Ce n'est pas une commande, mais un fichier lié. Si `ghidraRun` est trop lent ou manque de mémoire, tu modifies les paramètres `VMARGS` dans `support/launch.properties` pour augmenter la RAM allouée (ex: `-Xmx4G`).  
  
---  
  
**Expert Tip :** Sur Kali Linux, assure-toi d'être dans le répertoire d'installation de Ghidra pour exécuter `./ghidraRun`. Pour plus de confort, crée un alias dans ton `.zshrc` ou `.bashrc` :  
`alias ghidra='/chemin/vers/ghidra/ghidraRun'`  
  
Prêt à désassembler ton premier binaire ?**