# -*- coding: utf-8 -*-
"""seo_v8.py — post-traitement SEO v8 de tousprets.fr (idempotent, dernier maillon de redesign.py).
Usage : python3 seo_v8.py /chemin/du/site
Lit _outils/seo_v8.json et applique :
 1. <head> : title, meta description, og:title/description, twitter:title/description/image, suppression
    de meta keywords (ignorée par Google), préchargement de l'image LCP de l'accueil ;
 2. date « Mis à jour le » visible = date_modifiee (git, texte éditorial) ;
 3. ALT de l'image du héros (photo : description ; pictogramme SVG : alt vide, décoratif) ;
 4. JSON-LD : Article / CollectionPage / WebPage avec dates réelles, auteur = Organization « Tous prêts »,
    BreadcrumbList reconstruit depuis le fil d'Ariane visible ; accueil : WebSite (+ SearchAction vers
    tous-les-guides.html?q=), Organization, WebApplication (sans note ni avis) ;
 5. bloc « Guides complémentaires » (3 à 5 liens, sans doublon avec À lire aussi, précédent/suivant, fil d'Ariane) ;
 6. accueil : section statique seo-about (explication + liste de la checklist, lisible sans JS), accroche ;
 7. Tous les guides : filtre visible dès le HTML (évite le décalage de mise en page), masqué sans JS ;
 8. sitemap.xml : URL canoniques indexables, lastmod = date du dernier commit git du fichier, images ;
 9. style.css : bloc « v8 » du bloc Guides complémentaires.
Aucune page, URL, clé localStorage ni consigne de sécurité n'est modifiée."""
import re, os, sys, json, html, subprocess, datetime

SITE = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = json.load(open(os.path.join(SITE, "_outils", "seo_v8.json"), encoding="utf-8"))
BASE = "https://tousprets.fr/"
ORG = {"@type": "Organization", "@id": BASE + "#org", "name": "Tous prêts", "url": BASE}
PUB = dict(ORG, logo={"@type": "ImageObject", "url": BASE + "icon-512.png", "width": 512, "height": 512})
MOIS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"]

def esc(x): return html.escape(x, quote=True)
def txt(x): return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", x or ""))).strip()
def fr_date(d):
    y, m, j = map(int, d.split("-")); return f"{j}{'er' if j == 1 else ''} {MOIS[m-1]} {y}"
def url_of(f): return BASE if f == "index.html" else BASE + f
def ld_dump(j): return '<script type="application/ld+json">' + json.dumps(j, ensure_ascii=False) + "</script>"

def set_meta(s, attr, name, val, after=None):
    tag = f'<meta {attr}="{name}" content="{esc(val)}">'
    pat = rf'<meta {attr}="{re.escape(name)}" content="[^"]*">'
    if re.search(pat, s): return re.sub(pat, lambda m: tag, s, count=1)
    if after and re.search(after, s):
        m = re.search(after, s); return s[:m.end()] + tag + s[m.end():]
    return s

def head_part(s):
    i = s.find("</head>"); return s[:i], s[i:]

def fix_head(s, f, e):
    h, rest = head_part(s)
    h = re.sub(r"<title>.*?</title>", lambda m: f"<title>{esc(e['title'])}</title>", h, count=1, flags=re.S)
    h = set_meta(h, "name", "description", e["description"])
    h = set_meta(h, "property", "og:title", e["title"])
    h = set_meta(h, "property", "og:description", e["description"])
    h = re.sub(r'<meta name="keywords" content="[^"]*">\n?', "", h)
    can = re.findall(r'<link rel="canonical" href="([^"]*)"', h)
    if can: h = set_meta(h, "property", "og:url", can[0])
    if 'name="twitter:card"' in h:
        og_img = re.search(r'<meta property="og:image" content="([^"]*)"', h)
        h = set_meta(h, "name", "twitter:title", e["title"], after=r'<meta name="twitter:card" content="[^"]*">')
        h = set_meta(h, "name", "twitter:description", e["description"], after=r'<meta name="twitter:title" content="[^"]*">')
        if og_img: h = set_meta(h, "name", "twitter:image", og_img.group(1), after=r'<meta name="twitter:description" content="[^"]*">')
    return h + rest

def crumbs_list(s, f):
    m = re.search(r'<div class="crumbs">(.*?)</div>', s, re.S)
    if not m: return None
    parts = [p.strip() for p in m.group(1).split("›")]
    items = []
    for p in parts:
        a = re.search(r'<a href="([^"]*)">(.*?)</a>', p)
        if a:
            href = a.group(1); u = BASE if href in ("./", "/", "index.html") else BASE + href.lstrip("./")
            items.append((txt(a.group(2)), u))
        elif txt(p): items.append((txt(p), url_of(f)))
    out, seen = [], set()
    for n, u in items:
        if u in seen: continue
        seen.add(u); out.append({"@type": "ListItem", "position": len(out) + 1, "name": n, "item": u})
    return out

def fix_ld(s, f, e):
    blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S)
    if len(blocks) != 1: return s
    j = json.loads(blocks[0]); nodes = j.get("@graph", [j])
    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", s, re.S); h1 = txt(h1.group(1)) if h1 else e["title"]
    can = url_of(f); crumbs = crumbs_list(s, f)
    out, seen = [], set()
    for n in nodes:
        t = n.get("@type")
        if t in ("Article", "CollectionPage", "WebPage"):
            img = n.get("image")
            typ = e.get("schema") or ("WebPage" if t == "WebPage" else "Article")
            m = {"@type": typ}
            if typ == "Article": m["headline"] = h1[:110]
            else: m["name"] = h1; m["url"] = can
            m["description"] = e["description"]; m["inLanguage"] = "fr-FR"
            if typ != "WebPage" or 'class="byline"' in s:
                m["author"] = ORG
            m["publisher"] = PUB
            if typ == "WebPage" and 'class="byline"' not in s:
                m["dateModified"] = e["date_modifiee"]
            else:
                m["datePublished"] = e["date_publiee"]; m["dateModified"] = e["date_modifiee"]
            if typ == "Article": m["mainEntityOfPage"] = can
            m["isPartOf"] = {"@type": "WebSite", "@id": BASE + "#site", "name": "Tous prêts", "url": BASE}
            if isinstance(img, dict):
                img = dict(img)
                if e.get("alt_hero"): img["caption"] = e["alt_hero"]
                m["image"] = img
            elif img: m["image"] = img
            n = m
        elif t == "BreadcrumbList" and crumbs:
            n = {"@type": "BreadcrumbList", "itemListElement": crumbs}
        key = (t if t != "ImageObject" else json.dumps(n, sort_keys=True))
        if key in seen: continue  # doublon de schéma
        seen.add(key); out.append(n)
    if crumbs and not any(n.get("@type") == "BreadcrumbList" for n in out):
        out.append({"@type": "BreadcrumbList", "itemListElement": crumbs})
    nj = {"@context": "https://schema.org", "@graph": out}
    return s.replace(blocks[0], json.dumps(nj, ensure_ascii=False), 1)

def fix_byline(s, e):
    # « Vérifié le » : date de la dernière vérification documentée (commits de vérification v6), et non la date de mise à jour
    if e.get("date_verifiee"):
        s = re.sub(r'(<li class="hm-ok">.*?<span>Vérifié le )[^<]*(</span>)', lambda m: m.group(1) + fr_date(e["date_verifiee"]) + m.group(2), s, count=1, flags=re.S)
    return re.sub(r'(<p class="byline">[^\n]*?Mis à jour le )([0-9]{1,2}(?:er)? [a-zéû]+ [0-9]{4})',
                  lambda m: m.group(1) + fr_date(e["date_modifiee"]), s, count=1)

def fix_hero_alt(s, e):
    def rep(m):
        fig = m.group(0)
        alt = e.get("alt_hero") if "img/photos/" in fig else ""
        if alt is None: return fig
        return re.sub(r'(<img\b[^>]*?) alt="[^"]*"', lambda k: k.group(1) + f' alt="{esc(alt)}"', fig, count=1)
    return re.sub(r'<figure class="hero-img">.*?</figure>', rep, s, count=1, flags=re.S)

def block_links(s, start_pat):
    i = s.find(start_pat)
    if i < 0: return set()
    tag = "</section>" if start_pat.startswith("<section") else "</nav>"
    j = s.find(tag, i)
    return set(re.findall(r'href="([a-z0-9-]+)\.html"', s[i:j]))

def fix_compl(s, f, e):
    s = re.sub(r'<nav id="guides-compl".*?</nav>\n?', "", s, flags=re.S)
    cand = e.get("complementaires")
    if not cand: return s
    slug = f[:-5]
    excl = block_links(s, '<section id="voir-aussi"') | block_links(s, '<nav class="pn') | {slug}
    m = re.search(r'<div class="crumbs">(.*?)</div>', s, re.S)
    if m: excl |= set(re.findall(r'href="([a-z0-9-]+)\.html"', m.group(1)))
    # complément automatique : pages de la même famille (ordre éditorial de redesign.UNIV)
    fam = [x for lst in DATA.get("familles", {}).values() if slug in lst for x in lst]
    ok = [c for c in cand if c not in excl and c in DATA["ancres"] and os.path.exists(os.path.join(SITE, c + ".html"))]
    pick = []
    for c in (cand if len(ok) >= 3 else list(cand) + fam):
        if c not in excl and c not in pick and c in DATA["ancres"] and os.path.exists(os.path.join(SITE, c + ".html")):
            pick.append(c)
    pick = pick[:5]
    if len(pick) < 3: return s
    A = DATA["ancres"]
    lis = "".join(f'<li><a href="{c}.html">{esc(A[c])}</a></li>' for c in pick)
    blk = ('<nav id="guides-compl" class="gcompl noprint" aria-labelledby="guides-compl-t">'
           f'<h2 id="guides-compl-t">Guides complémentaires</h2><ul>{lis}</ul></nav>\n')
    for anchor in ('<section id="voir-aussi"', '<nav class="pn', '<p class="report', '<div class="cta-box'):
        k = s.find(anchor)
        if k >= 0: return s[:k] + blk + s[k:]
    return s

def fix_crumbs_self(s, f):
    # fil d'Ariane qui pointe vers la page elle-même (kit-de-survie-72h est aussi la page de sa rubrique)
    return re.sub(rf'(<div class="crumbs">.*?)<a href="{re.escape(f)}">[^<]*</a> › ', r"\1", s, count=1, flags=re.S)

def fix_hub_filter(s):
    s = s.replace('<div class="gfilter noprint" id="gfilter" hidden>', '<div class="gfilter noprint" id="gfilter">', 1)
    ns = '<noscript><style>#gfilter{display:none}</style></noscript>'
    if ns not in s: s = s.replace("</head>", ns + "\n</head>", 1)
    return s

# ---------- accueil ----------
def index_ld(e):
    return {"@context": "https://schema.org", "@graph": [
        {"@type": "WebSite", "@id": BASE + "#site", "url": BASE, "name": "Tous prêts", "inLanguage": "fr-FR",
         "description": "Site citoyen indépendant de préparation aux crises : checklist du kit d'urgence 72 h, réflexes en cas d'alerte, entraide entre voisins.",
         "publisher": {"@id": BASE + "#org"},
         "potentialAction": {"@type": "SearchAction",
                             "target": {"@type": "EntryPoint", "urlTemplate": BASE + "tous-les-guides.html?q={search_term_string}"},
                             "query-input": "required name=search_term_string"}},
        {"@type": "Organization", "@id": BASE + "#org", "name": "Tous prêts", "url": BASE,
         "logo": {"@type": "ImageObject", "url": BASE + "icon-512.png", "width": 512, "height": 512},
         "description": "Initiative citoyenne indépendante et gratuite de préparation aux crises, qui s'appuie sur le guide public « Tous responsables ». Ce n'est pas un service de l'État."},
        {"@type": "WebApplication", "@id": BASE + "#app", "name": "Tous prêts – checklist du kit d'urgence 72 h", "url": BASE,
         "applicationCategory": "LifestyleApplication", "operatingSystem": "Web", "browserRequirements": "Navigateur récent ; fonctionne hors ligne après une première visite",
         "inLanguage": "fr-FR", "isAccessibleForFree": True, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"},
         "description": e["description"],
         "featureList": ["Checklist du kit d'urgence 72 h d'après le guide « Tous responsables »",
                         "Quantités d'eau et de nourriture calculées selon la composition du foyer",
                         "Suivi du stock et des dates", "Réflexes par situation d'urgence",
                         "Fonctionne hors ligne après une première visite",
                         "Sans compte ni publicité, données enregistrées uniquement sur l'appareil"],
         "image": BASE + "icon-512.png", "author": {"@id": BASE + "#org"}, "publisher": {"@id": BASE + "#org"}}]}

def seo_about():
    ck = json.load(open(os.path.join(SITE, "checklist-kit-urgence-72h.json"), encoding="utf-8"))
    cats = "".join(f'<div class="sa-cat"><h3>{esc(c["nom"])}</h3><ul>' + "".join(f"<li>{esc(x)}</li>" for x in c["elements"]) + "</ul></div>"
                   for c in ck["categories"])
    return ('<section class="seo-about" aria-labelledby="seo-about-t" style="max-width:720px;margin:24px auto 8px;padding:0 16px;font-size:15px;line-height:1.6">\n'
            '<h2 id="seo-about-t" style="font-size:20px">Checklist du kit d’urgence 72 h : gratuite, adaptée à votre foyer, utilisable hors ligne</h2>\n'
            '<p>Le guide public « Tous responsables » (SGDSN, novembre 2025) invite chaque foyer à pouvoir tenir 72 heures en autonomie en cas de crise : coupure d’électricité, inondation, tempête… Tous prêts transforme cette recommandation en une checklist simple à cocher.</p>\n'
            '<h3 style="font-size:17px">Comment fonctionne la checklist</h3>\n'
            '<ol><li>Indiquez la composition de votre foyer : les quantités d’eau et de nourriture sont calculées pour vous (repère du guide : 6 litres d’eau par personne pour 72 heures).</li>'
            '<li>Cochez ce que vous avez déjà ; votre niveau de préparation se met à jour.</li>'
            '<li>Suivez votre stock et revenez vérifier votre kit deux fois par an.</li></ol>\n'
            '<p>Tout reste sur votre appareil : pas de compte, pas de publicité, aucune donnée envoyée. Après une première visite, l’appli fonctionne même sans connexion.</p>\n'
            f'<h3 style="font-size:17px">Ce que contient le kit d’urgence 72 h</h3>\n<div class="sa-list">{cats}</div>\n'
            '<p>Vous préférez le papier ? <a href="checklist-kit-urgence-72h.html">Imprimez la checklist du kit d’urgence</a>. Pour aller plus loin : '
            '<a href="kit-de-survie-72h.html">la liste complète expliquée</a>, <a href="combien-eau-stocker-par-personne.html">combien d’eau stocker par personne</a>, '
            '<a href="aliments-sans-cuisson-kit-urgence.html">les aliments sans cuisson</a>, <a href="kit-urgence-72h-famille-appartement-voiture.html">adapter le kit à votre famille</a>, '
            '<a href="coupure-electricite-que-faire.html">que faire en cas de coupure d’électricité</a>, <a href="inondation-que-faire.html">en cas d’inondation</a>, '
            '<a href="questions-reponses-kit-urgence.html">les questions pratiques</a> et <a href="tous-les-guides.html">tous les guides</a>.</p>\n'
            f'<p>Source : {esc(ck["source"])}. Tous prêts est une initiative citoyenne indépendante, pas un service de l’État : suivez toujours les consignes des autorités. Urgence : 112.</p>\n'
            '</section>')

def fix_index(s, e):
    s = fix_head(s, "index.html", e)
    h, rest = head_part(s)
    pre = '<link rel="preload" as="image" href="img/photos/vague-de-froid-que-faire.webp" type="image/webp" fetchpriority="high">'
    if pre not in h and "img/photos/vague-de-froid-que-faire.webp" in rest:
        h = h.replace('<link rel="manifest"', pre + "\n" + '<link rel="manifest"', 1)
    h = re.sub(r'<script type="application/ld\+json">.*?</script>', lambda m: ld_dump(index_ld(e)), h, count=1, flags=re.S)
    s = h + rest
    s = re.sub(r'<section class="seo-about".*?</section>', lambda m: seo_about(), s, count=1, flags=re.S)
    if ".seo-about .sa-list" not in s:
        s = s.replace('<style>.seo-about a{color:var(--text);text-decoration:underline}</style>',
                      '<style>.seo-about a{color:var(--text);text-decoration:underline}.seo-about h3{font-family:inherit;font-weight:700;margin:18px 0 6px}'
                      '.seo-about .sa-list{display:grid;gap:4px 24px;grid-template-columns:repeat(auto-fit,minmax(260px,1fr))}.seo-about .sa-cat h3{font-size:15px;margin:10px 0 2px}'
                      '.seo-about .sa-cat ul{margin:0;padding-left:20px}</style>', 1)
    s = s.replace('<p class="lp-kicker">Préparation aux crises · pour tous les foyers</p>',
                  '<p class="lp-kicker">Kit d’urgence 72 h · checklist gratuite pour tous les foyers</p>', 1)
    return s

# ---------- sitemap ----------
def git_date(f):
    try:
        d = subprocess.run(["git", "-C", SITE, "log", "-1", "--format=%cs", "--", f], capture_output=True, text=True).stdout.strip()
    except Exception: d = ""
    return d or datetime.date.today().isoformat()

def indexable(s, f):
    rob = re.search(r'<meta name="robots" content="([^"]*)"', s)
    if rob and "noindex" in rob.group(1): return False
    if 'http-equiv="refresh"' in s[:s.find("</head>")]: return False
    can = re.findall(r'<link rel="canonical" href="([^"]*)"', s)
    return len(can) == 1 and can[0] == url_of(f)

def build_sitemap(order):
    rows = []
    for f in order:
        s = open(os.path.join(SITE, f), encoding="utf-8").read()
        if not indexable(s, f): continue
        slug = f[:-5]; ims = []
        if os.path.exists(os.path.join(SITE, "img/photos", slug + ".jpg")) and f"img/photos/{slug}." in s:
            ims.append(f"img/photos/{slug}.jpg")
        for q in re.findall(r'<img [^>]*src="(img/qr/[a-z0-9-]+\.png)"', s):  # infographies originales
            if q not in ims and os.path.exists(os.path.join(SITE, q)): ims.append(q)
        img = "".join(f"<image:image><image:loc>{BASE}{q}</image:loc></image:image>" for q in ims)
        rows.append(f"  <url><loc>{url_of(f)}</loc><lastmod>{git_date(f)}</lastmod>{img}</url>")
    x = ('<?xml version="1.0" encoding="UTF-8"?>\n'
         '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n'
         + "\n".join(rows) + "\n</urlset>\n")
    p = os.path.join(SITE, "sitemap.xml")
    if open(p, encoding="utf-8").read() != x: open(p, "w", encoding="utf-8").write(x)
    return len(rows)

CSS = """/* v8 : Guides complémentaires */
.gcompl{margin:2rem 0 1.4rem;padding:1rem 1.2rem;border:1px solid var(--border,#D6DEE8);border-radius:var(--r,12px);background:var(--surface,#fff)}
.gcompl h2{font-size:1.05rem;margin:0 0 .5rem}
.gcompl ul{margin:0;padding-left:1.1rem;columns:2 16rem;column-gap:2rem}
.gcompl li{margin:.25rem 0;break-inside:avoid}
/* contraste du titre « À ne surtout pas faire » : 4,49:1 -> 4,85:1 (thème clair) */
.box--interdit .box-t{color:#B8352A}
@media (prefers-color-scheme:dark){.box--interdit .box-t{color:var(--box-c,var(--danger))}}
/* /v8 */
"""

def fix_css():
    p = os.path.join(SITE, "style.css"); c = open(p, encoding="utf-8").read()
    n = re.sub(r"/\* v8 : Guides complémentaires \*/.*?/\* /v8 \*/\n", "", c, flags=re.S) + CSS
    if n != c: open(p, "w", encoding="utf-8").write(n)

def main():
    P = DATA["pages"]; changed = 0
    for f, e in P.items():
        p = os.path.join(SITE, f)
        if not os.path.exists(p) or f == "privacy.html": continue
        s = open(p, encoding="utf-8").read(); o = s
        if f == "index.html":
            s = fix_index(s, e)
        else:
            s = fix_head(s, f, e)
            s = fix_crumbs_self(s, f)
            s = fix_byline(s, e)
            s = fix_hero_alt(s, e)
            s = fix_ld(s, f, e)
            s = fix_compl(s, f, e)
            if f == "tous-les-guides.html": s = fix_hub_filter(s)
        if s != o:
            open(p, "w", encoding="utf-8").write(s); changed += 1
    sm = open(os.path.join(SITE, "sitemap.xml"), encoding="utf-8").read()
    order = []
    for u in re.findall(r"<loc>(https://tousprets\.fr/[^<]*)</loc>", sm):
        if "/img/" in u: continue
        f = "index.html" if u == BASE else u[len(BASE):]
        if f not in order and os.path.exists(os.path.join(SITE, f)): order.append(f)
    for f in sorted(P):
        if f not in order and os.path.exists(os.path.join(SITE, f)): order.append(f)
    n = build_sitemap(order)
    fix_css()
    print(f"seo_v8 : {changed} pages modifiées, sitemap {n} URL")

if __name__ == "__main__":
    main()
