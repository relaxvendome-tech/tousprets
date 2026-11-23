#!/usr/bin/env python3
"""nav_v4.py — Navigation v4 de tousprets.fr (agent 5).

Usage : python3 nav_v4.py /chemin/du/site
A lancer APRES redesign.py. Idempotent : relancer ne change rien.
- remplace <div class="site-head">…</nav> (menu .topnav ou .mainnav) par l'en-tête v4 ;
- ajoute <script src="nav.js" defer></script> une seule fois ;
- copie nav.js (livré à côté de ce script) à la racine du site.
"""
import os, re, sys, shutil

HERE = os.path.dirname(os.path.abspath(__file__))

# (fichier, libellé)
MAIN = [
    ("./", "Accueil"),
    ("kit-de-survie-72h.html", "Se préparer"),
    ("comprendre-s-informer.html", "Comprendre les risques"),
    ("reagir-en-cas-de-crise.html", "Réagir en cas de crise"),
    ("proteger-son-foyer.html", "Protéger sa famille"),
    ("anticiper-s-entraider.html", "S'entraider"),
]
TOOLS = [
    ("diagnostic-suis-je-pret.html", "Suis-je prêt ?"),
    ("checklist-kit-urgence-72h.html", "Ma checklist"),
    ("plan-familial-mise-en-surete.html", "Plan familial"),
    ("glossaire-preparation-crise.html", "Glossaire"),
    ("tous-les-guides.html", "Tous les guides"),
    ("preparation-outre-mer.html", "Outre-mer"),
]
# univers (3e lien du fil d'Ariane, ou page hub hors menu) -> entrée du menu
UNIVERS = {
    "kit-de-survie-72h.html": "kit-de-survie-72h.html",
    "s-equiper-kit-urgence.html": "kit-de-survie-72h.html",
    "comprendre-s-informer.html": "comprendre-s-informer.html",
    "reagir-en-cas-de-crise.html": "reagir-en-cas-de-crise.html",
    "proteger-son-foyer.html": "proteger-son-foyer.html",
    "anticiper-s-entraider.html": "anticiper-s-entraider.html",
    "preparation-outre-mer.html": "preparation-outre-mer.html",
}

SEARCH_SVG = ('<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.2" '
              'stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>')
PHONE_SVG = ('<svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor" aria-hidden="true"><path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.25 11.4 11.4 0 0 0 3.6.57 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.25.2 2.45.57 3.57a1 1 0 0 1-.25 1z"/></svg>')
BURGER_SVG = ('<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2.2" '
              'stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>')
CLOSE_SVG = ('<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2.2" '
             'stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6 6 18"/></svg>')
CHEV_SVG = ('<svg class="mn-chev" viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" '
            'stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg>')


def current_target(fname, html):
    """Renvoie (href ciblé, valeur aria-current) ou (None, None)."""
    hrefs = [h for h, _ in MAIN + TOOLS]
    if fname in hrefs:
        return fname, "page"
    m = re.search(r'<div class="crumbs">(.*?)</div>', html, re.S)
    if m:
        links = re.findall(r'<a href="([^"]+)"', m.group(1))
        if len(links) >= 3 and links[1] == "tous-les-guides.html" and links[2] in UNIVERS:
            return UNIVERS[links[2]], "true"
    if fname in UNIVERS:
        return UNIVERS[fname], "true"
    return None, None


def header(fname, html):
    cur, val = current_target(fname, html)

    def a(href, label, cls=""):
        ac = f' aria-current="{val}"' if href == cur else ""
        c = f' class="{cls}"' if cls else ""
        return f'<a{c} href="{href}"{ac}>{label}</a>'

    items = "".join(f'<li class="mn-i">{a(h, t, "mn-a")}</li>' for h, t in MAIN)
    tools_cur = cur in [h for h, _ in TOOLS]
    sub = "".join(f'<li>{a(h, t, "mn-sa")}</li>' for h, t in TOOLS)
    items += (f'<li class="mn-i mn-sub{" is-cur" if tools_cur else ""}">'
              f'<button class="mn-btn" type="button" aria-expanded="false" aria-controls="mn-outils">Outils pratiques{CHEV_SVG}</button>'
              f'<ul class="mn-subl" id="mn-outils">{sub}</ul></li>')
    return (
        '<div class="site-head"><div class="wrap-w head-in">'
        '<a class="brand" href="./"><img src="icon-192.png" alt="" width="40" height="40"><span class="brand-t"><span class="brand-n">Tous prêts</span>'
        '<span class="brand-s">Se préparer chez soi, d\'après le guide officiel</span></span></a>'
        '<form class="search" role="search" action="tous-les-guides.html"><label class="sr" for="q">Rechercher un guide</label>'
        '<input id="q" name="q" type="search" placeholder="Rechercher : eau, radio, coupure…" autocomplete="off">'
        f'<button type="submit" aria-label="Rechercher">{SEARCH_SVG}</button><ul class="search-res" hidden></ul></form>'
        f'<a class="nav-sos" href="tel:112">{PHONE_SVG}<span class="nav-sos-l">Urgence </span>112<span class="sr"> : appeler les secours</span></a>'
        '<a class="head-cta nav-kit" href="./#app-start">Kit 72 h</a>'
        f'<button class="nav-toggle" type="button" aria-expanded="false" aria-controls="mainnav">{BURGER_SVG}<span>Menu</span></button>'
        '</div></div>'
        '<nav class="mainnav" id="mainnav" aria-label="Navigation principale"><div class="wrap-w mn-in">'
        f'<div class="mn-head"><span class="mn-title">Menu</span><button class="mn-close" type="button">{CLOSE_SVG}<span class="sr">Fermer le menu</span></button></div>'
        f'<ul class="mn-list">{items}</ul></div></nav>'
    )


BLOCK = re.compile(r'<div class="site-head">.*?<nav class="(?:topnav|mainnav)"[^>]*>.*?</nav>', re.S)


def transform(path):
    fname = os.path.basename(path)
    s = open(path, encoding="utf-8").read()
    o = s
    if not BLOCK.search(s):
        return "absent"
    s = BLOCK.sub(lambda m: header(fname, s), s, count=1)
    if 'src="nav.js"' not in s:
        tag = '<script src="nav.js" defer></script>'
        if '<script src="search.js" defer></script>' in s:
            s = s.replace('<script src="search.js" defer></script>', '<script src="search.js" defer></script>\n' + tag, 1)
        else:
            s = s.replace("</head>", tag + "\n</head>", 1)
    if s != o:
        open(path, "w", encoding="utf-8").write(s)
        return "modifié"
    return "inchangé"


def main():
    if len(sys.argv) != 2 or not os.path.isdir(sys.argv[1]):
        sys.exit("Usage : python3 nav_v4.py /chemin/du/site")
    site = sys.argv[1]
    stats = {}
    for f in sorted(os.listdir(site)):
        if not f.endswith(".html"):
            continue
        p = os.path.join(site, f)
        if 'class="site-head"' not in open(p, encoding="utf-8").read():
            continue
        r = transform(p)
        stats.setdefault(r, []).append(f)
    src = os.path.join(HERE, "nav.js")
    if os.path.exists(src) and os.path.abspath(src) != os.path.abspath(os.path.join(site, "nav.js")):
        shutil.copyfile(src, os.path.join(site, "nav.js"))
    for k, v in stats.items():
        print(f"{k} : {len(v)}" + (f" -> {', '.join(v)}" if k == "absent" else ""))


if __name__ == "__main__":
    main()
