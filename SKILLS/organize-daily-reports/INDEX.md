# Index - Organize Daily Reports Skill

## 📋 Table des Matières

### 📖 Documentation Principale
- **[README.md](_BRAIN/README.md)** - Aperçu rapide et démarrage
- **[SKILL.md](SKILL.md)** - Spécifications techniques complètes

### 🔧 Guides d'Utilisation
- **[references/usage-guide.md](references/usage-guide.md)** - Guide complet avec exemples
- **[references/weeks-config.md](references/weeks-config.md)** - Configuration des semaines et dossiers
- **[references/hook-automation-setup.md](references/hook-automation-setup.md)** - Setup automatisation quotidienne

### 💻 Scripts
- **[scripts/organize-reports.ps1](scripts/organize-reports.ps1)** - Script PowerShell principal
  - Détecte les fichiers `(YYYY-MM-DD)` 
  - Crée les dossiers de destination
  - Déplace les fichiers
  - Gère les doublons
  - Génère les rapports

- **[scripts/check-obsidian-links.py](scripts/check-obsidian-links.py)** - Vérificateur de liens Obsidian
  - Scanne tous les fichiers markdown
  - Détecte les liens cassés
  - Génère rapports détaillés
  - *Optionnel: nécessite Python*

- **[scripts/test-organize.ps1](scripts/test-organize.ps1)** - Script de test
  - Vérifie les chemins
  - Affiche les fichiers trouvés
  - Valide la configuration

### 📊 Rapports
- **[reports/](reports/)** - Dossier contenant les rapports d'exécution
  - `test-report-22-02-2026.md` - Rapport du test d'exécution
  - `daily-report-*.txt` - Rapports quotidiens (générés automatiquement)
  - `daily-summary-*.json` - Résumés quotidiens (générés automatiquement)
  - `link-check-*.json` - Rapports de vérification des liens

## 🚀 Démarrage Rapide

### 1️⃣ Utilisation Manuelle
```powershell
cd D:\Vault\Vault\SKILLS\organize-daily-reports\scripts
.\organize-reports.ps1 -Verbose
```

### 2️⃣ Mode Test (DRY RUN)
```powershell
cd D:\Vault\Vault\SKILLS\organize-daily-reports\scripts
.\organize-reports.ps1 -DryRun -Verbose
```

### 3️⃣ Vérifier les Liens
```bash
cd D:\Vault\Vault\SKILLS\organize-daily-reports\scripts
python check-obsidian-links.py
```

### 4️⃣ Automatiser Quotidiennement
Voir [references/hook-automation-setup.md](references/hook-automation-setup.md)

## 📁 Structure Complète

```
D:/Vault/Vault/SKILLS/organize-daily-reports/
│
├── 📄 README.md                              (Aperçu & démarrage)
├── 📄 SKILL.md                               (Specs techniques)
├── 📄 INDEX.md                               (Ce fichier)
│
├── 📁 scripts/
│   ├── organize-reports.ps1                  (Script principal)
│   ├── check-obsidian-links.py              (Vérificateur liens)
│   └── test-organize.ps1                     (Script test)
│
├── 📁 references/
│   ├── usage-guide.md                        (Guide d'utilisation)
│   ├── weeks-config.md                       (Config semaines)
│   └── hook-automation-setup.md              (Setup automation)
│
└── 📁 reports/
    ├── test-report-22-02-2026.md            (Rapport test)
    ├── daily-report-*.txt                    (Rapports quotidiens)
    ├── daily-summary-*.json                  (Résumés quotidiens)
    └── link-check-*.json                     (Vérification liens)
```

## 🎯 Cas d'Usage

### Cas 1: Classer rapidement les rapports d'aujourd'hui
→ [usage-guide.md](references/usage-guide.md) - Section "Exécution Basique"

### Cas 2: Tester avant d'automatiser
→ [usage-guide.md](references/usage-guide.md) - Section "Mode DRY RUN"

### Cas 3: Configurer l'automatisation quotidienne
→ [hook-automation-setup.md](references/hook-automation-setup.md)

### Cas 4: Vérifier que les liens ne sont pas cassés
→ [usage-guide.md](references/usage-guide.md) - Section "Vérification des Liens Obsidian"

### Cas 5: Ajouter une nouvelle semaine
→ [weeks-config.md](references/weeks-config.md) - Section "Configuration Future"

### Cas 6: Dépanner un problème
→ [usage-guide.md](references/usage-guide.md) - Section "Dépannage"

## 📊 Fonctionnalités

✅ Détecte les fichiers au format `(YYYY-MM-DD) Bilan du [jour|soir].md`
✅ Crée automatiquement les dossiers de destination
✅ Déplace les fichiers vers les bons emplacements
✅ Gère les doublons en renommant `_1.md`
✅ Génère des rapports détaillés
✅ Vérifie les liens Obsidian
✅ Peut être automatisé quotidiennement via Hook
✅ Support du mode DRY RUN pour tester

## 📈 Test Status

**Last Test:** 22-02-2026 20:31
**Result:** ✅ **SUCCÈS**
- 2 fichiers détectés
- 2 fichiers déplacés
- 0 doublons
- Dossiers créés automatiquement

## 🔐 Chemins Clés

| Description | Chemin |
|-------------|--------|
| Source (fichiers à traiter) | `D:/Vault/Vault/THIRTY3/daily` |
| Destination (rapports classés) | `D:/Vault/Vault/REPORT/declassified report/02 Rapport Février/Semaine du 16 au 22 VACANCE` |
| Skill (scripts & docs) | `D:/Vault/Vault/SKILLS/organize-daily-reports` |
| Rapports générés | `D:/Vault/Vault/SKILLS/organize-daily-reports/reports` |

## 💡 Points Important

1. **Tous les fichiers dans D:/Vault/Vault** - Aucun fichier en dehors du vault
2. **Pattern obligatoire:** `(YYYY-MM-DD)` avec parenthèses
3. **Format dossiers:** `DD-MM-YYYY` (ex: 22-02-2026)
4. **Doublons:** Renommés en `_1.md` pour analyse manuelle
5. **Liens:** Vérifiez après déplacement si nécessaire
6. **Automation:** Hook Claude Code recommandé

## 🆘 Support & Dépannage

Consultez [usage-guide.md - Dépannage](references/usage-guide.md#dépannage) pour:
- Source path not found
- Destination path not found
- Fichiers pas déplacés
- Liens cassés après déplacement

## 📞 Contact & Modification

Pour modifier le skill:
1. Consultez [SKILL.md](SKILL.md) pour les spécifications
2. Modifiez les scripts dans `scripts/`
3. Mettez à jour la documentation
4. Testez avec `test-organize.ps1`
5. Exécutez avec données réelles en mode `-DryRun`

## ✨ Prochaines Étapes

1. ✅ Skill créé et testé
2. ⏳ Configurer Hook quotidien (voir [hook-automation-setup.md](references/hook-automation-setup.md))
3. ⏳ Adapter pour autres semaines/mois
4. ⏳ Ajouter notifications email personnalisées
5. ⏳ Mettre en place archivage des rapports

---

**Version:** 1.0  
**Date de création:** 22-02-2026  
**Auteur:** Claude Code  
**Status:** ✅ Production Ready
