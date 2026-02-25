[[12-02-2026]] 
La vidéo est un cours complet « CS50’s Intro to Cybersecurity » de Harvard (7 h 44) qui introduit les bases de la cybersécurité pour publics techniques et non techniques. [youtube](https://www.youtube.com/watch?v=9HOpanT0GRs)

### Structure du cours
- Sécuriser les comptes (authentification, autorisation, mots de passe, 2FA, attaques par dictionnaire/brute force, credential stuffing, phishing, social engineering). [youtube](https://www.youtube.com/watch?v=9HOpanT0GRs)
- Sécuriser les données (hashing, salage, stockage des mots de passe, fonctions de hachage cryptographiques, NIST, gestion des fuites de bases de données). [youtube](https://www.youtube.com/watch?v=9HOpanT0GRs)
- Sécuriser les systèmes (malware, virus, vers, keyloggers, antivirus, mises à jour, principe de moindre privilège, défense en profondeur). [youtube](https://www.youtube.com/watch?v=9HOpanT0GRs)
- Sécuriser les logiciels (vulnérabilités, XSS, CSRF, injection, erreurs de design, bonnes pratiques de dev). [youtube](https://www.youtube.com/watch?v=9HOpanT0GRs)
- Préserver la vie privée (traçage, fingerprinting navigateur, cookies, référents HTTP, politiques de confidentialité, outils comme Tor/Tails évoqués). [youtube](https://www.youtube.com/watch?v=9HOpanT0GRs)

### Concepts clés martelés
- La sécurité est relative: jeu coûts/bénéfices pour toi vs risques/récompenses pour l’attaquant, jamais absolue. [youtube](https://www.youtube.com/watch?v=9HOpanT0GRs)
- Usabilité vs sécurité: plus un mécanisme est **fort**, plus les humains contournent (post‑it, mots de passe simples, réutilisation). [youtube](https://www.youtube.com/watch?v=9HOpanT0GRs)
- Mots de passe: longueur ≥ 8, idéalement longues passphrases; éviter dictionnaire, schémas évidents, réutilisation; utiliser gestionnaire de mots de passe + 2FA (app ou clé, SMS en dernier recours). [youtube](https://www.youtube.com/watch?v=9HOpanT0GRs)
- Stockage mots de passe côté serveur: ne jamais stocker en clair; utiliser hachage à sens unique + sel + fonctions lentes (type modernes dérivées de SHA/bcrypt/scrypt/Argon2) conformément aux recommandations NIST. [youtube](https://www.youtube.com/watch?v=9HOpanT0GRs)
- Cryptographie:  
  - Secret/symmetric key (AES, 3DES): même clé pour chiffrer/déchiffrer. [youtube](https://www.youtube.com/watch?v=9HOpanT0GRs)
  - Public key (RSA, Diffie‑Hellman, signatures numériques): paire clé publique/clé privée, chiffrement, échange de clés, signatures, passkeys/WebAuthn. [youtube](https://www.youtube.com/watch?v=9HOpanT0GRs)
- Web & attaques applicatives: XSS (réfléchi, stocké, DOM), CSRF, mauvaise utilisation de GET/POST (ex: « Buy Now »), validation/échappement serveur, politiques de sécurité (CSP, referrer-policy). [youtube](https://www.youtube.com/watch?v=9HOpanT0GRs)
- Vie privée & traçage: referer HTTP, fingerprinting (infos navigateur, plugins, résolution, etc.), risques de corrélation, quelques contre‑mesures (paramètres navigateur, extensions, réseaux comme Tor, systèmes live comme Tails). [youtube](https://www.youtube.com/watch?v=9HOpanT0GRs)

### Pratiques recommandées pour l’utilisateur
- Activer 2FA partout, préférer appli d’authentification ou clé physique aux SMS. [youtube](https://www.youtube.com/watch?v=9HOpanT0GRs)
- Utiliser un gestionnaire de mots de passe et des mots de passe uniques, longs et aléatoires pour chaque service. [youtube](https://www.youtube.com/watch?v=9HOpanT0GRs)
- Ne jamais réutiliser les mots de passe importants (mail, banque, cloud). [youtube](https://www.youtube.com/watch?v=9HOpanT0GRs)
- Se méfier du phishing/social engineering: vérifier l’URL, ne pas cliquer directement depuis emails sensibles, douter des demandes d’infos perso. [youtube](https://www.youtube.com/watch?v=9HOpanT0GRs)
- Éviter d’entrer ses identifiants sur des machines ou réseaux non maîtrisés, garder ses propres appareils à jour et protégés. [youtube](https://www.youtube.com/watch?v=9HOpanT0GRs)

En bref, le cours donne les fondations théoriques (hash, crypto, web) + des stratégies concrètes pour durcir comptes, données, systèmes, logiciels et vie privée, en insistant sur le compromis permanent entre sécurité et utilisabilité. [youtube](https://www.youtube.com/watch?v=9HOpanT0GRs)