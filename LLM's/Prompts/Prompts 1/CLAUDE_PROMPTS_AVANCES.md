---
date: 2026-02-14
type: prompts
tags: [claude, advanced, prompting, optimization]
---

# 🧠 CLAUDE PROMPTS AVANCÉS — Bibliothèque réutilisable

> Collection de prompts optimisés pour maximiser la valeur de Claude sur vos usecases productifs, revenu, et hacking.

---

## 🎯 Index

1. [[#Prompting Foundations](#Prompting-Foundations)]
2. [[#Revenue & Business](#Revenue--Business)]
3. [[#Ethical Hacking & Security](#Ethical-Hacking--Security)]
4. [[#Productivity & Workflows](#Productivity--Workflows)]
5. [[#Content Creation](#Content-Creation)]
6. [[#Code Generation](#Code-Generation)]

---

---

## Prompting Foundations

### 1️⃣ Chain-of-Thought (CoT) Template

**Usage :** Problèmes complexes nécessitant réflexion structurée

```markdown
Réfléchissez étape par étape pour [problème].

**Step 1: Comprendre le problème**
- Quel est le problème exatement?
- Quels sont les constraints?
- Quels sont les objectifs?

**Step 2: Identifier les options**
- Option A: ...
- Option B: ...
- Option C: ...

**Step 3: Évaluer chaque option**
- Option A — Pros: ... Cons: ... Score: X/10
- Option B — Pros: ... Cons: ... Score: X/10
- Option C — Pros: ... Cons: ... Score: X/10

**Step 4: Recommandation**
[Meilleure option avec justification]

Problème: [Votre problème ici]
```

---

### 2️⃣ Few-Shot Learning Template

**Usage :** Classification, pattern matching, output formatting

```markdown
Voici des exemples du format attendu:

**Exemple 1:**
Input: [exemple input 1]
Output: [exemple output 1]

**Exemple 2:**
Input: [exemple input 2]
Output: [exemple output 2]

**Exemple 3:**
Input: [exemple input 3]
Output: [exemple output 3]

---

Maintenant, faites la même chose pour:
Input: [votre input]
Output: ?
```

---

### 3️⃣ Structured Context Template

**Usage :** Tasks complexes avec beaucoup de contexte

```markdown
# Task Context

## Background
[Contexte détaillé du projet/situation]

## Current State
[État actuel — problèmes, ressources, blockers]

## Objective
[Objectif spécifique et mesurable]

## Constraints
- Budget: [si applicable]
- Timeline: [si applicable]
- Technical: [limitations tech]
- Other: [autres constraints]

## Success Criteria
- [ ] Critère 1 (mesurable)
- [ ] Critère 2 (mesurable)
- [ ] Critère 3 (mesurable)

## Expected Output Format
[Format spécifique attendu]

---

Basé sur tout ce contexte, [tâche spécifique].
```

---

---

## Revenue & Business

### 1️⃣ Service Ideation Prompt

**Usage :** Générer idées de service monétisables

```markdown
# Service Ideation

Je suis [Michaël], avec compétences en:
- [Skill 1: IA/Automation]
- [Skill 2: Ethical Hacking]
- [Skill 3: Obsidian/PKM]

Mon ICP (Ideal Customer Profile) est:
- Type: [startup/PME/enterprises]
- Pain point: [principal problème]
- Budget: $[X-Y]K

Générez 10 idées de service innovantes que je pourrais vendre dans ce marché.

Pour chaque idée, fournissez:
1. **Service name** — 1 line description
2. **Problem solved** — quoi exactement?
3. **Delivery model** — hourly/project/retainer/SaaS?
4. **Estimated revenue** — $ par mois/année
5. **Effort required** — low/medium/high
6. **Differentiator** — pourquoi c'est unique?
7. **First step** — comment commencer?
8. **Viability score** — 1-10

Rank them by: (Revenue potential * Ease of execution) / Effort required
```

---

### 2️⃣ Pricing Strategy Prompt

**Usage :** Calculer pricing optimal pour service

```markdown
# Pricing Analysis

**Service:** [Nom service]
**Description:** [1-2 line description]
**Target market:** [ICP description]

**Market research data (if available):**
- Competitors charging: $X-Y per...
- Industry standard: ...
- Customer budget typical: $...

**Your delivery:**
- Time to deliver: [X hours/weeks]
- Effort level: [high/medium/low]
- Scalability: [high/medium/low]
- Unique value: [key differentiator]

Proposez 3 modèles de pricing différents:

1. **Time-based** — $/hour
   - Justification
   - When to use
   - Pros/cons

2. **Project-based** — $/project
   - Scope definition
   - Price calculation
   - Why this works

3. **Value-based** — Based on customer value/ROI
   - How to calculate
   - Example customer
   - Potential earnings

---

**Recommendation:** Which model fits best? Why?

**ICP breakdown:**
- Who buys this most?
- What's their budget?
- How do you reach them?

**Go-to-market:**
- Where to find prospects?
- How to position?
- What's your advantage?
```

---

### 3️⃣ Lead Generation Prompt

**Usage :** Identifier et atteindre clients potentiels

```markdown
# Lead Generation Strategy

**Industry/Market:** [e.g., SaaS companies, agencies, etc.]
**Service:** [Your offering]
**Typical customer pain:** [Problem you solve]
**Budget range:** $[X-Y]K

Generate a lead generation strategy:

## 1. Target Company Profile
- Company size: [employees/revenue]
- Industry vertical: [specific industries]
- Technology stack: [what they use]
- Decision maker: [who has budget]

## 2. Top 10 Prospect Companies
[List with reasoning for each]

## 3. Outreach Strategy
- **Channel 1:** [LinkedIn/email/etc] — How to approach
- **Channel 2:** [Alternative method]
- **Cold email template:** [Basic template]
- **Success metrics:** [How you'll measure]

## 4. Positioning
- **Your unique angle:** [Why hire you vs competitors]
- **Case study needed:** [What to showcase]
- **Social proof:** [How to build credibility]

## 5. Sales Cycle
- **Timeline:** [How long from first contact to sale]
- **Touchpoints:** [How many interactions]
- **Objection handling:** [Common concerns + rebuttals]

Prioritize by: Ease of reach × Deal size × Close rate
```

---

---

## Ethical Hacking & Security

### 1️⃣ CTF Hint Prompt (Without spoilers)

**Usage :** Débloquer sur un CTF sans révéler la réponse

```markdown
# CTF Help Request

**Challenge:** [Name/Platform]
**Level:** [Difficulty]
**Category:** [Type: web/crypto/reverse-eng/etc]

**What I've tried:**
- Attempt 1: [what you tried + result]
- Attempt 2: [what you tried + result]
- Current understanding: [what you think]

**Where I'm stuck:**
[Describe the blockers]

**Without giving away the answer, help me by:**
1. Suggesting the next reconnaissance step
2. Recommending tools I might have missed
3. Highlighting a common pattern in this type of challenge
4. Asking clarifying questions about my approach

**My hypothesis:** [Your current theory about the vulnerability]

Is this direction promising? What should I explore?
```

---

### 2️⃣ Security Audit Prompt

**Usage :** Audit code/architecture pour vulnérabilités

```markdown
# Security Audit Request

**System/Code:** [Name + brief description]
**Type:** [Web app / API / Infrastructure / etc]
**Technology stack:** [Tech used]

[PASTE CODE/ARCHITECTURE HERE]

---

## Audit Scope

Analyze for vulnerabilities in:
- ✅ OWASP Top 10
- ✅ Authentication & authorization
- ✅ Data protection & encryption
- ✅ Input validation
- ✅ Error handling
- ✅ Logging & monitoring
- ✅ Secrets management

---

## Output Format

For each vulnerability found:
1. **Name** — What is it?
2. **Severity** — Critical/High/Medium/Low
3. **CWE** — [CWE number if applicable]
4. **Current risk** — What could happen?
5. **How to fix** — Specific code/architecture change
6. **Effort** — Time to fix
7. **Test** — How to verify it's fixed

---

Provide recommendations prioritized by severity × effort.
```

---

### 3️⃣ Exploit Development Prompt

**Usage :** Développer exploit (educational context only)

```markdown
# Exploit Development (Educational)

⚠️ **Context:** This is for [CTF / Lab / Educational purpose / Authorized pentest]

**Target vulnerability:** [CVE / CWE description]
**Affected system:** [What is vulnerable]
**Environment:** [Lab setup]

**What I understand:**
- How it works: [Your understanding]
- Why it's exploitable: [Root cause]
- Expected impact: [What an attacker could do]

**Help me develop a proof-of-concept by:**
1. Confirming my understanding is correct
2. Suggesting the exploit technique
3. Recommending tools/libraries
4. Providing pseudocode outline
5. Suggesting test cases

**I'll implement it myself** — just guide me on approach.

**Defense focus:** Once I exploit it, I'll document how to prevent/detect it.
```

---

---

## Productivity & Workflows

### 1️⃣ Daily Report Automation Prompt

**Usage :** Générer rapport quotidien structuré

```markdown
# Rapport Quotidien Automatisé — [DATE]

Basé sur ma journée d'aujourd'hui, créez un rapport structuré:

## Section 1: Summary (3 bullet points)
- [Accomplissement clé 1]
- [Accomplissement clé 2]
- [Accomplissement clé 3]

## Section 2: Tasks Completed
- [Task 1 avec résultat]
- [Task 2 avec résultat]
- [Task 3 avec résultat]

## Section 3: Blockers/Challenges
- [Blocker 1 + potential solution]
- [Blocker 2 + potential solution]

## Section 4: Tomorrow's Priorities
1. [Priority 1 — why]
2. [Priority 2 — why]
3. [Priority 3 — why]

## Section 5: Personal Notes
[Anything else worth noting]

---

Format en Markdown valide pour Obsidian.
Ajoute des tags pertinents.
Inclus un lien "Next day" pour continuité.
```

---

### 2️⃣ Note Cross-linking Prompt

**Usage :** Trouver connections entre notes existantes

```markdown
# Cross-Note Analysis

**Subject:** [Topic you want to understand deeply]
**Available notes in vault:** [List 3-5 relevant notes you have]

Analyze these notes and create a synthesis that:

1. **Identifies key concepts** from each note
2. **Shows connections** — how do they relate?
3. **Finds gaps** — what's missing?
4. **Suggests new angles** — what you haven't explored
5. **Recommends next steps** — what to research/create

Output format:
- Concept map (ASCII art or description)
- Connection matrix (shows relationships)
- Gaps analysis (what's missing)
- Recommended actions

This will become a note in my vault linking to all originals.
```

---

### 3️⃣ Weekly Planning Prompt

**Usage :** Planner sa semaine intelligemment

```markdown
# Weekly Planning

**Current priorities (from TODO_ACTIF):**
[List top 5-10 tasks]

**Available time:** [X hours/week]
**Energy distribution:** [When are you most productive]
**Blockers/dependencies:** [What might get in the way]

Create a week plan that:

1. **Distributes tasks** across days realistically
2. **Accounts for energy** — place hard tasks during peak hours
3. **Identifies dependencies** — what needs to be done first
4. **Adds buffer time** — for unexpected issues
5. **Includes review time** — 30 min daily + 1 hour weekly

---

Output format:
- **Monday:** [Task 1] — [Time estimate]
- **Tuesday:** [Task 1] — [Time estimate]
- etc.

Highlight: Which task would have biggest impact if completed?
```

---

---

## Content Creation

### 1️⃣ Article/Blog Prompt

**Usage :** Créer article professionnel from scratch

```markdown
# Content Creation — Article

**Topic:** [Your subject]
**Audience:** [Who reads this]
**Goal:** [What you want reader to do/learn]
**Format:** [Blog post / Tutorial / Guide / Case study]
**Length:** [approx words]

## Content Structure

Créez un article structured ainsi:

1. **Hook/Intro** — Grab attention in first paragraph
   - Why should reader care?
   - What problem does this solve?

2. **Background** — Context and definitions
   - What's the scenario?
   - Why does this matter now?

3. **Main Content** — 3-5 key points
   - Point 1: [Explanation + example]
   - Point 2: [Explanation + example]
   - Point 3: [Explanation + example]

4. **Practical Examples** — Show it working
   - Example 1: [Real-world scenario]
   - Example 2: [Real-world scenario]

5. **Call-to-Action** — What next?
   - What should reader do?
   - Resources to explore

---

Include: Subheadings, bold key terms, code blocks if applicable.
Optimize for: Clarity, scannability, value delivery.
Tone: [Professional / Casual / Educational / etc]
```

---

### 2️⃣ Case Study Prompt

**Usage :** Créer case study pour portfolio

```markdown
# Case Study Creation

**Project:** [Name]
**Client/Context:** [Who/why]
**Problem:** [What challenge were you solving]

---

## Structure

1. **The Challenge**
   - Situation: [Context before]
   - Problem: [Specific issue]
   - Impact: [Why it mattered]

2. **Your Solution**
   - Approach: [High level strategy]
   - Implementation: [How you did it]
   - Timeline: [How long]

3. **Results**
   - Metric 1: [Improvement with numbers]
   - Metric 2: [Improvement with numbers]
   - Metric 3: [Improvement with numbers]

4. **Key Learnings**
   - What worked: [Surprising wins]
   - What you'd do differently: [Honest reflection]
   - Takeaway for readers: [How they can apply]

---

Make it: Specific + Quantified + Credible + Relevant
```

---

---

## Code Generation

### 1️⃣ Claude API Integration Prompt

**Usage :** Générer code Python pour appels API Claude

```markdown
# Claude API Code Generation

**Use case:** [What you want to do with Claude]
**Input:** [What data goes in]
**Output:** [What you expect back]
**Language:** Python 3.10+

Generate complete, production-ready code that:

1. ✅ Uses latest Claude API (claude-3.5-sonnet or claude-opus-4)
2. ✅ Includes error handling (rate limits, timeouts)
3. ✅ Has configurable parameters (temperature, max_tokens)
4. ✅ Logs requests/responses for debugging
5. ✅ Follows Anthropic best practices

---

Include:
- Full imports
- Function definition with docstring
- Example usage
- Error handling
- Comments explaining key parts

Should be ready to copy-paste and run.
```

---

### 2️⃣ Automation Script Prompt

**Usage :** Générer script pour automation vault/workflows

```markdown
# Automation Script

**Goal:** [Automate what exactly]
**Trigger:** [When should this run]
**Input:** [What data needed]
**Output:** [What's created/updated]

Generate a [Python/Bash/Node] script that:

1. **Input handling** — Read from [files/API/stdin]
2. **Processing** — [Your specific logic]
3. **Output** — Write to [files/API/Obsidian]
4. **Error handling** — Graceful failures
5. **Logging** — Track what happened

---

Make it:
- Self-contained (minimal dependencies)
- Well-commented
- Easy to schedule (cron/Task Scheduler)
- Debuggable (logs, error messages)

Ready to run with: `python script.py` or similar.
```

---

---

## 🎯 Prompt Optimization Tips

### 1️⃣ Be specific
❌ "Help me with Python"
✅ "Generate Python function that takes [X] and returns [Y], handling [edge cases]"

### 2️⃣ Provide context
❌ "What should I price my service?"
✅ "I charge $X/h currently, market research shows..., my ICP is... — what pricing strategy fits?"

### 3️⃣ Request output format
❌ "Analyze this"
✅ "Analyze this and provide output as: [Heading] [Bullets] [Code blocks]"

### 4️⃣ Use constraints productively
```markdown
Constraint: Max 500 words
Constraint: Use only Python standard library
Constraint: Must be completable in 2 hours
```

### 5️⃣ Leverage examples
```markdown
Example format I want:
[Show example of desired output]
```

---

---

## 📚 Quick Prompt Selector

**Need:** → **Use this prompt**
- Revenue idea? → [[#Service Ideation Prompt]]
- Pricing help? → [[#Pricing Strategy Prompt]]
- CTF stuck? → [[#CTF Hint Prompt]]
- Code audit? → [[#Security Audit Prompt]]
- Daily report? → [[#Daily Report Automation Prompt]]
- Blog article? → [[#Article/Blog Prompt]]
- Python code? → [[#Claude API Integration Prompt]]
- Automation script? → [[#Automation Script Prompt]]

---

*Document created: 2026-02-14*
*Last updated: 2026-02-14*
*Version: 1.0*
