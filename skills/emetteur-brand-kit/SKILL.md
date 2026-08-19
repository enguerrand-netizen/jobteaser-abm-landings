---
name: emetteur-brand-kit
description: >-
  Construit le KIT DE MARQUE de l'ÉMETTEUR et récupère ses vrais éléments graphiques sur son site :
  charte (HEX/typo/do-don't), logo officiel (via logo-resolver), créas/motifs/photos réutilisables, et
  preuves de réassurance (chiffres, logos clients par secteur, écosystème/partenaires/écoles, témoignages,
  labels). Produit un brandbook émetteur réutilisable sur TOUTES les cibles. Déclencher depuis
  l'orchestrateur lp-rapprochement, ou sur "récupère la charte et les assets de [émetteur]",
  "brandbook émetteur", "éléments graphiques du site de [client]". S'exécute UNE fois par émetteur.
---

# emetteur-brand-kit — Kit de marque + assets de l'ÉMETTEUR (×1, réutilisable)

But : que la landing ressemble au client, pas à un template. On récupère du RÉEL. Anti-invention absolu.

## 1. Charte émetteur (ex-PHASE 1, volet émetteur)
Couleurs HEX exactes (dominante + accents), par ordre de fiabilité :
1. Skill `brand-extractor` si dispo.
2. Navigateur (Chrome) : styles calculés + variables CSS, couleur des boutons/CTA, `<meta name="theme-color">`, fonds header/footer.
3. Brandbook public / page « presse & médias » / kit de marque.
4. Exa/HTML : `meta theme-color`, backgrounds, classes de boutons.
Typographies (titres + corps) + source (Google Fonts…).
**Do/don't visuels** : formes (arrondi vs carré), ombres/dégradés/glow autorisés ou INTERDITS, motifs,
style photo, ton (flat vs riche). Ces règles conditionnent l'assemblage. Vérifier les contrastes réels.
Si doute sur une couleur → NE PAS DEVINER, demander.

## 2. Logo émetteur
Appeler **logo-resolver** (domaine émetteur) → `assets/logo-emetteur.*` (SVG/PNG). Jamais de texte seul
si un fichier est obtenable ; jamais de logo IA. Noter le niveau atteint (officiel/rehost/banque/SVG recréé).

## 3. Assets & réassurance du site émetteur (ex-PHASE 3bis) — OBLIGATOIRE
Via `web_search_exa` + `web_fetch_exa` (batcher). Lire home, produit, « clients/références », blog.
- **A. Créas & images à réutiliser/adapter** : photos hero, portraits, illustrations, mockups, pictos,
  motifs, vidéos. Extraire `img[src]`, `og:image`, `<video>`/poster, backgrounds CSS. Noter URL, type,
  usage, dominante. Servent de base à adapter (recadrage, recolorisation on-brand, sur-titrage co-brandé)
  et à INSPIRER les créas générées (voir cible-creas). Ne pas hotlinker en prod : rehost (logo-resolver).
- **B. Réassurance (trust signals)**, viser le MAXIMUM sourcé :
  - **Logos clients du SECTEUR du prospect (prioritaire) → FICHIERS, pas une liste.** « Ils nous font déjà
    confiance dans votre secteur ». Parcourir clients/références/case studies, filtrer par secteur du
    prospect, puis **appeler `logo-resolver` en batch** pour ramener chaque logo dans `assets/proof/`
    (officiel/rehost/banque/svg_recree, niveau consigné). Noter marque, secteur, source. Ces fichiers
    alimentent la bande « ils recrutent déjà avec [émetteur] » de la page (obligatoire dans l'assemblage).
  - **Écosystème / partenaires / labels (prioritaire)** : partenaires, intégrations, institutions,
    réseaux, accréditations (ex. JobTeaser : écoles & universités — HEC, ESSEC, Polytechnique…). Adapter
    au métier de l'émetteur.
  - Chiffres clés (clients, utilisateurs, partenaires, pays, ancienneté, volumes, croissance).
  - Témoignages/verbatims nominatifs, notes & avis (G2, Trustpilot, Capterra…).
  - Récompenses, labels, certifications (ISO, RGPD, sécurité), presse, classements.
  - Partenaires, intégrations, ROI/%, cas clients chiffrés.
  Chaque élément avec SOURCE + niveau de confiance. Jamais inventé. Prioriser ce qui parle au secteur/persona du prospect.
- **C. Proposition de valeur (exhaustive)** : extraire le MAX de briques (bénéfices, features/produits,
  différenciateurs, promesses, cas d'usage, résultats), reformulées côté prospect (« vous obtenez… »).

## Livrable
Un **brandbook émetteur** (fichier `brandbook-[emetteur].md`) = { HEX[], typo[], do/don't, sources } +
`assets/logo-emetteur.*` + `assets/emetteur/*` (créas/motifs récupérés) + `reassurance[]` (preuves sourcées)
+ `value_props[]`. Publier les HEX dans la conversation (preuve).

## GATE E (definition of done — bloquante)
```
[ ] HEX émetteur (dominante + accents) publiés + source
[ ] typo émetteur + do/don't visuels
[ ] assets/logo-emetteur.* présent (niveau : officiel/rehost/banque/SVG) — pas de simple texte
[ ] assets/proof/logo-*.* : ≥ 3 logos clients du SECTEUR de la cible (fichiers, via logo-resolver) — repli chips signalé si egress bloqué
[ ] ≥ N preuves sourcées (chiffres + écosystème + ≥1 témoignage si dispo)
[ ] value_props[] non vide
```
Toute case vide → STOP : compléter ou demander à l'utilisateur.
