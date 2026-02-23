# 🔌 MCP MASTERCLASS — Connecter Claude à Tes Outils

**Date:** 14-02-2026  
**Niveau:** Débutant → Intermédiaire  
**Durée:** ~40 min (incluant installation)  
**Lien:** [[1_SKILLS_MASTERCLASS]] | [[3_PROMPTING_MASTERCLASS]] | [[4_INTEGRATION_3_PILIERS]]

---

## 🎯 OBJECTIF DE CE COURS

À la fin, tu pourras:
✅ Comprendre l'architecture MCP (Model Context Protocol)  
✅ Installer les MCP servers essentiels (filesystem, Obsidian, git)  
✅ Connecter Claude à tes fichiers Obsidian en temps réel  
✅ Utiliser MCP pour tes projets revenue + hacking  

---

## 📚 PARTIE 1 — THÉORIE FONDAMENTALE

### C'est quoi le MCP?

**MCP = USB-C universel pour connecter Claude à tes outils**

```
Claude (IA puissante)
    ↓
MCP Client (Gestionnaire de connexion)
    ↓
MCP Servers (Tes outils : fichiers, APIs, DB, Obsidian, etc.)
```

**Avant MCP:**
- Claude lisait seulement ce que tu collais manuellement
- Tu devais copier/coller ton contexte à chaque conversation

**Avec MCP:**
- Claude peut lire directement tes fichiers Obsidian
- Claude peut créer/modifier des fichiers
- Claude peut interroger ta base de données
- Claude peut interagir avec ton Git

---

### Les 3 Primitives MCP

| Primitive | Quoi | Exemple |
|-----------|------|---------|
| **Tools** | Fonctions que Claude appelle | Créer un fichier, rechercher dans Obsidian |
| **Resources** | Données que Claude lit | Contenu d'une note Obsidian |
| **Prompts** | Templates réutilisables | Prompts système, few-shot examples |

---

### Types de Serveurs MCP

**Local (STDIO)** — Tourne sur ta machine
- Accès fichiers locaux, apps desktop
- Exemple: `filesystem`, `git`, `obsidian-local`

**Remote (HTTP)** — Tourne sur le cloud
- Accès APIs externes, services web
- Exemple: `GitHub MCP`, `Notion`, `Google Calendar`

---

## 🛠️ PARTIE 2 — INSTALLER LES MCP ESSENTIELS

### Serveurs prioritaires pour TOI

| Priorité | Serveur | Pourquoi |
|----------|---------|---------|
| ⭐⭐⭐ | **filesystem** | Lire/modifier tes fichiers Vault |
| ⭐⭐⭐ | **obsidian** | Accès direct à tes notes Obsidian |
| ⭐⭐⭐ | **fetch** | Scraper web, APIs |
| ⭐⭐ | **git** | Gérer tes repos (commits, branches) |
| ⭐⭐ | **sqlite** | Interroger ta DB (KALI labs, prospects) |

---

### Installation — WINDOWS

#### Prérequis
- Node.js installé (version 18+)
- Claude Desktop (version récente)

#### Step 1: Ouvrir config Claude

Sur Windows:
```
C:\Users\[TonNom]\AppData\Roaming\Claude\claude_desktop_config.json
```

Ou ouvre ce fichier directement:
```
%APPDATA%\Claude\claude_desktop_config.json
```

#### Step 2: Configuration de base

Édite le fichier JSON:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-filesystem", "D:\\Vault\\Vault"]
    },
    "fetch": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-fetch"]
    },
    "git": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-git", "D:\\Vault\\Vault"]
    }
  }
}
```

#### Step 3: Redémarrer Claude

Ferme complètement Claude et relance.

Vérifie si les MCP sont connectés:
- Vois le 🔌 icon en bas à gauche
- Clique → Doit montrer "filesystem", "fetch", "git"

---

## 🎯 EXEMPLE 1 — MCP FILESYSTEM

### Accès à tes fichiers du Vault

Maintenant que c'est installé, tu peux:

**À Claude:** "Lis le fichier SECURITY_AUDIT_LEADS.md et donne-moi le top 5 des meilleurs prospects"

**Claude fait:** 
- Accède automatiquement au filesystem
- Trouve `D:\Vault\Vault\🔐_SECURITY_AUDIT_PROJECT\SECURITY_AUDIT_LEADS.md`
- Le lit
- Extrait le top 5

**Pas de copy/paste manuelle!** 🚀

---

## 🔐 EXEMPLE 2 — MCP POUR TES CTF LABS

### Connecter KALI labs à Claude

Une fois que tu as KALI sync script exécuté, tu peux:

**À Claude:** "Lis les résultats du test_runner.py dans /tmp/claude_workspace/test_results.json et dis-moi quels payloads SQL injection n'ont pas fonctionné"

**Claude fait:**
- Accède au filesystem KALI
- Lit le JSON
- Analyse les failures
- Suggère fixes

---

## 🤖 EXEMPLE 3 — MCP GIT

### Automatiser ton vault Git

**À Claude:** "Crée un commit avec message 'Add SECURITY_AUDIT_PROJECT structure' et push vers main"

**Claude fait:**
- `git add` les nouveaux fichiers
- `git commit` avec ton message
- `git push` vers remote

---

## 📚 PARTIE 3 — MCP + TON VAULT

### Setup complet MCP pour Vault

Copie cette config complète dans ton `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-filesystem", "D:\\Vault\\Vault"]
    },
    "fetch": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-fetch"]
    },
    "git": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-git", "D:\\Vault\\Vault"]
    }
  }
}
```

**Redémarrer Claude après!**

---

## 🎬 EXERCICE 1 — Tester MCP Filesystem

### Test simple:

À Claude, dis:
```
Lis le fichier SECURITY_AUDIT_SERVICE.md dans mon Vault 
et donne-moi le résumé de l'offre en 3 lignes.
```

Si Claude peut le faire sans que tu copies/colles = ✅ MCP filesystem marche!

---

## 🎬 EXERCICE 2 — Automatiser une tâche répétée

### Avant MCP:
1. Tu ouvres SECURITY_AUDIT_LEADS.md
2. Tu copies manuellement chaque prospect
3. Tu les colles dans Claude
4. Claude les analyse
5. Tu copies la réponse ailleurs

**= 10 minutes, 5 copy/paste**

### Avec MCP:
**À Claude:** "Analyse tous les prospects dans SECURITY_AUDIT_LEADS.md et crée une nouvelle note PROSPECTS_QUALIFIED.md avec les top 10, scorés 1-10"

Claude fait tout en 30 secondes. ✅

---

## 🔒 SÉCURITÉ MCP

### Rules immuables

❌ **Ne jamais:**
- Exposer ton MCP config sur GitHub (contient chemins privés)
- Utiliser MCP pour accéder à des fichiers sensibles sans vérification
- Laisser Claude modifier les fichiers critiques sans révision

✅ **À faire:**
- Vérifier que les permissions sont correctes
- Un humain doit valider les modifications critiques
- Utiliser des variables d'environnement pour credentials
- Teste chaque MCP avant production

---

## 📖 DÉCOUVERTE — Autres MCP Servers

**Registre officiel:** https://registry.smithery.ai

Serveurs utiles pour toi:

| Serveur | Utilité | Status |
|---------|---------|--------|
| **Obsidian** | Lire/écrire notes directement | ⭐ À installer |
| **Notion** | Accès Notion DB | À considérer |
| **GitHub** | PR reviews, issues | À considérer |
| **Stripe** | Gerer payments | À considérer later |

---

## 🎬 EXERCICE 3 — Installer MCP Obsidian (BONUS)

Si tu veux la version ULTRA (Obsidian MCP):

```json
{
  "mcpServers": {
    "obsidian": {
      "command": "node",
      "args": ["/chemin/vers/obsidian-mcp-server.js"],
      "env": {
        "OBSIDIAN_VAULT_PATH": "D:\\Vault\\Vault"
      }
    }
  }
}
```

Alors Claude peut:
- Lire notes par tag (#revenu, #hacking)
- Créer notes formatées avec templates
- Générer liens bidirectionnels
- Mettre à jour le DASHBOARD en temps réel

---

## ✅ CHECKLIST FINALE

- [ ] J'ai installé Node.js
- [ ] J'ai édité `claude_desktop_config.json`
- [ ] J'ai redémarré Claude
- [ ] J'ai vérifié que les MCP sont connectés (🔌 icon)
- [ ] J'ai testé filesystem (lis 1 fichier Vault)
- [ ] J'ai testé fetch (scrape 1 page web)
- [ ] J'ai testé git (fais 1 commit)

---

## 🎯 PROCHAINE ÉTAPE

Voir: [[3_PROMPTING_MASTERCLASS]] — Parler comme un pro à Claude  
Voir: [[4_INTEGRATION_3_PILIERS]] — Combiner Skills + MCP + Prompts

---

**Tags:** #mcp #automation #claude #tools #integration #14-02-2026
