---
name: verification-web
description: >
  Vérifie et propose des améliorations pour une landing page / page web HTML produite par une autre
  skill (ex. lp-rapprochement) AVANT livraison. Lance un checker statique automatique (bugs récurrents :
  placeholders laissés, logos via API tierce cassés, CTA mort, assets manquants, couleurs non sourcées,
  accessibilité, poids), fait une revue visuelle par screenshot, produit un rapport noté /100 avec les
  correctifs priorisés, et applique les corrections sûres. Déclencher quand l'utilisateur dit : "vérifie
  cette landing", "audite la page", "check la LP", "y a trop de bugs", "qu'est-ce qui cloche sur la page",
  "propose des améliorations", "relis la landing avant envoi", "valide la page", ou juste après avoir
  produit une page web (auto-QA). Ne pas confondre avec relecture-code (projets de code) ni
  audit-website-cro (optimisation conversion d'un site en ligne) : ici on VÉRIFIE la QUALITÉ TECHNIQUE +
  VISUELLE d'un fichier HTML livrable et on liste les bugs à corriger.
---

# Vérification & amélioration d'une page web (QA livrable)

## Objectif
Empêcher qu'un livrable HTML parte avec des bugs. La skill combine un **contrôle automatique** (script)
et une **revue visuelle** (screenshot), produit un **rapport noté** avec correctifs priorisés, puis
**corrige** ce qui est sûr. Elle est seedée avec les pannes réellement vécues (placeholders « à sourcer »,
jaune « de mémoire », logos Clearbit cassés, halo gris sur PNG aplati en JPEG, CTA en `#`).

## Workflow

### 1. Contrôle automatique (obligatoire)
Lancer le checker avec le MAXIMUM de contexte (marques + couleurs attendues) :
```
python3 scripts/check_lp.py page.html \
   --assets-dir DOSSIER_ASSETS \
   --emetteur "Bulldozer" --prospect "Sanofi" \
   --brand "#DDFF56" --accent "#7A00E6" \
   --font "GT Pressura" --flat --cta-required
```
- `--font "…"` : vérifie que la police de charte est bien dans le CSS (sinon police non appliquée).
- `--flat` : charte minimale/flat → signale tout **dégradé, ombre, blur, particule/3D** (interdits).
Il renvoie un **score /100**, les problèmes **classés par catégorie** (Contenu, Couleurs, Liens/CTA,
Assets, Accessibilité, Technique, Structure) et par sévérité (⛔ BLOCKER, 🔴 HIGH, 🟠 MED, 🟡 LOW, ℹ️ INFO),
plus un **VERDICT livrable OUI/NON** (code retour ≠ 0 s'il reste un BLOCKER/HIGH). ~30 contrôles :
- **Contenu** : `template_tokens` (`{{}}`/`[[]]`/`${}`), `lazy_placeholder` (à sourcer/à remplacer/de mémoire/
  TODO/lorem/à définir…), `js_artifact` (NaN/undefined/[object Object]), `thin_copy`, `repeated_text`,
  `stray_brand` (marque d'exemple du template restée), `missing_emetteur`/`missing_prospect`.
- **Couleurs** : **contraste WCAG calculé** texte/fond, texte secondaire, texte-bouton (`contrast_*`),
  `brand_missing`/`accent_missing` (couleur attendue absente), rappel `colors` (sourcing).
- **Liens/CTA** : `dead_cta` (`#`), `no_real_cta`, `broken_anchor`, `noopener`, `empty_link`.
- **Assets** : `missing_assets`, `logo_api` (Clearbit/Brandfetch→cassés), `mixed_content`, `remote_img`.
- **Accessibilité** : `html_lang`, `img_alt`, `no_h1`/`multi_h1`, `viewport`.
- **Charte** (avec `--font`/`--flat`) : `font_missing` (police charte non appliquée), `flat_gradient`,
  `flat_shadow`, `flat_blur`, `flat_particles` (éléments interdits par une charte flat).
- **Mobile / responsive (PRIORITÉ — mobile-first avant tout)** : `no_media_query` (BLOCKER : pas responsive),
  `few_breakpoints`, `fixed_width` (largeur px >480 sans max-width → débordement), `img_fluid`
  (images sans max-width:100%), `overflowx`, `no_sticky_cta`, `base_font` (<15px), `nowrap`.
- **Technique** : `reduced_motion`, `video_muted`/`playsinline`/`poster`, `storage`, `title`/`title_long`,
  `meta_desc`, `console_log`, `weight`.
- **Structure** : `thin_page`, `no_counters`, `bad_count`, `no_proof`, `no_visual`.

> **Mobile-first = priorité n°1.** Une page qui n'est pas irréprochable sur 360/390/414 px n'est PAS
> livrable, même parfaite sur desktop. Le check `no_media_query` est bloquant ; toujours faire aussi le
> screenshot mobile (étape 2). La charte forte de l'émetteur prime sur le style par défaut du template
> (police + do/don't : dégradés/ombres/glow interdits si la charte l'exige → utiliser `--flat`).

### 2. Revue visuelle (obligatoire — non automatisable)
Rendre la page et prendre un **screenshot desktop (1440px) + mobile (390px)**. Si aucun navigateur
headless n'est dispo : héberger (bulldozer-hosting) puis capturer via Claude-in-Chrome, OU décrire
précisément le rendu attendu bloc par bloc.
**Audit logos automatisé (dans le navigateur)** : coller `scripts/audit_logos.js` dans la console/
javascript_tool → il échantillonne les pixels de CHAQUE logo et le compare à son fond (foncé‑sur‑clair /
clair‑sur‑foncé), y compris sur média. Pour le pire cas vidéo : figer une frame CLAIRE (`video.currentTime`)
AVANT de lancer l'audit. Tout `⚠️ MÊME TON` ou `⚠️ SUR MÉDIA sans plaque` = à corriger (variante de couleur
via logo-resolver `normalize_logo.py`, ou plaque de fond solide). Puis vérifier aussi à l'œil :
- Hero lisible sur le fond animé (voile suffisant), pas de texte avalé par la vidéo.
- **Pas de halo gris** : un visuel détouré doit être un PNG transparent, jamais un JPEG aplati.
- **Logos réels visibles PARTOUT** : pas cassés (API), pas invisibles (logo noir sur fond noir → pastille claire).
  **Logo sur une vidéo/motion** : figer la vidéo sur une frame CLAIRE et vérifier qu'il reste lisible — sinon
  poser le logo sur une plaque/pill solide (fond sombre semi-opaque ou carte de couleur de marque). Auditer
  CHAQUE emplacement de logo (nav, hero, bande, footer, cartes) : taille rendue > 0 ET contraste suffisant.
- Couleurs = **vraies** couleurs de marque, contraste AA titre/texte/bouton.
- Mobile 360/390/414 : 1 colonne propre, CTA sticky, pas de scroll horizontal, tap targets ≥ 44px.

### 3. Rapport + propositions d'amélioration
Produire un rapport court :
- **Score** /100 (auto) + verdict (livrable OUI/NON).
- **Bugs** par sévérité, chacun avec sa **cause** et le **correctif proposé**.
- **Améliorations** (au-delà des bugs) : densité de preuve, hiérarchie, micro-interactions, perfs.
- Comparaison à l'exemple d'or de `lp-rapprochement/reference/example/` si applicable.

### 4. Corrections
- **Auto-fix les correctifs sûrs** : remplacer un CTA `#` par le lien fourni, poser un `alt`, ajouter
  viewport/reduced-motion, convertir un logo API en lockup/fichier, remplacer un placeholder par la
  donnée réelle **après l'avoir sourcée** (recherche web / charte / fichiers).
- **Ne jamais “corriger” en inventant** : si une preuve/logo manque, la SOURCER (recherche) ; à défaut,
  le signaler comme action à l'utilisateur — mais ne pas laisser un « à sourcer » dans le livrable final.
- Relancer le checker jusqu'à **0 bloquant / 0 HIGH**, puis re-screenshot.

## Règle d'autonomie (importante)
« À sourcer » n'est PAS une sortie acceptable. Pour un bandeau de logos clients, des chiffres, un
témoignage : **faire la recherche soi-même** (site de l'émetteur, presse, `WebSearch`/Exa, données
Bulldozer) et intégrer du réel. On ne délègue à l'utilisateur que ce qui est réellement introuvable,
et jamais sous forme de placeholder laissé dans la page.

## Garde-fous
- Le checker statique ne remplace pas l'œil : toujours faire la revue visuelle (étape 2).
- Ne pas marquer « livrable OUI » s'il reste un ⛔ ou un 🔴.
- Toute correction de contenu (chiffre, logo, témoignage) doit être sourcée, jamais inventée.
- Ne pas confondre avec relecture-code (code) ni audit-website-cro (CRO d'un site en ligne).
