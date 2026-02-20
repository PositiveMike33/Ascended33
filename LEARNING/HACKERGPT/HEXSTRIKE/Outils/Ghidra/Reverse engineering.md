# 🎓 Leçon : Lancer l'environnement de Reverse Engineering  
  
**📝 Ce que fait cette commande  
La commande `./ghidraRun` est un script shell (sous Linux/Kali) ou un fichier batch (sous Windows) qui sert de **bootstrapper** pour la suite Ghidra.  
  
Techniquement, elle :  
1. Vérifie la présence d'un environnement d'exécution Java (JRE) compatible.  
2. Configure le *classpath* et les variables d'environnement nécessaires.  
3. Alloue la mémoire initiale à la Machine Virtuelle Java (JVM).  
4. Lance l'interface graphique (GUI) de Ghidra.  
  
## 🎯 Pourquoi on l'utilise  
On l'utilise pour initialiser le "Project Manager". Sans ce script, tu devrais manuellement appeler Java en spécifiant des dizaines de bibliothèques `.jar`, ce qui est source d'erreurs. C'est la porte d'entrée pour passer d'un binaire binaire opaque (0101...) à une représentation lisible en langage C (décompilation).  
  
## 🔍 Scénarios appropriés  
  
1. **Analyse Statique de Malware :** Tu as récupéré un spécimen suspect. Tu lances `ghidraRun` pour importer l'exécutable, laisser l'auto-analyseur identifier les fonctions malveillantes et comprendre les intentions de l'attaquant sans exécuter le code.  
2. **Audit de Sécurité de Firmware :** Tu travailles sur un équipement IoT. Tu extrais le binaire du processeur et tu utilises Ghidra pour chercher des mots de passe "hardcodés" ou des vulnérabilités de type *buffer overflow* dans le code métier.  
3. **Interopérabilité et Rétro-conception :** Tu dois faire communiquer un logiciel moderne avec un vieux protocole propriétaire dont la documentation a disparu. Tu lances Ghidra pour reconstruire les structures de données du protocole à partir du client original.  
  
## ⚠️ Précautions  
* **Isolation :** Même si Ghidra fait principalement de l'analyse statique, certains scripts d'extension ou plugins peuvent déclencher des comportements imprévus. Travaille toujours dans une **VM isolée** lors de l'analyse de malwares réels.  
* **Ressources :** Ghidra est gourmand en RAM (Java oblige). Assure-toi d'avoir au moins 4Go à 8Go de RAM libre pour les gros projets.  
* **Légalité :** Le reverse engineering est soumis à des lois strictes (interdiction de contourner des mesures de protection technique sauf cas spécifiques comme l'interopérabilité ou la recherche en sécurité). Vérifie tes autorisations.  
  
## 💡 Variantes utiles  
  
1. **Allocation de mémoire personnalisée :**  
Si Ghidra plante sur un gros binaire, tu ne modifies pas `ghidraRun`, mais le fichier `support/launch.properties` pour augmenter `MAXMEM`. Cependant, tu peux vérifier ton environnement avec :  
```bash  
./support/analyzeHeadless --help  
```  
*(Pour l'analyse en ligne de commande sans interface graphique).*  
  
2. **Lancement en mode Debug :**  
Si Ghidra refuse de démarrer ou si un plugin plante :  
```bash  
./ghidraRun debug  
```  
Cela permet d'attacher un debugger Java pour voir exactement où le chargement échoue.  
  
3. **Exécution directe via le PATH :**  
Pour plus d'efficacité sur Kali, ajoute le dossier Ghidra à ton `$PATH`. Tu pourras alors simplement taper `ghidraRun` depuis n'importe quel répertoire de travail contenant tes binaires.  
  
---  
**Conseil d'expert :** "Avant de lancer l'analyse automatique après ton `./ghidraRun`, prends toujours le temps de vérifier si le format du binaire (ELF, PE, Mach-O) et l'architecture (x86, ARM, MIPS) ont été correctement détectés. Une mauvaise détection initiale rendra la décompilation incohérente."**