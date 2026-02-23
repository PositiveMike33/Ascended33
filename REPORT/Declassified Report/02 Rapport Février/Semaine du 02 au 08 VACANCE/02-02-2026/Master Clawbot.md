#02-02-2026 
La vidéo présente un guide complet (≈35 minutes) pour installer, configurer et utiliser OpenClaw/Clawdbot (ex‑Moltbot), un agent IA capable de piloter votre ordinateur, vos apps et des services externes de façon autonome. [youtube](https://www.youtube.com/watch?v=4evf5YqVzOM)

## Ce qu’est OpenClaw / Clawdbot

- Agent IA qui ne se limite pas aux réponses textuelles : il peut contrôler le navigateur, accéder aux fichiers locaux, envoyer des messages, gérer calendrier et emails, etc. [youtube](https://www.youtube.com/watch?v=4evf5YqVzOM)
- L’auteur insiste sur le fait qu’il s’agit d’un outil très puissant, mais complexe et avec des risques de sécurité élevés s’il est mal configuré. [youtube](https://www.youtube.com/watch?v=4evf5YqVzOM)

## Installation et interfaces

- Installation montrée sur Mac, Windows et sur un VPS, avec l’usage de warp.dev comme terminal assisté par IA et d’un wizard d’onboarding pour choisir modèles (OpenAI, Google Gemini, etc.) et canaux (WhatsApp, Telegram). [youtube](https://www.youtube.com/watch?v=4evf5YqVzOM)
- Utilisation via trois interfaces : interface web locale, TUI (terminal user interface) qui expose plus d’options (modèle, sessions, statut, etc.) et application de bureau macOS accessible depuis la barre de menus. [youtube](https://www.youtube.com/watch?v=4evf5YqVzOM)

## Connexions externes et automatisation

- Connexion à des messageries (WhatsApp, Telegram, Discord, Slack), avec un focus sur les limites de WhatsApp (reliage nécessaire après redémarrage) et la supériorité des canaux basés API pour un service 24/7. [youtube](https://www.youtube.com/watch?v=4evf5YqVzOM)
- Intégrations via « skills » : générateur de descriptions et de titres YouTube, intégration Google Workspace (Gmail, Calendar, Drive, Sheets), gestion de Kanban (Linear) via API/MCP, installation de skills depuis un hub ou manuellement dans le dossier skills. [youtube](https://www.youtube.com/watch?v=4evf5YqVzOM)

## Web, navigateur et planification

- Activation de la recherche web via Brave Search API et commande de configuration pour permettre à l’agent de faire de la recherche en ligne. [youtube](https://www.youtube.com/watch?v=4evf5YqVzOM)
- Installation d’une extension Chrome (mode développeur, dossier caché, etc.) pour que l’agent prenne le contrôle du navigateur et exécute des workflows complexes (ex. génération d’images Gemini directement dans le navigateur). [youtube](https://www.youtube.com/watch?v=4evf5YqVzOM)
- Mise en place de cron jobs récurrents (analyse YouTube hebdomadaire, rapports de ventes App Store, etc.) et de « heartbeats » qui vérifient périodiquement mails et calendrier et ne notifient que si quelque chose mérite attention. [youtube](https://www.youtube.com/watch?v=4evf5YqVzOM)

## Personnalisation et sécurité

- Personnalité et règles de l’agent définies dans soul.md (ton, rôle de « chief of staff », limites comme « ne jamais supprimer tous mes fichiers ») et comportements de surveillance définis dans heartbeat.md. [youtube](https://www.youtube.com/watch?v=4evf5YqVzOM)
- Section sécurité : détection de passerelles exposées, recommandations de ne pas faire tourner l’agent sur la machine principale, exécution d’un audit de sécurité, activation stricte de l’authentification gateway et durcissement des permissions de fichiers; suggestion d’utiliser un VPS ou une machine dédiée plutôt qu’un ordinateur personnel ou un environnement corporate. [youtube](https://www.youtube.com/watch?v=4evf5YqVzOM)

## Avis final du créateur

- Points négatifs : difficile à installer et à maintenir, gourmand en tokens, plus lent que certaines solutions maison, important risque de sécurité et nombreux edge cases. [youtube](https://www.youtube.com/watch?v=4evf5YqVzOM)
- Points positifs : plateforme unifiée très puissante, contrôle depuis le téléphone, énorme potentiel via les skills et l’écosystème, adaptée surtout à des utilisateurs intermédiaires qui maîtrisent déjà prompts, VPS et APIs, mais pas idéale pour débutants ni pour environnements d’entreprise sensibles. [youtube](https://www.youtube.com/watch?v=4evf5YqVzOM)