# Guide d'Utilisation - Organize Daily Reports

## Vue d'ensemble

Le skill `organize-daily-reports` automatise le classement des fichiers de rapports quotidiens dans votre Vault Obsidian.

**Fonctionnalités principales:**
- Détecte les fichiers commençant par `(YYYY-MM-DD) Bilan du jour` et `(YYYY-MM-DD) Bilan du soir`
- Déplace les fichiers vers les dossiers de destination appropriés
- Crée automatiquement les dossiers de destination au format `DD-MM-YYYY`
- Gère les fichiers en double en les renommant avec le suffixe `_1.md`
- Vérifie que les liens Obsidian ne sont pas cassés

## Utilisation Manuel

### Exécution Basique

```powershell
# Depuis D:/Vault/Vault/SKILLS/organize-daily-reports/scripts/

# Mode DRY RUN (pas de modifications)
.\organize-reports.ps1 -DryRun -Verbose

# Mode EXÉCUTION (applique les changements)
.\organize-reports.ps1 -Verbose
```

### Paramètres

| Paramètre | Type | Default | Description |
|-----------|------|---------|-------------|
| SourcePath | string | `D:/Vault/Vault/THIRTY3/daily` | Chemin source contenant les fichiers |
| DestinationBasePath | string | `D:/Vault/Vault/REPORT/declassified report/02 Rapport Février/Semaine du 16 au 22 VACANCE` | Chemin base de destination |
| DryRun | switch | false | Affiche les actions sans les exécuter |
| Verbose | switch | false | Affiche les détails des opérations |

### Exemples

**Exemple 1: Test avec affichage détaillé**
```powershell
.\organize-reports.ps1 -DryRun -Verbose
```

**Exemple 2: Exécution réelle avec rapport**
```powershell
.\organize-reports.ps1 -Verbose
```

**Exemple 3: Chemin personnalisé**
```powershell
.\organize-reports.ps1 `
  -SourcePath "D:/Vault/Vault/THIRTY3/daily" `
  -DestinationBasePath "D:/Vault/Vault/REPORT/declassified report/02 Rapport Février/Semaine du 16 au 22 VACANCE" `
  -Verbose
```

## Résultat de l'Exécution

Après exécution, le script affiche:

```
====== Operate Daily Reports ======
Source: D:/Vault/Vault/THIRTY3/daily
Destination Base: D:/Vault/Vault/REPORT/declassified report/02 Rapport Février/Semaine du 16 au 22 VACANCE
Mode: EXECUTION
======================================

====== OPERATION REPORT ======
Total files processed: 2
Moved: 2
Moved and Renamed (Duplicates): 0
Skipped: 0
====================================
```

## Gestion des Doublons

Quand un fichier en double est détecté:

1. Le fichier est renommé avec le suffixe `_1.md`
   - Exemple: `(2026-02-22) Bilan du jour_1.md`

2. Un rapport affiche les fichiers à examiner
   - Section: "*** ATTENTION: DUPLICATES DETECTED ***"

3. Vous devez analyser manuellement et fusionner/supprimer le doublon

## Vérification des Liens Obsidian

Après le déplacement des fichiers, vérifiez que les liens ne sont pas cassés:

```bash
cd D:/Vault/Vault/SKILLS/organize-daily-reports/scripts/
python check-obsidian-links.py
```

Cela génère un rapport: `reports/link-check-YYYYMMDD-HHMMSS.json`

## Automatisation Quotidienne (Hook)

Pour automatiser le classement quotidien, configurez un Hook:

1. Ouvrez Claude Code
2. Créez un Hook qui exécute le script chaque jour
3. Configurez le déclenchement (ex: 7:00 AM)

Configuration recommandée:
- **Déclencheur:** Quotidien à 7:00 AM
- **Script:** `organize-reports.ps1`
- **Paramètres:** `-Verbose`
- **Notification:** Alerter en cas de doublons

## Dépannage

### Problème: "Source path not found"
**Cause:** Le chemin source n'existe pas
**Solution:** Vérifiez que `D:/Vault/Vault/THIRTY3/daily` existe

### Problème: "Destination base path not found"
**Cause:** Le chemin de destination n'existe pas
**Solution:** Créez la structure `D:/Vault/Vault/REPORT/declassified report/02 Rapport Février/Semaine du 16 au 22 VACANCE`

### Problème: Fichiers pas déplacés
**Cause:** Format de nom de fichier non reconnu
**Solution:** Vérifiez que les fichiers commencent par `(YYYY-MM-DD)`
- ✅ Correct: `(2026-02-22) Bilan du jour.md`
- ❌ Incorrect: `2026-02-22 Bilan du jour.md` (pas de parenthèses)

### Problème: Liens cassés après déplacement
**Cause:** Les liens relatifs n'ont pas été mis à jour
**Solution:** 
1. Utilisez `check-obsidian-links.py` pour identifier les liens cassés
2. Mettez à jour manuellement les références dans Obsidian
3. Utilisez Obsidian's "Update Links" si disponible

## Fichiers de Configuration

- `SKILL.md` - Définition du skill
- `scripts/organize-reports.ps1` - Script principal PowerShell
- `scripts/check-obsidian-links.py` - Vérificateur de liens
- `references/weeks-config.md` - Configuration des semaines
- `references/usage-guide.md` - Ce guide

## Support

Pour toute question ou amélioration:
1. Consultez les logs générés lors de l'exécution
2. Vérifiez la configuration des semaines
3. Testez en mode DRY RUN avant l'exécution réelle
