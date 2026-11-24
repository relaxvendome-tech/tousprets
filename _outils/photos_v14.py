# -*- coding: utf-8 -*-
"""photos_v14 : remplace les dessins img/cards/<slug>.svg par des photos CC0 / domaine public
(Wikimedia Commons, licences vérifiées par l'API Commons le 24/11/2026). Idempotent.
Sources : _outils/photos_v14/ (originaux 960 px + sel.json). Usage : cd _outils && python3 photos_v14.py"""
import os, re, json, glob
from PIL import Image

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'photos_v14')
P = os.path.join(ROOT, 'img', 'photos')

ALT = {
 'arnaque-kit-urgence-gratuit': 'Main tenant un smartphone allumé',
 'batterie-externe-station-electrique': 'Batterie externe branchée à un câble de recharge',
 'cyclone-que-faire': 'Palmiers courbés par le vent sous un ciel clair',
 'frigo-congelateur-coupure-electricite': 'Réfrigérateur ouvert rempli d’aliments',
 'groupe-electrogene-securite': 'Groupe électrogène posé dehors, dans l’herbe',
 'kit-7-jours-strategie-europeenne-72h': 'Étagère de provisions dans un placard',
 'kit-de-survie-72h-pas-cher': 'Sac à dos de randonnée prêt à être rempli',
 'kit-de-survie-gouvernement-pdf': 'Main qui coche une liste sur un carnet',
 'kit-urgence-saint-martin-saint-barthelemy': 'Port de Gustavia à Saint-Barthélemy, vu des hauteurs',
 'panne-numerique-cyberattaque-72h': 'Câbles réseau branchés sur des équipements informatiques',
 'purifier-eau-pastilles-filtre': 'Eau qui bout dans une casserole',
 's-equiper-kit-urgence': 'Couteau multifonction ouvert',
 'kit-urgence-la-reunion': 'Vue satellite de l’île de La Réunion',
}

def crop169(im):
    w, h = im.size; th = int(w * 9 / 16)
    if h > th:
        t = (h - th) // 2; im = im.crop((0, t, w, t + th))
    else:
        tw = int(h * 16 / 9); l = (w - tw) // 2; im = im.crop((l, 0, l + tw, h))
    return im

def images(sel):
    os.makedirs(os.path.join(P, '480'), exist_ok=True)
    for x in sel:
        k = x['k']
        im = crop169(Image.open(os.path.join(SRC, '%s__%d.jpg' % (k, x['i']))).convert('RGB')).resize((960, 540), Image.LANCZOS)
        im.save(os.path.join(P, k + '.jpg'), quality=82, optimize=True, progressive=True)
        im.save(os.path.join(P, k + '.webp'), quality=78)
        im.resize((480, 270), Image.LANCZOS).save(os.path.join(P, '480', k + '.webp'), quality=76)

def pic(k, attrs, sizes):
    return ('<picture><source srcset="img/photos/480/%s.webp 480w, img/photos/%s.webp 960w" sizes="%s" type="image/webp">'
            '<img src="img/photos/%s.jpg"%s></picture>' % (k, k, sizes, k, attrs))

def pages(sel):
    ks = [x['k'] for x in sel]; n = 0
    for f in glob.glob(os.path.join(ROOT, '*.html')):
        s = open(f, encoding='utf-8').read(); u = s
        for k in ks:
            alt = ALT[k].replace('"', '&quot;')
            # héros du guide : photo décrite
            u = u.replace('<figure class="hero-img"><img src="img/cards/%s.svg" alt="" width="960" height="540" fetchpriority="high"></figure>' % k,
                          '<figure class="hero-img">' + pic(k, ' alt="%s" width="960" height="540" fetchpriority="high"' % alt, '(min-width: 1000px) 960px, 100vw') + '</figure>')
            # cartes : image décorative (le titre de la carte suffit)
            def rep(m):
                attrs = m.group(1).replace(' alt=""', '')
                return pic(k, ' alt=""' + attrs, '(min-width: 640px) 33vw, 50vw')
            u = re.sub(r'<img src="img/cards/%s\.svg" alt=""([^>]*)>' % re.escape(k), rep, u)
        base = os.path.basename(f)[:-5]
        if base in ks:
            u = re.sub(r'(<meta (?:property|name)="(?:og|twitter):image" content=")https://tousprets\.fr/og-image\.png"', r'\1https://tousprets.fr/img/photos/%s.jpg"' % base, u)
        if u != s: open(f, 'w', encoding='utf-8').write(u); n += 1
    return n

def credits(sel):
    p = os.path.join(P, 'credits.json'); c = json.load(open(p, encoding='utf-8'))
    have = {x['slug'] for x in c}
    for x in sel:
        if x['k'] in have: continue
        c.append({'slug': x['k'], 'titre': x['t'], 'auteur': x.get('by', ''), 'licence': x['lic'], 'source': 'wikimedia commons',
                  'page': 'https://commons.wikimedia.org/wiki/File:' + x['t'].replace(' ', '_')})
    json.dump(c, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

if __name__ == '__main__':
    sel = json.load(open(os.path.join(SRC, 'sel.json'), encoding='utf-8'))
    images(sel); n = pages(sel); credits(sel)
    print('photos_v14 :', len(sel), 'photos ;', n, 'pages modifiées')
