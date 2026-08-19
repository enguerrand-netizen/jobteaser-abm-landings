#!/usr/bin/env python3
"""
normalize_logo.py — produit des variantes de logo lisibles sur fond clair ET sombre,
en normalisant les `fill` AU NIVEAU DES PATHS (pas seulement la racine <svg>).

Pourquoi : beaucoup de wordmarks SVG ont `fill="white"` (ou "black", ou "currentColor")
codé sur chaque path. Changer seulement `fill` sur la balise <svg> est IGNORÉ → le logo
reste invisible sur le mauvais fond. Ce script règle exactement ce bug.

Usage :
  # inspecter la palette de fills
  python3 normalize_logo.py logo.svg --check

  # variante foncée (pour fond CLAIR : nav blanche, bande de couleur) en préservant un accent
  python3 normalize_logo.py logo.svg --mode dark  --keep '#5BFF77' -o logo-dark.svg

  # variante blanche (pour fond SOMBRE : hero, footer)
  python3 normalize_logo.py logo.svg --mode white --keep '#5BFF77' -o logo-white.svg

  # couleur cible explicite
  python3 normalize_logo.py logo.svg --mode color --target '#1A191C' -o logo-ink.svg

Sortie : écrit le fichier -o et imprime les fills résultants + un rappel de contraste.
Ne génère jamais de logo par IA ; se contente de recolorer un vrai fichier.
"""
import argparse, re, sys, os

HEXRE = re.compile(r'#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b')
FILL_ATTR = re.compile(r'fill\s*=\s*"([^"]*)"')
FILL_STYLE = re.compile(r'fill\s*:\s*([^;"\'}\s]+)')

NAMED = {  # couleurs nommées SVG les plus fréquentes sur les logos
    'white': (255, 255, 255), 'black': (0, 0, 0), 'currentcolor': None,
}

def to_rgb(c):
    if c is None: return None
    c = c.strip().lower()
    if c in ('none', 'transparent'): return None
    if c in NAMED: return NAMED[c]
    m = HEXRE.fullmatch(c) or HEXRE.match(c)
    if m:
        h = m.group(1)
        if len(h) == 3: h = ''.join(ch * 2 for ch in h)
        return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
    m = re.match(r'rgba?\(([^)]+)\)', c)
    if m:
        p = [x.strip() for x in m.group(1).split(',')]
        return tuple(int(float(p[i])) for i in range(3))
    return None

def norm_hex(c):
    rgb = to_rgb(c)
    return None if rgb is None else '#%02x%02x%02x' % rgb

def is_special(c):
    """fill à NE PAS toucher : none/transparent (no-fill volontaire)."""
    return c is None or c.strip().lower() in ('none', 'transparent', 'url', '') or c.strip().lower().startswith('url(')

def collect_fills(svg):
    vals = set()
    for m in FILL_ATTR.finditer(svg): vals.add(m.group(1))
    for m in FILL_STYLE.finditer(svg): vals.add(m.group(1))
    return vals

def recolor(svg, target, keep_hexes):
    keep = {norm_hex(k) for k in keep_hexes if norm_hex(k)}
    changed = [0]
    def repl_attr(m):
        v = m.group(1)
        if is_special(v): return m.group(0)
        if norm_hex(v) in keep: return m.group(0)
        changed[0] += 1
        return 'fill="%s"' % target
    def repl_style(m):
        v = m.group(1)
        if is_special(v): return m.group(0)
        if norm_hex(v) in keep: return m.group(0)
        changed[0] += 1
        return 'fill:%s' % target
    svg = FILL_ATTR.sub(repl_attr, svg)
    svg = FILL_STYLE.sub(repl_style, svg)
    return svg, changed[0]

def has_any_path_fill(svg):
    # y a-t-il au moins un <path .../> avec un fill non-none ?
    for m in re.finditer(r'<path\b[^>]*>', svg):
        tag = m.group(0)
        fm = FILL_ATTR.search(tag) or FILL_STYLE.search(tag)
        if fm and not is_special(fm.group(1)):
            return True
    return False

def ensure_root_fill(svg, target):
    """Si aucun path n'a de fill explicite (paths comptent sur le noir par défaut) et que
    la racine a fill="none" (=> tout invisible), forcer fill=target sur la racine."""
    if has_any_path_fill(svg):
        return svg, False
    # racine <svg ...>
    def fix(m):
        tag = m.group(0)
        if FILL_ATTR.search(tag):
            return FILL_ATTR.sub('fill="%s"' % target, tag, count=1)
        return tag[:-1] + ' fill="%s">' % target
    return re.sub(r'<svg\b[^>]*>', fix, svg, count=1), True

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('svg')
    ap.add_argument('--mode', choices=['dark', 'white', 'color', 'check'], default='check')
    ap.add_argument('--check', action='store_true', help='alias de --mode check (inspecte la palette)')
    ap.add_argument('--target', help='hex pour --mode color')
    ap.add_argument('--keep', action='append', default=[], help='couleur(s) accent à préserver (répétable)')
    ap.add_argument('-o', '--out')
    a = ap.parse_args()
    if a.check: a.mode = 'check'

    if not os.path.isfile(a.svg):
        print('fichier introuvable:', a.svg); sys.exit(2)
    svg = open(a.svg, encoding='utf-8').read()
    fills = collect_fills(svg)
    palette = sorted({norm_hex(f) or f for f in fills})

    if a.mode == 'check':
        print('fills détectés :', ', '.join(palette) if palette else '(aucun — paths en noir par défaut ?)')
        print('paths avec fill explicite :', 'oui' if has_any_path_fill(svg) else 'NON (recolorer via racine)')
        return

    target = a.target if a.mode == 'color' else ('#ffffff' if a.mode == 'white' else '#1a191c')
    if a.mode == 'color' and not target:
        print('--target requis pour --mode color'); sys.exit(2)

    out, n = recolor(svg, target, a.keep)
    out, rootfix = ensure_root_fill(out, target)
    dest = a.out or (os.path.splitext(a.svg)[0] + '-' + a.mode + '.svg')
    open(dest, 'w', encoding='utf-8').write(out)
    print('écrit :', dest)
    print('fills remplacés :', n, ('(+ fill racine forcé)' if rootfix else ''))
    print('fills résultants :', ', '.join(sorted({norm_hex(f) or f for f in collect_fills(out)})))
    bg = 'CLAIR (nav blanche, bande de couleur)' if a.mode == 'dark' else ('SOMBRE (hero, footer)' if a.mode == 'white' else '?')
    print('→ à utiliser sur fond', bg)
    print('RAPPEL : vérifier le rendu réel (audit_logos.js) ; sur une vidéo, poser le logo sur une plaque solide.')

if __name__ == '__main__':
    main()
