

Salut ! Ici **Nikto Expert**, ton instructeur de l'unité HexStrike. Aujourd'hui, nous allons disséquer la commande fondamentale de l'un des outils de scan de vulnérabilités web les plus emblématiques de Kali Linux : **Nikto**.  
  
Voici ta leçon sur la commande de base.  
  
---  
  
# 🎓 Leçon : Initiation au Scan Web avec Nikto  
  
**📝 Ce que fait cette commande  
`nikto -h url`  
  
La commande `nikto` (l'outil) associée au flag `-h` (pour *host*) lance une analyse automatisée contre un serveur web spécifique. Nikto va scanner la cible pour identifier :  
- Les fichiers et scripts potentiellement dangereux (plus de 6700 éléments).  
- Les versions de serveurs obsolètes.  
- Les problèmes de configuration (fichiers de backup, répertoires exposés).  
- L'absence de headers de sécurité essentiels (XSS-Protection, HSTS, etc.).  
  
## 🎯 Pourquoi on l'utilise  
En tant que pentester, on utilise cette commande pour **détecter les "low-hanging fruits"** (vulnérabilités faciles à exploiter). C'est un outil de reconnaissance active rapide qui permet d'avoir une vue d'ensemble de la surface d'attaque d'un serveur web avant de passer à des outils plus ciblés comme Burp Suite ou SQLMap.  
  
## 🔍 Scénarios appropriés  
1. **Audit de configuration rapide :** Vérifier si un serveur Apache ou Nginx fraîchement installé possède encore ses pages par défaut ou des méthodes HTTP dangereuses (comme `PUT` ou `TRACE`) activées.  
2. **Recherche de fichiers "oubliés" :** Identifier des fichiers de configuration type `config.php.bak` ou des répertoires `.git` exposés qui pourraient contenir des secrets.  
3. **Analyse de conformité des headers :** S'assurer que les en-têtes de sécurité recommandés par l'OWASP sont bien implémentés pour protéger les utilisateurs finaux.  
  
## ⚠️ Précautions  
- **Bruit (Stealth) :** Nikto est **extrêmement bruyant**. Il génère des milliers de requêtes HTTP en peu de temps. Il sera immédiatement repéré par n'importe quel IDS/IPS (système de détection d'intrusion).  
- **Légalité :** Ne lance jamais cette commande sur un domaine que tu ne possèdes pas ou pour lequel tu n'as pas d'autorisation écrite explicite.  
- **Impact :** Bien que généralement sûr, le scan de scripts CGI anciens peut parfois causer des ralentissements sur des serveurs très fragiles.  
  
## 💡 Variantes utiles  
Pour aller plus loin, voici comment optimiser ton scan :  
  
1. **Exporter les résultats :** Pour intégrer tes trouvailles dans un rapport.  
```bash  
nikto -h http://cible.com -o rapport.html -Format htm  
```  
2. **Passer par un proxy (Tor ou Burp) :** Pour masquer ton IP ou analyser les requêtes.  
```bash  
nikto -h http://cible.com -useproxy http://localhost:8080  
```  
3. **Scan spécifique (Tuning) :** Si tu veux uniquement chercher des injections SQL (type 9) et des fichiers intéressants (type 4).  
```bash  
nikto -h http://cible.com -Tuning 49  
```  
  
---  
**Conseil d'expert :** Nikto ne remplace pas une analyse manuelle, mais il est imbattable pour ne rien oublier lors de la phase d'énumération initiale. Reste éthique et bon hacking !**