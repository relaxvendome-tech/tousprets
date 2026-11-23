#!/usr/bin/env python3
"""legal_v5.py — En-tête, navigation et pied de page communs pour les pages
qui n'en ont pas (pages légales : sources, mentions légales, confidentialité,
accessibilité, privacy…). Idempotent (marqueur <!-- tp-legal-v5 -->).

Usage : python3 legal_v5.py /chemin/du/site
A lancer AVANT nav_v4.py (qui met ensuite l'en-tête à jour comme partout).
- remplace la feuille de style intégrée par style.css (+ police Inter) ;
- remplace <nav>← Retour…</nav> par lien d'évitement + bandeau + en-tête v4 ;
- entoure le contenu de <main id="contenu" class="pg-legal"><div class="wrap"> ;
- remplace le pied de page minimal par le pied de page commun (copié d'une page
  de référence) en gardant les liens légaux ;
- ajoute og:*, twitter:card et un JSON-LD WebPage s'ils manquent ;
- privacy.html (redirection) : un H1 unique et un seul canonical.
Le contenu légal (<main>) n'est jamais modifié.
"""
import os, re, sys, json, html

HERE = os.path.dirname(os.path.abspath(__file__))
sys.dont_write_bytecode = True
sys.path.insert(0, HERE)
import nav_v4  # noqa: E402

MARK = "<!-- tp-legal-v5 -->"
REFS = ("charte-editoriale.html", "kit-de-survie-72h.html", "pourquoi.html")
BAND = ('<header><div class="band"><div class="wrap"><span>Appli citoyenne indépendante, pas un service de l\'État</span>'
        '<span>Urgence : <a href="tel:112">112</a> · SMS <a href="sms:114">114</a></span></div></div>')
HEADCSS = ('<meta name="theme-color" content="#0F2440">\n'
           '<link rel="icon" type="image/png" sizes="192x192" href="icon-192.png">\n'
           '<link rel="apple-touch-icon" href="apple-touch-icon.png">\n'
           '<link rel="preload" href="fonts/inter-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>\n'
           '<link rel="stylesheet" href="style.css">')


def ref_footer(site):
    for r in REFS:
        p = os.path.join(site, r)
        if os.path.exists(p):
            m = re.search(r'<footer class="site-foot">.*?</footer>', open(p, encoding="utf-8").read(), re.S)
            if m:
                return m.group(0)
    return None


def meta(s, attr, name):
    m = re.search(rf'<meta {attr}="{re.escape(name)}" content="([^"]*)"', s)
    return m.group(1) if m else None


def transform(path, footer):
    fname = os.path.basename(path)
    s = open(path, encoding="utf-8").read()
    o = s
    redirect = 'http-equiv="refresh"' in s
    if MARK not in s:
        # 1. <head> : style intégré -> design system commun
        s = re.sub(r'<meta name="theme-color"[^>]*>\n?', "", s)
        s = re.sub(r'<style>.*?</style>\n?', "", s, count=1, flags=re.S)
        s = s.replace("</head>", HEADCSS + "\n" + MARK + "\n</head>", 1)
        # 2. en-tête : remplace le lien retour (ou s'insère après <body>)
        head = BAND + '<div class="site-head"></div><nav class="mainnav"></nav></header>'
        skip = '<a class="skip" href="#contenu">Aller au contenu</a>\n'
        if re.search(r'<body>\s*<nav>.*?</nav>', s, re.S):
            s = re.sub(r'<body>\s*<nav>.*?</nav>', lambda m: "<body>\n" + skip + head, s, count=1, flags=re.S)
        else:
            s = s.replace("<body>", "<body>\n" + skip + head, 1)
        # 3. contenu
        if "<main>" in s:
            s = s.replace("<main>", '<main id="contenu" class="pg-legal"><div class="wrap">', 1)
            s = s.replace("</main>", "</div></main>", 1)
        else:  # page de redirection : envelopper le contenu restant
            i = s.index("</header>") + len("</header>")
            j = s.index("</body>")
            body = s[i:j].strip()
            s = s[:i] + '\n<main id="contenu" class="pg-legal"><div class="wrap">\n' + body + "\n</div></main>\n" + s[j:]
        # 4. scripts communs
        for js in ("search.js", "nav.js"):
            if f'src="{js}"' not in s:
                s = s.replace("</body>", f'<script src="{js}" defer></script>\n</body>', 1)
    # 5. en-tête v4 (vide au premier passage, puis maintenu par nav_v4)
    s = re.sub(r'<div class="site-head"></div><nav class="mainnav"></nav>',
               lambda m: nav_v4.header(fname, s), s, count=1)
    # 6. pied de page commun (resynchronisé à chaque passage)
    if footer:
        s = re.sub(r'<footer(?: class="site-foot")?>.*?</footer>', lambda m: footer, s, count=1, flags=re.S)
    # 7. métadonnées sociales et JSON-LD
    title = re.search(r"<title>(.*?)</title>", s, re.S).group(1).strip()
    desc = meta(s, "name", "description") or ""
    canon = re.findall(r'<link rel="canonical" href="([^"]*)">', s)
    url = next((c for c in canon if c.startswith("https://")), f"https://tousprets.fr/{fname}")
    if len(canon) > 1:  # un seul canonical, absolu
        s = re.sub(r'<link rel="canonical" href="(?!https://)[^"]*">\n?', "", s)
    add = []
    if 'property="og:title"' not in s:
        add.append('<meta property="og:type" content="website"><meta property="og:locale" content="fr_FR">'
                   '<meta property="og:site_name" content="Tous prêts">'
                   f'<meta property="og:url" content="{url}"><meta property="og:title" content="{title}">'
                   f'<meta property="og:description" content="{desc}">'
                   '<meta property="og:image" content="https://tousprets.fr/og-image.png">')
    if 'name="twitter:card"' not in s:
        add.append('<meta name="twitter:card" content="summary_large_image">')
    if "application/ld+json" not in s and not redirect:
        h1 = re.search(r"<h1[^>]*>(.*?)</h1>", s, re.S)
        name = html.unescape(re.sub("<[^>]+>", "", h1.group(1))) if h1 else html.unescape(title)
        ld = {"@context": "https://schema.org", "@graph": [
            {"@type": "WebPage", "name": name, "description": html.unescape(desc), "url": url, "inLanguage": "fr-FR",
             "isPartOf": {"@type": "WebSite", "name": "Tous prêts", "url": "https://tousprets.fr/"}},
            {"@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Tous prêts", "item": "https://tousprets.fr/"},
                {"@type": "ListItem", "position": 2, "name": name, "item": url}]}]}
        add.append('<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + "</script>")
    if add:
        s = s.replace(MARK, "\n".join(add) + "\n" + MARK, 1)
    # 8. privacy.html (redirection) : H1 unique
    if redirect and "<h1" not in s:
        s = s.replace('<main id="contenu" class="pg-legal"><div class="wrap">\n',
                      '<main id="contenu" class="pg-legal"><div class="wrap">\n<h1>Politique de confidentialité</h1>\n', 1)
    if s != o:
        open(path, "w", encoding="utf-8").write(s)
        return "modifié"
    return "inchangé"


def main():
    if len(sys.argv) != 2 or not os.path.isdir(sys.argv[1]):
        sys.exit("Usage : python3 legal_v5.py /chemin/du/site")
    site = sys.argv[1]
    footer = ref_footer(site)
    stats = {}
    for f in sorted(os.listdir(site)):
        if not f.endswith(".html") or f in ("index.html",) or f.startswith("google"):
            continue
        p = os.path.join(site, f)
        s = open(p, encoding="utf-8").read()
        if MARK not in s and 'class="site-head"' in s:
            continue
        stats.setdefault(transform(p, footer), []).append(f)
    for k, v in stats.items():
        print(f"legal_v5 {k} : {len(v)} -> {', '.join(v)}")


if __name__ == "__main__":
    main()
