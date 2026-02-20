# 🎓 Leçon : Audit global des processus avec `checksec`  
  
**📝 Ce que fait cette commande  
La commande `checksec --proc-all` analyse **l'intégralité des processus en cours d'exécution** sur le système. Elle inspecte chaque binaire chargé en mémoire pour vérifier la présence des mécanismes de protection modernes :  
* **RELRO (Relocation Read-Only) :** Protection de la table GOT (Global Offset Table).  
* **Stack Canary :** Détection des débordements de tampon (Buffer Overflow).  
* **NX (No-Execute) :** Empêche l'exécution de code sur la pile ou le tas.  
* **PIE (Position Independent Executable) :** Permet au binaire d'être chargé n'importe où en mémoire (essentiel pour l'ASLR).  
* **Fortify Source :** Vérifie si des fonctions sensibles (comme `strcpy`) sont remplacées par des versions sécurisées.  
  
## 🎯 Pourquoi on l'utilise  
En tant que pentester ou auditeur, cette commande est ton "scanner de santé" immédiat. Elle permet de :  
1. **Identifier les maillons faibles :** Repérer un service critique (serveur web, base de données) qui aurait été compilé sans protections, facilitant ainsi son exploitation.  
2. **Vérifier la configuration du kernel :** Elle confirme si l'ASLR est activé globalement sur le système.  
3. **Évaluer l'hygiène logicielle :** S'assurer que les applications tierces installées respectent les standards de sécurité actuels.  
  
## 🔍 Scénarios appropriés  
1. **Post-Exploitation / Élévation de privilèges :** Tu as un accès utilisateur limité. Tu lances `checksec --proc-all` pour trouver un processus tournant en `root` qui n'a pas de *Stack Canary* ou de *PIE*, en faisant une cible parfaite pour un exploit de type Buffer Overflow.  
2. **Audit de Hardening (Blue Team) :** Après avoir configuré un serveur de production, tu lances cette commande pour valider que tous les services exposés sont correctement durcis.  
3. **Analyse de Conteneurs :** Vérifier si les binaires à l'intérieur d'un conteneur Docker sont vulnérables avant leur déploiement.  
  
## ⚠️ Précautions  
* **Privilèges :** Pour obtenir des résultats complets sur tous les processus (notamment ceux appartenant à `root`), tu dois impérativement exécuter la commande avec `sudo`.  
* **Performance :** Sur un système avec des centaines de processus, l'analyse peut prendre quelques secondes et solliciter le CPU.  
* **Cadre légal :** N'utilise cet outil que sur des systèmes où tu possèdes une autorisation explicite (contrat de pentest ou ta propre machine).  
  
## 💡 Variantes utiles  
* **Cibler un seul processus :**  
```bash  
checksec --proc  
```  
*Utile pour se concentrer sur une cible spécifique après l'avoir identifiée via `top` ou `ps`.*  
  
* **Sortie formatée pour rapport (JSON) :**  
```bash  
checksec --proc-all --output=json  
```  
*Idéal pour intégrer les résultats dans un script d'automatisation ou un rapport d'audit.*  
  
* **Vérifier un fichier binaire avant exécution :**  
```bash  
checksec --file /usr/sbin/apache2  
```  
*Pratique pour analyser un programme sans avoir besoin de le lancer.*  
  
---  
**Conseil d'expert :** Si tu vois un processus en rouge (No Canary, No PIE, No NX), c'est là que ton travail d'exploitation commence. Reste éthique, reste curieux.  
  
Des questions sur une protection spécifique ?_**