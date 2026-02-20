#OSINT 
# Fiche de stratégie : Maîtriser la recherche en ligne et éviter les « terriers de lapin »

## 1. L'état d'esprit de l'investigateur : L'objectif avant l'outil

Pour transformer une simple navigation en une investigation efficace, il est impératif de distinguer « naviguer sur le Web » d'une « recherche structurée ». Selon l'expert Ryan MacDougall, l'OSINT (_Open Source Intelligence_) ne repose pas sur la puissance de vos logiciels, mais sur votre mentalité (_mindset_). Un expert ne se définit pas par sa collection d'outils — qui sont par nature éphémères — mais par sa rigueur méthodologique.

L'un des plus grands pièges est de croire que plus de données ou des outils payants (comme People.com) garantissent de meilleurs résultats. En réalité, ces plateformes génèrent souvent plus de « bruit » que de « signal », noyant l'information utile sous une masse de détails non pertinents.

**La Règle d'Or :** Effectuer une recherche en ligne sans avoir d'objectif précis n'est rien d'autre que du simple surf sur le Web. Pour qu'une recherche soit productive, chaque action doit être dictée par une question spécifique à résoudre.

Cette clarté d'objectif est votre garde-fou : elle dicte la gestion de votre temps et détermine jusqu'où vous devez descendre dans l'exploration avant de pivoter.

## 2. Identifier et éviter le « Terrier de Lapin » (Rabbit Hole)

En OSINT, le « terrier de lapin » survient lorsqu'on investit un temps disproportionné dans une piste sans issue. Cela arrive souvent pour deux raisons : soit l'investigateur commence par une supposition et cherche désespérément à la prouver, soit il se laisse submerger par des bases de données massives sans lien direct avec son besoin initial. Pour rester efficace, il faut savoir quand l'accumulation de données cesse de servir la décision finale.

|   |   |   |
|---|---|---|
|Caractéristiques|Recherche Productive|Terrier de Lapin (Rabbit Hole)|
|**Orientation**|Toujours orientée vers l'objectif final et le budget/temps imparti.|Perte de vue du but initial au profit de la curiosité pure.|
|**Résultats**|Produit des données exploitables (« Signal »).|Accumulation de données sans lien avec la décision (ex: s'enfoncer dans un agrégateur payant).|
|**Progression**|Avance par étapes logiques et vérifiables.|Sensation d'être submergé par trop de détails et de « bruit ».|
|**Finalité**|Mène à une conclusion ou une action concrète.|Entraîne une confusion mentale et un épuisement des ressources.|

Pour s'extraire d'un terrier, l'investigateur doit savoir prendre de la hauteur et évaluer si la profondeur de sa recherche actuelle dépasse la valeur de l'information recherchée.

## 3. La stratégie de l'arborescence (Spiderwebbing) : Savoir reculer pour mieux avancer

La technique du « Spiderwebbing » consiste à ne pas s'enfoncer de manière linéaire, mais à explorer plusieurs branches en rayonnant autour d'un point central. L'idée est d'avancer par bonds itératifs et de savoir faire marche arrière pour explorer une nouvelle voie.

- **1. Exploration initiale :**
    - Commencer par un point d'entrée (nom, téléphone, entreprise).
    - Limiter la progression à **3 ou 5 étapes** maximum dans une seule direction.
- **2. Évaluation de la pertinence (Critères de décision) :**
    - Analyser la fraîcheur de l'information. _Exemple :_ Si vous cherchez un entrepreneur, est-ce que ses données datent de 1998 (ancienne activité) ou de 2019 (activité actuelle) ?
    - Déterminer si la source (ex: réseaux sociaux) n'est qu'un masque ou si elle offre un véritable caractère informatif.
- **3. Pivotement (Forking) :**
    - Si une branche stagne, revenez au point précédent et créez un « Fork » vers une nouvelle source.
    - _Exemple :_ Passer d'un profil Facebook (peu fiable pour évaluer le caractère) à un profil LinkedIn pour confirmer un statut professionnel (VP de banque), puis aux registres fonciers pour valider une adresse.

Cette agilité de mouvement permet de couvrir un spectre large sans s'épuiser. Elle exige toutefois une trace écrite rigoureuse pour ne pas tourner en rond.

## 4. La cartographie du parcours : Documenter pour ne pas se perdre

La documentation est ce qui transforme une recherche désordonnée en une compétence professionnelle. Noter précisément son cheminement permet de « figer » le signal trouvé et d'éviter de répéter des recherches stériles. Suivre une structure simple permet de passer l'enquête à un tiers ou d'y revenir des semaines plus tard sans perte de contexte.

**Modèle de Log de Recherche (Exemple inspiré du cas "Julia") :**

1. **Outil :** Google (Images) **Terme :** `"Julia [Nom de famille]" + [État]` **URL :** `https://www.linkedin.com/in/julia-target-123` **Note :** Confirmation visuelle de la cible. Le lien image Google mène à un profil LinkedIn sans photo, mais la corrélation université/poste confirme l'identité.
2. **Outil :** Registres Publics (Voter Records) **Terme :** `[Adresse résidentielle]` **URL :** `https://voterrecords.com/address/xyz` **Note :** Identification du mari (Victor) et confirmation de la co-propriété d'une entreprise immobilière.
3. **Outil :** Recherche Manta / Sociétés **Terme :** `[Nom de l'entreprise immobilière]` **URL :** `https://www.manta.com/c/company-profile` **Note :** Julia est listée comme VP de banque et propriétaire de l'entreprise. Statut professionnel haut placé (probablement cautionnée par l'État/federally bonded), ce qui renforce la confiance.

## 5. Synthèse : Les 3 piliers de l'efficacité numérique

Pour maîtriser l'abondance d'informations, l'apprenant doit s'appuyer sur ces trois piliers :

- **L'Objectif (Mindset) :** Définir la mission avant d'ouvrir un navigateur.
    - _Bénéfice :_ Clarté mentale et protection contre la surcharge d'informations.
- **L'Itération (Forking) :** Appliquer la règle des 3-5 étapes et savoir abandonner une branche stérile.
    - _Bénéfice :_ Préservation des ressources et évitement des terriers de lapin improductifs.
- **La Rigueur (Documentation) :** Consigner chaque étape (Outil, Terme, URL, Note).
    - _Bénéfice :_ Fiabilité totale des résultats et capacité à reconstruire le puzzle de l'information à tout moment.

La maîtrise de ces techniques augmente radicalement votre efficacité, que ce soit pour vérifier les antécédents d'un contractant ou pour sécuriser votre environnement familial. Gardez en tête que dans le monde de l'information, la connaissance n'est pas seulement un pouvoir : **la connaissance est la confiance.**