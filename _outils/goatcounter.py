"""Mesure d'audience GoatCounter (sans cookie) : script hébergé sur le site + autorisation CSP. Idempotent.
Usage : python3 goatcounter.py <site>"""
import sys, os, glob
site = sys.argv[1] if len(sys.argv) > 1 else '.'
TAG = '<script data-goatcounter="https://tousprets.goatcounter.com/count" async src="count.js"></script>'
GC = 'https://tousprets.goatcounter.com'
n = 0
for f in glob.glob(os.path.join(site, '*.html')):
    s = open(f, encoding='utf-8').read(); t = s
    if os.path.basename(f) == 'privacy.html':
        continue
    if 'data-goatcounter=' not in t and '</head>' in t:
        t = t.replace('</head>', TAG + '\n</head>', 1)
    if "connect-src 'self';" in t:
        t = t.replace("img-src 'self' data: blob:;", "img-src 'self' data: blob: " + GC + ";", 1)
        t = t.replace("connect-src 'self';", "connect-src 'self' " + GC + ";", 1)
    if t != s:
        open(f, 'w', encoding='utf-8').write(t); n += 1
print('goatcounter :', n, 'page(s)')
