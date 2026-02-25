---
allowed-tools: Bash(gh issue view:*), Bash(gh search:*), Bash(gh issue list:*), Bash(gh pr comment:*), Bash(gh pr diff:*), Bash(gh pr view:*), Bash(gh pr list:*)
description: Code review a pull request
disable-model-invocation: false
---

Fournir une revue de code pour la demande d'extraction donnée.

Pour ce faire, suivez les étapes suivantes avec précision :

1. Utilisez un agent Haiku pour vérifier si la demande (a) est fermée, (b) est un brouillon, (c) n'a pas besoin d'une revue de code (par exemple parce que c'est une demande automatisée, ou parce qu'elle est très simple et manifestement ok), ou (d) a déjà fait l'objet d'une revue de code de votre part plus tôt. Si c'est le cas, ne continuez pas.
2. Utilisez un autre agent Haiku pour vous donner une liste de chemins d'accès (mais pas le contenu) à tous les fichiers CLAUDE.md pertinents de la base de code : le fichier CLAUDE.md racine (s'il existe), ainsi que tous les fichiers CLAUDE.md dans les répertoires dont les fichiers ont été modifiés par la demande d'extraction.
3. Utilisez un agent Haiku pour voir la demande d'extraction, et demandez à l'agent de renvoyer un résumé du changement.
4. Ensuite, lancez 5 agents Sonnet en parallèle pour faire une revue de code indépendante de la modification. Les agents devraient faire ce qui suit, puis renvoyer une liste de problèmes et la raison pour laquelle chaque problème a été signalé (par exemple, adhésion à CLAUDE.md, bogue, contexte historique de git, etc :)
   a. Agent #1 : Auditer les changements pour s'assurer qu'ils sont conformes au CLAUDE.md. Notez que CLAUDE.md est un guide pour Claude lorsqu'il écrit du code, donc toutes les instructions ne seront pas applicables lors de la revue de code.
   b. Agent #2 : Lisez les changements de fichiers dans la demande d'extraction, puis faites un examen superficiel pour les bogues évidents. Évitez de lire un contexte supplémentaire au-delà des changements, en vous concentrant uniquement sur les changements eux-mêmes. Concentrez-vous sur les bogues importants et évitez les petits problèmes et les détails. Ignorez les faux positifs probables.
   c. Agent #3 : Lisez le blâme git et l'historique du code modifié, afin d'identifier les bogues à la lumière de ce contexte historique.
   d. Agent #4 : Lisez les requêtes précédentes qui ont touché ces fichiers, et vérifiez s'il y a des commentaires sur ces requêtes qui peuvent aussi s'appliquer à la requête actuelle.
   e. Agent #5 : Lisez les commentaires de code dans les fichiers modifiés, et assurez-vous que les changements dans la demande d'extraction sont conformes à tout conseil dans les commentaires.
5. Pour chaque problème trouvé en #4, lancez un agent Haiku parallèle qui prend le PR, la description du problème, et la liste des fichiers CLAUDE.md (de l'étape 2), et renvoie un score pour indiquer le niveau de confiance de l'agent pour savoir si le problème est réel ou faussement positif. Pour ce faire, l'agent doit noter chaque problème sur une échelle de 0 à 100, en indiquant son niveau de confiance. Pour les problèmes signalés en raison des instructions du fichier CLAUDE.md, l'agent doit vérifier que le fichier CLAUDE.md mentionne bien le problème en question. L'échelle est la suivante (donnez cette rubrique à l'agent mot pour mot) :
   a. 0 : Pas du tout confiant. Il s'agit d'un faux positif qui ne résiste pas à un examen approfondi ou d'un problème préexistant.
   b. 25 : Assez confiant. Il peut s'agir d'un problème réel, mais aussi d'un faux positif. L'agent n'a pas été en mesure de vérifier qu'il s'agit d'un problème réel. Si le problème est d'ordre stylistique, il n'a pas été explicitement mentionné dans le CLAUDE.md correspondant.
   c. 50 : Moyennement confiant. L'agent a pu vérifier qu'il s'agit d'un problème réel, mais il peut s'agir d'un point de détail ou d'une situation peu fréquente dans la pratique. Par rapport au reste du PR, ce n'est pas très important.
   d. 75 : Très confiant. L'agent a revérifié la question et a vérifié qu'il est très probable qu'il s'agisse d'un problème réel qui se posera dans la pratique. L'approche existante dans le PR est insuffisante. Le problème est très important et aura un impact direct sur la fonctionnalité du code, ou c'est un problème qui est directement mentionné dans le CLAUDE.md pertinent.
   e. 100 : Absolument certain. L'agent a revérifié le problème et a confirmé qu'il s'agit bien d'un problème réel, qui se produira fréquemment dans la pratique. Les éléments de preuve le confirment directement.
6. Filtrez tous les problèmes dont le score est inférieur à 80. Si aucun problème ne répond à ce critère, ne procédez pas.
7. Utilisez un agent Haiku pour répéter la vérification de l'éligibilité à partir de #1, pour s'assurer que la requête est toujours éligible pour une revue de code.
8. Enfin, utilisez la commande gh bash pour commenter la demande d'extraction avec le résultat. Lorsque vous écrivez votre commentaire, gardez à l'esprit de :
   a. rester bref
   b. Evitez les emojis
   c. Lier et citer le code, les fichiers et les URL pertinents

Exemples de faux positifs, pour les étapes 4 et 5 :

- Problèmes préexistants
- Quelque chose qui ressemble à un bogue mais qui n'en est pas vraiment un
- Pointillés pédants qu'un ingénieur expérimenté ne signalerait pas.
- Des problèmes qu'un linter, un vérificateur de type ou un compilateur pourrait détecter (par exemple, des importations manquantes ou incorrectes, des erreurs de type, des tests cassés, des problèmes de formatage, des problèmes de style pédants comme les nouvelles lignes). Il n'est pas nécessaire d'exécuter ces étapes de compilation vous-même - on peut supposer qu'elles seront exécutées séparément dans le cadre de l'IC.
- Les problèmes généraux de qualité du code (par exemple, le manque de couverture des tests, les problèmes généraux de sécurité, une mauvaise documentation), à moins qu'ils ne soient explicitement requis dans CLAUDE.md.
- Les problèmes qui sont mentionnés dans CLAUDE.md, mais qui sont explicitement passés sous silence dans le code (par exemple, en raison d'un commentaire lint ignore).
- Les changements de fonctionnalité qui sont probablement intentionnels ou qui sont directement liés à un changement plus large.
- Problèmes réels, mais sur des lignes que l'utilisateur n'a pas modifiées dans sa demande d'extraction.

Notes :

- Ne vérifiez pas le signal de construction ou n'essayez pas de construire ou de vérifier le type de l'application. Ces opérations seront exécutées séparément, et ne sont pas pertinentes pour votre revue de code.
- Utilisez `gh` pour interagir avec Github (par exemple pour récupérer une pull request, ou pour créer des commentaires en ligne), plutôt que web fetch.
- Faites d'abord une liste de choses à faire
- Vous devez citer et lier chaque bogue (par exemple, si vous faites référence à un CLAUDE.md, vous devez le lier).
- Pour votre commentaire final, suivez précisément le format suivant (en supposant pour cet exemple que vous avez trouvé 3 problèmes) :

---

### Revue de code

Nous avons trouvé 3 problèmes :

1. <brève description du bogue> (CLAUDE.md dit "<...>")

<lien vers le fichier et la ligne avec le sha1 complet + la plage de lignes pour le contexte, notez que vous DEVEZ fournir le sha complet et ne pas utiliser bash ici, par exemple https://github.com/anthropics/claude-code/blob/1d54823877c4de72b2316a64032a54afc404e619/README.md#L13-L17>

2. <brève description du bogue> (some/other/CLAUDE.md dit "<...>")

<lien vers le fichier et la ligne avec le sha1 complet + la plage de lignes pour le contexte>

3. <brève description du bogue> (bogue dû à <fichier et extrait de code>)

<lien vers le fichier et la ligne avec sha1 complet + intervalle de lignes pour le contexte>

Généré avec [Code Claude](https://claude.ai/code)

<sub>- Si cette revue de code vous a été utile, réagissez avec 👍. Sinon, réagissez avec 👎.</sub>

---

- Ou, si vous n'avez trouvé aucun problème :

---

### Revue de code

Aucun problème n'a été trouvé. Vérification des bogues et de la conformité du fichier CLAUDE.md.

Généré avec [Code Claude](https://claude.ai/code)

- Lorsque vous créez un lien vers du code, suivez précisément le format suivant, sinon l'aperçu Markdown ne s'affichera pas correctement : https://github.com/anthropics/claude-cli-internal/blob/c21d3c10bc8e898b7ac1a2d745bdc9bc4e423afe/package.json#L10-L15
  - Requiert le sha complet de git
  - Vous devez fournir le sha complet. Des commandes comme `https://github.com/owner/repo/blob/$(git rev-parse HEAD)/foo/bar` ne fonctionneront pas, puisque votre commentaire sera directement rendu en Markdown.
  - Le nom du repo doit correspondre au repo que vous révisez.
  - Le signe # après le nom du fichier
  - Le format de l'intervalle de lignes est L[start]-L[end].
  - Fournissez au moins une ligne de contexte avant et après, centrée sur la ligne que vous commentez (par exemple, si vous commentez les lignes 5-6, vous devez faire un lien vers `L4-7`).