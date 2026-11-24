# -*- coding: utf-8 -*-
"""seo15 (24/11/2026) : mission SEO « référence française ». Idempotent, dernier maillon.
- accueil : title, description, H1 descriptif (slogan conservé en surtitre), un seul H1 dans le source,
  section « Le kit d'urgence 72 h, en bref » (principe, 8 indispensables, mode d'emploi, questions),
  image du héros responsive (640 px sur mobile)
- titres : congélateur (61 → 57 car.), sac de secours (+ « sac d'évacuation »)
Usage : cd _outils && python3 seo15.py"""
import os, re, sys
from PIL import Image

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
def rd(p): return open(os.path.join(ROOT, p), encoding='utf-8').read()
def wr(p, s): open(os.path.join(ROOT, p), 'w', encoding='utf-8').write(s)

HOME_T = "Kit d&#x27;urgence 72h : checklist gratuite | Tous prêts"
HOME_D = "Préparez votre foyer avec une checklist 72h gratuite, interactive et utilisable hors ligne. Guides pratiques et conseils pour toute la famille."

BREF = '''<section class="v15-bref" aria-labelledby="v15BrefT">
        <h2 class="lp-h" id="v15BrefT">Le kit d’urgence 72 h, en bref</h2>
        <div class="v15-grid">
          <div><h3>Qu’est-ce que c’est ?</h3><p>Une réserve préparée à l’avance pour tenir <strong>trois jours</strong> chez vous si l’eau, l’électricité ou les commerces sont coupés, ou pour partir vite si l’on vous demande d’évacuer.</p></div>
          <div><h3>Pourquoi 72 heures ?</h3><p>Le guide officiel « Tous responsables » (SGDSN, novembre 2025) et la stratégie européenne de préparation (mars 2025) recommandent de pouvoir tenir 72 heures en autonomie. Pendant ce temps, les secours s’occupent des situations les plus urgentes.</p></div>
          <div><h3>Pour qui ?</h3><p>Pour tous les foyers, à adapter : <a href="kit-urgence-bebe.html">bébé</a>, <a href="kit-urgence-enfants-ecole.html">enfants</a>, <a href="kit-urgence-personne-agee.html">personnes âgées</a>, <a href="kit-urgence-handicap.html">handicap</a>, <a href="kit-urgence-animaux.html">animaux</a>, <a href="kit-urgence-72h-famille-appartement-voiture.html">appartement ou voiture</a>.</p></div>
        </div>
        <h3 class="v15-h3">Les 8 indispensables</h3>
        <ol class="v15-ess">
          <li><a href="combien-eau-stocker-par-personne.html"><span><strong>Eau</strong> : 6 litres par personne</span></a></li>
          <li><a href="aliments-sans-cuisson-kit-urgence.html"><span><strong>Nourriture</strong> qui se mange sans cuisson</span></a></li>
          <li><a href="que-mettre-dans-un-kit-d-urgence.html"><span><strong>Médicaments</strong> et copies des ordonnances</span></a></li>
          <li><a href="trousse-de-secours-kit-urgence.html"><span><strong>Trousse</strong> de premiers secours</span></a></li>
          <li><a href="radio-a-piles-kit-urgence.html"><span><strong>Radio</strong> à piles ou à manivelle</span></a></li>
          <li><a href="lampe-frontale-lanterne-kit-urgence.html"><span><strong>Lampe</strong> et piles de rechange</span></a></li>
          <li><a href="kit-de-survie-72h.html"><span><strong>Copies</strong> des papiers importants</span></a></li>
          <li><a href="kit-de-survie-72h.html"><span><strong>Argent liquide</strong> en petites coupures</span></a></li>
        </ol>
        <h3 class="v15-h3">Utiliser la checklist en 3 étapes</h3>
        <ol class="v15-steps"><li>Indiquez combien vous êtes : les quantités se calculent.</li><li>Cochez ce que vous avez déjà : « à prévoir », « en partie » ou « disponible ».</li><li>Complétez à votre rythme et vérifiez votre kit deux fois par an.</li></ol>
        <p class="v15-cta"><a class="btn-primary v15-btn" href="#app-start" data-v14go="kit">Ouvrir ma checklist</a> <a class="v15-link" href="checklist-kit-urgence-72h.html">ou l’imprimer</a></p>
        <h3 class="v15-h3">Questions fréquentes</h3>
        <div class="v15-faq">
          <details><summary>Le gouvernement distribue-t-il un kit d’urgence gratuit ?</summary><p>Non. Le guide officiel indique quoi préparer, mais aucun kit n’est envoyé gratuitement. Un message qui vous propose un « kit gratuit » contre des frais de livraison est une arnaque : <a href="arnaque-kit-urgence-gratuit.html">comment la repérer</a>. Ce que dit le guide : <a href="kit-urgence-72h-gouvernement.html">le kit 72 h du gouvernement</a>.</p></details>
          <details><summary>Faut-il acheter un kit tout prêt ?</summary><p>Ce n’est pas nécessaire. La plupart des éléments sont déjà chez vous ; il suffit de les rassembler. Voir <a href="kit-de-survie-72h-pas-cher.html">un kit 72 h pas cher</a>.</p></details>
          <details><summary>Combien d’eau prévoir ?</summary><p>Le guide officiel indique 6 litres par personne pour 72 heures, soit 2 litres par jour pour boire et cuisiner. <a href="combien-eau-stocker-par-personne.html">Le calcul détaillé</a>.</p></details>
          <details><summary>Où ranger le kit, et quand le vérifier ?</summary><p>Dans un endroit facile d’accès, connu de tout le foyer. Le guide officiel conseille de vérifier son contenu deux fois par an (dates, piles, eau).</p></details>
        </div>
        <p class="v15-src">Sources : guide « Tous responsables », SGDSN, 20 novembre 2025 ; stratégie de l’Union pour la préparation, Commission européenne, 26 mars 2025. <a href="sources.html">Notre méthode</a></p>
      </section>
'''

CSS = '''<style id="v15css">
.v15-kicker{margin:0 0 6px!important;font-size:1rem;font-weight:700;letter-spacing:.02em;color:rgba(255,255,255,.92)}
.v15-bref{margin:32px 0 8px}
.v15-grid{display:grid;grid-template-columns:minmax(0,1fr);gap:12px}
@media (min-width:760px){.v15-grid{grid-template-columns:repeat(3,minmax(0,1fr))}}
.v15-grid>div{background:var(--bg-raised);border:1px solid var(--line);border-radius:14px;padding:16px}
.v15-grid h3,.v15-h3{font-size:1.125rem;margin:0 0 6px}
.v15-h3{margin:22px 0 8px}
.v15-grid p{margin:0}
.v15-ess{display:grid;grid-template-columns:minmax(0,1fr);gap:8px;margin:0;padding:0;list-style:none;counter-reset:e}
.v15-ess li,.v15-ess a{min-width:0;overflow-wrap:anywhere}
@media (min-width:640px){.v15-ess{grid-template-columns:repeat(2,minmax(0,1fr))}}
.v15-ess li{counter-increment:e}
.v15-ess a{display:flex;gap:10px;align-items:center;min-height:48px;padding:10px 14px;background:var(--bg-raised);border:1px solid var(--line);border-radius:12px;color:var(--text);text-decoration:none}
.v15-ess a::before{content:counter(e);flex:none;width:28px;height:28px;border-radius:50%;background:var(--teal);color:#fff;display:grid;place-items:center;font-weight:800;font-size:14px}
:root[data-theme="dark"] .v15-ess a::before{color:var(--bg)}
.v15-ess a:hover{border-color:var(--teal)}
.v15-steps{margin:0;padding-left:1.3em;display:grid;gap:6px}
.v15-cta{display:flex;flex-wrap:wrap;gap:10px 16px;align-items:center;margin:16px 0 0}
.v15-btn{display:inline-flex;align-items:center;width:auto;min-height:48px;padding:12px 20px;text-decoration:none}
.v15-link{color:var(--teal);font-weight:650;text-decoration:underline}
.v15-faq details{border-top:1px solid var(--line);padding:4px 0}
.v15-faq summary{cursor:pointer;font-weight:650;min-height:48px;display:flex;align-items:center}
.v15-faq p{margin:0 0 12px}
.v15-faq a,.v15-bref p a:not(.btn-primary){color:var(--teal)}
.v15-src{font-size:.9375rem;color:var(--text-dim);margin-top:14px}
</style>'''

def must(s, old, new, label):
    if old not in s: sys.exit('seo15 : motif introuvable (%s)' % label)
    return s.replace(old, new, 1)

def home():
    s = rd('index.html')
    s = re.sub(r'<title>[^<]*</title>', '<title>%s</title>' % HOME_T, s, count=1)
    s = re.sub(r'(<meta name="description" content=")[^"]*"', r'\g<1>%s"' % HOME_D, s, count=1)
    for k in ('property="og:title"', 'name="twitter:title"'):
        s = re.sub(r'(<meta %s content=")[^"]*"' % re.escape(k), r'\g<1>%s"' % HOME_T, s, count=1)
    for k in ('property="og:description"', 'name="twitter:description"'):
        s = re.sub(r'(<meta %s content=")[^"]*"' % re.escape(k), r'\g<1>%s"' % HOME_D, s, count=1)
    if 'v15-kicker' not in s:
        s = must(s, '<h1 id="lpT">Être prêt change tout.</h1>',
                 '<p class="v15-kicker">Être prêt change tout.</p>\n          <h1 id="lpT">Kit d’urgence 72 h : préparez votre famille sereinement</h1>', 'h1')
    s = s.replace("p.innerHTML = '<h1>Bilan d\\'exercice — Tous prêts</h1>'", "p.innerHTML = '<h2>Bilan d\\'exercice — Tous prêts</h2>'")
    s = re.sub(r'<section class="v15-bref".*?</section>\n\s*', '', s, flags=re.S)
    s = must(s, '<div class="lp-sec lp-kit" aria-labelledby="lpS3">', BREF + '\n      <div class="lp-sec lp-kit" aria-labelledby="lpS3">', 'bref')
    s = s.replace('<source srcset="img/photos/vague-de-froid-que-faire.webp" type="image/webp"><img class="lp-hero-bg"',
                  '<source srcset="img/photos/640/vague-de-froid-que-faire.webp 640w, img/photos/vague-de-froid-que-faire.webp 960w" sizes="100vw" type="image/webp"><img class="lp-hero-bg"')
    s = re.sub(r'<style id="v15css">.*?</style>\n?', '', s, flags=re.S)
    s = must(s, '</head>', CSS + '\n</head>', 'head')
    wr('index.html', s)
    d = os.path.join(ROOT, 'img', 'photos', '640'); os.makedirs(d, exist_ok=True)
    im = Image.open(os.path.join(ROOT, 'img', 'photos', 'vague-de-froid-que-faire.jpg')).convert('RGB')
    im.resize((640, 360), Image.LANCZOS).save(os.path.join(d, 'vague-de-froid-que-faire.webp'), quality=72)

def titles():
    T = {'frigo-congelateur-coupure-electricite.html': 'Congélateur sans courant : combien de temps ? (frigo 4 h)',
         'sac-de-secours.html': 'Sac de secours (sac d’évacuation) : que mettre dedans ?'}
    for p, t in T.items():
        s = rd(p)
        s = re.sub(r'<title>[^<]*</title>', '<title>%s</title>' % t, s, count=1)
        for k in ('property="og:title"', 'name="twitter:title"'):
            s = re.sub(r'(<meta %s content=")[^"]*"' % re.escape(k), r'\g<1>%s"' % t, s, count=1)
        wr(p, s)

def pdf():
    """checklist-kit-urgence-72h.pdf : PDF A4 de la page à imprimer (Chrome sans interface)."""
    try:
        import asyncio
        from playwright.async_api import async_playwright
    except ImportError:
        print('  (playwright absent : PDF non régénéré)'); return
    async def run():
        async with async_playwright() as p:
            b = await p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
            pg = await (await b.new_context(service_workers='block')).new_page()
            await pg.goto('file://' + os.path.join(ROOT, 'checklist-kit-urgence-72h.html')); await pg.wait_for_timeout(800)
            await pg.emulate_media(media='print')
            await pg.pdf(path=os.path.join(ROOT, 'checklist-kit-urgence-72h.pdf'), format='A4', print_background=True,
                         margin={'top': '12mm', 'bottom': '12mm', 'left': '12mm', 'right': '12mm'})
            await b.close()
    asyncio.run(run())

def pdf_links():
    p = 'checklist-kit-urgence-72h.html'; s = rd(p)
    if 'checklist-kit-urgence-72h.pdf' not in s:
        s = s.replace('<a class="btn btn-2" href="kit-urgence-72h-gouvernement.html">Comprendre le guide de l\'État</a>',
                      '<a class="btn btn-2" href="checklist-kit-urgence-72h.pdf" download>Télécharger la checklist en PDF</a><a class="btn btn-2" href="kit-urgence-72h-gouvernement.html">Comprendre le guide de l\'État</a>', 1)
        if 'checklist-kit-urgence-72h.pdf' not in s: sys.exit('seo15 : bouton PDF non placé')
        wr(p, s)
    s = rd('index.html')
    s = s.replace('<a class="v15-link" href="checklist-kit-urgence-72h.html">ou l’imprimer</a>',
                  '<a class="v15-link" href="checklist-kit-urgence-72h.html">l’imprimer</a> · <a class="v15-link" href="checklist-kit-urgence-72h.pdf" download>la télécharger en PDF</a>')
    wr('index.html', s)

if __name__ == '__main__':
    home(); titles(); pdf_links(); pdf(); print('seo15 : accueil, titres, checklist PDF à jour')
