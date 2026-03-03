# La méthodologie du chasseur de bogues : De la reconnaissance à l'analyse d'application

Dans l'univers de la chasse aux bogues, les vulnérabilités complexes comme les exécutions de code à distance (RCE) ou les falsifications de requêtes côté serveur (SSRF) captivent l'imagination. Pourtant, les récompenses les plus spectaculaires ne découlent pas toujours des exploits les plus techniques. Comme l'a révélé le chasseur de bogues Teflon dans une vidéo de NahamSec, une prime de 70 000 $ peut provenir d'une observation minutieuse et d'une compréhension profonde de la logique d'une application. C'est précisément cette acuité, développée lors de la phase de reconnaissance, qui sépare les amateurs des professionnels. Trop de chercheurs se lancent tête baissée, armés de listes de commandes, sans prendre le temps de cartographier leur cible. Cet article vous guidera à travers une méthodologie structurée pour analyser méthodiquement les applications, transformant le chaos initial d'une nouvelle cible en une stratégie de test ciblée et efficace.

--------------------------------------------------------------------------------

## 1. L'état d'esprit du chasseur : Surmonter les barrières mentales

Avant même de lancer le moindre outil, la première bataille du chasseur de bogues se livre dans son propre esprit. Comme l'explique l'expert en sécurité Jason Haddix, les outils les plus sophistiqués sont inutiles si des barrières mentales nous empêchent de nous attaquer sérieusement à une cible. Reconnaître et déconstruire ces obstacles est la première étape vers le succès. Pour ceux qui débutent, il est également essentiel de construire une base solide. Des textes fondamentaux comme le **Web Application Hacker's Handbook 2**, souvent considéré comme la « bible » du piratage d'applications web, et des ouvrages plus récents comme **Real-World Bug Hunting** sont des lectures indispensables pour forger cet état d'esprit.

### **1.1. Les quatre obstacles courants**

Jason Haddix a identifié quatre obstacles psychologiques fréquents qui peuvent paralyser un chercheur. Chacun repose sur une fausse prémisse qui peut être contrée par une logique simple : la taille et la complexité d'une application génèrent inévitablement plus de bogues.

- **La réputation du client** Des entreprises comme Tesla emploient certains des ingénieurs en sécurité les plus brillants au monde. Il est facile de se dire : « Je ne trouverai jamais rien qu'ils n'aient déjà vu ». C'est une erreur de logique. Plus l'empreinte numérique d'une entreprise est vaste et complexe, plus les opportunités de bogues augmentent.
- **Les tests antérieurs** Des programmes comme celui de GitHub ont été audités par des milliers de chercheurs talentueux. Penser que la cible a déjà été « entièrement pillée » est une autre barrière. La réalité est que les applications évoluent constamment; chaque mise à jour, chaque nouvelle fonctionnalité introduit un potentiel pour de nouvelles vulnérabilités.
- **La taille et la complexité** Face à une application tentaculaire comme Salesforce, avec ses milliers de paramètres et de fonctionnalités, le sentiment d'être submergé est normal. Cependant, cette complexité est un avantage pour le chercheur. De plus, une grande partie du code est souvent basée sur des modèles, ce qui signifie qu'une vulnérabilité découverte dans une section peut être reproduite ailleurs.
- **Les logiciels open source ou payants** L'idée qu'un logiciel open source a été examiné par d'innombrables yeux et est donc exempt de bogues est fausse. Comme le dit Haddix : « il a été prouvé à maintes reprises que les projets open source ont parfois plus de bogues que les logiciels propriétaires ».

### **1.2. Le cinquième obstacle : L'exploration en surface**

Après avoir surmonté les quatre premiers obstacles, de nombreux chasseurs tombent dans le piège de ce que Jason Haddix appelle « l'iceberg ». Ils se contentent de tester la partie émergée de l'application, c'est-à-dire les fonctionnalités accessibles sans authentification, et se découragent rapidement. La véritable mine d'or se trouve presque toujours sous la surface, après la connexion.

Les fonctionnalités les plus « juteuses » se trouvent généralement derrière l'authentification :

- La section « Mon profil », riche en données persistantes (une cible de choix pour les XSS stockées).
- Les fonctions de téléversement de fichiers (documents, images de profil).
- Les intégrations avec des services tiers, qui peuvent être une source de SSRF.
- Les fonctions réservées aux comptes payants ou à différents niveaux d'utilisateurs.
- Les appels d'API non documentés, souvent moins sécurisés.
- Les outils d'administration auxquels on peut tenter d'accéder sans les privilèges requis.

Une fois ces barrières mentales franchies et un compte créé, la véritable chasse peut commencer.

--------------------------------------------------------------------------------

## 2. Phase 1 : Élargir la surface d'attaque

Cette première phase active consiste à cartographier l'empreinte numérique complète de la cible. L'objectif est d'identifier de manière exhaustive tous les actifs potentiels — domaines racines, sous-domaines, adresses IP et ports ouverts — avant de se plonger dans l'analyse des applications elles-mêmes. C'est l'étape de la collecte de renseignements à grande échelle.

### **2.1. Énumération des sous-domaines**

L'énumération des sous-domaines est le point de départ classique et fondamental. Des outils comme **SubFinder**, **Amass** et **Chaos** sont essentiels ici. Ils agrègent des données provenant d'une multitude de sources, telles que les journaux de transparence des certificats (Certificate Transparency logs), les enregistrements DNS passifs, les archives web et les moteurs de recherche, pour compiler une liste initiale de tous les sous-domaines associés à notre cible.

### **2.2. Analyse des relations et découverte de domaines racines**

Un programme de bug bounty peut définir un scope initial (ex. : `*.entreprise.com`), mais des actifs oubliés ou indirectement liés peuvent exister sur d'autres domaines racines. Les découvrir est une excellente façon de trouver des terrains moins explorés.

- **Acquisitions :** Les entreprises acquièrent d'autres sociétés, et les anciens domaines de ces dernières peuvent rester connectés à l'infrastructure principale. Une recherche sur des plateformes comme Crunchbase permet d'identifier les acquisitions passées et d'ajouter leurs domaines à notre liste de cibles.
- **Numéros de système autonome (ASN) :** Les grandes entreprises possèdent souvent leurs propres plages d'adresses IP, regroupées sous un ASN. En identifiant l'ASN de la cible via des services comme `bgp.he.net`, on peut cartographier l'ensemble de ses blocs d'IP. Ensuite, des outils comme `amass intel` peuvent interroger ces plages pour découvrir de nouveaux domaines racines qui y sont hébergés.
- **Reverse Whois :** Les informations d'enregistrement d'un nom de domaine (Whois) peuvent révéler l'entité qui l'a enregistré. Des services de "Reverse Whois" comme **waxy** permettent de faire la recherche inverse : trouver tous les autres domaines enregistrés par cette même entité, révélant potentiellement des domaines hors du scope initial mais appartenant à la même organisation.

### **2.3. Identification des actifs vivants**

Une longue liste de noms de domaine n'est utile que si l'on sait lesquels sont actifs et quels services ils hébergent. Ce processus se fait en deux temps.

1. **Vérification des serveurs web :** Un outil comme **HTTPX** est utilisé pour envoyer des requêtes HTTP/HTTPS à toute la liste de sous-domaines. Il filtre rapidement ceux qui hébergent un serveur web actif sur les ports standards (80, 443) et élimine les domaines inactifs.
2. **Scan de ports :** Il ne faut pas s'arrêter aux ports standards. Un scan de ports plus large avec des outils rapides comme **Nabu** ou **Rustscan** est crucial. Il permet de découvrir des services web ou des API hébergés sur des ports non conventionnels (ex. : 8080, 8443, 9000). Ces services sont souvent moins sécurisés car il s'agit fréquemment d'applications internes ou de développement qui n'étaient pas censées être exposées, ce qui en fait des cibles de choix.

Maintenant que nous avons notre carte, la véritable exploration commence. Découvrons ce que ces actifs recèlent.

--------------------------------------------------------------------------------

## 3. Phase 2 : La découverte de contenu, au cœur de la méthodologie

La découverte de contenu est l'une des activités les plus rentables pour un chasseur de bogues. C'est ici que l'on débusque les pépites : des fonctionnalités cachées, des fichiers de configuration oubliés, des panneaux d'administration non protégés ou des endpoints d'API non documentés. Une simple URL oubliée peut mener à une vulnérabilité critique.

### **3.1. Outils et listes de mots : Le duo gagnant**

Pour trouver ces ressources cachées, on utilise des outils de _fuzzing_ de répertoires. Le paysage est vaste (gobuster, dirsearch, wfuzz), mais **Feroxbuster** et **FFUF** se démarquent. Feroxbuster, le favori actuel de Jason Haddix, est particulièrement apprécié pour ses fonctionnalités avancées comme la possibilité de mettre en pause et de reprendre un scan ou son auto-ajustement pour filtrer le bruit. Cependant, l'efficacité de ces outils dépend entièrement de la qualité de la liste de mots (_wordlist_) utilisée. La stratégie consiste à procéder en deux temps : d'abord, utiliser une liste de mots spécifiquement adaptée à la technologie de la cible (ex. : PHP, IIS, Java), puis lancer une liste générique plus large. Le projet **wordlist.assetnote.io** est une ressource inestimable qui propose des listes optimisées pour de nombreuses technologies, basées sur l'analyse de millions de sites web.

### **3.2. Techniques avancées de découverte**

Au-delà du simple _fuzzing_, des techniques plus sophistiquées permettent de découvrir du contenu que les méthodes traditionnelles pourraient manquer.

1. **Le scan récursif :** Lorsqu'un répertoire est découvert (ex. : `/admin/`), il ne faut pas s'arrêter là, même s'il renvoie une erreur d'autorisation (401 Unauthorized ou 403 Forbidden). Il est crucial de continuer à scanner _à l'intérieur_ de ce répertoire. Haddix insiste : « J'ai gagné beaucoup d'argent grâce à la découverte de contenu récursive ». Il cite un exemple où un accès non autorisé a été trouvé profondément dans une arborescence `/admin/`, menant au compromis d'un million de dossiers personnels.
2. **L'analyse des applications mobiles :** Les applications mobiles communiquent souvent avec des API dont les endpoints ne sont pas visibles sur le site web principal. En décompilant le fichier d'installation d'une application Android (APK) avec un outil comme **apk leaks**, on peut extraire une liste précieuse d'endpoints d'API, de clés codées en dur et d'autres informations utiles.
3. **L'exploration du JavaScript :** Les fichiers JavaScript sont une mine d'or d'informations. Ils contiennent souvent des chemins relatifs, des endpoints d'API et des routes cachées. Des outils comme **LinkFinder**, **xnLinkFinder** (qui analyse également le JavaScript intégré directement dans les pages HTML) et l'extension Burp Suite **GAP** automatisent la recherche de ces informations dans les fichiers JS internes et externes.
4. **L'exploitation des données historiques :** Des services d'archivage du web conservent des copies anciennes des sites. Des endpoints qui ont été retirés du site actuel peuvent parfois rester actifs sur le serveur. Des outils comme **Gao** et **Waymore** interrogent ces archives pour extraire d'anciennes URL. La stratégie consiste ensuite à utiliser un outil comme **wordlistgen** pour transformer ces URL en une liste de mots personnalisée, créant ainsi un dictionnaire de cibles potentielles qui ne sont plus publiquement liées mais pourraient encore fonctionner.

Une fois cette phase de découverte terminée, il faut comprendre la technologie qui fait fonctionner ce contenu.

--------------------------------------------------------------------------------

## 4. Phase 3 : Profilage technologique et recherche de vulnérabilités connues

Comprendre la pile technologique d'une cible est essentiel pour affiner la stratégie de test. Savoir si l'on fait face à un WordPress, un Drupal, une application en Java ou en PHP permet de concentrer ses efforts sur les classes de vulnérabilités les plus probables. Cette phase permet également d'identifier rapidement des vulnérabilités connues et des erreurs de configuration évidentes, souvent qualifiées de « low-hanging fruit », avant de se lancer dans une analyse manuelle plus approfondie.

### **4.1. Identifier la pile technologique**

La première étape consiste à identifier les technologies utilisées par chaque application web découverte. Des extensions de navigateur comme **Wappalyzer** et **WhatRuns** sont très efficaces pour cela. En analysant les en-têtes HTTP, le code source et les scripts, elles peuvent détecter le CMS (ex. : Drupal), le framework (ex. : Laravel), le serveur web (ex. : Nginx), et bien plus encore. Pour ceux qui préfèrent automatiser ce processus en ligne de commande, **web-analyze** offre une alternative puissante.

### **4.2. La chasse aux CVE et aux mauvaises configurations**

Une fois la technologie identifiée, l'étape logique suivante est de vérifier si elle est affectée par des vulnérabilités publiquement connues (CVE) ou des erreurs de configuration communes. **Nuclei** est devenu l'outil de référence dans ce domaine. Il utilise une vaste bibliothèque de modèles (_templates_) pour scanner rapidement des milliers de cibles à la recherche de signatures de vulnérabilités spécifiques.

Cependant, comme le souligne Jason Haddix, l'approche doit être nuancée. Exécuter les modèles Nuclei par défaut sur des cibles très populaires et déjà largement testées (comme `tesla.com`) mènera souvent à des résultats dupliqués. En revanche, cette approche est extrêmement efficace dans deux scénarios :

1. Sur des sous-domaines nouvellement découverts ou moins connus (« green field »), qui ont probablement reçu moins d'attention de la part d'autres chercheurs.
2. En utilisant des modèles personnalisés pour des vulnérabilités récentes (0-day ou N-day) qui ne font pas encore partie des scans automatisés de tout le monde.

Cette approche automatisée permet de s'assurer qu'aucune vulnérabilité évidente n'a été manquée, préparant ainsi le terrain pour une analyse plus ciblée.

--------------------------------------------------------------------------------

## 5. Phase 4 : Heat Mapping, l'intuition du chasseur

Une fois les scans automatisés terminés, il est temps de faire appel à ce que Jason Haddix appelle l'« intuition du hacker ». Le heat mapping est sa méthode pour codifier cette intuition : identifier les zones d'une application où les vulnérabilités critiques se cachent le plus souvent. C'est ici que l'on commence à prioriser l'analyse manuelle.

- **Les fonctions de téléversement :** Elles sont une priorité absolue. Il faut distinguer les _intégrations_ (ex. : importer une photo de profil depuis un service tiers, une source potentielle de XSS/SSRF via les métadonnées) des _téléversements directs_. Pour ces derniers, le type de fichier est crucial : les documents (PDF, DOCX) sont souvent basés sur XML et doivent être testés pour les XXE et les SSRF, tandis que les images peuvent être manipulées (nom, métadonnées EXIF, en-têtes binaires) pour tenter des XSS ou des attaques de type shell upload.
- **Les types de contenu :** Dans votre proxy, filtrez par type de contenu. Les réponses `JSON` et `XML` sont des signaux forts indiquant la présence d'une API ou d'un service web. Ces endpoints sont des cibles privilégiées pour les problèmes de logique métier, de contrôle d'accès et de fuite d'informations.
- **La section « Compte » :** C'est un terrain de chasse idéal. La zone du profil utilisateur, où les données sont stockées et affichées, est une cible de choix pour les XSS stockées. Les sections de configuration abritent souvent des intégrations avec des services tiers, qui reposent sur des URL ou des webhooks, créant des opportunités parfaites pour des attaques SSRF.
- **La surveillance des erreurs :** Les erreurs d'application ne sont pas du bruit, ce sont des indices. Chaque erreur 500, chaque message de débogage révèle des informations sur le fonctionnement interne de l'application, les technologies utilisées ou les chemins de fichiers. Analysez ce qui a déclenché l'erreur : un métacaractère ? une charge utile trop volumineuse ? Ces informations sont précieuses pour affiner vos tentatives d'injection.

--------------------------------------------------------------------------------

## 6. Phase 5 : L'analyse de paramètres, le super-pouvoir du chasseur

C'est ce que Jason Haddix décrit comme son « super-pouvoir » : la capacité de prédire les classes de vulnérabilités probables en se basant sur une analyse statistique des noms de paramètres. Cette technique, issue de son projet `hunt`, permet de prioriser les tests sur des applications massives comptant des milliers de paramètres. Le concept a depuis évolué et a été popularisé sous forme de `gf patterns`.

L'idée est simple : certains noms de paramètres sont historiquement plus vulnérables à certains types d'attaques. En se concentrant sur ces derniers, on maximise ses chances de succès. Voici un exemple pour les vulnérabilités de type IDOR (Insecure Direct Object Reference) :

- `id`
- `user`
- `account`
- `number`
- `order`
- `key`
- `email`

Si vous repérez l'un de ces paramètres dans une requête, il doit immédiatement devenir une priorité pour des tests d'IDOR. Haddix prévoit de consolider et de publier une liste exhaustive de ces paramètres suspects dans un projet nommé `jhaddix/sus_params`. Maîtriser cette approche transforme la recherche de bogues d'une simple exécution de commandes à une stratégie de priorisation intelligente.

--------------------------------------------------------------------------------

## Conclusion : D'une liste de domaines à un plan d'attaque

Nous avons parcouru un long chemin : de la déconstruction des barrières psychologiques à la constitution d'une carte exhaustive des actifs, en passant par la découverte de contenu, les scans automatisés, puis l'analyse ciblée guidée par le heat mapping et l'analyse de paramètres. Ce voyage méthodique transforme une tâche intimidante en une série d'étapes logiques et gérables. La différence fondamentale entre un chasseur de bogues amateur et un professionnel réside dans cette approche structurée et cette curiosité insatiable qui pousse à explorer au-delà de la surface. En adoptant cet état d'esprit, vous ne vous contentez plus de chercher des bogues au hasard ; vous élaborez un véritable plan d'attaque. Rappelez-vous l'exemple de Teflon : la prochaine prime de 70 000 $ ne se cache pas forcément derrière un exploit complexe, mais dans une observation plus fine et une analyse plus rigoureuse de la surface d'attaque que les autres ont négligée.