---
name: lp-rapprochement
description: >-
  Orchestrateur ABM 1-to-1 : produit UNE landing page HTML autonome, nominative et co-brandée,
  envoyée par un CLIENT ÉMETTEUR à UN compte cible (le PROSPECT), démontrant en < 30 s pourquoi le
  rapprochement est évident, avec un CTA unique. Déclencher sur : "fais une landing page pour rapprocher
  [X] de [Y]", "LP de rapprochement", "page ABM pour approcher [prospect]", "landing perso pour [prospect]",
  "[client] veut se rapprocher de [prospect]", "one-to-one landing pour [compte cible]". Cet orchestrateur
  N'ÉCRIT PAS la page lui-même : il enchaîne les sous-skills (emetteur-brand-kit, cible-brand-kit,
  cible-signaux, cible-creas, lp-assemblage) et lance verification-web en QA final, en bloquant à chaque
  gate. Distinct de conversion-optimization (audit d'une LP existante) et de sea-cartographie-intentions
  (LP SEA à l'échelle) : ici UNE page nominative pour UN compte nommé.
---

# lp-rapprochement — Orchestrateur ABM 1-to-1 (v3 modulaire)

## Rôle
Chef d'orchestre. Découpe le process historique en sous-skills autonomes et **testables**, chacune close
par une **gate bloquante** (definition of done). On ne dégrade JAMAIS en silence : si un livrable réel
manque (logo-fichier, image dans `assets/`, HEX sourcé, signal sourcé), on **STOP et on réclame**.

## Règles d'or (valables partout, héritées de la v1)
- **Anti-invention (non négociable)** : jamais une couleur, un logo, un chiffre, un témoignage ou une
  actualité « de mémoire ». Toute donnée vient d'une source réelle ou est demandée à l'utilisateur.
- **Design (non négociable)** : on ne code jamais une page de zéro. `lp-assemblage` part du template de
  référence tokenisé (`reference/template.html`) ; niveau cible = l'exemple d'or `reference/example/`.
- **Logos** : jamais générés par IA. Échelle officiel → rehost → banque (Clearbit/Brandfetch) → recréation
  SVG fidèle (via `logo-resolver`). La gate note QUEL niveau a été atteint.
- **Une seule page, un seul compte cible, un seul CTA** par exécution.
- Si le plugin Bulldozer est actif : logger `bdzCreateAiMetric` (type `AI_METRIC_TYPE_SKILL_USED`,
  reference `lp-rapprochement`) et exploiter ICP / tone of voice / success stories / contacts si dispo.

## PHASE 0 — Identifier les acteurs (fait par l'orchestrateur)
Clarifier (demander seulement ce qui manque) :
1. ÉMETTEUR : nom, ce qu'il vend/apporte, URL, contact.
2. PROSPECT(S) : nom, URL, secteur, contact visé (nom, poste) si connu. (Plusieurs cibles = on rejoue les
   sous-skills /cible pour chacune ; l'émetteur n'est traité qu'une fois.)
3. SENS : c'est l'émetteur qui veut se rapprocher / vendre au prospect.
4. ANGLE : ce que l'émetteur veut vendre / le partenariat visé.
5. CTA : lien de RDV (Calendly) ou email/contact. Si absent → `#` signalé OU mailto de contact réel.
Livrable : « [ÉMETTEUR] veut se rapprocher de [PROSPECT] — angle : [X] — CTA : [lien] ».

## Séquence d'appel (et gates)
```
1. emetteur-brand-kit   (×1, réutilisable)   → GATE E : HEX+typo publiés, logo-fichier présent, ≥N preuves
2. logo-resolver        (utilitaire, appelé par 1/2/4)
POUR CHAQUE CIBLE :
  3. cible-brand-kit     → GATE C1 : HEX+typo cible publiés, logo-fichier présent (+ niveau atteint)
  4. cible-signaux       → GATE C2 : ≥3 signaux sourcés (URL+date) + thèse
  5. cible-creas         → GATE C3 : N images RÉELLEMENT dans assets/ (pas des liens)
  6. lp-assemblage       → GATE C4 : tokens :root remplis, 0 placeholder, 1 CTA réel, co-branding présent
  7. verification-web    → GATE FINALE : score ≥ seuil, 0 BLOCKER/HIGH, cible visible nav+bande+footer
```
Toute gate rouge = STOP sur cette cible : demander l'asset manquant ou relancer la sous-skill. Ne pas
enchaîner sur du dégradé silencieux.

## Contrôle des gates — `abm-process-gate` (obligatoire à chaque transition)
Après chaque sous-skill, invoquer **`abm-process-gate`** (skill dédiée) qui vérifie, via son script
`check_process.py <dossier> --emetteur X --cible Y`, que le livrable réel existe (brandbooks, ≥3 signaux
sourcés, créas dans assets/ ou galerie, page sans placeholder, co-branding présent). Verdict PASS/FAIL par
gate ; FAIL = on ne franchit pas. Options : `--strict-assets` (photos en dur exigées) et `--strict-logos`
(logos officiels exigés) pour le mode « tout ou rien ». C'est le garde-barrière du process ; `verification-web`
reste le QA esthétique final.

## Politique de dégradation (explicite, jamais muette)
Si un asset ne peut pas être obtenu au niveau idéal, la sous-skill le dit et propose le repli :
- Logo : officiel indisponible → rehost → banque → SVG recréé (signalé). La gate exige AU MINIMUM un
  fichier présent (même recréé) ; « simple texte » interdit si un fichier est obtenable.
- Image : Studio indisponible/non rapatriable → galerie de récupération + `assets/` câblé en fallback.
- Le mode « tout ou rien » se règle ici : si l'utilisateur exige des assets officiels, durcir les gates
  logo/image pour bloquer au lieu de recréer/dégrader.

## Contrainte d'environnement (à connaître)
Le sandbox a une **allowlist egress** : télécharger un fichier (S3 Studio, logos de marque) peut être
bloqué. Voir `cible-creas` et `logo-resolver` pour le pont download/rehost et les replis. Si l'egress est
ouvert (domaines ajoutés) → rapatriement direct dans `assets/` (durable). Sinon → dépôt utilisateur.

## PHASE 7 — Livraison (fait par l'orchestrateur)
- Rassembler `lp-[emetteur]-[cible].html` + `assets/` (+ brandbooks + `prompts-images-*.md`) et présenter
  les fichiers à l'utilisateur.
- Proposer en une ligne : déploiement, ajustements de wording, déclinaison pour d'autres comptes.

### Déploiement (Bulldozer hosting) — procédure validée
1. Bundler `index-standalone.html` (assets inlinés base64, transparents = PNG), optimisé (< 25 Mo, ~2 Mo idéal).
2. `bdzRequestFridgeCode` → upload fridge (`upload_fridge_file.py --file … --code …`) → `file.id`.
3. `bdzCreateHosting` (`fridgeId=file.id`, type `HOSTING_TYPE_SINGLE_FILE`) → `bdzExploreHosting` → URL signée (1 h ; ré-explorer pour un lien frais).
4. ⚠️ `HOSTING_TYPE_STATIC_SITE` (URL publique `*.bulldozer-os.fr`) = 500 actuellement → livrer le fichier autonome. Repli : Netlify/Vercel drop du dossier statique.

## Ton (hérité)
Direct, orienté bénéfice prospect, zéro jargon d'agence, zéro superlatif creux. La page se lit en < 1 min ;
le prospect doit sentir qu'elle a été écrite pour lui seul.

## Reproductibilité
`[émetteur]`/`[prospect]` sont des variables. Rien codé en dur. Émetteur traité 1×, cible rejouée N fois.

## Garde-fous
- Ne jamais assembler avant que GATE E + C1 + C2 + C3 soient vertes.
- Ne jamais inventer ; logos jamais IA ; cible toujours co-brandée et visible ; un seul CTA.
- Si émetteur/prospect/sens ambigu → demander avant de produire.
