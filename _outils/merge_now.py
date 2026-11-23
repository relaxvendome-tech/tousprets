"""Supprime le bloc .now (3 gestes) sur les pages qui ont déjà « L'essentiel » (ess:v4). Idempotent."""
import re,sys,glob,os
site=sys.argv[1] if len(sys.argv)>1 else '.'
n=0
for f in glob.glob(os.path.join(site,'*.html')):
    s=open(f,encoding='utf-8').read()
    if 'ess:v4' not in s: continue
    t=re.sub(r'<div class="now" role="note">.*?</p></div>','',s,count=1,flags=re.S)
    if t!=s: open(f,'w',encoding='utf-8').write(t); n+=1
print('merge_now :',n,'page(s)')
