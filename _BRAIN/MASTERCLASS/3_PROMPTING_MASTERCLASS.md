# ✍️ PROMPTING MASTERCLASS — Parler comme un Pro à Claude

**Date:** 14-02-2026  
**Niveau:** Débutant → Avancé  
**Durée:** ~30 min (+ 30 min practice)  
**Lien:** [[1_SKILLS_MASTERCLASS]] | [[2_MCP_MASTERCLASS]] | [[4_INTEGRATION_3_PILIERS]]

---

## 🎯 OBJECTIF DE CE COURS

À la fin, tu pourras:
✅ Utiliser les 6 techniques de prompting avancé  
✅ Écrire des prompts qui génèrent des réponses de qualité 10x  
✅ Adapter ton style de prompting pour revenue + hacking  
✅ Maximiser la valeur de chaque conversation Claude  

---

## 📚 PARTIE 1 — LES 6 TECHNIQUES FONDAMENTALES

### Technique 1: RÔLE (Role-Playing)

**Concept:** Dis à Claude quel rôle d'expert il doit jouer

```
❌ FAIBLE: "Aide-moi à écrire un email de prospection"

✅ EXCELLENT: "Tu es un copywriter expert en B2B SaaS avec 15 ans d'expérience.
Tu spécialises dans les emails de prospection qui génèrent 20%+ de taux 
de réponse. Tu parles français québécois professionnel (pas trop formel,
pas trop familier). Tu connais la vente consultative."
```

**Pourquoi ça marche?**
- Claude adapte son ton/style au rôle
- Claude ajoute expertise du domaine
- Résultats plus cohérents avec ce que tu attends

---

### Technique 2: CONTEXTE (Context)

**Concept:** Explique qui TU es et pourquoi tu as besoin de ça

```
❌ FAIBLE: "Analyse ce prospect"

✅ EXCELLENT: "Je suis consultant en sécurité IT basé à Montréal.
Je vends des audits de sécurité à PMEs tech ($5,500 par projet).
Mes prospects idéaux: VP Engineering/CTO, SaaS/fintech, 20-75 employees, Montréal.
Je veux qualifier les prospects rapidement pour ne pas gaspiller temps."
```

**Pourquoi ça marche?**
- Claude comprend tes contraintes réelles
- Claude personalise la réponse
- Moins de "generic advice", plus de "actionable insights"

---

### Technique 3: XML TAGS (Structure)

**Concept:** Utilise balises XML pour structurer ton prompt clairement

```xml
<role>
Tu es un expert en analyse de données
</role>

<context>
Je dois qualifier 100 prospects en 2 heures
</context>

<task>
Analyse ce prospect et dis-moi si c'est bon fit
</task>

<constraints>
Max 5 minutes par prospect
Donne un score 1-10
Sois brutal dans ton évaluation
</constraints>

<output_format>
Score: X/10
Raison: [1-2 phrases]
CTA: [Action suivante]
</output_format>
```

**Pourquoi ça marche?**
- Structure claire = moins d'ambiguïté
- Claude sait exactement ce qui est important
- Résultats plus structurés et prévisibles

---

### Technique 4: MULTISHOT (Examples)

**Concept:** Montre des exemples input/output pour calibrer le style

```
Tu es un analyste de prospection.

Exemple 1:
INPUT: "Jean-Paul, VP Engineering, 40 emp, SaaS, Montréal"
OUTPUT: "✅ 9/10 — Décideur direct, taille parfaite, tech, local"

Exemple 2:
INPUT: "Marie, HR Manager, 200 emp, Retail, Toronto"
OUTPUT: "❌ 2/10 — HR ≠ décideur IT, retail bas-priorité, pas local"

Maintenant analyse: "Claude, CTO, 25 emp, Fintech, Montréal"
```

**Pourquoi ça marche?**
- Claude voit le pattern attendu
- Claude adapte son style automatiquement
- Consistency à travers plusieurs analyses

---

### Technique 5: CHAIN-OF-THOUGHT (Réflexion)

**Concept:** Demande à Claude de "réfléchir" avant de répondre

```
Avant de répondre, réfléchis étape par étape dans des balises <thinking>.
Puis donne ta réponse finale dans <answer>.

<thinking>
1. Analyser le problème...
2. Considérer les options...
3. Évaluer les trade-offs...
</thinking>

<answer>
Ma recommandation est...
</answer>
```

**Pourquoi ça marche?**
- Claude fait un "reasoning" visible
- Moins d'erreurs logiques
- Tu peux auditer la réflexion

---

### Technique 6: CHAÎNER LES PROMPTS (Decomposition)

**Concept:** Décompose une tâche complexe en étapes séquentielles

```
Tâche: "Crée un plan d'outreach revenue complet"

STEP 1: "Analyse ces 50 CTOs et crée une liste des TOP 10 prospects"
STEP 2: "Pour chaque prospect, crée un message personnalisé"
STEP 3: "Organise ces 10 messages dans un plan d'action par semaine"
STEP 4: "Crée un tracking spreadsheet avec des métriques"
```

**Pourquoi ça marche?**
- Problèmes complexes deviennent simples
- Claude excelle à des tâches bien-définies
- Meilleure qualité que "fais-moi tout à la fois"

---

## 💰 PARTIE 2 — EXEMPLE REVENUE

### Scénario: Écrire un email de prospection EXCELLENT

#### AVANT (Mauvais prompt):
```
Écris un email de prospection pour un CTO
```

**Résultat:** Generic, pas bon, pas personnalisé.

---

#### APRÈS (Excellent prompt):

```xml
<role>
Tu es un copywriter B2B expert avec 15 ans d'expérience en SaaS.
Tu spécialises dans les emails de prospection qui créent urgence + crédibilité.
Tu sais qu'un email court et spécifique > email long et generic.
</role>

<context>
Je suis consultant en sécurité IT à Montréal.
Je vends des audits de sécurité complète ($5,500, 2 semaines).
Mon prospect: Jean-Paul Leblanc, VP Engineering, fintech avec 35 employees.
Leur tech stack: React frontend, Node.js backend, PostgreSQL, AWS.
Ils croissent rapidement (~20% YoY) mais n'ont pas d'audit de sécurité récent.
</context>

<task>
Écris un email pour Jean-Paul qui:
1. Crée URGENCE autour de la sécurité (fintech = haute exposure)
2. Montre que tu comprends leur stack spécifique
3. Propose un meeting court (30 min) pour une "quick assessment"
4. Ends with clear next step
</task>

<constraints>
- Max 150 mots
- Ton: Professionnel mais humain (pas salesy)
- Include 1 social proof ou win recent
- No jargon technique excessif
- Subject line that creates curiosity (not salesy)
</constraints>

<examples>
GOOD: "Jean-Paul, j'ai vu que vous scalez rapidement — souvent le moment où 
on oublie la sécurité. J'ai aidé 12 SaaS similaires à passer leur audit. 
On parle 30 min?"

BAD: "Hi Jean-Paul! We offer comprehensive security auditing solutions for 
your organization. Our services include..."
</examples>

<output>
Subject line: [optimized]
Email body: [150 words max]
Alternative subjects: [2 other options]
</output>
```

**Résultat:** Email spécifique, personnalisé, haute conversion! 🎯

---

## 🔐 PARTIE 3 — EXEMPLE HACKING

### Scénario: Documenter un CTF walkthrough

#### MAUVAIS PROMPT:
```
Documente ce CTF
```

---

#### BON PROMPT:

```xml
<role>
Tu es un expert en cybersécurité créant des ressources pédagogiques
pour des hackers éthiques (niveau intermédiaire).
Ton but: expliquer le POURQUOI, pas juste le HOW.
</role>

<context>
Je viens de résoudre un CTF de SQL injection sur TryHackMe.
Je veux documenter ça pour:
1. Consolider mon learning
2. Créer un portfolio pour certification CEH
3. Aider d'autres à apprendre
</context>

<task>
Transforme mon recap brut en un walkthrough PROFESSIONNEL qui inclut:
1. Contexte du challenge
2. Étapes détaillées avec EXPLICATIONS (pas juste commandes)
3. Les payloads utilisées + pourquoi elles marchent
4. Les concepts clés OWASP Top 10
5. Comment défendre contre cette attaque
6. Ressources pour aller plus loin
</task>

<constraints>
- Format MARKDOWN
- Tagging: [[ctf]] [[sql-injection]] [[learning]] [[beginner]] [[owasp]]
- Link à OWASP Top 10 relevante
- Tone: Éducatif (expliquer aux débutants)
- Structure: Utilisable dans portfolio
</constraints>

<output_format>
# 🔐 [CTF Name] — Walkthrough Complet

**Challenge:** [Description]
**Difficulty:** X/10
**Time:** [temps utilisé]
**Category:** [OWASP categoria]

## Walkthrough
[Étapes détaillées]

## Concepts Clés
[Ce qu'on apprend]

## Défense
[Comment se protéger]

## Resources
[Liens utiles]
</output_format>
```

**Résultat:** Walkthrough professionnel utilisable dans portfolio! 📚

---

## 🧠 PARTIE 4 — TEMPLATE UNIVERSEL

### Tu peux utiliser ce template pour TOUT:

```xml
<role>
Je suis [expert en quoi, avec combien d'années].
Je specialise dans [domaine specifique].
Mon style: [ton, approach].
</role>

<context>
Je suis [qui tu es, ton rôle].
J'ai besoin de ça parce que [pourquoi c'est urgent/important].
Contraintes: [budget/time/ressources].
</context>

<task>
[Instruction claire et spécifique]
Les sous-tâches:
1. [Sous-tâche 1]
2. [Sous-tâche 2]
3. [Sous-tâche 3]
</task>

<examples>
[Input 1] → [Output 1]
[Input 2] → [Output 2]
</examples>

<constraints>
Max [longueur/durée]
Ton: [formel/décontracté/technique]
Format: [liste/tableau/code/prose]
[Autre constraint]
</constraints>

<output>
[Structure exacte attendue]
</output>
```

---

## 💡 PARTIE 5 — LES ERREURS À ÉVITER

### ❌ Erreur 1: Prompt trop court
```
❌ "Aide-moi avec mon budget"
✅ "J'ai $3,600/mois de revenu fixe, $1,190 dépenses fixes. Aide-moi 
   à budgetter pour lancer une offre de sécurité audit ($5,500/projet) 
   avec ROI clair."
```

### ❌ Erreur 2: Pas de contexte personnel
```
❌ "Crée un script Python"
✅ "Je dois crawler 100 prospects LinkedIn CTOs à Montréal, extraire 
   nom/email/entreprise, sauvegarder dans CSV. Je suis débutant Python."
```

### ❌ Erreur 3: Pas d'exemples
```
❌ "Qualifie ce prospect"
✅ "GOOD: Score 9/10 parce que VP Engineering + SaaS + 40 emp + Montréal
    BAD: Score 2/10 parce que HR + retail + 200 emp + Toronto
    Maintenant qualifie: [prospect]"
```

### ❌ Erreur 4: Trop d'attentes à la fois
```
❌ "Crée une stratégie revenue complète avec pricing, leads, outreach, 
   proposals, et closing tactics"
✅ "Step 1: Crée 5 idées de services revenue"
   [Puis Step 2, Step 3, etc. séparément]
```

---

## 🎬 EXERCICE 1 — Réécrire un de tes prompts

Prends un prompt que tu utilises souvent et réécris-le avec:
- [ ] Un rôle clair
- [ ] Du contexte personnel
- [ ] Balises XML
- [ ] Au moins 1 exemple
- [ ] Des contraintes explicites

Compare les résultats. Tu vas voir la différence! 🚀

---

## 🎬 EXERCICE 2 — Prompt audit

Prends ces 3 prompts et juge-les 1-10 (10 = excellent):

```
PROMPT A: "Crée un plan d'action revenue"
Score: ___/10

PROMPT B: "Je vends sécurité audit à PMEs ($5.5K). Crée un plan 
pour générer $15K en 3 mois avec LinkedIn outreach."
Score: ___/10

PROMPT C: 
<role>Je suis consultant sécurité IT avec 8 ans d'expérience à Montréal</role>
<context>Je dois générer $15K de revenue en 3 mois via service audit sécurité ($5.5K/projet)</context>
<task>Crée un plan d'action avec: lead strategy, outreach, conversion</task>
<constraints>Je peux dédier 10 hrs/semaine. Besoin de ROI clair.</constraints>
Score: ___/10
```

**Réponses:** A: 2/10 | B: 5/10 | C: 9/10

---

## ✅ CHECKLIST FINAL

- [ ] Je comprends les 6 techniques (rôle, contexte, XML, examples, CoT, chaining)
- [ ] J'ai reécrit 1 prompt avec la structure XML
- [ ] J'ai testé 2 prompts similaires et comparé les résultats
- [ ] Je sais quand utiliser chaîner les prompts vs. un seul prompt
- [ ] Je peux reconnaître un "bad prompt" et le fixer

---

## 🎯 PROCHAINE ÉTAPE

Voir: [[4_INTEGRATION_3_PILIERS]] — Combiner Skills + MCP + Prompts ensemble  
Voir: [[1_SKILLS_MASTERCLASS]] — Créer tes skills

---

**Tags:** [[prompting]] [[claude]] [[communication]] [[leverage]] [[automation]] [[14-02-2026]]
