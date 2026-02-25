Voici la liste des 8 commandes essentielles Windows Repair avec leur fonctionnalité :

1. **sfc /scannow**  
    Analyse et répare automatiquement les fichiers système Windows corrompus.
    
2. **DISM /Online /Cleanup-Image /RestoreHealth**  
    Répare l’image de Windows (fichiers système) en ligne sans nécessiter une réinstallation.
    
3. **chkdsk C: /f /r**  
    Vérifie et corrige les erreurs du disque dur, repère et répare les secteurs défectueux.
    
4. **bootrec /fixmbr | /fixboot**  
    Répare le secteur de démarrage ou le Master Boot Record, utile si Windows ne démarre plus.
    
5. **net stop cryptSvc**  
    Arrête le service de chiffrement, souvent nécessaire lors de certaines réparations système.
    
6. **net stop bits**  
    Arrête le service BITS (Background Intelligent Transfer Service), utile pour résoudre des problèmes de mises à jour Windows.
    
7. **net stop msiserver**  
    Interrompt le service Windows Installer, ce qui peut aider à débloquer l’installation de logiciels ou de mises à jour.
    
8. **regedit**  
    Ouvre l’éditeur du registre Windows pour modifier des paramètres avancés manuellement.
    