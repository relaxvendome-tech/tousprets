#!/usr/bin/env python3
"""v6_structure.py — post-traitement idempotent de la refonte v6 (structure, pas le texte).

Usage : python3 v6_structure.py /chemin/du/site   (branché en fin de redesign.py)

Ne réécrit aucune phrase des guides : ajoute des blocs et du balisage autour.
- pages.js chargé sur les pages outils (test, tous les guides, questions, glossaire, checklist) ;
- tous-les-guides : avis « sources officielles » déplacé sous le panneau de recherche ;
- questions-reponses : navigation rapide par thème (ancres, nombre de questions) + champ de filtrage ;
  encadré « Appelez le … » sur les réponses qui demandent déjà d'appeler les secours (numéros repris du texte) ;
- glossaire : barre alphabétique (ancres sur les <dt>) + champ de filtrage ;
- checklist : barre de progression, boutons Imprimer / Partager, en-tête d'impression ;
- privacy.html : redirection immédiate (meta refresh 0 + location.replace + lien), noindex,follow ;
- sitemap.xml : jamais privacy.html.
"""
import os, re, sys, html, unicodedata

SITE = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES_JS = '<script src="pages.js" defer></script>'
TOOLS = ("diagnostic-suis-je-pret.html", "tous-les-guides.html", "questions-reponses-kit-urgence.html",
         "glossaire-preparation-crise.html", "checklist-kit-urgence-72h.html")
SEARCH_SVG = ('<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2.2" '
              'stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>')


def txt(h):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", h))).strip()


def fold(c):
    return unicodedata.normalize("NFD", c)[0].upper()


def pages_js(s):
    if PAGES_JS not in s:
        s = s.replace("</body>", PAGES_JS + "\n</body>", 1)
    return s


def hub(s):
    # l'avis « sources officielles » passe sous le panneau de recherche (le champ reste en tête)
    m = re.search(r'(<p class="disclaimer">.*?</p>)(<div class="gfilter)', s, re.S)
    if m and '<section id="faq"' in s:
        disc = m.group(1)
        s = s[:m.start()] + s[m.start(2):]
        s = s.replace('<section id="faq"', disc + '\n<section id="faq"', 1)
    return s


SOS_RE = re.compile(r"(?i)\b(appelez|composez|appeler)\b[^.;]{0,40}?\b(112|15|17|18)\b")


def qa(s):
    # encadré « Appelez le … » : uniquement si la question/réponse demande déjà d'appeler un numéro d'urgence
    def det(m):
        d = m.group(0)
        if 'class="qa-sos"' in d:
            return d
        summ, body = m.group(1), m.group(2)
        if not SOS_RE.search(txt(summ + " . " + body)):
            return d
        nums = []
        for n in re.findall(r"\b(112|15|17|18)\b", txt(body)):
            if n not in nums:
                nums.append(n)
        if not nums:
            return d
        tag = ('<p class="sos-tag"><span class="sos-i" aria-hidden="true">!</span><span>Appelez le '
               + " / ".join(f'<a href="tel:{n}">{n}</a>' for n in nums) + "</span></p>")
        return f'<details class="qa-sos"><summary>{summ}</summary>{tag}{body}</details>'
    s = re.sub(r"<details(?: class=\"qa-sos\")?><summary>(.*?)</summary>(.*?)</details>", det, s, flags=re.S)
    if 'id="qa-tools"' in s:
        return s
    secs = re.findall(r'<section id="([^"]+)" aria-labelledby="[^"]+"><h2[^>]*>(.*?)</h2><div class="faq">(.*?)</div></section>', s, re.S)
    secs = [(i, t, b.count("<details")) for i, t, b in secs if b.count("<details")]
    total = sum(n for _, _, n in secs)
    nav = "".join(f'<li><a href="#{i}">{t} <span class="qa-c">{n}</span></a></li>' for i, t, n in secs)
    tools = (f'<div class="qa-tools" id="qa-tools"><nav class="qa-nav" aria-label="Thèmes des questions"><p class="qa-nav-t">Aller au thème</p><ul>{nav}</ul></nav>'
             f'<div class="lf noprint" hidden><label class="lf-l" for="qaq">Filtrer les {total} questions</label>'
             f'<div class="lf-in">{SEARCH_SVG}<input id="qaq" type="search" placeholder="Ex. : toilettes, médicaments, radio…" autocomplete="off" aria-describedby="qa-n"></div>'
             '<p class="lf-n" id="qa-n" role="status" aria-live="polite"></p>'
             '<div class="lf-empty qa-empty" hidden><p><strong>Aucune question ne correspond.</strong> Essayez un autre mot, '
             'ou cherchez dans <a href="tous-les-guides.html">tous les guides</a>.</p>'
             '<button type="button" class="btn btn-2 qa-reset">Effacer le filtre</button></div></div></div>\n')
    s, k = re.subn(r'<nav class="toc" aria-label="Sommaire">.*?</nav>\n?', lambda m: tools, s, count=1, flags=re.S)
    if not k:
        s = s.replace('<section id="' + secs[0][0] + '"', tools + '<section id="' + secs[0][0] + '"', 1)
    return s


def gloss(s):
    seen = {}

    def dt(m):
        attrs, inner = m.group(1), m.group(2)
        c = fold(txt(inner)[:1] or "#")
        key = "0-9" if c.isdigit() else c.lower()
        if key in seen:
            return m.group(0)
        seen[key] = c if not c.isdigit() else "0-9"
        if 'id="lettre-' in attrs:
            return m.group(0)
        return f'<dt id="lettre-{key}"{attrs}>{inner}</dt>'
    s = re.sub(r"<dt((?:\s+[^>]*)?)>(.*?)</dt>", dt, s, flags=re.S)
    if 'id="gl-tools"' in s:
        return s
    letters = ["0-9"] + [chr(x) for x in range(65, 91)]
    items = "".join((f'<li><a href="#lettre-{l.lower()}">{l}</a></li>' if l.lower() in seen else
                     f'<li><span aria-hidden="true">{l}</span></li>') for l in letters)
    n = len(re.findall(r"<dt[\s>]", s))
    tools = (f'<div class="gl-tools" id="gl-tools"><nav class="gl-az" aria-label="Accès par lettre"><ul>{items}</ul></nav>'
             f'<div class="lf noprint" hidden><label class="lf-l" for="glq">Filtrer les {n} termes</label>'
             f'<div class="lf-in">{SEARCH_SVG}<input id="glq" type="search" placeholder="Ex. : alerte, DICRIM, iode…" autocomplete="off" aria-describedby="gl-n"></div>'
             '<p class="lf-n" id="gl-n" role="status" aria-live="polite"></p>'
             '<div class="lf-empty gl-empty" hidden><p><strong>Aucun terme ne correspond.</strong> Essayez un autre mot, '
             'ou consultez les <a href="questions-reponses-kit-urgence.html">questions pratiques</a>.</p>'
             '<button type="button" class="btn btn-2 gl-reset">Effacer le filtre</button></div></div></div>\n')
    s, k = re.subn(r'<nav class="toc" aria-label="Sommaire">.*?</nav>\n?', lambda m: tools, s, count=1, flags=re.S)
    if not k:
        s = s.replace("<section id=", tools + "<section id=", 1)
    return s


def checklist(s):
    if 'id="ck-tools"' in s:
        return s
    s = re.sub(r'<p class="print-head">.*?</p>\n?', "", s)
    n = len(re.findall(r"<li>", re.search(r'<section id="checklist".*?</section>', s, re.S).group(0)))
    tools = ('<div class="ck-tools noprint" id="ck-tools">'
             f'<div class="ck-prog" hidden><p class="ck-n" id="ck-n">0 élément coché sur {n}</p>'
             f'<div class="dg-bar" role="progressbar" aria-labelledby="ck-n" aria-valuemin="0" aria-valuemax="{n}" aria-valuenow="0"><span></span></div></div>'
             '<div class="ck-btns" hidden><button type="button" class="btn" id="ck-print">Imprimer la checklist</button>'
             '<button type="button" class="btn btn-2 share-btn" id="ck-share"><span class="share-l">Partager la checklist</span></button>'
             '<button type="button" class="linkbtn" id="ck-reset">Tout décocher</button><span class="share-msg" role="status" aria-live="polite"></span></div>'
             '<p class="ck-note" hidden>Les cases cochées sont gardées sur cet appareil uniquement : rien n\'est envoyé.</p></div>\n')
    head = '<p class="print-head">Tous prêts · Checklist du kit d\'urgence 72 h · tousprets.fr/checklist-kit-urgence-72h.html</p>'
    s = s.replace('<section id="checklist"', tools + '<section id="checklist"', 1)
    if 'class="print-head"' not in s:
        s = s.replace('<main id="contenu">', '<main id="contenu">' + head, 1)
    return s


def privacy(s):
    s = re.sub(r'<meta name="robots" content="[^"]*">', '<meta name="robots" content="noindex,follow">', s, count=1)
    if 'name="robots"' not in s:
        s = s.replace("</title>", '</title>\n<meta name="robots" content="noindex,follow">', 1)
    s = re.sub(r'<meta http-equiv="refresh" content="[^"]*">', '<meta http-equiv="refresh" content="0; url=confidentialite.html">', s, count=1)
    if 'http-equiv="refresh"' not in s:
        s = s.replace("</title>", '</title>\n<meta http-equiv="refresh" content="0; url=confidentialite.html">', 1)
    js = '<script>location.replace("confidentialite.html" + location.hash);</script>'
    if js not in s:
        s = s.replace('<meta http-equiv="refresh"', js + '\n<meta http-equiv="refresh"', 1)
    body = ('<h1>Politique de confidentialité</h1>\n'
            '<p class="redir">Cette adresse redirige vers la politique de confidentialité en français : '
            '<a href="confidentialite.html">ouvrir la politique de confidentialité</a>.</p>\n')
    s = re.sub(r'(<main id="contenu" class="pg-legal"><div class="wrap">\n).*?(</div></main>)', lambda m: m.group(1) + body + m.group(2), s, count=1, flags=re.S)
    return s


def sitemap(site):
    p = os.path.join(site, "sitemap.xml")
    s = open(p, encoding="utf-8").read()
    o = s
    s = re.sub(r"[ \t]*<url><loc>https://tousprets\.fr/privacy\.html</loc>.*?</url>\n?", "", s, flags=re.S)
    if s != o:
        open(p, "w", encoding="utf-8").write(s)
        return 1
    return 0


def main():
    n = 0
    for f, fn in (("tous-les-guides.html", hub), ("questions-reponses-kit-urgence.html", qa),
                  ("glossaire-preparation-crise.html", gloss), ("checklist-kit-urgence-72h.html", checklist),
                  ("privacy.html", privacy), ("diagnostic-suis-je-pret.html", None)):
        p = os.path.join(SITE, f)
        if not os.path.exists(p):
            print("v6 : absent", f)
            continue
        s = open(p, encoding="utf-8").read()
        o = s
        if fn:
            s = fn(s)
        if f in TOOLS:
            s = pages_js(s)
        if s != o:
            open(p, "w", encoding="utf-8").write(s)
            n += 1
    n += sitemap(SITE)
    print(f"v6_structure : {n} fichier(s) modifié(s)")


if __name__ == "__main__":
    main()
