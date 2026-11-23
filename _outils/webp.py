#!/usr/bin/env python3
"""webp.py — Tous prêts v4 (agent 4).

Usage : python3 webp.py /chemin/du/site [--quality 78] [--lazy]

1. Génère img/photos/X.webp (même taille, qualité ~78) à côté de chaque img/photos/X.jpg
   (régénère seulement si le .webp est absent ou plus ancien que le .jpg). Les JPG ne sont
   jamais réécrits (métadonnées intactes).
2. Dans chaque page *.html à la racine du site, remplace
     <img src="img/photos/X.jpg" ...>
   par
     <picture><source srcset="img/photos/X.webp" type="image/webp"><img src="img/photos/X.jpg" ...></picture>
   en conservant l'élément <img> tel quel (width/height/alt/loading/fetchpriority).
   Les .svg, img/qr, img/cards et les URL absolues (JSON-LD, og:image) ne sont pas touchés.

Option --lazy : ajoute loading="lazy" decoding="async" aux <img> img/photos qui n'ont ni
loading ni fetchpriority (cartes « Voir aussi » sous la ligne de flottaison). Le héros
(fetchpriority="high") n'est jamais modifié.

Idempotent : une <img> déjà précédée d'un <source> dans un <picture> n'est pas re-enveloppée.
"""
import argparse
import os
import re
import sys

from PIL import Image

IMG_RE = re.compile(r'<img\b[^>]*?\bsrc="(img/photos/([A-Za-z0-9._-]+)\.jpe?g)"[^>]*>', re.I)


def make_webps(site, quality):
    pdir = os.path.join(site, 'img', 'photos')
    made, kept = 0, 0
    if not os.path.isdir(pdir):
        return made, kept
    for name in sorted(os.listdir(pdir)):
        base, ext = os.path.splitext(name)
        if ext.lower() not in ('.jpg', '.jpeg'):
            continue
        src = os.path.join(pdir, name)
        dst = os.path.join(pdir, base + '.webp')
        if os.path.exists(dst) and os.path.getmtime(dst) >= os.path.getmtime(src):
            kept += 1
            continue
        with Image.open(src) as im:  # lecture seule : le JPG n'est jamais réécrit
            im = im.convert('RGB')
            tmp = dst + '.tmp'
            im.save(tmp, 'WEBP', quality=quality, method=6)
            os.replace(tmp, dst)
        made += 1
    return made, kept


def add_lazy(tag):
    if re.search(r'\b(loading|fetchpriority)=', tag, re.I):
        return tag
    extra = ' loading="lazy"' + ('' if re.search(r'\bdecoding=', tag, re.I) else ' decoding="async"')
    return re.sub(r'\s*/?>$', lambda m: extra + m.group(0), tag, count=1)


def wrap_html(html, site, lazy=False):
    count = 0

    def repl(m):
        nonlocal count
        start = m.start()
        tag = add_lazy(m.group(0)) if lazy else m.group(0)
        # Idempotence : déjà dans <picture> (un <source> juste avant)
        before = html[max(0, start - 200):start]
        if re.search(r'<source\b[^>]*>\s*$', before, re.I) or re.search(r'<picture\b[^>]*>\s*$', before, re.I):
            return tag
        webp_rel = 'img/photos/%s.webp' % m.group(2)
        if not os.path.exists(os.path.join(site, webp_rel)):
            return tag  # pas de webp => on ne crée pas de lien cassé
        count += 1
        return '<picture><source srcset="%s" type="image/webp">%s</picture>' % (webp_rel, tag)

    new = IMG_RE.sub(repl, html)
    return new, count


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('site')
    ap.add_argument('--quality', type=int, default=78)
    ap.add_argument('--lazy', action='store_true', help='ajoute loading="lazy" aux vignettes sans loading')
    a = ap.parse_args()
    site = os.path.abspath(a.site)
    if not os.path.isfile(os.path.join(site, 'index.html')):
        sys.exit('Site introuvable : %s' % site)
    made, kept = make_webps(site, a.quality)
    pages, imgs = 0, 0
    for name in sorted(os.listdir(site)):
        if not name.endswith('.html'):
            continue
        p = os.path.join(site, name)
        with open(p, encoding='utf-8') as f:
            html = f.read()
        new, n = wrap_html(html, site, a.lazy)
        if new != html:
            with open(p, 'w', encoding='utf-8', newline='') as f:
                f.write(new)
            pages += 1
            imgs += n
    print('webp : %d créés, %d à jour ; HTML : %d <img> enveloppées, %d pages modifiées' % (made, kept, imgs, pages))


if __name__ == '__main__':
    main()
