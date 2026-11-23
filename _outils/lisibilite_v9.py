#!/usr/bin/env python3
"""v9 lisibilité, ergonomie et charge cognitive (idempotent). Dernier maillon de redesign.py.
Usage : python3 lisibilite_v9.py /chemin/du/site
 1. style.css : bloc « v9 » (source _outils/lisibilite_v9.css) toujours en dernier ;
 2. guides : les questions de FAQ qui contiennent une consigne de sécurité restent ouvertes (attribut open) ;
    l'avis « sources officielles » passe juste avant la FAQ (ordre : contenu, erreurs, sources, FAQ, liens) ;
    « L'essentiel » reste avant le sommaire ;
 3. index.html (appli) : bloc CSS « v9 appli » (source lisibilite_v9_app.css), libellé visible « Réglages »,
    noms accessibles des boutons ✕, état vide utile des contacts, progression des scénarios, confirmation
    discrète d'enregistrement (script v9-js, lecture seule : aucune clé localStorage, aucune logique modifiée)."""
import os, re, sys, glob

SITE = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HERE = os.path.dirname(os.path.abspath(__file__))
CSS = open(os.path.join(HERE, "lisibilite_v9.css"), encoding="utf-8").read().strip("\n") + "\n"
APP_CSS = open(os.path.join(HERE, "lisibilite_v9_app.css"), encoding="utf-8").read().strip("\n")
# version compacte dans index.html (la source commentée reste dans _outils) ; marqueurs conservés pour l'idempotence
_body = re.sub(r"/\*.*?\*/", "", APP_CSS, flags=re.S)
_body = re.sub(r"\s*\n\s*", "", _body); _body = re.sub(r"\s*([{};,])\s*", r"\1", _body).replace(";}", "}")
APP_CSS = "/* ===== v9 appli (source : _outils/lisibilite_v9_app.css) ===== */" + _body + "/* /v9 appli */"

# Consigne de sécurité dans une réponse : on ne la cache pas dans un accordéon fermé
SAFE = re.compile(r"(?i)\b(jamais|monoxyde|mortel|mortelle|intoxication|asphyxi\w*|appelez|composez|112|évacue\w*|évacuation"
                  r"|ne (?:pas|surtout)|n['’]utilisez|interdit\w*|immédiatement|danger de mort)\b")


def fix_css():
    p = os.path.join(SITE, "style.css"); c = open(p, encoding="utf-8").read()
    n = re.sub(r"/\* ===== v9 : lisibilité.*?/\* /v9 \*/\n?", "", c, flags=re.S)
    n = n.rstrip("\n") + "\n" + CSS
    if n != c: open(p, "w", encoding="utf-8").write(n); return 1
    return 0


def open_safety(s):
    def rep(m):
        tag, body = m.group(1), m.group(2)
        if re.search(r"\bopen\b", tag): return m.group(0)
        txt = re.sub(r"<summary>.*?</summary>", " ", body, flags=re.S)
        txt = re.sub(r"<[^>]+>", " ", txt)
        if SAFE.search(txt):
            return tag[:-1] + " open>" + body + "</details>"
        return m.group(0)
    return re.sub(r"(<details[^>]*>)(.*?)</details>", rep, s, flags=re.S)


def reorder(s):
    if 'class="toc"' not in s or '<section id="faq"' not in s or 'class="gfilter' in s or re.search(r'<main[^>]*class="[^"]*\bhub\b', s):
        return s
    m = re.search(r'<p class="disclaimer">.*?</p>', s, re.S)
    if m:
        disc = m.group(0)
        f = s.find('<section id="faq"')
        # déjà juste avant la FAQ ?
        if not s[:f].rstrip().endswith(disc):
            s = s[:m.start()] + s[m.end():]
            f = s.find('<section id="faq"')
            s = s[:f] + disc + "\n" + s[f:]
    e = re.search(r'(?:<!-- ess:v4 -->)?<section class="essentiel".*?</section>', s, re.S)
    t = s.find('<nav class="toc"')
    if e and t >= 0 and e.start() > t:
        blk = e.group(0); s = s[:e.start()] + s[e.end():]
        t = s.find('<nav class="toc"'); s = s[:t] + blk + s[t:]
    return s


APP_JS = r"""<script id="v9-js">/* v9 : progression lisible et confirmation d'enregistrement. Lecture seule. */
(function(){
 function $(i){return document.getElementById(i)}
 function font(){try{var f=new FontFace('Inter',"url(fonts/inter-latin-wght-normal.woff2) format('woff2')",{weight:'100 900',display:'swap'});f.load().then(function(x){document.fonts.add(x)},function(){})}catch(e){}}
 if(document.readyState==='complete')font();else addEventListener('load',font);
 var toast,tt;
 function ok(){try{return !!window.localStorage}catch(e){return false}}
 function show(){if(!ok())return;if(!toast){toast=document.createElement('div');toast.className='v9-toast';toast.setAttribute('role','status');document.body.appendChild(toast)}
  toast.textContent='Enregistré sur cet appareil';toast.classList.add('on');clearTimeout(tt);tt=setTimeout(function(){toast.classList.remove('on')},1600)}
 var main=$('contenu');if(!main)return;
 main.addEventListener('change',function(e){var t=e.target;if(t&&t.matches&&t.matches('input,select,textarea')&&!t.closest('#landing'))show()});
 main.addEventListener('click',function(e){var b=e.target&&e.target.closest&&e.target.closest('.stepper button,.hh-btn,.del,.add-row');if(b)setTimeout(show,30)});
 var box=$('v9ScenProg'),sc=$('scenarioContent');
 function prog(){if(!box||!sc)return;var c=sc.querySelectorAll('ul.checklist input[type=checkbox]');if(!c.length){box.hidden=true;return}
  var d=0,next=null;for(var i=0;i<c.length;i++){if(c[i].checked)d++;else if(!next)next=c[i]}
  var r=c.length-d,p=Math.round(d*100/c.length),h='<p class="v9-prog-t"><span><b>'+d+'</b> fait'+(d>1?'s':'')+' sur '+c.length+'</span><span><b>'+r+'</b> à faire</span></p>'
  +'<div class="v9-prog-bar" role="img" aria-label="'+d+' sur '+c.length+' cochés"><i style="width:'+p+'%"></i></div>';
  if(next){var l=sc.querySelector('label[for="'+next.id+'"]'),ph=next.closest('.card'),hd=ph&&ph.querySelector('.card-head');
   h+='<p class="v9-prog-n"><strong>Prochaine étape :</strong> '+(l?l.textContent.replace(/</g,'&lt;'):'')+(hd?' <span>('+hd.textContent.replace(/</g,'&lt;')+')</span>':'')+'</p>'}
  else h+='<p class="v9-prog-n"><strong>Tout est coché pour ce scénario.</strong> Pensez à vérifier les dates deux fois par an.</p>';
  box.innerHTML=h;box.hidden=false}
 if(sc){new MutationObserver(prog).observe(sc,{childList:true});sc.addEventListener('change',prog);prog()}
})();
</script>"""


def fix_index(s):
    # 1. CSS appli : à la fin de la première feuille <style>
    s = re.sub(r"\n?/\* ===== v9 appli.*?/\* /v9 appli \*/", "", s, flags=re.S)
    i = s.find("<style>"); j = s.find("</style>", i)
    s = s[:j].rstrip("\n") + "\n" + APP_CSS + "\n" + s[j:]
    # 2. Réglages : libellé visible
    s = s.replace('aria-label="Réglages" style="background:var(--bg-soft);color:var(--text);"><span aria-hidden="true">⚙️</span></button>',
                  'aria-label="Réglages" style="background:var(--bg-soft);color:var(--text);"><span aria-hidden="true">⚙️</span><span class="v9-lbl">Réglages</span></button>', 1)
    # 3. boutons ✕
    s = s.replace('<button class="clear-search" id="clearGuideSearch">✕</button>',
                  '<button class="clear-search" id="clearGuideSearch" aria-label="Effacer la recherche">✕</button>', 1)
    s = s.replace('<button class="del" data-idx="${idx}">✕</button>',
                  '<button class="del" data-idx="${idx}" aria-label="Supprimer ce contact">✕</button>', 1)
    # 4. état vide des contacts
    s = s.replace("""'<div style="padding:16px;color:var(--text-dim);font-size:13.5px;">Aucun contact enregistré.</div>'""",
                  """'<div class="v9-empty"><strong>Aucun contact enregistré.</strong>Ajoutez au moins un proche à prévenir en cas de crise avec le bouton ci-dessous. Le numéro reste sur cet appareil.</div>'""", 1)
    # 5. progression des scénarios
    if 'id="v9ScenProg"' not in s:
        s = s.replace('<div id="scenarioContent"', '<div id="v9ScenProg" class="v9-prog" hidden></div>\n    <div id="scenarioContent"', 1)
    # 6. script
    s = re.sub(r'<script id="v9-js">.*?</script>\n?', "", s, flags=re.S)
    k = s.rfind("</body>")
    s = s[:k] + APP_JS + "\n" + s[k:]
    return s


# Pages ajoutées en v9 : rattachement aux hubs (générés par hub.py / univers.py, qu'on ne relance pas)
NEW = {"panne-numerique-cyberattaque-72h": ("cyberattaque-que-faire", "reagir",
       "Panne numérique : tenir 72 h", "Paiement par carte bloqué, réseau coupé, rumeurs : les 4 réflexes pour tenir 72 h.")}
XREF = {"cyberattaque-que-faire": ('<p class="xref-v9">Panne générale du réseau ou du paiement par carte : voir '
                                   '<a href="panne-numerique-cyberattaque-72h.html">Panne numérique : tenir 72 h sans réseau ni paiement par carte</a>.</p>')}


def hubs(b, s):
    for slug, (after, univ, t, d) in NEW.items():
        if not os.path.exists(os.path.join(SITE, slug + ".html")) or f'href="{slug}.html"' in s and 'class="gcard" href="' + slug in s:
            continue
        if b not in ("tous-les-guides.html", "reagir-en-cas-de-crise.html"): continue
        m = re.search(r'<a class="gcard" href="' + after + r'\.html"[^>]*>.*?</a>', s, re.S)
        if not m: continue
        attrs = ' data-u="%s" data-p=""' % univ if b == "tous-les-guides.html" else ""
        card = (f'<a class="gcard" href="{slug}.html"{attrs}><picture><source srcset="img/photos/{after}.webp" type="image/webp">'
                f'<img src="img/photos/{after}.jpg" alt="" width="480" height="270" loading="lazy"></picture>'
                f'<span class="gcard-b"><strong>{t}</strong><span>{d}</span></span></a>')
        s = s[:m.end()] + card + s[m.end():]
    if b == "tous-les-guides.html":
        n = len(re.findall(r'<a class="gcard" href="[^"]+" data-u=', s))
        s = re.sub(r"Rechercher parmi les \d+ guides", f"Rechercher parmi les {n} guides", s)
        s = re.sub(r'(<p class="gf-n" id="gf-n"[^>]*>)\d+ guides', lambda m: m.group(1) + f"{n} guides", s)
    return s


def xref(b, s):
    x = XREF.get(b[:-5])
    if x and 'class="xref-v9"' not in s:
        t = s.find('<nav class="toc"')
        if t >= 0: s = s[:t] + x + s[t:]
    return s


def main():
    n = fix_css(); pages = 0; opened = 0
    for f in sorted(glob.glob(os.path.join(SITE, "*.html"))):
        b = os.path.basename(f)
        s = open(f, encoding="utf-8").read(); o = s
        if b == "index.html":
            s = fix_index(s)
        elif b != "privacy.html":
            before = len(re.findall(r"<details[^>]*\bopen\b", s))
            s = open_safety(s); s = reorder(s); s = hubs(b, s); s = xref(b, s)
            opened += len(re.findall(r"<details[^>]*\bopen\b", s)) - before
        if s != o:
            open(f, "w", encoding="utf-8").write(s); pages += 1
    print("lisibilite_v9 : style.css", "modifié" if n else "inchangé", "·", pages, "page(s) modifiée(s) ·", opened, "question(s) de sécurité ouverte(s)")


if __name__ == "__main__":
    main()
