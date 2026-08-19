---
name: abm-linkedin-creas
description: >-
  Génère des créas publicitaires LinkedIn co-brandées (VRAIS logos ÉMETTEUR + PROSPECT sur CHAQUE
  créa) en logique ABM 1-to-1, pour cibler UN compte nommé (le prospect, ex. Sanofi) au nom d'un
  client émetteur (ex. JobTeaser). 3 types : (1) Visibilité — mur de VRAIS logos clients de
  l'émetteur + success stories de l'industrie du prospect ; (2) Ad content « fausse présentation »
  — créa au format natif type slide/mockup qui décortique la problématique chiffrée du prospect ;
  (3) Ads NOMINATIVES portées par le commercial/BDR de l'émetteur — SA PHOTO (sa tête) + il parle en
  « je » au décideur : « [Prénom Nom], je peux vous aider à recruter [X]. Échangeons ensemble. » +
  ses coordonnées. Pour chaque créa : angle, copy et prompt image prêt à coller. Déclencher sur
  « monte-moi les créas ABM LinkedIn pour [compte] », « des ads pour cibler [compte] », « créas
  co-brandées [client] x [compte] », « ads nominatives sur les décideurs de [compte] », « créas ABM ».
  Générique : réutilisable pour tout couple émetteur × prospect. Cousine de lp-rapprochement (qui
  produit LA landing page) ; ici on produit LES créas.
---

# ABM LinkedIn — créas co-brandées (générique)

## Rôle

Produire des **créas publicitaires LinkedIn prêtes à briefer** pour qu'un **ÉMETTEUR** (le client,
ex. JobTeaser) chauffe **UN PROSPECT** nommé (le compte cible, ex. Sanofi) et ses décideurs.
Créas en **3 types**, **toutes co-brandées** : les **DEUX VRAIS logos** (émetteur + prospect) sur
CHAQUE créa, sans exception.

Skill sœur de `lp-rapprochement` (qui assemble LA landing page co-brandée). Même famille ABM 1-to-1,
mêmes règles d'or, mêmes sous-skills — mais ici la sortie, ce sont les **créas d'acquisition**.

## Règles d'or (non négociables)

- **FORMAT CARRÉ 1080×1080 EXCLUSIVEMENT** — TOUS les types, TOUTES les créas. Jamais de paysage
  (1200×627) ni de vertical. Un seul ratio : **1:1**. Les prompts image et les rendus l'imposent.
- **PAS DE « BANDEAU » / CARTOUCHE** : ne jamais enfermer un logo (ni le visage du BDR) dans une
  bande ou une boîte blanche posée sur la créa. Les logos sont intégrés **directement** sur le fond,
  proprement — en **version blanche/monochrome** si le fond est sombre (recolorer le SVG en #fff),
  jamais dans un rectangle blanc « bandeau ».
- **Anti-invention** : jamais une couleur, un logo, un chiffre, un témoignage, un client ou une
  actualité « de mémoire ». Toute donnée vient d'une source réelle (Phase 0) ou est demandée à
  l'utilisateur. Non sourcé = `[À CONFIRMER]`. Personne non vérifiée = `[MOCK — à remplacer]`.
  **Un logo n'est affiché comme « client de l'émetteur » que si c'est prouvé** (présent sur le site
  de l'émetteur, ou confirmé par l'utilisateur). Sinon on parle de « pairs du secteur », pas de clients.
- **CO-BRANDING SYSTÉMATIQUE, VRAIS LOGOS OBLIGATOIRES** : les DEUX logos (émetteur + prospect) sur
  CHAQUE créa. Voir le **Workflow logos** ci-dessous. **Aucune créa ne sort sans ses 2 vrais logos.**
- **Logos JAMAIS générés par IA** (l'IA les déforme). L'IA génère le FOND ; les vrais logos (et la
  photo du BDR) sont **overlayés en post-prod** dans des zones réservées.
- **La photo du BDR est obligatoire sur le Type 3** (voir Phase 0 + Type 3). C'est un vrai fichier
  fourni par l'utilisateur, jamais un visage généré par IA.
- **Reproductibilité** : `[émetteur]`, `[prospect]`, `[BDR]` sont des **variables**. Rien n'est codé
  en dur. JobTeaser × Sanofi × Alexis n'est qu'un EXEMPLE (voir `references/exemple-abm.md`).
- **Un prospect, des décideurs nommés, un objectif par type** par exécution.

## Phase 0 — Réunir la matière (ne jamais produire à l'aveugle)

Appeler les sous-skills dédiées si dispo ; sinon faire l'équivalent inline (recherche web + fetch).

1. **Kit de marque émetteur** → `emetteur-brand-kit` : charte (HEX/typo), **logo officiel** (Workflow
   logos), + **la liste des VRAIS clients affichés** par l'émetteur (scraper son site : section
   « ils nous font confiance ») → sert le mur de références du Type 1. Traité 1× par émetteur.
2. **Kit de marque prospect** → `cible-brand-kit` : charte réelle (HEX/typo) + **logo officiel** du
   prospect (Workflow logos). C'est ce qui rend le co-branding fidèle. Un par prospect.
3. **Signaux + success stories du prospect/secteur** → `cible-signaux` : 3-5 signaux vérifiés (fait +
   URL + date) sur 12 mois **+ au moins une success story de l'industrie du prospect** (ex. un pair
   qui recrute massivement) + la **phrase-thèse** « Parce que [signal prospect], [émetteur] peut
   [bénéfice] pour [prospect] ». Nourrit les Types 1 et 2.
4. **Décideurs** : ~10 personnes clés du prospect sur la fonction visée. Fournies → les utiliser ;
   sinon rechercher (réel) OU personas `[MOCK]` crédibles. Tableau : Prénom Nom · Intitulé · Métier · statut.
5. **BDR / commercial de l'émetteur (OBLIGATOIRE pour le Type 3)** : **Prénom Nom, intitulé, téléphone,
   lien de prise de RDV (Calendly) ET SA PHOTO (headshot, vrai fichier)**. Sans la photo, le Type 3
   ne peut pas être produit tel que voulu → la RÉCLAMER explicitement à l'utilisateur. C'est ce
   visage qui porte les ads nominatives (« la tête du BDR »).

Restituer en tête du livrable, section **"Contexte & inputs"** : signaux datés (source), success
story, kits de marque (HEX + les 2 logos + logos clients de l'émetteur), phrase-thèse, table des
décideurs, **fiche BDR (coordonnées + photo)**.

## Workflow logos (le cœur du co-branding — VRAIS fichiers)

Ordre d'acquisition d'un logo (s'arrêter au 1er qui marche) :
1. **Site/CDN officiel de la marque** (ex. og:image, `/_next/static/media/*.svg`, page presse/brand).
2. **Wikimedia Commons** — construire l'URL directe via le hash MD5 du nom de fichier :
   `https://upload.wikimedia.org/wikipedia/commons/{h0}/{h0h1}/{Nom_Fichier.svg}` où `h = md5(nom)`.
   (Egress sandbox : `upload.wikimedia.org` OK, CDN JobTeaser OK ; **`logo.clearbit.com` BLOQUÉ** → ne pas l'utiliser.)
3. **`logo-resolver`** (recréation SVG fidèle) en dernier recours.

- **Overlay SANS BANDEAU** : le fond (carré 1080×1080) est généré avec des **zones calmes réservées**
  (haut pour les 2 logos, la zone visage pour le BDR). On **compose** ensuite les vrais logos (et la
  photo BDR pour le Type 3) **posés directement** sur le fond — logos en **version blanche/monochrome**
  si le fond est sombre. **Jamais de cartouche/rectangle blanc** derrière un logo.
- Si un logo reste introuvable : emplacement réservé « [LOGO {marque} — à insérer] », jamais un logo inventé.

## Co-branding & couleurs

- **Univers du prospect dominant** (~70 %) : ses couleurs (HEX réels), ses codes, son logo au premier
  plan. Émetteur en signature claire mais secondaire (~30 %).
- **Jamais de partenariat sur-affiché** s'il n'existe pas : « [émetteur] peut aider [prospect] à… ».
- **Couleurs** : à défaut de HEX sourcés, DÉCRIRE l'univers colorimétrique en langage naturel dans le
  prompt image ; le HEX exact reste `[À CONFIRMER]`. On ne fabrique pas un hex précis « de mémoire ».

## Les 3 types de créa

Logique froid → chaud : Type 1 (se faire connaître / prouver) → Type 2 (montrer qu'on comprend leur
problème) → Type 3 (interpeller nommément, incarné par le BDR).

### TYPE 1 — Visibilité & preuve (logos + success stories)
CTA soft. Univers prospect dominant + 2 logos.
1. **Références (mur de logos)** : les **VRAIS clients de l'émetteur** (sourcés Phase 0), en priorité
   ceux proches du secteur du prospect. « Ils recrutent/travaillent déjà avec [émetteur]. » Logos
   réels overlayés. Si aucun client prouvé du secteur → « les acteurs de [secteur] » (pairs), sans
   les qualifier de clients.
2. **Success story de l'industrie** : mettre en avant un **cas réel du secteur du prospect** (chiffre
   + source Phase 0) qui prouve que « ça marche » pour un acteur comme lui.
3. **Crédibilité** : chiffres clés de l'émetteur (réels) ou label/preuve rassurant.

### TYPE 2 — Ad content « fausse présentation » (format natif)
Créa qui **ressemble à une slide / un extrait de présentation / un mockup** (pas une pub léchée
d'agence) — le format « fausse présentation » performe en natif sur LinkedIn. Contenu = la
**problématique chiffrée du moment du prospect** (signaux Phase 0) décortiquée : titre de slide,
gros chiffre/enjeu, 2-3 puces, l'émetteur comme réponse, CTA de conversion. Univers prospect
dominant, **2 logos** (comme un logo d'entête de deck). 3 variantes (par problématique ou métier).
> Se caler sur la **créa de référence fournie par l'utilisateur** pour le style exact du « faux slide ».

### TYPE 3 — Ads NOMINATIVES portées par le BDR (une par décideur)
Le plus différenciant. **L'ad montre LA TÊTE du BDR de l'émetteur** (sa vraie photo) qui s'adresse
en **« je »** au décideur du prospect. **Formule à respecter** :
> **[Prénom Nom du décideur], je peux vous aider à [bénéfice chiffré/concret] de [prospect].**
> **Échangeons ensemble.** (CTA)
Signé : **[BDR — Prénom Nom · intitulé · téléphone · lien RDV]**.
Exemples (transposables) :
> « Nicolas, je peux vous aider à recruter vos 1 000+ alternants de Place d'Avenir. Échangeons ensemble. » — Alexis Samuel, Resp. dév. partenariats.
- **Photo BDR OBLIGATOIRE et EN GRAND** (vrai fichier, overlay, jamais IA). Le visage du BDR est un
  **élément principal** de la créa : grand portrait (≈ 40-55 % de la surface — ex. moitié droite, ou
  cercle large), pas une vignette. **Exiger une photo HD** (≥ 500×500 px) ; si l'utilisateur ne
  fournit qu'une basse résolution, le signaler (rendu pixelisé si agrandie) et réclamer une version HD.
  Pas de bandeau autour du visage : détourage propre / cercle net, intégré au fond.
- **Bénéfice/chiffre** : issu d'un signal réel du prospect, sinon générique ou `[X — à confirmer]`.
- **Volume** : **une créa par décideur** de la liste + un **gabarit variabilisé**
  `[Prénom Nom] · [Intitulé] · [bénéfice]`.
- **Visuel** : carré 1080×1080, univers prospect ultra-dominant, **grand visage du BDR**, texte roi,
  **2 logos posés directement (sans bandeau)**, **coordonnées du BDR** (nom, intitulé, tél, RDV).
- **Éthique/RGPD** : nommer un décideur dans une pub est sensible → signaler validation wording + image.

## Production des visuels (Studio + overlay)

**Toujours en carré 1080×1080.** Le plus fiable : générer le **FOND** via Studio, puis **composer en
HTML/CSS** (rendu net) les logos + le grand visage du BDR + le texte, plutôt que d'incruster le texte
par l'IA (qui le déforme).
1. Générer le **FOND** carré via Studio/IA (`bdzCreateStudioJob`, `useTov:false`) : **1:1**, univers
   prospect dominant (HEX réels), **zones calmes réservées** (bandeau haut pour les logos, zone visage
   pour le BDR au Type 3). Toujours « no logos, no brand marks, no text drawn » — le texte et les logos
   viennent en overlay.
2. **Overlayer** (HTML/CSS → capture 1080×1080) : 2 vrais logos **posés directement, sans cartouche**
   (versions blanches sur fond sombre) + **grand visage du BDR** (Type 3) + texte exact + CTA + coordonnées.
3. Si du texte est incrusté par l'IA : l'imposer **ligne par ligne** + « Spelling accuracy is the top
   priority » (sinon l'IA déforme la fin de phrase). Préférer toujours le texte en HTML overlay.

## Livrable

Un seul document Markdown. Pour CHAQUE créa, remplir `references/brief-crea-template.md` : type,
objectif, angle (adossé à un signal réel), **copy complet** (accroche + corps + CTA), et **prompt
image prêt à coller**. **Suivre `references/exemple-abm.md`** pour le niveau (à TRANSPOSER).

## Règles de qualité

- **FORMAT CARRÉ 1080×1080 partout** — aucun autre ratio.
- **Aucun bandeau / cartouche** : logos posés directement (blancs sur fond sombre).
- **3 types** ; Type 3 décliné sur toute la liste de décideurs.
- **2 VRAIS logos par créa** (Workflow logos), univers prospect dominant (~70/30), **logos jamais IA**.
- **Type 3 = la tête du BDR EN GRAND** (photo réelle HD ≥ 500 px) + « [Nom], je peux vous aider à …
  Échangeons ensemble » + coordonnées.
- **Type 2 = format « fausse présentation »** calé sur la réf utilisateur.
- **Chiffres, actus, couleurs, clients réels** (Phase 0), sinon `[À CONFIRMER]` ; personnes `[MOCK]`.
- **100 % générique** : `[émetteur]`/`[prospect]`/`[BDR]` = variables ; aucun cas codé en dur.
- **Briefable tel quel** : prompts image concrets, prêts à coller.

## Format de sortie

```
# Créas ABM LinkedIn — [Émetteur] × [Prospect]
## Contexte & inputs  (signaux datés + success story, kits de marque + 2 logos + logos clients émetteur,
                       phrase-thèse, table décideurs, FICHE BDR : coordonnées + photo)
## TYPE 1 — Visibilité & preuve
### 1.1 Références (vrais clients émetteur)   ### 1.2 Success story industrie   ### 1.3 Crédibilité
## TYPE 2 — Ad content « fausse présentation »
### 2.1   ### 2.2   ### 2.3   (par problématique/métier)
## TYPE 3 — Ads nominatives portées par le BDR (une par décideur)
### 3.1 [Nom]   ### 3.2 [Nom]   ### 3.3 [Nom]   + reste de la liste + gabarit variabilisé
## Points à confirmer / à remplacer  ([À CONFIRMER] + [MOCK] + photo/coordonnées BDR)
```

Proposer à la fin : générer les visuels (Studio + overlay logos & photo BDR), décliner le Type 3 sur
toute la liste, ou enchaîner sur `lp-rapprochement` pour la landing page de destination.
