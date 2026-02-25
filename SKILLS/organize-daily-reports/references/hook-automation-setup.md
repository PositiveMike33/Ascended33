# Configuration de l'Automation Quotidienne - Hook

## 📅 Vue d'ensemble

Ce guide explique comment configurer un Hook Claude Code pour automatiser l'exécution quotidienne du skill `organize-daily-reports`.

## 🎯 Objectif

Exécuter automatiquement chaque matin à 7:00 AM:
1. Le script PowerShell pour déplacer les fichiers
2. Le vérificateur de liens (optionnel)
3. Notifier en cas de doublon ou erreur

## 🔧 Configuration du Hook

### Option 1: Hook Simple (Recommandée)

**Déclencheur:** Quotidien à 7:00 AM

**Script à exécuter:**
```powershell
cd 'D:\Vault\Vault\SKILLS\organize-daily-reports\scripts'
.\organize-reports.ps1 -Verbose
```

**Sortie attendue:**
```
====== Operate Daily Reports ======
[résultats...]
====== OPERATION REPORT ======
```

### Option 2: Hook avec Vérification des Liens

**Déclencheur:** Quotidien à 7:00 AM

**Script:**
```powershell
cd 'D:\Vault\Vault\SKILLS\organize-daily-reports\scripts'
$result = .\organize-reports.ps1 -Verbose
Write-Host "Checking Obsidian links..."
python check-obsidian-links.py
```

**Note:** Nécessite Python installé sur le système

### Option 3: Hook avec Rapport Email

**Déclencheur:** Quotidien à 7:00 AM

**Script:**
```powershell
cd 'D:\Vault\Vault\SKILLS\organize-daily-reports\scripts'
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$report = "=== Daily Report Organization - $timestamp ===" 
$report += "`n" + (.\organize-reports.ps1 -Verbose | Out-String)
Write-Host $report

# Sauvegarder le rapport
$report | Out-File -FilePath "reports/daily-report-$(Get-Date -Format 'yyyyMMdd').txt" -Force
```

## 📋 Étapes de Configuration

### Étape 1: Ouvrir Claude Code
1. Lancez Claude Code
2. Allez à **Settings** → **Hooks**
3. Cliquez sur **New Hook**

### Étape 2: Créer le Hook

**Nom:** `Daily Reports Organization`

**Description:** Automatise le classement quotidien des rapports du jour/soir

**Déclencheur:**
- Type: **Scheduled**
- Fréquence: **Daily**
- Heure: **07:00 AM**
- Fuseau horaire: Votre fuseau horaire local

### Étape 3: Configurer l'Action

**Type d'action:** PowerShell Script

**Script:**
```powershell
cd 'D:\Vault\Vault\SKILLS\organize-daily-reports\scripts'
.\organize-reports.ps1 -Verbose
```

### Étape 4: Notifications

**Sur succès:**
- Email: `votre-email@example.com`
- Sujet: `✅ Rapports classés avec succès`

**Sur erreur:**
- Email: `votre-email@example.com`
- Sujet: `❌ Erreur classement rapports`

**Sur doublon détecté:**
- Email: `votre-email@example.com`
- Sujet: `⚠️ Doublon détecté - Analyse manuelle requise`

## 🛠️ Configuration des Alertes

### Alerter sur Doublon

```powershell
# À la fin du script organize-reports.ps1
$duplicates = $results | Where-Object { $_.Status -eq 'MOVED_RENAMED' }
if ($duplicates.Count -gt 0) {
    Write-Error "DUPLICATES DETECTED - Manual review needed!" -ErrorAction Continue
    # Cela déclenchera une notification d'erreur du Hook
}
```

### Générer un Résumé Quotidien

```powershell
$summary = @{
    Date = Get-Date -Format 'yyyy-MM-dd'
    FilesProcessed = $results.Count
    FilesMoved = ($results | Where-Object { $_.Status -eq 'MOVED' }).Count
    Duplicates = ($results | Where-Object { $_.Status -eq 'MOVED_RENAMED' }).Count
}

$summary | ConvertTo-Json | Out-File "reports/daily-summary-$(Get-Date -Format 'yyyyMMdd').json"
```

## 📊 Monitoring et Logging

### Logs Disponibles

Tous les logs sont sauvegardés dans:
```
D:/Vault/Vault/SKILLS/organize-daily-reports/reports/
```

**Format des fichiers:**
- `daily-report-YYYYMMDD.txt` - Rapport texte quotidien
- `daily-summary-YYYYMMDD.json` - Résumé JSON
- `link-check-YYYYMMDD-HHMMSS.json` - Vérification des liens

### Vérifier les Exécutions Réussies

Depuis Claude Code:
1. **Hooks** → **Daily Reports Organization**
2. Onglet **Execution History**
3. Consultez les rapports d'exécution

### Dépannage du Hook

**Le Hook ne s'exécute pas:**
1. Vérifiez que PowerShell est installé
2. Vérifiez les chemins dans le script
3. Testez manuellement le script
4. Vérifiez les logs d'erreur du Hook

**Le Hook s'exécute mais ne déplace pas:**
1. Vérifiez que les fichiers existants commencent par `(YYYY-MM-DD)`
2. Testez en mode DRY RUN: `.\organize-reports.ps1 -DryRun -Verbose`
3. Vérifiez les permissions d'accès aux dossiers

## 🔄 Maintenance

### Arrêter temporairement

```powershell
# Dans Claude Code - Hooks
# Onglet Daily Reports Organization
# Clic sur "Disable"
```

### Planifier à différentes heures

**Exemple: Exécution à 7:00 AM ET 7:00 PM**

Créer 2 hooks:
1. Hook #1: 07:00 AM
2. Hook #2: 19:00 PM (7:00 PM)

Même script pour les deux

### Résumé hebdomadaire

Hook supplémentaire qui s'exécute le dimanche à 20:00:

```powershell
cd 'D:\Vault\Vault\SKILLS\organize-daily-reports\reports'
$weeklyFiles = Get-ChildItem -Filter "daily-report-*" -File | 
    Where-Object { $_.LastWriteTime -gt (Get-Date).AddDays(-7) }
    
Write-Host "=== WEEKLY SUMMARY ===" 
Write-Host "Files processed this week: $($weeklyFiles.Count)"
$weeklyFiles | Select-Object Name, LastWriteTime, Length
```

## ✅ Checklist de Configuration

- [ ] Hook créé dans Claude Code
- [ ] Déclencheur fixé à 07:00 AM quotidien
- [ ] Script PowerShell configuré
- [ ] Notifications d'erreur activées
- [ ] Notifications de doublon activées
- [ ] Premier test effectué (vérifier logs)
- [ ] Dossier `reports` créé
- [ ] Chemins accessibles depuis Claude Code

## 📝 Notes Importantes

1. **Fuseau horaire:** Assurez-vous que le fuseau horaire du Hook correspond à votre fuseau
2. **Permissions:** L'utilisateur exécutant Claude Code doit avoir accès à D:/Vault/Vault
3. **PowerShell:** Nécessite PowerShell 5.0+ ou PowerShell Core
4. **Archivage:** Les rapports s'accumulent - prévoir une archivage mensuelle
5. **Mise à jour:** Mettez à jour la configuration si vous changez les chemins

## 🚀 Test de Vérification

Avant d'activer l'automation, testez:

```powershell
# Test 1: Vérifier les chemins
Test-Path 'D:\Vault\Vault\SKILLS\organize-daily-reports\scripts\organize-reports.ps1'

# Test 2: Exécuter en mode DRY RUN
cd 'D:\Vault\Vault\SKILLS\organize-daily-reports\scripts'
.\organize-reports.ps1 -DryRun -Verbose

# Test 3: Exécuter réellement
.\organize-reports.ps1 -Verbose
```

---

**Hook Status:** ✅ **PRÊT POUR CONFIGURATION**

Une fois le Hook configuré, l'automation quotidienne s'exécutera automatiquement chaque matin à 7:00 AM.
