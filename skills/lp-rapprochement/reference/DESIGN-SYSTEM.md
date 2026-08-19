# Design-system — lp-rapprochement

Le rendu premium NE dépend PAS de l'inspiration : il dépend de ces tokens + de l'algorithme de theming.
On part TOUJOURS de `template.html` et on remplit `:root`. On ne code pas une page de zéro.

## 1. Tokens (déjà dans template.html)
- Rayons : `--radius:20px`, `--radius-sm:14px`.
- Espacement : `--s1..--s6` = 8 / 16 / 24 / 40 / 72 / 96 px. Sections = `--s6`.
- Type : `--font-display` (titres) + `--font-body` (corps) = polices RÉELLES de l'émetteur (PHASE 1),
  fallback système. Titres `clamp()` déjà réglés.
- Couleurs : `--bg --surface --text --muted --line` (neutres) + `--brand`/`--brand-ink`/`--brand-hi`
  (émetteur) + `--accent`/`--accent-soft` (prospect).

## 2. Algorithme de theming (PHASE 5bis) — le point le plus important
But : que la page soit belle quelle que soit la marque, y compris marques claires.

1. **Choisir le MODE depuis l'émetteur :**
   - Marque à dominante sombre / forte perso dark (ex. noir, bleu nuit) → **MODE DARK**.
   - Marque claire / corporate lumineuse (blanc, pastel) → **MODE LIGHT**.
   - En cas de doute : DARK si `--brand` est vif/saturé (il ressort mieux sur fond noir), sinon LIGHT.
2. **Poser les neutres du mode :**
   - DARK : `--bg:#0A0A0A; --surface:#141416; --text:#FFFFFF; --muted:#A7ADB5; --line:#242428`.
   - LIGHT: `--bg:#FFFFFF; --surface:#F5F6F8; --text:#101014; --muted:#5A5F6B; --line:#E6E8EC`.
3. **Mapper les marques :**
   - `--brand` = couleur signature de l'ÉMETTEUR (boutons, highlight du titre, num d'étapes, chiffres).
   - `--accent` = couleur signature du PROSPECT (kicker, points `.dot`, halos, focus).
   - Si les deux couleurs sont trop proches → décaler l'accent en teinte/luminosité pour les distinguer.
4. **Garantir le contraste (AA) :**
   - `--brand-ink` = texte SUR le bouton brand : `#04110A`/noir si `--brand` est clair/vif, `#FFFFFF` si `--brand` est foncé.
   - Vérifier titre/texte sur `--bg` ≥ 4.5:1 ; boutons lisibles. Si un accent est illisible en texte, ne l'utiliser qu'en aplat/déco.
   - `--brand-hi` = `--brand` éclairci ~12 % (hover). `--accent-soft` = accent très désaturé pour fonds.
5. **Ne jamais** utiliser une couleur « de mémoire » : toutes viennent de PHASE 1 (brand-extractor / site).

## 3. Fallback visuel premium (si pas de photos en PHASE 4)
Une page sans photo doit RESTER belle. Dans l'ordre :
1. **Vidéo motion générée** (rendu local type points/particules aux 2 couleurs) en fond de hero.
2. Sinon **canvas/Three.js** (particules + halos bi-couleur).
3. Sinon **fond gradient animé CSS** : dégradés `--brand`↔`--accent` en mouvement lent + grain.
Jamais un aplat statique. Le hero ne doit jamais être « vide ».

## 4. Composants fournis (dans template.html)
nav co-brandée · hero (fond animé + voile + colonne centrée) · why-now (grille signaux) ·
valeur (grille ≥3) · preuve (bandeau logos + 4 compteurs + témoignage) · étapes · FAQ · CTA final ·
footer co-brandé · barre de progression · reveals au scroll · compteurs · CTA mobile sticky · responsive complet.

## 5. Exemple d'or (niveau à atteindre)
`example/lp-jobteaser-sanofi.html` = la référence validée (JobTeaser noir/vert × Sanofi violet).
Avant de livrer, comparer son rendu au tien : même densité de preuve, même soin d'animation, même
lisibilité du hero. Si le tien est en-dessous → itérer (PHASE 6bis).

## 6. Copywriting — gabarits à trous
- Hero H1 : « [Verbe d'action] les [cible du prospect] qui [bénéfice/mission] » + accent sur 2-3 mots.
- Sous-titre (thèse) : « [Signal prospect] a créé [X]. Chez [émetteur], on [bénéfice concret pour vous]. »
- Signal (why-now) : titre = le fait ; texte = « donc [opportunité pour le prospect] ».
- Valeur : titre = bénéfice côté prospect ; texte = comment, sans jargon.
- Toujours 2e personne (« vous »), phrases courtes, zéro superlatif creux.
