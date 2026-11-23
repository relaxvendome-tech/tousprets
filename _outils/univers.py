# -*- coding: utf-8 -*-
import sys; sys.path.insert(0, "/home/claude/seo")
import newpages as N
import redesign as R
REFLEXES = '''<div class="start"><p class="start-t">Les réflexes communs à toutes les alertes</p><ol class="steps-list">
<li>Mettez-vous à l'abri dans le bâtiment le plus proche, sauf consigne d'évacuer.</li>
<li>Écoutez la radio et suivez les consignes des autorités (FR-Alert, préfecture).</li>
<li>Ne vous rendez pas à l'école ou à l'établissement scolaire : les équipes appliquent le plan particulier de mise en sûreté (PPMS) et assurent la prise en charge des élèves.</li>
<li>Limitez vos appels téléphoniques aux urgences afin de ne pas saturer les réseaux mobile et fixe, et privilégiez les messages courts si nécessaire.</li></ol></div>'''
U = {
 "reagir": dict(slug="reagir-en-cas-de-crise", emoji="🚨", title="Réagir en cas de crise : les bons réflexes par situation",
   desc="Inondation, tempête, séisme, feu de forêt, coupure, confinement, alerte : les bons réflexes officiels pour chaque situation, avant, pendant et après.",
   h1="Réagir en cas de crise : les bons réflexes, situation par situation",
   lead="Face à une alerte, les premiers gestes comptent. Retrouvez ici chaque situation (inondation, tempête, séisme, feu de forêt, cyclone, canicule, froid, coupure, confinement, attaque, cyberattaque) avec les réflexes officiels avant, pendant et après.",
   pre=REFLEXES,
   faq=[("Que faire en premier quand l'alerte sonne ?","Se mettre à l'abri sauf ordre d'évacuer, écouter la radio et suivre les consignes des autorités."),
        ("Faut-il aller chercher ses enfants à l'école ?","Non. L'établissement active son plan particulier de mise en sûreté (PPMS) et encadre les élèves selon les consignes des autorités ; se déplacer vers l'école peut exposer au danger et gêner les secours."),
        ("Comment connaître les risques majeurs près de chez vous ? Consultez georisques.gouv.fr en renseignant votre adresse, ainsi que le DICRIM et les informations diffusées par votre mairie et votre préfecture.","Sur georisques.gouv.fr en saisissant votre adresse, et auprès de votre mairie (DICRIM).")]),
 "foyer": dict(slug="proteger-son-foyer", emoji="🏠", title="Protéger son foyer : enfants, aînés, handicap, animaux",
   desc="Préparer toute la famille à une crise : bébé, enfants et école, personne âgée, handicap, animaux, appartement, voiture et plan familial de mise en sûreté.",
   h1="Protéger son foyer : adapter la préparation à chaque membre de la famille",
   lead="Un kit d'urgence est d'autant plus utile qu'il est adapté à la composition et aux besoins spécifiques de votre foyer. Bébé, enfants, parents âgés, personne en situation de handicap, animaux, petit appartement ou longs trajets en voiture : voici les adaptations concrètes, et comment s'organiser en famille.",
   pre="", faq=[("Par où commencer pour toute la famille ?","Par le plan familial de mise en sûreté : qui fait quoi, où se retrouver, qui prévenir. Puis adaptez le kit à chacun."),
        ("Que prévoir pour une personne âgée ou dépendante ?","Prévoyez une réserve adaptée de médicaments prescrits avec l'ordonnance correspondante, les aides techniques indispensables (lunettes, appareils, matériel médical), les documents utiles et des personnes référentes. L'inscription sur le registre nominatif communal (géré par la mairie ou le CCAS) permet aux services municipaux de proposer un accompagnement lors d'épisodes de canicule, de grand froid ou d'autres alertes déclenchées par le préfet.")]),
 "equiper": dict(slug="s-equiper-kit-urgence", emoji="🔦", title="S'équiper pour une crise : le matériel utile, sans gadgets",
   desc="Radio à piles, lampe frontale, piles, batterie externe, trousse de secours, purification de l'eau, détecteur de fumée : quoi choisir, sans marques ni gadgets.",
   h1="S'équiper intelligemment : le matériel vraiment utile en cas de crise",
   lead="Il n'est pas nécessaire d'acheter un kit tout prêt : de nombreux objets utiles sont déjà présents au domicile et peuvent être regroupés. Ces contenus détaillent l'équipement de base, des critères de choix neutres et les règles de sécurité essentielles (prévention des intoxications au monoxyde de carbone, éclairage sûr, gestion des piles et batteries).",
   pre="", faq=[("Faut-il acheter un kit de survie tout fait ?","Non. La plupart des objets sont déjà chez vous. Complétez ce qui manque, en priorité l'eau, une lampe et une radio à piles."),
        ("Peut-on utiliser un groupe électrogène à l'intérieur ?","Jamais : un groupe électrogène dégage du monoxyde de carbone, un gaz incolore et inodore qui peut être mortel. Il doit toujours être utilisé à l'extérieur, à distance des portes, fenêtres et entrées d'air.")]),
 "anticiper": dict(slug="anticiper-s-entraider", emoji="🤝", title="Anticiper et s'entraider : se préparer en famille et entre voisins",
   desc="Faire le test « Suis-je prêt ? », préparer son plan familial, s'organiser avec ses voisins et déjouer les arnaques : se préparer ensemble, simplement.",
   h1="Anticiper et s'entraider : se préparer ensemble, à son rythme",
   lead="Se préparer ne se fait pas seul. Faites le point en 2 minutes, organisez votre famille, créez un groupe d'entraide avec vos voisins grâce à l'appli, et apprenez à repérer les fausses offres de « kit officiel ».",
   pre="", faq=[("Comment savoir si je suis prêt ?","Faites le test en 10 questions : il donne votre niveau de préparation et les 3 actions les plus utiles, sans rien enregistrer."),
        ("Comment s'organiser avec ses voisins ?","Échangez vos coordonnées avec vos voisins, soyez attentif aux personnes isolées ou vulnérables et orientez-les vers les dispositifs municipaux (mairie, CCAS) en cas de besoin.")]),
 "outremer": dict(slug="preparation-outre-mer", emoji="🌴", title="Kit d'urgence en outre-mer : cyclones, séismes, volcans",
   desc="Se préparer en Guadeloupe, Martinique, Guyane, à La Réunion, Mayotte, Saint-Martin et Saint-Barthélemy : risques du territoire, kit adapté et alertes officielles.",
   h1="Se préparer en outre-mer : les risques et le kit, territoire par territoire",
   lead="Cyclones, séismes, éruptions volcaniques, tsunamis, fortes pluies ou coupures d'eau : les risques varient selon les territoires d'outre-mer. Consultez les informations relatives à votre territoire pour connaître les risques locaux, les adaptations utiles du kit et les canaux officiels d'alerte (préfecture, Météo-France, FR-Alert).",
   pre="", faq=[("Quand se termine la saison cyclonique aux Antilles ?","Dans l'Atlantique Nord et aux Antilles, la saison cyclonique s'étend officiellement du 1er juin au 30 novembre selon Météo-France. Préparez votre kit avant le début de la saison."),
        ("Faut-il plus d'eau en outre-mer ?","Le repère de base est d'au moins 6 litres d'eau potable par personne sur 3 jours (2 litres par jour), à augmenter en cas de forte chaleur ou de contraintes d'approvisionnement locales.")]),
 "comprendre": dict(slug="comprendre-s-informer", emoji="📚", title="Comprendre la préparation aux crises : guide, glossaire",
   desc="Le guide officiel « Tous responsables » résumé, les questions pratiques, le glossaire des termes de crise, nos sources, notre méthode et notre charte éditoriale.",
   h1="Comprendre et s'informer : le guide officiel, les mots, nos sources",
   lead="Une synthèse des repères du guide « Tous responsables », des réponses aux questions pratiques, un glossaire des termes de sécurité civile et une présentation de la démarche de vérification du site.",
   pre="", faq=[("Tous prêts est-il un site officiel ?","Non. Il s'agit d'un site citoyen indépendant, sans lien institutionnel avec l'État, qui s'appuie sur des sources publiques et ne remplace pas les consignes officielles."),
        ("Où lire le guide officiel ?","Le guide « Tous responsables » est diffusé par les services de l'État, notamment sur info.gouv.fr ; vérifiez toujours que vous consultez la version officielle à jour.")]),
}
# v6 : regroupements d'affichage (uniquement des pages existantes)
SUBGROUPS = {
 "reagir": [("Alerte et danger immédiat : les premiers gestes", R.UNIV["reagir"][:8]),
            ("Les autres situations", R.UNIV["reagir"][8:])],
 "equiper": [("Eau et aliments", ["purifier-eau-pastilles-filtre", "frigo-congelateur-coupure-electricite"]),
             ("Lumière et énergie", ["lampe-frontale-lanterne-kit-urgence", "piles-kit-urgence", "batterie-externe-station-electrique", "groupe-electrogene-securite"]),
             ("Communication", ["radio-a-piles-kit-urgence", "recharger-telephone-coupure-courant"]),
             ("Soins", ["trousse-de-secours-kit-urgence"]),
             ("Chaleur", ["couverture-de-survie"]),
             ("Sécurité incendie", ["detecteur-de-fumee"])],
}
def grid(key, slugs):
    if key not in SUBGROUPS: return R.cards(slugs, short=True, eager=3)
    got = [x for _, l in SUBGROUPS[key] for x in l]
    assert sorted(got) == sorted(slugs), (key, set(got) ^ set(slugs))
    out, n = "", 0
    for t, l in SUBGROUPS[key]:
        out += f'<h3 class="ggroup">{t}</h3>' + R.cards(l, short=True, eager=max(0, 3 - n)); n += len(l)
    return out

for key, d in U.items():
    slugs = [x for x in R.UNIV[key] if x != d["slug"]]
    gname, intro = [(g[1], g[2]) for g in R.GROUPS if g[0] == key][0]
    p = dict(slug=d["slug"], emoji=d["emoji"], title=d["title"], desc=d["desc"], h1=d["h1"], lead=d["lead"],
             source="guide « Tous responsables » (SGDSN, 2025) et sites officiels", nav_label=gname, nav_emoji=d["emoji"],
             sections=([("reflexes", "Les premiers réflexes", d["pre"])] if d["pre"] else []) + [("guides", "Tous les guides : " + gname[0].lower() + gname[1:], f"<p>{intro}</p>" + grid(key, slugs))],
             faq=d["faq"], related=["diagnostic-suis-je-pret", "kit-de-survie-72h", "checklist-kit-urgence-72h"])
    N.TITLES[p["slug"]] = p["h1"]
    h = N.build(p).replace('<main id="contenu">', '<main id="contenu" class="wide">', 1)
    open(f"{N.SITE}/{p['slug']}.html", "w", encoding="utf-8").write(h)
    print("ok", p["slug"], len(p["title"]), len(p["desc"]))
