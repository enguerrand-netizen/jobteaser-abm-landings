---
name: lp-assemblage
description: >-
  Monte la landing page co-brandée à partir du template de référence tokenisé, en consommant le brandbook
  émetteur, le brandbook cible, les signaux et les créas déjà produits. Theming (HEX réels), co-branding
  (logos partout : nav + bande + footer), structure complète, effet wow (3D/motion + reveals + compteurs),
  responsive mobile-first, gestion fine des images. NE COLLECTE RIEN (les données arrivent des sous-skills
  amont). Déclencher depuis l'orchestrateur lp-rapprochement, ou sur "assemble la LP", "monte la page".
---

# lp-assemblage — Montage de la page (/cible)

**Règle design (non négociable)** : on ne code JAMAIS de zéro. On part de `reference/template.html`
(design productisé, tokenisé) et on remplit `:root` + les `{{PLACEHOLDERS}}`. Niveau cible = l'exemple
d'or `reference/example/lp-jobteaser-sanofi.html`. Règles couleurs/typo/fallback : `reference/DESIGN-SYSTEM.md`.
Entrées attendues (des sous-skills) : `brandbook-[emetteur].md`, `brandbook-[cible].md`, `signaux[]`+`these`,
`assets/` (logos + créas).

## PHASE Theming (ex-5bis) — remplir les tokens AVANT de coder
Algorithme de `reference/DESIGN-SYSTEM.md` :
1. MODE (dark/light) selon la marque ÉMETTRICE.
2. Neutres du mode (`--bg --surface --text --muted --line`).
3. `--brand` = signature émetteur ; `--accent` = signature prospect (HEX réels des brandbooks). Si trop
   proches → décaler l'accent en teinte/luminosité.
4. Contraste AA : `--brand-ink` (texte sur bouton), `--brand-hi` (hover), `--accent-soft` (fonds).
4b. **⭐ `--accent-ink` (luminance de l'accent, CRUCIAL)** : couleur du texte/logos POSÉS sur `--accent`.
    Accent CLAIR (lime `#DDFF56`) → `--accent-ink:#1A191C` (foncé) ; accent FONCÉ (violet `#7A00E6`) →
    `--accent-ink:#FFFFFF` (blanc). Partout où le fond = `--accent` (carte « POUR VOUS », bande, surlignage
    `.acc`), texte = `--accent-ink` ET **variante de logo cible adaptée** (blanche si accent foncé). Changer
    seulement la couleur casse le contraste — cf. `reference/DESIGN-SYSTEM.md §1`.
5. `--font-display`/`--font-body` = polices réelles de la charte émetteur (+ fallbacks OFFICIELS ; jamais
   une police « proche » de mémoire).
Publier le bloc `:root` complété.
> ⚠️ **La charte émetteur PRIME sur le style par défaut du template.** Si la charte impose d'autres codes
> (ex. flat : PAS de dégradé/ombre/glow/particules, coins carrés) → écraser ces éléments du template.
> Changer seulement la couleur ne suffit pas.

## PHASE Rédaction & code (ex-6)
Remplir `:root` + tous les `{{PLACEHOLDERS}}` ; brancher `assets/` (logos, images, motion). Ne rien
réécrire de la structure/CSS/JS sauf besoin explicite. Grilles extensibles (ajouter/retirer signaux et
value_props selon la matière). Copywriting selon les gabarits du DESIGN-SYSTEM.

### Structure (déjà dans le template)
1. **Hero co-brandé, composition « ad » émetteur** : reproduire la mise en page publicitaire signature de
   l'émetteur (cf. cible-creas §0/A+) — ex. talent détouré dans un **cercle accent** + **vraies cartes-logos**
   (écoles/clients, fichiers réels) + **flèches/motifs** de la marque, par-dessus le fond motion. Logos RÉELS
   émetteur + prospect (jamais IA). Titre nominatif, sous-titre = la thèse, CTA principal.
   **⭐ Ultra-perso** : afficher un élément co-brandé **« [Prospect] × [Émetteur] »** proéminent (carte
   « POUR VOUS », écran/mockup co-brandé) pour que le prospect voie que la page est faite pour lui.
   **Fond vidéo** : superposer le lockup des 2 logos PAR-DESSUS la `<video>` (overlay HTML, z-index au-dessus)
   → les logos sont « dans » le fond animé, nets, jamais générés par l'IA.
   ⚠️ **Tout logo sur une vidéo/photo = sur un fond solide** (plaque/pill sombre `rgba(14,14,14,.6)`+blur, ou
   carte de couleur de marque). Une vidéo bouge → sans plaque, le logo disparaît sur les frames claires.
   Contrôle obligatoire : figer la vidéo sur une frame CLAIRE et vérifier que CHAQUE logo reste lisible.
2. **Pourquoi vous, pourquoi maintenant** : 2-3 phrases reprenant les signaux réels du prospect.
3. **Valeur pour le prospect** : ≥ 3 blocs côté prospect (« vous obtenez Y »), plus si `value_props[]`.
4. **Preuve / réassurance** — OBLIGATOIRE et dense : **bande « ils recrutent déjà avec [émetteur] » avec
   les vrais logos clients du SECTEUR de la cible en tête** (ex. cible fintech → BNP Paribas d'abord), puis
   écosystème/partenaires, 3-4 chiffres, ≥1 témoignage nominatif, notes/avis, labels, 1 mini-cas — tout
   depuis le brandbook émetteur (`reassurance[]`). Logos via `logo-resolver` (fichiers) ; si indisponibles
   (egress fermé) → **repli chips texte des marques** + note « logos à intégrer », jamais rien d'inventé.
   Ne pas se contenter d'une liste d'écoles génériques : la bande clients-secteur prime.
5. **Comment on collabore** : 3 étapes rassurantes (pas d'engagement lourd au 1er pas).
6. **CTA final = section « Rencontrez [Commercial] » (humain, recommandé)** : au lieu d'un simple bouton,
   présenter le commercial en chair et en os → **photo réelle** (jamais IA ; fallback initiales si absente),
   nom, rôle, **message à la 1re personne** (« Bonjour, je suis … »), puis **Calendly** (CTA principal),
   **téléphone** (`tel:+33…`) et email. Un visage + une ligne directe = beaucoup plus humain et convertit
   mieux qu'un mailto. Photo cerclée aux 2 accents (émetteur + cible). C'est ce vers quoi pointent la nav,
   le hero et le CTA sticky mobile (`#contact`).
Optionnel : FAQ objections (2-3).

### Rendre la page HUMAINE (exigence)
Vrais visages (créas + le commercial), voix à la 1re/2e personne, chaleureuse. Le prospect doit sentir une
personne derrière la page : nom + photo + créneau + numéro. La 3D/motion encadre l'humain, ne le remplace pas.

### Co-branding — la cible TOUJOURS visible (exigence forte)
Lockup « [émetteur-logo] × [prospect-logo] » réutilisé : **nav** (sticky), **hero**, **bande co-brandée
pleine largeur** mid-page, séparateurs de sections, **footer**. Nom/logo du prospect repris dans sa couleur
d'accent à chaque section (kicker, `.dot`, titres). Prévoir `<img src="assets/logo-*.svg">` + fallback
(texte/SVG recréé) via `onerror` : jamais d'image cassée, cible jamais absente.

### Effet « wow »
Hero 3D/motion (Three.js r128 via cdnjs OU canvas particules bi-couleur) + ≥ 1 2e moment 3D (objet au
scroll / cartes tilt) + reveals (IntersectionObserver) + compteurs animés + hovers. Toujours un fallback
(poster/statique), coupé si `prefers-reduced-motion` ou WebGL absent. Fond animé, jamais un aplat statique.

### Mobile-first (OBLIGATOIRE)
1 colonne, ordre logique, hero sans scroll horizontal, images recadrées portrait, bandeaux logos en
carrousel/grille 2-3 col. Titres qui ne débordent pas, corps ≥ 16px, CTA ≥ 44px, zones tap espacées.
3D/motion allégée sur mobile, `prefers-reduced-motion`, poster + `muted playsinline`. CTA sticky bas
recommandé. Tester 360/390/414 px.

### Très humain
Vrais visuels/portraits (assets créas) en hero et preuve ; texte 1re/2e personne, chaleureux ; visages et
témoignages réels plutôt que pictos. La 3D encadre l'humain, ne le remplace pas.

### Gestion des images (pièges vécus)
- Transparent → PNG (alpha préservé) ; ne JAMAIS aplatir en JPEG (halo gris/blanc sur dark).
- Fond intégré non transparent → régénérer en fond transparent/noir, ou carte assumée.
- Optimiser : opaques JPEG q≈82 ≤1600px ; transparents PNG. Page légère.
- Logos réels en post (jamais IA).
- HTML autonome (1 fichier, CSS inline). Pas de localStorage/sessionStorage. Accessibilité : `alt`, contrastes, sémantique.

## Auto-contrôle avant de passer au QA
Comparer explicitement à l'exemple d'or : « mon rendu est-il au niveau de `reference/example/` ? ». Puis
passer la main à `verification-web` (QA lourd).

## Livrable
`lp-[emetteur]-[cible].html` autonome + `assets/` branchés.

## GATE C4 (bloquante)
```
[ ] Page partie du template (pas de zéro), :root rempli (HEX réels)
[ ] 0 placeholder résiduel (@@…@@ / {{…}} / [[…]] / ${…})
[ ] Co-branding : cible visible nav + bande + footer ; accent cible repris par section
[ ] Logos branchés depuis assets/ avec fallback (pas d'image cassée)
[ ] Créas humaines en hero + preuve (ou fallback animé assumé)
[ ] 1 seul CTA, lien réel (ou # signalé), responsive + reduced-motion
```
Case vide → STOP. Puis QA final `verification-web`.
