---
name: protect-md-files
enabled: true
event: bash
pattern: rm\s+.*\.md|rm\s+-rf\s+.*\.md
action: warn
---

⚠️ **Suppression de fichier .md détectée !**

Tu es sur le point de supprimer une note Markdown de ton Vault.
- Les notes Obsidian sont précieuses et contiennent tes connaissances.
- Vérifie si c'est vraiment ce que tu veux faire.
- Si tu veux archiver, déplace plutôt vers un dossier `_ARCHIVE/`.

**Commande bloquée pour ta protection.**