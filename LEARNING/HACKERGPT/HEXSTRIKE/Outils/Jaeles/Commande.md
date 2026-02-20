### 1. Commandes de Scan (Cœur de l'outil)

*   **Scan simple d'une cible unique :**
    ```bash
    jaeles scan -u https://target.com
    ```
*   **Scan massif avec liste d'URLs et signatures spécifiques :**
    ```bash
    jaeles scan -U list_urls.txt -s /path/to/signatures/ -c 50
    ```
    *Note : `-c 50` définit le parallélisme (concurrency) pour un multi-threading optimal.*
*   **Filtrage des signatures par mot-clé (Grep) :**
    ```bash
    jaeles scan -u https://target.com -G "cve-2024"
    ```
*   **Utilisation d'un proxy (Burp Suite/ZAP) pour analyse :**
    ```bash
    jaeles scan -u https://target.com --proxy http://127.0.0.1:8080
    ```

### 2. Gestion des Signatures (YAML-based)

*   **Mettre à jour les signatures par défaut :**
    ```bash
    jaeles config init
    jaeles config update
    ```
*   **Vérifier la syntaxe d'une signature custom :**
    ```bash
    jaeles scan -s my_custom_sig.yaml -u https://test.com --debug
    ```

### 3. Mode Serveur & API

*   **Lancer Jaeles en mode API (Interaction HexStrike) :**
    ```bash
    jaeles server --host 0.0.0.0 --port 5000
    ```
*   **Soumettre un scan via l'API (Client-side) :**
    ```bash
    curl -X POST http://localhost:5000/api/scan -d '{"url": "https://target.com"}'
    ```

### 4. Options Avancées & Fuzzing

*   **Scan passif (Analyse des réponses sans nouveaux paramètres) :**
    ```bash
    jaeles scan -u https://target.com -s "passive/.*"
    ```
*   **Fuzzing de paramètres avec payloads personnalisés :**
    ```bash
    jaeles scan -u "https://target.com/api?id=FUZZ" -s "fuzzing/sqli.yaml"
    ```
*   **Génération de rapport formaté :**
    ```bash
    jaeles scan -u https://target.com -o /path/to/output_dir
    ```

### 5. Analyse Technique & Debug

*   **Mode verbeux pour l'analyse comportementale (Behavioral) :**
    ```bash
    jaeles scan -u https://target.com -v --vv
    ```
    *Permet de voir les requêtes/réponses exactes générées par le moteur YAML.*

**Rappel Expert :** L'efficacité de Jaeles réside dans la précision de ses sélecteurs YAML (`lookups`, `detections`). Toujours tester les signatures avec `--debug` pour éviter les faux négatifs dus à des conditions `AND/OR` mal structurées.

#### 📋 Quick Commands

`jaeles scan -u url -s signatures/``jaeles server`