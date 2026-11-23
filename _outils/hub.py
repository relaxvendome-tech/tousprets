# -*- coding: utf-8 -*-
"""Page « Tous les guides » (tous-les-guides.html).
v6 : champ de recherche en tête (filtre en direct, logique de search.js via pages.js),
puces de filtre par rubrique (7 univers) et par public, état vide, aucune carte en double,
images en loading=lazy sauf les premières. Sans JavaScript : la page reste une liste complète."""
import sys, re, html; sys.path.insert(0, "/home/claude/seo")
import newpages as N
import redesign as R

# Public visé : uniquement des pages existantes, regroupées selon leur sujet déclaré (CAT / UNIV)
PUBLIC = [
 ("famille", "Familles et enfants", ["kit-urgence-72h-famille-appartement-voiture", "kit-urgence-bebe", "kit-urgence-enfants-ecole", "plan-familial-mise-en-surete"]),
 ("fragiles", "Aînés et handicap", ["kit-urgence-personne-agee", "kit-urgence-handicap", "entraide-voisins-crise"]),
 ("animaux", "Animaux", ["kit-urgence-animaux"]),
 ("voiture", "En voiture", ["kit-urgence-voiture", "kit-urgence-72h-famille-appartement-voiture"]),
 ("outremer", "Outre-mer", R.UNIV["outremer"] + ["cyclone-que-faire"]),
]
aud = {}
for pid, _, sl in PUBLIC:
    for x in sl: aud.setdefault(x, []).append(pid)

seen = set(); secs = []; total = 0
for gi, (gid, title, intro) in enumerate(R.GROUPS):
    # ordre de l'univers (UNIV), chaque page une seule fois, dans sa rubrique principale (CAT)
    slugs = [s for s in R.UNIV.get(gid, []) if R.CAT.get(s, ("",))[0] == gid and s not in seen]
    slugs += [s for s, v in R.CAT.items() if v[0] == gid and s not in slugs and s not in seen]
    seen.update(slugs); total += len(slugs)
    cs = "".join(R.card(s, short=True, eager=(gi == 0 and i < 4),
                        attrs=f' data-u="{gid}" data-p="{" ".join(aud.get(s, []))}"') for i, s in enumerate(slugs))
    secs.append((gid, title, f'<p>{intro}</p><div class="gcards gcards--short">{cs}</div>'))

SVG = '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>'
chips_u = '<button type="button" class="chip" data-f="u" data-v="" aria-pressed="true">Toutes</button>' + "".join(
    f'<button type="button" class="chip" data-f="u" data-v="{g}" aria-pressed="false">{html.escape(t)}</button>' for g, t, _ in R.GROUPS)
chips_p = '<button type="button" class="chip" data-f="p" data-v="" aria-pressed="true">Tout le monde</button>' + "".join(
    f'<button type="button" class="chip" data-f="p" data-v="{pid}" aria-pressed="false">{html.escape(t)}</button>' for pid, t, _ in PUBLIC)
PANEL = (f'<div class="gfilter noprint" id="gfilter" hidden><form class="gf-form" role="search" aria-label="Filtrer les guides" action="tous-les-guides.html">'
         f'<label class="gf-l" for="gq">Rechercher parmi les {total} guides</label>'
         f'<div class="gf-in">{SVG}<input id="gq" name="q" type="search" placeholder="Ex. : eau, radio, inondation, bébé…" autocomplete="off" aria-describedby="gf-n"></div></form>'
         f'<div class="gf-row"><span class="gf-t" id="gf-tu">Rubrique</span><div class="gf-chips" role="group" aria-labelledby="gf-tu">{chips_u}</div></div>'
         f'<div class="gf-row"><span class="gf-t" id="gf-tp">Public</span><div class="gf-chips" role="group" aria-labelledby="gf-tp">{chips_p}</div></div>'
         f'<div class="gf-foot"><p class="gf-n" id="gf-n" role="status" aria-live="polite">{total} guides</p><button type="button" class="linkbtn gf-clear" hidden>Tout afficher</button></div>'
         '<div class="gf-empty" hidden><p><strong>Aucun guide ne correspond à cette recherche.</strong> '
         'Essayez un mot plus simple (« eau », « radio », « coupure »), retirez un filtre, ou consultez les '
         '<a href="questions-reponses-kit-urgence.html">questions pratiques</a> et le <a href="glossaire-preparation-crise.html">glossaire</a>.</p>'
         '<button type="button" class="btn btn-2 gf-reset">Effacer la recherche et les filtres</button></div></div><!-- /gfilter -->\n')

p = dict(
 slug="tous-les-guides", emoji="📚",
 title="Kit d'urgence 72h : tous nos guides pratiques",
 desc="Tous les guides Tous prêts : la liste du kit 72h, l'eau, les aliments, le guide officiel, FR-Alert, les risques (coupure, inondation, tempête) et le matériel.",
 h1="Kit d'urgence 72\u00a0h : tous nos guides",
 lead="Se préparer chez soi, d'après le guide officiel « Tous responsables » : par où commencer, quoi adapter à votre foyer, et que faire selon chaque risque. Chaque guide est court, sourcé et gratuit.",
 source="guide « Tous responsables » (SGDSN, 2025) et sites officiels",
 nav_label="Tous les guides", nav_emoji="📚",
 sections=secs,
 faq=[("Par où commencer pour préparer son kit d'urgence ?", "Commencez par l'eau (6 litres par personne), puis la nourriture sans cuisson, la radio à piles, la lampe et les médicaments. La checklist permet de cocher au fur et à mesure."),
      ("Ces guides sont-ils officiels ?", "Non. Tous prêts est une initiative citoyenne indépendante qui s'appuie sur le guide officiel « Tous responsables » et cite ses sources. Les consignes des autorités font toujours foi."),
      ("Les guides fonctionnent-ils hors ligne ?", "Oui, une fois l'appli ouverte, les pages consultées restent disponibles sans connexion.")],
 related=["kit-de-survie-72h", "checklist-kit-urgence-72h", "questions-reponses-kit-urgence"],
)
N.TITLES[p["slug"]] = p["h1"]
h = N.build(p).replace('<main id="contenu">', '<main id="contenu" class="wide hub">', 1)
# v6 : pas de sommaire (remplacé par les puces) ni de « À lire aussi » (cartes en double)
h = re.sub(r'<nav class="toc".*?</nav>\n?', "", h, count=1, flags=re.S)
h = re.sub(r'<section id="voir-aussi".*?</section>\n?', "", h, count=1, flags=re.S)
M = '</div></div>\n<div class="wrap">\n'
assert M in h
h = h.replace(M, M + PANEL, 1)
assert len(seen) == total
open(f"{N.SITE}/tous-les-guides.html", "w", encoding="utf-8").write(h)
print("hub ok", total, "guides")
