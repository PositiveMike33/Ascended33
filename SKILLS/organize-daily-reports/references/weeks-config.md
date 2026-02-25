# Configuration des Semaines

## Février 2026 - Semaine du 16 au 22 VACANCE

Cette configuration mappe les jours de février 2026 aux dossiers de destination.

### Mapping des Jours aux Dossiers

| Jour | Date | Dossier de Destination |
|------|------|----------------------|
| Jeudi | 16-02-2026 | 16-02-2026 |
| Vendredi | 17-02-2026 | 17-02-2026 |
| Samedi | 18-02-2026 | 18-02-2026 |
| Dimanche | 19-02-2026 | 19-02-2026 |
| Lundi | 20-02-2026 | 20-02-2026 |
| Mardi | 21-02-2026 | 21-02-2026 |
| Mercredi | 22-02-2026 | 22-02-2026 |

### Format des Dossiers

Les dossiers sont créés au format: `DD-MM-YYYY`

Exemple: `22-02-2026`

### Arborescence Complète

```
D:/Vault/Vault/REPORT/declassified report/02 Rapport Février/Semaine du 16 au 22 VACANCE/
├── 16-02-2026/
│   └── (fichiers du 16 février)
├── 17-02-2026/
│   └── (fichiers du 17 février)
├── 18-02-2026/
│   └── (fichiers du 18 février)
├── 19-02-2026/
│   └── (fichiers du 19 février)
├── 20-02-2026/
│   └── (fichiers du 20 février)
├── 21-02-2026/
│   └── (fichiers du 21 février)
└── 22-02-2026/
    └── (fichiers du 22 février)
```

### Notes Importantes

- Les dossiers sont créés automatiquement s'ils n'existent pas
- Chaque fichier (YYYY-MM-DD) Bilan du jour/soir est placé dans le dossier correspondant
- Les fichiers en double sont renommés avec suffixe `_1.md` pour analyse manuelle
- Seuls les fichiers commençant par `(YYYY-MM-DD)` sont traités

### Configuration Future

Pour ajouter d'autres semaines ou mois:

1. Créer la structure de dossiers appropriée dans `/REPORT/declassified report/`
2. Ajouter le mapping dans `scripts/organize-reports.ps1`
3. Mettre à jour ce fichier avec la nouvelle configuration
