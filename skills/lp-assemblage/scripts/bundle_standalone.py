#!/usr/bin/env python3
"""
bundle_standalone.py — fusionne une LP + son dossier assets/ en UN SEUL fichier HTML autonome
(tous les assets en data:URI base64), prêt à héberger (Bulldozer hosting / Netlify / drop).

Usage :
  python3 bundle_standalone.py page.html --assets-dir assets -o index-standalone.html

- Inline src="assets/..." et url(assets/...) (CSS) en data:URI.
- SVG : inliné en data:image/svg+xml;utf8 (léger). Images/vidéo : base64.
- Transparents (PNG) préservés (jamais aplatis). Vidéo mp4 inlinée telle quelle.
- Imprime la taille finale + un avertissement si > 25 Mo (limite hosting single-file).
Ne modifie pas la source ; écrit seulement le fichier -o.
"""
import argparse, os, re, base64, mimetypes, sys, urllib.parse

MIME = {'.svg': 'image/svg+xml', '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg',
        '.webp': 'image/webp', '.gif': 'image/gif', '.mp4': 'video/mp4', '.webm': 'video/webm',
        '.woff2': 'font/woff2', '.woff': 'font/woff'}

def data_uri(path):
    ext = os.path.splitext(path)[1].lower()
    mime = MIME.get(ext) or mimetypes.guess_type(path)[0] or 'application/octet-stream'
    raw = open(path, 'rb').read()
    if ext == '.svg':
        txt = raw.decode('utf-8', 'ignore')
        txt = re.sub(r'<\?xml[^>]*\?>', '', txt).strip()
        return 'data:image/svg+xml;utf8,' + urllib.parse.quote(txt), len(raw)
    return 'data:%s;base64,%s' % (mime, base64.b64encode(raw).decode()), len(raw)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('html')
    ap.add_argument('--assets-dir', default='assets')
    ap.add_argument('-o', '--out', default='index-standalone.html')
    a = ap.parse_args()
    base = os.path.dirname(os.path.abspath(a.html))
    html = open(a.html, encoding='utf-8').read()

    cache, missing, total_raw = {}, [], [0]
    def resolve(ref):
        ref = ref.strip().strip('"\'')
        if ref.startswith('data:') or ref.startswith('http') or ref.startswith('#'):
            return None
        rel = ref.split('?')[0].split('#')[0]
        p = os.path.join(base, rel)
        if not os.path.isfile(p):
            missing.append(rel); return None
        if p not in cache:
            uri, n = data_uri(p); cache[p] = uri; total_raw[0] += n
        return cache[p]

    # 1) attribut src="..." / poster="..."
    def repl_attr(m):
        attr, q, ref = m.group(1), m.group(2), m.group(3)
        uri = resolve(ref)
        return '%s=%s%s%s' % (attr, q, uri, q) if uri else m.group(0)
    html = re.sub(r'(src|poster)\s*=\s*(["\'])([^"\']+)\2', repl_attr, html)

    # 2) <source src="...">
    # (déjà couvert par src= ci-dessus)

    # 3) url(...) dans le CSS inline
    def repl_url(m):
        ref = m.group(1)
        uri = resolve(ref)
        return 'url(%s)' % uri if uri else m.group(0)
    html = re.sub(r'url\(\s*([^)]+?)\s*\)', repl_url, html)

    open(a.out, 'w', encoding='utf-8').write(html)
    size = os.path.getsize(a.out)
    print('écrit :', a.out)
    print('assets inlinés :', len(cache), '| source brute :', round(total_raw[0] / 1e6, 2), 'Mo',
          '| fichier final :', round(size / 1e6, 2), 'Mo')
    if missing:
        print('⚠️ références NON trouvées (laissées telles quelles) :', ', '.join(sorted(set(missing))[:10]))
    leftover = re.findall(r'(?:src|poster)\s*=\s*["\']assets/', html) + re.findall(r'url\(\s*["\']?assets/', html)
    if leftover:
        print('⚠️ il reste %d référence(s) assets/ non inlinées → vérifier' % len(leftover))
    else:
        print('✅ aucune référence assets/ restante — fichier 100%% autonome')
    if size > 25 * 1e6:
        print('⛔ > 25 Mo : au-dessus de la limite hosting single-file → compresser la vidéo/images.')
    elif size > 8 * 1e6:
        print('ℹ️ > 8 Mo (vidéo lourde) : ok pour hosting mais compresser la vidéo pour viser ~2 Mo si possible.')

if __name__ == '__main__':
    main()
