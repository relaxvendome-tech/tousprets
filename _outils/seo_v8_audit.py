# -*- coding: utf-8 -*-
"""Audit SEO v8 page par page (lecture seule). Usage : python3 seo_v8_audit.py [SITE] [sortie.json]
Extrait title, description, og/twitter, H1/Hn, canonical, robots, JSON-LD, liens internes
entrants/sortants, profondeur de clic depuis l'accueil, images (alt, dimensions, lazy, poids)."""
import re, os, sys, json, html, glob
from collections import defaultdict, deque

SITE = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = sys.argv[2] if len(sys.argv) > 2 else None
BASE = "https://tousprets.fr/"

def txt(x): return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", x or ""))).strip()
def meta(s, attr, name):
    m = re.search(rf'<meta {attr}="{re.escape(name)}" content="([^"]*)"', s)
    return html.unescape(m.group(1)) if m else None

def url_of(f): return BASE if f == "index.html" else BASE + f

def types_of(j, acc):
    if isinstance(j, dict):
        t = j.get("@type")
        if t: acc.append(t if isinstance(t, str) else "/".join(t))
        for k, v in j.items():
            if k in ("@graph",): types_of(v, acc)
    elif isinstance(j, list):
        for x in j: types_of(x, acc)
    return acc

def main_part(s):
    i = s.find('<main'); j = s.find('</main>')
    return s[i:j] if i >= 0 and j > i else s

pages = sorted(os.path.basename(p) for p in glob.glob(f"{SITE}/*.html"))
R = {}
links_out = {}
ctx_out = {}
for f in pages:
    s = open(f"{SITE}/{f}", encoding="utf-8").read()
    head = s[:s.find("</head>")]
    r = {"page": f}
    t = re.search(r"<title>(.*?)</title>", s, re.S); r["title"] = txt(t.group(1)) if t else ""
    r["description"] = meta(head, "name", "description") or ""
    r["og_title"] = meta(head, "property", "og:title"); r["og_description"] = meta(head, "property", "og:description")
    r["tw_title"] = meta(head, "name", "twitter:title"); r["tw_description"] = meta(head, "name", "twitter:description")
    r["keywords_meta"] = meta(head, "name", "keywords") is not None
    c = re.findall(r'<link rel="canonical" href="([^"]*)"', s); r["canonical"] = c
    r["robots"] = meta(head, "name", "robots") or ""
    r["refresh"] = 'http-equiv="refresh"' in head
    h1 = re.findall(r"<h1[^>]*>(.*?)</h1>", s, re.S); r["h1"] = [txt(x) for x in h1]
    hs = [int(x) for x in re.findall(r"<h([1-6])[\s>]", s)]
    jumps = []
    for a, b in zip(hs, hs[1:]):
        if b > a + 1: jumps.append(f"h{a}>h{b}")
    r["hn"] = "".join(str(x) for x in hs); r["hn_jumps"] = sorted(set(jumps))
    r["h2"] = [txt(x) for x in re.findall(r"<h2[^>]*>(.*?)</h2>", s, re.S)]
    lds = re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S)
    typ, bad, dates = [], 0, {}
    for b in lds:
        try:
            j = json.loads(b); types_of(j, typ)
            for n in (j.get("@graph", [j]) if isinstance(j, dict) else j):
                if isinstance(n, dict):
                    for k in ("datePublished", "dateModified"):
                        if k in n: dates[k] = n[k]
                    if n.get("@type") == "WebSite" and "potentialAction" in n: dates["searchaction"] = True
                    if "aggregateRating" in n or "review" in n: dates["rating"] = True
        except Exception: bad += 1
    r["jsonld_blocks"] = len(lds); r["jsonld_types"] = typ; r["jsonld_invalid"] = bad; r["jsonld_info"] = dates
    hrefs = re.findall(r'href="([^"#?:]*\.html|\./|/)(?:[#?][^"]*)?"', s)
    norm = set()
    for h in hrefs:
        h = "index.html" if h in ("./", "/") else h.lstrip("./")
        if h != f: norm.add(h)
    links_out[f] = norm
    mp = main_part(s)
    # liens contextuels = dans <main>, hors fil d'Ariane et hors précédent/suivant
    mp2 = re.sub(r'<div class="crumbs">.*?</div>', "", mp, flags=re.S)
    mp2 = re.sub(r'<nav class="pn.*?</nav>', "", mp2, flags=re.S)
    ctx = set(h for h in re.findall(r'href="([a-z0-9-]+\.html)', mp2) if h != f)
    ctx_out[f] = ctx
    imgs = re.findall(r"<img\b[^>]*>", s)
    ii = []
    for k, im in enumerate(imgs):
        src = re.search(r'src="([^"]+)"', im); src = src.group(1) if src else ""
        alt = re.search(r'alt="([^"]*)"', im)
        size = os.path.getsize(f"{SITE}/{src}") if src and os.path.exists(f"{SITE}/{src}") else None
        ii.append({"src": src, "alt": None if alt is None else alt.group(1), "wh": ("width=" in im and "height=" in im),
                   "lazy": 'loading="lazy"' in im, "prio": 'fetchpriority="high"' in im, "bytes": size})
    r["images"] = ii
    r["words_main"] = len(txt(re.sub(r"<(script|style|nav)[^>]*>.*?</\1>", "", mp, flags=re.S)).split())
    r["has_essentiel"] = 'class="essentiel"' in s
    r["has_lead"] = 'class="lead"' in s
    r["voir_aussi"] = 'id="voir-aussi"' in s
    r["guides_compl"] = 'id="guides-compl"' in s
    r["prevnext"] = 'class="pn' in s
    r["crumbs"] = 'class="crumbs"' in s
    R[f] = r

inb = defaultdict(set); inb_ctx = defaultdict(set)
for f, outs in links_out.items():
    for o in outs:
        if o in R: inb[o].add(f)
for f, outs in ctx_out.items():
    for o in outs:
        if o in R: inb_ctx[o].add(f)
# profondeur de clic (BFS sur tous les liens, depuis l'accueil)
depth = {"index.html": 0}; q = deque(["index.html"])
while q:
    u = q.popleft()
    for v in links_out.get(u, ()):
        if v in R and v not in depth:
            depth[v] = depth[u] + 1; q.append(v)
for f, r in R.items():
    r["out_links"] = len([x for x in links_out[f] if x in R]); r["out_ctx"] = len(ctx_out[f])
    r["in_links"] = len(inb[f]); r["in_ctx"] = len(inb_ctx[f]); r["depth"] = depth.get(f)
    r["dead_links"] = sorted(x for x in links_out[f] if x not in R and not os.path.exists(f"{SITE}/{x}"))

# sitemap(s)
sm = {}
for p in sorted(glob.glob(f"{SITE}/sitemap*.xml")):
    x = open(p).read()
    sm[os.path.basename(p)] = {"url": len(re.findall(r"<url>", x)), "loc": re.findall(r"<url>\s*<loc>([^<]+)</loc>", x),
                               "images": len(re.findall(r"<image:loc>", x)), "sitemaps": re.findall(r"<sitemap>\s*<loc>([^<]+)", x),
                               "lastmods": sorted(set(re.findall(r"<lastmod>([^<]+)", x)))}
res = {"pages": R, "sitemaps": sm, "robots": open(f"{SITE}/robots.txt").read()}
if OUT: json.dump(res, open(OUT, "w"), ensure_ascii=False, indent=1)
else:
    print(len(R), "pages")
