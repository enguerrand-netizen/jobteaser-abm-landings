# Brandbook cible — Bulldozer

> Kit de marque du PROSPECT pour co-brander la LP ABM **JobTeaser → Bulldozer**.
> Données sourcées des styles calculés live de bulldozer-collective.com + fichiers logo officiels. Aucune invention.

## 1. Couleurs (HEX) — sourcées (styles calculés live, juillet 2026)

| Rôle | HEX | Source / fréquence |
|------|-----|--------------------|
| **Lime signature (accent)** | `#DDFF56` | `rgb(221,255,86)` — boutons (9×) + fonds de section (10×) + fill du logo. Signature de Bulldozer. |
| Lime translucide (déco) | `rgba(221,255,86,0.2)` | fonds de blocs accent |
| **Ink / titres** | `#0E0E0E` | couleur des h1/h2 |
| Texte courant | `#141414` | `rgb(20,20,20)` — couleur texte la plus fréquente (1357×) |
| Noir sections | `#000000` | 61 fonds de section (usage dark massif) |
| Olive foncé (logo) | `#1F2600` | fill du picto officiel |
| Gris clair | `#F7F7F7` | boutons/cartes secondaires |
| Gris clair 2 | `#F5F5F5` | fonds |
| Blanc | `#FFFFFF` | fond principal |

**Combo signature Bulldozer** : fond noir `#000000` + accent lime `#DDFF56` + texte blanc. Même logique dark+accent-vif que JobTeaser.

## 2. Typographie — sourcée
- **Titres + corps** : `Pressura` (GT Pressura, grotesque à empattements techniques / mono-influence), fallback `sans-serif`.
- Fallback si Pressura indisponible (licence commerciale) : une grotesque technique proche (Space Grotesk / Suisse Int'l) — à signaler dans l'assemblage.

## 3. Do / Don't visuels
**DO** — flat, contraste fort noir/blanc, accent lime `#DDFF56` en aplat vif, coins arrondis (picto = carré très arrondi), sections dark `#000` + accent lime.
**DON'T** — pas de dégradés, pas de lime en petit texte (illisible), pas de logo recréé/IA.

## 4. Logo cible (fichiers présents — niveau : OFFICIEL)
- `assets/logo-bulldozer.svg` — picto officiel (carré arrondi 40×40). Fills : `#1F2600` + `#DDFF56`.
- `assets/logo-bulldozer-wordmark.svg` — wordmark "Bulldozer Collective" officiel (1272×484, paths sans fill → rendu noir/currentColor ; prévoir variante blanche sur fond dark via `filter: invert()` ou `currentColor`).
- Source : `cdn.prod.website-files.com` (CDN Webflow officiel de Bulldozer).

## 5. Lisibilité de l'accent sur la page
- La LP est **JobTeaser-led** : mode majoritaire clair + sections dark JobTeaser (`#1A191C`).
- `#DDFF56` sur fond noir/dark = **excellent contraste** → OK en aplat, badges, soulignés, lockup co-brandé.
- `#DDFF56` en **texte sur blanc = illisible** → **usage aplat/déco uniquement**, jamais en texte courant. (noté)

## Co-branding (note pour l'assemblage)
- Émetteur JobTeaser accent = `#5BFF77` (mint) ; cible Bulldozer accent = `#DDFF56` (lime-jaune). Deux verts vifs sur noir, très compatibles esthétiquement et suffisamment distincts pour un lockup à deux marques.
- Hiérarchie : marque JobTeaser dominante (émetteur), Bulldozer présent en co-branding (nav lockup « JobTeaser × Bulldozer », bande, footer).

## Source
- https://www.bulldozer-collective.com (styles calculés live)
- CDN officiel : cdn.prod.website-files.com (Webflow)
