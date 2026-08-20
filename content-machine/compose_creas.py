# -*- coding: utf-8 -*-
"""Compose les créas 1080x1080 : fond Studio + logos réels + texte, en post-prod."""
import os
from PIL import Image, ImageDraw, ImageFont

A = "/Users/enguerrandchalvondemersay/jobteaser-abm-landings/content-machine"
BG = f"{A}/assets/creas"
OUT = f"{A}/assets/creas_final"
os.makedirs(OUT, exist_ok=True)

SANOFI_LOGO = f"{A}/assets/logo-sanofi-white_fixed.png"
JT_LOGO = f"{A}/assets/logo-emetteur-white_fixed.png"

def font(size):
    for p in ["/System/Library/Fonts/Helvetica.ttc",
              "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
              "/System/Library/Fonts/Supplemental/Arial.ttf"]:
        if os.path.exists(p):
            try: return ImageFont.truetype(p, size)
            except Exception: pass
    return ImageFont.load_default()

def wrap(draw, text, f, max_w):
    words = text.split(); lines = []; line = ""
    for w in words:
        t = (line + " " + w).strip()
        if draw.textlength(t, font=f) > max_w and line:
            lines.append(line); line = w
        else:
            line = t
    lines.append(line)
    return lines

def paste_logo(canvas, path, x, y, h):
    if not os.path.exists(path): return x
    im = Image.open(path).convert("RGBA")
    r = im.width / im.height
    w = int(h * r)
    im2 = im.resize((w, h))
    canvas.paste(im2, (int(x), int(y)), im2)
    return x + w

def compose(bg_file, tag, headline, cta, out_name):
    im = Image.open(f"{BG}/{bg_file}").convert("RGB").resize((1080, 1080))
    canvas = im.convert("RGBA")
    draw = ImageDraw.Draw(canvas)

    lx = 56
    lx = paste_logo(canvas, JT_LOGO, lx, 46, 40)
    draw.text((lx+8, 52), "JobTeaser", font=font(30), fill=(255,255,255,255))
    lx += 8 + draw.textlength("JobTeaser", font=font(30))
    draw.text((lx+16, 52), "×", font=font(28), fill=(180,178,190,255))
    paste_logo(canvas, SANOFI_LOGO, lx+52, 44, 46)

    tag_f = font(22)
    tw = draw.textlength(tag.upper(), font=tag_f)
    draw.rounded_rectangle([56, 120, 56+tw+36, 120+42], radius=21, fill=(91,255,119,235))
    draw.text((74, 129), tag.upper(), font=tag_f, fill=(20,19,26,255))

    scrim = Image.new("RGBA", (1080, 480), (0,0,0,0))
    sd = ImageDraw.Draw(scrim)
    for i in range(480):
        a = int(215 * (i/480)**1.4)
        sd.line([(0,i),(1080,i)], fill=(10,9,14,a))
    canvas.alpha_composite(scrim, (0, 600))

    hf = font(52)
    lines = wrap(draw, headline, hf, 960)
    ty = 1080 - 210 - (len(lines)-1)*60
    for ln in lines:
        draw.text((58, ty), ln, font=hf, fill=(255,255,255,255))
        ty += 60

    cf = font(28)
    tw = draw.textlength(cta, font=cf)
    bx0, by0, by1 = 56, 1080-70, 1080-24
    bx1 = bx0 + tw + 66
    draw.rounded_rectangle([bx0, by0, bx1, by1], radius=23, fill=(91,255,119,255))
    draw.text((bx0+28, by0+7), cta, font=cf, fill=(20,19,26,255))
    ay = (by0+by1)//2; ax = bx1-30
    draw.line([(ax-10,ay-8),(ax+2,ay),(ax-10,ay+8)], fill=(20,19,26,255), width=3, joint="curve")

    canvas.convert("RGB").save(f"{OUT}/{out_name}.jpg", "JPEG", quality=86)
    print(out_name, "ok")

CREAS = [
    ("bg1.png", "Content", "Le premier biopharma piloté par l'IA à grande échelle.", "Découvrir Sanofi", "cc_content_1"),
    ("bg2.png", "Content", "IA et science ne font plus qu'un chez Sanofi.", "En savoir plus", "cc_content_2"),
    ("bg9.png", "Content", "5 M étudiants. Vos futurs talents R&D, Digital, Commercial.", "Voir le vivier", "cc_content_3"),
    ("bg4.png", "Visibilité", "800+ écoles partenaires · 5 M étudiants · 10 pays européens", "Découvrir JobTeaser", "cc_visi_1"),
    ("bg5.png", "Visibilité", "Sanofi × OpenAI × Formation Bio — une première en pharma", "Voir le partenariat", "cc_visi_2"),
    ("bg6.png", "Visibilité", "Le bon réseau pour les profils science + data", "Le partenariat", "cc_visi_3"),
    ("bg3.png", "Conversion", "Les profils hybrides science + data se font rares.", "Sourcer maintenant", "cc_conv_1"),
    ("bg7.png", "Conversion", "Sourcer vos talents Early Careers, dès aujourd'hui.", "Échangeons ensemble", "cc_conv_2"),
    ("bg8.png", "Conversion", "30 minutes pour cadrer votre plan Early Careers 2026.", "Réserver un créneau", "cc_conv_3"),
]
for c in CREAS:
    compose(*c)
print("Terminé :", len(CREAS), "créas")
