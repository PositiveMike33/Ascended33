## 💰 SKILL REVENUE

### "revenue-prospect-analyzer"

**Objectif:** Analyser un profil LinkedIn de CTO pour voir s'il est bon prospect pour sécurité audit.

Crée ce fichier: `revenue-prospect-analyzer/Skill.md`

```yaml
---
name: revenue-prospect-analyzer
description: |
  Analyse un profil LinkedIn de CTO/responsable IT pour voir si c'est un BON PROSPECT 
  pour notre service de security audit à $5,500.
  Utilise quand je te partage un profil LinkedIn à analyser.
---

## Vue d'ensemble
Ce skill prend un profil LinkedIn (nom, poste, entreprise, taille, industrie) 
et te dit: "BON PROSPECT ✅" ou "À PASSER ❌" avec raison.

Ça t'économise des heures de recherche manuelle!

## Instructions
1. **Lire le profil** — Poste, entreprise, taille, industrie, seniority
2. **Évaluer les critères:**
   - Entreprise tech? (startup, SaaS, fintech = OUI; retail = NON)
   - Taille 20-75 employees? (Sweet spot = OUI; trop petit/gros = NON)
   - Responsable IT/Security/CTO/VP Eng? (OUI = décideur; non = passe)
   - À Montréal ou région? (OUI = proximité; NON = passe)
3. **Scorer 1-10** (10 = excellent prospect, 1 = à passer)
4. **Donner résumé** — Pourquoi BON/MAUVAIS prospect

## Exemples

**Input:**
```
Nom: Jean-Paul Leblanc
Poste: VP Engineering
Entreprise: TechStartup MTL
Taille: 35 employees
Industrie: SaaS/Fintech
Location: Montréal, QC
```

**Output:**
```
✅ BON PROSPECT (Score: 9/10)

Raison:
- VP Engineering = décideur direct ✅
- 35 employees = sweet spot parfait ✅
- SaaS/Fintech = valeur sécurité critique ✅
- Montréal = proximité pour meetings ✅
- Probabilité intérêt: 85%

Action: PRIORITÉ HAUTE pour outreach
Angle d'approche: "Vous cherchez à sécuriser votre stack fintech?"
```

## Quand utiliser ce skill
- Tu as une liste de 50 CTOs et veux les qualifier rapidement
- Tu veux pas gaspiller temps sur mauvais prospects
- Tu veux scorer de façon cohérente

## Critères de scoring
- **9-10:** VP/CTO, tech, 20-75 emp, MTL région → IMMÉDIAT
- **6-8:** Bon profil mais quelques critères manquent → À CONTACTER
- **3-5:** Peut-être, mais moins prioritaire → FOLLOW-UP LATER
- **1-2:** Pas bon fit → PASSER

## Notes
Si tu as des doutes, dis "score 7/10 - à évaluer manuellement".
Mieux vaut être prudent que de dépenser temps sur bad prospects.
```
