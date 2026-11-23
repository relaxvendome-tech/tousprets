"""Espaces insécables avant : ? ! ; dans les titres h1-h4 (évite « : que faire ? » en début de ligne). Idempotent."""
import re,sys,glob,os
site=sys.argv[1] if len(sys.argv)>1 else '.'
H=re.compile(r'(<h[1-4][^>]*>)(.*?)(</h[1-4]>)',re.S)
def fix(m): return m.group(1)+re.sub(r' ([:?!;])(?=\s|<|$)',' \\1',m.group(2))+m.group(3)
n=0
for f in glob.glob(os.path.join(site,'*.html')):
    s=open(f,encoding='utf-8').read(); t=H.sub(fix,s)
    if t!=s: open(f,'w',encoding='utf-8').write(t); n+=1
print('typo_fr :',n,'page(s)')
