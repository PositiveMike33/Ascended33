# Organize Daily Reports Skill

Automatisez le classement de vos rapports quotidiens dans votre Vault Obsidian.

## 📋 Aperçu

Ce skill organise automatiquement les fichiers de rapport quotidien:
- **Source:** `D:/Vault/Vault/THIRTY3/daily`
- **Destination:** `D:/Vault/Vault/REPORT/declassified report/02 Rapport Février/Semaine du 16 au 22 VACANCE/`

### Fichiers Traités

- `(YYYY-MM-DD) Bilan du jour.md`
- `(YYYY-MM-DD) Bilan du soir.md`

## 🚀 Démarrage Rapide

### Exécution Manuelle

```powershell
# Mode test (pas de modifications)
cd D:\Vault\Vault\SKILLS\organize-daily-reports\scripts
.\organize-reports.ps1 -DryRun -Verbose

# Mode réel (applique les changements)
.\organize-reports.ps1 -Verbose
```

### Vérification des Liens

```bash
cd D:\Vault\Vault\SKILLS\organize-daily-reports\scripts
python check-obsidian-links.py
```

## 📁 Structure du Skill

```
D:/Vault/Vault/SKILLS/organize-daily-reports/
├── SKILL.md                          # Définition du skill
├── README.md                         # Ce fichier
├── scripts/
│   ├── organize-reports.ps1         # Script PowerShell principal
│   └── check-obsidian-links.py      # Vérificateur de liens Obsidian
├── references/
│   ├── weeks-config.md              # Configuration des semaines
│   └── usage-guide.md               # Guide complet d'utilisation
└── reports/                         # Dossier pour les rapports générés
    └── link-check-*.json            # Rapports de vérification des liens
```

## ⚙️ Fonctionnalités

### ✅ Déplacement de Fichiers
- Détecte les fichiers au format `(YYYY-MM-DD) Bilan du [jour|soir].md`
- Déplace vers le dossier date approprié (format `DD-MM-YYYY`)
- Crée automatiquement les dossiers de destination

### 📝 Gestion des Doublons
- Détecte les fichiers en double
- Renomme avec suffixe `_1.md`
- Marque pour analyse manuelle
- Rapporte dans le résultat de l'exécution

### 🔍 Vérification des Liens
- Scanne tous les fichiers markdown du Vault
- Détecte les liens cassés
- Génère un rapport détaillé en JSON

### 📊 Rapports
- Résumé des opérations effectuées
- Liste des fichiers déplacés
- Alerte sur les doublons détectés
- Rapport détaillé des vérifications de liens

## 🔄 Automatisation Quotidienne

Pour automatiser l'exécution quotidienne:

1. **Via Claude Code Hook:**
   - Déclencher quotidiennement à heure fixe
   - Exécuter `organize-reports.ps1`
   - Notifier en cas d'erreur ou doublon

2. **Configuration recommandée:**
   - Heure: 7:00 AM
   - Fréquence: Quotidienne
   - Action: `-Verbose` pour voir les détails

## 📖 Documentation

- **SKILL.md** - Spécifications techniques complètes
- **usage-guide.md** - Guide détaillé avec exemples
- **weeks-config.md** - Configuration des semaines et dossiers

## 🐛 Dépannage

### Fichiers non déplacés?
1. Vérifiez le format: `(YYYY-MM-DD)` (avec parenthèses)
2. Testez en mode DRY RUN: `.\organize-reports.ps1 -DryRun -Verbose`
3. Vérifiez les chemins source et destination

### Liens cassés après déplacement?
1. Exécutez `python check-obsidian-links.py`
2. Consultez le rapport généré: `reports/link-check-*.json`
3. Mettez à jour manuellement les liens si nécessaire

## 📝 Notes

- **IMPORTANT:** Tous les fichiers sont stockés dans `D:/Vault/Vault`
- Les fichiers en double doivent être analysés manuellement
- Toujours tester en mode DRY RUN avant exécution réelle
- Sauvegarder votre Vault avant d'automatiser

## 🔗 Chemins Clés

- **Source des fichiers:** `D:/Vault/Vault/THIRTY3/daily`
- **Destination:** `D:/Vault/Vault/REPORT/declassified report/02 Rapport Février/Semaine du 16 au 22 VACANCE`
- **Scripts:** `D:/Vault/Vault/SKILLS/organize-daily-reports/scripts`
- **Configuration:** `D:/Vault/Vault/SKILLS/organize-daily-reports/references`
- **Rapports:** `D:/Vault/Vault/SKILLS/organize-daily-reports/reports`

## 📅 Dernière Mise à Jour

- **Date:** 2026-02-22
- **Version:** 1.0
- **Auteur:** Claude Code

---

**Prêt à organiser vos rapports quotidiens!** 🎯
