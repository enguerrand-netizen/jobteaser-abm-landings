---
name: abm-process-gate
description: >-
  Contrôleur de PROCESS pour le pipeline ABM (lp-rapprochement) : vérifie, étape par étape, que CHAQUE
  livrable attendu existe RÉELLEMENT avant d'autoriser l'étape suivante. Distinct de verification-web (qui
  juge le rendu HTML final) : ici on vérifie que le PROCESS a été fait — brandbook émetteur (HEX+logo+preuves),
  brandbook cible, ≥3 signaux sourcés, créas réellement dans assets/ (ou galerie+fallback), page assemblée
  sans placeholder. Déclencher entre chaque sous-skill, ou sur "vérifie que chaque étape a été faite",
  "les gates sont-elles vertes", "contrôle le process ABM", "process-gate". Rend un PASS/FAIL par gate +
  un verdict global bloquant (exit ≠ 0 si une gate échoue).
---

# abm-process-gate — Le process a-t-il vraiment été fait ? (gate bloquante)

## Rôle
Empêcher la livraison d'un travail « à trous ». C'est le garde-barrière entre les étapes du pipeline
`lp-rapprochement`. Il ne juge PAS l'esthétique (ça, c'est `verification-web`) : il vérifie que chaque
sous-skill a produit son **livrable réel**. « À sourcer / à déposer / de mémoire » = FAIL.

## Quand l'appeler
- Après chaque sous-skill (gate correspondante), et/ou en une passe finale avant assemblage/livraison.
- L'orchestrateur `lp-rapprochement` l'invoque à chaque transition ; toute gate FAIL = STOP.

## Ce qu'il contrôle (par gate)
```
GATE E  (emetteur-brand-kit)  : brandbook-[emetteur].md existe ; ≥2 HEX ; typo ; source ;
                                 assets/logo-emetteur.* présent ; ≥1 bande de preuves (logos clients/
                                 écosystème) listée ; value_props non vide.
GATE C1 (cible-brand-kit)     : brandbook-[cible].md existe ; ≥2 HEX + source ; assets/logo-[cible].* ;
                                 niveau logo indiqué (officiel/rehost/banque/svg_recree).
GATE C2 (cible-signaux)       : signaux-[cible].md ; ≥3 items, chacun avec URL http(s) + date ; thèse.
GATE C3 (cible-creas)         : assets/hero-[cible].* + ≥2 portraits  OU  apercu-*.html (galerie) +
                                 <img src="assets/..."> câblés avec onerror (fallback) ; prompts-images-*.md.
GATE C4 (lp-assemblage)       : lp-[emetteur]-[cible].html ; 0 placeholder (@@..@@/{{..}}/[[..]]/${..}) ;
                                 lockup co-brandé en nav + bande + footer ; 1 CTA réel (lien, mailto) ;
                                 media queries présentes.
```
Chaque gate renvoie PASS / FAIL + la liste des manques. FAIL sur une gate = on ne franchit pas.

## Outil
`scripts/check_process.py <dossier_sortie> --emetteur "X" --cible "Y" [--strict-assets] [--strict-logos]`
- Scanne le dossier, applique les contrôles ci-dessus, imprime un rapport par gate + verdict global.
- `--strict-assets` : GATE C3 exige les FICHIERS images dans assets/ (refuse la galerie seule) → pour le
  mode « tout ou rien » quand l'egress est ouvert.
- `--strict-logos` : GATE E/C1 exigent un logo de niveau ≥ rehost (refuse le SVG recréé) → assets officiels obligatoires.
- Code retour ≠ 0 si une gate échoue (utilisable en pré-commit / pré-livraison).

## Politique
- Par défaut, tolérant sur les replis EXPLICITES (galerie créas, logo recréé) mais **jamais** sur un manque
  silencieux (placeholder laissé, HEX absent, 0 signal sourcé, image cassée sans fallback).
- Les flags `--strict-*` activent le mode exigeant demandé par l'utilisateur (« il me faut les vrais assets »).
- Ce contrôleur ne CORRIGE rien : il liste les manques et renvoie à la sous-skill concernée.
