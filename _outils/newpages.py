# -*- coding: utf-8 -*-
"""Génère les nouvelles pages longue traîne de tousprets.fr à partir du gabarit existant."""
import json, re, html

SITE = "/home/claude/tousprets"
TPL = open("/home/claude/seo/template_old.html", encoding="utf-8").read()
DATE = "2026-11-23"
DATE_FR = "23 novembre 2026"

PAGES = []

def page(**kw):
    PAGES.append(kw)

# ---------------------------------------------------------------- 1. Frigo / congélateur
page(
 slug="frigo-congelateur-coupure-electricite",
 emoji="🧊",
 title="Congélateur sans électricité : combien de temps ? (frigo 4 h)",
 desc="Frigo fermé : environ 4 h. Congélateur plein : environ 48 h, à moitié plein : 24 h. Les bons gestes pendant la coupure et quoi jeter ensuite.",
 h1="Combien de temps tient un congélateur sans électricité ?",
 lead="Un congélateur plein tient environ 48 heures sans électricité, 24 heures s'il est à moitié rempli, à condition de ne pas l'ouvrir. Un réfrigérateur fermé garde le froid environ 4 heures. Au-delà, il faut trier. Voici les repères des autorités sanitaires et les gestes qui font gagner des heures.",
 source="FDA, Département de la santé du Connecticut, guide « Tous responsables »",
 nav_label="Frigo et congélateur", nav_emoji="🧊",
 sections=[
  ("reperes","Combien de temps tiennent le frigo et le congélateur ?", """
<table class="tbl"><thead><tr><th>Appareil (porte fermée)</th><th>Garde le froid environ</th></tr></thead><tbody>
<tr><td>Réfrigérateur</td><td>4 heures</td></tr>
<tr><td>Congélateur à moitié plein</td><td>24 heures</td></tr>
<tr><td>Congélateur plein</td><td>48 heures</td></tr></tbody></table>
<p>Ces durées supposent que les portes restent fermées. Chaque ouverture fait entrer de l'air chaud et raccourcit le délai. Un congélateur plein tient plus longtemps parce que les aliments congelés se refroidissent mutuellement.</p>
<p>Ces délais montrent aussi pourquoi le guide « Tous responsables » demande un kit de <strong>nourriture qui ne nécessite ni froid ni cuisson</strong> : sur 72 heures sans électricité, le frigo et le congélateur ne suffisent pas. Voir la <a href="aliments-sans-cuisson-kit-urgence.html">liste des aliments sans cuisson</a>.</p>"""),
  ("pendant","Que faire pendant la coupure ?", """
<div class="cards"><div class="card"><h3><span class="ic" aria-hidden="true">🚪</span>Garder le froid</h3><ul><li>N'ouvrez ni le frigo ni le congélateur, sauf nécessité</li><li>Si la coupure dépasse 4 heures, transférez les aliments du frigo dans une glacière avec des pains de glace</li><li>Regroupez les produits congelés pour qu'ils se protègent entre eux</li></ul></div>
<div class="card"><h3><span class="ic" aria-hidden="true">🌡️</span>Savoir mesurer</h3><ul><li>Un thermomètre de frigo (quelques euros) permet de savoir ce qui reste sûr</li><li>Gardez à l'avance quelques bouteilles d'eau congelées : elles servent de pains de glace, puis d'eau potable</li></ul></div></div>"""),
  ("apres","Après la coupure : que garder, que jeter ?", """
<ul class="check">
<li><strong>Coupure de 4 heures ou moins, porte restée fermée</strong> : les aliments du réfrigérateur sont en principe sûrs.</li>
<li><strong>Aliments restés au-dessus de 4 °C pendant plus de 2 heures</strong> : jetez les produits sensibles (viande, poisson, plats cuisinés, produits laitiers frais, restes, œufs cuits).</li>
<li><strong>Produits décongelés</strong> : ne les recongelez pas. S'ils sont encore très froids et contiennent des cristaux de glace, cuisinez-les et mangez-les rapidement. S'ils ont complètement décongelé et se sont réchauffés, jetez-les.</li><li><strong>Conserves bombées, rouillées ou qui fuient</strong> : jetez-les sans les ouvrir ni les goûter.</li>
<li><strong>Dans le doute, jetez.</strong> Ne goûtez jamais un aliment pour vérifier : l'odeur et l'aspect ne suffisent pas à détecter les bactéries.</li>
<li>Nettoyez le réfrigérateur et le congélateur avant de les remplir à nouveau.</li></ul>
<p class="note">Ces règles valent pour un foyer. Pour les médicaments qui se conservent au froid (insuline par exemple), demandez conseil à votre pharmacien avant toute coupure prévisible.</p>"""),
 ],
 faq=[
  ("Combien de temps un congélateur tient-il sans électricité ?", "Environ 48 heures s'il est plein et environ 24 heures s'il est à moitié rempli, à condition de ne pas l'ouvrir."),
  ("Combien de temps un réfrigérateur tient-il sans électricité ?", "Environ 4 heures porte fermée. Au-delà, mettez les aliments sensibles dans une glacière."),
  ("Peut-on recongeler un aliment après une coupure ?", "Non : un aliment décongelé ne se recongèle pas. S'il est encore très froid, cuisinez-le et mangez-le rapidement ; s'il s'est réchauffé, jetez-le."),
 ],
 related=["coupure-electricite-que-faire","aliments-sans-cuisson-kit-urgence","combien-eau-stocker-par-personne"],
)

# ---------------------------------------------------------------- 2. Eau
page(
 slug="combien-eau-stocker-par-personne",
 emoji="💧",
 title="Combien de litres d'eau stocker par personne ? (72 h)",
 desc="Le guide officiel demande 6 litres d'eau par personne pour 72 heures, soit 2 litres par jour. Tableau par taille de foyer, stockage et renouvellement.",
 h1="Combien d'eau stocker par personne pour 72 heures ?",
 lead="Le guide « Tous responsables » fixe la règle : 6 litres d'eau potable par personne, en bouteilles, pour tenir 72 heures. Soit 2 litres par jour pour boire. Voici le calcul pour votre foyer, ce qu'il faut ajouter et comment stocker cette eau.",
 source="guide « Tous responsables » (SGDSN, 2025), Santé Canada",
 nav_label="Réserve d'eau", nav_emoji="💧",
 sections=[
  ("calcul","Le calcul pour votre foyer", """
<p>La règle officielle tient en une ligne : <strong>6 litres × nombre de personnes</strong>.</p>
<table class="tbl"><thead><tr><th>Personnes dans le foyer</th><th>Eau à stocker pour 72 h</th></tr></thead><tbody>
<tr><td>1</td><td>6 litres</td></tr><tr><td>2</td><td>12 litres</td></tr><tr><td>3</td><td>18 litres</td></tr>
<tr><td>4</td><td>24 litres</td></tr><tr><td>5</td><td>30 litres</td></tr><tr><td>6</td><td>36 litres</td></tr></tbody></table>
<p>L'<a href="./">appli Tous prêts</a> fait ce calcul automatiquement selon la composition de votre foyer.</p>"""),
  ("plus","Quand prévoir davantage", """
<div class="cards"><div class="card"><h3><span class="ic" aria-hidden="true">🧼</span>Hygiène et cuisine</h3><ul><li>Les 6 litres couvrent la boisson</li><li>Santé Canada conseille environ 2 litres de plus par personne et par jour pour se laver les mains, les dents et préparer les repas</li></ul></div>
<div class="card"><h3><span class="ic" aria-hidden="true">👶</span>Situations particulières</h3><ul><li>Bébé nourri au lait en poudre : eau en bouteille pour les biberons (voir le <a href="kit-urgence-bebe.html">kit bébé</a>)</li><li>Animaux : leur eau en plus (voir le <a href="kit-urgence-animaux.html">kit animaux</a>)</li><li>Forte chaleur, grossesse, maladie : prévoir plus</li></ul></div></div>"""),
  ("stocker","Comment stocker l'eau", """
<ul class="check"><li>Privilégiez des <strong>bouteilles scellées du commerce</strong> : petites bouteilles, plus faciles à transporter en cas d'évacuation.</li>
<li>Rangez-les au frais, à l'abri de la lumière, loin des produits ménagers.</li>
<li>Notez la date limite et faites tourner le stock : buvez les plus anciennes, remplacez-les. Le guide demande de vérifier le kit deux fois par an.</li>
<li>Gardez quelques bouteilles en plastique fermées au congélateur, en laissant un peu de place pour la dilatation (jamais de verre) : en cas de coupure, elles gardent le froid puis deviennent de l'eau potable.</li>
<li><strong>En dernier recours</strong>, le guide prévoit des pastilles de décontamination de l'eau. Respectez la notice et le temps d'action.</li></ul>"""),
 ],
 faq=[
  ("Combien de litres d'eau par personne pour 3 jours ?", "6 litres par personne selon le guide « Tous responsables », soit 2 litres par jour pour boire."),
  ("Combien d'eau pour une famille de 4 ?", "24 litres pour 72 heures, auxquels on peut ajouter de l'eau pour l'hygiène."),
  ("L'eau du robinet stockée en bouteille convient-elle ?", "Les bouteilles scellées du commerce sont recommandées : elles se conservent mieux et leur date limite est indiquée."),
 ],
 related=["aliments-sans-cuisson-kit-urgence","frigo-congelateur-coupure-electricite","kit-de-survie-72h"],
)

# ---------------------------------------------------------------- 3. Aliments sans cuisson
page(
 slug="aliments-sans-cuisson-kit-urgence",
 emoji="🥫",
 title="Aliments sans cuisson pour le kit d'urgence : la liste",
 desc="Que manger pendant 3 jours sans électricité ni gaz ? Liste d'aliments sans cuisson ni frigo pour le kit 72h, conseils de stockage et pièges à éviter.",
 h1="Aliments sans cuisson pour le kit d'urgence : la liste",
 lead="Le guide « Tous responsables » demande de la nourriture non périssable et qui ne nécessite pas de cuisson : en cas de coupure, ni plaque, ni four, ni micro-ondes, ni frigo. Voici une liste concrète d'aliments qui se mangent tels quels et se gardent des mois.",
 source="guide « Tous responsables » (SGDSN, 2025)",
 nav_label="Aliments sans cuisson", nav_emoji="🥫",
 sections=[
  ("liste","La liste des aliments qui se mangent tels quels", """
<div class="cards"><div class="card"><h3><span class="ic" aria-hidden="true">🐟</span>Protéines</h3><ul><li>Thon, sardines, maquereaux en conserve</li><li>Pois chiches, haricots, lentilles en conserve (déjà cuits)</li><li>Plats cuisinés en conserve qui se mangent froids</li><li>Beurre de cacahuète, amandes, noix</li></ul></div>
<div class="card"><h3><span class="ic" aria-hidden="true">🍞</span>Féculents</h3><ul><li>Crackers, biscottes, pain suédois</li><li>Biscuits secs, barres de céréales</li><li>Céréales du petit-déjeuner</li></ul></div>
<div class="card"><h3><span class="ic" aria-hidden="true">🍑</span>Fruits et légumes</h3><ul><li>Compotes en gourde ou en pot</li><li>Fruits au sirop, macédoine en conserve</li><li>Fruits secs : abricots, raisins, dattes</li></ul></div>
<div class="card"><h3><span class="ic" aria-hidden="true">🥛</span>Le reste</h3><ul><li>Lait UHT en petites briques</li><li>Petits pots pour bébé si besoin</li><li>Chocolat, sucre : de l'énergie rapide</li><li>Nourriture pour les animaux</li></ul></div></div>"""),
  ("regles","Les règles pour bien choisir", """
<ul class="check"><li><strong>Petits formats</strong> : une boîte entamée ne se garde pas sans frigo. Mieux vaut des portions qui se finissent en un repas.</li>
<li><strong>Ouvre-boîte manuel</strong> : indispensable, ou des boîtes à ouverture facile. Le guide le cite dans le kit.</li>
<li><strong>Ce que vous aimez</strong> : en situation de stress, on mange mieux des aliments familiers. Évitez les achats « spécial survie » que personne ne touchera.</li>
<li><strong>Allergies et régimes</strong> : adaptez la liste à chaque membre du foyer.</li>
<li><strong>Sel</strong> : les conserves salées donnent soif. Elles comptent dans le calcul de votre <a href="combien-eau-stocker-par-personne.html">réserve d'eau</a>.</li></ul>"""),
  ("stock","Faire tourner le stock", """
<p>Le plus simple est de piocher dans le kit au quotidien et de racheter aussitôt : les produits restent frais et rien n'est gaspillé. Le guide demande de vérifier les dates de péremption au moins deux fois par an. L'<a href="./">appli Tous prêts</a> garde la liste et la date de votre dernière vérification.</p>"""),
 ],
 faq=[
  ("Que manger pendant une coupure d'électricité ?", "Des aliments qui se mangent sans cuisson ni frigo : conserves de poisson ou de légumineuses, crackers, compotes, fruits secs, barres de céréales, lait UHT."),
  ("Combien de nourriture prévoir pour 72 heures ?", "Le guide ne donne pas de quantité : prévoyez trois jours de repas habituels pour chaque personne, en petites portions."),
  ("Faut-il acheter des rations de survie ?", "Non, des aliments du supermarché suffisent. Choisissez ce que votre famille mange déjà."),
 ],
 related=["combien-eau-stocker-par-personne","frigo-congelateur-coupure-electricite","kit-de-survie-72h-pas-cher"],
)

# ---------------------------------------------------------------- 4. Recharger son téléphone
page(
 slug="recharger-telephone-coupure-courant",
 emoji="🔋",
 title="Recharger son téléphone pendant une coupure de courant",
 desc="Batterie externe, voiture, manivelle, solaire : comment garder un téléphone chargé pendant une coupure longue, et comment économiser la batterie.",
 h1="Comment recharger son téléphone pendant une coupure de courant ?",
 lead="Le guide « Tous responsables » met un chargeur de téléphone dans le kit d'urgence. Mais sans électricité, encore faut-il une source d'énergie. Voici les solutions, de la plus simple à la plus autonome, et les réglages qui font durer la batterie.",
 source="guide « Tous responsables » (SGDSN, 2025)",
 nav_label="Recharger son téléphone", nav_emoji="🔋",
 sections=[
  ("solutions","Les solutions pour recharger", """
<div class="cards"><div class="card"><h3><span class="ic" aria-hidden="true">🔋</span>Batterie externe</h3><ul><li>La solution la plus simple : rechargez-la tous les 3 mois</li><li>10 000 mAh donnent en général 2 recharges d'un smartphone</li></ul></div>
<div class="card"><h3><span class="ic" aria-hidden="true">🚗</span>La voiture</h3><ul><li>Un câble pour la prise USB ou allume-cigare</li><li><strong>Jamais moteur allumé dans un garage fermé</strong> : risque d'intoxication au monoxyde de carbone</li></ul></div>
<div class="card"><h3><span class="ic" aria-hidden="true">☀️</span>Manivelle et solaire</h3><ul><li>Certaines radios à manivelle rechargent aussi un téléphone, lentement</li><li>Un petit panneau solaire fonctionne bien en journée, mal par temps couvert</li></ul></div></div>
<p class="note">Un groupe électrogène s'utilise toujours dehors, loin des fenêtres : il produit du monoxyde de carbone, un gaz mortel et sans odeur.</p>"""),
  ("economiser","Faire durer la batterie", """
<ul class="check"><li>Activez le <strong>mode économie d'énergie</strong> et baissez la luminosité.</li>
<li>Désactivez le Wi-Fi, le Bluetooth et la localisation si vous ne vous en servez pas.</li>
<li>Préférez les <strong>SMS aux appels</strong> : ils consomment moins et passent mieux quand le réseau est saturé. Gardez les appels pour les urgences (112).</li>
<li>Ne gardez pas le téléphone allumé pour suivre l'actualité : une <a href="radio-a-piles-kit-urgence.html">radio à piles</a> le fait sans vider la batterie.</li>
<li>Notez sur papier les numéros importants : si le téléphone s'éteint, vous les aurez encore.</li></ul>"""),
  ("alerte","Rester joignable par les autorités", """
<p>Le dispositif <strong>FR-Alert</strong> envoie des messages d'alerte sur les téléphones présents dans la zone concernée. Un téléphone chargé et allumé de temps en temps permet de les recevoir. Les consignes officielles passent aussi par la radio locale du service public.</p>"""),
 ],
 faq=[
  ("Comment charger son téléphone sans électricité ?", "Avec une batterie externe chargée à l'avance, la prise USB d'une voiture à l'extérieur, une radio à manivelle ou un petit panneau solaire."),
  ("Peut-on recharger son téléphone dans la voiture pendant une coupure ?", "Oui, mais jamais moteur allumé dans un garage fermé, à cause du monoxyde de carbone."),
  ("Pourquoi envoyer des SMS plutôt qu'appeler ?", "Les SMS consomment moins de batterie et passent mieux quand le réseau est saturé."),
 ],
 related=["coupure-electricite-que-faire","radio-a-piles-kit-urgence","frigo-congelateur-coupure-electricite"],
)

# ---------------------------------------------------------------- 5. Bébé
page(
 slug="kit-urgence-bebe",
 emoji="👶",
 title="Kit d'urgence bébé : la liste pour 72h",
 desc="Couches, lait infantile, eau pour les biberons, petits pots, carnet de santé : ce qu'il faut ajouter au kit d'urgence 72h quand on a un bébé.",
 h1="Kit d'urgence bébé : quoi prévoir pour 72 heures ?",
 lead="Le guide « Tous responsables » rappelle d'adapter le kit à chaque membre du foyer et y cite les petits pots pour bébé. Un nourrisson ne peut pas attendre : voici ce qu'il faut ajouter au kit familial pour tenir trois jours sans eau courante ni électricité.",
 source="guide « Tous responsables » (SGDSN, 2025), Croix-Rouge, autorités sanitaires",
 nav_label="Kit bébé", nav_emoji="👶",
 sections=[
  ("liste","La liste pour bébé", """
<div class="cards"><div class="card"><h3><span class="ic" aria-hidden="true">🍼</span>Repas</h3><ul><li>Lait infantile habituel pour au moins 3 jours</li><li>Si possible du <strong>lait prêt à l'emploi</strong> : il ne demande pas d'eau</li><li>Eau en bouteille <strong>marquée « convient à la préparation des aliments des nourrissons »</strong>, réservée aux biberons</li><li>Biberons et tétines propres, petits pots, cuillère</li></ul></div>
<div class="card"><h3><span class="ic" aria-hidden="true">🧷</span>Change et hygiène</h3><ul><li>Couches adaptées à la taille du bébé pour au moins 3 jours.</li><li>Lingettes, crème pour le change, sacs pour les couches sales</li><li>Gel hydroalcoolique pour les mains</li></ul></div>
<div class="card"><h3><span class="ic" aria-hidden="true">🩺</span>Santé et papiers</h3><ul><li>Médicaments habituels et thermomètre</li><li>Copie du carnet de santé et des ordonnances</li><li>Vêtements de rechange, couverture, doudou</li></ul></div></div>"""),
  ("eau","L'eau des biberons", """
<p>Si l'eau du robinet n'est plus potable, par exemple après une inondation, préparez les biberons <strong>uniquement avec une eau en bouteille adaptée aux nourrissons</strong> (mention « convient à la préparation des aliments des nourrissons » sur l'étiquette), jusqu'à ce que les autorités annoncent que l'eau du robinet est de nouveau potable. Respectez exactement les doses de la boîte. Préparez chaque biberon juste avant de le donner et jetez ce qui reste : sans frigo, un biberon ne se garde pas. Même règle pour le lait prêt à l'emploi entamé : suivez l'étiquette. Ajoutez cette eau à la <a href="combien-eau-stocker-par-personne.html">réserve de 6 litres par personne</a>.</p>
<p>Si vous allaitez, poursuivez si possible : l'allaitement ne dépend ni de l'eau ni de l'électricité. Si votre bébé prend du lait infantile, prévoyez son lait habituel en quantité suffisante. Le lait infantile en poudre n'est pas stérile : lavez-vous soigneusement les mains, nettoyez et désinfectez le matériel, et reconstituez chaque biberon immédiatement avant la tétée. Le lait liquide prêt à l'emploi est précieux en cas de coupure d'eau. En cas de difficulté, demandez conseil à un professionnel de santé.</p>"""),
  ("verifier","Vérifier plus souvent", """
<p>Un bébé grandit vite : la taille des couches, la quantité de lait et le type de repas changent tous les quelques mois. Vérifiez le kit bébé <strong>chaque mois</strong> plutôt que deux fois par an comme le reste du kit. L'<a href="./">appli Tous prêts</a> adapte la liste quand vous ajoutez un bébé au foyer.</p>
<p class="note">En cas de fièvre, de refus de boire, de signes de déshydratation ou de doute sur la santé de votre bébé, appelez le 15 (Samu) ou le 112.</p>"""),
 ],
 faq=[
  ("Que mettre dans un kit d'urgence pour bébé ?", "Lait infantile et eau en bouteille pour 3 jours, biberons, petits pots, couches, lingettes, médicaments, thermomètre, copie du carnet de santé, vêtements chauds."),
  ("Avec quelle eau préparer les biberons en cas de crise ?", "Avec une eau en bouteille portant la mention « convient à la préparation des aliments des nourrissons », tant que les autorités n'ont pas confirmé que l'eau du robinet est potable."),
  ("Tous les combien vérifier le kit bébé ?", "Chaque mois, car les besoins d'un bébé changent vite."),
 ],
 related=["kit-urgence-72h-famille-appartement-voiture","combien-eau-stocker-par-personne","kit-urgence-animaux"],
)

# ---------------------------------------------------------------- 6. Animaux
page(
 slug="kit-urgence-animaux",
 emoji="🐾",
 title="Kit d'urgence pour chien et chat : la liste",
 desc="Nourriture, eau, médicaments, carnet de santé, identification, caisse de transport : le kit d'urgence de votre chien ou chat et le plan en cas d'évacuation.",
 h1="Kit d'urgence pour animaux : chien, chat, que prévoir ?",
 lead="Le guide « Tous responsables » inclut la nourriture pour animaux dans le kit d'urgence. Un animal dépend entièrement de vous pendant une crise. Voici sa liste pour 72 heures et ce qu'il faut prévoir si vous devez quitter votre logement.",
 source="guide « Tous responsables » (SGDSN, 2025), autorités canadiennes de protection civile",
 nav_label="Kit animaux", nav_emoji="🐾",
 sections=[
  ("liste","La liste pour votre animal", """
<div class="cards"><div class="card"><h3><span class="ic" aria-hidden="true">🥣</span>Nourriture et eau</h3><ul><li>Sa nourriture habituelle pour au moins 3 jours, conservée dans un contenant hermétique et à l'abri de l'humidité.</li><li>De l'eau en plus de celle du foyer, et une gamelle</li><li>Ouvre-boîte si sa nourriture est en conserve</li></ul></div>
<div class="card"><h3><span class="ic" aria-hidden="true">💊</span>Santé</h3><ul><li>Ses médicaments et leur ordonnance</li><li>Copie du carnet de santé et des vaccins</li><li>Coordonnées du vétérinaire</li></ul></div>
<div class="card"><h3><span class="ic" aria-hidden="true">🦮</span>Transport</h3><ul><li>Laisse, collier ou harnais</li><li>Caisse ou sac de transport</li><li>Litière et sacs pour les déjections</li><li>Une couverture ou un jouet familier pour le calmer</li></ul></div></div>"""),
  ("identification","L'identification, votre meilleure assurance", """
<ul class="check"><li>Vérifiez que votre animal est identifié (puce électronique ou tatouage) et que vos coordonnées sont à jour dans le fichier national d\'identification.</li>
<li>Gardez une <strong>photo récente de vous avec votre animal</strong> : elle prouve qu'il est à vous si vous êtes séparés.</li>
<li>Une médaille avec votre numéro de téléphone sur le collier aide à le retrouver vite.</li></ul>"""),
  ("evacuation","Si vous devez évacuer", """
<p>N'attendez pas la dernière minute pour savoir où aller avec votre animal. Beaucoup de lieux d'hébergement d'urgence n'acceptent que les animaux d'assistance. Préparez à l'avance une liste : proches, amis, pensions, hôtels qui acceptent les animaux, à l'intérieur et à l'extérieur de votre commune. Renseignez-vous auprès de votre mairie sur ce que prévoit son plan communal de sauvegarde.</p>
<p>Ne laissez pas votre animal attaché ou enfermé seul dans un logement menacé. Si les autorités vous imposent de partir sans lui, laissez-lui de l'eau et de la nourriture et signalez-le aux secours.</p>"""),
 ],
 faq=[
  ("Que mettre dans un kit d'urgence pour chien ou chat ?", "Sa nourriture et de l'eau pour 3 jours, ses médicaments, une copie de son carnet de santé, une laisse, une caisse de transport, de la litière et une photo de vous avec lui."),
  ("Les centres d'hébergement d'urgence acceptent-ils les animaux ?", "Pas toujours. Préparez à l'avance une liste de proches ou de lieux qui peuvent accueillir votre animal."),
  ("Pourquoi faire identifier son animal ?", "Une puce ou un tatouage à jour permet de le retrouver si vous êtes séparés pendant une crise."),
 ],
 related=["kit-urgence-bebe","kit-urgence-72h-famille-appartement-voiture","combien-eau-stocker-par-personne"],
)

# =============================================================== rendu
TITLES = {}  # slug -> titre court pour les liens connexes
for f in __import__("glob").glob(f"{SITE}/*.html"):
    s = open(f, encoding="utf-8").read()
    m = re.search(r"<h1>(.*?)</h1>", s)
    if m: TITLES[f.split("/")[-1][:-5]] = re.sub("<[^>]+>", "", m.group(1))
for p in PAGES: TITLES[p["slug"]] = p["h1"]

head_end = TPL.index("<script type=\"application/ld+json\">")
nav_start = TPL.index("<div class=\"layout\">")
main_start = TPL.index("<main id=\"contenu\">")
foot_start = TPL.index("<footer")

def ld(p):
    url = f"https://tousprets.fr/{p['slug']}.html"
    g = [
      {"@type": "Article", "headline": p["h1"], "description": p["desc"], "inLanguage": "fr-FR",
       "author": {"@type": "Organization", "name": "Tous prêts", "url": "https://tousprets.fr/"},
       "publisher": {"@type": "Organization", "name": "Tous prêts", "logo": {"@type": "ImageObject", "url": "https://tousprets.fr/icon-512.png"}},
       "datePublished": DATE, "dateModified": DATE, "mainEntityOfPage": url, "image": "https://tousprets.fr/og-image.png"},
      {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Tous prêts", "item": "https://tousprets.fr/"},
        {"@type": "ListItem", "position": 2, "name": p["h1"], "item": url}]},
      {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in p["faq"]]},
    ]
    return '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@graph": g}, ensure_ascii=False) + "</script>\n"

def build(p):
    url = f"https://tousprets.fr/{p['slug']}.html"
    head = TPL[:head_end]
    old_title = re.search(r"<title>(.*?)</title>", head).group(1)
    old_desc = re.search(r'name="description" content="(.*?)"', head).group(1)
    head = head.replace(old_title, html.escape(p["title"], quote=False)).replace(old_desc, html.escape(p["desc"]))
    head = head.replace("https://tousprets.fr/radio-a-piles-kit-urgence.html", url)
    head = head.replace("kit d'urgence 72h, radio à piles", "kit d'urgence 72h, " + p["nav_label"].lower())
    rest_head = TPL[TPL.index("</script>", head_end) + len("</script>\n"):nav_start]  # goatcounter + body start
    nav = TPL[nav_start:main_start].replace(' aria-current="page"', "")
    toc = "".join(f'<li><a href="#{sid}">{t}</a></li>' for sid, t, _ in p["sections"]) + '<li><a href="#faq">Questions fréquentes</a></li>'
    secs = "".join(f'<section id="{sid}" aria-labelledby="{sid}-t"><h2 id="{sid}-t">{t}</h2>{body.strip()}</section>' for sid, t, body in p["sections"])
    faq = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in p["faq"])
    rel = "".join(f'<li><a href="{r}.html">{TITLES.get(r, r)}</a></li>' for r in p["related"]) + '<li><a href="./">Checklist du kit d\'urgence 72h (appli gratuite)</a></li>'
    main = (f'<main id="contenu"><div class="hero"><div class="wrap">\n'
            f'<div class="crumbs"><a href="./">Tous prêts</a> › {p["h1"]}</div>\n'
            f'<span class="emoji" aria-hidden="true">{p["emoji"]}</span>\n<h1>{p["h1"]}</h1>\n'
            f'<p class="lead">{p["lead"]}</p>\n'
            f'<div class="meta"><span>Mis à jour le {DATE_FR}</span><span>Sources : {p["source"]}</span></div>\n</div></div>\n<div class="wrap">\n'
            f'<nav class="toc" aria-label="Sommaire"><strong>Sommaire</strong><ol>{toc}</ol></nav>\n{secs}\n'
            f'<section id="faq" class="faq" aria-labelledby="faq-t"><h2 id="faq-t">Questions fréquentes</h2>{faq}</section>\n'
            f'<section id="voir-aussi" aria-labelledby="voir-aussi-t"><h2 id="voir-aussi-t">À lire aussi</h2><ul>{rel}</ul></section>\n'
            f'<div class="cta-box noprint"><p>Cochez votre liste, adaptez-la à votre foyer, même hors ligne.</p><a class="btn" href="./">Préparer mon kit dans l\'appli gratuite</a></div>\n</div></main>')
    return head + ld(p) + rest_head + nav + main + "</div>\n" + TPL[foot_start:]

for p in PAGES:
    open(f"{SITE}/{p['slug']}.html", "w", encoding="utf-8").write(build(p))
    print("écrit", p["slug"], len(p["title"]), len(p["desc"]))

json.dump([{k: p[k] for k in ("slug", "nav_label", "nav_emoji")} for p in PAGES], open("/home/claude/seo/pages.json", "w"), ensure_ascii=False)
