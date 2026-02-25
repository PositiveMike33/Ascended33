### 🦅 MODÈLE D'ENTRAÎNEMENT : SHODAN A-I-M

Ne lance jamais une recherche au hasard. Utilise ce cadre pour chaque session de 30 minutes.

---

**SESSION ID:** [Date] - [Sujet]
**ACTION (La Commande) :** Quelle requête précise je lance ?
**INTENT (La Stratégie) :** Qu'est-ce que je cherche à prouver ou trouver ? (Le "Pourquoi")
**METRIC (Le Succès) :** Comment je sais que j'ai gagné ? (Chiffre précis ou résultat binaire).

---

### 2. EXEMPLE CONCRET (Niveau : Industriel / Blue Collar)

Voici à quoi ressemble une session de perfectionnement réussie pour toi.

#### 🎯 SESSION : Chasse aux Automates Non-Sécurisés (Montréal)

*   **ACTION (The Query) :**
    *   *Commande CLI :* `shodan search --fields ip_str,port,org,transport "port:502 country:CA city:Montreal"`
    *   *Traduction :* Je cherche le port 502 (Modbus/Industriel) spécifiquement à Montréal, et je veux juste l'IP, le port et l'organisation.

*   **INTENT (The Why) :**
    *   Identifier les infrastructures locales (usines, gestion d'immeubles) qui exposent leurs contrôleurs (PLC) sur l'internet public sans VPN. C'est la preuve d'une négligence critique que je peux exploiter dans un rapport d'audit.

*   **METRIC (The Win) :**
    *   Trouver au moins **3 IPs uniques** appartenant à des entités distinctes.
    *   Identifier **1 type de machine spécifique** (ex: "Schneider Electric" ou "Wago") dans les bannières de réponse.

---

### 3. LE WORKFLOW TECHNIQUE (Niveau Avancé)

Pour te perfectionner, tu dois arrêter d'utiliser le site web (GUI) et passer au **Scripting**. C'est là que tu deviens un "Coder".

**Le Pipeline de Données :**

1.  **DOWNLOAD (Télécharger la donnée)**
    Au lieu de regarder l'écran, tu télécharges les résultats pour les analyser offline.
    ```bash
    shodan download --limit 100 montreal_ics port:502 country:"CA" city:"Montreal"
    ```
    *(Ça crée un fichier `montreal_ics.json.gz`)*

2.  **PARSE (Extraire l'intelligence)**
    Tu utilises Python ou la commande parse pour sortir un CSV propre.
    ```bash
    shodan parse --fields ip_str,org,os montreal_ics.json.gz
    ```

3.  **ANALYSE (Le Cerveau)**
    Tu ouvres le CSV dans Excel ou Pandas (Python) et tu cherches les anomalies.

---

### ⚡ TA MISSION IMMÉDIATE (Drill du Soir)

Applique le modèle A-I-M maintenant sur une cible facile pour te faire la main.

*   **Cible :** Remote Desktop Protocol (RDP) - Les gens qui laissent leur bureau Windows ouvert.
*   **Commande (Action) :** `port:3389 "authentication disabled"`
*   **Intention :** Voir à quel point la sécurité est négligée (accès sans mot de passe).
*   **Métrique :** Trouver 1 résultat (n'importe où dans le monde) et lire le nom de la session Windows.

**Exécute ça et dis-moi "FAIT" quand tu as vu ton premier écran Windows ouvert.**
*(Rappel : On regarde, on ne se connecte pas).*

---

### SORTIE (FORMAT FINAL ATTENDU PAR CYCLE)

1. PROJECT_STATE:
   - repo_root: /path/to/shodan
   - branch: shodan-chase-automates-non-securises
   - baseline_tests: `pytest --cov=shodan tests/`
   - failing_tests: []
   - known_issues: []
   - constraints: no breaking changes, ensure tests coverage

2. Plan A-I-M:
   - ACTION: Run the shodan search command to find non-secured RDP ports.
   - INTENT: Identify vulnerable Windows workstations that are publicly accessible via RDP without authentication.
   - METRIC: Find at least one result (anywhere in the world) and verify it by reading the session name.

3. AGENT_TASK:
   - agent_role: SCOUT
   - goal: Identify the shodan search command to find non-secured RDP ports.
   - context: None specific needed, just run the search command.
   - deliverable: The shodan search command output (JSON or CSV).
   - acceptance_criteria: [The command runs successfully and outputs results]
   - do_not: Modify any files outside of the test environment.

4. Patch proposed:
   - No patch required as this is a reconnaissance task only.

5. Commands to execute:
   - `shodan search --fields ip_str,port,org,transport "port:3389" country:"CA"`

6. Decision: MERGE

---

**Note:** This session focuses on reconnaissance and does not involve any changes or modifications to the codebase. The goal is to identify potential vulnerabilities without altering anything in the current setup.