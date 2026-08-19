---
name: logo-resolver
description: >-
  Utilitaire réutilisable : à partir d'un nom de marque / domaine, ramène un FICHIER logo local dans
  assets/, selon l'échelle officiel → rehost → banque (Clearbit/Brandfetch) → recréation SVG fidèle.
  Jamais de logo généré par IA. Renvoie le fichier + le NIVEAU atteint (pour les gates). Appelé par
  emetteur-brand-kit, cible-brand-kit et cible-creas. Déclencher sur "récupère le logo de [marque]",
  "logo officiel de [X] en fichier", ou depuis une skill amont.
---

# logo-resolver — Résolution de logo en FICHIER (utilitaire)

But : ne jamais laisser un logo « en simple texte » ni le faire générer par IA. Toujours produire un
fichier dans `assets/`, en descendant l'échelle jusqu'au premier niveau atteignable, et en le signalant.

## Il résout TROIS jeux de logos (appels distincts)
1. **Logo ÉMETTEUR** (pour emetteur-brand-kit) → `assets/logo-emetteur.*`.
2. **Logo CIBLE** (pour cible-brand-kit) → `assets/logo-[cible].*`.
3. **Logos de RÉASSURANCE** = clients/écosystème de l'émetteur, filtrés sur le SECTEUR de la cible
   (pour la bande « ils recrutent déjà avec [émetteur] ») → `assets/proof/logo-[client].*` (batch).
Aucun des trois ne doit rester en simple texte si un fichier est obtenable.

## PRÉREQUIS EGRESS — tester AVANT, ne pas échouer en silence
Récupérer un fichier officiel = requête réseau sortante. Le sandbox a une **allowlist** : S3
(`bdz-saas.s3…`) et les CDN de marque (`*.jobteasercdn.com`, `cloudfront.net`, sites de marque) sont
souvent **bloqués** (`X-Proxy-Error: blocked-by-allowlist`).
1. **Tester la connectivité** de chaque domaine cible (`curl -sI`), CONSIGNER lesquels sont bloqués.
2. Domaine ouvert → télécharger + rehéberger dans `assets/` (niveau *officiel*/*rehost*).
3. Domaine bloqué → NE PAS abandonner en silence : soit demander à l'utilisateur d'ajouter le domaine à
   l'egress (idéal), soit lui faire déposer le fichier, soit descendre au niveau *banque* puis *svg_recree*.
4. Toujours DIRE dans le rapport : « logo X = niveau atteint (officiel/rehost/banque/svg_recree), domaine
   testé = ouvert/bloqué ». C'est ce qui manquait : le logo « pas récupéré » vient de l'egress, pas d'un oubli.

## Échelle (s'arrêter au 1er niveau fiable)
1. **Fichier officiel fourni par l'utilisateur** (SVG/PNG déposé dans `assets/`). ← à privilégier/demander.
2. **Fichier officiel du site de la marque** (page presse / brand kit / `og:image` / favicon HD) → SVG > PNG HD,
   **rehébergé** dans `assets/` (ne pas hotlinker en prod).
   - ⭐ **SVG inline** : beaucoup de sites (ex. Sanofi) rendent leur logo en `<svg>` inline (pas un fichier).
     Le capturer via le navigateur : repérer le `<svg aria-label="[marque]">` (souvent un viewBox type `0 0 80 22`),
     nettoyer les classes framework, ajouter `xmlns`, et sauver le `outerHTML` en `assets/logo-[marque].svg`.
     C'est du niveau *officiel* (vrai tracé de marque), pas une recréation.
3. **Banque de logos** : `logo.clearbit.com/<domaine>`, Brandfetch → à SIGNALER, à TESTER (peut casser).
4. **Recréation SVG fidèle** : wordmark typographique simple reproduit aux HEX réels de la charte
   (police officielle ou fallback officiel). Uniquement pour logos typographiques simples, et SIGNALÉ.
   → jamais pour un logo figuratif complexe (risque de faux).

## Variantes de couleur (fond clair ET sombre) — OBLIGATOIRE
Un logo est utilisé sur plusieurs fonds (nav claire, hero sombre, bande de couleur). Il faut donc en
produire les variantes **lisibles sur chaque fond**. ⚠️ Piège vécu : beaucoup de SVG ont `fill="white"`
(ou "black"/"currentColor") **codé sur chaque path** → changer le `fill` de la seule balise `<svg>` est
IGNORÉ, le logo reste invisible sur le mauvais fond.
→ Utiliser `scripts/normalize_logo.py` qui recolore AU NIVEAU DES PATHS :
```
python3 scripts/normalize_logo.py logo.svg --check                         # inspecter la palette
python3 scripts/normalize_logo.py logo.svg --mode dark  --keep '#ACCENT' -o logo-dark.svg   # fond CLAIR
python3 scripts/normalize_logo.py logo.svg --mode white --keep '#ACCENT' -o logo-white.svg  # fond SOMBRE
```
`--keep` préserve la/les couleur(s) d'accent de la marque (le reste passe en foncé/blanc). Livrer au
minimum la variante foncée + la variante blanche, et **vérifier le contraste réel** (voir verification-web
`audit_logos.js`) : un logo sur une vidéo doit en plus être posé sur une plaque solide.

## Interdits
- Jamais de logo généré par IA (rendus faux type « Rache » pour Roche).
- Jamais un logo détouré aplati en JPEG (halo) → transparent = PNG (alpha préservé).

## Contrainte egress (sandbox)
Le téléchargement direct (S3 / domaines de marque) peut être bloqué par l'allowlist. Alors :
- demander à l'utilisateur de déposer le fichier, OU
- rehéberger via un pont serveur (Bulldozer hosting/fridge) si dispo, OU
- descendre au niveau 4 (SVG recréé) en le signalant.

## Sortie
`assets/logo-[marque].{svg|png}` + `niveau` ∈ {officiel, rehost, banque, svg_recree} + note de confiance.
Le niveau alimente les gates des skills appelantes (une gate « stricte » peut refuser < officiel).
