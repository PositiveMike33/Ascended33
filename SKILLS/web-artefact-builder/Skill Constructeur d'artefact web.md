---

### Licence

Termes complets dans LICENSE.txt

# Web Artifacts Builder (Constructeur d'artefacts Web)

Pour construire de puissants artefacts frontaux claude.ai, suivez ces étapes :

1. Initialisez le repo frontend en utilisant `scripts/init-artifact.sh`
2. Développez votre artefact en éditant le code généré
3. Regroupez tout le code dans un seul fichier HTML en utilisant `scripts/bundle-artifact.sh`
4. Affichez l'artefact à l'utilisateur
5. tester l'artefact (facultatif)

**Stack** : React 18 + TypeScript + Vite + Parcel (bundling) + Tailwind CSS + shadcn/ui

## Lignes directrices en matière de conception et de style

TRES IMPORTANT : Pour éviter ce que l'on appelle souvent "AI slop", évitez d'utiliser des mises en page trop centrées, des dégradés violets, des coins arrondis uniformes et la police Inter.

## Démarrage rapide

### Étape 1 : Initialisation du projet

Exécutez le script d'initialisation pour créer un nouveau projet React :

bash

```bash
bash scripts/init-artifact.sh <nom-du-projet>
cd <nom du projet>
```

Ceci crée un projet entièrement configuré avec :

- ✅ React + TypeScript (via Vite)
- ✅ Tailwind CSS 3.4.1 avec le système de thématisation shadcn/ui
- ✅ Alias de chemin (`@/`) configurés
- ✅ 40+ composants shadcn/ui pré-installés
- ✅ Toutes les dépendances de Radix UI incluses
- ✅ Parcel configuré pour le bundling (via .parcelrc)
- ✅ Compatibilité Node 18+ (auto-détecte et épingle la version de Vite)

### Étape 2 : Développez votre artefact

Pour construire l'artefact, éditez les fichiers générés. Voir **Tâches de développement communes** ci-dessous pour des conseils.

### Étape 3 : Regroupement en un seul fichier HTML

Pour regrouper l'application React en un seul artefact HTML :

bash

```bash
bash scripts/bundle-artifact.sh
```

Cela crée `bundle.html` - un artefact autonome avec tout le JavaScript, le CSS et les dépendances soulignés. Ce fichier peut être directement partagé dans les conversations de Claude en tant qu'artefact.

**Exigences** : Votre projet doit avoir un `index.html` dans le répertoire racine.

**Ce que fait le script** :

- Installe les dépendances (parcel, @parcel/config-default, parcel-resolver-tspaths, html-inline)
- Crée la configuration `.parcelrc` avec le support des alias de chemin.
- Construit avec Parcel (pas de source maps)
- Inline toutes les ressources en un seul HTML en utilisant html-inline

### Étape 4 : Partager l'artefact avec l'utilisateur

Enfin, partagez le fichier HTML regroupé en conversation avec l'utilisateur afin qu'il puisse le voir comme un artefact.

### Étape 5 : Test/visualisation de l'artefact (facultatif)

Remarque : cette étape est totalement facultative. Ne l'exécutez que si elle est nécessaire ou demandée.

Pour tester/visualiser l'artefact, utilisez les outils disponibles (y compris d'autres compétences ou des outils intégrés comme Playwright ou Puppeteer). En général, évitez de tester l'artefact dès le départ, car cela ajoute un temps de latence entre la demande et le moment où l'artefact fini peut être vu. Testez plus tard, après avoir présenté l'artefact, si cela est demandé ou si des problèmes surviennent.

## Référence

- **shadcn/composants d'interface utilisateur** : [https://ui.shadcn.com/docs/components](https://ui.shadcn.com/docs/components)