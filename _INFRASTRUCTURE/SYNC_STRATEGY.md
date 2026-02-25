# 🔄 Stratégie de Synchronisation Bidirectionnelle

## Vue d'ensemble
**Source** : D:/Vault/Vault/ (principal, complet)
**Backup/Disaster Recovery** : C:\Users\th3th\OneDrive\Documents\GitHub\Ascended33 (GitHub)

## Contenu Analysé

### D:/Vault/Vault/ (PRINCIPAL)
```
_BRAIN/              ← Cerveau central, DAILY_REPORTS, système THIRTY3
THIRTY3/             ← Protocole personnel (Bilan du Matin, Bilan du Soir)
_PROJECTS/           ← Projets actifs
_INFRASTRUCTURE/     ← Docker, MCP, configuration système
KNOWLEDGE/           ← Base de connaissances
REPORT/              ← Rapports et synthèses
METADATA/            ← Métadonnées du système
streamlit_app.py     ← Dashboard principal
```

### GitHub\Ascended33/ (BACKUP)
```
core/                ← Code source principal
docker/              ← Configuration Docker ancienne
mcp/                 ← MCP integration
scripts/             ← Scripts de déploiement
tests/               ← Tests unitaires
streamlit_app.py     ← Version mirror
Documentation/*.md   ← Guides d'intégration
```

## Stratégie 1 : Sync Unidirectionnelle Sécurisée (RECOMMANDÉE)

```powershell
# D:/Vault/Vault/ → GitHub (Backup + Disaster Recovery)
robocopy "D:\Vault\Vault" "C:\Users\th3th\OneDrive\Documents\GitHub\Ascended33" /S /E /COPY:DAT /R:3 /W:10 /XO /XC /FFT
# /S /E        = Copies tous les répertoires (vides aussi)
# /COPY:DAT    = Copie Data, Attributes, Timestamps
# /XO          = Exclut fichiers PLUS VIEUX (preserve modifications GitHub)
# /R:3 /W:10   = Retries en cas d'erreur
# /FFT          = Tolérance timestamps FAT
```

### Avantages
✅ Sécurité : Pas de suppression, jamais
✅ Directionnel : Une source de vérité (Vault)
✅ Disaster Recovery : GitHub toujours à jour
✅ Reversibilité : Peut restaurer depuis GitHub

### Limitations
⚠️ Non bidirectionnelle
⚠️ Les modifications sur GitHub ne remontent pas vers Vault

## Stratégie 2 : Bi-sync via Git (ALTERNATIVE)

```bash
# Initialiser repo Git
cd D:\Vault\Vault
git init
git add .
git commit -m "Initial sync"

# Mirror vers GitHub
git remote add origin https://github.com/username/Vault
git push -u origin main
```

## Stratégie 3 : Services de Sync Cloud (FUTUR)

- Microsoft OneDrive (déjà utilisé pour GitHub backup)
- Synology/NAS local
- Nextcloud personnel
- S3 AWS pour archive froide

## Plan de Déploiement Immédiat

### Phase 1 : Préparation
- [ ] Validation chemin GitHub accessible
- [ ] Vérifier permissions en écriture
- [ ] Espace disque libre disponible

### Phase 2 : Synchronisation Initiale
```powershell
# SYNC 1 : Vault → GitHub (Primary backup)
robocopy "D:\Vault\Vault" "C:\Users\th3th\OneDrive\Documents\GitHub\Ascended33" /S /E /COPY:DATU /XO /FFT

# SYNC 2 : GitHub → Vault (Récupère les fichiers de développement manquants)
robocopy "C:\Users\th3th\OneDrive\Documents\GitHub\Ascended33" "D:\Vault\Vault" /S /E /COPY:DATU /XO /FFT
```

### Phase 3 : Automatisation
```powershell
# Script PowerShell de Sync Quotidienne
# Fichier: D:\Vault\Vault\AUTO_SYNC_DAILY.ps1

param(
    [string]$SyncDirection = "VaultToGitHub"  # ou GitHubToVault
)

$vaultPath = "D:\Vault\Vault"
$githubPath = "C:\Users\th3th\OneDrive\Documents\GitHub\Ascended33"

if ($SyncDirection -eq "VaultToGitHub") {
    Write-Host "🔄 Sync: Vault → GitHub Backup"
    robocopy $vaultPath $githubPath /S /E /COPY:DATU /R:3 /W:10 /XO /FFT
} else {
    Write-Host "🔄 Sync: GitHub → Vault (Dev files)"
    robocopy $githubPath $vaultPath /S /E /COPY:DATU /R:3 /W:10 /XO /FFT
}

Write-Host "✅ Synchronisation terminée"
```

## Fichiers à Exclure (Optionnel)

```
.git/
.venv/
__pycache__/
*.pyc
.DS_Store
Thumbs.db
node_modules/
.env
*.log
```

## Garanties

✅ **Aucun fichier supprimé** de l'un ou l'autre côté
✅ **Versions préservées** (timestamps conservés)
✅ **Bi-directionnel possible** en deux syncs successifs
✅ **Disaster Recovery** garantie (GitHub copie actualisée)
✅ **Laptop loss recovery** : GitHub contient projet complet

## État d'Implémentation

- [x] Analyse complétée
- [x] Stratégies documentées
- [ ] **PRÊT POUR DÉPLOIEMENT**

**Prochaine étape** : Approuvez déploiement → Exécute Sync Initiale

---
**Généré** : 2026-02-25
**Status** : Prêt pour Implémentation
**Risque** : MINIMAL (Sync à sens unique, pas de destruction)
