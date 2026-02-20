✅ Response from Hashcat Expert

Salut, je suis **HackerGPT**, ton expert Hashcat intégré à l'environnement **HexStrike**. 

Le cassage de condensats (hashing) est un art qui demande de la précision. Hashcat est l'outil le plus puissant au monde pour cela, car il exploite la puissance brute des GPU pour tester des milliards de combinaisons par seconde.

Voici ton mode d'emploi opérationnel pour maîtriser Hashcat comme un pro.

---

### 1. La Syntaxe Fondamentale
La structure de base d'une commande Hashcat est toujours la suivante :
**Shell Snippet**
```bash
hashcat [options] -m [mode] -a [attaque] [fichier_hash] [dictionnaire/masque/répertoire]
```





### 2. Identifier le Hash (-m)
Avant de lancer l'attaque, tu dois connaître l'algorithme.
- **0** : MD5
- **100** : SHA1
- **1000** : NTLM (Windows)
- **1800** : sha512crypt (Linux)
- **3200** : bcrypt
- **22000** : WPA/WPA2 (PMKID/EAPOL)

*Astuce HexStrike :* Si tu ignores le type, utilise `hashid -m [hash]` pour l'identifier.

---

### 3. Les Modes d'Attaque (-a)

#### A. Attaque par Dictionnaire (Mode 0)
C'est la base. On teste une liste de mots.
```bash
hashcat -m 0 -a 0 target.hash /usr/share/wordlists/rockyou.txt
```
**Optimisation avec Règles (-r) :** Pour augmenter tes chances, applique des mutations (majuscules, chiffres à la fin, etc.).
```bash
hashcat -m 0 -a 0 target.hash rockyou.txt -r rules/best64.rule
```
*Pourquoi ?* Les règles transforment "password" en "P4ssw0rd!", multipliant l'efficacité de ton dictionnaire.

#### B. Attaque Brute-Force & Masques (Mode 3)
Utilisé quand on connaît la structure du mot de passe.
- `?l` : minuscule [a-z]
- `?u` : majuscule [A-Z]
- `?d` : chiffre [0-9]
- `?s` : symbole [!@#...]
- `?a` : tout (all)

**Exemple :** Un mot de passe de 6 caractères commençant par une majuscule et finissant par deux chiffres.
```bash
hashcat -m 1000 -a 3 hash_ntlm.txt ?u?l?l?l?d?d
```

#### C. Attaque Combinée (Mode 1)
Combine deux dictionnaires. Si `dict1` contient "Admin" et `dict2` contient "2023", Hashcat testera "Admin2023".
```bash
hashcat -m 0 -a 1 hashes.txt dict1.txt dict2.txt
```

#### D. Attaque Hybride (Mode 6 et 7)
- **6 :** Dictionnaire + Masque (ex: `motdepasse123`)
- **7 :** Masque + Dictionnaire (ex: `123motdepasse`)
```bash
hashcat -m 0 -a 6 hashes.txt dict.txt ?d?d?d
```

---

### 4. Optimisation de la Performance (GPU)
Dans HexStrike, nous voulons que le GPU brûle les hashs le plus vite possible.
- `-w 3` ou `-w 4` : Définit le profil de charge (Workload). 4 est le maximum (peut ralentir le système, mais booste le cracking).
- `-O` : Active les kernels optimisés (plus rapide, mais limite la longueur des mots de passe).

**Commande optimisée :**
```bash
hashcat -m 1000 target.txt rockyou.txt -w 4 -O --status
```

---

### 5. La Défense : Pourquoi certains résistent ?
En tant qu'expert, tu dois comprendre la résistance des cibles :
- **Bcrypt (3200) / Argon2 :** Ces algorithmes utilisent un "coût" (work factor). Ils sont délibérément lents pour empêcher le brute-force massif.
- **Salage (Salting) :** Un sel unique par utilisateur empêche l'utilisation de Rainbow Tables.
- **Délais progressifs :** Une défense système qui bloque les tentatives après X échecs, rendant le cracking hors-ligne (sur un dump de base de données) la seule option viable.

---

### Rappel de Sécurité (HackerGPT)
> **ATTENTION :** L'utilisation de Hashcat doit se faire exclusivement sur des systèmes dont tu es propriétaire ou pour lesquels tu as une autorisation écrite explicite (Mandat de Pentest). Le cassage de mots de passe sans autorisation est illégal et contraire à l'éthique de la communauté HexStrike.

**Un hash spécifique à soumettre ou une règle personnalisée à créer ? Dis-moi, je suis prêt.**

#### 📋 Quick Commands

`hashcat -m 0 hash.txt wordlist.txt``hashcat -a 3 hash.txt ?a?a?a?a`