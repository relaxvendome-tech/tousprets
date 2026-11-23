import sys,re,os
SITE="/home/claude/tousprets"
existing={f[:-5] for f in os.listdir(SITE) if f.endswith('.html')}
NEW=set()
def load(path):
    P=[]
    def page(**k): P.append(k)
    src=open(path,encoding='utf-8').read()
    src=re.sub(r'^```\w*\n|```\s*$','',src.strip(),flags=re.M)
    i=src.find('"""SOURCES'); code=src if i<0 else src[:i]
    exec(code,{'page':page})
    return P
if __name__=="__main__":
    allp=[]
    for path in sys.argv[1:]:
        P=load(path); allp+=P; NEW.update(p['slug'] for p in P)
    for p in allp:
        html=" ".join(b for _,_,b in p['sections'])
        tags=set(re.findall(r'<([a-z0-9]+)',html))-{'p','strong','em','a','ul','li','ol','table','thead','tbody','tr','th','td','div','h3','span','br'}
        links=[l for l in re.findall(r'href="([a-z0-9-]+)\.html"',html)+p['related'] if l not in existing and l not in NEW]
        print(f"## {p['slug']} | T{len(p['title'])} D{len(p['desc'])} L{len(p['lead'].split())}w S{len(p['sections'])} F{len(p['faq'])}"
              +(f" BADTAGS{tags}" if tags else "")+(f" BADLINKS{links}" if links else ""))
        txt=re.sub(r'<[^>]+>',' ',html)+' '+' '.join(a for _,a in p['faq'])
        sents=[s.strip() for s in re.split(r'(?<=[.!?])\s+',re.sub(r'\s+',' ',txt)) if re.search(r'\d',s)]
        for s in sents: print('  -',s[:220])
