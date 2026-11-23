"""Enrichissements adaptés des sites officiels américains (CDC, NWS, USGS, CISA, Croix-Rouge américaine). Idempotent.
Données : us_v10.json. Usage : python3 us_v10.py <site>"""
import json, re, sys, os, html
site = sys.argv[1] if len(sys.argv) > 1 else '.'
D = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'us_v10.json'), encoding='utf-8'))
ORG = {'cdc.gov': 'CDC', 'weather.gov': 'National Weather Service', 'usgs.gov': 'USGS', 'cisa.gov': 'CISA', 'redcross.org': 'Croix-Rouge américaine', 'fda.gov': 'FDA', 'ready.gov': 'Ready.gov'}
def org(u):
    for k, v in ORG.items():
        if k in u: return v
    return 'source officielle américaine'
n = 0
# 1. Questions-réponses
f = os.path.join(site, 'questions-reponses-kit-urgence.html')
s = open(f, encoding='utf-8').read(); t = s
for q in D['questions']:
    summ = '<summary>' + html.escape(q['question'], quote=False) + '</summary>'
    if summ in t: continue
    body = '<p>' + html.escape(q['reponse'], quote=False) + '</p><p class="qa-src">Conseil adapté au contexte français à partir de : <a href="' + q['source_us'] + '" rel="noopener" target="_blank">' + org(q['source_us']) + ' (États-Unis)</a>. En cas de différence, suivez les consignes des autorités françaises.</p>'
    det = '<details>' + summ + body + '</details>'
    m = re.search(r'(<section id="' + q['theme'] + r'"[^>]*>.*?<div class="faq">)(.*?)(</div></section>)', t, re.S)
    if not m: continue
    t = t[:m.end(2)] + det + t[m.end(2):]
    # JSON-LD FAQPage
    m2 = re.search(r'("@type": "FAQPage".*?"mainEntity": \[)', t, re.S)
    if m2:
        txt = q['reponse'] + ' Conseil adapté à partir de : ' + org(q['source_us']) + ' (États-Unis).'
        t = t[:m2.end()] + json.dumps({"@type": "Question", "name": q['question'], "acceptedAnswer": {"@type": "Answer", "text": txt}}, ensure_ascii=False) + ', ' + t[m2.end():]
if t != s: open(f, 'w', encoding='utf-8').write(t); n += 1
# 2. Enrichissements des guides
for e in D['enrichissements']:
    f = os.path.join(site, e['page'])
    if not os.path.exists(f): continue
    s = open(f, encoding='utf-8').read()
    mark = '<!-- us:v10 ' + str(abs(hash(e['texte'][:40])) % 10**8) + ' -->'
    key = e['texte'][:60]
    if html.escape(key, quote=False) in s or key in s: continue
    box = ('<div class="box us-tip"><p><strong>Le conseil en plus</strong> : ' + html.escape(e['texte'], quote=False) +
           ' <span class="qa-src">(adapté de <a href="' + e['source_us'] + '" rel="noopener" target="_blank">' + e['org'] + ', États-Unis</a>)</span></p></div>')
    i = s.find('<section id="faq"')
    if i < 0: continue
    s = s[:i] + box + '\n' + s[i:]
    open(f, 'w', encoding='utf-8').write(s); n += 1
print('us_v10 :', n, 'fichier(s)')
