#!/usr/bin/env python3
"""prevnext_v5.py — Bloc « Guide précédent / Guide suivant » dans chaque univers.

Usage : python3 prevnext_v5.py /chemin/du/site
Pour chaque guide rattaché à un univers (UNIV / CAT de redesign.py), insère avant
le bloc de partage (<div class="share noprint">) un petit bloc de navigation dans
l'ordre de l'univers. Idempotent : le bloc (<nav class="pn" …>…</nav><!-- /pn -->)
est retiré puis régénéré à chaque passage. Les pages absentes sont sautées.
"""
import os, re, sys, html

HERE = os.path.dirname(os.path.abspath(__file__))
sys.dont_write_bytecode = True
sys.path.insert(0, HERE)
from redesign import CAT, UNIV, GROUPS, PILLARS  # noqa: E402

BLOCK = re.compile(r'<nav class="pn(?: [^"]*)?"[^>]*>.*?</nav><!-- /pn -->\n?', re.S)
ARROW_L = '<span class="pn-ar" aria-hidden="true">←</span>'
ARROW_R = '<span class="pn-ar" aria-hidden="true">→</span>'


def build(slug, site):
    cat = CAT.get(slug, (None,))[0]
    if cat not in UNIV or slug not in UNIV[cat]:
        return None
    seq = [x for x in UNIV[cat] if os.path.exists(os.path.join(site, x + ".html"))]
    if slug not in seq or len(seq) < 2:
        return None
    i = seq.index(slug)
    prev = seq[i - 1] if i > 0 else None
    nxt = seq[i + 1] if i + 1 < len(seq) else None
    gname = dict((g[0], g[1]) for g in GROUPS).get(cat, "")
    pillar = PILLARS.get(cat, "tous-les-guides")

    def link(s, cls, lab, ar_l="", ar_r=""):
        return (f'<a class="pn-a {cls}" href="{s}.html" rel="{"prev" if cls == "pn-prev" else "next"}">'
                f'{ar_l}<span class="pn-t"><small>{lab}</small><strong>{html.escape(CAT[s][4])}</strong></span>{ar_r}</a>')

    parts = [link(prev, "pn-prev", "Guide précédent", ar_l=ARROW_L) if prev else '<span class="pn-a pn-empty"></span>',
             link(nxt, "pn-next", "Guide suivant", ar_r=ARROW_R) if nxt else '<span class="pn-a pn-empty"></span>']
    return (f'<nav class="pn noprint" aria-label="Dans l\'univers « {html.escape(gname)} »">'
            f'<p class="pn-u">Guide {i + 1} sur {len(seq)} · <a href="{pillar}.html">{html.escape(gname)}</a></p>'
            f'<div class="pn-row">{"".join(parts)}</div></nav><!-- /pn -->\n')


def main():
    if len(sys.argv) != 2 or not os.path.isdir(sys.argv[1]):
        sys.exit("Usage : python3 prevnext_v5.py /chemin/du/site")
    site = sys.argv[1]
    n = 0
    for f in sorted(os.listdir(site)):
        if not f.endswith(".html") or f == "index.html":
            continue
        p = os.path.join(site, f)
        s = open(p, encoding="utf-8").read()
        o = s
        s = BLOCK.sub("", s)
        blk = build(f[:-5], site)
        if blk and '<div class="share noprint">' in s:
            s = s.replace('<div class="share noprint">', blk + '<div class="share noprint">', 1)
        if s != o:
            open(p, "w", encoding="utf-8").write(s)
            n += 1
    print("prevnext_v5 : pages modifiées", n)


if __name__ == "__main__":
    main()
