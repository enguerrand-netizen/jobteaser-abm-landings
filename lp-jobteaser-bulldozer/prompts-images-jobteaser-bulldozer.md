# Prompts images — LP JobTeaser × Bulldozer

> Créas calées sur la CIBLE (Bulldozer), lumière/accents co-brandés : **rim light vert JobTeaser `#5BFF77`** + **glow lime Bulldozer `#DDFF56`**, fond ink `#1A191C`/`#000`.
> Négatifs communs : `no distorted hands, no text artifacts, no watermark, no stock cliché, no fake brand logos`.
> ⚠️ **Aucun logo dans le prompt** — logos JobTeaser & Bulldozer ajoutés EN POST (overlay HTML). Univers = agence growth/marketing IA (écrans, dashboards, open space créatif, jeunes talents en action).

---

## Famille A — Humain mis en scène dans l'univers Bulldozer (IMAGE)

**A1 — HERO 16:9**
> Editorial photoreal wide shot, a young diverse growth-marketing team in a bright modern creative agency open space, late-20s talents collaborating around large screens showing analytics dashboards and AI tools, laptops and sticky notes, energetic focused mood, shallow depth of field, cinematic. Cool daylight with a subtle **mint-green `#5BFF77` rim light** on hair/shoulders and a soft **lime `#DDFF56` glow** from a screen. Dark editorial background `#1A191C`. Premium, authentic, not corporate stock. 16:9.

**A2 — Portrait 4:5**
> Photoreal editorial portrait of a young graduate (early career, ~24, confident, casual-smart), working on a laptop with marketing dashboards, in a modern agency, shallow depth of field, **mint-green `#5BFF77` rim light**, dark background, subtle lime accent. Authentic, warm, aspirational. 4:5.

**A3 — Scène 4:5**
> Photoreal candid scene, two young talents (diverse) reviewing a growth campaign on a wall screen in a dark creative studio, **lime `#DDFF56`** UI glow on their faces + **mint `#5BFF77`** back rim light, editorial, shallow DoF. 4:5.

---

## Famille B — Motion fond de hero (VIDEO) — sans personne (Veo-safe)
> Abstract 3D loop, flowing particles and light streaks in **mint-green `#5BFF77`** and **lime `#DDFF56`** over deep black `#000`, evoking data flow / talent network connecting nodes (campus dots linking to a company hub), smooth premium, seamless loop, no text, no people. 16:9.

**Repli si Studio/Veo indisponible → motion CSS/canvas** (particules + réseau de nœuds animés, mêmes couleurs). Réalisable sans génération.

---

## Famille C — Illustrations / mockups outils (IMAGE ou SVG)
**C1 — Mockup "talent match" 16:9**
> Flat premium UI illustration of a talent-matching interface: candidate cards (young graduates) flowing into a "matched" column, school badges, AI-match score, in **mint `#5BFF77`** + **ink `#1A191C`** on off-white, clean, no real logos, no lorem text. 16:9.

**C2 — Schéma écosystème 16:9**
> Flat illustration: a network diagram linking "800+ écoles" nodes to a central company hub, European map hint, **mint-green** links, **lime** company node, minimal, premium flat. 16:9.

**Repli → SVG flat** (réalisable directement en code, on-brand, sans génération IA).

---

## Statut génération (FINAL — via Bulldozer Studio)
Plugin Bulldozer autorisé → tout généré via `bdzCreateStudioJob`, rapatrié en dur dans `assets/` (egress S3 ouvert).

**Vraies images émetteur récupérées** (`assets/emetteur/`) et utilisées comme **`referenceUrls`** de style :
- `jt-og-default.jpg` (og:image officielle) — décode le langage JobTeaser : fond noir, vert + **accent violet**, **flèches montantes**, line-art géométrique.
- `jt-team-adrien-nicolas.png` (fondateurs) — cartes blanches à **ombre verte décalée** + motifs flèches vert→violet.

**Famille A — photos humaines (IMAGE)** ✅ : `hero-bulldozer.jpg`, `portrait-bulldozer.jpg`, `scene-bulldozer.jpg`.
**Famille B — motion (VIDEO/Veo)** ✅ : `motion-hero.mp4` (8 s, loop abstrait mint × lime, sans personne) + `motion-hero-poster.png`. Câblée en fond de hero (`autoplay muted loop playsinline`, reduced-motion + pause hors-écran).
**Famille C — illustrations (IMAGE)** ✅ : `illus-talentmatch.jpg` + `illus-ecosysteme.jpg`, régénérées avec `referenceUrls` = og:image JobTeaser → reprennent flèches + accent violet + cartes à ombre verte, avec highlight **lime Bulldozer**.
