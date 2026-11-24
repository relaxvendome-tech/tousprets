# -*- coding: utf-8 -*-
"""v14 : refonte ergonomique (dernier maillon de redesign.py, idempotent).
Accueil (héros, engagements, 3 portes), navigation 4 entrées, écran « Ma préparation »,
checklist 3 états, besoins du foyer, guides « L'essentiel » en 3 parties.
Usage : cd _outils && python3 v14.py
"""
import os, re, json, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
OUT = os.path.dirname(os.path.abspath(__file__))
CSS = open(os.path.join(OUT, 'v14.css'), encoding='utf-8').read().strip()
JS = open(os.path.join(OUT, 'v14.js'), encoding='utf-8').read().strip()

def rd(p): return open(os.path.join(ROOT, p), encoding='utf-8').read()
def wr(p, s): open(os.path.join(ROOT, p), 'w', encoding='utf-8').write(s)

def must(s, old, new, label, count=1):
    if s.count(old) != count:
        sys.exit('v14 : motif introuvable ou ambigu (%s) : %d' % (label, s.count(old)))
    return s.replace(old, new)

ICON = {
 'home': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 11 12 4l9 7"/><path d="M5 10v10h14V10"/><path d="M10 20v-6h4v6"/></svg>',
 'prep': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="4" y="3" width="16" height="18" rx="2"/><path d="m8 9 2 2 4-4"/><path d="M8 15h8"/></svg>',
 'reflex': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="m15.5 8.5-2 5-5 2 2-5z"/></svg>',
 'guides': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 5a2 2 0 0 1 2-2h13v16H6a2 2 0 0 0-2 2z"/><path d="M4 19V5"/><path d="M9 7h6"/></svg>',
 'shield': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3 5 6v5c0 4.5 3 8.5 7 10 4-1.5 7-5.5 7-10V6z"/><path d="M12 8v4l2 2"/></svg>',
}

NAV = ('<nav class="bottom" aria-label="Navigation principale">'
  '<button type="button" data-screen="home" class="active" aria-current="page">' + ICON['home'] + '<span>Accueil</span></button>'
  '<button type="button" data-screen="prep">' + ICON['prep'] + '<span>Ma préparation</span></button>'
  '<button type="button" data-screen="guides">' + ICON['reflex'] + '<span>Bons réflexes</span></button>'
  '<a href="tous-les-guides.html">' + ICON['guides'] + '<span>Guides</span></a>'
  '</nav>')

HERO_NEW = '''<p class="lp-value">Préparez votre foyer, apprenez les bons réflexes et avancez à votre rythme.</p>
          <p class="lp-sub">Votre kit d’urgence 72 h, calculé pour votre foyer, d’après le guide officiel « Tous responsables ».</p>
          <p class="lp-cta v14-cta"><a class="lp-btn lp-btn1" href="#app-start" data-v14go="prep">Préparer mon foyer</a><a class="lp-btn lp-btn2" href="reagir-en-cas-de-crise.html" data-v14go="guides">Découvrir les bons réflexes</a></p>
          <ul class="v14-engage" role="list" aria-label="Nos engagements"><li>Gratuit</li><li>Sans inscription</li><li>Sans publicité</li><li>Fonctionne hors ligne</li><li>Données conservées sur l’appareil</li></ul>
          <ul class="lp-alt" role="list"><li>Faire le point en quelques questions : <a href="diagnostic-suis-je-pret.html">Suis-je prêt ?</a></li></ul>'''

DOORS = '''<ul class="v14-doors" role="list" aria-label="Trois façons de commencer">
        <li><a class="v14-door" href="#app-start" data-v14go="prep">''' + ICON['prep'] + '''<span class="k">Préparer</span><strong>Constituer son kit d’urgence et organiser son foyer.</strong><span class="go">Ma préparation →</span></a></li>
        <li><a class="v14-door" href="reagir-en-cas-de-crise.html" data-v14go="guides">''' + ICON['reflex'] + '''<span class="k">Agir</span><strong>Comprendre les bons réflexes selon les situations.</strong><span class="go">Les bons réflexes →</span></a></li>
        <li><a class="v14-door" href="comprendre-s-informer.html">''' + ICON['shield'] + '''<span class="k">Anticiper</span><strong>Comprendre les risques et protéger ses proches.</strong><span class="go">Les risques →</span></a></li>
      </ul>'''

HUB = '''<ul class="v14-hub" role="list" aria-label="Ma préparation">
      <li class="wide"><button type="button" data-v14go="kit"><b>Ma checklist kit 72 h</b><span>Les 8 indispensables d’abord, puis le reste à votre rythme.</span></button></li>
      <li><button type="button" data-v14go="profils"><b>Mon foyer</b><span>Personnes et besoins particuliers</span></button></li>
      <li><button type="button" data-v14go="stock"><b>Stock et quantités</b><span>Eau, nourriture, équipement</span></button></li>
      <li><button type="button" data-v14go="contacts"><b>Contacts</b><span>Les numéros à garder</span></button></li>
      <li><button type="button" data-v14go="voisinage"><b>Voisins</b><span>Un groupe d’entraide sans compte</span></button></li>
      <li><button type="button" data-v14go="scenarios"><b>Par situation</b><span>Tempête, coupure, canicule…</span></button></li>
      <li><button type="button" data-v14go="exercise"><b>Mode exercice</b><span>S’entraîner, chronomètre en main</span></button></li>
    </ul>'''

HEADP = '<div class="section-title"><h2 id="app-start">Ma préparation</h2></div>\n      <p class="v14-hint">Où vous en êtes et la prochaine action utile. Tout reste sur votre appareil.</p>'

def back(): return '<button type="button" class="v14-back" data-goto="prep"><span aria-hidden="true">←</span> Ma préparation</button>'

def index():
    s = rd('index.html')
    if 'id="screen-prep"' in s:
        # déjà transformé : on ne met à jour que le CSS et le JS injectés
        pass
    else:
        # 1. héros
        s = re.sub(r'<p class="lp-value">.*?</ul>\s*(?=</div>\s*</div>\s*<ul class="lp-benefits")', HERO_NEW + '\n        ', s, count=1, flags=re.S)
        if 'v14-engage' not in s: sys.exit('v14 : héros non remplacé')
        # 2. trois portes à la place des bénéfices
        s, n = re.subn(r'<ul class="lp-benefits".*?</ul>', DOORS, s, count=1, flags=re.S)
        if n != 1: sys.exit('v14 : bénéfices introuvables')
        s = s.replace('<a class="lp-btn lp-btn1" href="#app-start">', '<a class="lp-btn lp-btn1" href="#app-start" data-v14go="prep">')
        # 3. navigation : 4 entrées, dans l'en-tête (barre du bas sur mobile)
        s, n = re.subn(r'\n<nav class="bottom" aria-label="Navigation principale">.*?</nav>\n', '\n', s, count=1, flags=re.S)
        if n != 1: sys.exit('v14 : nav introuvable')
        s = must(s, '<button class="emergency-btn" id="openEmergency"><span aria-hidden="true">🆘</span> Urgence</button>\n  </div>\n</header>',
                 '<button class="emergency-btn" id="openEmergency"><span aria-hidden="true">🆘</span> Urgence</button>\n  </div>\n  ' + NAV + '\n</header>', 'header')
        # 4. écran « Ma préparation »
        a = s.find('      <h2 class="lp-h lp-app-h" id="app-start">')
        b = s.find('    </section>\n    <div class="install-banner" id="installBanner">')
        c = s.find('    <div class="welcome-card" id="welcomeCard" hidden>')
        d = s.find('  </section>\n\n  <!-- SCÉNARIOS -->')
        if min(a, b, c, d) < 0 or not (a < b < c < d): sys.exit('v14 : découpage accueil impossible')
        head = s[a:b]
        head = re.sub(r'<h2 class="lp-h lp-app-h" id="app-start">[^<]*</h2>\s*<p class="lp-sub2">.*?</p>', HEADP, head, flags=re.S)
        app = s[c:d]
        # tableau de bord : score + prochaine action + indispensables
        i = app.find('    <div class="score-card">'); j = app.find('    <section class="parcours"')
        score = app[i:j]
        app = app[:i] + '    <div class="v14-dash" aria-labelledby="v14DashT"><h3 id="v14DashT" class="v14-sr">Mon tableau de bord</h3>\n' + score + '    <div id="v14Dash"></div><p id="v14Live" class="v14-sr" aria-live="polite"></p></div>\n    ' + HUB + '\n' + app[j:]
        # axes du guide officiel et chips de scénarios : repliés
        mi = re.search(r'    <div class="section-title"><h2>Source\W{1,3}guide[^<]*</h2></div>', app)
        j = app.find('    <!-- ===== MODULE EXERCICE')
        if not mi or j < 0: sys.exit('v14 : axes introuvables')
        i = mi.start()
        axes = app[mi.end():j].replace('<div class="section-title"><h2>Scénarios</h2></div>', '<p class="v14-hint">Checklists par situation :</p>')
        axes = re.sub(r'\s*<div class="note">Ouvrez l\'onglet <strong>Scénarios</strong>.*?</div>', '', axes, flags=re.S)
        app = app[:i] + '    <details class="v14-axes"><summary>Le guide officiel « Tous responsables » en 3 axes</summary>\n' + axes + '    </details>\n' + app[j:]
        s = s[:a] + s[b:c] + s[d:]
        s = s.replace('  </section>\n\n  <!-- SCÉNARIOS -->', '  </section>\n  <!-- MA PRÉPARATION (v14) -->\n  <section class="screen" id="screen-prep">\n' + head + app + '  </section>\n\n  <!-- SCÉNARIOS -->', 1)
        # 5. retours et titres des sous-écrans
        for sid in ('scenarios', 'stock', 'profils', 'contacts', 'voisinage'):
            s = must(s, '<section class="screen" id="screen-%s">' % sid, '<section class="screen" id="screen-%s">\n    %s' % (sid, back()), sid)
        s = must(s, '<div class="section-title"><h2>Scénarios</h2></div>\n    <div class="chip-row" id="scenarioChips">', '<div class="section-title"><h2>Ma checklist</h2></div>\n    <div class="chip-row" id="scenarioChips">', 'titre scénarios')
        s = must(s, '<div class="section-title"><h2>Guides rapides</h2></div>',
          '<div class="section-title"><h2>Bons réflexes</h2></div>\n    <div class="v14-reflex"><a href="reagir-en-cas-de-crise.html"><b>Réagir en cas de crise →</b><span>Avant, pendant, après : les réflexes officiels, situation par situation.</span></a><a href="signal-alerte-sirene.html"><b>Reconnaître l’alerte →</b><span>Sirène, FR-Alert : que faire quand l’alerte retentit.</span></a></div>\n    <p class="v14-hint">Ou cherchez une réponse rapide, même sans réseau :</p>', 'titre guides')
        # 6. foyer : besoins particuliers
        s = must(s, '<p class="note">Les quantités d\'eau (6 L par personne)',
          '<fieldset class="card v14-needs"><legend class="hh-q">Besoins particuliers</legend><p class="hh-sum">Cochez ce qui concerne votre foyer. La checklist s’adapte. Rien n’est envoyé.</p><div class="v14-nbox" id="v14Needs"></div><div id="v14NeedTips"></div></fieldset>\n    <p class="note">Les quantités d\'eau (6 L par personne)', 'foyer')
        # 7. progression v9 : ignorée quand la checklist v14 (kit 72 h) est affichée
        s = must(s, 'function prog(){if(!box||!sc)return;', 'function prog(){if(!box||!sc)return;if(sc.dataset.v14){box.hidden=true;return}', 'v9 prog')
        s = must(s, "<div id=\"v9ScenProg\" class=\"v9-prog\" hidden></div>", "<div id=\"v9ScenProg\" class=\"v9-prog\" hidden></div>", 'v9 box')
    # 8. CSS et JS (remplacés à chaque passage)
    s = re.sub(r'<style id="v14css">.*?</style>\n?', '', s, flags=re.S)
    s = re.sub(r'<script id="v14js">.*?</script>\n?', '', s, flags=re.S)
    s = must(s, '</head>', '<style id="v14css">' + CSS + '</style>\n</head>', 'head')
    s = must(s, '</body>', '<script id="v14js">' + JS + '</script>\n</body>', 'body')
    wr('index.html', s)

def guides():
    data = json.load(open(os.path.join(OUT, 'essentiels.json'), encoding='utf-8'))
    n = 0
    for slug, d in data.items():
        p = slug + '.html'
        s = rd(p)
        if '<!-- ess:v14 -->' in s: continue
        m = re.search(r'<!-- ess:v4 --><section class="essentiel" aria-labelledby="ess-t">.*?</section>', s, re.S)
        if not m: print('  (pas de bloc essentiel)', slug); continue
        lead = re.search(r'<p class="lead">(.*?)</p>', s, re.S)
        aside = re.search(r'\s*<aside class="box box--interdit">.*?</aside>', s, re.S)
        dis = re.search(r'<p class="disclaimer"><strong>Informations pratiques, sources officielles</strong> \((.*?)\)\. ', s, re.S)
        ver = re.search(r'Vérifié le ([^<]+)', s)
        ol = re.search(r'<ol>.*?</ol>', m.group(0), re.S).group(0)
        no = ''.join('<li>%s</li>' % x for x in d.get('interdit', []))
        blk = ('<!-- ess:v14 --><section class="essentiel" aria-labelledby="ess-t"><h2 id="ess-t">L\'essentiel</h2>'
               + ('<p class="v14-know"><strong>Ce qu’il faut savoir :</strong> %s</p>' % lead.group(1).strip() if lead else '')
               + '<div class="v14-ess-g"><div class="v14-do"><h3>Ce qu’il faut faire</h3>' + ol + '</div>'
               + ('<div class="v14-no"><h3>Ce qu’il ne faut pas faire</h3><ul>' + no + '</ul></div>' if no else '')
               + '</div><p class="v14-src"><strong>Sources officielles :</strong> ' + (dis.group(1) if dis else 'voir la page Sources') + '.'
               + (' Vérifié le %s.' % ver.group(1).strip() if ver else '') + ' <a href="sources.html">Notre méthode</a></p></section>')
        s = s[:m.start()] + blk + s[m.end():]
        if aside and no: s = s.replace(aside.group(0), '', 1)
        wr(p, s); n += 1
    return n

def ctas():
    import glob
    n = 0
    for f in glob.glob(os.path.join(ROOT, '*.html')):
        t = open(f, encoding='utf-8').read()
        u = t.replace('<a class="btn" href="./">Cocher ma liste', '<a class="btn" href="./#screen-scenarios">Cocher ma liste')
        if u != t: open(f, 'w', encoding='utf-8').write(u); n += 1
    return n


def editorial_nav():
    """Harmonise le menu des pages éditoriales avec l'appli (v14b)."""
    import glob
    n = 0
    for f in glob.glob(os.path.join(ROOT, '*.html')):
        t = open(f, encoding='utf-8').read(); u = t
        u = u.replace('<a class="head-cta nav-kit" href="./#app-start">Kit 72 h</a>', '<a class="head-cta nav-kit" href="./#screen-prep">Ma préparation</a>')
        if 'href="./#screen-prep">Ma préparation</a></li>' not in u:
            u = re.sub(r'(<li class="mn-i"><a class="mn-a" href="\./"[^>]*>Accueil</a></li>)', r'\1<li class="mn-i"><a class="mn-a" href="./#screen-prep">Ma préparation</a></li>', u, count=1)
        u = re.sub(r'(<a class="mn-a" href="reagir-en-cas-de-crise\.html"[^>]*>)Réagir en cas de crise</a>', r'\1Bons réflexes</a>', u, count=1)
        m1 = re.search(r'<li class="mn-i"><a class="mn-a" href="comprendre-s-informer\.html"[^>]*>[^<]*</a></li>', u)
        m2 = re.search(r'<li class="mn-i"><a class="mn-a" href="reagir-en-cas-de-crise\.html"[^>]*>[^<]*</a></li>', u)
        if m1 and m2 and m1.start() < m2.start():
            a, b = m1.group(0), m2.group(0)
            u = u[:m1.start()] + b + u[m1.end():m2.start()] + a + u[m2.end():]
        u = u.replace('<a class="mn-sa" href="checklist-kit-urgence-72h.html">Ma checklist</a>', '<a class="mn-sa" href="checklist-kit-urgence-72h.html">Checklist à imprimer</a>')
        if u != t: open(f, 'w', encoding='utf-8').write(u); n += 1
    return n

def faq_power():
    p = 'questions-reponses-kit-urgence.html'; s = rd(p)
    if 'v14-power' in s or 'station électrique portable ?' not in s: return 0
    old = "s'il y a assez de soleil."
    new = ("s'il y a assez de soleil. Le temps de recharge dépend de la puissance du panneau, de l'ensoleillement et du modèle de station.")
    s = s.replace(old, new)
    old2 = 'Elle ne brûle aucun carburant'
    new2 = ("Elle n'alimente pas n'importe quel appareil : la puissance de l'appareil doit rester sous la puissance de sortie de la station, et sa capacité en Wh fixe la durée d'utilisation. Elle ne brûle aucun carburant")
    s = s.replace(old2, new2)
    s = s.replace('<details><summary>Quelle différence entre une batterie externe', '<details class="v14-power"><summary>Quelle différence entre une batterie externe', 1)
    wr(p, s); return 1

def home_density():
    s = rd('index.html')
    if '<details class="v14-feat">' in s: return 0
    s, n = re.subn(r'(<ul class="lp-feat" role="list">.*?</ul>)', r'<details class="v14-feat"><summary>Ce que contient la checklist</summary>\1</details>', s, count=1, flags=re.S)
    wr('index.html', s); return n

def styles():
    s = rd('style.css')
    s = re.sub(r'/\* ===== v14 \(source.*?/\* /v14 \*/\n?', '', s, flags=re.S)
    wr('style.css', s.rstrip() + '\n' + CSS + '\n')

def sw():
    s = rd('sw.js')
    m = re.search(r"CACHE_VERSION = 'tous-prets-v(\d+)'", s)
    if m and '/* v14b */' not in s:
        s = s.replace(m.group(0), "CACHE_VERSION = 'tous-prets-v%d'" % (int(m.group(1)) + 1)) + '\n/* v14b */\n'
        wr('sw.js', s)

if __name__ == '__main__':
    index(); g = guides(); c = ctas(); e = editorial_nav(); fq = faq_power(); hd = home_density(); styles(); sw()
    print('v14 : accueil, navigation, Ma préparation, checklist, foyer ; guides :', g, '; boutons appli :', c, '; menus :', e, '; FAQ :', fq, '; accueil :', hd)
