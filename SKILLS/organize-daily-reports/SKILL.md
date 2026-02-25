---
name: organize-daily-reports
description: Organise et classe les fichiers quotidiens "Bilan du jour" et "Bilan du soir" à partir du dossier D:/Vault/Vault/THIRTY3/daily vers la structure REPORT/Declassified Report. Crée automatiquement les dossiers datés (DD-MM-YYYY) et détecte les doublons. À utiliser chaque jour pour traiter les nouveaux fichiers commençant par (YYYY-MM-DD). Préserve les liens Obsidian et met en évidence les doublons pour analyse manuelle.
user-invocable: true
---

# Organize Daily Reports

## Vue d'ensemble

Cette skill automatise l'organisation de vos rapports quotidiens Obsidian. Elle :

1. **Détecte** les fichiers commençant par `(YYYY-MM-DD)` dans `D:/Vault/Vault/THIRTY3/daily`
2. **Crée** automatiquement les dossiers datés (format DD-MM-YYYY)
3. **Déplace** les fichiers "Bilan du jour" et "Bilan du soir" vers la structure REPORT appropriée
4. **Détecte les doublons** et les met en évidence avec un suffixe `_1.md` pour analyse manuelle
5. **Préserve** les liens Obsidian en mettant à jour les chemins

## Flux de travail

### Étape 1 : Détection
Scan du dossier `D:/Vault/Vault/THIRTY3/daily` pour les fichiers avec pattern `(YYYY-MM-DD)`.

### Étape 2 : Identification de la destination
Pour chaque date trouvée (ex: 2026-02-22) :
- Extrait le mois/année (02/2026 = Février)
- Détermine la semaine (16-22 VACANCE pour le 22)
- Construit le chemin : `D:/Vault/Vault/REPORT/Declassified Report/02 Rapport Février/Semaine du 16 au 22 VACANCE/22-02-2026/`

### Étape 3 : Création des dossiers
Si le dossier n'existe pas, le crée automatiquement.

### Étape 4 : Déplacement des fichiers
Déplace uniquement :
- `(YYYY-MM-DD) Bilan du jour.md`
- `(YYYY-MM-DD) Bilan du soir.md`
- Tout autre fichier commençant par `(YYYY-MM-DD) ...`

### Étape 5 : Gestion des doublons
Si le fichier existe déjà à la destination :
- Renomme l'entrée sortante en `Bilan du jour_1.md` ou `Bilan du soir_1.md`
- **Met en évidence** le doublon pour analyse manuelle
- Affiche un rapport avec le chemin exact

### Étape 6 : Mise à jour des liens Obsidian
Analyse les autres fichiers Obsidian pour mettre à jour les liens cassés (si applicable).

## Résultat

Après exécution, vous recevrez un rapport détaillé :

```
✅ RAPPORT D'ORGANISATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📦 Fichiers déplacés :
  ✓ (2026-02-22) Bilan du jour.md 
    → D:/Vault/.../22-02-2026/

  ✓ (2026-02-22) Bilan du soir.md 
    → D:/Vault/.../22-02-2026/

⚠️  DOUBLONS DÉTECTÉS (à analyser) :
  ! (2026-02-22) Bilan du jour_1.md 
    → D:/Vault/.../22-02-2026/Bilan du jour_1.md
    (ancien fichier existait déjà)

📊 Résumé :
  • Fichiers traités : 2
  • Fichiers déplacés : 2
  • Doublons créés : 1
  • Temps : X secondes
```

## Notes importantes

- Les fichiers sont cherchés avec le pattern `(YYYY-MM-DD) ...` (parenthèses obligatoires)
- Les dossiers sont créés automatiquement s'ils n'existent pas
- Les doublons sont renommés en `_1.md` pour faciliter l'analyse
- Les liens Obsidian existants sont analysés mais pas modifiés automatiquement
- Exécutable manuellement ou via Hook quotidien
