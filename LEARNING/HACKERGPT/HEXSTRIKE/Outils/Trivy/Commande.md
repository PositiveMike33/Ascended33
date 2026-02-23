### 1. Scan d'Images Container
```bash
# Scan basique
trivy image [IMAGE_NAME]

# Scan filtré par sévérité (HIGH, CRITICAL)
trivy image --severity HIGH,CRITICAL [IMAGE_NAME]

# Scan avec export au format JSON
trivy image -f json -o results.json [IMAGE_NAME]
```

### 2. Scan de Système de Fichiers (FS)
```bash
# Scan d'un répertoire local (recherche de vulnérabilités dans les dépendances)
trivy fs /path/to/project

# Scan incluant les fichiers de configuration (IaC)
trivy fs --scanners vuln,config /path/to/project
```

### 3. Scan de Dépôt Git (Repo)
```bash
# Scan d'un repo distant
trivy repo https://github.com/user/repo

# Scan avec sortie formatée pour l'intégration CI/CD (SARIF)
trivy repo --format sarif --output results.sarif [REPO_URL]
```

### 4. Scan de Configuration (IaC / Kubernetes)
```bash
# Scan de fichiers Dockerfile, Terraform, Kubernetes
trivy config ./infrastructure/

# Vérification stricte des politiques
trivy config --exit-code 1 --severity CRITICAL ./k8s-manifests/
```

### 5. Gestion de la Database (Vulnerability DB)
```bash
# Mise à jour forcée de la base de données de vulnérabilités
trivy image --download-db-only

# Suppression du cache
trivy image --clear-cache
```

### 6. Intégration CI/CD (Pipeline Defense)
```bash
# Échoue le build si des vulnérabilités CRITICAL sont trouvées (Exit code 1)
trivy image --exit-code 1 --severity CRITICAL [IMAGE_NAME]

# Ignore les vulnérabilités sans correctif disponible (Réduction du bruit)
trivy image --ignore-unfixed [IMAGE_NAME]
```

### 7. Formats de Sortie (Reporting)
```bash
# Tableau (par défaut)
trivy image --format table [IMAGE]

# JSON (pour parsing automatique)
trivy image --format json [IMAGE]

# SARIF (pour GitHub Security Tab)
trivy image --format sarif [IMAGE]
```

Besoin d'un flag spécifique ou d'une intégration particulière ? Demande-moi.

#### 📋 Quick Commands

`trivy image imagename``trivy fs --security-checks vuln,config /`