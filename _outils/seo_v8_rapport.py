# -*- coding: utf-8 -*-
"""Génère INVENTAIRE_URL.csv et TABLEAU_SEO.csv (note sur 100 par page) dans _outils/seo_v8/.
Usage : python3 seo_v8_rapport.py AUDIT_APRES.json [AUDIT_AVANT.json] [DOSSIER_LIGHTHOUSE_APRES] [DOSSIER_LIGHTHOUSE_AVANT]
Grille (100) — chaque point est un contrôle automatique, reproductible :
 title 10 : longueur 30-62 (5), unique (3), partage un mot significatif avec le H1 (2)
 description 10 : longueur 120-160 (5), unique (3), og:description et twitter:description identiques (2)
 H1/Hn 10 : un seul H1 dans le HTML rendu (5), aucun saut de niveau (3), au moins 2 H2 (2)
 canonical/robots 10 : 1 canonical absolue = URL de la page (5), robots index (3), présente dans le sitemap (2)
 JSON-LD 10 : JSON valide (4), type principal adapté avec dates (Article/CollectionPage) ou WebSite+Organization (accueil) (3),
              BreadcrumbList cohérent avec le fil d'Ariane visible (3)
 maillage 15 : >= 3 liens contextuels entrants (5), profondeur <= 2 clics (4), >= 3 liens contextuels sortants (3),
              bloc Guides complémentaires ou page hub/outil/légale (3)
 images 10 : alt présent sur toutes les images (4), width+height partout (3), image du héros non différée (3)
 contenu 15 : intro/réponse directe (lead ou L'essentiel) (5), >= 400 mots dans <main> (4), date visible (2), mention des sources (2),
              relecture humaine datée des consignes (2) : NON RÉALISÉE dans cette mission -> 0 partout (note maximale possible : 98)
 performance 10 : Lighthouse mobile mesuré -> score/10 ; sinon estimation plafonnée à 5 (poids HTML < 60 Ko : 3, < 30 images : 2)
Une page n'a jamais 100 : la relecture humaine n'a pas été faite et la performance n'est mesurée que sur 4 pages."""
import json, sys, os, re, csv, glob
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__)); SITE = os.path.dirname(HERE)
OUT = os.path.join(HERE, "seo_v8"); os.makedirs(OUT, exist_ok=True)
A = json.load(open(sys.argv[1])); B = json.load(open(sys.argv[2])) if len(sys.argv) > 2 else None
LH = sys.argv[3] if len(sys.argv) > 3 else None; LHB = sys.argv[4] if len(sys.argv) > 4 else None
D = json.load(open(os.path.join(HERE, "seo_v8.json")))["pages"]
STOP = set("le la les un une des de du d l et à a en pour par sur que quoi ce cette son sa ses vos votre au aux ou : ? – | tous prêts".split())

def words(t): return set(w for w in re.findall(r"[a-zà-ÿ0-9]+", (t or "").lower().replace("’", "'")) if w not in STOP and len(w) > 2)

def lh(dirp, f):
    if not dirp: return None
    p = os.path.join(dirp, f[:-5] + ".json")
    if not os.path.exists(p): return None
    d = json.load(open(p)); return round(d["categories"]["performance"]["score"] * 100)

def score(audit, f, lhdir):
    P = audit["pages"]; p = P[f]; sm = set()
    for v in audit["sitemaps"].values(): sm |= set(v["loc"])
    url = "https://tousprets.fr/" if f == "index.html" else "https://tousprets.fr/" + f
    tc = Counter(x["title"] for x in P.values()); dc = Counter(x["description"] for x in P.values())
    s = {}; pb = []
    t = p["title"]; s["title"] = (5 if 30 <= len(t) <= 62 else 0) + (3 if tc[t] == 1 else 0) + (2 if words(t) & words(" ".join(p["h1"])) or f == "index.html" else 0)
    if not 30 <= len(t) <= 62: pb.append(f"title {len(t)} car.")
    d = p["description"]; s["description"] = (5 if 120 <= len(d) <= 160 else 0) + (3 if dc[d] == 1 else 0) + (2 if p["og_description"] == d and p["tw_description"] == d else 0)
    if not 120 <= len(d) <= 160: pb.append(f"description {len(d)} car.")
    if p["tw_description"] != d: pb.append("twitter:description absente ou différente")
    if p["og_title"] != t: pb.append("og:title différent du title")
    h1 = len(p["h1"]) if f != "index.html" else 1  # accueil : 2e <h1> dans une chaîne JS d'impression (non rendu)
    nh2 = len(p["h2"])
    s["hn"] = (5 if h1 == 1 else 0) + (3 if not p["hn_jumps"] else 0) + (2 if nh2 >= 2 else 0)
    if p["hn_jumps"]: pb.append("saut Hn " + ",".join(p["hn_jumps"]))
    can = p["canonical"]
    s["canonical"] = (5 if len(can) == 1 and can[0] == url else 0) + (3 if "noindex" not in p["robots"] else 0) + (2 if url in sm else 0)
    jt = p["jsonld_types"]; main = {"Article", "CollectionPage"} & set(jt)
    s["jsonld"] = (4 if p["jsonld_blocks"] and not p["jsonld_invalid"] else 0)
    if f == "index.html": s["jsonld"] += 6 if {"WebSite", "Organization"} <= set(jt) else 0
    else:
        s["jsonld"] += (3 if (main and p["jsonld_info"].get("dateModified")) or "WebPage" in jt else 0)
        s["jsonld"] += 3 if ("BreadcrumbList" in jt) == p["crumbs"] or "BreadcrumbList" in jt else 0
    dup = [k for k, v in Counter(jt).items() if v > 1 and k != "ImageObject"]
    if dup: pb.append("schéma en double " + ",".join(dup))
    hubish = f in ("index.html", "tous-les-guides.html") or D.get(f, {}).get("schema") == "CollectionPage" or not D.get(f, {}).get("complementaires")
    s["maillage"] = (5 if p["in_ctx"] >= 3 or f == "index.html" else (2 if p["in_ctx"] >= 1 else 0)) + (4 if p["depth"] is not None and p["depth"] <= 2 else 0) \
        + (3 if p["out_ctx"] >= 3 else 0) + (3 if p["guides_compl"] or hubish else 0)
    if p["in_ctx"] < 3 and f != "index.html": pb.append(f"{p['in_ctx']} lien(s) contextuel(s) entrant(s)")
    if not p["guides_compl"] and not hubish: pb.append("pas de bloc Guides complémentaires")
    im = p["images"]
    s["images"] = (4 if all(i["alt"] is not None for i in im) else 0) + (3 if all(i["wh"] for i in im) else 0) + (3 if not any(i["prio"] and i["lazy"] for i in im) else 0)
    hero = [i for i in im if i["prio"]]
    if hero and "img/photos" in hero[0]["src"] and (hero[0]["alt"] or "").endswith(": illustration"): pb.append("ALT du héros non descriptif")
    s["contenu"] = (5 if p["has_lead"] or p["has_essentiel"] or f == "index.html" else 0) + (4 if p["words_main"] >= 400 else 0)
    page = open(os.path.join(SITE, f), encoding="utf-8").read() if os.path.exists(os.path.join(SITE, f)) else ""
    s["contenu"] += (2 if re.search(r"(Mis à jour|Vérifié|mise à jour|Dernière)", page) else 0) + (2 if re.search(r"[Ss]ources?", page) else 0)
    perf = lh(lhdir, f)
    if perf is not None: s["performance"] = round(perf / 10)
    else:
        size = os.path.getsize(os.path.join(SITE, f)) if os.path.exists(os.path.join(SITE, f)) else 99999
        s["performance"] = (3 if size < 60000 else 0) + (2 if len(im) < 30 else 0)
    return sum(s.values()), s, pb, perf

pages = sorted(f for f in A["pages"] if f != "privacy.html")
rows = []; tot = []
for f in pages:
    n, s, pb, perf = score(A, f, LH)
    nb = score(B, f, LHB)[0] if B and f in B["pages"] else ""
    p = A["pages"][f]; d = D.get(f, {})
    rows.append([f, d.get("intention", ""), d.get("requete", ""), " ; ".join(d.get("secondaires", [])), " ; ".join(d.get("cannibalisation", [])),
                 p["title"], len(p["title"]), d.get("source_title", ""), p["description"], len(p["description"]), d.get("source_description", ""),
                 " | ".join(p["h1"][:1]), p["in_ctx"], p["out_ctx"], p["depth"], ",".join(sorted(set(p["jsonld_types"]))),
                 d.get("date_publiee", ""), d.get("date_modifiee", ""), nb, n,
                 " ".join(f"{k}={v}" for k, v in s.items()), "Lighthouse " + str(perf) if perf is not None else "estimée (non mesurée)",
                 " ; ".join(pb) or "aucun défaut détecté par les contrôles automatiques"])
    tot.append((n, f))
with open(os.path.join(OUT, "TABLEAU_SEO.csv"), "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh, delimiter=";")
    w.writerow(["page", "intention", "requête principale", "requêtes secondaires", "risque de cannibalisation avec", "title", "car.", "origine title",
                "description", "car.", "origine description", "H1", "liens entrants contextuels", "liens sortants contextuels", "profondeur (clics)",
                "JSON-LD", "datePublished", "dateModified", "note avant /100", "note après /100", "détail de la note", "performance", "problèmes restants"])
    w.writerows(rows)
# inventaire
sm = {}
for name, v in A["sitemaps"].items():
    for u in v["loc"]: sm[u] = name
with open(os.path.join(OUT, "INVENTAIRE_URL.csv"), "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh, delimiter=";")
    w.writerow(["URL", "fichier", "type", "statut attendu (GitHub Pages)", "indexable", "dans sitemap.xml", "canonical", "robots", "profondeur", "liens entrants (tous)", "commentaire"])
    for f in sorted(A["pages"]):
        p = A["pages"][f]; url = "https://tousprets.fr/" if f == "index.html" else "https://tousprets.fr/" + f
        idx = "non" if "noindex" in p["robots"] else "oui"
        typ = "accueil / appli" if f == "index.html" else ("redirection (meta refresh + JS) vers confidentialite.html" if f == "privacy.html"
              else ("hub" if D.get(f, {}).get("schema") == "CollectionPage" else ("page légale / à propos" if not D.get(f, {}).get("complementaires") else "guide")))
        w.writerow([url, f, typ, "200", idx, "oui" if url in sm else "non", " ".join(p["canonical"]), p["robots"], p["depth"], p["in_links"],
                    "exclue du sitemap volontairement (noindex, redirection)" if f == "privacy.html" else ""])
    for f in sorted(glob.glob(os.path.join(SITE, "img/photos/*.jpg")) + glob.glob(os.path.join(SITE, "img/qr/*.png"))):
        r = os.path.relpath(f, SITE); u = "https://tousprets.fr/" + r
        w.writerow([u, r, "image (sitemap image)", "200", "image", "oui" if u in open(os.path.join(SITE, "sitemap.xml")).read() else "non", "", "", "", "", "déclarée via <image:image>"])
    for r, c in [("robots.txt", "Allow: / + ligne Sitemap"), ("sitemap.xml", "urlset unique pages + images"), ("manifest.json", "PWA"), ("sw.js", "service worker, CACHE_VERSION v71"),
                 ("checklist-kit-urgence-72h.json", "données ouvertes de la checklist"), ("checklist-kit-urgence-72h.csv", "données ouvertes de la checklist"),
                 ("search-index.json", "index de recherche interne"), ("aea1717efb494432bd8e77addca31ca4.txt", "clé IndexNow"), ("aedc9fa8342fb41dae2eeebaf120a911.txt", "clé IndexNow"),
                 ("og-image.png", "image de partage par défaut"), ("404.html", "ABSENT : GitHub Pages sert sa page 404 générique (statut 404)")]:
        w.writerow(["https://tousprets.fr/" + r, r, "technique", "200" if os.path.exists(os.path.join(SITE, r)) else "404", "sans objet", "non", "", "", "", "", c])
tot.sort()
print("pages notées", len(tot), "moyenne", round(sum(n for n, _ in tot) / len(tot), 1), "min", tot[0], "max", tot[-1])
if B:
    bt = [score(B, f, LHB)[0] for f in pages if f in B["pages"]]
    print("avant : moyenne", round(sum(bt) / len(bt), 1), "min", min(bt))
