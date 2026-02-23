# 🧠 INTEGRATION MASTERCLASS — Skills + MCP + Prompts Ensemble

**Date:** 14-02-2026  
**Niveau:** Intermédiaire → Avancé  
**Durée:** ~20 min (theory) + 1h (build)  
**Lien:** [[1_SKILLS_MASTERCLASS]] | [[2_MCP_MASTERCLASS]] | [[3_PROMPTING_MASTERCLASS]]

---

## 🎯 OBJECTIF DE CE COURS

À la fin, tu pourras:
✅ Combiner les 3 piliers pour créer des workflows puissants  
✅ Automatiser ta stratégie revenue complète  
✅ Automatiser ton learning hacking complet  
✅ Créer des systèmes que tu utilises pendant des mois  

---

## 📚 PARTIE 1 — COMMENT ILS S'ARTICULENT

### Les 3 Piliers travaillent ENSEMBLE

```
SKILLS 
= Le QUOI & COMMENT (tes workflows)
  "Je veux analyser prospects rapidement"

MCP
= L'ACCÈS aux données (où sont tes données)
  "Lis dans mon Vault / ma DB / mon web"

PROMPTING
= La COMMUNICATION (parler parfaitement à Claude)
  "Structure ton prompt avec XML, exemples, rôle"

=================

RÉSULTAT = Système puissant et automatisé!
```

---

### Architecture générale

```
User Input
    ↓
Claude détecte quel SKILL utiliser
    ↓
Skill utilise MCP pour accéder aux données
    ↓
MCP lit données de ton Vault / web / DB
    ↓
Claude utilise PROMPTING technique pour traiter
    ↓
Output précis et actionnable
```

**Exemple concrète:**
```
User: "Qualifie les 50 prospects LinkedIn dans mon Vault"
    ↓
Claude: "Je vais utiliser skill 'revenue-prospect-analyzer'"
    ↓
Skill: "Utilise MCP filesystem pour lire SECURITY_AUDIT_LEADS.md"
    ↓
MCP: "Lit D:\Vault\Vault\🔐_SECURITY_AUDIT_PROJECT\SECURITY_AUDIT_LEADS.md"
    ↓
Claude: "Utilise XML structure + chain-of-thought pour scorer chacun"
    ↓
Output: "Top 10 prospects qualifiés, scorés 8-10, prêts pour outreach"
```

---

## 💰 PARTIE 2 — WORKFLOW REVENUE COMPLET

### Scénario: Générer $15K en 3 mois

Tu veux automatiser TOUT le processus de revenue:
1. **Lead generation** → Trouver prospects
2. **Qualification** → Scorer les prospects
3. **Outreach** → Écrire messages personnalisés
4. **Follow-up** → Relancer sans réponse
5. **Closing** → Créer proposals

---

### Configuration SKILLS pour Revenue

**Skill 1: "revenue-prospect-analyzer"**
```
Quand: Tu donnes un profil LinkedIn
Fait: Score le prospect 1-10
MCP utilisé: filesystem (lit tes critères dans Vault)
Prompting: XML structure + scoring rubric
```

**Skill 2: "email-prospection-optimizer"**
```
Quand: Tu veux écrire un email de prospection
Fait: Crée un email personnalisé haute-conversion
MCP utilisé: fetch (cherche social proof récente du prospect)
Prompting: Rôle + contexte + contraintes
```

**Skill 3: "proposal-generator"**
```
Quand: Un prospect dit "raconte-moi plus"
Fait: Génère une proposal professionnelle
MCP utilisé: filesystem (lit service details) + fetch (prix comparatifs)
Prompting: Chain-of-thought (structure logique de vente)
```

---

### Setup MCP pour Revenue

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-filesystem", "D:\\Vault\\Vault"]
    },
    "fetch": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-fetch"]
    }
  }
}
```

Claude peut maintenant:
- Lire tes fichiers Vault (SECURITY_AUDIT_LEADS.md, SERVICE.md, etc.)
- Scraper web pour social proof
- Créer content basé sur données réelles

---

### Workflow Complet — STEP BY STEP

#### STEP 1: Qualifier les prospects

**À Claude:**
```xml
<skill>revenue-prospect-analyzer</skill>

<task>
Lis SECURITY_AUDIT_LEADS.md et qualifie tous les prospects 1-10.
Utilise ces critères:
- Poste: VP/CTO = 10, Manager = 5, HR = 1
- Taille: 20-75 = 10, 10-20 = 7, 75-150 = 7, >150 = 1
- Industrie: Tech/SaaS/Fintech = 10, Autres = 3
- Location: Montréal = 10, Région = 8, Ailleurs = 1

Donne score final + raison en 1-2 lignes.
</task>

<output>
Crée une note PROSPECTS_QUALIFIED.md avec:
1. Top 10 (score 8-10) → URGENT (cette semaine)
2. Medium 10 (score 5-7) → Soon (2e semaine)
3. Low 30 (score 1-4) → Follow-up (si besoin)
```

**Claude output:**
```
✅ PROSPECTS_QUALIFIED.md créée avec:

TOP 10 (This Week):
1. Jean-Paul Leblanc (9/10) — VP Engineering, SaaS, 40 emp, MTL
2. Marie Côté (8/10) — CTO, Fintech, 35 emp, MTL
3. Claude Marchand (8/10) — VP IT, SaaS, 50 emp, MTL
...
```

---

#### STEP 2: Écrire emails personnalisés

**À Claude:**
```xml
<skill>email-prospection-optimizer</skill>

<context>
Je vais écrire 10 emails cette semaine pour mes top 10 prospects.
Chaque email doit être personnalisé (pas generic).
Objectif: 3 replies min qui disent "oui" pour call
</context>

<task>
Pour chaque prospect du TOP 10 dans PROSPECTS_QUALIFIED.md:
1. Lis leur profil LinkedIn (cherche info unique)
2. Crée un email personnalisé de 100-150 mots
3. Include 1 specific insight sur leur company/industry
4. End avec clear CTA: "30-min call for quick security assessment?"
</task>

<output>
Crée note: EMAILS_PERSONALIZED.md avec 10 emails prêts à copier/coller
```

**Claude output:**
```
✅ EMAILS_PERSONALIZED.md créée

Email 1 (To: Jean-Paul Leblanc):
Subject: Quick win for TechStartup MTL security

Hi Jean-Paul,

I was checking out TechStartup's recent Series B funding (congrats!).
With that growth, security audit is usually one of the next steps...
[Rest of personalized email]

Email 2 (To: Marie Côté):
[Different email, personalized for her fintech context]
```

---

#### STEP 3: Track responses

**À Claude:**
```xml
<task>
Crée une tracking sheet: TRACKING_RESPONSES.md

Columns:
- Prospect Name
- Email Sent (date)
- Status (sent/opened/replied/declined/meeting booked)
- Notes
- Next Action
- Date for follow-up

Laisse à jour chaque jour:
1. Mark emails as "sent"
2. Track replies
3. Suggest follow-up timings
</task>
```

**Claude output:**
```
✅ TRACKING_RESPONSES.md créée et mise à jour daily

| Prospect | Sent | Status | Follow-up |
|----------|------|--------|-----------|
| Jean-Paul | Feb 14 | Opened | Feb 17 |
| Marie | Feb 14 | Sent | Feb 17 |
| Claude | Feb 15 | Replied! | CALL ASAP |
```

---

#### STEP 4: Create proposals

**À Claude:**
```xml
<skill>proposal-generator</skill>

<task>
Un prospect demande: "Tell me more about your service"

Génère une proposal professionnelle qui inclut:
1. Executive summary (problème + solution)
2. Scope détaillé (ce qu'on audite)
3. Timeline (2 semaines)
4. Pricing: $5,500 fixed (avec 3 options de paiement)
5. Next steps + CTA

Format: Prêt à envoyer par email ou imprimer
</task>
```

**Claude output:**
```
✅ PROPOSAL_[CompanyName].md créée (prêt à envoyer)

Subject: Security Audit Proposal — TechStartup MTL
Date: Feb 15, 2026
Prepared for: Jean-Paul Leblanc, VP Engineering

EXECUTIVE SUMMARY
Your platform processes customer payment data...
[Full proposal]
```

---

## 🔐 PARTIE 3 — WORKFLOW HACKING COMPLET

### Scénario: Master OWASP Top 10 en 8 semaines

Tu veux automatiser ton learning hacking:
1. **Learn concept** → Understand vulnerability
2. **Practice CTF** → Solve hands-on challenge
3. **Document** → Create walkthrough
4. **Defend** → Know how to fix/prevent
5. **Track progress** → See your level grow

---

### Configuration SKILLS pour Hacking

**Skill 1: "owasp-concept-explainer"**
```
Quand: Tu veux apprendre un concept OWASP
Fait: Crée une note éducative complète
MCP utilisé: fetch (cherche ressources PortSwigger/WebGoat)
Prompting: Explique simply, donne exemples, labs
```

**Skill 2: "ctf-walkthrough-documenter"**
```
Quand: Tu finis un CTF
Fait: Documente le walkthrough professionnel
MCP utilisé: filesystem (lis ton KALI labs output)
Prompting: Chain-of-thought (explique chaque étape)
```

**Skill 3: "defense-strategy-builder"**
```
Quand: Après avoir appris une vulnérabilité
Fait: Crée un guide "comment défendre contre ça"
MCP utilisé: fetch (cherche best practices OWASP)
Prompting: Rôle = security architect
```

---

### Setup MCP pour Hacking

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-filesystem", "D:\\Vault\\Vault"]
    },
    "fetch": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-fetch"]
    },
    "git": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-git", "D:\\Vault\\Vault"]
    }
  }
}
```

Claude peut maintenant:
- Lire tes KALI lab outputs
- Scraper PortSwigger, WebGoat, TryHackMe
- Créer/commit walkthroughs dans ton Vault

---

### Workflow Complet — OWASP Learning Path

#### WEEK 1: SQL Injection

**DAY 1: Learn**
```xml
<skill>owasp-concept-explainer</skill>

<task>
Crée une note: OWASP_A03_SQL_INJECTION.md

Include:
1. What is SQL injection (simple explanation)
2. Types (UNION-based, Boolean-based, Time-based, Stacked)
3. Real-world examples
4. Why it's dangerous
5. Live labs link (PortSwigger, TryHackMe)
</task>
```

**DAY 2-3: Practice**
```
Tu résous les PortSwigger SQL Injection labs (10 labs)
```

**DAY 4: Document**
```xml
<skill>ctf-walkthrough-documenter</skill>

<task>
Tu as fini 3 labs. Documente chacun:
- Lab name + difficulty
- Walkthrough complet avec payloads
- Screenshots/outputs
- What you learned
- How to defend
</task>
```

**DAY 5: Create Defense Guide**
```xml
<skill>defense-strategy-builder</skill>

<task>
Crée: DEFENSE_SQL_INJECTION.md

Tu es security architect.
Enseigne comment DÉFENDRE une application contre SQL injection:
1. Code-level (parameterized queries)
2. Database-level (least privilege)
3. Application-level (WAF rules)
4. Detection (logging, monitoring)
</task>
```

---

#### WEEK 2-8: Repeat pour each OWASP Top 10

```
Week 2: A01 — Authentication
Week 3: A02 — Cryptography
Week 4: A04 — XML External Entities
Week 5: A05 — Broken Access Control
Week 6: A06 — CSRF
Week 7: A07 — Command Injection
Week 8: A08 — Server-Side Template Injection
```

**Résultat:**
- 8 notes éducatives complètes
- 24+ CTF walkthroughs documentés
- 8 defense guides
- **Prêt(e) pour CEH exam!** 🎓

---

## 🎬 EXEMPLE LIVE — Revenue Workflow

### Que tu fasses maintenant:

```
1. Tu dis à Claude: "Qualifie mes prospects"
   ↓
2. Claude utilise skill "revenue-prospect-analyzer"
   ↓
3. Skill utilise MCP pour lire SECURITY_AUDIT_LEADS.md
   ↓
4. Claude applique prompting XML pour scorer
   ↓
5. Output: 50 prospects qualifiés, top 10 identifiés
   ↓
6. Tu dis: "Crée les emails"
   ↓
7. Claude utilise skill "email-optimizer"
   ↓
8. Skill utilise MCP/fetch pour personnaliser chacun
   ↓
9. Output: 10 emails prêts à copier/coller
   ↓
10. Tu envoies 10 emails
   ↓
11. Résultat potentiel: 3-5 replies = $15-25K revenue 🎯
```

---

## ✅ CHECKLIST — Tu es prêt(e)!

- [ ] J'ai créé mon 1er skill (revenue-prospect-analyzer)
- [ ] J'ai installé MCP (filesystem + fetch au minimum)
- [ ] J'ai testé MCP (lis 1 fichier du Vault)
- [ ] J'ai reécrit 2 prompts avec XML structure
- [ ] Je comprends comment Skills + MCP + Prompts travaillent ensemble
- [ ] Je peux expliquer le workflow à quelqu'un d'autre

---

## 🚀 TES PROCHAINES ÉTAPES

### Immédiates:
1. **Finish les 3 masterclass** (tu y es presque!)
2. **Create skill "revenue-prospect-analyzer"** (30 min)
3. **Install MCP servers** (20 min)
4. **Test: Qualify prospects** (10 min)

### Court terme (cette semaine):
- Send 5-7 emails à top prospects
- Document 1 CTF walkthrough
- Create 1 defense guide

### Moyen terme (ce mois):
- 10 qualified prospects analyzed
- 7+ emails sent
- 2-3 discovery calls booked
- 3 CTF walkthroughs documented
- First revenue earned! 💰

---

## 🎯 BONUS — Combiner TOUT ENSEMBLE

### The Ultimate Prompt (use this template):

```xml
<!-- This prompt combines all 3 pillars -->

<skill>revenue-prospect-analyzer</skill>

<role>
Tu es un expert en qualification prospects B2B SaaS.
Tu as aidé 50+ startups à qualifier leurs leads pour conversion max.
Tu es brutal mais juste dans ton évaluation.
</role>

<context>
Je lance une offre security audit ($5.5K).
J'ai 100 prospects LinkedIn à qualifier rapidement.
Je veux que tu scores chaque prospect 1-10 en 2 min MAX.
</context>

<task>
1. Lis tous les prospects dans mon Vault (utilise MCP filesystem)
2. Score chacun 1-10 basé sur critères (poste, taille, industrie, location)
3. Create PROSPECTS_QUALIFIED.md avec top 10
4. Add "Next Action" pour chaque top prospect
</task>

<constraints>
Max 2 min par prospect.
Score doit être justifié en 1-2 lignes.
Format: Ready for outreach.
Ton: Direct, no BS.
</constraints>

<output>
PROSPECTS_QUALIFIED.md avec:
- Top 10 (score 8-10) → This week priority
- Medium 10 (score 5-7) → Next week
- Rest → Follow-up pool
</output>
```

**This single prompt:**
- Uses skill framework (structured workflow)
- Uses MCP (accesses your vault data)
- Uses prompting techniques (XML, role, context, constraints)
- **= Automation puissance 1000x!**

---

## 🎬 C'EST TON TOUR!

Tu as maintenant:
✅ 3 masterclass complètes (Skills + MCP + Prompting)
✅ 2 workflows complets (Revenue + Hacking)
✅ 6 templates de skills prêts à utiliser
✅ Setup guide pour MCP
✅ Les 6 techniques de prompting avancé

**Prochaine étape:** Retourne à [[README_PROJECTS]] et lance tes projets! 🚀

---

**Tags:** #integration #automation #skills #mcp #prompting #workflow #14-02-2026
