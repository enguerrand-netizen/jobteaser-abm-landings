# DESIGN-SYSTEM — LP ABM co-brandées (lp-rapprochement)

Règles productisées, tirées des pages réelles (JobTeaser × Bulldozer / × Sanofi). On part TOUJOURS de
`reference/template.html` (structure + CSS + JS prêts) et on remplit `:root` + les `{{PLACEHOLDERS}}`.
Exemple d'or : `reference/example/lp-jobteaser-sanofi.html`.

## 1. Theming — algorithme des tokens `:root`
1. **MODE** = charte de l'ÉMETTEUR. Base claire + sections dark (hero/preuve/final/footer) pour un émetteur
   au style dark éditorial (ex. JobTeaser : fond `#1A191C` + accent vif).
2. **Neutres** : `--bg --surface --surface-2 --text --muted --line --dark --dark-2`.
3. **`--brand`** = signature ÉMETTEUR ; **`--accent`** = signature CIBLE (HEX RÉELS des brandbooks). Si les
   deux sont trop proches en teinte → décaler l'accent.
4. **`--brand-ink`** = texte lisible SUR le bouton `--brand`. `--brand-hi` = hover.
5. **⭐ `--accent-ink` = texte/logos lisibles SUR l'accent (règle de luminance, CRUCIALE).**
   - Calculer la luminance de `--accent` : `L = 0.299R + 0.587G + 0.114B` (ou simple moyenne).
   - **Accent CLAIR** (L ≳ 150, ex. lime `#DDFF56`) → `--accent-ink:#1A191C` (texte/logos FONCÉS sur l'accent).
   - **Accent FONCÉ** (L ≲ 150, ex. violet Sanofi `#7A00E6`) → `--accent-ink:#FFFFFF` (texte/logos BLANCS).
   - Partout où le fond est `--accent` (carte « POUR VOUS », bande co-brandée, surlignage `.acc`) : couleur
     texte = `--accent-ink`, et **utiliser la variante de logo cible correspondante** (foncée si accent clair,
     blanche si accent foncé). C'est ce qui casse si on ne fait que changer la couleur.
6. **Polices** = charte ÉMETTEUR (la page est émetteur-led) + fallbacks OFFICIELS, jamais « de mémoire ».
   JobTeaser : `Space Grotesk` (display, fallback approuvé de PolySans) + `Plus Jakarta Sans` (corps).

## 2. Structure (déjà dans le template)
1. **Nav** sticky — lockup co-brandé `[émetteur] × [cible]` (logos FONCÉS sur nav claire) + CTA → `#contact`.
2. **Hero** — composition « ad » de l'émetteur (voir §3) sur fond **motion vidéo** ; lockup sur plaque + carte
   « POUR VOUS » ; H1 nominatif, sous-titre = la thèse, 2 CTA, trust-row (3 chiffres).
3. **Pourquoi [cible], pourquoi maintenant** — signaux RÉELS sourcés (4 cartes `.sig` : fait + libellé + source/date).
4. **Ce que [cible] obtient** — ≥ 4 `.val` (tag + titre + bénéfice « vous obtenez »), chaque carte avec une créa.
5. **Preuve** (dark) — compteurs animés (5M / 800+ / 250k+ / 10), **mur de logos écoles/clients réels**, ≥1 témoignage.
6. **Bande co-brandée** pleine largeur (fond `--accent`, texte `--accent-ink`, logos variante adaptée).
7. **Comment on démarre** — 3 étapes rassurantes.
8. **Rencontrez [Commercial]** (`#contact`) — section HUMAINE (voir §4).
9. **Footer** — lockup co-brandé (dark → logos blancs).

## 3. Hero « ad » émetteur (composition)
Reproduire la mise en page pub signature de l'émetteur (JobTeaser : talent dans un **cercle vert**, entouré de
**vraies cartes-logos d'écoles**, **flèches montantes** vert + accent 2ndaire, sur fond motion). Assemblé en
HTML/CSS (photo en cercle + cartes `position:absolute` + SVG flèches), jamais en un seul rendu IA.
**Ultra-perso obligatoire** : carte « POUR VOUS · [émetteur] × [cible] » visible.

## 4. Section humaine « Rencontrez [Commercial] » (recommandée, = `#contact`)
Plus humain et meilleure conversion qu'un mailto. Bloc `.rep` :
- **Photo RÉELLE** du commercial (jamais IA) — `assets/[prenom]-[nom].jpg`, cerclée aux 2 accents
  (`box-shadow:0 0 0 4px var(--brand),0 0 0 8px [accent]`). **Fallback initiales** via `onerror` (jamais cassé).
- Nom, rôle, **message à la 1re personne** (« Bonjour, je suis … »).
- **Calendly** (CTA principal, `target="_blank" rel="noopener"`) + **téléphone** (`tel:+33…`) + email.
- Nav / hero / CTA sticky mobile pointent vers `#contact`.

## 5. Co-branding — la cible TOUJOURS visible ET lisible
Lockup `[émetteur] × [cible]` en **nav + hero + bande + footer** + carte « POUR VOUS ». Logos = vrais fichiers,
3 variantes via `logo-resolver/normalize_logo.py` : **foncée** (fonds clairs), **blanche** (fonds sombres),
et sur l'accent selon `--accent-ink`. **Logo sur vidéo/photo = sur plaque solide** (pill sombre + blur, ou carte
de couleur). Contrôle : `verification-web/audit_logos.js` (figer une frame vidéo claire).

## 6. Effet & robustesse
Motion vidéo de fond (mint émetteur × accent cible, sans personne) + reveals (IntersectionObserver) + compteurs
(avec filet `setTimeout`) + hovers. Toujours : `poster`, `prefers-reduced-motion` (masque la vidéo), pause
hors-écran. Mobile-first (1 colonne, CTA sticky, 0 scroll horizontal, tap ≥ 44px). HTML autonome, `alt`, contrastes AA.

## 7. Reproductibilité (émetteur 1× / cible N×)
Kit ÉMETTEUR (logos + variantes + logos écoles `assets/proof/` + brandbook + motion) réutilisé pour toutes les
cibles ; par cible on ne change que : `--accent` (+`--accent-ink`), logos cible, copie (signaux/thèse/value props),
créas sectorielles, et la section commercial. Passer les gates via `abm-process-gate/check_process.py` +
`verification-web/check_lp.py`.
