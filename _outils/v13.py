#!/usr/bin/env python3
"""v13 (2026-11-23) : dernier maillon de redesign.py, idempotent.

1. Accueil (index.html) : pas d'animation d'apparition sur l'écran affiché au chargement.
   L'animation fadeIn (opacity 0 -> 1) de .screen.active retardait le LCP (image du héros)
   après l'événement load. Elle reste active dès le premier clic (classe html.tp-nav).
2. GoatCounter : aucune mesure dans l'application Android (hôte appassets.androidplatform.net),
   comme l'annonce la politique de confidentialité.
3. charte-editoriale.html : section « Journal des corrections » (données : JOURNAL ci-dessous,
   tirées de `git log --format='%cs %s'` ; n'ajouter que des corrections réellement publiées).

4. Accueil : vignettes 480 px (img/photos/480/) en srcset pour les cartes, au lieu des photos 960 px.

5. style.css : éléments « noprint » (dont .hero-cta) masqués à l'impression.

Usage : python3 v13.py /chemin/du/site
"""
import os, re, sys

site = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')

# ---------- 1. accueil : premier affichage sans animation ----------
NAV_CSS = '<style id="v13-css">html:not(.tp-nav) .screen.active{animation:none}</style>'
NAV_JS = ('<script id="v13-js">document.addEventListener("click",function(){'
          'document.documentElement.classList.add("tp-nav")},{once:true,capture:true});</script>')

def accueil():
    p = os.path.join(site, 'index.html')
    s = open(p, encoding='utf-8').read()
    t = re.sub(r'<style id="v13-css">.*?</style>', '', s, flags=re.S)
    t = re.sub(r'<script id="v13-js">.*?</script>', '', t, flags=re.S)
    i = t.find('</head>')
    t = t[:i] + NAV_CSS + NAV_JS + t[i:]
    if t != s:
        open(p, 'w', encoding='utf-8').write(t)
        return 1
    return 0

# ---------- 2. GoatCounter : pas de mesure dans l'appli Android ----------
GC_TAG = '<script data-goatcounter="https://tousprets.goatcounter.com/count" async src="count.js"></script>'
GC_GUARD = ('<script id="v13-gc">if(/appassets\\.androidplatform\\.net/.test(location.host))'
            'window.goatcounter={no_onload:true};</script>')

def goatcounter():
    n = 0
    for f in sorted(os.listdir(site)):
        if not f.endswith('.html'):
            continue
        p = os.path.join(site, f)
        s = open(p, encoding='utf-8').read()
        if GC_TAG not in s:
            continue
        t = re.sub(r'<script id="v13-gc">.*?</script>', '', s, flags=re.S)
        t = t.replace(GC_TAG, GC_GUARD + GC_TAG, 1)
        if t != s:
            open(p, 'w', encoding='utf-8').write(t); n += 1
    return n

# ---------- 3. charte : journal des corrections ----------
# (date ISO, texte HTML). Source : historique git du site. Ordre : du plus récent au plus ancien.
JOURNAL = [
    ('2026-11-23', 'Droits d’auteur : retrait des mentions « libre de droits », CC BY et CC0 sur les pages, '
                   'les données structurées et les métadonnées des photos. Les visuels sont publiés sous droits réservés '
                   '(voir <a href="licence-visuels.html">Droits d’auteur et réutilisation</a>).'),
    ('2026-11-23', 'Titre « Entraide entre voisins » rétabli : il avait été altéré.'),
    ('2026-11-23', '183 corrections de contenu sur 53 pages, après une relecture croisée par plusieurs outils '
                   'd’intelligence artificielle et une vérification de chaque correction.'),
    ('2026-11-23', '25 consignes précisées, notamment : le 114 est réservé aux personnes sourdes et malentendantes ; '
                   'tsunami ; symptômes d’une intoxication au monoxyde de carbone ; calfeutrage ; double authentification.'),
    ('2026-11-23', 'Mentions légales : hébergeur corrigé (GitHub Pages).'),
    ('2026-11-23', 'Précautions précisées pour les biberons et le lait infantile, le lavage des mains, '
                   'les talkies-walkies et les bouteilles d’eau congelées.'),
    ('2026-11-23', 'Corrections de sécurité : réfrigérateur à 4 °C au plus (et non 7 °C), pas de recongélation, '
                   'conserves bombées ; eau adaptée aux nourrissons et biberon préparé juste avant ; chauffe-eau à laisser '
                   'refroidir avant de le vider, son eau à boire en dernier recours ; toilettes sèches ; numéros 112 et 15, 17, 18 ; '
                   'talkies-walkies ; appel d’urgence par satellite nuancé.'),
]
MOIS = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre']

def date_fr(iso):
    a, m, j = iso.split('-')
    return f'{int(j)}{"er" if j == "01" else ""} {MOIS[int(m) - 1]} {a}'

def journal_html():
    li = ''.join(f'<li><time datetime="{d}">{date_fr(d)}</time> : {t}</li>' for d, t in JOURNAL)
    return ('<section id="journal-corrections" aria-labelledby="journal-t"><h2 id="journal-t">Journal des corrections</h2>'
            '<p>Les corrections de fond apportées aux contenus, d’après l’historique des modifications du site. '
            'Les changements de présentation n’y figurent pas. Vous avez repéré une erreur ? '
            'Utilisez le lien « Signaler une erreur » présent sur chaque page.</p>'
            f'<ul class="journal">{li}</ul></section>\n').replace(' : ', '\u00a0: ').replace(' ;', '\u00a0;').replace('« ', '«\u00a0').replace(' »', '\u00a0»').replace(' ?', '\u00a0?')

def charte():
    p = os.path.join(site, 'charte-editoriale.html')
    if not os.path.exists(p):
        return 0
    s = open(p, encoding='utf-8').read()
    t = re.sub(r'<section id="journal-corrections".*?</section>\n', '', s, flags=re.S)
    # avant le bloc sources (p.disclaimer) placé juste avant la FAQ par lisibilite_v9, pour ne pas le déplacer
    i = t.find('<section id="faq"')
    d = t.rfind('<p class="disclaimer"', 0, i) if i >= 0 else -1
    if d >= 0 and t[d:i].count('</p>') == 1 and t[t.find('</p>', d) + 4:i].strip() == '':
        i = d
    if i < 0:
        i = t.find('</main>')
    t = t[:i] + journal_html() + t[i:]
    if t != s:
        open(p, 'w', encoding='utf-8').write(t)
        return 1
    return 0

# ---------- 4. accueil : vignettes 480 px pour les cartes (au lieu des photos 960 px) ----------
TAILLES = {'card': '(min-width: 1100px) 270px, (min-width: 640px) 33vw, 50vw',
           'row': '(min-width: 640px) 25vw, 64px',
           'link': '(min-width: 640px) 50vw, 96px'}

def vignettes():
    from PIL import Image
    p = os.path.join(site, 'index.html')
    s = open(p, encoding='utf-8').read()
    def rep(m):
        kind, nom = m.group(2), m.group(4)
        src = os.path.join(site, 'img/photos', nom + '.webp')
        dst = os.path.join(site, 'img/photos/480', nom + '.webp')
        if not os.path.exists(src):
            return m.group(0)
        if not os.path.exists(dst):  # créée une seule fois : sortie stable d'un passage à l'autre
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            im = Image.open(src)
            im.resize((480, round(480 * im.height / im.width)), Image.LANCZOS).save(dst, 'WEBP', quality=72, method=6)
        return (f'{m.group(1)}<source srcset="img/photos/480/{nom}.webp 480w, img/photos/{nom}.webp 960w" '
                f'sizes="{TAILLES[kind]}" type="image/webp">')
    t = re.sub(r'(<a class="lp-(card|row|link)([^"]*)" href="[^"]*"><picture>)<source srcset="img/photos/([a-z0-9-]+)\.webp" type="image/webp">',
               rep, s)
    if t != s:
        open(p, 'w', encoding='utf-8').write(t)
        return 1
    return 0

# ---------- 5. style.css : ce qui est marqué « noprint » reste masqué à l'impression ----------
# (le bloc v9 redonne display:flex à .hero-cta, ce qui l'emportait sur la règle d'impression)
PRINT_CSS = ('/* ===== v13 : impression (v13.py) ===== */\n'
             '@media print{.noprint,.hero-cta,.hero-note{display:none!important}}\n')

def impression():
    p = os.path.join(site, 'style.css')
    s = open(p, encoding='utf-8').read()
    t = re.sub(r'/\* ===== v13 : impression \(v13\.py\) ===== \*/\n.*?\n', '', s, flags=re.S)
    t = t.rstrip('\n') + '\n' + PRINT_CSS
    if t != s:
        open(p, 'w', encoding='utf-8').write(t)
        return 1
    return 0

if __name__ == '__main__':
    print('v13 : accueil', accueil(), '| goatcounter', goatcounter(), 'page(s) | charte', charte(), '| vignettes', vignettes(), '| impression', impression())
