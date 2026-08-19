---
name: cible-signaux
description: >-
  Recherche prospect sourcée (12 mois) + construction de la thèse de rapprochement. Produit 3-5 signaux
  vérifiés (fait + URL + date) et une phrase-thèse "Parce que [signal prospect], [émetteur] peut [bénéfice]
  pour [prospect]". Déclencher depuis l'orchestrateur lp-rapprochement, ou sur "trouve les signaux de
  [prospect]", "actus récentes de [compte]", "pourquoi maintenant pour [cible]". S'exécute UNE fois PAR CIBLE.
---

# cible-signaux — Signaux prospect + thèse (/cible)

But : ancrer la page dans le réel du prospect (preuve de personnalisation). Anti-invention : un fait non
sourçable est écarté ou formulé comme hypothèse, jamais présenté comme fait.

## Recherche (ex-PHASE 3) — obligatoire AVANT toute rédaction
Chercher (web / Exa ; Bulldozer si dispo) :
- Actualités récentes (12 mois) : levées, lancements, acquisitions, réorganisations, nominations, priorités annoncées.
- Enjeux du secteur du prospect qui recoupent l'offre de l'émetteur.
- Poste/persona du contact visé et ses priorités probables.
- 1-2 « signaux » concrets exploitables comme accroche (recrute massivement, ouvre un marché, change de
  dirigeant, publie un axe stratégique…).
Consigner 3 à 5 faits vérifiés avec URL + date.

## Thèse & message match
Une phrase : « Parce que [signal/enjeu prospect], [émetteur] peut [bénéfice précis, chiffré si possible]
pour [prospect]. » Tout le reste de la page en découle.

## Livrable
`signaux[]` = [{ fait, source (URL), date }] (≥ 3) + `these` (1 phrase). Publier dans la conversation.

## GATE C2 (bloquante)
```
[ ] ≥ 3 signaux, chacun avec URL + date réelles
[ ] 0 fait inventé (les non-sourçables sont écartés ou marqués hypothèse)
[ ] thèse en une phrase, reliant un signal prospect à un bénéfice émetteur
```
Case vide → STOP : relancer la recherche ou demander des sources.
