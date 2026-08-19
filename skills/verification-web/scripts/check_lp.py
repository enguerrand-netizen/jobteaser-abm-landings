#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
check_lp.py — vérificateur statique EXHAUSTIF d'une landing page HTML (skill verification-web).
Seedé avec les bugs réellement rencontrés en prod. Sans dépendance (Python 3 stock).

Usage:
  python3 check_lp.py page.html [--assets-dir DIR] [--emetteur NOM] [--prospect NOM]
      [--brand "#RRGGBB"] [--accent "#RRGGBB"] [--cta-required]

- --emetteur / --prospect : noms attendus → vérifie qu'ils apparaissent ET signale les
  marques d'exemple parasites (jobteaser/sanofi/loreal…) laissées par le template.
- --brand / --accent : couleurs de marque attendues → vérifie qu'elles sont bien utilisées.
Sortie : rapport par catégorie + score /100 ; code retour 1 s'il reste des BLOCKER/HIGH.
Le rendu VISUEL (hero lisible, halos, mobile) reste à valider au screenshot (voir SKILL.md).
"""
import sys, os, re

# ---------------- utils couleur / contraste WCAG ----------------
def _lin(c):
    c=c/255.0
    return c/12.92 if c<=0.03928 else ((c+0.055)/1.055)**2.4
def luminance(hexc):
    h=hexc.lstrip('#')
    if len(h)==3: h=''.join(ch*2 for ch in h)
    r,g,b=int(h[0:2],16),int(h[2:4],16),int(h[4:6],16)
    return 0.2126*_lin(r)+0.7152*_lin(g)+0.0722*_lin(b)
def contrast(a,b):
    la,lb=luminance(a),luminance(b); hi,lo=max(la,lb),min(la,lb)
    return (hi+0.05)/(lo+0.05)

def get_arg(flag):
    for i,a in enumerate(sys.argv):
        if a==flag and i+1<len(sys.argv): return sys.argv[i+1]
    return None

def main():
    pos=[a for a in sys.argv[1:] if not a.startswith('--')]
    # retirer les valeurs de flags des positionnels
    flagvals=set()
    for f in ('--assets-dir','--emetteur','--prospect','--brand','--accent'):
        v=get_arg(f);
        if v: flagvals.add(v)
    pos=[p for p in pos if p not in flagvals]
    if not pos:
        print("usage: check_lp.py page.html [--assets-dir DIR] [--emetteur NOM] [--prospect NOM] [--brand HEX] [--accent HEX] [--cta-required]"); sys.exit(2)
    path=pos[0]
    assets_dir=get_arg('--assets-dir'); emetteur=get_arg('--emetteur'); prospect=get_arg('--prospect')
    brand=get_arg('--brand'); accent=get_arg('--accent'); cta_required='--cta-required' in sys.argv
    flat='--flat' in sys.argv       # charte "flat" : interdit dégradés / ombres / glow / particules
    font_expected=get_arg('--font') # ex. "GT Pressura" : vérifie sa présence dans le CSS
    base=os.path.dirname(os.path.abspath(path))
    html=open(path,encoding='utf-8',errors='replace').read()
    low=html.lower()
    issues=[]
    def add(cat,sev,code,msg): issues.append((cat,sev,code,msg))

    # ================= CONTENU =================
    toks=sorted(set(re.findall(r'\{\{[^}]+\}\}|\[\[[^\]]+\]\]|%%[^%]+%%|\$\{[^}]+\}',html)))
    if toks: add('Contenu','BLOCKER','template_tokens',"Tokens de template non remplis : "+", ".join(toks[:8]))
    lazy=['à sourcer','a sourcer','à insérer','a inserer','à insérer','à remplacer','a remplacer',
          'de mémoire','de memoire','à confirmer','a confirmer','placeholder','lorem ipsum','lipsum',
          'todo','à compléter','a completer','à définir','a definir','à venir','xxxx','sample text','[à ','(à ']
    hits=sorted({w for w in lazy if w in low})
    if hits: add('Contenu','BLOCKER','lazy_placeholder',"Placeholders/à-faire laissés : "+", ".join(hits))
    # artefacts JS : recherche stricte (éviter les faux positifs type 'nan' dans un mot)
    txt=re.sub(r'<(script|style)[\s\S]*?</\1>',' ',html)   # ignorer JS/CSS
    txt=re.sub(r'<[^>]+>',' ',txt)                          # ne garder que le texte visible
    for pat,label in [(r'\bNaN\b','NaN'),(r'\bundefined\b','undefined'),
                      (r'\[object Object\]','[object Object]'),(r'\bInfinity\b','Infinity')]:
        if re.search(pat,txt): add('Contenu','HIGH','js_artifact',"Artefact JS visible dans le texte : '%s'."%label)
    words=len(re.findall(r'\w+', re.sub(r'<[^>]+>',' ',html)))
    if words<180: add('Contenu','MED','thin_copy',"Copy très courte (~%d mots) : la page risque d'être creuse."%words)
    # répétition grossière : même phrase de +40 car répétée
    sents=re.findall(r'>([^<]{40,})<', html)
    seen={}
    for s in sents:
        k=re.sub(r'\s+',' ',s).strip().lower(); seen[k]=seen.get(k,0)+1
    dups=[k for k,v in seen.items() if v>=3]
    if dups: add('Contenu','LOW','repeated_text',"Texte répété ≥3× (copier-coller ?) : \"%s…\""%dups[0][:40])

    # ============ CONTAMINATION TEMPLATE (marques d'exemple) ============
    # marques d'exemple du template (à ne PAS laisser). NB: filtrées par les marques déclarées.
    example_brands=['jobteaser','sanofi','loreal',"l'oréal"]
    declared=[x.lower() for x in [emetteur,prospect] if x]
    stray=[b for b in example_brands if b in low and not any(b in d or d in b for d in declared)]
    if stray and (emetteur or prospect):
        add('Contenu','HIGH','stray_brand',"Marque d'exemple laissée par le template : "+", ".join(sorted(set(stray)))+" (ne correspond pas à émetteur/prospect déclarés).")
    if emetteur and emetteur.lower() not in low: add('Contenu','HIGH','missing_emetteur',"Le nom de l'émetteur (%s) n'apparaît pas dans la page."%emetteur)
    if prospect and prospect.lower() not in low: add('Contenu','HIGH','missing_prospect',"Le nom du prospect (%s) n'apparaît pas dans la page."%prospect)

    # ================= MARQUE / COULEURS / CONTRASTE =================
    def cssvar(name):
        m=re.search(r'--%s\s*:\s*(#[0-9a-fA-F]{3,6})'%re.escape(name), html)
        return m.group(1) if m else None
    bg=cssvar('bg'); text=cssvar('text'); br=cssvar('brand'); bink=cssvar('brand-ink'); mut=cssvar('muted')
    if bg and text:
        c=contrast(bg,text)
        if c<4.5: add('Couleurs','HIGH','contrast_text',"Contraste texte/fond insuffisant (%.1f:1 < 4.5). %s sur %s."%(c,text,bg))
    if bg and mut:
        c=contrast(bg,mut)
        if c<3.0: add('Couleurs','MED','contrast_muted',"Texte secondaire peu lisible (%.1f:1). %s sur %s."%(c,mut,bg))
    if br and bink:
        c=contrast(br,bink)
        if c<4.0: add('Couleurs','HIGH','contrast_button',"Texte du bouton peu lisible sur le brand (%.1f:1). brand-ink=%s sur brand=%s."%(c,bink,br))
    if brand and brand.lower() not in low: add('Couleurs','HIGH','brand_missing',"Couleur émetteur attendue %s absente du CSS."%brand)
    if accent and accent.lower() not in low: add('Couleurs','MED','accent_missing',"Couleur prospect attendue %s absente du CSS."%accent)
    hexes=sorted(set(re.findall(r'#[0-9a-fA-F]{6}', html)))
    add('Couleurs','INFO','colors',"HEX détectés : "+", ".join(hexes[:14])+(" …" if len(hexes)>14 else "")+"  → chaque couleur de marque doit être SOURCÉE (charte / brand-extractor), pas 'de mémoire'.")

    # ============ CONFORMITÉ CHARTE (do/don't visuels) ============
    if font_expected and font_expected.lower() not in low:
        add('Charte','HIGH','font_missing',"Police de charte attendue absente du CSS : '%s' (police non appliquée)."%font_expected)
    if flat:
        # une charte 'flat' interdit dégradés, ombres, glow/blur, particules/canvas/vidéo déco
        css=' '.join(re.findall(r'<style[\s\S]*?</style>', html, re.I))
        if re.search(r'(linear|radial)-gradient\(', css):
            add('Charte','HIGH','flat_gradient',"Dégradé(s) CSS présents alors que la charte est FLAT (interdit).")
        if re.search(r'box-shadow\s*:\s*(?!none)', css) or re.search(r'text-shadow\s*:\s*(?!none)', css):
            add('Charte','HIGH','flat_shadow',"Ombre(s) (box/text-shadow) présentes alors que la charte est FLAT (interdit).")
        if re.search(r'filter\s*:\s*[^;]*blur|backdrop-filter', css):
            add('Charte','MED','flat_blur',"Effet blur/backdrop présent alors que la charte est FLAT.")
        if '<canvas' in low or ('<video' in low and 'id="scene"' in low) or 'three.min.js' in low:
            add('Charte','MED','flat_particles',"Fond animé/particules/3D présent alors que la charte est minimale/flat.")

    # ================= LIENS / CTA =================
    hrefs=re.findall(r'href="([^"]*)"', html)
    btn_hash=re.search(r'class="btn[^"]*"[^>]*href="#"', html) or re.search(r'href="#"[^>]*class="btn', html)
    if btn_hash: add('Liens/CTA','HIGH','dead_cta',"CTA en href=\"#\" (lien mort). Mettre l'URL de RDV/mailto réelle.")
    if cta_required and not any(h.startswith(('http','mailto:')) for h in hrefs):
        add('Liens/CTA','HIGH','no_real_cta',"Aucun CTA vers une vraie destination (http/mailto).")
    ids=set(re.findall(r'id="([^"]+)"', html))
    for h in hrefs:
        if h.startswith('#') and len(h)>1 and h[1:] not in ids:
            add('Liens/CTA','MED','broken_anchor',"Ancre interne cassée : %s (id absent)."%h)
    for a in re.findall(r'<a\b[^>]*target="_blank"[^>]*>', html):
        if 'rel=' not in a or 'noopener' not in a: add('Liens/CTA','LOW','noopener',"Lien target=_blank sans rel=\"noopener\" (sécurité).")
    for a in re.findall(r'<a\b[^>]*>\s*</a>', html):
        add('Liens/CTA','MED','empty_link',"Lien <a> sans texte (accessibilité/SEO).")

    # ================= ASSETS =================
    refs=re.findall(r'(?:src|href|poster)="([^"]+)"', html)
    local=[r for r in refs if not r.startswith(('http://','https://','#','data:','mailto:','tel:'))]
    missing=[]
    for r in local:
        if not (os.path.exists(os.path.join(base,r)) or (assets_dir and os.path.exists(os.path.join(assets_dir,os.path.basename(r))))):
            missing.append(r)
    if missing: add('Assets','HIGH','missing_assets',"Assets locaux introuvables (cassés) : "+", ".join(sorted(set(missing))[:8]))
    if 'logo.clearbit.com' in low or 'brandfetch' in low or 'logo.dev' in low or 'logo.uplead' in low:
        add('Assets','HIGH','logo_api',"Logos via API tierce (Clearbit/Brandfetch/logo.dev) : souvent 404 → cassés. Fichiers officiels ou lockup texte on-brand.")
    if re.search(r'(src|href)="http://', html): add('Assets','MED','mixed_content',"Ressource(s) en http:// (mixed content sur https).")
    # images distantes autres que data → dépendance réseau
    ext_imgs=[r for r in re.findall(r'<img\b[^>]*src="(https?://[^"]+)"', html)]
    if ext_imgs: add('Assets','LOW','remote_img',"%d image(s) chargée(s) depuis un domaine externe (dépendance/latence)."%len(ext_imgs))

    # ================= ACCESSIBILITÉ =================
    if not re.search(r'<html[^>]+lang=', html, re.I): add('Accessibilité','MED','html_lang',"<html> sans attribut lang.")
    imgs=re.findall(r'<img\b[^>]*>', html, re.I)
    noalt=[i for i in imgs if not re.search(r'\balt=', i)]
    emptyalt=[i for i in imgs if re.search(r'\balt=""', i)]
    if noalt: add('Accessibilité','MED','img_alt',"%d <img> sans attribut alt."%len(noalt))
    if len(emptyalt)>2: add('Accessibilité','LOW','img_alt_empty',"%d <img> avec alt vide."%len(emptyalt))
    h1=re.findall(r'<h1\b', html, re.I)
    if len(h1)==0: add('Accessibilité','HIGH','no_h1',"Aucun <h1> (hiérarchie/SEO).")
    if len(h1)>1: add('Accessibilité','MED','multi_h1',"%d <h1> (devrait être unique)."%len(h1))
    if not re.search(r'<meta[^>]+name="viewport"', html, re.I): add('Accessibilité','HIGH','viewport',"Meta viewport manquant (responsive KO).")

    # ================= TECHNIQUE / PERF =================
    if 'prefers-reduced-motion' not in low and ('@keyframes' in low or 'requestanimationframe' in low or '<video' in low):
        add('Technique','MED','reduced_motion',"Animations présentes sans prise en charge de prefers-reduced-motion.")
    if '<video' in low and 'muted' not in low: add('Technique','MED','video_muted',"Vidéo sans 'muted' → autoplay bloqué par les navigateurs.")
    if '<video' in low and 'playsinline' not in low: add('Technique','LOW','video_playsinline',"Vidéo sans 'playsinline' (plein écran forcé iOS).")
    if '<video' in low and 'poster=' not in low: add('Technique','LOW','video_poster',"Vidéo sans poster (écran noir au chargement).")
    if 'localstorage' in low or 'sessionstorage' in low: add('Technique','HIGH','storage',"localStorage/sessionStorage utilisé (interdit en page autonome/artefact).")
    if '<title' not in low or re.search(r'<title>\s*</title>', low): add('Technique','MED','title',"<title> vide ou absent.")
    else:
        tt=re.search(r'<title>(.*?)</title>', html, re.S)
        if tt and len(tt.group(1))>65: add('Technique','LOW','title_long',"<title> > 65 caractères (tronqué en SERP).")
    if not re.search(r'<meta[^>]+name="description"', html, re.I): add('Technique','LOW','meta_desc',"Meta description absente.")
    if re.search(r'console\.log', html): add('Technique','LOW','console_log',"console.log laissé dans le JS.")
    kb=os.path.getsize(path)//1024
    if kb>6000: add('Technique','MED','weight',"Page lourde (%d Ko) : optimiser images (JPEG q~82 ; PNG pour transparents)."%kb)

    # ================= STRUCTURE / PREUVE =================
    n_sections=len(re.findall(r'<section', low))
    if n_sections<4: add('Structure','MED','thin_page',"Page peu dense (%d <section>) : viser hero+why-now+valeur+preuve+étapes+CTA."%n_sections)
    if 'data-count' not in low: add('Structure','LOW','no_counters',"Pas de compteurs animés (data-count) sur les chiffres.")
    for m in re.findall(r'data-count="([^"]*)"', html):
        if m and not re.match(r'^-?\d+(\.\d+)?$', m): add('Structure','LOW','bad_count',"data-count non numérique : '%s'."%m)
    if not any(w in low for w in ['logos','témoign','temoign','blockquote','avis','note ','⭐']):
        add('Structure','MED','no_proof',"Preuve faible : ni logos, ni témoignage, ni note détectés.")
    if low.count('<img')<1 and 'background-image' not in low and '<video' not in low and '<svg' not in low:
        add('Structure','MED','no_visual',"Aucun visuel (img/video/svg) : page probablement trop textuelle.")

    # ================= MOBILE / RESPONSIVE (mobile-first) =================
    css=' '.join(re.findall(r'<style[\s\S]*?</style>', html, re.I)) or html
    mq=re.findall(r'@media[^{]+', css)
    if not mq:
        add('Mobile','BLOCKER','no_media_query',"AUCUNE media query : la page n'est pas responsive (mobile-first KO).")
    else:
        has_max=any('max-width' in m for m in mq)
        has_min=any('min-width' in m for m in mq)
        if has_min and not has_max:
            add('Mobile','LOW','desktop_first',"Media queries en min-width seulement → OK si vraiment pensé mobile-first (sinon préférer une base mobile).")
        if len(mq)<2: add('Mobile','MED','few_breakpoints',"Un seul breakpoint : prévoir tablette + mobile + petit mobile (≈900/680/400px).")
    # largeurs fixes qui cassent le mobile (width:NNNpx > 480 sans max-width à côté)
    big=[w for w in re.findall(r'[^-]width\s*:\s*(\d{3,})px', css) if int(w)>480]
    if big and 'max-width' not in css:
        add('Mobile','HIGH','fixed_width',"Largeur(s) fixes >480px sans max-width (débordement horizontal probable) : "+", ".join(sorted(set(big))[:5]))
    if 'overflow-x' not in css:
        add('Mobile','LOW','overflowx',"Pas d'overflow-x:hidden global (garde-fou anti-scroll horizontal).")
    # images fluides
    if '<img' in low and 'max-width:100%' not in css.replace(' ','') and 'width:100%' not in css.replace(' ',''):
        add('Mobile','MED','img_fluid',"Images sans max-width:100% : risque de débordement sur petit écran.")
    # CTA mobile sticky (recommandé)
    if 'mobile-cta' not in low and 'position:fixed' not in css.replace(' ',''):
        add('Mobile','LOW','no_sticky_cta',"Pas de CTA mobile sticky détecté (recommandé sur mobile).")
    # nowrap sur potentiellement long
    if re.search(r'white-space\s*:\s*nowrap', css):
        add('Mobile','LOW','nowrap',"white-space:nowrap présent : vérifier que rien ne déborde sur mobile.")
    # taille de police de base
    m=re.search(r'html\s*\{[^}]*font-size\s*:\s*(\d+)px', css)
    if m and int(m.group(1))<15:
        add('Mobile','MED','base_font',"Police de base <15px (%spx) : corps trop petit sur mobile (viser ≥16px)."%m.group(1))

    # ================= SCORE =================
    weights={'BLOCKER':40,'HIGH':14,'MED':6,'LOW':2,'INFO':0}
    score=max(0,100-sum(weights[s] for _,s,_,_ in issues))
    order={'BLOCKER':0,'HIGH':1,'MED':2,'LOW':3,'INFO':4}
    cats=['Contenu','Charte','Couleurs','Mobile','Liens/CTA','Assets','Accessibilité','Technique','Structure']
    print("="*66)
    print("VERIFICATION — %s"%os.path.basename(path))
    print("Score: %d/100  |  %d Ko  |  %d sections  |  %d problèmes"%(score,kb,n_sections,len([i for i in issues if i[1]!='INFO'])))
    print("="*66)
    icon={'BLOCKER':'⛔','HIGH':'🔴','MED':'🟠','LOW':'🟡','INFO':'ℹ️'}
    for cat in cats+['(autres)']:
        grp=[i for i in issues if i[0]==cat] if cat!='(autres)' else [i for i in issues if i[0] not in cats]
        if not grp: continue
        grp.sort(key=lambda x:order[x[1]])
        print("\n### %s"%cat)
        for c,sev,code,msg in grp:
            print("  %s [%s] %s — %s"%(icon[sev],sev,code,msg))
    print("\n"+"-"*66)
    print("À VÉRIFIER AU SCREENSHOT (non automatisable) : hero lisible sur le fond ; pas de halo")
    print("gris (transparents=PNG) ; logos réels visibles ; contraste réel ; mobile 360/390/414.")
    blockers=[i for i in issues if i[1] in ('BLOCKER','HIGH')]
    print("\nVERDICT : "+("❌ NON livrable (%d bloquant/HIGH)"%len(blockers) if blockers else "✅ livrable (sous réserve du QA visuel)"))
    sys.exit(1 if blockers else 0)

if __name__=='__main__':
    main()
