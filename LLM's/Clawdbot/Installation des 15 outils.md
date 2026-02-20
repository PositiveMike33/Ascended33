Voici 15 outils/skills cités dans la vidéo, sous forme de liste compacte.
### Outils
1. VPS Hostinger (instance OpenClaw préconfigurée) [youtube](https://www.youtube.com/watch?v=VPauGdSTULg&t=1s)
2. Claude (LLM principal pour OpenClaw) [youtube](https://www.youtube.com/watch?v=VPauGdSTULg&t=1s)
3. Perplexity (search web skill) [youtube](https://www.youtube.com/watch?v=VPauGdSTULg&t=1s)
4. TranscriptAPI (transcription/synthèse YouTube) [youtube](https://www.youtube.com/watch?v=VPauGdSTULg&t=1s)
5. Whisper local (speech-to-text offline sur le VPS) [youtube](https://www.youtube.com/watch?v=VPauGdSTULg&t=1s)
6. VirusTotal (scan de sécurité intégré pour les skills) [youtube](https://www.youtube.com/watch?v=VPauGdSTULg&t=1s)
7. Google Analytics 4 skill (analyse trafic, SEO, indexation) [youtube](https://www.youtube.com/watch?v=VPauGdSTULg&t=1s)
8. Exa (recherche neuronale code/docs/papers) [youtube](https://www.youtube.com/watch?v=VPauGdSTULg&t=1s)
9. CloudHub search skill (recherche de nouveaux skills dans CloudHub) [youtube](https://www.youtube.com/watch?v=VPauGdSTULg&t=1s)
10. Home Assistant skill (pilotage domotique) [youtube](https://www.youtube.com/watch?v=VPauGdSTULg&t=1s)
11. Self‑improving agent / learning logger [youtube](https://www.youtube.com/watch?v=VPauGdSTULg&t=1s)
12. ElevenLabs skill (TTS, voice agents) [youtube](https://www.youtube.com/watch?v=VPauGdSTULg&t=1s)
13. Financial Market Analyst skill (marchés/finance, classé suspect) [youtube](https://www.youtube.com/watch?v=VPauGdSTULg&t=1s)
14. Stock Analysis skill (analyse actions/crypto, classé suspect) [youtube](https://www.youtube.com/watch?v=VPauGdSTULg&t=1s)
15. ClawDBot / documentation skill + n8n workflow skill (gestion docs et automatisations) [youtube](https://www.youtube.com/watch?v=VPauGdSTULg&t=1s)
# Précautions
- Ne **jamais** installer OpenClaw/OpenCloud en local : toujours sur un VPS isolé (Hostinger recommandé), sinon risque de fuite de fichiers, mots de passe, cartes, etc. [youtube](https://www.youtube.com/watch?v=VPauGdSTULg&t=1s)

- Utiliser l’instance Hostinger préconfigurée (2 vCPU, 8 Go RAM, OpenClaw déjà installé) pour éviter le terminal et sécuriser le déploiement. [youtube](https://www.youtube.com/watch?v=VPauGdSTULg&t=1s)

- Protéger absolument le Gateway Token OpenClaw (équivalent mot de passe root) et toutes les clés API (Claude, Perplexity, Exa, n8n, TranscriptAPI, N8N) dans un endroit privé. [youtube](https://www.youtube.com/watch?v=VPauGdSTULg&t=1s)

- Claude est privilégié comme LLM principal pour OpenClaw, jugé bien plus efficace que les modèles GPT 5.2 pour le web/data scraping. [youtube](https://www.youtube.com/watch?v=VPauGdSTULg&t=1s)

- ClawHub = marketplace d’extensions/skills :  
  - But : ajouter des compétences spécialisées (YouTube, Excel, web, doc, GA4, etc.) pour que l’agent exécute des tâches complexes sur simple prompt. [youtube](https://www.youtube.com/watch?v=VPauGdSTULg&t=1s)
  - Danger : n’importe qui publie des skills → il faut filtrer et ne jamais installer à l’aveugle. [youtube](https://www.youtube.com/watch?v=VPauGdSTULg&t=1s)

- Vérification sécurité des skills via VirusTotal intégré :  
  - Vert = clean → installable.  
  - Orange “suspect” = connexion à des services/ports externes, risque de futures injections → à éviter sauf audit manuel.  
  - Rouge = code Python malveillant (exfiltration de données, mots de passe) → ne jamais installer. [youtube](https://www.youtube.com/watch?v=VPauGdSTULg&t=1s)

- Skills YouTube/transcription :  
  - Premier skill YouTube bloqué par l’auth YouTube (captcha, login) → évité. [youtube](https://www.youtube.com/watch?v=VPauGdSTULg&t=1s)
  - Switch vers TranscriptAPI (compte + API, ~100 crédits gratuits) pour récupérer transcription + résumé de vidéos YouTube, piloté par OpenClaw. [youtube](https://www.youtube.com/watch?v=VPauGdSTULg&t=1s)

- Perplexity skill :  
  - Installé comme moteur de recherche web interne d’OpenClaw.  
  - Nécessite une API pay-as-you-go (1–2 $ suffisent pour des centaines de requêtes).  
  - Utilisé pour toute recherche profonde (VPS, sécurité, meilleures pratiques), avec réponses + sources. [youtube](https://www.youtube.com/watch?v=VPauGdSTULg&t=1s)

- Whisper local (OpenAI speech) :  
  - Télécharge ~1 Go de modèle sur le VPS pour transcription audio en **local** (MP3/WAV/M4A) sans coût API OpenAI, beaucoup plus rapide.  
  - Idéal pour usage intensif avec Telegram/WhatsApp (voice → texte). [youtube](https://www.youtube.com/watch?v=VPauGdSTULg&t=1s)

- Google Analytics 4 skill :  
  - L’agent lit GA4 (property id, client email, private key, domaine) et génère rapports, suivi en temps réel, alertes SEO/indexation automatiquement. [youtube](https://www.youtube.com/watch?v=VPauGdSTULg&t=1s)

- Exa skill (code/doc search) :  
  - Sert à la recherche neuronale dans documentation, scientific papers, code, et à générer/tenir la doc de projets créés par l’IA.  
  - Fortement recommandé pour devs; API Exa gratuite avec quelques crédits. [youtube](https://www.youtube.com/watch?v=VPauGdSTULg&t=1s)

- Skill “CloudHub search” :  
  - Permet à l’agent de parcourir CloudHub pour trouver de nouveaux skills, mais est signalé “à risque” car installation globale de packages non vérifiés.  
  - Ne pas laisser installer d’autres skills automatiquement via ce skill; toujours vérifier manuellement. [youtube](https://www.youtube.com/watch?v=VPauGdSTULg&t=1s)

- Home Assistant skill :  
  - Connecte OpenClaw à votre domotique (lumières, thermostat, alarme, etc.) via token Home Assistant pour pilotage voix/texte. [youtube](https://www.youtube.com/watch?v=VPauGdSTULg&t=1s)

- Self-improving agent :  
  - Skill critique : loggue toutes les erreurs, demandes de nouvelles fonctions, corrections, etc., pour qu’OpenClaw apprenne de ses échecs et améliore ses stratégies.  
  - Stocke erreurs, learnings, feature requests, cas récurrents avec horodatage. [youtube](https://www.youtube.com/watch?v=VPauGdSTULg&t=1s)

- ElevenLabs skill :  
  - Pilotage d’ElevenLabs (TTS + voice agents) via OpenClaw, permet agents vocaux (réponse en voix custom, appels, WhatsApp, etc.). [youtube](https://www.youtube.com/watch?v=VPauGdSTULg&t=1s)

- Skills finance/crypto (Financial Market Analyst, Stock Analysis) :  
  - Très puissants mais classés “suspects”.  
  - Utilisent des services obscurs (par ex. bored.pub, Firebase externe) et ports non transparents → risque de fuite d’API et données; recommandation : **ne pas installer**. [youtube](https://www.youtube.com/watch?v=VPauGdSTULg&t=1s)

- ClawDBot / documentation skill :  
  - Agent dédié documentation, capable de crawler, analyser, résumer, suivre versions, générer rapports structurés sur docs/sites. [youtube](https://www.youtube.com/watch?v=VPauGdSTULg&t=1s)

- n8n workflow skill :  
  - L’agent peut lister, créer, modifier, activer/désactiver, déboguer des workflows n8n via API (instance + API key).  
  - Il génère un JSON de workflow prêt à être importé et peut piloter une grosse stack d’automatisations. [youtube](https://www.youtube.com/watch?v=VPauGdSTULg&t=1s)

- Architecture globale recommandée :  
  - VPS Hostinger isolé + OpenClaw préinstallé.  
  - LLM principal Claude + Perplexity pour recherche.  
  - Whisper local, TranscriptAPI, Exa, GA4, n8n, ElevenLabs, ClawDBot, self-improving agent.  
  - Filtrage systématique des skills via VirusTotal et bannissement des skills suspects/malveillants. [youtube](https://www.youtube.com/watch?v=VPauGdSTULg&t=1s)