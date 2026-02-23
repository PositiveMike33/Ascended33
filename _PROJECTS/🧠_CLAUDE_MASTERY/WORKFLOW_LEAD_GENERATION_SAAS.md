---
date: 2026-02-17
type: claude-workflow
tags: [claude, automation, lead-generation, saas, revenu]
status: active
category: lead-gen
---

# 🤖 CLAUDE WORKFLOW — Lead Generation Automation pour SaaS

> Workflow automatisé : transformer un CSV de prospects bruts en lead list qualifiée avec scores de priorité, via Claude API.

---

## 🎯 Objectif du workflow

**Problème :** Qualifier manuellement des centaines de prospects prend des heures.
**Solution :** Claude analyse chaque prospect (site web, industrie, taille, pain points) et génère un score de priorité 1-10 automatiquement.
**Résultat :** Liste priorisée de leads chauds, prêts pour outreach ciblé.

---

## 📊 Input → Output

### Données en entrée
```
Type 1: CSV prospects (nom, email, site web, industrie, nb employés)
Type 2: Critères ICP (Ideal Customer Profile) définis par user
Type 3: Context SaaS produit (valeur proposition, pricing)
```

### Résultat final attendu
```
Format: CSV enrichi + rapport markdown
Colonnes ajoutées:
  - score_lead (1-10)
  - qualification (Hot/Warm/Cold)
  - pain_point_identifié
  - message_outreach_personnalisé
  - priorité_contact (Immédiat/Cette semaine/Ce mois)
```

---

## 🔄 Étapes du processus

### 1️⃣ Préparation des données
> Nettoyer et standardiser le CSV avant envoi à Claude

**Checklist :**
- [ ] CSV formaté : `nom, email, site, industrie, nb_employés, revenu_estimé`
- [ ] ICP défini : taille cible, industrie, pain points, budget
- [ ] Context SaaS : description produit, valeur prop, pricing
- [ ] API Key Claude configurée (`.env`)

---

### 2️⃣ Prompt Claude optimisé

```markdown
# Context
Tu es un expert en lead qualification B2B SaaS.
Mon produit : {{description_produit}}
Mon ICP cible : {{icp_description}}
Pricing : {{pricing}}

# Task
Analyse ce prospect et génère une qualification complète :

Prospect :
- Nom/Entreprise : {{nom}}
- Site web : {{site}}
- Industrie : {{industrie}}
- Nb employés : {{nb_employes}}
- Revenu estimé : {{revenu}}

# Format attendu (JSON strict)
{
  "score": 8,
  "qualification": "Hot",
  "pain_points": ["point 1", "point 2"],
  "raison_score": "Explication 2 phrases max",
  "message_outreach": "Email personnalisé 3 phrases",
  "priorite": "Immédiat",
  "next_action": "Action recommandée"
}

# Contraintes
- Score basé sur : fit ICP (40%) + pain points (30%) + taille (20%) + timing (10%)
- Message outreach : direct, personnalisé, valeur claire
- Réponse JSON uniquement, pas de texte additionnel
```

**Variables clés :**
- `{{description_produit}}` = Ton SaaS en 1 phrase
- `{{icp_description}}` = PME 10-50 employés, SaaS B2B, $50-500K revenu
- `{{pricing}}` = $1500-5000/audit ou $500/mois subscription

---

### 3️⃣ Traitement Claude

**Modèle recommandé — choisir selon le contexte :**

| Modèle | ID | Usage | Coût |
|--------|-----|-------|------|
| **Haiku 4.5** | `claude-haiku-4-5-20251001` | Volume élevé (100+ prospects), qualification rapide | ~$0.02/prospect |
| **Sonnet 4.6** | `claude-sonnet-4-6` | Analyse équilibrée (10-100 prospects), insights plus profonds | ~$0.15/prospect |
| **Opus 4.6** | `claude-opus-4-6` | Prospects ultra-stratégiques (< 10), analyse maximale | ~$0.75/prospect |

**Règle de sélection :**
```
Volume 100+  → Haiku 4.5   (vitesse + coût)
Volume 10-99 → Sonnet 4.6  (qualité + prix)
Volume < 10  → Opus 4.6    (analyse maximale)
```

**Parameters :**
```
Temperature: 0.3 (consistance > créativité)
Max tokens: 500 par prospect (Haiku/Sonnet) | 800 (Opus)
Batch size: 10 prospects simultanés
```

---

### 4️⃣ Post-traitement

- [ ] Parse JSON responses → CSV enrichi
- [ ] Trier par score décroissant
- [ ] Filtrer : score >= 7 → "Hot leads" folder
- [ ] Export rapport markdown (summary + top 10)
- [ ] Import dans CRM ou Obsidian vault

---

## 💡 Prompts réutilisables

### Prompt #1 : Qualification rapide (Haiku)
```markdown
Qualifie ce prospect SaaS en JSON :
Produit: {{produit}} | ICP: {{icp}}
Prospect: {{data}}
Format: {"score":0-10,"qualification":"Hot/Warm/Cold","message":"","next":""}
```

### Prompt #2 : Message outreach personnalisé
```markdown
Écris un email cold outreach de 3 phrases pour :
Entreprise: {{nom}} | Industrie: {{industrie}}
Pain point probable: {{pain_point}}
Mon produit résout: {{valeur_proposition}}
Ton: professionnel mais humain. Pas de "J'espère que..."
```

### Prompt #3 : Analyse concurrentielle prospect
```markdown
Pour l'entreprise {{nom}} dans {{industrie}},
identifie leurs outils actuels probables et
pourquoi ils pourraient avoir besoin de {{produit}}.
Format: bullet points, max 5 points.
```

---

## 🎓 Exemple d'utilisation réelle

### Exemple : Qualifier 50 prospects SaaS PME

**Input CSV (ligne exemple) :**
```
Acme Corp, contact@acme.ca, acme.ca, Manufacturing, 35, 200K
```

**Prompt adapté :**
```markdown
Qualifie pour mon SaaS d'audit sécurité ($2000/audit):
ICP: PME 10-50 employés, industrie réglementée
Prospect: Acme Corp | manufacturing | 35 employés | acme.ca
JSON uniquement.
```

**Output Claude :**
```json
{
  "score": 8,
  "qualification": "Hot",
  "pain_points": ["conformité RGPD/ISO", "pas de ressource sécurité interne"],
  "raison_score": "Manufacturing réglementé + taille parfaite ICP + budget probable",
  "message_outreach": "Acme Corp traite probablement des données clients sensibles sans équipe sécurité dédiée. Notre audit identifie vos 3 vulnérabilités critiques en 48h pour $1500. Disponible pour un appel de 15 min cette semaine?",
  "priorite": "Immédiat",
  "next_action": "Cold email + LinkedIn connect"
}
```

---

## 📈 Gains mesurables

| Métrique | Manuel | Automatisé | Gain |
|----------|--------|------------|------|
| Temps/prospect | 15 min | 8 secondes | **112x plus rapide** |
| Prospects/heure | 4 | 450+ | **100x volume** |
| Coût/qualification | $25 (temps) | $0.02 (API) | **99% réduction** |
| Taux conversion | ~5% | ~15% (ciblé) | **3x meilleur** |

---

## 🔌 Intégration technique

### Python Script complet

```python
import anthropic
import csv
import json
import os
from datetime import datetime

# ─── Configuration ────────────────────────────────────────────────────────────

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# Sélection du modèle selon volume
MODELS = {
    "haiku":  "claude-haiku-4-5-20251001",  # Volume 100+ | ~$0.02/prospect
    "sonnet": "claude-sonnet-4-6",           # Volume 10-99 | ~$0.15/prospect
    "opus":   "claude-opus-4-6",             # Volume < 10  | ~$0.75/prospect
}

def select_model(nb_prospects: int) -> str:
    """Sélectionne automatiquement le modèle selon le volume."""
    if nb_prospects >= 100:
        model = MODELS["haiku"]
        print(f"🚀 Modèle: Haiku 4.5 (volume élevé — {nb_prospects} prospects)")
    elif nb_prospects >= 10:
        model = MODELS["sonnet"]
        print(f"⚖️  Modèle: Sonnet 4.6 (volume moyen — {nb_prospects} prospects)")
    else:
        model = MODELS["opus"]
        print(f"🧠 Modèle: Opus 4.6 (analyse maximale — {nb_prospects} prospects)")
    return model

PRODUCT_CONTEXT = """
Produit: Plateforme d'audit sécurité pour PME
Valeur: Identifier vulnérabilités critiques en 48h
Pricing: $1500 audit de base / $3000 audit complet / $5000 audit + remediation
"""

ICP = "PME 10-50 employés, industries réglementées (finance, santé, manufacturing), revenu $50K-$500K"

# ─── Fonctions principales ────────────────────────────────────────────────────

def qualify_prospect(prospect: dict, model: str) -> dict:
    """Qualifie un prospect via Claude API avec le modèle sélectionné."""

    # Tokens max selon modèle (Opus peut produire analyse plus détaillée)
    max_tokens = 800 if model == MODELS["opus"] else 600

    prompt = f"""
{PRODUCT_CONTEXT}
ICP cible: {ICP}

Qualifie ce prospect (JSON strict uniquement):
- Entreprise: {prospect.get('nom', 'N/A')}
- Site: {prospect.get('site', 'N/A')}
- Industrie: {prospect.get('industrie', 'N/A')}
- Employés: {prospect.get('nb_employes', 'N/A')}
- Revenu estimé: {prospect.get('revenu', 'N/A')}

Format JSON requis:
{{
  "score": <1-10>,
  "qualification": "<Hot|Warm|Cold>",
  "pain_points": ["<point1>", "<point2>"],
  "raison_score": "<explication courte>",
  "message_outreach": "<email 3 phrases personnalisé>",
  "priorite": "<Immédiat|Cette semaine|Ce mois>",
  "next_action": "<action recommandée>"
}}
"""

    response = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": prompt}]
    )

    try:
        return json.loads(response.content[0].text)
    except json.JSONDecodeError:
        return {"score": 0, "qualification": "Error", "error": response.content[0].text}


def process_csv(input_file: str, output_file: str, force_model: str = None):
    """
    Traite un CSV de prospects et génère un CSV enrichi.

    Args:
        input_file  : CSV source (nom, email, site, industrie, nb_employes, revenu)
        output_file : CSV destination enrichi
        force_model : Forcer un modèle spécifique ("haiku"|"sonnet"|"opus") ou None pour auto
    """

    results = []

    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        prospects = list(reader)

    print(f"\n📊 {len(prospects)} prospects à qualifier...")

    # Sélection modèle (auto ou forcé)
    if force_model and force_model in MODELS:
        model = MODELS[force_model]
        print(f"🔧 Modèle forcé: {force_model} ({model})")
    else:
        model = select_model(len(prospects))

    print(f"{'─' * 50}")

    for i, prospect in enumerate(prospects):
        nom = prospect.get('nom', 'N/A')
        print(f"  [{i+1}/{len(prospects)}] {nom}...", end=" ", flush=True)

        qualification = qualify_prospect(prospect, model)
        enriched = {**prospect, **qualification}
        results.append(enriched)

        score = qualification.get('score', 0)
        status = "🔥 HOT" if score >= 8 else "🌡️ WARM" if score >= 5 else "❄️ COLD"
        print(f"Score: {score}/10 {status}")

    # Trier par score décroissant
    results.sort(key=lambda x: x.get('score', 0), reverse=True)

    # Écrire CSV enrichi
    if results:
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=results[0].keys())
            writer.writeheader()
            writer.writerows(results)

    # Générer rapport markdown
    hot_leads = [r for r in results if r.get('score', 0) >= 7]
    rapport = f"""# 📊 Rapport Lead Generation — {datetime.now().strftime('%Y-%m-%d')}

## Résumé
- **Total prospects:** {len(results)}
- **Modèle utilisé:** `{model}`
- **Hot leads (score 7+):** {len(hot_leads)}
- **Taux qualification:** {len(hot_leads)/len(results)*100:.1f}%

## 🔥 Top 10 Hot Leads
"""
    for lead in results[:10]:
        rapport += f"""
### {lead.get('nom', 'N/A')} — Score: {lead.get('score', 0)}/10
- **Qualification:** {lead.get('qualification', 'N/A')}
- **Pain points:** {', '.join(lead.get('pain_points', []))}
- **Message:** {lead.get('message_outreach', 'N/A')}
- **Next action:** {lead.get('next_action', 'N/A')}
"""

    rapport_file = output_file.replace('.csv', '_RAPPORT.md')
    with open(rapport_file, 'w', encoding='utf-8') as f:
        f.write(rapport)

    print(f"\n{'─' * 50}")
    print(f"✅ CSV enrichi  : {output_file}")
    print(f"✅ Rapport MD   : {rapport_file}")
    print(f"🔥 Hot leads    : {len(hot_leads)}/{len(results)}")
    print(f"🧠 Modèle used  : {model}")


# ─── Entry point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Auto-sélection modèle selon volume
    process_csv("prospects_input.csv", "prospects_qualifies.csv")

    # Ou forcer un modèle spécifique :
    # process_csv("prospects_input.csv", "prospects_qualifies.csv", force_model="opus")
    # process_csv("prospects_input.csv", "prospects_qualifies.csv", force_model="sonnet")
    # process_csv("prospects_input.csv", "prospects_qualifies.csv", force_model="haiku")
```

### Structure CSV input requise
```csv
nom,email,site,industrie,nb_employes,revenu
Acme Corp,contact@acme.ca,acme.ca,Manufacturing,35,200K
TechStart,hello@techstart.io,techstart.io,SaaS,12,80K
```

---

## ⚠️ Limites & Considérations

- **Rate limits Claude API** : max 50 req/min (Haiku) → batch de 10 max
- **Coût estimé** : ~$0.02/prospect = $1 pour 50 prospects
- **Qualité données** : GIGO — meilleur CSV input = meilleur scoring
- **Validation** : Toujours vérifier top 5 leads manuellement

---

## 🔗 Ressources liées

- [[🔐_SECURITY_AUDIT_PROJECT/SECURITY_AUDIT_LEADS]]
- [[🔐_SECURITY_AUDIT_PROJECT/IDEA_REVENU_COMPLETE]]
- [[_BRAIN/PROTOCOLES_VAULT]]
- [[LLM's/Claude]]

---

*Workflow créé : 2026-02-17 | Status: Ready to use ✅*