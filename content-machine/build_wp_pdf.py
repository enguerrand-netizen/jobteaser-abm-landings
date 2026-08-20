# -*- coding: utf-8 -*-
"""Génère un livre blanc PDF cobrandé à partir d'un markdown structuré + images de chapitre."""
import re, sys, os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage, PageBreak
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_JUSTIFY
from PIL import Image as PILImage

INK = HexColor("#14131A")
GREY = HexColor("#5A5A66")
GREEN = HexColor("#5BFF77")
GREEN_D = HexColor("#0E9E43")
VIOLET = HexColor("#7A00E6")
LINE = HexColor("#E7E4EF")

PAGE_W, PAGE_H = A4
MARGIN = 20 * mm

def parse_md(path):
    raw = open(path, encoding="utf-8").read()
    raw = re.sub(r'(?m)^---+\s*$', '', raw)  # séparateurs markdown horizontaux : jamais un vrai paragraphe
    title_m = re.search(r'^# (.+)$', raw, re.M)
    title = title_m.group(1).strip() if title_m else "Livre blanc"
    sub_m = re.search(r'^### (.+)$', raw, re.M)
    subtitle = sub_m.group(1).strip() if sub_m else ""
    sections = re.split(r'\n## ', raw)
    chapters, edito, conclusion, sources, contact = [], "", "", "", ""
    for sec in sections[1:]:
        head, _, body = sec.partition("\n")
        head = head.strip(); body = body.strip()
        if head.startswith("Édito"):
            edito = body
        elif head.startswith("Chapitre"):
            m = re.match(r'Chapitre\s*(\d+)\s*—\s*(.+)', head)
            num = m.group(1) if m else "?"
            ctitle = m.group(2) if m else head
            data_m = re.search(r'\*\*Donnée d\'ouverture\s*:\s*(.+?)\*\*', body)
            data = data_m.group(1).strip() if data_m else ""
            brief_m = re.search(r'^\s*>\s*\*\*Brief illustration[^*]*\*\*\s*:\s*(.+)$', body, re.M)
            brief = brief_m.group(1).strip() if brief_m else ""
            text = re.sub(r'^\s*>.*$', '', body, flags=re.M)
            text = re.sub(r'\*\*Donnée d\'ouverture.*?\*\*', '', text, count=1, flags=re.S)
            chapters.append({"num": num, "title": ctitle, "data": data, "brief": brief, "text": text.strip()})
        elif head.startswith("Conclusion"):
            conclusion = body
        elif head.startswith("Méthodologie"):
            sources = body
        elif head.startswith("Contact"):
            contact = body
    return {"title": title, "subtitle": subtitle, "edito": edito, "chapters": chapters,
            "conclusion": conclusion, "sources": sources, "contact": contact}

def md_inline(t):
    t = t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    t = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)
    t = re.sub(r'\[([^\]]+)\]\((https?://[^)]+)\)', r'<link href="\2" color="#0E9E43">\1</link>', t)
    return t

def para_style(name, size=10.5, leading=15.5, color=INK, bold=False, align=TA_JUSTIFY, space_after=8):
    return ParagraphStyle(name, fontName="Helvetica-Bold" if bold else "Helvetica",
                           fontSize=size, leading=leading, textColor=color,
                           alignment=align, spaceAfter=space_after)

STY = {
    "body": para_style("body"),
    "lead": para_style("lead", size=12.5, leading=18, bold=True, color=INK, space_after=10),
    "h2": para_style("h2", size=18, leading=22, bold=True, align=TA_LEFT, space_after=10),
    "kicker": para_style("kicker", size=10, leading=13, bold=True, color=GREEN_D, align=TA_LEFT, space_after=4),
    "caption": para_style("caption", size=8.5, leading=11, color=GREY, align=TA_LEFT, space_after=14),
    "h3": para_style("h3", size=12.5, leading=16, bold=True, color=INK, align=TA_LEFT, space_after=6),
    "small": para_style("small", size=9, leading=13, color=GREY, align=TA_JUSTIFY, space_after=6),
}

def cover_page(c, W, H, title, subtitle, cover_img, logo_a_path, logo_b_path):
    c.setFillColor(INK); c.rect(0, 0, W, H, fill=1, stroke=0)
    img_top_gap = 32*mm
    img_bottom_y = H * 0.42
    if cover_img and os.path.exists(cover_img):
        im = PILImage.open(cover_img); iw, ih = im.size
        avail_h = H - img_top_gap - (H - img_bottom_y)
        target_h = min(avail_h, (W - 2*MARGIN) * ih / iw)
        scale = target_h / ih; draw_w = iw * scale
        if draw_w > W - 2*MARGIN:
            draw_w = W - 2*MARGIN; target_h = draw_w * ih / iw
        c.drawImage(cover_img, (W - draw_w) / 2, img_bottom_y, width=draw_w, height=target_h, mask='auto')
    x = MARGIN; band_y = H - 20*mm
    if logo_a_path and os.path.exists(logo_a_path):
        im = PILImage.open(logo_a_path); r = im.width / im.height
        h = 8*mm; w = h*r
        c.drawImage(logo_a_path, x, band_y, width=w, height=h, mask='auto'); x += w + 8*mm
    c.setFillColor(GREY); c.setFont("Helvetica", 11); c.drawString(x, band_y+2*mm, "×"); x += 6*mm
    if logo_b_path and os.path.exists(logo_b_path):
        im = PILImage.open(logo_b_path); r = im.width / im.height
        h = 8*mm; w = h*r
        c.drawImage(logo_b_path, x, band_y, width=w, height=h, mask='auto')
    c.setFillColor(white); c.setFont("Helvetica-Bold", 30)
    ty = img_bottom_y - 16*mm
    words = title.split(); line = ""; lines = []
    for w2 in words:
        test = (line + " " + w2).strip()
        if c.stringWidth(test, "Helvetica-Bold", 30) > (W - 2*MARGIN):
            lines.append(line); line = w2
        else:
            line = test
    lines.append(line)
    for ln in lines:
        c.drawString(MARGIN, ty, ln); ty -= 11*mm
    c.setFont("Helvetica", 12); c.setFillColor(HexColor("#B9B7C4"))
    c.drawString(MARGIN, ty - 3*mm, subtitle)
    c.setFont("Helvetica", 9); c.setFillColor(GREY)
    c.drawString(MARGIN, 12*mm, "Livre blanc cobrandé — Bulldozer × JobTeaser · 2026")

def make_pdf(md_path, out_path, cover_img, chapter_imgs, logo_a, logo_b):
    doc_data = parse_md(md_path)

    def on_first(c, d):
        c.saveState()
        cover_page(c, PAGE_W, PAGE_H, doc_data["title"], doc_data["subtitle"], cover_img, logo_a, logo_b)
        c.restoreState()

    def on_later(c, d):
        c.saveState()
        c.setStrokeColor(LINE); c.setLineWidth(0.6)
        c.line(MARGIN, PAGE_H-14*mm, PAGE_W-MARGIN, PAGE_H-14*mm)
        c.setFont("Helvetica", 8); c.setFillColor(GREY)
        c.drawString(MARGIN, PAGE_H-12*mm, "JobTeaser × Sanofi")
        c.drawRightString(PAGE_W-MARGIN, PAGE_H-12*mm, doc_data["title"][:60])
        c.line(MARGIN, 14*mm, PAGE_W-MARGIN, 14*mm)
        c.drawString(MARGIN, 10*mm, "alexis.samuel@jobteaser.com · 06 08 03 18 36")
        c.drawRightString(PAGE_W-MARGIN, 10*mm, str(d.page))
        if logo_a and os.path.exists(logo_a):
            im = PILImage.open(logo_a); r = im.width/im.height; h=5*mm
            c.drawImage(logo_a, PAGE_W-MARGIN-h*r, 4*mm, width=h*r, height=h, mask='auto')
        c.restoreState()

    doc = SimpleDocTemplate(out_path, pagesize=A4,
                             leftMargin=MARGIN, rightMargin=MARGIN,
                             topMargin=18*mm, bottomMargin=20*mm,
                             title=doc_data["title"])
    story = [PageBreak()]  # page 1 = couverture (dessinée via onFirstPage, sans flowable)
    story.append(Paragraph("ÉDITO DE SYNTHÈSE", STY["kicker"]))
    paras = doc_data["edito"].split("\n\n")
    for i, para in enumerate(paras):
        p = para.strip()
        if not p:
            continue
        if p.startswith("### "):
            story.append(Paragraph(md_inline(p[4:].strip()), STY["h3"]))
        else:
            story.append(Paragraph(md_inline(p), STY["lead"] if i == 0 else STY["body"]))

    for i, ch in enumerate(doc_data["chapters"]):
        story.append(PageBreak())
        story.append(Paragraph(f"CHAPITRE {ch['num']}", STY["kicker"]))
        story.append(Paragraph(md_inline(ch["title"]), STY["h2"]))
        if i < len(chapter_imgs) and chapter_imgs[i] and os.path.exists(chapter_imgs[i]):
            im = PILImage.open(chapter_imgs[i]); r = im.width / im.height
            w = PAGE_W - 2*MARGIN; h = w / r
            story.append(RLImage(chapter_imgs[i], width=w, height=h))
            if ch["brief"]:
                story.append(Paragraph("Illustration — " + md_inline(ch["brief"][:160]) + ("…" if len(ch["brief"])>160 else ""), STY["caption"]))
        if ch["data"]:
            story.append(Paragraph(md_inline(ch["data"]), STY["lead"]))
        for para in ch["text"].split("\n\n"):
            p = para.strip()
            if not p:
                continue
            if p.startswith("### "):
                story.append(Paragraph(md_inline(p[4:].strip()), STY["h3"]))
            else:
                story.append(Paragraph(md_inline(p), STY["body"]))

    if doc_data["conclusion"].strip():
        story.append(PageBreak())
        story.append(Paragraph("CONCLUSION", STY["kicker"]))
        for para in doc_data["conclusion"].split("\n\n"):
            if para.strip():
                story.append(Paragraph(md_inline(para.strip()), STY["body"]))

    story.append(Spacer(1, 6*mm))
    story.append(Paragraph("MÉTHODOLOGIE & SOURCES", STY["kicker"]))
    for para in doc_data["sources"].split("\n\n"):
        if para.strip():
            story.append(Paragraph(md_inline(para.strip()), STY["small"]))

    story.append(Spacer(1, 8*mm))
    story.append(Paragraph("CONTACT", STY["kicker"]))
    story.append(Paragraph(md_inline(doc_data["contact"]).replace("\n", "<br/>"), STY["body"]))

    doc.build(story, onFirstPage=on_first, onLaterPages=on_later)
    return out_path, len(doc_data["chapters"])

if __name__ == "__main__":
    A = "/Users/enguerrandchalvondemersay/jobteaser-abm-landings/content-machine"
    JT_LOGO = f"{A}/assets/logo-emetteur-white_fixed.png"
    SANOFI_LOGO = f"{A}/assets/logo-sanofi-white_fixed.png"
    out1, n1 = make_pdf(f"{A}/wp1_early_careers.md", f"{A}/Livre-Blanc-1_JobTeaser-x-Sanofi.pdf",
                         f"{A}/assets/cover_wp1.jpg",
                         [f"{A}/assets/wp1_ch{i}.jpg" for i in range(1,7)],
                         JT_LOGO, SANOFI_LOGO)
    print("WP1 ->", out1, n1, "chapitres")
    out2, n2 = make_pdf(f"{A}/wp2_ia_paradoxe.md", f"{A}/Livre-Blanc-2_JobTeaser-x-Sanofi.pdf",
                         f"{A}/assets/cover_wp2.jpg",
                         [f"{A}/assets/wp2_ch{i}.jpg" for i in range(1,7)],
                         JT_LOGO, SANOFI_LOGO)
    print("WP2 ->", out2, n2, "chapitres")
