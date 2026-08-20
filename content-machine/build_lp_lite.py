# -*- coding: utf-8 -*-
"""Version allégée et autonome de la landing réelle JobTeaser x Sanofi pour embed Shadow DOM."""
import re, base64, io, os
from PIL import Image

SRC_DIR = "/Users/enguerrandchalvondemersay/jobteaser-abm-landings/lp-jobteaser-sanofi"
OUT = "/Users/enguerrandchalvondemersay/jobteaser-abm-landings/content-machine/lp_sanofi_lite.html"

html = open(f"{SRC_DIR}/lp-jobteaser-sanofi.html", encoding="utf-8").read()

# Supprimer la vidéo (poster cassé) -> fond statique avec hero-person.jpg
html = re.sub(
    r'<video id="hero-video"[^>]*>.*?</video>',
    '<img class="hero-bg" src="assets/hero-person.jpg" alt="" aria-hidden="true" style="object-fit:cover">',
    html, flags=re.S)

def to_data_uri(path):
    ext = os.path.splitext(path)[1].lower()
    if ext == ".svg":
        data = open(path, "rb").read()
        return "data:image/svg+xml;base64," + base64.b64encode(data).decode()
    im = Image.open(path).convert("RGB")
    if max(im.size) > 900:
        im.thumbnail((900, 900))
    b = io.BytesIO()
    im.save(b, "JPEG", quality=68, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()

def repl(m):
    rel = m.group(1)
    full = os.path.join(SRC_DIR, "assets", rel)
    if not os.path.exists(full):
        return m.group(0)
    try:
        return f'src="{to_data_uri(full)}"'
    except Exception:
        return m.group(0)

html = re.sub(r'src="assets/([^"]+)"', repl, html)
open(OUT, "w", encoding="utf-8").write(html)
print("lp_sanofi_lite.html ->", round(os.path.getsize(OUT)/1024/1024, 2), "MB")
