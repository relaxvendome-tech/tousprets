#!/usr/bin/env python3
"""Insère « L'essentiel » et « À ne surtout pas faire » dans les guides de risques.
Usage : python3 essentiels.py /chemin/du/site   (idempotent)"""
import html, json, os, sys

SITE = sys.argv[1] if len(sys.argv) > 1 else "."
DATA = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "essentiels.json"), encoding="utf-8"))
M_ESS, M_INT = "<!-- ess:v4 -->", "<!-- int:v4 -->"


def lis(items):
    return "".join(f"<li>{html.escape(x, quote=False)}</li>" for x in items)


def traite(path, d):
    s = open(path, encoding="utf-8").read()
    if M_ESS in s:
        return "déjà fait"
    i = s.find('class="disclaimer"')
    if i < 0 or s.count('id="faq"') != 1:
        return "ERREUR : repères absents"
    fin = s.find("</p>", i) + 4
    ess = (f'{M_ESS}<section class="essentiel" aria-labelledby="ess-t"><h2 id="ess-t">L\'essentiel</h2>'
           f'<ol>{lis(d["essentiel"])}</ol></section>')
    s = s[:fin] + ess + s[fin:]
    j = s.find('<section id="faq"')
    if j < 0:
        j = s.rfind("<section", 0, s.find('id="faq"'))
    inte = (f'{M_INT}<aside class="box box--interdit"><p class="box-t">À ne surtout pas faire</p>'
            f'<ul>{lis(d["interdit"])}</ul></aside>\n')
    s = s[:j] + inte + s[j:]
    t = s.find('class="toc"')
    if t >= 0:
        o = s.find("<ol>", t) + 4
        s = s[:o] + '<li><a href="#ess-t">L\'essentiel</a></li>' + s[o:]
    open(path, "w", encoding="utf-8").write(s)
    return "ok"


for slug, d in DATA.items():
    p = os.path.join(SITE, slug + ".html")
    print(slug, traite(p, d) if os.path.exists(p) else "ABSENT")
