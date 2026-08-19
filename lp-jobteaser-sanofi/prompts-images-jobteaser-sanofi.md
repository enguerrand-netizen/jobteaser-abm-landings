# Prompts images — LP JobTeaser × Sanofi

> Co-brand : accent émetteur **mint #5BFF77** × accent cible **violet Sanofi #7A00E6**, fond ink #1A191C.
> Négatifs communs : `no distorted hands, no text artifacts, no watermark, no stock cliché, no fake brand logos`.
> Logos ajoutés EN POST (overlay HTML), jamais dans le prompt. Vraies images émetteur JobTeaser en `referenceUrls`.

## Famille A — Humain (IMAGE) — contexte pharma / santé / science
- **hero-person.jpg** (talent seul, fond gris clair détourable pour le cercle) : jeune ~24, smart-casual, laptop, rim mint + glow violet.
- **portrait-sanofi.jpg** (4:5) : jeune diplômé en environnement R&D / health-tech, dashboards data, rim mint + glow violet.
- **scene-sanofi.jpg** (4:5) : 2 jeunes talents analysant des données moléculaires/protéines sur écran en labo biopharma, glow violet + rim mint.

## Famille B — Motion (VIDEO / Veo, sans personne)
- **motion-hero.mp4** (8 s, loop) : particules + filaments ADN/molécules + streaks en **mint #5BFF77 × violet #7A00E6** sur near-black, réseau de nœuds science/data → hub entreprise. Câblé en fond de hero (autoplay muted loop playsinline, poster, reduced-motion, pause hors-écran). Lockup 2 logos sur plaque au-dessus.

## Famille C — Illustrations (IMAGE, style JobTeaser réel via referenceUrls og:image)
- **illus-ecosysteme.jpg** (16:9) : carte Europe, nœuds écoles verts → hub central **violet #7A00E6**, flèches montantes.
- **illus-talentmatch.jpg** (16:9) : cartes candidats + jauges de match, flux vers carte « matched », mint + accent violet, flèches, cartes à ombre verte.

## Statut génération (FINAL)
Tout généré via Bulldozer Studio (`bdzCreateStudioJob`), rapatrié en dur dans `assets/` (egress S3 ouvert).
`referenceUrls` illustrations = og:image officielle JobTeaser (langage visuel : noir + vert + violet + flèches + cartes à ombre verte).
