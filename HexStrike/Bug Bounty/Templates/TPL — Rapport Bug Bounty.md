# Rapport de Vulnérabilité — Bug Bounty

---

## En-tête

| Champ | Valeur |
|-------|--------|
| **Programme** | [Nom du programme] |
| **Plateforme** | HackerOne / Bugcrowd / Intigriti / etc. |
| **Date** | YYYY-MM-DD |
| **Chercheur** | Michael — HexStrike |

---

## Titre de la Vulnérabilité

**[Type de vulnérabilité] dans [Composant/Paramètre] permettant [Impact]**

*Exemple : "XSS Reflected dans le paramètre `search` de la page principale permettant l'exécution de code JavaScript arbitraire"*

---

## Résumé

*[2-3 phrases. Expliquer simplement ce qui est vulnérable et ce qu'un attaquant peut faire.]*

---

## Sévérité

**Criticité :** Critique / Élevée / Moyenne / Faible

**Score CVSS :** X.X (calculé sur [cvss.me](https://cvss.me) ou [nvd.nist.gov](https://nvd.nist.gov/vuln-metrics/cvss))

**Vecteur CVSS :** `AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:N`

---

## Étapes de Reproduction

**Pré-requis :**
- [ ] Compte utilisateur standard (pas d'admin)
- [ ] Navigateur Firefox / Chrome
- [ ] [Autres pré-requis]

**Étapes :**

1. Se connecter à [URL] avec les credentials : `user@test.com / password123`
2. Naviguer vers [URL spécifique]
3. Dans le champ [Nom du champ], entrer le payload suivant :
   ```
   [PAYLOAD EXACT]
   ```
4. Cliquer sur [Bouton]
5. Observer [résultat]

**Résultat attendu (comportement normal) :**
> [Ce qui devrait se passer]

**Résultat obtenu (comportement vulnérable) :**
> [Ce qui se passe réellement]

---

## Preuve de Concept (PoC)

### Requête HTTP (depuis Burp Suite)
```http
POST /api/search HTTP/1.1
Host: target.com
Content-Type: application/json
Cookie: session=abc123

{"query": "<PAYLOAD>"}
```

### Réponse HTTP
```http
HTTP/1.1 200 OK
Content-Type: text/html

[Réponse montrant la vulnérabilité]
```

### Captures d'Écran
*[Attacher les screenshots montrant la vulnérabilité]*

---

## Impact

**Impact direct :**
> [Ce qu'un attaquant peut faire concrètement — rester factuel]

**Scénario d'attaque réaliste :**
> [Comment un attaquant exploiterait ceci dans un contexte réel]

**Données/utilisateurs affectés :**
> [Portée de l'impact]

---

## Recommandation de Correction

> [Suggestion technique spécifique pour corriger la vulnérabilité]

**Références :**
- [OWASP - Nom de la catégorie]
- [CVE si applicable]
- [Documentation officielle du framework]

---

## Informations Additionnelles

**URL(s) affectée(s) :**
- `https://target.com/path/to/vulnerable/page`

**Paramètre(s) vulnérable(s) :**
- `search` (GET parameter)

**Navigateurs testés :**
- Firefox 121.0 ✓
- Chrome 120.0 ✓

**Reproductibilité :** 100% — Testé 3 fois

---

*Rapport soumis le YYYY-MM-DD — HexStrike*
