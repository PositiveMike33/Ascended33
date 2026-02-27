---
name: protect-git-commands
enabled: true
event: bash
pattern: git\s+(push\s+--force|push\s+-f|reset\s+--hard|clean\s+-fd|checkout\s+--\s+\.)
action: warn
---

🚨 **Commande Git risquée détectée !**

Cette commande peut causer des pertes de données ou affecter le dépôt partagé :

| Commande | Risque |
|----------|--------|
| `git push --force` | Écrase l'historique distant |
| `git reset --hard` | Perd les modifications non commitées |
| `git clean -fd` | Supprime fichiers non trackés |
| `git checkout -- .` | Annule toutes les modifications |

**Alternatives sûres :**
- `git push --force-with-lease` (vérifie avant d'écraser)
- `git stash` (sauvegarde avant reset)
- `git clean -fd --dry-run` (prévisualise d'abord)

**Veux-tu vraiment exécuter cette commande risquée ?**