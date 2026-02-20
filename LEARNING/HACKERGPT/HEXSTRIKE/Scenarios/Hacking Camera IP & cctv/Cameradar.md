## Github
[https://github.com/Ullaakut/cameradar](https://github.com/Ullaakut/cameradar)[](https://github.com/Ullaakut/cameradar)]
## Résumé de la vidéo : Piratage de caméras IP (CCTV)

Cette vidéo de **43 minutes** (publiée le 11 mai 2025) présente une discussion approfondie entre David Bombal et OccupyTheWeb (OTW) sur les vulnérabilités des caméras IP et leurs techniques d'exploitation.[[youtube](https://www.youtube.com/watch?v=yMAWcHP6yn8&t=1991s)]​

## Contexte et cas d'usage réel

OTW révèle qu'il y a environ trois ans, le gouvernement ukrainien a sollicité son équipe pour pirater **900 caméras** afin de surveiller les mouvements russes pendant la guerre. Cette mission souligne l'importance stratégique du contrôle des caméras : "Celui qui contrôle les caméras contrôle le flux d'information".[[youtube](https://www.youtube.com/watch?v=yMAWcHP6yn8&t=1991s)]​

## Démonstrations techniques

## Reconnaissance et accès initial

La vidéo présente plusieurs techniques pratiques:[[youtube](https://www.youtube.com/watch?v=yMAWcHP6yn8&t=1991s)]​

1. **Scan réseau** : Utilisation de `nmap` pour découvrir les caméras Hikvision sur le réseau local (192.168.1.x)
    
2. **Identification des ports** : Découverte du port RTSP 554 utilisé pour le streaming vidéo
    
3. **Accès via VLC** : Connexion directe aux flux RTSP en utilisant `rtsp://192.168.1.4:554`
    
4. **Mots de passe par défaut** : Démonstration que de nombreuses caméras utilisent toujours admin/[vide] comme identifiants
    

## Outils de craquage de mots de passe

**Cameradar** : Outil principal démontré, fonctionnant avec Docker, qui:[[youtube](https://www.youtube.com/watch?v=yMAWcHP6yn8&t=1991s)]​

- Utilise des listes de dictionnaires pour attaquer les identifiants
    
- Peut être personnalisé avec des listes de mots de passe (SecLists)
    
- Teste automatiquement les combinaisons username/password
    

## Concepts techniques essentiels

## Protocole RTSP

Le **Real-Time Streaming Protocol** est expliqué comme:[[youtube](https://www.youtube.com/watch?v=yMAWcHP6yn8&t=1991s)]​

- Port par défaut : 554 (parfois 8554 ou 5554)
    
- Utilisé pour le streaming en direct, distinct de l'authentification HTTP/HTTPS
    
- Maintient un état de connexion, contrairement à HTTP
    

## Vulnérabilités spécifiques

**Vulnérabilité Dahua (CVE-2021-33044/045)** : Faille majeure permettant:[[youtube](https://www.youtube.com/watch?v=yMAWcHP6yn8&t=1991s)]​

- Contournement de l'authentification en usurpant l'adresse 127.0.0.1
    
- Accès administrateur sans mot de passe
    
- Ajout de comptes utilisateurs persistants
    

## Fabricants concernés

Les caméras **Hikvision** et **Dahua** sont particulièrement vulnérables:[[youtube](https://www.youtube.com/watch?v=yMAWcHP6yn8&t=1991s)]​

- Présentes dans des millions d'installations mondiales
    
- Souvent revendues sous d'autres marques (white label)
    
- Plusieurs pays (États-Unis, Royaume-Uni) les ont interdites dans les sites sensibles
    
- Questions soulevées sur une facilité de piratage intentionnelle
    

## Observations de sécurité

OTW partage ses constatations après avoir accédé à des centaines de caméras:[[youtube](https://www.youtube.com/watch?v=yMAWcHP6yn8&t=1991s)]​

- **Plus de 90%** ont un compte "admin" (admin, admin1, admin2, etc.)
    
- **5-10%** conservent les identifiants par défaut
    
- Beaucoup utilisent la "sécurité par obscurité" (ports non standard comme 8085)
    
- Fréquemment en HTTP plutôt qu'HTTPS
    

## Recommandations de sécurité

La vidéo insiste sur:[[youtube](https://www.youtube.com/watch?v=yMAWcHP6yn8&t=1991s)]​

1. **Ne jamais** utiliser les mots de passe par défaut
    
2. Implémenter l'authentification à deux facteurs (2FA)
    
3. Héberger les caméras localement sans accès Internet
    
4. Mettre à jour régulièrement le firmware pour corriger les vulnérabilités
    

## Approche pédagogique

OTW et David Bombal soulignent l'importance de comprendre les technologies sous-jacentes plutôt que de simplement utiliser des outils. Cette approche permet aux professionnels de la sécurité de développer de nouvelles techniques lorsque les vulnérabilités connues sont corrigées.[[youtube](https://www.youtube.com/watch?v=yMAWcHP6yn8&t=1991s)]​

**Note importante** : Toutes les démonstrations sont présentées à des fins éducatives uniquement, et les auteurs insistent sur l'illégalité du piratage de caméras sans autorisation.[[youtube](https://www.youtube.com/watch?v=yMAWcHP6yn8&t=1991s)]​