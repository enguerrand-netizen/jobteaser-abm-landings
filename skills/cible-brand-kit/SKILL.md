---
name: cible-brand-kit
description: >-
  Construit le KIT DE MARQUE du PROSPECT (la cible) : charte réelle (HEX/typo/do-don't) + logo officiel
  du prospect (via logo-resolver). Produit un brandbook cible livrable, un par compte. Déclencher depuis
  l'orchestrateur lp-rapprochement, ou sur "récupère la charte de [prospect]", "brandbook de [cible]",
  "les couleurs et le logo de [compte]". S'exécute UNE fois PAR CIBLE.
---

# cible-brand-kit — Kit de marque du PROSPECT (/cible)

But : disposer des VRAIES couleurs + du logo du prospect pour co-brander la page (accent = prospect).
Anti-invention absolu : jamais une couleur « de mémoire ».

## 1. Charte du prospect (ex-PHASE 1, volet prospect)
Couleurs HEX exactes (dominante + accents), par ordre de fiabilité :
1. Skill `brand-extractor` si dispo.
2. Navigateur (Chrome) : styles calculés + variables CSS du site, boutons/CTA, `<meta name="theme-color">`, fonds header/footer.
3. Brandbook public / page « presse & médias » / kit de marque.
4. Exa/HTML : `meta theme-color`, backgrounds, classes de boutons.
Typographies + source. **Do/don't visuels** de la marque (formes, ombres/dégradés autorisés ou non, motifs, ton).
Vérifier lisibilité de l'accent sur le mode de la page (dark/light de l'émetteur). Si un accent est
illisible en texte → ne l'utiliser qu'en aplat/déco (le noter). Doute sur une couleur → demander, ne pas deviner.

## 2. Logo du prospect
Appeler **logo-resolver** (domaine prospect) → `assets/logo-[cible].*`. Jamais de texte seul si un fichier
est obtenable ; jamais de logo IA. Enregistrer le **niveau atteint** (officiel / rehost / banque / SVG recréé).

## Livrable
Un **brandbook cible** (fichier `brandbook-[cible].md`) = { HEX[], typo[], do/don't, source, niveau logo } +
`assets/logo-[cible].*`. Publier les HEX + le niveau logo dans la conversation.

## GATE C1 (bloquante)
```
[ ] HEX cible (dominante + accents) publiés + source (pas « de mémoire »)
[ ] typo + do/don't visuels
[ ] assets/logo-[cible].* présent, avec niveau atteint indiqué
[ ] accent cible lisible sur le mode de la page (sinon usage aplat/déco noté)
```
Case vide → STOP. Si seul le SVG recréé est atteignable et que l'utilisateur exige l'officiel → réclamer le fichier.
