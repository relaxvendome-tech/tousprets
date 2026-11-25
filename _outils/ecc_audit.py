#!/usr/bin/env python3
"""Audit économe en tokens de tousprets.fr, inspiré des agents ECC
(seo-specialist, performance-optimizer, a11y-architect, security-reviewer).

N'affiche QUE les problèmes, triés par gravité, au format court ECC :
  [GRAVITÉ] fichier : problème
Usage : python3 _outils/ecc_audit.py [racine_du_site] [--max N] [--json]
Sortie limitée à N lignes (défaut 40) pour économiser le contexte.
"""
import json, re, sys, os
from html.parser import HTMLParser
from pathlib import Path
from collections import Counter, defaultdict

ROOT = Path(next((a for a in sys.argv[1:] if not a.startswith("--")), "."))
MAX = int(sys.argv[sys.argv.index("--max") + 1]) if "--max" in sys.argv else 40
AS_JSON = "--json" in sys.argv
SKIP = {"_outils", "node_modules", ".git", "fonts"}
SITE = "https://tousprets.fr/"


class P(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = ""; self._t = False
        self.meta = {}; self.canon = None; self.robots = ""
        self.h1 = 0; self.heads = []; self.imgs_noalt = 0; self.imgs_nodim = 0
        self.imgs = 0; self.links = []; self.jsonld = []; self._j = False
        self.lang = None; self.ext_blank_noopener = 0; self.scripts_blocking = 0
        self.inline_handlers = 0; self.text = []; self._skip = 0

    def handle_starttag(self, tag, a):
        a = dict(a)
        if any(k.startswith("on") for k in a): self.inline_handlers += 1
        if tag == "html": self.lang = a.get("lang")
        elif tag == "title": self._t = True
        elif tag == "meta":
            n = (a.get("name") or a.get("property") or "").lower()
            if n: self.meta[n] = a.get("content", "")
            if n == "robots": self.robots = (a.get("content") or "").lower()
        elif tag == "link" and "canonical" in (a.get("rel") or ""): self.canon = a.get("href")
        elif tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self.heads.append(int(tag[1]))
            if tag == "h1": self.h1 += 1
        elif tag == "img":
            self.imgs += 1
            if a.get("alt") is None: self.imgs_noalt += 1
            if not (a.get("width") and a.get("height")): self.imgs_nodim += 1
        elif tag == "a" and a.get("href"):
            self.links.append(a["href"])
            if a.get("target") == "_blank" and "noopener" not in (a.get("rel") or "") \
                    and a["href"].startswith("http"):
                self.ext_blank_noopener += 1
        elif tag == "script":
            if a.get("type") == "application/ld+json": self._j = True; self.jsonld.append("")
            elif a.get("src") and "defer" not in a and "async" not in a and a.get("type") != "module":
                self.scripts_blocking += 1
            self._skip += 1
        elif tag == "style": self._skip += 1

    def handle_endtag(self, tag):
        if tag == "title": self._t = False
        if tag in ("script", "style"): self._skip = max(0, self._skip - 1); self._j = False

    def handle_data(self, d):
        if self._t: self.title += d
        if self._j: self.jsonld[-1] += d
        elif not self._skip: self.text.append(d)


def main():
    pages = sorted(p for p in ROOT.rglob("*.html") if not (set(p.relative_to(ROOT).parts) & SKIP))
    names = {p.relative_to(ROOT).as_posix() for p in pages}
    issues = []  # (rang, gravité, fichier, message)
    add = lambda r, g, f, m: issues.append((r, g, f, m))
    titles, descs, inbound = defaultdict(list), defaultdict(list), Counter()
    sitemap = (ROOT / "sitemap.xml").read_text("utf-8", "ignore") if (ROOT / "sitemap.xml").exists() else ""
    robots = (ROOT / "robots.txt").read_text("utf-8", "ignore") if (ROOT / "robots.txt").exists() else ""
    if not sitemap: add(0, "CRITIQUE", "sitemap.xml", "absent")
    if "sitemap" not in robots.lower(): add(1, "HAUTE", "robots.txt", "ne déclare pas le sitemap")

    for p in pages:
        f = p.relative_to(ROOT).as_posix()
        raw = p.read_text("utf-8", "ignore")
        h = P(); h.feed(raw)
        t = h.title.strip(); d = h.meta.get("description", "").strip()
        noindex = "noindex" in h.robots
        words = len(" ".join(h.text).split())
        if not noindex:
            titles[t].append(f); descs[d].append(f)
            if f not in ("404.html",) and sitemap and (SITE + ("" if f == "index.html" else f)) not in sitemap:
                add(1, "HAUTE", f, "absente du sitemap.xml")
        if not t: add(0, "CRITIQUE", f, "pas de <title>")
        elif not 25 <= len(t) <= 65: add(2, "MOYENNE", f, f"title {len(t)} car. (viser 30-60)")
        if not d: add(1, "HAUTE", f, "pas de meta description")
        elif not 70 <= len(d) <= 165: add(2, "MOYENNE", f, f"meta description {len(d)} car. (viser 120-160)")
        if h.h1 != 1: add(1, "HAUTE", f, f"{h.h1} balise(s) H1 (attendu : 1)")
        if any(b - a > 1 for a, b in zip(h.heads, h.heads[1:])): add(2, "MOYENNE", f, "saut de niveau de titres (ex. H2→H4)")
        if not h.canon: add(1, "HAUTE", f, "pas de canonical")
        elif not h.canon.startswith(SITE): add(0, "CRITIQUE", f, f"canonical hors domaine : {h.canon}")
        if h.lang != "fr": add(2, "MOYENNE", f, f"<html lang> = {h.lang!r}")
        if "og:title" not in h.meta or "og:image" not in h.meta: add(3, "BASSE", f, "Open Graph incomplet")
        if not h.jsonld and not noindex: add(2, "MOYENNE", f, "pas de JSON-LD")
        for j in h.jsonld:
            try: json.loads(j)
            except Exception as e: add(0, "CRITIQUE", f, f"JSON-LD invalide : {str(e)[:50]}")
        if not noindex and words < 300 and f != "index.html": add(2, "MOYENNE", f, f"contenu mince ({words} mots)")
        if h.imgs_noalt: add(1, "HAUTE", f, f"{h.imgs_noalt} image(s) sans alt (a11y)")
        if h.imgs_nodim: add(3, "BASSE", f, f"{h.imgs_nodim} image(s) sans width/height (CLS)")
        if h.scripts_blocking: add(2, "MOYENNE", f, f"{h.scripts_blocking} script(s) bloquant(s) sans defer")
        if h.ext_blank_noopener: add(2, "MOYENNE", f, f"{h.ext_blank_noopener} lien(s) target=_blank sans noopener")
        if p.stat().st_size > 150_000: add(3, "BASSE", f, f"HTML lourd ({p.stat().st_size // 1024} Ko)")
        if re.search(r"(api[_-]?key|secret|token)\s*[:=]\s*['\"][A-Za-z0-9_\-]{16,}", raw, re.I):
            add(0, "CRITIQUE", f, "secret probable dans le HTML (sécurité)")
        for l in h.links:
            l2 = l.split("#")[0].split("?")[0]
            if not l2 or l2.startswith(("http", "mailto:", "tel:", "javascript:", "data:")):
                if l2.startswith(SITE): l2 = l2[len(SITE):] or "index.html"
                else: continue
            l2 = re.sub(r"^(\./)+", "", l2).lstrip("/") or "index.html"
            if l2.endswith("/"): l2 += "index.html"
            if l2.endswith(".html"):
                if l2 not in names: add(0, "CRITIQUE", f, f"lien interne cassé → {l2}")
                elif l2 != f: inbound[l2] += 1

    for t, fs in titles.items():
        if t and len(fs) > 1: add(1, "HAUTE", fs[0], f"title dupliqué sur {len(fs)} pages : {', '.join(fs[1:3])}")
    for d, fs in descs.items():
        if d and len(fs) > 1: add(1, "HAUTE", fs[0], f"meta description dupliquée ×{len(fs)}")
    for f in names:
        if inbound[f] == 0 and f not in ("index.html", "404.html"): add(2, "MOYENNE", f, "page orpheline (0 lien interne entrant)")

    issues = sorted(set(issues))
    c = Counter(g for _, g, _, _ in issues)
    if AS_JSON:
        print(json.dumps({"pages": len(pages), "total": c, "issues": [i[1:] for i in issues[:MAX]]}, ensure_ascii=False)); return
    print(f"{len(pages)} pages | " + " ".join(f"{g}:{c[g]}" for g in ("CRITIQUE", "HAUTE", "MOYENNE", "BASSE")))
    for _, g, f, m in issues[:MAX]: print(f"[{g}] {f} : {m}")
    if len(issues) > MAX: print(f"… {len(issues) - MAX} autres (--max N pour voir plus)")


if __name__ == "__main__":
    main()
