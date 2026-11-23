"""Identité v7 : logo SVG, nom « Tous prêts » plus grand, mentions déplacées en bas de page. Idempotent.
Usage : python3 brand_v7.py <site>"""
import re, sys, os, glob

site = sys.argv[1] if len(sys.argv) > 1 else '.'
TAG = "Se préparer chez soi, d'après le guide public « Tous responsables »."
n = 0

for f in glob.glob(os.path.join(site, '*.html')):
    s = open(f, encoding='utf-8').read()
    t = s
    # 1. Logo et nom dans l'en-tête des guides
    t = t.replace('<a class="brand" href="./"><img src="icon-192.png" alt="" width="40" height="40">',
                  '<a class="brand" href="./" aria-label="Tous prêts, accueil"><img src="logo.svg" alt="" width="44" height="44">')
    # 2. Retirer la mention sous le nom
    t = re.sub(r'<span class="brand-s">.*?</span>', '', t)
    # 3. Mention en bas du pied de page
    if 'class="site-foot"' in t and 'class="foot-tag"' not in t:
        t = re.sub(r'(<footer class="site-foot">.*?)(</div></footer>)',
                   lambda m: m.group(1) + '<p class="foot-tag">' + TAG + '</p>' + m.group(2), t, count=1, flags=re.S)
    if os.path.basename(f) == 'index.html':
        t = t.replace('<div class="brand"><span style="font-size:19px;" aria-hidden="true">🧭</span><p class="brand-name">Tous prêts</p></div>',
                      '<div class="brand"><img src="logo.svg" alt="" width="38" height="38" class="brand-logo"><p class="brand-name">Tous prêts</p></div>')
        m = re.search(r'\n\s*<p class="note" style="margin:0 0 10px;font-size:12px;color:var\(--text-dim\);">(Appli citoyenne indépendante.*?)</p>', t)
        if m:
            t = t.replace(m.group(0), '', 1)
            t = t.replace('\n    <p class="note home-foot-note">' + m.group(1) + '</p>\n', '\n')
            note = '<p class="note home-foot-note">' + m.group(1) + '</p>'
            i = t.find('<section class="seo-about"')
            j = t.find('</section>', i) + len('</section>')
            t = t[:j] + note + t[j:]
        # déplacement d'une version précédente placée en fin d'accueil
        m2 = re.search(r'\n\s*<p class="note home-foot-note">(.*?)</p>\n', t)
        if m2 and t.find('<section class="seo-about"') > m2.start():
            t = t.replace(m2.group(0), '\n', 1)
            i = t.find('<section class="seo-about"'); j = t.find('</section>', i) + len('</section>')
            t = t[:j] + '<p class="note home-foot-note">' + m2.group(1) + '</p>' + t[j:]
        if '/* brand v7 */' not in t:
            t = t.replace('</style>', '/* brand v7 */\n.topbar .brand .brand-name{font-family:var(--sans,Inter,system-ui,sans-serif)!important;font-weight:800!important;font-size:26px!important;letter-spacing:-.02em;color:#0F2440}\n.topbar .brand-logo{width:38px;height:38px;border-radius:9px;display:block}\n@media (prefers-color-scheme:dark){.topbar .brand .brand-name{color:#fff}}\n.home-foot-note{max-width:720px;margin:20px auto 96px!important;padding:0 16px;font-size:12px!important;color:var(--text-dim)!important;text-align:center}\nhtml.in-app .home-foot-note{margin-top:16px!important}\n</style>', 1)
    if t != s:
        open(f, 'w', encoding='utf-8').write(t)
        n += 1
print('brand_v7 :', n, 'page(s)')
