# 🎓 SKILLS MASTERCLASS — Créer tes Premiers Skills

**Date:** 14-02-2026  
**Niveau:** Débutant → Intermédiaire  
**Durée:** ~30 min pour comprendre + créer 1er skill  
**Lien:** [[4_INTEGRATION_3_PILIERS]] | [[2_MCP_MASTERCLASS]] | [[3_PROMPTING_MASTERCLASS]]

---

## 🎯 OBJECTIF DE CE COURS

À la fin, tu pourras:
✅ Créer un skill Markdown simple (pas besoin de code!)  
✅ Packager et upload ton skill dans Claude  
✅ Automatiser tes workflows récurrents  
✅ Créer des skills pour revenue + hacking  

---

## 📚 PARTIE 1 — THÉORIE FONDAMENTALE

### C'est quoi exactement un Skill?

**Un Skill = Un dossier avec Skill.md**

```
mon-skill/
├── Skill.md          ← Le fichier MAGIQUE (c'est tout ce que tu dois pour commencer!)
├── REFERENCE.md      ← Documentation optionnelle
└── assets/           ← Templates, exemples (optionnel)
```

**Le Skill.md contient:**
- Nom + Description (Claude les lit pour décider d'activer)
- Instructions claires (étapes que Claude doit suivre)
- Exemples (input/output pour calibrer)
- Cas d'usage (quand l'utiliser)

---

### Pourquoi les Skills?

| Avant Skills | Avec Skills |
|--------------|------------|
| Tu dis chaque fois: "Réécris cet email comme copywriter B2B, objectif = vendre service de $5K, ton = pro mais humain, max 150 mots" | Tu dis: "Email de prospection revenue" et Claude sait exactement quoi faire |
| Claude oublie ton contexte à chaque conversation | Ton contexte est **sauvegardé** dans le skill |
| Tu dois répéter le même prompt 100 fois | Un skill = réutilisable infiniment |

---

## 🛠️ PARTIE 2 — CRÉER TON 1ER SKILL (SIMPLE!)

### Template de base — COPIER/COLLER

```yaml
---
name: mon-premier-skill
description: |
  Décris rapidement ce que fait ce skill ET QUAND l'utiliser.
  Ex: Analyse des prospects LinkedIn pour mon service de security audit.
  Utilise quand tu me donne un profil de CTO.
---

## Vue d'ensemble
Explique en 2-3 phrases claires ce que le skill fait.

## Instructions
1. Étape 1 — Comprendre le contexte
2. Étape 2 — Analyser/traiter
3. Étape 3 — Outputter le résultat

## Exemples
**Input:**
[Exemple de ce que tu donnes au skill]

**Output:**
[Exemple du résultat attendu]

## Quand utiliser ce skill
- Cas d'usage 1
- Cas d'usage 2
- Cas d'usage 3

## Notes importantes
Toute précision qui aide Claude à bien faire le job.
```

---

## 💰 EXEMPLE 1 — SKILL REVENUE

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

---

## 🔐 EXEMPLE 2 — SKILL HACKING

### "ctf-walkthrough-documenter"

**Objectif:** Documenter automatiquement un CTF que tu viens de résoudre, avec lessons learned.

Crée ce fichier: `ctf-walkthrough-documenter/Skill.md`

```yaml
---
name: ctf-walkthrough-documenter
description: |
  Tu me décris comment tu as résolu un CTF (les étapes, les payloads, les tricks).
  Je crée une note ETHICAL_HACKING_NOTE parfaitement formatée avec:
  - Walkthrough complet
  - Concepts clés appris
  - Défenses à connaître
  - Ressources pour aller plus loin
  
  Utilise quand tu finis un CTF et veux le documenter.
---

## Vue d'ensemble
Ce skill prend ton CTF recap brut et le transforme en note 
PROFESSIONELLE prête pour ton portfolio + learning path OWASP.

## Instructions
1. **Récupérer ton recap CTF** (étapes, commandes, payloads)
2. **Formater dans structure ETHICAL_HACKING_NOTE:**
   - Challenge: [nom]
   - Difficulty: [1-10]
   - Concepts: [liste skills apprises]
   - Walkthrough: [étapes avec explanations]
   - Payloads: [exploits utilisés]
   - Lessons: [ce que t'as appris]
   - Defense: [comment défendre contre ça]
   - Resources: [liens utiles]
3. **Ajouter liens** vers OWASP Top 10 categoria
4. **Tagging** automatique (#ctf #hacking #learning #[category])

## Exemples

**Input:**
```
CTF: SQL Injection 101 on TryHackMe
Difficulty: Easy

Steps:
1. Discovered login form
2. Tried ' OR '1'='1 -- and bypassed login
3. Found admin panel
4. Used UNION injection to extract user table
5. Got flag: flag{sql_injection_is_dangerous}

Learned: SQL injection, UNION-based injection, comment syntax
```

**Output:**
```
# 🔐 CTF: SQL Injection 101 — TryHackMe

**Difficulty:** 2/10 (Beginner)
**Category:** OWASP Top 10 #A03:2021 – Injection
**Date Completed:** 2026-02-14
**Time Spent:** 45 minutes

## 🎯 Challenge Summary
...
[Full formatted walkthrough]
...

## 🛡️ Defense & Mitigation
- Use parameterized queries (prepared statements)
- Input validation + sanitization
- WAF (Web Application Firewall)
- Principle of least privilege

## 📚 Next Steps
- Try SQL Injection Advanced on HackTheBox
- Study OWASP Top 10 #A01:2021 (Authentication)

#ctf #sql-injection #hacking #learning #beginner #owasp
```

## Quand utiliser ce skill
- Tu viens de résoudre un CTF
- Tu veux documenter pour ton learning path
- Tu construis un portfolio de walkthroughs

## Notes
Ça t'économise 30min de formatting par CTF.
Au bout de 10 CTFs = 5 heures de temps économisé = 1 vrai walkthrough qu'on peut vendre!
```

---

## 🧠 EXEMPLE 3 — SKILL CLAUDE MASTERY

### "claude-prompting-optimizer"

**Objectif:** Prendre un prompt mediocre et le rendre EXCELLENT avec structure XML + roleplay.

Crée ce fichier: `claude-prompting-optimizer/Skill.md`

```yaml
---
name: claude-prompting-optimizer
description: |
  Tu me donne un prompt (même brut/mal structuré).
  Je le réécris comme un PRO avec: rôle, contexte, instructions claires, 
  balises XML, exemples, contraintes.
  
  Utilise quand tu veux maximiser la qualité des réponses de Claude.
---

## Vue d'ensemble
Ce skill optimise ton communication avec Claude en utilisant les 6 techniques
de prompting avancé (rôle, XML, chain-of-thought, few-shot, etc.).

## Instructions
1. **Identifier l'intent** — Que veux-tu vraiment?
2. **Ajouter un rôle** — Claude = expert en quoi?
3. **Structurer avec XML** — <instructions>, <context>, <format>
4. **Donner exemples** — Input/output pour calibrer le style
5. **Ajouter contraintes** — Max longueur, ton, format
6. **Tester et refiner** — Affiner si nécessaire

## Exemples

**Input (Prompt brut):**
```
Améliore mon email de prospection
```

**Output (Prompt optimisé):**
```
<role>
Tu es un copywriter expert en B2B SaaS avec 10 ans d'expérience.
Tu spécialises dans les emails de prospection qui génèrent 20%+ de réponses.
Tu parles français québécois professionnel (pas trop formel).
</role>

<context>
Je suis consultant en sécurité IT basé à Montréal.
Je vends des audits de sécurité à PMEs tech ($5,500 par projet).
Mon prospect est un VP Engineering d'une fintech avec 40 employees.
</context>

<task>
Réécris cet email de prospection pour obtenir un meeting de 30 minutes.
Objectif: Créer urgence autour de "vous exposez vos données clients".
Ton: Professionnel mais human, pas salesy.
</task>

<constraints>
- Max 150 mots
- Include 1 specific win/social proof
- End with clear CTA (meeting request)
- Pas de "boilerplate" generic stuff
</constraints>

<output_format>
- Subject line (max 10 words)
- Email body (150 words max)
- Alt subject lines (2 variants)
</output_format>
```

## Quand utiliser ce skill
- Tu dois écrire un prompt important
- Tes résultats Claude sont mediocres
- Tu veux maximiser la qualité/pertinence

## Tips
Plus tu donnes de contexte + constraints = meilleure réponse.
"Sois concis" + "Sois créatif" = conflict. Sois spécifique!
```

---

## 📦 PARTIE 3 — PACKAGER ET UPLOAD

### Étape 1: Créer le dossier
```
revenue-prospect-analyzer/
├── Skill.md
└── REFERENCE.md (optionnel - liens utiles)
```

### Étape 2: Zipper
- Clique droit sur le dossier
- "Envoyer vers > Dossier compressé"
- Renomme en `revenue-prospect-analyzer.zip`

### Étape 3: Upload dans Claude
1. Ouvre Claude Desktop
2. Paramètres > Capacités
3. "Ajouter une capacité" > Upload ZIP
4. Sélectionne `revenue-prospect-analyzer.zip`
5. Active le skill
6. Teste avec: "Analyse ce profil: [profil LinkedIn]"

### Étape 4: Vérifier l'activation
Si Claude dit "Utilisation du skill revenue-prospect-analyzer" = ✅ Success!

---

## ✅ CHECKLIST AVANT UPLOAD

- [ ] Le nom du dossier = le nom dans le YAML
- [ ] Description dit QUOI + QUAND (pas trop long)
- [ ] Instructions claires et numérotées
- [ ] Au moins 1 exemple Input/Output
- [ ] "Quand utiliser ce skill" rempli
- [ ] Pas de clés API ou secrets
- [ ] Fichiers correctement formatés (pas d'erreurs Markdown)

---

## 🎬 TON EXERCICE

**Crée le 1er skill maintenant:**

1. Crée dossier: `D:\Vault\Vault\🧠_CLAUDE_MASTERY\SKILLS\revenue-prospect-analyzer\`
2. Crée `Skill.md` avec le template de l'EXEMPLE 1
3. Zippe et upload dans Claude
4. Teste avec un vrai profil LinkedIn
5. Observe si Claude active le skill automatiquement

**Résultat:** Tu auras automatisé 1 tâche récurrente! 🎉

---

## 🔗 PROCHAINE ÉTAPE

Voir: [[2_MCP_MASTERCLASS]] — Connecter Claude à tes outils  
Voir: [[4_INTEGRATION_3_PILIERS]] — Comment utiliser Skills + MCP + Prompts ensemble

---

**Tags:** #skills #automation #claude #learning #masterclass #14-02-2026
