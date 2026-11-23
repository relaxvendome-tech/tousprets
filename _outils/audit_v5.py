#!/usr/bin/env python3
"""audit_v5.py — Audit SEO / intégrité de toutes les pages de tousprets.fr.

Usage : python3 audit_v5.py /chemin/du/site   (code de sortie 1 s'il reste des défauts)
Contrôles : title et meta description uniques, un seul H1, canonical = URL de la
page, og:title / og:description / og:image, JSON-LD valide, alt sur chaque <img>,
liens internes et ancres non cassés, pages publiques (non noindex) présentes dans
sitemap.xml (et inversement), robots.txt cohérent.
"""
import os, re, sys, json, html
from urllib.parse import urlparse, unquote

BASE = "https://tousprets.fr/"


def url_of(f):
    return BASE if f == "index.html" else BASE + f


def main():
    site = sys.argv[1] if len(sys.argv) > 1 else "."
    pages = sorted(f for f in os.listdir(site) if f.endswith(".html") and not f.startswith("google"))
    errs, warns = [], []
    titles, descs, public = {}, {}, set()
    ids_cache = {}

    def ids(f):
        if f not in ids_cache:
            s = open(os.path.join(site, f), encoding="utf-8").read()
            ids_cache[f] = set(re.findall(r'\bid="([^"]+)"', s)) | set(re.findall(r'\bname="([^"]+)"', s))
        return ids_cache[f]

    for f in pages:
        s = open(os.path.join(site, f), encoding="utf-8").read()
        noindex = bool(re.search(r'<meta name="robots" content="[^"]*noindex', s))
        redirect = 'http-equiv="refresh"' in s
        if not noindex:
            public.add(f)
        t = re.search(r"<title>(.*?)</title>", s, re.S)
        if not t or not t.group(1).strip():
            errs.append(f"{f}: title absent")
        else:
            titles.setdefault(html.unescape(t.group(1).strip()), []).append(f)
        d = re.search(r'<meta name="description" content="([^"]*)"', s)
        if not d or not d.group(1).strip():
            errs.append(f"{f}: meta description absente")
        else:
            descs.setdefault(d.group(1).strip(), []).append(f)
            if not noindex and not (50 <= len(html.unescape(d.group(1))) <= 170):
                warns.append(f"{f}: description de {len(html.unescape(d.group(1)))} caractères")
        body = re.sub(r"<(script|style|template)\b.*?</\1>", "", s, flags=re.S)
        h1 = len(re.findall(r"<h1[\s>]", body))
        if h1 != 1:
            errs.append(f"{f}: {h1} H1")
        canon = re.findall(r'<link rel="canonical" href="([^"]*)"', s)
        if len(canon) != 1:
            errs.append(f"{f}: {len(canon)} balises canonical")
        elif not redirect and canon[0] != url_of(f):
            errs.append(f"{f}: canonical {canon[0]} != {url_of(f)}")
        for p in ("og:title", "og:description", "og:image"):
            if not redirect and f'property="{p}"' not in s:
                errs.append(f"{f}: {p} absent")
        for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
            try:
                json.loads(m.group(1))
            except Exception as e:
                errs.append(f"{f}: JSON-LD invalide ({e})")
        if not redirect and "application/ld+json" not in s:
            warns.append(f"{f}: pas de JSON-LD")
        for img in re.findall(r"<img\b[^>]*>", s):
            if not re.search(r'\salt="', img):
                errs.append(f"{f}: <img> sans alt : {img[:80]}")
        # liens internes
        for href in set(re.findall(r'\b(?:href|src)="([^"]+)"', body)):
            if href.startswith(("http:", "https:", "mailto:", "tel:", "sms:", "data:", "javascript:", "//")):
                continue
            u = urlparse(href)
            path, frag = unquote(u.path), u.fragment
            if path in ("", "./", "/"):
                target = f if path == "" else "index.html"
            else:
                target = path.lstrip("./") if path.startswith("./") else path.lstrip("/")
            if not os.path.exists(os.path.join(site, target)):
                errs.append(f"{f}: lien cassé {href}")
                continue
            if frag and target.endswith(".html") and frag not in ids(target):
                errs.append(f"{f}: ancre introuvable {href}")
    for t, fs in titles.items():
        if len(fs) > 1:
            errs.append(f"title en double ({t[:50]}…) : {', '.join(fs)}")
    for d, fs in descs.items():
        if len(fs) > 1:
            errs.append(f"description en double : {', '.join(fs)}")
    # sitemap
    sm = open(os.path.join(site, "sitemap.xml"), encoding="utf-8").read()
    locs = re.findall(r"<loc>(.*?)</loc>", sm)
    inmap = set("index.html" if l == BASE else l.replace(BASE, "") for l in locs)
    for f in sorted(public - inmap):
        errs.append(f"sitemap : page publique absente {f}")
    for f in sorted(inmap - public):
        errs.append(f"sitemap : {f} listée mais absente ou noindex")
    if len(locs) != len(set(locs)):
        errs.append("sitemap : URL en double")
    # robots.txt
    rb = open(os.path.join(site, "robots.txt"), encoding="utf-8").read()
    if "Sitemap: https://tousprets.fr/sitemap.xml" not in rb:
        errs.append("robots.txt : ligne Sitemap absente")
    for dis in re.findall(r"(?im)^Disallow:\s*(\S+)", rb):
        for f in public:
            if ("/" + f).startswith(dis):
                errs.append(f"robots.txt : {f} publique mais bloquée ({dis})")
    print(f"audit_v5 : {len(pages)} pages, {len(public)} publiques, {len(locs)} URL dans le sitemap")
    print(f"ERREURS : {len(errs)}")
    for e in errs:
        print("  -", e)
    print(f"Avertissements : {len(warns)}")
    for w in warns:
        print("  ·", w)
    sys.exit(1 if errs else 0)


if __name__ == "__main__":
    main()
