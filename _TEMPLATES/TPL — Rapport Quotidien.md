---
date: <% tp.date.now("YYYY-MM-DD") %>
semaine: <% tp.date.now("WW") %>
jour: <% tp.date.now("dddd", 0, "fr") %>
type: rapport-quotidien
humeur:
energie:
focus:
freelance_revenu_jour: 0
tags: [quotidien, rapport]
---

# 📋 Rapport — <% tp.date.now("DD MMMM YYYY", 0, "fr") %>

> *Semaine <% tp.date.now("WW") %> — <% tp.date.now("dddd D MMMM", 0, "fr") %>*

---

## 🎯 Priorités du jour (3 max)

- [ ] **P1 —**
- [ ] **P2 —**
- [ ] **P3 —**

---

## ✅ Accompli aujourd'hui

-

---

## 🧠 Apprentissages & insights

-

---

## 💰 Finance (si applicable)

| Poste | Montant | Type |
|-------|---------|------|
| | | dépense |
| | | revenu |

**Revenu freelance du jour : $**

---

## 🔐 Hacking / Sécurité

- **Session :** aucune / CTF / pentest / OSINT
- **Concept étudié :**
- **Progrès OSCP :**

---

## 🤖 IA & Automation

- **Workflow testé :**
- **Claude interactions :**

---

## 🔗 Notes créées aujourd'hui

- [[]]

---

## ⚡ Scores de la journée

| Dimension | Score /10 |
|-----------|-----------|
| Énergie matin | |
| Énergie soir | |
| Focus | |
| Productivité | |
| **MOYENNE** | |

---

## 🔄 Priorités pour demain

- [ ]
- [ ]
- [ ]

---

## 💬 Note libre

>

---

```dataview
TABLE energie AS "Énergie", focus AS "Focus", freelance_revenu_jour AS "$ Jour"
FROM "REPORT/Declassified Report"
WHERE type = "rapport-quotidien" AND date >= date(today) - dur(7 days)
SORT date DESC
LIMIT 7
```

---
*Rapport généré le <% tp.date.now("YYYY-MM-DD [à] HH:mm") %> — Semaine <% tp.date.now("WW") %>*
