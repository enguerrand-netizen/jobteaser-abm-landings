# Brandbook cible — Sanofi

> Kit de marque du PROSPECT pour co-brander la LP ABM **JobTeaser → Sanofi**.
> Données sourcées des styles calculés live de sanofi.com + logo officiel (SVG inline capturé). Aucune invention.

## 1. Couleurs (HEX) — sourcées (styles calculés live, juillet 2026)
| Rôle | HEX | Source / fréquence |
|------|-----|--------------------|
| **Violet signature (accent)** | `#7A00E6` | `rgb(122,0,230)` — boutons (7×) + fonds de section (7×) + points du logo. Signature Sanofi. |
| Bleu secondaire | `#3860BE` | boutons/liens secondaires |
| Slate foncé | `#27455C` | fonds de sections sombres |
| Ink / texte | `#171717` | couleur de texte principale |
| Blanc | `#FFFFFF` | fond principal |
| Gris clair | `#EFEFEF` / `#F5F5F5` | surfaces secondaires |

**Combo signature Sanofi** : blanc + violet `#7A00E6` vif, ou slate `#27455C` + violet en accent.

## 2. Typographie — sourcée
- **Titres + corps** : `Sanofi Sans` (police propriétaire) → fallback réel du site : **Work Sans** (Google Fonts), puis Raleway / Roboto.
- Pour l'assemblage : utiliser **Work Sans** (fallback officiel de leur propre CSS), pas une police « proche » devinée.

## 3. Do / Don't visuels
**DO** — épuré, blanc dominant, violet `#7A00E6` en accent franc (boutons, points, soulignés), photos humaines/science, slate pour les blocs sombres.
**DON'T** — pas de violet délavé, pas de dégradés criards ; logo jamais recréé/IA (fichier officiel dispo).

## 4. Logo cible (fichiers présents — niveau : OFFICIEL)
- `assets/logo-sanofi.svg` — wordmark officiel (lettres noires + 2 points violets `#7A00E6`), capturé du SVG inline live du site.
- `assets/logo-sanofi-white.svg` — variante blanche (points violets préservés) pour fonds sombres, générée via `normalize_logo.py`.
- Source : sanofi.com (SVG inline `aria-label="Sanofi"`, viewBox 0 0 80 22).

## 5. Lisibilité de l'accent sur la page
- `#7A00E6` violet : excellent contraste sur blanc ET sur slate/dark → utilisable en texte accent, boutons, aplats, lockup.
- LP JobTeaser-led (fond dark hero + sections claires) : le violet Sanofi ressort très bien.

## Co-branding (note pour l'assemblage)
- Émetteur JobTeaser accent = `#5BFF77` (vert mint) ; cible Sanofi accent = `#7A00E6` (violet). **Vert × violet = contraste fort et complémentaire** — lockup co-brandé très lisible.
- Hiérarchie : marque JobTeaser dominante (émetteur), Sanofi présent en co-branding (nav lockup, carte « POUR VOUS », bande, footer), accent violet repris par section.

## Source
- https://www.sanofi.com/en (styles calculés live + SVG logo inline)
