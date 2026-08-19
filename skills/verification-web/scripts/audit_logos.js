/* audit_logos.js — audit de VISIBILITÉ des logos (à exécuter dans le navigateur)
 *
 * Ce que check_lp.py (statique) NE PEUT PAS voir : un logo blanc sur fond blanc,
 * un logo noyé sur une frame claire de vidéo, un lockup sans plaque de fond.
 * Ce script échantillonne les pixels de CHAQUE logo et compare au fond réel.
 *
 * Usage (via javascript_tool / console) : coller tout le fichier. Retourne un rapport JSON.
 * Options : window.__logoSel = ['img.logo', ...] pour cibler ; sinon heuristique large.
 * Pour tester le PIRE cas vidéo : figer la vidéo sur une frame claire AVANT
 *   d'exécuter, ex.  var v=document.querySelector('video'); v.pause(); v.currentTime=2.2;
 */
(function () {
  function bgLum(el) {
    var e = el;
    while (e && e !== document.documentElement) {
      var cs = getComputedStyle(e), b = cs.backgroundColor, m = b && b.match(/[\d.]+/g);
      if (m && (m.length < 4 || +m[3] > 0.5)) {
        if (!(m[0] === '0' && m[1] === '0' && m[2] === '0' && m.length === 3 && b === 'rgba(0, 0, 0, 0)'))
          return (+m[0] + +m[1] + +m[2]) / 3;
      }
      // fond image/vidéo derrière ? on ne peut pas lire ses pixels ici → signaler "média"
      if (cs.backgroundImage && cs.backgroundImage !== 'none' && !cs.backgroundImage.includes('gradient'))
        return 'media';
      e = e.parentElement;
    }
    return null;
  }
  // un logo posé au-dessus d'une <video>/<img> de fond (frères en position absolute) ?
  function overMedia(el) {
    var sec = el.closest('section, header, .hero, [class*="hero"]') || document.body;
    return !!sec.querySelector('video, img[class*="bg"], .hero-bg');
  }
  function probe(img) {
    return new Promise(function (res) {
      var p = new Image();
      p.onload = function () {
        var c = document.createElement('canvas'); c.width = 64; c.height = 24;
        var x = c.getContext('2d'); x.drawImage(p, 0, 0, 64, 24);
        try {
          var d = x.getImageData(0, 0, 64, 24).data, dk = 0, lt = 0, t = 0;
          for (var i = 0; i < d.length; i += 4) { if (d[i + 3] < 20) continue; t++; ((d[i] + d[i + 1] + d[i + 2]) / 3 < 100) ? dk++ : lt++; }
          res({ t: t, dk: dk, lt: lt });
        } catch (e) { res({ error: 'canvas tainted (CORS)' }); }
      };
      p.onerror = function () { res(null); };
      p.crossOrigin = 'anonymous';
      p.src = img.src + (img.src.indexOf('?') < 0 ? '?' : '&') + 'audit=' + Date.now() + Math.random();
    });
  }
  var sel = (window.__logoSel && window.__logoSel.join(',')) ||
    'header img, nav img, footer img, [class*="lockup"] img, [class*="logo"] img, [class*="lk"] img, [class*="cobrand"] img, [class*="brand"] img, [class*="wm"] img';
  var imgs = Array.prototype.slice.call(document.querySelectorAll(sel))
    .filter(function (i) { var r = i.getBoundingClientRect(); return r.width > 4 && r.height > 4 && getComputedStyle(i).display !== 'none'; });
  var seen = new Set(), uniq = [];
  imgs.forEach(function (i) { var k = i.src + '@' + Math.round(i.getBoundingClientRect().top); if (!seen.has(k)) { seen.add(k); uniq.push(i); } });

  return Promise.all(uniq.map(function (img) {
    return probe(img).then(function (pr) {
      var bl = bgLum(img), om = overMedia(img), hasPlate = false;
      // plaque = un ancêtre proche avec bg opaque (dans les 3 niveaux)
      var e = img.parentElement, n = 0;
      while (e && n < 3) { var b = getComputedStyle(e).backgroundColor, m = b && b.match(/[\d.]+/g); if (m && (m.length < 4 || +m[3] > 0.4)) { hasPlate = true; break; } e = e.parentElement; n++; }
      // ratio sombre/opaque : >0.8 = quasi tout foncé ; <0.2 = quasi tout clair ; entre = multicolore (OK)
      var ratio = pr && !pr.error && (pr.dk + pr.lt) ? pr.dk / (pr.dk + pr.lt) : null;
      var logo = ratio == null ? '?' : (ratio > 0.8 ? 'dark' : ratio < 0.2 ? 'light' : 'mixte');
      var verdict;
      if (!pr || pr.error) verdict = '⚠️ non mesurable (' + ((pr && pr.error) || 'load fail') + ')';
      else if (bl === 'media' || (om && !hasPlate)) verdict = '⚠️ SUR MÉDIA sans plaque → figer une frame claire / poser une plaque solide';
      else if (bl == null) verdict = 'ℹ️ fond indéterminé — vérifier à l’œil';
      else if (logo === 'mixte') verdict = 'ℹ️ multicolore — vérifier à l’œil';
      else { var bgLight = bl > 128; verdict = ((logo === 'dark') === bgLight) ? '✅ lisible' : '⚠️ MÊME TON (quasi invisible)'; }
      return { src: (img.getAttribute('src') || '').split('/').pop(), logo: logo, bg: (bl === 'media' ? 'média' : bl == null ? '?' : (bl > 128 ? 'clair' : 'sombre')), plaque: hasPlate, verdict: verdict };
    });
  })).then(function (rows) {
    var bad = rows.filter(function (r) { return r.verdict.indexOf('⚠️') === 0; });
    console.table(rows);
    return { total: rows.length, problemes: bad.length, rows: rows, verdict: bad.length ? '❌ ' + bad.length + ' logo(s) à corriger' : '✅ tous les logos lisibles' };
  });
})();
