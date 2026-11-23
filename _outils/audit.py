import re,glob,json,os,html,collections,csv
SITE="/home/claude/tousprets"
pages={}
for f in sorted(glob.glob(SITE+"/*.html")):
    n=os.path.basename(f); s=open(f,encoding='utf-8').read()
    g=lambda p: (re.search(p,s,re.S) or [None,None])[1]
    main=s[s.find('<main'):s.find('</main>')] if '<main' in s else s
    txt=re.sub(r'\s+',' ',re.sub(r'<[^>]+>',' ',re.sub(r'<(script|style)[^>]*>.*?</\1>','',main,flags=re.S)))
    ld=[]
    for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>',s,re.S):
        try:
            j=json.loads(b); items=j.get('@graph',[j]); ld+= [i.get('@type') for i in items]
        except: ld.append('INVALID')
    imgs=re.findall(r'<img[^>]*>',s)
    pages[n]=dict(title=html.unescape(g(r'<title>(.*?)</title>') or ''),desc=html.unescape(g(r'name="description" content="(.*?)"') or ''),
      h1=len(re.findall(r'<h1[\s>]',s)),h2=len(re.findall(r'<h2[\s>]',main)),canon=g(r'rel="canonical" href="(.*?)"'),
      og=sorted(set(re.findall(r'property="og:([a-z_:]+)"',s))),tw=bool(re.search(r'name="twitter:card"',s)),robots=g(r'name="robots" content="(.*?)"'),
      ld=ld,words=len(txt.split()),noalt=sum(1 for i in imgs if 'alt=' not in i),nodim=sum(1 for i in imgs if 'width=' not in i),
      links=set(re.findall(r'href="([a-z0-9-]+\.html)',main)),txt=txt.lower())
inl=collections.Counter(l for p in pages.values() for l in p['links'])
def sh(t): w=re.findall(r'\w+',t); return {' '.join(w[i:i+5]) for i in range(len(w)-4)}
S={k:sh(v['txt']) for k,v in pages.items()}
sim=[]
ks=list(pages)
for i,a in enumerate(ks):
    for b in ks[i+1:]:
        if S[a] and S[b]:
            j=len(S[a]&S[b])/len(S[a]|S[b])
            if j>0.12: sim.append((round(j,2),a,b))
titles=collections.Counter(p['title'] for p in pages.values())
rows=[]
for k,p in pages.items():
    issues=[]
    if not 30<=len(p['title'])<=65: issues.append(f"title {len(p['title'])} car.")
    if titles[p['title']]>1: issues.append("title en double")
    if not 110<=len(p['desc'])<=165: issues.append(f"description {len(p['desc'])} car.")
    if p['h1']!=1: issues.append(f"{p['h1']} H1")
    if not p['canon']: issues.append("pas de canonical")
    miss=[x for x in ['title','description','type','url','image','site_name','locale'] if x not in p['og']]
    if miss: issues.append("OG manquants: "+",".join(miss))
    if not p['tw']: issues.append("pas de Twitter card")
    if p['noalt']: issues.append(f"{p['noalt']} img sans alt")
    if p['words']<350 and k not in('index.html','privacy.html'): issues.append(f"contenu court ({p['words']} mots)")
    if inl[k]==0 and k!='index.html': issues.append("page orpheline (0 lien interne)")
    if 'INVALID' in p['ld']: issues.append("JSON-LD invalide")
    rows.append([k,p['title'],len(p['title']),p['desc'],len(p['desc']),p['h1'],p['h2'],p['words'],inl[k],"/".join(x for x in p['ld'] if x),"; ".join(issues)])
with open('/tmp/audit.csv','w',newline='',encoding='utf-8-sig') as f:
    w=csv.writer(f,delimiter=';'); w.writerow(['URL','Title','Long.','Meta description','Long.','H1','H2','Mots','Liens entrants','Schema','Problèmes']); w.writerows(rows)
c=collections.Counter()
for r in rows:
    for i in r[-1].split('; '):
        if i: c[re.sub(r'\d+','N',i.split(':')[0])]+=1
print(len(rows),'pages'); print(c.most_common(20))
print('Similarité >0.12:',sorted(sim,reverse=True)[:12])
print('orphelines',[r[0] for r in rows if 'orpheline' in r[-1]])
