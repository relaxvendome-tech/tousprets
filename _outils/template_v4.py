#!/usr/bin/env python3
"""template_v4.py — post-traitement idempotent des pages de guides de tousprets.fr.

À lancer APRÈS redesign.py (et nav_v4.py) :  python3 template_v4.py [chemin_du_site]
(défaut /home/claude/tousprets). Ne traite que les pages ayant class="site-head" et un .hero.

Pour chaque guide :
  1. <link rel="preload"> de la police Inter (avant style.css) ;
  2. ligne méta du héros (<ul class="hero-meta">) : Catégorie (3e lien du fil d'Ariane),
     temps de lecture (mots du <main> / 200, arrondi, min. 1) et « Vérifié le <date du byline> » ;
  3. bloc de partage (.share) avant .report + <script src="share.js" defer> ;
  4. tableaux enveloppés dans <div class="tscroll"> (défilement horizontal sur mobile).
Copie aussi share.js et fonts/ (livrés à côté du script) dans le site s'ils sont absents ou différents.
Relancer le script donne exactement le même résultat (blocs régénérés, jamais dupliqués).
"""
import html
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = 'fonts/inter-latin-wght-normal.woff2'
PRELOAD = f'<link rel="preload" href="{FONT}" as="font" type="font/woff2" crossorigin>'
SCRIPT = '<script src="share.js" defer></script>'

I_CAT = ('<svg aria-hidden="true" viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" '
         'stroke-linecap="round" stroke-linejoin="round"><path d="M3 7h7l2 2h9v10H3z"/></svg>')
I_TIME = ('<svg aria-hidden="true" viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" '
          'stroke-linecap="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>')
I_OK = ('<svg aria-hidden="true" viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.4" '
        'stroke-linecap="round" stroke-linejoin="round"><path d="m5 12 5 5L20 7"/></svg>')
I_SHARE = ('<svg aria-hidden="true" viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" '
           'stroke-linecap="round" stroke-linejoin="round"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/>'
           '<circle cx="18" cy="19" r="3"/><path d="m8.6 13.5 6.8 4M15.4 6.5l-6.8 4"/></svg>')

SHARE = ('<div class="share noprint"><p class="share-t">Ce guide peut aider un proche ?</p>'
         f'<button type="button" class="share-btn">{I_SHARE}<span class="share-l">Partager ce guide</span></button>'
         '<span class="share-msg" role="status" aria-live="polite"></span></div>\n')

RE_META = re.compile(r'<ul class="hero-meta"[^>]*>.*?</ul>\n?', re.S)
RE_SHARE = re.compile(r'<div class="share noprint">.*?</span></div>\n?', re.S)


def words_in_main(s):
    m = re.search(r'<main\b[^>]*>(.*?)</main>', s, re.S)
    if not m:
        return 0
    t = m.group(1)
    t = re.sub(r'<(script|style|svg|noscript)\b.*?</\1>', ' ', t, flags=re.S)
    t = re.sub(r'<[^>]+>', ' ', t)
    t = html.unescape(t)
    return len(re.findall(r"[0-9A-Za-zÀ-ÖØ-öø-ÿŒœ]+(?:['’][0-9A-Za-zÀ-ÖØ-öø-ÿŒœ]+)*", t))


def category(s):
    m = re.search(r'<div class="crumbs">(.*?)</div>', s, re.S)
    if not m:
        return None
    links = re.findall(r'<a href="([^"]+)"[^>]*>(.*?)</a>', m.group(1), re.S)
    if len(links) < 3:
        return None
    return links[2]


def build_meta(s):
    items = []
    cat = category(s)
    if cat:
        href, name = cat
        items.append(f'<li class="hm-cat">{I_CAT}<span>Catégorie : <a href="{href}">{name.strip()}</a></span></li>')
    mins = max(1, round(words_in_main(s) / 200))
    items.append(f'<li class="hm-time">{I_TIME}<span>Lecture : {mins} min</span></li>')
    d = re.search(r'<p class="byline">.*?Mis à jour le ([^<·]+?)\s*(?:<|·)', s, re.S)
    if d:
        items.append(f'<li class="hm-ok">{I_OK}<span>Vérifié le {d.group(1).strip()}</span></li>')
    return '<ul class="hero-meta" aria-label="À propos de ce guide">' + ''.join(items) + '</ul>\n'


def wrap_tables(s):
    out, pos = [], 0
    for m in re.finditer(r'<table\b.*?</table>', s, re.S):
        before = s[max(0, m.start() - 200):m.start()]
        out.append(s[pos:m.start()])
        if re.search(r'<div class="tscroll"[^>]*>\s*$', before):
            out.append(m.group(0))
        else:
            out.append('<div class="tscroll" role="region" tabindex="0" aria-label="Tableau (défilable)">'
                       + m.group(0) + '</div>')
        pos = m.end()
    out.append(s[pos:])
    return ''.join(out)


def process(s):
    # 1. preload police
    if PRELOAD not in s:
        s = s.replace('<link rel="stylesheet" href="style.css">',
                      PRELOAD + '\n<link rel="stylesheet" href="style.css">', 1)
    # 2/3. retirer les blocs générés pour recalculer proprement
    s = RE_META.sub('', s)
    s = RE_SHARE.sub('', s)
    s = wrap_tables(s)
    meta = build_meta(s)
    m = re.search(r'<p class="byline">.*?</p>', s, re.S)
    if m:
        s = s[:m.end()] + meta + s[m.end():]
    else:
        h = re.search(r'</h1>\n?', s)
        if h:
            s = s[:h.end()] + meta + s[h.end():]
    # 3. partage
    for anchor in ('<p class="report', '<div class="cta-box', '</div></main>'):
        i = s.find(anchor)
        if i != -1:
            s = s[:i] + SHARE + s[i:]
            break
    if SCRIPT not in s:
        s = s.replace('</body>', SCRIPT + '\n</body>', 1)
    return s


def sync_assets(site):
    pairs = [(os.path.join(HERE, 'share.js'), os.path.join(site, 'share.js')),
             (os.path.join(HERE, FONT), os.path.join(site, FONT))]
    for src, dst in pairs:
        if not os.path.exists(src):
            print('  ! absent :', src)
            continue
        if not os.path.exists(dst) or open(src, 'rb').read() != open(dst, 'rb').read():
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copyfile(src, dst)
            print('  copié :', os.path.relpath(dst, site))


def main():
    site = sys.argv[1] if len(sys.argv) > 1 else '/home/claude/tousprets'
    sync_assets(site)
    n = 0
    for f in sorted(os.listdir(site)):
        if not f.endswith('.html'):
            continue
        p = os.path.join(site, f)
        s = open(p, encoding='utf-8').read()
        if 'class="site-head"' not in s or not re.search(r'class="hero[ "]', s):
            continue
        new = process(s)
        if new != s:
            open(p, 'w', encoding='utf-8').write(new)
            n += 1
    print(f'template_v4 : {n} page(s) modifiée(s) dans {site}')


if __name__ == '__main__':
    main()
