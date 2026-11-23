#!/usr/bin/env python3
"""Remplace le bloc d'accueil (#landing) et son CSS .lp dans index.html.
Usage : python3 apply_landing.py chemin/vers/index.html [landing.html] [landing.css]
Idempotent : relancé sur un fichier déjà traité, il remplace le bloc v4 par la version courante."""
import re, sys, pathlib

here = pathlib.Path(__file__).resolve().parent
idx = pathlib.Path(sys.argv[1])
html_new = pathlib.Path(sys.argv[2] if len(sys.argv) > 2 else here / 'landing.html').read_text(encoding='utf-8').strip('\n')
css_new = pathlib.Path(sys.argv[3] if len(sys.argv) > 3 else here / 'landing.css').read_text(encoding='utf-8').strip('\n')
s = idx.read_text(encoding='utf-8')

# 1) Bloc HTML : <section class="lp" id="landing" ...> ... </section> (aucune <section> imbriquée)
m = re.search(r'[ \t]*<section class="lp" id="landing"[^>]*>.*?</section>', s, re.S)
if not m:
    sys.exit('ERREUR : bloc <section class="lp" id="landing"> introuvable')
if '<section' in m.group(0)[10:]:
    sys.exit('ERREUR : <section> imbriquée dans #landing, remplacement annulé')
s = s[:m.start()] + html_new + s[m.end():]

# 2) CSS .lp
V4 = re.compile(r'/\* ===== Accueil éditorial v4 \(\.lp\).*?/\* ===== fin accueil v4 \(\.lp\) ===== \*/', re.S)
if V4.search(s):
    s = V4.sub(lambda _: css_new, s, count=1)
else:
    m = re.search(r'^\.lp\{.*?^html\.in-app \.lp\{display:none\}[ \t]*$', s, re.S | re.M)
    if not m:
        sys.exit('ERREUR : ancien CSS .lp introuvable')
    old = m.group(0).splitlines()
    bad = [l for l in old if '.lp' not in l]
    if bad:
        sys.exit('ERREUR : la zone CSS .lp contient des règles étrangères : %r' % bad[:3])
    s = s[:m.start()] + css_new + s[m.end():]

# 3) Contrôles
assert s.count('id="landing"') == 1 and s.count('id="app-start"') == 1, 'ancres en double'
idx.write_text(s, encoding='utf-8')
print('OK : bloc #landing et CSS .lp remplacés dans', idx)
