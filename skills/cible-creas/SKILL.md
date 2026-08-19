---
name: cible-creas
description: >-
  Produit les VRAIES images humaines de la landing (pas seulement des prompts) : hero secteur + portraits
  divers, calés sur les 2 chartes et inspirés des vraies créas du site émetteur, générés via Bulldozer
  Studio, puis TÉLÉCHARGÉS/rehébergés dans assets/ (ou livrés via une galerie de récupération si le
  rapatriement est bloqué). Déclencher depuis l'orchestrateur lp-rapprochement, ou sur "génère les créas
  pour [cible]", "images humaines de la LP". S'exécute UNE fois PAR CIBLE (portraits réutilisables).
---

# cible-creas — Créas humaines (/cible)

But : page très humaine (vrais visages, vraies scènes métier), pas des icônes abstraites. Cette phase
PRODUIT des images réelles prêtes à placer.

## 0. RÉCUPÉRER LES VRAIES IMAGES DE L'ÉMETTEUR D'ABORD (obligatoire, avant tout prompt)
On ne génère pas « à l'aveugle » : on part du style réel de l'émetteur.
1. **Rapatrier les vrais visuels de l'émetteur** dans `assets/emetteur/` s'ils n'y sont pas déjà
   (emetteur-brand-kit §3A) : `og:image`, photos hero, illustrations, mockups. Les pages SPA lazy-load →
   lire l'`og:image`/`twitter:image` dans le `<head>` (fiable, sans scroll) + les images déjà chargées ;
   dérouler l'URL des optimiseurs (`next/image?url=…` → URL d'origine). Domaines CDN émetteur = souvent
   ouverts à l'egress même si Clearbit est bloqué.
2. **DÉCODER le langage visuel de l'émetteur** (le regarder vraiment) : motifs signature (ex. JobTeaser =
   flèches montantes vert→violet, cartes blanches à ombre verte décalée, line-art géométrique sur fond noir),
   accent secondaire (ex. le violet de JobTeaser en plus du vert), style photo, cadrage. **Changer la
   couleur ne suffit pas** : reproduire ces motifs, sinon la créa ne « ressemble » pas à la marque.
3. **Passer ces images en RÉFÉRENCE à Studio** via `referenceUrls:[…]` (URLs publiques) ou
   `fridgeIds:[…]` — c'est le levier n°1 pour que le rendu colle au vrai style. À défaut d'images
   émetteur, décrire explicitement les motifs décodés dans le prompt.

## 1. TROIS familles de créas OBLIGATOIRES (toutes via Bulldozer Studio, calées sur la CIBLE)
Toutes injectent les HEX de marque en lumière/accents (rim light émetteur + glow accent cible), **reprennent
les motifs signature de l'émetteur décodés en §0**, et sont générées avec les vraies images émetteur en
`referenceUrls`. Négatifs communs :
`no distorted hands, no text artifacts, no watermark, no stock cliché, no fake brand logos`.
**Jamais de logo généré par l'IA** : le logo de la cible s'ajoute EN POST (overlay HTML), pas dans le prompt.

**A. Humain mis en scène AVEC la cible (mediaType IMAGE).**
Jeunes talents dans l'UNIVERS RÉEL de la cible : décor du secteur de la cible, couleurs de la cible en
lumière, accessoires/produit de la cible (ex. Mooncard → carte de paiement + app de dépenses ; Dalkia →
site énergie ; banque → bureau finance). 1 hero 16:9 + 2-3 portraits/scènes 4:5, divers, photoréaliste
éditorial, faible profondeur de champ. Utiliser `assetIds` (image de référence) pour garder une personne
cohérente entre plusieurs plans si besoin.
> **Générer une personne sur fond neutre détourable** (fond gris/blanc uni, marges généreuses) quand on
> veut la COMPOSER façon « pub émetteur » (cf. A+ ci-dessous) : cercle accent + cartes-logos autour.

**A+. Composition « ad » à la manière de l'émetteur (montée en POST, pas en génération).**
Reproduire la mise en page publicitaire signature de l'émetteur (décodée en §0). Ex. JobTeaser : le talent
dans un **cercle vert**, entouré de **vraies cartes-logos d'écoles/clients** (fichiers réels), de **flèches
montantes** vert + violet, sur fond dark/motion. On assemble ça en HTML/CSS (photo détourée en cercle +
cartes `position:absolute` avec les vrais logos + SVG flèches), PAS en un seul rendu IA. C'est ce qui fait
« vraie campagne de la marque » et non « image d'agence générique ».

**⭐ ULTRA-PERSONNALISATION (obligatoire) — « pour vous, [cible] ».**
Le hero DOIT afficher au moins un élément co-brandé **« [cible] × [émetteur] »** bien visible (une carte
« POUR VOUS » façon notification, un écran/laptop montrant un dashboard co-brandé, un mockup). Objectif :
le prospect voit immédiatement que la page est faite pour LUI. Les logos = **vrais fichiers en overlay HTML**,
jamais générés par l'IA (l'IA déforme les logos → « faux logo » interdit). Si la scène contient un écran,
générer un écran au **bandeau/haut propre** pour y poser le lockup réel en post.

**B. Motion adaptée à la cible (mediaType VIDEO) — À GÉNÉRER, pas à esquiver.**
Fond animé de hero : loop 3D abstrait bi-couleur (accent émetteur + accent cible) évoquant le métier de la
cible (réseau de nœuds talents↔entreprise, streaks, particules ; carte/pièce pour une fintech, molécule
pour la santé, etc.). **Génération OBLIGATOIRE via `bdzCreateStudioJob` mediaType VIDEO** (`durationSeconds`
8), pas un simple fond CSS. ⚠️ Veo bloque souvent les humains → **motion SANS personne** (abstrait), laisser
`personGeneration` non défini (auto-résolu). La vidéo (~1 min de rendu) sert de `<video autoplay muted loop
playsinline poster=…>` en fond de hero. **Repli CSS/canvas UNIQUEMENT si le job VIDEO échoue** (à noter
explicitement) — jamais par défaut. Toujours fournir un `poster` (frame extraite ou aplat sombre) + gérer
`prefers-reduced-motion` (masquer la vidéo) + pause hors-écran/onglet caché.
> **Les 2 logos (émetteur + cible) DOIVENT être présents sur le fond vidéo.** Comme on ne met jamais de
> logo dans un rendu Veo (déformé), on les superpose en POST : lockup co-brandé `position:absolute`
> par-dessus la `<video>` (SVG réels, nets, z-index au-dessus de la vidéo). (Burn-in dans le mp4 = seulement
> si un pipeline vidéo/ffmpeg est dispo.)
> ⚠️ **LISIBILITÉ SUR TOUTE FRAME (obligatoire).** Une vidéo bouge → un logo posé « à nu » dessus disparaît
> sur les frames claires. Donc **tout logo sur une vidéo/photo est posé sur un fond solide** : plaque/pill
> sombre semi-opaque (ex. `rgba(14,14,14,.6)` + `backdrop-filter:blur`) OU carte de couleur de marque (ex.
> carte lime co-brandée auto-portée). Ne JAMAIS compter sur la frame. Vérifier au pire cas : figer la vidéo
> sur une frame claire (`video.currentTime`) et contrôler que chaque logo reste lisible.

**C. Illustrations / outils (mediaType IMAGE).**
Illustrations plates / mockups produit aux couleurs cible + motifs signature émetteur (§0) : UI de l'outil/app,
pictos, motifs, mock 16:9 ou 9:16. Pour les sections Valeur/illustration. **Injecter les 2 accents** (émetteur
+ cible) et les motifs décodés (ex. flèches, cartes à ombre colorée), pas seulement une teinte. Générer avec
les vraies images émetteur en `referenceUrls`. Style flat premium. Interdire tout texte/lettre/chiffre dans
le prompt (les artefacts typographiques IA sont fréquents → « no text, no letters, no numbers »).

## 2. Génération RÉELLE (Studio)
- Vérifier l'accès plugin (`bdzGetCustomerSubscription`) ; projet dans `~/bulldozer.json` (customerId+projectId).
- `bdzCreateStudioJob` : `mediaType` = `STUDIO_MEDIA_TYPE_IMAGE` (A, C) ou `STUDIO_MEDIA_TYPE_VIDEO` (B).
  `inputs` = tableau JSON d'objets, chacun : `text` (prompt), `referenceUrls:[URLs publiques]` (images de
  style/cohérence — **utiliser les vraies images émetteur ici**, jusqu'à 14 pour IMAGE / 3 pour VIDEO),
  `fridgeIds:[…]` (fichiers fridge dont on est propriétaire). VIDEO : `durationSeconds` 4/6/8 (8 si
  referenceUrls). → polling `bdzGetStudioJob` (statut `completed` ; image ~10-40 s, vidéo ~1 min ; poller
  plusieurs fois) → `results[].assets[].url` = URL S3 présignée (~1 h).
- Cohérence d'un même personnage entre plans : passer l'asset déjà généré en `referenceUrls`.
- Régénérer si artefacts (texte parasite, hex qui fuit dans l'image, mains déformées) : durcir les négatifs.
- Si Studio indisponible (plugin non autorisé) : le DIRE à l'utilisateur et proposer (a) autoriser le plugin,
  (b) déposer ses propres photos, (c) fond CSS/canvas + illustrations SVG on-brand (réalisables sans Studio).
  Jamais de stock cliché ni de fausse photo en silence.

## 3. Rapatriement dans assets/ (le point critique)
Les sorties Studio vivent sur S3 (lien présigné, expirant) et le **sandbox peut être bloqué** (allowlist egress).
- **Si egress ouvert** (domaine S3 autorisé) : `curl` le lien → `assets/hero-[cible].jpg`, `assets/portrait-N.jpg`.
  Optimiser : opaques → JPEG q≈82 ≤1600px ; transparents → PNG (jamais aplati). C'est la voie DURABLE.
- **Si bloqué** : produire une **galerie de récupération** `apercu-creas.html` référençant les liens
  présignés, avec pour chaque image un `<a download="nom-cible.jpg">` → l'utilisateur enregistre en 1 clic
  dans `assets/`. Regénérer des liens frais si expirés. Câbler les `<img src="assets/…">` avec `onerror`
  (repli fond animé) pour zéro image cassée.

## Livrable
Fichiers dans `assets/` : vrais visuels émetteur (`assets/emetteur/*`), photos famille A
(`hero-[cible].jpg` + portraits/scènes), **motion `motion-hero.mp4` + `motion-hero-poster.*`**, illustrations
famille C — le tout + `prompts-images-[emetteur]-[cible].md` (prompts + `referenceUrls` utilisés).

## GATE C3 (bloquante)
```
[ ] Vraies images émetteur récupérées dans assets/emetteur/ + langage visuel décodé (motifs + accent 2ndaire)
[ ] Prompts écrits pour les 3 familles, avec referenceUrls (images émetteur) + 2 accents (émetteur+cible)
[ ] Studio completed : ≥1 image A + ≥1 illustration C + 1 MOTION VIDÉO (mp4) — repli CSS seulement si le job
    VIDEO a échoué, et alors NOTÉ explicitement (jamais « pas de vidéo » en silence)
[ ] Hero = composition « ad » émetteur (A+) : talent + cercle/accent + vraies cartes-logos + flèches
[ ] Ultra-perso : élément co-brandé « [cible] × [émetteur] » VISIBLE dans le hero (logos réels en overlay)
[ ] Les 2 logos (émetteur + cible) présents sur le fond vidéo (lockup/filigrane overlay), jamais en IA
[ ] Fichiers présents dans assets/ (egress ouvert) — OU galerie de récupération + assets/ câblé en fallback
[ ] Motion : poster fourni + reduced-motion géré + pause hors-écran
[ ] Règles images respectées (transparents = PNG, pas de halo, pas de texte IA) ; aucun logo IA (logos en post)
```
Si l'utilisateur exige des photos en dur et que le rapatriement est bloqué → STOP : demander l'ouverture
egress ou le dépôt manuel, ne pas livrer une page « sans images » en silence.
