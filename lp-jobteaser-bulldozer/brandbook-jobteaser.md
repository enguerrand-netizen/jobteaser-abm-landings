# Brandbook émetteur — JobTeaser

> Kit de marque réutilisable pour la LP ABM 1-to-1 **JobTeaser → Bulldozer**.
> Toutes les données sont sourcées (site officiel, design system "Spark", CDN JobTeaser, recherche web). Aucune invention.

## 1. Couleurs (HEX) — sourcées

Extraites des styles calculés du site officiel + design system interne **"Spark"** (`--sk-*` tokens) + fichiers logo officiels.

| Rôle | HEX | Note / source |
|------|-----|---------------|
| **Ink / primaire** | `#1A191C` | Couleur du wordmark officiel (fills SVG). Boutons UI en `#000000` pur (token `--sk-action-...-primary-default-light`). |
| **Vert signature (accent)** | `#5BFF77` | Couleur "Teasy" du logo + token `--sk-action-color-background-highlight-default`. Signature de la marque. |
| Vert accent — hover | `#52E66B` | `--sk-...-highlight-hover/focus` |
| Vert accent — active | `#49CC5F` | `--sk-...-highlight-active` |
| Slate (texte secondaire) | `#526E7A` | 2e couleur de texte la plus fréquente sur le site |
| Neutre foncé | `#323036` | échelle neutre Spark |
| Neutre moyen | `#7D7887` | échelle neutre Spark |
| Neutre clair | `#E5E4E7` | bordures / séparateurs |
| Fond off-white | `#F9F9FC` | fonds de sections |
| Blanc | `#FFFFFF` | fond principal |

**Combo signature** : fond noir `#1A191C` + accent vert `#5BFF77` + texte blanc. C'est LA signature JobTeaser (cf. logo "dark background").

## 2. Typographies — sourcées

- **Titres** : `PolySans` (font-family calculée : `polysans`). Grotesque géométrique, caractère fort.
- **Corps** : `Plus Jakarta Sans` (Google Fonts, dispo librement) + fallback `Helvetica, Arial, sans-serif`.
- Fallback titres si PolySans indisponible (licence) : `Plus Jakarta Sans` en gras, ou une grotesque proche (Space Grotesk).

## 3. Do / Don't visuels

**DO**
- Style flat, épuré, beaucoup de blanc/noir, accents verts ponctuels et francs.
- Coins arrondis modérés (boutons, cards).
- Contraste fort noir/blanc ; le vert `#5BFF77` en touche (CTA highlight, soulignés, pictos).
- Combo dark : sections fond `#1A191C` + titres blancs + accent vert.

**DON'T**
- Pas de dégradés criards, pas de glow, pas de multi-couleurs façon arc-en-ciel.
- Pas de vert délavé/pastel : rester sur le `#5BFF77` saturé.
- Pas de logo recréé/IA — utiliser les fichiers officiels ci-dessous.

## 4. Logos (fichiers présents — niveau : OFFICIEL)

- `assets/logo-emetteur.svg` — wordmark couleur (light background), officiel, nettoyé (artefact JSX retiré). Fills : `#1A191C` + `#5BFF77`.
- `assets/logo-emetteur-picto.svg` — picto "FY25" (carré arrondi), officiel. Fills : `#1D1D1B` + `#5BFF77`.
- Source : `static-assets.jobteasercdn.com` (CDN officiel JobTeaser).

## 5. Réassurance (trust signals) — sourcés

**Chiffres clés** (source : jobteaser.com/corporate/about-us, recherche web juillet 2026)
- **Leader européen** du recrutement & de l'orientation des jeunes talents (Gen Z).
- **800+ écoles & universités** partenaires en Europe.
- **5 millions** d'étudiants & jeunes diplômés sur la plateforme.
- **250 000+** recruteurs utilisent JobTeaser.
- **10 pays** européens avec partenariats écoles exclusifs.
- Fondée en **2009**.
- Produit IA : **TalentMatch** — matching automatique offres ↔ candidats jeunes diplômés.

**Écosystème écoles/universités — LOGOS FICHIERS (réels, via CDN JobTeaser)** — `assets/proof/school-01..10.png`
Identifiés : **3iL Ingénieurs** (school-01), **AgroParisTech** (school-09), **3W Academy** (school-02), **AAMS – Aarhus School of Marine and Technical Engineering** (school-05, Danemark → preuve empreinte européenne). + 6 autres logos écoles réels non nominalement identifiés (affichés en mur, comme sur le site JobTeaser).
> C'est la réassurance signature de JobTeaser : le réseau d'écoles. Substitue de façon assumée les "logos clients du secteur du prospect" — Bulldozer étant une agence growth boutique sans secteur-client clairement mappable dans le roster JobTeaser. Dégradation signalée (non muette).

**Témoignage nominatif** (source : jobteaser.com/corporate/about-us)
- **ESCP Business School** : « JobTeaser is unique in its ability to offer our students a wide range of internships and job opportunities. » — représentant ESCP.

## 6. Value props (reformulées côté prospect = Bulldozer)

Angle : permettre à Bulldozer de recruter ses futurs talents junior (growth / marketing / sales / tech) via JobTeaser.

1. **Accédez à 5M de jeunes talents** — étudiants & jeunes diplômés actifs sur la plateforme, dont les profils growth/marketing/tech que recrute une agence comme Bulldozer.
2. **Recrutez dans 800+ écoles & universités** — dont écoles de commerce, d'ingénieurs et académies tech (3W Academy, 3iL Ingénieurs…) directement dans votre vivier.
3. **Laissez l'IA trouver les bons profils** — TalentMatch analyse vos offres et remonte automatiquement les candidats les plus pertinents. Moins de temps de sourcing.
4. **Marque employeur intégrée** — page entreprise dédiée visible auprès des étudiants, diffusion d'offres illimitée, candidature simplifiée.
5. **Le réseau des écoles vient à vous** — workshops, événements carrière et orientation gérés par les établissements = accès privilégié aux talents avant le marché ouvert.
6. **Leader européen, éprouvé** — 250 000+ recruteurs, 10 pays, depuis 2009. Un canal de recrutement junior déjà validé à grande échelle.

## Sources
- https://www.jobteaser.com/en/corporate/about-us
- https://www.jobteaser.com/fr/corporate/recruiters
- https://www.jobteaser.com/en/corporate/our-network-of-schools-and-universities
- https://www.jobteaser.com/fr/corporate/recrutement-jeune-diplome
- https://en.wikipedia.org/wiki/JobTeaser
- Design system interne "Spark" (`--sk-*` CSS custom properties, styles calculés live)
- CDN officiel : static-assets.jobteasercdn.com
