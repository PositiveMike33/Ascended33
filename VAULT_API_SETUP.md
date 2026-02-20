# OBSIDIAN VAULT REST API — Configuration Guide

## ❌ Error 401 — L'authentification échoue

Le message d'erreur `401 Client Error: Unauthorized` signifie que l'API key Obsidian n'est pas configurée correctement ou n'existe pas.

---

## ✅ Solution : Configuration Rapide (3 étapes)

### Étape 1: Obtenir votre API Key depuis Obsidian

1. **Ouvrir Obsidian** (s'assurer que D:\Vault est ouvert)
2. **Aller à Settings**
   - Cliquer sur le petit **gear icon** (⚙️) en bas à gauche
3. **Trouver le plugin "Local REST API"**
   - Settings → **Community Plugins**
   - Si le plugin n'est pas installé:
     - Cliquer **Browse**
     - Chercher "Local REST API"
     - Installer
     - **Activer le toggle** (S'assurer qu'il est ON)
4. **Copier l'API Key**
   - Dans la liste des plugins, chercher "Local REST API"
   - Cliquer l'**icône gear** à côté du plugin
   - Vous verrez votre API Key (longue chaîne alphanumeric)
   - **Copier** (Ctrl+C)

**Exemple d'API Key:**
```
khu29d8fh29d89hd29dh29hd29j2h0d9j20j20d  (vraiment long!)
```

### Étape 2: Ajouter l'API Key à config/config.yaml

1. **Ouvrir** `config/config.yaml` dans VSCode
2. **Trouver la section vault**:
   ```yaml
   vault:
     mode: "rest_api"
     base_url: "http://localhost:27123"
     api_key: ""              # ← C'EST LA LIGNE À MODIFIER
     vault_path: "D:/Vault"
   ```

3. **Remplacer** la ligne vide par votre clé:
   ```yaml
   api_key: "khu29d8fh29d89hd29dh29hd29j2h0d9j20j20d"
   ```

4. **Sauvegarder** le fichier (Ctrl+S)

### Étape 3: Tester la Connexion

```bash
python3 test-vault-connection.py
```

**Résultat attendu:**
```
[1/5] Loading configuration...
  ✓ Mode: rest_api
  ✓ Base URL: http://localhost:27123
  ✓ API Key: ****... (20 chars)

[2/5] Checking API key...
  ✓ API key is set (43 chars)

[3/5] Testing Obsidian Vault connection...
  ✓ Vault API reachable (HTTP 200)

[4/5] Testing authentication...
  ✓ Authentication successful!

[5/5] Testing vault operations...
  ✓ Successfully read template (1234 chars)
  ✓ Vault client works!

✓ ALL TESTS PASSED - Vault connection is working!
```

---

## 🔧 Troubleshooting

### "API key is EMPTY!"

**Solution:**
- Vérifier que vous avez bien copié la clé depuis Obsidian
- Vérifier qu'il n'y a pas d'espaces vides
- Vérifier la syntaxe YAML dans config.yaml
  ```yaml
  api_key: "votre_clé_ici"  # ✓ Correct
  api_key: votre_clé_ici     # ✗ Faux (guillemets manquants)
  api_key:  ""                # ✗ Faux (vide)
  ```

### "Cannot connect to http://localhost:27123"

**Solution:**
1. Vérifier qu'Obsidian est en cours d'exécution (vérifier system tray)
2. Vérifier que D:\Vault est ouvert dans Obsidian
3. Vérifier que le plugin "Local REST API" est **ACTIVÉ**
   - Settings → Community Plugins
   - Trouver "Local REST API"
   - Vérifier que le toggle est ON (bleu/vert)
4. Si Obsidian écoute sur un port différent:
   - Vérifier dans les settings du plugin
   - Mettre à jour `config/config.yaml`: `base_url: "http://localhost:27123"`

### "Authentication FAILED (401 Unauthorized)"

**Solutions:**
1. **Vérifier la clé API:**
   - Est-elle complètement copiée? (Pas de troncature)
   - N'y a-t-il pas d'espaces au début/fin?
   - Regénérez-la: Settings → Local REST API → Refresh

2. **Vérifier le format dans config.yaml:**
   ```yaml
   api_key: "KEY_WITHOUT_SPACES"  # ✓ Correct
   api_key: "KEY WITH SPACES"      # ✗ Peut causer problèmes
   api_key: " KEY_HERE"            # ✗ Espace au début
   ```

3. **Redémarrer Obsidian:**
   - Fermer Obsidian complètement
   - Rouvrir Obsidian
   - Réessayer

### Les trois tests échouent?

Démarrer par le diagnostic complet:
```bash
# 1. Vérifier que Obsidian run
ps aux | grep Obsidian

# 2. Vérifier que port 27123 écoute
netstat -ltn | grep 27123

# 3. Vérifier manualmente la connexion
curl -v http://localhost:27123/

# 4. Tester avec clé API
curl -v -H "Authorization: Bearer YOUR_API_KEY" http://localhost:27123/vault/
```

---

## ✨ Après Configuration

Une fois que tout fonctionne:

1. **Streamlit Dashboard:**
   - Rafraîchir la page (F5)
   - Cliquer **"🔄 Full Vault Sync"**
   - Voir le message ✓ de succès

2. **OPSEC Operations:**
   ```bash
   ./launch-opsec-session.sh "Test" "self" "osint"
   ```
   - Les opérations s'auto-loggent dans Vault
   - Vérifier: D:\Vault\Security\Operations\

3. **Recherche:**
   - Utiliser **Vault Quick Search** dans Streamlit
   - Rechercher par nom, tag, ou mot-clé

---

## 📚 Documentation Complète

- **[CLAUDE.md](CLAUDE.md)** — Architecture complète du système
- **[OPSEC_GUIDE.md](OPSEC_GUIDE.md)** — Système OPSEC complet
- **[README.md](README.md)** — Vue d'ensemble du projet

---

## 🆘 Besoin d'aide?

1. **Exécuter le test:**
   ```bash
   python3 test-vault-connection.py
   ```

2. **Vérifier les logs:**
   ```bash
   tail -f ~/.config/obsidian/logs/app.log
   ```

3. **Consulter la doc du plugin:**
   - https://github.com/coddingtonbear/obsidian-local-rest-api

---

*Last Updated: 2026-02-19*
*Ascended33 Obsidian Vault Integration*
