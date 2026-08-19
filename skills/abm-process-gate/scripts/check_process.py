#!/usr/bin/env python3
"""
check_process.py — garde-barrière du pipeline lp-rapprochement.
Vérifie que CHAQUE sous-skill a produit son LIVRABLE RÉEL (pas « à sourcer »).
Ne juge PAS l'esthétique (ça, c'est verification-web).

Usage :
  python3 check_process.py <dossier> --emetteur "JobTeaser" --cible "Bulldozer"
                                     [--strict-assets] [--strict-logos]
Gates : E (émetteur), C1..C4 (cible). PASS/FAIL par gate + verdict global.
Code retour != 0 si une gate échoue.
"""
import argparse, os, re, glob, sys

def slug(s): return re.sub(r'[^a-z0-9]+', '-', (s or '').lower()).strip('-')

def read(p):
    try: return open(p, encoding='utf-8', errors='ignore').read()
    except Exception: return ''

def find(folder, *names):
    """premier fichier existant parmi des motifs glob (insensible à la casse via slug)."""
    for n in names:
        hits = glob.glob(os.path.join(folder, n))
        if hits: return hits[0]
    return None

HEX = re.compile(r'#[0-9a-fA-F]{6}\b')
URL = re.compile(r'https?://[^\s)\]]+')
DATE = re.compile(r'\b(20\d{2}|\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|janv|févr|fév|mars|avril|mai|juin|juil|août|sept|oct|nov|déc)\b', re.I)
PLACEHOLDER = re.compile(r'@@[^@]+@@|\{\{[^}]+\}\}|\[\[[^\]]+\]\]|\$\{[^}]+\}')
LAZY = re.compile(r'\b(à sourcer|à remplacer|à définir|de mémoire|lorem ipsum|TODO|FIXME|placeholder)\b', re.I)

def has_logo(folder, base):
    return bool(glob.glob(os.path.join(folder, 'assets', base + '.*')))

def logo_level(text):
    m = re.search(r'(officiel|rehost|banque|svg[_ ]?recree|svg[_ ]?recré)', text, re.I)
    return m.group(1).lower() if m else None

def gate_E(folder, em, strict_logos):
    fails = []
    bb = find(folder, 'brandbook-%s.md' % slug(em), 'brandbook-emetteur.md', 'brandbook-*.md')
    if not bb: return ['brandbook émetteur absent']
    t = read(bb)
    if len(set(HEX.findall(t))) < 2: fails.append('≥2 HEX émetteur requis (+ source)')
    if not re.search(r'(typo|font|police|jakarta|grotesk|sans|serif)', t, re.I): fails.append('typo émetteur absente')
    if not URL.search(t) and 'source' not in t.lower(): fails.append('sources absentes')
    if not has_logo(folder, 'logo-emetteur'): fails.append('assets/logo-emetteur.* absent')
    if not re.search(r'(logo|écol|ecol|client|partenaire|réassur|reassur|témoign|temoign|chiffre)', t, re.I):
        fails.append('bande de preuves/réassurance non listée')
    if not re.search(r'(value[ _]?prop|proposition de valeur|vous obtenez|bénéfice|benefice)', t, re.I):
        fails.append('value_props vide')
    if strict_logos and logo_level(t) not in ('officiel', 'rehost'):
        fails.append('--strict-logos : niveau logo émetteur < rehost')
    return fails

def gate_C1(folder, ci, strict_logos):
    fails = []
    bb = find(folder, 'brandbook-%s.md' % slug(ci), 'brandbook-cible.md')
    if not bb:
        # tolère brandbook-*.md distinct de l'émetteur
        cands = [p for p in glob.glob(os.path.join(folder, 'brandbook-*.md')) if slug(ci) in p.lower()]
        bb = cands[0] if cands else None
    if not bb: return ['brandbook cible absent']
    t = read(bb)
    if len(set(HEX.findall(t))) < 2: fails.append('≥2 HEX cible requis (+ source)')
    if not re.search(r'(typo|font|police|sans|serif|pressura|grotesk)', t, re.I): fails.append('typo cible absente')
    if not (URL.search(t) or 'source' in t.lower()): fails.append('source cible absente')
    if not has_logo(folder, 'logo-' + slug(ci)) and not has_logo(folder, 'logo-cible'):
        fails.append('assets/logo-[cible].* absent')
    if not logo_level(t): fails.append('niveau logo cible non indiqué (officiel/rehost/banque/svg_recree)')
    if strict_logos and logo_level(t) not in ('officiel', 'rehost'):
        fails.append('--strict-logos : niveau logo cible < rehost')
    return fails

def gate_C2(folder, ci):
    fails = []
    f = find(folder, 'signaux-%s.md' % slug(ci), 'signaux-*.md', 'signals-*.md')
    if not f: return ['fichier signaux absent']
    t = read(f)
    # compter les items ayant URL + date (approx : lignes/blocs avec une URL et une date)
    blocks = re.split(r'\n\s*\n|\n(?=\d+\.|\n?[-*] )', t)
    ok = [b for b in blocks if URL.search(b) and DATE.search(b)]
    if len(ok) < 3: fails.append('≥3 signaux avec URL + date requis (trouvés : %d)' % len(ok))
    if not re.search(r'(thèse|these|message match|parce que)', t, re.I): fails.append('thèse (1 phrase) absente')
    return fails

def gate_C3(folder, ci, strict_assets):
    fails = []
    hero = glob.glob(os.path.join(folder, 'assets', 'hero-*.*')) or glob.glob(os.path.join(folder, 'assets', 'hero-person.*'))
    portraits = glob.glob(os.path.join(folder, 'assets', 'portrait-*.*')) + glob.glob(os.path.join(folder, 'assets', 'scene-*.*'))
    gallery = find(folder, 'apercu-*.html', 'galerie-*.html')
    prompts = find(folder, 'prompts-images-*.md', 'prompts-*.md')
    motion = glob.glob(os.path.join(folder, 'assets', 'motion-*.mp4')) or glob.glob(os.path.join(folder, 'assets', '*.mp4'))
    if not prompts: fails.append('prompts-images-*.md absent')
    if strict_assets:
        if not hero: fails.append('--strict-assets : assets/hero-*.* absent')
        if len(portraits) < 2: fails.append('--strict-assets : ≥2 portraits/scènes requis (trouvés : %d)' % len(portraits))
    else:
        if not (hero or gallery): fails.append('ni hero en dur ni galerie de récupération')
    if not motion: fails.append('motion vidéo (assets/*.mp4) absente — repli CSS à noter explicitement')
    return fails

def gate_C4(folder, em, ci):
    fails = []
    f = find(folder, 'lp-%s-%s.html' % (slug(em), slug(ci)), 'lp-*.html', 'index*.html', '*.html')
    # éviter d'attraper une galerie
    if f and ('apercu' in os.path.basename(f) or 'galerie' in os.path.basename(f)):
        cands = [p for p in glob.glob(os.path.join(folder, '*.html')) if 'apercu' not in p and 'galerie' not in p]
        f = cands[0] if cands else None
    if not f: return ['page lp-[emetteur]-[cible].html absente']
    t = read(f)
    ph = PLACEHOLDER.findall(t)
    if ph: fails.append('placeholders résiduels : %s' % ', '.join(sorted(set(ph))[:4]))
    if LAZY.search(t): fails.append('mention paresseuse (« %s »)' % LAZY.search(t).group(0))
    # co-branding : les 2 marques présentes
    if slug(em) not in slug(t): fails.append('émetteur absent de la page')
    if slug(ci) not in slug(t): fails.append('cible absente de la page')
    # CTA réel : mailto ou http (hors # nu)
    if not re.search(r'href="(mailto:[^"]+|https?://[^"]+|tel:[^"]+)"', t): fails.append('aucun CTA réel (lien mailto/http)')
    if re.search(r'href="#"', t): fails.append('CTA en # (mort) présent')
    if '@media' not in t: fails.append('aucune media query (non responsive)')
    # co-branding réparti (nav + footer au minimum) : heuristique sur des ancres de logo
    logo_refs = len(re.findall(r'logo-(emetteur|' + slug(ci) + r'|bulldozer)', t))
    if logo_refs < 3: fails.append('co-branding insuffisant (logos répétés nav/bande/footer)')
    # ⭐ CO-BRANDING DE LA CRÉA/HERO (exigence forte) : le hero DOIT porter les 2 logos
    mh = re.search(r'<section[^>]*class="[^"]*hero[^"]*"[\s\S]*?</section>', t, re.I)
    hero = mh.group(0) if mh else (re.search(r'<section[\s\S]*?</section>', t) or [None]) and (re.search(r'<section[\s\S]*?</section>', t).group(0) if re.search(r'<section[\s\S]*?</section>', t) else '')
    if hero:
        em_in = bool(re.search(r'logo-emetteur', hero))
        ci_in = bool(re.search(r'logo-(' + slug(ci) + r'|bulldozer)', hero))
        if not (em_in and ci_in):
            fails.append('HERO/créa NON co-brandé (les 2 logos doivent être dans le hero : émetteur=%s, cible=%s)' % (em_in, ci_in))
    else:
        fails.append('section hero introuvable (impossible de vérifier le co-branding de la créa)')
    return fails

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('folder')
    ap.add_argument('--emetteur', required=True)
    ap.add_argument('--cible', required=True)
    ap.add_argument('--strict-assets', action='store_true')
    ap.add_argument('--strict-logos', action='store_true')
    a = ap.parse_args()
    if not os.path.isdir(a.folder): print('dossier introuvable:', a.folder); sys.exit(2)

    gates = [
        ('E  (emetteur-brand-kit)', gate_E(a.folder, a.emetteur, a.strict_logos)),
        ('C1 (cible-brand-kit)', gate_C1(a.folder, a.cible, a.strict_logos)),
        ('C2 (cible-signaux)', gate_C2(a.folder, a.cible)),
        ('C3 (cible-creas)', gate_C3(a.folder, a.cible, a.strict_assets)),
        ('C4 (lp-assemblage)', gate_C4(a.folder, a.emetteur, a.cible)),
    ]
    print('=' * 64)
    print('ABM PROCESS GATE — %s → %s' % (a.emetteur, a.cible))
    print('dossier :', a.folder, '| strict-assets:', a.strict_assets, '| strict-logos:', a.strict_logos)
    print('=' * 64)
    failed = 0
    for name, fails in gates:
        if fails:
            failed += 1
            print('❌ GATE %s : FAIL' % name)
            for f in fails: print('     - ' + f)
        else:
            print('✅ GATE %s : PASS' % name)
    print('-' * 64)
    print('VERDICT :', ('❌ %d gate(s) en échec — NE PAS franchir' % failed) if failed else '✅ toutes les gates vertes')
    sys.exit(1 if failed else 0)

if __name__ == '__main__':
    main()
