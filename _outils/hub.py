# -*- coding: utf-8 -*-
import sys; sys.path.insert(0, "/home/claude/seo")
import newpages as N
import redesign as R
secs = []
for gid, title, intro in R.GROUPS:
    slugs = [s for s, v in R.CAT.items() if v[0] == gid]
    secs.append((gid, title, f"<p>{intro}</p>" + R.cards(slugs)))
p = dict(
 slug="tous-les-guides", emoji="📚",
 title="Kit d'urgence 72h : tous nos guides pratiques",
 desc="Tous les guides Tous prêts : la liste du kit 72h, l'eau, les aliments, le guide officiel, FR-Alert, les risques (coupure, inondation, tempête) et le matériel.",
 h1="Kit d'urgence 72 h : tous nos guides",
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
h = N.build(p).replace('<main id="contenu">', '<main id="contenu" class="wide">', 1)
open(f"{N.SITE}/tous-les-guides.html", "w", encoding="utf-8").write(h)
print("hub ok")
