# HexStrike — Engagements

Ce dossier contient un dossier par engagement client.

## Format de Nommage

```
YYYY-MM — [NOM CLIENT] — [TYPE]/
```

Exemples :
- `2026-03 — Entreprise XYZ — Pentest Web/`
- `2026-04 — Journal ABC — OSINT/`
- `2026-05 — Programme HackerOne — Bug Bounty Tracker/`

## Contenu Minimum par Dossier d'Engagement

```
[Nom Engagement]/
├── Brief.md             ← Autorisation, scope, contacts
├── Notes Recon.md       ← Notes de reconnaissance
├── Vulnérabilités.md    ← Tracker des vulnérabilités trouvées
├── Rapport Final.md     ← Rapport livré au client
└── Lessons Learned.md  ← Ce que j'ai appris (pour THIRTY3)
```

## Checklist de Clôture d'Engagement

- [ ] Rapport final livré et confirmé reçu
- [ ] Données sensibles collectées supprimées (selon accord)
- [ ] Note de facturation envoyée
- [ ] Lessons Learned documentées
- [ ] Preuve ajoutée dans `THIRTY3/Preuves/` si notable
- [ ] Témoignage client demandé

## Statuts d'Engagement

- **Actif** — En cours
- **Livré** — Rapport envoyé, en attente de retour
- **Clôturé** — Engagement terminé et archivé
- **Bug Bounty** — Programme continu (pas de clôture)
