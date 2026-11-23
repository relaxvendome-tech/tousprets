"""Droits d'auteur v11 : plus aucune mention « libre de droits » / CC BY / CC0 sur le site ; page licence-visuels réécrite
(tous droits réservés). Idempotent. Usage : python3 droits_v11.py <site>"""
import re, sys, os, glob, json
site = sys.argv[1] if len(sys.argv) > 1 else '.'
MAIN = """<main id="contenu"><div class="wrap">
<nav class="crumbs" aria-label="Fil d'Ariane"><a href="./">Tous prêts</a> › Droits d'auteur</nav>
<h1>Droits d'auteur et réutilisation des contenus</h1>
<p class="lead">Les guides, les infographies, le logo, le design et l'application Tous prêts sont des créations originales protégées par le droit d'auteur. <strong>Tous droits réservés.</strong></p>
<h2>Ce que vous pouvez faire</h2>
<ul>
<li><strong>Partager le lien</strong> d'une page ou de l'application, par message, sur les réseaux sociaux ou dans un bulletin : c'est même encouragé.</li>
<li><strong>Citer un court extrait</strong> en indiquant clairement la source « Tous prêts — tousprets.fr » et le lien vers la page, dans les limites du droit de courte citation (article L122-5 du Code de la propriété intellectuelle).</li>
<li><strong>Imprimer pour votre usage personnel</strong> la checklist et les pages qui vous sont utiles.</li>
</ul>
<h2>Ce qui nécessite une autorisation écrite</h2>
<ul>
<li>Reproduire, en tout ou en partie, les textes, les infographies, le logo ou la présentation du site, sur un autre site, une application, une publication ou un support imprimé.</li>
<li>Toute utilisation commerciale ou toute réutilisation dans un produit, une formation ou un kit vendu.</li>
<li>Copier la structure, le design ou le code de l'application.</li>
</ul>
<p>Toute reproduction non autorisée constitue une contrefaçon (article L122-4 du Code de la propriété intellectuelle).</p>
<h2>Demander une autorisation</h2>
<p>Mairies, écoles, associations, médias : vous souhaitez utiliser un contenu de Tous prêts ? Écrivez-nous en précisant le contenu, l'usage et le support prévus : <a href="mailto:relaxvendome@gmail.com?subject=Demande%20d%27autorisation%20%E2%80%93%20Tous%20pr%C3%AAts">relaxvendome@gmail.com</a>. Nous répondons volontiers aux projets d'intérêt général.</p>
<h2>Photographies et composants tiers</h2>
<p>Certaines photographies proviennent de banques d'images dont la licence autorise cet usage ; elles ne sont pas la propriété de Tous prêts. Les bibliothèques logicielles tierces et leurs licences sont indiquées dans les <a href="mentions-legales.html">mentions légales</a>. Les informations publiques citées le sont dans les conditions précisées sur la page <a href="sources.html">Sources</a>.</p>
</div></main>"""
REPL = [
    ('>Licence des visuels<', ">Droits d'auteur<"),
    ('Infographie : Tous prêts — tousprets.fr, licence CC BY 4.0', 'Infographie : © Tous prêts — tousprets.fr'),
    (' Les photos sont libres de droits (domaine public) et créditées sur la page <a href="licence-visuels.html">Licence des visuels</a>.',
     ' Les photos sont utilisées dans le respect de leurs licences ; voir la page <a href="licence-visuels.html">Droits d\'auteur</a>.'),
    ("<strong>Réutiliser nos visuels</strong><span>Les infographies Tous prêts sont sous licence CC BY 4.0 : réutilisation libre, y compris imprimée, en citant tousprets.fr. Formulation à copier.</span>",
     "<strong>Droits d'auteur</strong><span>Ce que vous pouvez partager, ce qui demande une autorisation, et comment nous contacter.</span>"),
]
def clean_ld(o):
    if isinstance(o, dict):
        own = 'creativecommons.org/licenses/by' in str(o.get('license', ''))
        for k in ('license', 'acquireLicensePage', 'creditText'):
            o.pop(k, None)
        if own and o.get('@type') == 'ImageObject':
            o['copyrightNotice'] = '© Tous prêts'
            o['creditText'] = 'Tous prêts'
        for v in o.values(): clean_ld(v)
    elif isinstance(o, list):
        for v in o: clean_ld(v)
n = 0
for f in glob.glob(os.path.join(site, '*.html')):
    s = open(f, encoding='utf-8').read(); t = s
    for a, b in REPL: t = t.replace(a, b)
    t = re.sub(r'Les photos sont libres de droits \(domaine public\) et créditées sur la page <a href="licence-visuels.html">[^<]*</a>\.', 'Les photos sont utilisées dans le respect de leurs licences ; voir la page <a href="licence-visuels.html">Droits d\'auteur</a>.', t)
    t = re.sub(r'<strong>Réutiliser nos visuels</strong><span>.*?</span>', "<strong>Droits d'auteur</strong><span>Ce que vous pouvez partager, ce qui demande une autorisation, et comment nous contacter.</span>", t)
    t = re.sub(r'Tous prêts, <a href="https://creativecommons\.org/licenses/by/4\.0/deed\.fr" rel="license">licence CC BY 4\.0</a> : réutilisation libre en citant tousprets\.fr\.?', '© Tous prêts, tous droits réservés.', t)
    t = re.sub(r', licence CC BY 4\.0 : réutilisation libre en citant tousprets\.fr\.', ' — © Tous prêts, tous droits réservés.', t)
    t = re.sub(r'\s*\(licence Creative Commons Attribution 4\.0 International\)', '', t)
    def ld(m):
        try: o = json.loads(m.group(2))
        except Exception: return m.group(0)
        clean_ld(o)
        if os.path.basename(f) == 'licence-visuels.html':
            DESC = "Textes, infographies, logo et application Tous prêts sont protégés par le droit d'auteur : ce qui est permis et comment demander une autorisation."
            def fix(x):
                if isinstance(x, dict):
                    if '@graph' in x: x['@graph'] = [g for g in x['@graph'] if not (isinstance(g, dict) and g.get('@type') == 'FAQPage')]
                    for k, v in list(x.items()):
                        if isinstance(v, str) and ('CC BY' in v or 'libres de droits' in v or "c'est libre" in v):
                            x[k] = DESC if k == 'description' else "Droits d'auteur et réutilisation des contenus"
                        else: fix(v)
                elif isinstance(x, list):
                    for v in x: fix(v)
            fix(o)
            if isinstance(o, dict) and o.get('@type') == 'FAQPage': return ''
        return m.group(1) + json.dumps(o, ensure_ascii=False) + m.group(3)
    t = re.sub(r'(<script type="application/ld\+json">)(.*?)(</script>)', ld, t, flags=re.S)
    if os.path.basename(f) == 'licence-visuels.html' and 'Droits d\'auteur et réutilisation des contenus</h1>' not in t:
        t = re.sub(r'<main id="contenu">.*?</main>', lambda m: MAIN, t, count=1, flags=re.S)
    if t != s:
        open(f, 'w', encoding='utf-8').write(t); n += 1
# sitemap : retirer les licences d'images éventuelles
sm = os.path.join(site, 'sitemap.xml')
if os.path.exists(sm):
    s = open(sm, encoding='utf-8').read(); t = re.sub(r'\s*<image:license>.*?</image:license>', '', s)
    if t != s: open(sm, 'w', encoding='utf-8').write(t)
print('droits_v11 :', n, 'page(s)')
