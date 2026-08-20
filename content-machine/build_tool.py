# -*- coding: utf-8 -*-
import base64, io, os, re, json as _json
from PIL import Image
A = "/Users/enguerrandchalvondemersay/jobteaser-abm-landings/content-machine"
AS = A + "/assets"; OUT = A + "/artifact.html"

def jpg(path, q=76, maxw=None):
    im = Image.open(path).convert("RGB")
    if maxw and im.width > maxw:
        im = im.resize((maxw, int(im.height*maxw/im.width)))
    b = io.BytesIO(); im.save(b, "JPEG", quality=q, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()

def png(path):
    return "data:image/png;base64," + base64.b64encode(open(path, "rb").read()).decode()

def pdf(path):
    return "data:application/pdf;base64," + base64.b64encode(open(path, "rb").read()).decode()

def stamp(key, label):
    return f'<span class="vstamp" data-val="{key}" data-label="{label}"></span>'

def shadow_html(fname):
    h = open(fname, encoding="utf-8").read()
    css = "".join(re.findall(r'<style[^>]*>(.*?)</style>', h, re.S))
    css = re.sub(r'(?<![\w.#-])(?:html\s*,\s*body|body\s*,\s*html|:root|html|body)(?=\s*[,{])', ':host', css)
    m = re.search(r'<body[^>]*>(.*)</body>', h, re.S)
    body = m.group(1) if m else h
    body = re.sub(r'<script[^>]*>.*?</script>', '', body, flags=re.S)
    body = re.sub(r'<link[^>]*>', '', body)
    return "<style>:host{display:block;overflow:hidden}" + css + "</style>" + body

def jsstr(s): return _json.dumps(s).replace("</", "<\\/")

TE_LOGO = png(f"{AS}/logo-sanofi-white_fixed.png")

LPJS = "var LPHTML={a:" + jsstr(shadow_html(f"{A}/lp_sanofi_lite.html")) + "};"

WP1 = pdf(f"{A}/Livre-Blanc-1_JobTeaser-x-Sanofi.pdf")
WP2 = pdf(f"{A}/Livre-Blanc-2_JobTeaser-x-Sanofi.pdf")
COVER1 = jpg(f"{AS}/cover_wp1.jpg", 80, 480)
COVER2 = jpg(f"{AS}/cover_wp2.jpg", 80, 480)

exec(open(f"{A}/roadmap_data.py", encoding="utf-8").read())

# ---------- Créas ----------
CAMP = [
 ("content", "Content", "Employer brand — installer le sujet auprès des candidats.",
  [("cc_content_1", "Le premier biopharma piloté par l'IA à grande échelle"),
   ("cc_content_2", "IA et science ne font plus qu'un chez Sanofi"),
   ("cc_content_3", "5 M étudiants — vos futurs talents R&amp;D, Digital, Commercial")]),
 ("visi", "Visibilité", "Reach + crédibilité sur le compte Sanofi.",
  [("cc_visi_1", "800+ écoles partenaires · 5 M étudiants · 10 pays européens"),
   ("cc_visi_2", "Sanofi × OpenAI × Formation Bio — une première en pharma"),
   ("cc_visi_3", "Le bon réseau pour les profils science + data")]),
 ("conv", "Conversion", "Le dernier mètre vers le RDV — sourcing ciblé, offre concrète.",
  [("cc_conv_1", "Les profils hybrides science + data se font rares"),
   ("cc_conv_2", "Sourcer vos talents Early Careers, dès aujourd'hui"),
   ("cc_conv_3", "30 minutes pour cadrer votre plan Early Careers 2026")]),
]
def ccamp(key, t):
    return f'<figure class="g"><img src="{jpg(f"{AS}/creas_final/{key}.jpg", 74, 640)}" alt="{t}"><figcaption>{t}{stamp("cr_"+key, "Créa — "+t)}</figcaption></figure>'
def camp_sub(i, cid, name, desc, items):
    g = "".join(ccamp(*it) for it in items)
    on = " on" if i == 0 else ""
    return f'<div id="s-{cid}" class="sub{on}"><p class="sintro">{desc}</p><div class="gal">{g}</div></div>'
camp_tabs = "".join(f'<button class="subtab{" act" if i==0 else ""}" onclick="showSub(\'s-{c[0]}\',event)">{c[1]}<span class="cbadge">{len(c[3])}</span></button>' for i, c in enumerate(CAMP))
camp_subs = "".join(camp_sub(i, *c) for i, c in enumerate(CAMP))

# ---------- Roadmap ----------
sprint_html = "".join(
 f'<div class="spr"><div class="sprh"><b>{n}</b><span>{w}</span></div><div class="sprm">{m}</div><h4>{t}</h4><p>{d}</p>'
 f'<div class="sprc"><span class="sprcl">POINT D\'ÉTAPE À VALIDER</span>{cp}</div>{stamp("spr_"+n.lower().replace(" ","_"), "Roadmap — "+n+" : "+t)}</div>'
 for n, w, m, t, d, cp in SPRINTS)
OWN = {"bdz": ("Bulldozer", "o-b"), "jt": ("JobTeaser", "o-j"), "mix": ("Commun", "o-m")}
def lev_row(name, who, cls, vals):
    lbl, ocls = OWN[cls]
    cells = "".join(f'<td><span class="lv lv{v}"></span></td>' for v in vals)
    return f'<tr><th class="lvn">{name}</th><td class="lvo"><span class="own {ocls}">{lbl}</span></td>{cells}</tr>'
swim_html = "".join(lev_row(*l) for l in LEVERS)
def month_block(m, t, b, c, auds, creakeys, acts):
    a = "".join(f'<span class="chip">{x}</span>' for x in auds)
    g = "".join(f'<img src="{jpg(f"{AS}/creas_final/{k}.jpg", 60, 150)}" alt="créa">' for k in creakeys)
    li = "".join(f'<li>{x}</li>' for x in acts)
    return (f'<div class="mblock {c}"><div class="mbh"><div><div class="rmt">{m}</div><div class="rmf">{t}</div></div><div class="rmbud">{b}</div></div>'
            f'<div class="mbs"><span class="mbl">AUDIENCES</span><div class="chips">{a}</div></div>'
            f'<div class="mbs"><span class="mbl">CRÉAS MOBILISÉES</span><div class="mcreas">{g}</div></div>'
            f'<div class="mbs"><span class="mbl">CE QU\'ON FAIT</span><ul class="rl">{li}</ul></div></div>')
months_html = "".join(month_block(*m) for m in MONTHS)
_mx = max(v for _, v, _ in WEEKS)
week_bars = "".join(f'<div class="wk"><span class="wkb{" cond" if c else ""}" style="height:{round(v/_mx*100)}%"></span><span class="wkl">{w}</span></div>' for w, v, c in WEEKS)

# ---------- Webinaire ----------
def webi_card(i, wid, title, tag, data, persona, promesse, ads):
    a = "".join(f'<div class="wad"><span class="wadt">{t}</span><b>{acc}</b><p>{cp}</p><div class="wadf"><span class="wcta">{cta}</span><em>Direction visuelle — {vis}</em></div></div>' for t, acc, cp, cta, vis in ads)
    return (f'<div class="wcard"><div class="wch"><span class="wtag">{tag}</span><label class="pick"><input type="radio" name="webinar-choice" value="{title}"> Thème retenu</label></div>'
            f'<h3>{title}</h3><p class="wdata">{data}</p><div class="wmeta"><span><b>Cible</b> — {persona}</span><span><b>Promesse</b> — {promesse}</span></div>'
            f'<details class="wads"><summary>Voir les 3 ads associées →</summary>{a}</details>{stamp("web_"+wid, "Webinaire — "+title)}</div>')
webi_html = "".join(webi_card(i, *w) for i, w in enumerate(WEBI))

# ---------- Audience ----------
AUD_FONCTION = [("Exploitation", 23), ("Recherche", 13), ("Ingénierie", 9), ("Technologies de l'information", 8), ("Ventes", 8)]
AUD_NIVEAU = [("Jeune diplômé", 41), ("Expérimenté", 30), ("Directeur", 11), ("Manager", 11), ("Non payé (stage/alternance)", 2)]
AUD_ORGANIC = [("R&amp;D / Science / Clinique", "25-30%"), ("Digital / Data / IA", "15%"), ("Manufacturing / Supply Chain / Qualité / Ingénierie", "18-20%"), ("Commercial / Sales / Marketing / Access", "15%"), ("Médical (Medical Affairs)", "8-10%"), ("Fonctions corporate (RH, Legal, Finance, Stratégie, Achats)", "10%")]
def aud_bar(label, pct):
    return f'<div class="abar"><span class="abl">{label}</span><div class="abt"><div class="abf" style="width:{pct}%"></div></div><span class="abv">{pct}%</span></div>'
aud_fonction_html = "".join(aud_bar(*x) for x in AUD_FONCTION)
aud_niveau_html = "".join(aud_bar(*x) for x in AUD_NIVEAU)
aud_organic_html = "".join(f'<div class="abar"><span class="abl">{l}</span><span class="abv" style="min-width:70px;text-align:right">{p}</span></div>' for l, p in AUD_ORGANIC)

# ---------- À valider ----------
VAL = [("livrables","Valider les livrables","2 livres blancs, 9 créas, 1 landing (pilote), webinaire — ce qui est OK / à retravailler."),
 ("charte","Retour charte graphique","Couleurs Sanofi (violet #7A00E6 sourcé), JobTeaser (mint #5BFF77 sourcé), logos, ton."),
 ("landing","Landing pilote","Retours sur le contenu et les CTA de la page « Recrutez les jeunes talents qui feront la Sanofi de demain »."),
 ("webinar","Webinaire IA &amp; biopharma","Quelle thématique parmi les 6 ? Intervenants, date visée."),
 ("budget","Budget &amp; seuil go/no-go","OK sur ~500 €/mois M1-M2, règle M3 (scale si probant, sinon pause) ?"),
 ("bdr","Fiche BDR","Alexis Samuel — coordonnées confirmées. Photo présente (assets/alexis-samuel.jpg) : à valider pour usage nominatif."),
 ("audience","Audience LinkedIn","Voir l'onglet Audience — 2 040 profils organiques (OS) + ciblage pub Campaign Manager (32k, France). Pas encore de compte pub Sanofi dédié dans l'OS."),
 ("cobranding","Accord co-branding Sanofi","Feu vert Sanofi pour logo, nom, chiffres (positionnement IA, 294 M$…) dans des créas publiques ?"),
 ("autres","Autres retours","Tout élément utile de la part de JobTeaser.")]
val_html = "".join(f'<div class="vitem"><label class="vh">{t}</label><p class="vd">{d}</p><textarea data-fb="{k}" placeholder="Vos retours…"></textarea></div>' for k, t, d in VAL)
VAL_JS = "{" + ",".join(f'{k}:{_json.dumps(t)}' for k, t, _ in VAL) + "}"

CSS = """
*{box-sizing:border-box}
#tool{--green:#5BFF77;--green-d:#0E9E43;--purple:#7A00E6;--red:#7A00E6;--ink:#14131A;--grey:#5A5A66;--line:#E7E4EF;font-family:-apple-system,'Helvetica Neue',Arial,sans-serif;color:#14131A;background:#f7f6fa}
#tool .wrap{max-width:980px;margin:0 auto;padding:0 24px}
#tool .topbar{background:var(--ink);color:#fff;padding:18px 0}
#tool .topbar .wrap{display:flex;align-items:center;gap:14px;flex-wrap:wrap}
#tool .brand{font-weight:800;font-size:16px}
#tool .sub{color:#8f8d9c;font-size:12px}
#tool .fb{margin-left:auto;background:var(--green);color:var(--ink);font-weight:800;font-size:13px;padding:9px 16px;border-radius:20px;border:0;cursor:pointer}
#tool .tabs{display:flex;gap:4px;overflow-x:auto;background:#fff;border-bottom:1px solid var(--line)}
#tool .tab{background:none;border:0;padding:16px 14px;font-weight:700;font-size:13.5px;color:var(--grey);cursor:pointer;white-space:nowrap;border-bottom:3px solid transparent}
#tool .tab.act{color:var(--ink);border-bottom-color:var(--green-d)}
#tool .panel{display:none;padding:34px 0 60px}
#tool .panel.on{display:block}
#tool .stitle{font-size:11px;font-weight:800;letter-spacing:.08em;color:var(--green-d)}
#tool .shead{font-size:28px;font-weight:800;margin:6px 0 14px}
#tool .sintro{color:var(--grey);font-size:14.5px;max-width:700px;margin-bottom:20px}
#tool .subtabs{display:flex;gap:8px;margin-bottom:20px;border-bottom:1px solid var(--line)}
#tool .subtab{background:none;border:0;padding:10px 4px;margin-right:14px;font-weight:700;color:var(--grey);cursor:pointer;border-bottom:2px solid transparent}
#tool .subtab.act{color:var(--ink);border-bottom-color:var(--purple)} #tool .sub{display:none} #tool .sub.on{display:block}
#tool .cbadge{display:inline-block;margin-left:7px;background:#efeef4;color:var(--grey);font-size:11px;font-weight:800;padding:1px 7px;border-radius:10px}
#tool .abar{display:flex;align-items:center;gap:10px;margin-bottom:10px}
#tool .abl{width:270px;flex:0 0 270px;font-size:13px;color:var(--ink);font-weight:600}
#tool .abt{flex:1;height:10px;background:#efeef4;border-radius:6px;overflow:hidden}
#tool .abf{height:100%;background:var(--green-d);border-radius:6px}
#tool .abv{width:44px;flex:0 0 44px;text-align:right;font-weight:800;font-size:13px}
#tool .aud-src{font-size:11px;color:var(--grey);margin:4px 0 22px}
#tool .subtab.act .cbadge{background:var(--purple);color:#fff}
#tool .gal{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
#tool .gal figure{margin:0;background:#fff;border:1px solid var(--line);border-radius:12px;overflow:hidden}
#tool .gal img{width:100%;display:block}
#tool .gal figcaption{padding:10px 12px;font-size:12.5px;color:#33333b}
#tool .vstamp{display:block;margin-top:8px}
#tool .vb{border:1px solid var(--line);background:#fff;border-radius:14px;padding:4px 10px;font-size:11px;font-weight:800;margin-right:6px;cursor:pointer;color:var(--grey)}
#tool .vb.ok.on{background:#EAF7EE;border-color:var(--green-d);color:var(--green-d)}
#tool .vb.rw.on{background:#F3EAFE;border-color:var(--purple);color:var(--purple)}
#tool .devs{display:flex;gap:30px;align-items:flex-end;flex-wrap:wrap;justify-content:center;max-width:100%}
#tool .devs>*{min-width:0;max-width:100%}
#tool .lpv{background:#fff;border:1px solid var(--line);border-radius:16px;padding:22px;margin-bottom:20px}
#tool .lpvh{display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;flex-wrap:wrap;gap:8px}
#tool .lpvh span{color:var(--grey);font-weight:400}
#tool .pick{font-size:12.5px;color:var(--grey)}
#tool .laptop{width:600px;max-width:100%} #tool .lbar{background:#e8e6ef;border-radius:10px 10px 0 0;padding:8px 12px;display:flex;gap:6px}
#tool .lbar i{width:9px;height:9px;border-radius:50%;background:#c9c6d4;display:inline-block}
#tool .lscreen{width:100%;height:400px;overflow-y:auto;overflow-x:hidden;border:1px solid #d6d2e0;background:#fff}
#tool .lscreen .lpshot{width:1300px;height:auto;border:0}
#tool .lbase{height:10px;background:#d6d2e0;border-radius:0 0 6px 6px}
#tool .phone{width:232px;border:9px solid #1a1720;border-radius:36px;background:#1a1720;position:relative;box-shadow:0 14px 34px rgba(0,0,0,.2)}
#tool .pnotch{position:absolute;top:0;left:50%;transform:translateX(-50%);width:90px;height:18px;background:#1a1720;border-radius:0 0 12px 12px;z-index:2}
#tool .pscreen{width:214px;height:430px;overflow-y:auto;overflow-x:hidden;border-radius:27px;background:#fff}
#tool .pscreen .lpshot{width:390px;height:auto;border:0}
#tool .dlabel{text-align:center;font-size:11px;color:var(--grey);margin-top:8px;font-weight:700}
#tool .lpcta{text-align:center;margin-top:16px}
#tool .btn{background:var(--green);color:var(--ink);font-weight:800;border:0;border-radius:22px;padding:11px 20px;cursor:pointer;font-size:13.5px}
@media(max-width:680px){#tool .devs{gap:22px}#tool .laptop{width:100%}#tool .lscreen{height:340px}}
#tool #lpov{display:none;position:fixed;inset:0;background:#0e0d12;z-index:99999;overflow:auto}
#tool #lpovx{position:fixed;top:14px;right:16px;z-index:100000;background:var(--green);color:var(--ink);border:0;border-radius:22px;padding:10px 18px;font-weight:800;cursor:pointer}
#tool .lpfull{width:1300px;max-width:100%;margin:0 auto;background:#fff}
#tool .wp{display:flex;gap:18px;background:#fff;border:1px solid var(--line);border-radius:14px;padding:16px;margin-bottom:14px}
#tool .wp img{width:110px;border-radius:8px}
#tool .badge{display:inline-block;background:#f0eff4;color:var(--grey);font-size:10.5px;font-weight:800;padding:3px 9px;border-radius:12px;margin-bottom:6px}
#tool .wcards{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:22px}
@media(max-width:900px){#tool .wcards{grid-template-columns:1fr}}
#tool .wcard{background:#fff;border:1px solid var(--line);border-radius:14px;padding:18px}
#tool .wch{display:flex;align-items:center;justify-content:space-between;gap:10px}
#tool .wtag{font-size:10.5px;font-weight:800;letter-spacing:.06em;text-transform:uppercase;color:var(--purple);background:#F3EAFE;padding:3px 9px;border-radius:12px}
#tool .wdata{font-size:12.6px;color:var(--grey);border-left:3px solid var(--green);padding-left:10px;margin:8px 0 10px}
#tool .wmeta{display:grid;gap:4px;font-size:12.6px;color:#33333b;margin-bottom:10px}
#tool .wads{border-top:1px solid var(--line);padding-top:10px}
#tool .wads summary{cursor:pointer;font-weight:800;font-size:13px;color:var(--green-d)}
#tool .wad{background:#faf9fc;border:1px solid var(--line);border-radius:10px;padding:12px;margin-top:10px}
#tool .wadt{font-size:10.5px;font-weight:800;text-transform:uppercase;color:var(--grey)}
#tool .wad b{display:block;font-size:14px;margin:4px 0} #tool .wad p{margin:0;font-size:12.8px;color:#33333b}
#tool .wadf{margin-top:8px;display:flex;flex-wrap:wrap;gap:8px;align-items:center}
#tool .wcta{background:var(--green);color:var(--ink);font-weight:800;font-size:11.5px;padding:3px 10px;border-radius:12px}
#tool .wadf em{font-style:normal;font-size:11.5px;color:var(--grey)}
#tool .sprints{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
@media(max-width:900px){#tool .sprints{grid-template-columns:1fr 1fr}} @media(max-width:600px){#tool .sprints{grid-template-columns:1fr}}
#tool .spr{background:#fff;border:1px solid var(--line);border-radius:14px;padding:15px;border-top:4px solid var(--green-d)}
#tool .sprh{display:flex;justify-content:space-between;font-size:11px;font-weight:800;color:var(--grey)}
#tool .sprm{font-size:10.5px;color:var(--purple);font-weight:800;margin-top:2px}
#tool .spr h4{font-size:16px;margin:6px 0} #tool .spr p{font-size:12.8px;color:#33333b;margin:0 0 10px}
#tool .sprc{background:#F6FBF7;border:1px dashed #9ad8ab;border-radius:10px;padding:10px;font-size:12.4px;color:#1d4b2c}
#tool .sprcl{display:block;font-size:9.5px;font-weight:800;color:var(--green-d);margin-bottom:4px}
#tool .swimwrap{overflow-x:auto} #tool .swim{width:100%;border-collapse:collapse;min-width:760px;background:#fff;border:1px solid var(--line);border-radius:12px}
#tool .swim th,#tool .swim td{padding:9px 10px;border-bottom:1px solid var(--line);text-align:center;font-size:12.6px}
#tool .swim thead th{background:#faf9fc;font-size:11px;color:var(--grey);font-weight:800}
#tool .swim .lvn{text-align:left;font-weight:700;min-width:220px} #tool .swim .lvo{min-width:120px}
#tool .lv{display:inline-block;width:26px;height:14px;border-radius:4px;background:#eceaf2}
#tool .lv1{background:#C8EBD1} #tool .lv2{background:#6FE08C} #tool .lv3{background:var(--green-d)}
#tool .own{font-size:10.5px;font-weight:800;padding:3px 9px;border-radius:12px;white-space:nowrap}
#tool .o-b{background:#EAF7EE;color:#0E9E43} #tool .o-j{background:#F3EAFE;color:var(--purple)} #tool .o-m{background:#f0eff4;color:var(--grey)}
#tool .mblocks{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
@media(max-width:900px){#tool .mblocks{grid-template-columns:1fr}}
#tool .mblock{background:#fff;border:1px solid var(--line);border-radius:14px;padding:16px;border-top:5px solid var(--green-d)}
#tool .mblock.p{border-top-color:var(--purple)}
#tool .mbh{display:flex;justify-content:space-between;margin-bottom:12px}
#tool .mbs{margin-bottom:12px} #tool .mbl{display:block;font-size:9.5px;font-weight:800;color:var(--grey);margin-bottom:6px}
#tool .chips{display:flex;flex-wrap:wrap;gap:6px}
#tool .chip{background:#f2f0f7;color:#33333b;font-size:11.5px;padding:4px 9px;border-radius:12px}
#tool .mcreas{display:flex;flex-wrap:wrap;gap:6px} #tool .mcreas img{width:54px;height:54px;object-fit:cover;border-radius:7px;border:1px solid var(--line)}
#tool .rl{margin:0;padding-left:16px} #tool .rl li{font-size:12.6px;margin:5px 0;color:#33333b}
#tool .rmt{font-size:11px;font-weight:800;color:var(--grey)} #tool .rmf{font-size:19px;font-weight:900;margin:2px 0 8px}
#tool .rmbud{font-size:20px;font-weight:900;color:var(--green-d)} #tool .mblock.p .rmbud{color:var(--purple)}
#tool .acard{background:#fff;border:1px solid var(--line);border-radius:14px;padding:18px;margin-top:16px}
#tool .wchart{display:flex;align-items:flex-end;gap:8px;height:150px;margin-top:14px;padding-bottom:22px;border-bottom:1px solid var(--line)}
#tool .wk{flex:1;display:flex;flex-direction:column;align-items:center;height:100%;justify-content:flex-end;position:relative}
#tool .wkb{width:100%;max-width:34px;background:linear-gradient(180deg,#5BFF77,#0E9E43);border-radius:5px 5px 0 0;min-height:4px}
#tool .wkb.cond{background:linear-gradient(180deg,#B266F0,#7A00E6);opacity:.85}
#tool .wkl{position:absolute;bottom:-18px;font-size:10px;color:var(--grey)}
#tool .pending{background:#F3EAFE;border:1px dashed #C79EF0;border-radius:12px;padding:18px;font-size:13.5px;color:#4a1a7a}
#tool .vitem{margin-bottom:20px} #tool .vh{font-weight:800;display:block;margin-bottom:4px}
#tool .vd{font-size:12.8px;color:var(--grey);margin-bottom:8px}
#tool textarea{width:100%;min-height:70px;border:1px solid var(--line);border-radius:10px;padding:10px;font-family:inherit;font-size:13px}
#tool .fbbar{margin-top:20px;display:flex;align-items:center;gap:12px}
#tool .vsum{font-size:13px;color:var(--grey);margin-bottom:16px}
#tool .foot{background:var(--ink);color:#8f8d9c;font-size:12px;padding:22px 0;text-align:center}
"""

HTML = f"""<div id="tool">
<style>{CSS}</style>
<div class="topbar"><div class="wrap">
  <div><div class="brand">JobTeaser × Sanofi</div><div class="sub">Content Machine — ABM · Bulldozer</div></div>
  <button class="fb" id="fb-open">💬 Laisser un retour</button>
</div></div>
<div class="tabs wrap">
  <button class="tab act" data-t="paid" onclick="showTab('t-paid',event)">Stratégie &amp; Roadmap</button>
  <button class="tab" data-t="landing" onclick="showTab('t-landing',event)">Landing page</button>
  <button class="tab" data-t="content" onclick="showTab('t-content',event)">Content</button>
  <button class="tab" data-t="crea" onclick="showTab('t-crea',event)">Créa</button>
  <button class="tab" data-t="webi" onclick="showTab('t-webi',event)">Webinar</button>
  <button class="tab" data-t="audience" onclick="showTab('t-audience',event)">Audience</button>
  <button class="tab" data-t="val" onclick="showTab('t-val',event)">À valider</button>
</div>

<div id="t-paid" class="panel on"><div class="wrap">
  <div class="stitle">STRATÉGIE &amp; ROADMAP</div><div class="shead">Cibler Sanofi, du reach au rendez-vous</div>
  <p class="sintro">Pilote volontairement petit (~<b>500 €/mois</b>), 6 sprints de 2 semaines. On préchauffe (Content/Visibilité), on entre en relation avant l'outbound, on convertit — et au mois 3 on décide de scaler ou de mettre en pause.</p>
  <div class="stitle" style="margin-top:6px">LES 6 SPRINTS</div><div class="shead" style="font-size:20px">Points d'étape toutes les 2 semaines</div>
  <div class="sprints">{sprint_html}</div>
  <div style="margin-top:34px" class="stitle">PLAN PAR LEVIER</div><div class="shead" style="font-size:20px">Intensité de chaque levier, sprint par sprint</div>
  <div class="swimwrap"><table class="swim"><thead><tr><th class="lvn">Levier</th><th class="lvo">Pilote</th><th>S1</th><th>S2</th><th>S3</th><th>S4</th><th>S5</th><th>S6</th></tr></thead><tbody>{swim_html}</tbody></table></div>
  <div style="margin-top:34px" class="stitle">LE DÉTAIL MOIS PAR MOIS</div><div class="shead" style="font-size:20px">Audiences, créas et actions</div>
  <div class="mblocks">{months_html}</div>
  <div class="acard"><h4>Le budget dans le temps (par semaine)</h4><p class="mut">~500 €/mois engagés M1-M2. Mois 3 (<span style="color:var(--purple);font-weight:800">violet</span>) conditionnel — scale si probant, sinon pause.</p><div class="wchart">{week_bars}</div></div>
</div></div>

<div id="t-landing" class="panel"><div class="wrap">
  <div class="stitle">LANDING PAGE · PILOTE</div><div class="shead">Aperçu desktop &amp; mobile</div>
  <p class="sintro">Landing réelle, cobrandée (charte Sanofi violet #7A00E6 + JobTeaser mint #5BFF77 sourcées), dans un écran d'ordinateur et un smartphone.</p>
  <div class="lpv">
    <div class="lpvh"><b>Variante pilote</b> <span>« Recrutez les jeunes talents qui feront la Sanofi de demain »</span></div>
    <div class="devs">
      <div class="laptop"><div class="lbar"><i></i><i></i><i></i></div><div class="lscreen"><div class="lpshot" data-lp="a"></div></div><div class="lbase"></div><div class="dlabel">ORDINATEUR</div></div>
      <div><div class="phone"><div class="pnotch"></div><div class="pscreen"><div class="lpshot" data-lp="a"></div></div></div><div class="dlabel">SMARTPHONE</div></div>
    </div>
    <div class="lpcta"><button class="btn" onclick="openLP('a')">🖥 Ouvrir en grand →</button></div>
  </div>
  <div class="acard"><p class="mut">Version allégée pour cet outil (vidéo hero → image statique, images compressées). La version complète (vidéo incluse) est disponible dans <code>lp-jobteaser-sanofi/index-standalone.html</code>.</p></div>
</div></div>

<div id="t-content" class="panel"><div class="wrap">
  <div class="stitle">CONTENT</div><div class="shead">Les livrables de fond</div>
  <div class="wp"><img src="{COVER1}" alt="Livre blanc 1"><div><span class="badge">LIVRE BLANC Nº1 · 17 P.</span><h3>Cinq pipelines Early Careers, un seul vivier de talents ?</h3><p>Le sourcing mutualisé des 4 pipelines Early Careers de Sanofi. 6 sources.</p><a class="btn" href="{WP1}" download="Livre-Blanc-1_JobTeaser-x-Sanofi.pdf">Télécharger (PDF) →</a>{stamp("wp1","Livre blanc nº1")}</div></div>
  <div class="wp"><img src="{COVER2}" alt="Livre blanc 2"><div><span class="badge">LIVRE BLANC Nº2 · 16 P.</span><h3>Le paradoxe de l'IA à grande échelle</h3><p>Le dossier décideur : ce que le pari technologique de Sanofi engage pour sa stratégie talents. 6 sources.</p><a class="btn" href="{WP2}" download="Livre-Blanc-2_JobTeaser-x-Sanofi.pdf">Télécharger (PDF) →</a>{stamp("wp2","Livre blanc nº2")}</div></div>
</div></div>

<div id="t-crea" class="panel"><div class="wrap">
  <div class="stitle">CRÉA</div><div class="shead">Les visuels d'activation</div>
  <p class="sintro">9 créas rangées par campagne. Chaque campagne a son objectif, son budget et ses cibles (voir Stratégie &amp; Roadmap).</p>
  <div class="subtabs">{camp_tabs}</div>
  {camp_subs}
</div></div>

<div id="t-webi" class="panel"><div class="wrap">
  <div class="stitle">WEBINAR · IA &amp; BIOPHARMA</div><div class="shead">Le temps fort de fin de mois 2</div>
  <p class="sintro">Un webinaire <b>secteur biopharma/IA</b> programmé fin du mois 2. Sélectionnez une thématique : ses 3 ads sont déjà écrites.</p>
  <div class="wcards">{webi_html}</div>
</div></div>

<div id="t-audience" class="panel"><div class="wrap">
  <div class="stitle">AUDIENCE</div><div class="shead">Qui est réellement Sanofi sur LinkedIn</div>
  <p class="sintro">Deux sources réelles et sourcées : l'audience organique (salariés Sanofi identifiés via l'OS Bulldozer) et l'audience publicitaire (ciblage LinkedIn Campaign Manager, testé en direct — aucune campagne enregistrée ni lancée).</p>

  <div class="acard">
    <h4>Audience organique — 2 040 profils Sanofi identifiés</h4>
    <p class="mut">Scraping LinkedIn via l'OS Bulldozer (job du 22/07/2026). Répartition estimée sur un échantillon de ~220 profils.</p>
    {aud_organic_html}
    <p class="aud-src">Source : OS Bulldozer, bdzListLinkedInEmployees, companyLinkedInId=sanofi, 2 040 profils au total.</p>
  </div>

  <div class="acard">
    <h4>Audience publicitaire — ciblage LinkedIn Campaign Manager</h4>
    <p class="mut"><b>32 000+ personnes</b> ciblables en France sur le critère « Sanofi » (poste actuel). 97% de l'audience travaille dans une entreprise de + de 10 000 employés — cohérent avec le groupe.</p>
    <div class="stitle" style="margin-top:18px;font-size:10px">RÉPARTITION PAR FONCTION</div>
    {aud_fonction_html}
    <div class="stitle" style="margin-top:18px;font-size:10px">RÉPARTITION PAR NIVEAU HIÉRARCHIQUE</div>
    {aud_niveau_html}
    <p class="aud-src">Source : LinkedIn Campaign Manager (compte BULLDOZER), ciblage test « Noms d'entreprises = Sanofi », France, 20/08/2026. Brouillon non enregistré, aucune campagne créée. Comptes similaires suggérés par LinkedIn : Roche, Boehringer Ingelheim, GSK, Abbott.</p>
  </div>

  <div class="acard"><p class="mut">41% « jeune diplômé » confirme un vivier Early Careers solide (cohérent avec le Livre blanc nº1). 22% Directeur+Manager valide la cible décisionnaire de l'approche ABM. Pas encore de compte pub LinkedIn dédié Sanofi dans l'OS — le compte existant (B2B France) est la marque JobTeaser générique.</p></div>
</div></div>

<div id="t-val" class="panel"><div class="wrap">
  <div class="stitle">À VALIDER · RETOURS JOBTEASER</div><div class="shead">Vos commentaires, au même endroit</div>
  <p class="sintro">Laissez vos retours ci-dessous. Validez chaque contenu (✓ / À revoir) dans les onglets Créa et Webinar.</p>
  <div class="vsum" id="vsum"></div>
  {val_html}
  <div class="fbbar"><button class="btn" id="fb-export">⬇︎ Exporter les retours</button><span id="fb-status"></span></div>
</div></div>

<div class="foot">JobTeaser × Sanofi — Bulldozer · 2026 · Outil de travail &amp; validation.</div>
</div>
<script>
(function(){{
 {LPJS}
 document.querySelectorAll('#tool .lpshot').forEach(function(el){{
   var k=el.getAttribute('data-lp');
   try{{ if(!el.shadowRoot) el.attachShadow({{mode:'open'}}); el.shadowRoot.innerHTML=LPHTML[k]; }}
   catch(e){{ el.parentElement.innerHTML='<div style="padding:16px;font:14px system-ui">Aperçu non disponible. Utilisez « Ouvrir en grand ».</div>'; }}
 }});
 window.fitLP=function(){{
   document.querySelectorAll('#tool .lscreen > .lpshot').forEach(function(h){{ var w=h.parentElement.clientWidth; if(w>0) h.style.zoom=(w/1300); }});
   document.querySelectorAll('#tool .pscreen > .lpshot').forEach(function(h){{ var w=h.parentElement.clientWidth; if(w>0) h.style.zoom=(w/390); }});
 }};
 fitLP();
 window.addEventListener('resize', function(){{ clearTimeout(window._fitT); window._fitT=setTimeout(fitLP,120); }});
 window.addEventListener('load', fitLP);

 window.openLP=function(k){{
   var ov=document.getElementById('lpov');
   if(!ov){{ ov=document.createElement('div'); ov.id='lpov'; ov.innerHTML='<button id="lpovx" type="button">✕ Fermer</button><div id="lpovc"></div>'; document.getElementById('tool').appendChild(ov);
     ov.querySelector('#lpovx').onclick=function(){{ov.style.display='none';document.documentElement.style.overflow='';}}; }}
   var c=ov.querySelector('#lpovc'); c.innerHTML='';
   var host=document.createElement('div'); host.className='lpfull'; c.appendChild(host);
   try{{ host.attachShadow({{mode:'open'}}).innerHTML=LPHTML[k]; }}catch(e){{}}
   ov.style.display='block'; ov.scrollTop=0; document.documentElement.style.overflow='hidden';
 }};

 window.showTab=function(id,ev){{
   document.querySelectorAll('#tool .panel').forEach(function(p){{p.classList.remove('on')}});
   document.getElementById(id).classList.add('on');
   document.querySelectorAll('#tool .tab').forEach(function(t){{t.classList.remove('act')}});
   if(ev) ev.currentTarget.classList.add('act');
   if(window.fitLP) setTimeout(window.fitLP,0);
 }};
 window.showSub=function(id,ev){{
   var par=ev.currentTarget.closest('.wrap');
   par.querySelectorAll('.sub').forEach(function(s){{s.classList.remove('on')}});
   document.getElementById(id).classList.add('on');
   ev.currentTarget.parentNode.querySelectorAll('.subtab').forEach(function(t){{t.classList.remove('act')}});
   ev.currentTarget.classList.add('act');
 }};

 var KEY='abm_sanofi_fb_v2';
 function load(){{try{{return JSON.parse(localStorage.getItem(KEY)||'{{}}')}}catch(e){{return{{}}}}}}
 function save(d){{try{{localStorage.setItem(KEY,JSON.stringify(d))}}catch(e){{}}}}
 var data=load();
 var CS=(function(){{try{{return JSON.parse(localStorage.getItem('abm_sanofi_cs_v2')||'{{}}')}}catch(e){{return {{}};}}}})();
 function renderSum(){{var e=document.getElementById('vsum');if(!e)return;var o=0,r=0,k;for(k in CS){{if(CS[k]==='ok')o++;else if(CS[k]==='rw')r++;}}e.innerHTML='<b>'+o+'</b> contenu(s) validé(s) · '+r+' à revoir — boutons ✓/À revoir sur chaque créa &amp; webinaire.';}}
 function saveCS(){{try{{localStorage.setItem('abm_sanofi_cs_v2',JSON.stringify(CS));}}catch(e){{}}renderSum();}}
 document.querySelectorAll('#tool .vstamp').forEach(function(el){{
   var k=el.getAttribute('data-val');
   el.innerHTML='<button type="button" class="vb ok">✓ Validé</button><button type="button" class="vb rw">À revoir</button>';
   var ok=el.querySelector('.ok'),rw=el.querySelector('.rw');
   function paint(){{ok.classList.toggle('on',CS[k]==='ok');rw.classList.toggle('on',CS[k]==='rw');}}
   ok.onclick=function(){{if(CS[k]==='ok')delete CS[k];else CS[k]='ok';saveCS();paint();}};
   rw.onclick=function(){{if(CS[k]==='rw')delete CS[k];else CS[k]='rw';saveCS();paint();}};
   paint();
 }});
 renderSum();
 document.querySelectorAll('[data-fb]').forEach(function(el){{
   if(data[el.getAttribute('data-fb')]) el.value=data[el.getAttribute('data-fb')];
   el.addEventListener('input', function(){{data[el.getAttribute('data-fb')]=el.value;save(data);}});
 }});
 document.querySelectorAll('input[name=webinar-choice]').forEach(function(r){{
   if(data.webinar_choice===r.value)r.checked=true;
   r.addEventListener('change',function(){{data.webinar_choice=r.value;save(data);}});
 }});
 var btn=document.getElementById('fb-export');
 if(btn) btn.addEventListener('click', async function(){{
   var d=load(); var L={VAL_JS};
   var out=['# Retours JobTeaser × Sanofi','',(d.webinar_choice?('Webinaire retenu : '+d.webinar_choice):'Webinaire : (non précisé)'),''];
   Object.keys(L).forEach(function(k){{out.push('## '+L[k]);out.push(d[k]?d[k]:'—');out.push('')}});
   var txt=out.join('\\n');
   try{{
     if(window.claude&&window.claude.downloads){{ await window.claude.downloads.save({{filename:'retours-jobteaser-sanofi.md', data: txt}}); document.getElementById('fb-status').textContent='Exporté ✓'; }}
     else{{ document.getElementById('fb-status').textContent='Export indisponible ici — copiez le texte manuellement.'; }}
   }}catch(e){{ document.getElementById('fb-status').textContent='Export annulé.'; }}
 }});
 document.getElementById('fb-open').onclick=function(){{ showTab('t-val'); document.querySelectorAll('#tool .tab').forEach(function(t){{t.classList.toggle('act', t.getAttribute('data-t')==='val')}}); }};
}})();
</script>
"""

open(OUT, "w", encoding="utf-8").write(HTML)
print("tool artifact.html ->", round(os.path.getsize(OUT)/1024/1024, 2), "MB")
