# -*- coding: utf-8 -*-
import sys; sys.path.insert(0, "/home/claude/seo")
import newpages as N
import redesign as R
REFLEXES = '''<div class="start"><p class="start-t">Les réflexes communs à toutes les alertes</p><ol class="steps-list">
<li>Mettez-vous à l'abri dans le bâtiment le plus proche, sauf consigne d'évacuer.</li>
<li>Écoutez la radio et suivez les consignes des autorités (FR-Alert, préfecture).</li>
<li>N'allez pas chercher vos enfants à l'école : ils y sont protégés.</li>
<li>Ne téléphonez qu'en cas d'urgence vitale, pour laisser les lignes aux secours.</li></ol></div>'''
U = {
 "reagir": dict(slug="reagir-en-cas-de-crise", emoji="🚨", title="Réagir en cas de crise : les bons réflexes par situation",
   desc="Inondation, tempête, séisme, feu de forêt, coupure, confinement, alerte : les bons réflexes officiels pour chaque situation, avant, pendant et après.",
   h1="Réagir en cas de crise : les bons réflexes, situation par situation",
   lead="Face à une alerte, les premiers gestes comptent. Retrouvez ici chaque situation (inondation, tempête, séisme, feu de forêt, cyclone, canicule, froid, coupure, confinement, attaque, cyberattaque) avec les réflexes officiels avant, pendant et après.",
   pre=REFLEXES,
   faq=[("Que faire en premier quand l'alerte sonne ?","Se mettre à l'abri sauf ordre d'évacuer, écouter la radio et suivre les consignes des autorités."),
        ("Faut-il aller chercher ses enfants à l'école ?","Non. L'école applique son plan de mise en sûreté et les enseignants protègent les élèves."),
        ("Comment savoir quels risques concernent ma commune ?","Sur georisques.gouv.fr en saisissant votre adresse, et auprès de votre mairie (DICRIM).")]),
 "foyer": dict(slug="proteger-son-foyer", emoji="🏠", title="Protéger son foyer : enfants, aînés, handicap, animaux",
   desc="Préparer toute la famille à une crise : bébé, enfants et école, personne âgée, handicap, animaux, appartement, voiture et plan familial de mise en sûreté.",
   h1="Protéger son foyer : adapter la préparation à chaque membre de la famille",
   lead="Un kit d'urgence n'est utile que s'il correspond à votre foyer. Bébé, enfants, parents âgés, personne en situation de handicap, animaux, petit appartement ou longs trajets en voiture : voici les adaptations concrètes, et comment s'organiser en famille.",
   pre="", faq=[("Par où commencer pour toute la famille ?","Par le plan familial de mise en sûreté : qui fait quoi, où se retrouver, qui prévenir. Puis adaptez le kit à chacun."),
        ("Que prévoir pour une personne âgée ou dépendante ?","Ses traitements et ordonnances, ses aides techniques, et une personne de contact. Le registre communal permet aussi d'être aidé lors des canicules et grands froids.")]),
 "equiper": dict(slug="s-equiper-kit-urgence", emoji="🔦", title="S'équiper pour une crise : le matériel utile, sans gadgets",
   desc="Radio à piles, lampe frontale, piles, batterie externe, trousse de secours, purification de l'eau, détecteur de fumée : quoi choisir, sans marques ni gadgets.",
   h1="S'équiper intelligemment : le matériel vraiment utile en cas de crise",
   lead="Inutile d'acheter un kit de survie complet : l'essentiel se trouve souvent à la maison. Ces guides expliquent, poste par poste, ce qui sert vraiment, comment choisir sans marque imposée, et les règles de sécurité (monoxyde de carbone, bougies, piles).",
   pre="", faq=[("Faut-il acheter un kit de survie tout fait ?","Non. La plupart des objets sont déjà chez vous. Complétez ce qui manque, en priorité l'eau, une lampe et une radio à piles."),
        ("Peut-on utiliser un groupe électrogène à l'intérieur ?","Jamais : il produit du monoxyde de carbone, un gaz mortel. Il s'installe toujours à l'extérieur, loin des ouvertures.")]),
 "anticiper": dict(slug="anticiper-s-entraider", emoji="🤝", title="Anticiper et s'entraider : se préparer en famille et entre voisins",
   desc="Faire le test « Suis-je prêt ? », préparer son plan familial, s'organiser avec ses voisins et déjouer les arnaques : se préparer ensemble, simplement.",
   h1="Anticiper et s'entraider : se préparer ensemble, à son rythme",
   lead="Se préparer ne se fait pas seul. Faites le point en 2 minutes, organisez votre famille, créez un groupe d'entraide avec vos voisins grâce à l'appli, et apprenez à repérer les fausses offres de « kit officiel ».",
   pre="", faq=[("Comment savoir si je suis prêt ?","Faites le test en 10 questions : il donne un score et les 3 actions les plus utiles, sans rien enregistrer."),
        ("Comment s'organiser avec ses voisins ?","Échangez vos numéros, repérez les personnes isolées et créez un groupe d'entraide dans l'onglet Voisins de l'appli, sans compte.")]),
 "outremer": dict(slug="preparation-outre-mer", emoji="🌴", title="Kit d'urgence en outre-mer : cyclones, séismes, volcans",
   desc="Se préparer en Guadeloupe, Martinique, Guyane, à La Réunion, Mayotte, Saint-Martin et Saint-Barthélemy : risques du territoire, kit adapté et alertes officielles.",
   h1="Se préparer en outre-mer : les risques et le kit, territoire par territoire",
   lead="Cyclones, séismes, volcans, fortes pluies, coupures d'eau : les risques ne sont pas les mêmes d'un territoire à l'autre. Choisissez le vôtre pour connaître ses risques, ce qui change dans le kit 72 h et les sites officiels d'alerte.",
   pre="", faq=[("Quand se termine la saison cyclonique aux Antilles ?","Elle va du 1er juin au 30 novembre selon Météo-France. Préparez votre kit avant le début de la saison."),
        ("Faut-il plus d'eau en outre-mer ?","Le minimum reste 6 litres par personne pour 72 heures ; prévoyez davantage par forte chaleur et là où les coupures d'eau sont fréquentes.")]),
 "comprendre": dict(slug="comprendre-s-informer", emoji="📚", title="Comprendre la préparation aux crises : guide, glossaire",
   desc="Le guide officiel « Tous responsables » résumé, les questions pratiques, le glossaire des termes de crise, nos sources, notre méthode et notre charte éditoriale.",
   h1="Comprendre et s'informer : le guide officiel, les mots, nos sources",
   lead="Ce que dit vraiment le guide « Tous responsables », les réponses aux questions pratiques, les mots de la crise expliqués simplement, et la façon dont Tous prêts vérifie chaque conseil.",
   pre="", faq=[("Tous prêts est-il un site officiel ?","Non. C'est une initiative citoyenne indépendante qui s'appuie sur le guide officiel et cite ses sources."),
        ("Où lire le guide officiel ?","Sur info.gouv.fr. Notre page « Kit de survie du gouvernement en PDF » donne le lien direct.")]),
}
for key, d in U.items():
    slugs = [x for x in R.UNIV[key] if x != d["slug"]]
    gname, intro = [(g[1], g[2]) for g in R.GROUPS if g[0] == key][0]
    p = dict(slug=d["slug"], emoji=d["emoji"], title=d["title"], desc=d["desc"], h1=d["h1"], lead=d["lead"],
             source="guide « Tous responsables » (SGDSN, 2025) et sites officiels", nav_label=gname, nav_emoji=d["emoji"],
             sections=([("reflexes", "Les premiers réflexes", d["pre"])] if d["pre"] else []) + [("guides", "Tous les guides : " + gname[0].lower() + gname[1:], f"<p>{intro}</p>" + R.cards(slugs))],
             faq=d["faq"], related=["diagnostic-suis-je-pret", "kit-de-survie-72h", "checklist-kit-urgence-72h"])
    N.TITLES[p["slug"]] = p["h1"]
    h = N.build(p).replace('<main id="contenu">', '<main id="contenu" class="wide">', 1)
    open(f"{N.SITE}/{p['slug']}.html", "w", encoding="utf-8").write(h)
    print("ok", p["slug"], len(p["title"]), len(p["desc"]))
