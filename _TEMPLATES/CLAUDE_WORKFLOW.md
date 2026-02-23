---
date: {{date}}
type: claude-workflow
tags: [claude, automation, prompt, {{category}}]
status: draft
---

# 🤖 CLAUDE WORKFLOW — {{nom_workflow}}

> Workflow intégrant Claude pour maximiser productivité & revenus.

---

## 🎯 Objectif du workflow

> Quel problème résout ce workflow ? Résultat attendu ?

---

## 📊 Input → Output

### Données en entrée
```
Type 1:
Type 2:
```

### Résultat final attendu
```
Format:
Utilisation:
```

---

## 🔄 Étapes du processus

### 1️⃣ Capture/Préparation
> Comment préparer les données pour Claude ?

**Checklist :**
- [ ] Données formatées correctement
- [ ] Contexte fourni
- [ ] Exemples inclus (si pertinent)

---

### 2️⃣ Prompt Claude optimisé

```markdown
[PROMPT COMPLET UTILISÉ AVEC CLAUDE]

# Context
{{contexte}}

# Task
{{tâche}}

# Format attendu
{{format}}

# Exemples (si applicable)
{{exemples}}

# Contraintes
- Contrainte 1
- Contrainte 2
```

**Variables clés :**
- `{{variable1}}` = Description
- `{{variable2}}` = Description

---

### 3️⃣ Traitement Claude

**Modèle utilisé :**
- [ ] Claude 3.5 Sonnet (optimal pour tâches complexes)
- [ ] Claude 4.5 Opus (pour tasks ultra-complexes)
- [ ] Claude Haiku (léger, rapide, cost-efficient)

**Temperature / Parameters :**
```
Temperature:
Top P:
Max tokens:
```

---

### 4️⃣ Post-traitement

> Comment affiner/intégrer les résultats Claude ?

- [ ] Étape 1:
- [ ] Étape 2:
- [ ] QA/Review

---

## 💡 Prompts réutilisables

### Prompt #1 : {{nom}}
```markdown
[PROMPT]
```

### Prompt #2 : {{nom}}
```markdown
[PROMPT]
```

---

## 🎓 Exemples d'utilisation réelle

### Exemple 1
**Input :**
```
[Input réel]
```

**Prompt utilisé :**
```markdown
[Prompt adapté]
```

**Output Claude :**
```
[Résultat]
```

**Résultat final :**
```
[Après post-traitement]
```

---

## 📈 Gains mesurables

| Métrique | Avant | Après | Gain |
|----------|-------|-------|------|
| Temps/tâche | | | |
| Qualité | | | |
| Coût | | | |
| Volume | | | |

---

## 🔌 Intégration technique (si applicable)

### API Claude

```python
import anthropic

client = anthropic.Anthropic(api_key="your-key")

response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": "{{prompt}}"
        }
    ]
)

print(response.content[0].text)
```

### Zapier / Make Integration
- Trigger:
- Action:
- Webhook:

---

## ⚠️ Limites & Considerations

- Limite 1:
- Limite 2:
- Cas d'exception:

---

## 🔗 Ressources liées

- [[Prompt Library]]
- [[Claude API Docs]]
- [[Related Workflow]]

---

*Workflow créé : {{date}} | Dernière mise à jour : {{date}}*
