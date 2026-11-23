# -*- coding: utf-8 -*-
"""Page Questions / réponses pratiques : sujets absents du site (communication sans réseau, toilettes, rangement...)."""
import importlib.util, json, re
spec = importlib.util.spec_from_file_location("np", "/home/claude/seo/newpages.py")
np = importlib.util.module_from_spec(spec); spec.loader.exec_module(np)  # régénère aussi les 6 pages (identiques)

def qa(groups):
    out = []
    for gid, gtitle, items in groups:
        body = "".join(f'<details><summary>{q}</summary>{a}</details>' for q, a in items)
        out.append((gid, gtitle, f'<div class="faq">{body}</div>'))
    return out

IMG_TITLES = {}
def fig(name, alt):
    alt = alt.replace(" tousprets.fr", "").rstrip(" .") + "."
    title = {"toilettes-seches-seau":"Toilettes sèches avec un seau","chauffe-eau-reserve-eau":"Le chauffe-eau, une réserve d'eau",
             "communiquer-sans-reseau":"Communiquer sans réseau","rangement-petit-appartement":"Ranger son kit d'urgence sans cave",
             "objets-oublies-kit-urgence":"8 objets qu'on oublie dans le kit d'urgence"}[name]
    IMG_TITLES[name] = (title, alt)
    return (f'<figure class="visuel" id="visuel-{name}"><picture><source srcset="img/qr/{name}.webp" type="image/webp" width="1080" height="1350">'
            f'<img src="img/qr/{name}.png" width="1080" height="1350" loading="lazy" decoding="async" alt="{alt}" title="Infographie : {title}"></picture>'
            f'<figcaption>Infographie « {title} » — Tous prêts, <a href="https://creativecommons.org/licenses/by/4.0/deed.fr" rel="license">licence CC BY 4.0</a> : '
            f'réutilisation libre en citant tousprets.fr. <a href="img/qr/{name}.png" download>Télécharger en haute définition (2160 × 2700)</a> · '
            f'<a href="licence-visuels.html">Conditions</a></figcaption></figure>')

GROUPS = [
 ("reseau", "Plus de réseau, plus d'internet", [
  ("Mon téléphone ne capte plus : comment être prévenu des consignes ?",
   "<p><strong>Par la radio.</strong> Une radio à piles ou à manivelle capte la radio locale du service public (« ici », ex-France Bleu), qui relaie les consignes des autorités. Les sirènes et les messages par haut-parleur de la mairie restent aussi actifs. FR-Alert, lui, a besoin du réseau mobile. Voir <a href=\"radio-a-piles-kit-urgence.html\">la radio à piles</a>.</p>"),
  ("Mon opérateur ne capte plus : puis-je quand même appeler le 112 ?",
   "<p>En France, les numéros directs restent le <strong>15</strong> (Samu), le <strong>17</strong> (police) et le <strong>18</strong> (pompiers) ; le <strong>112</strong> fonctionne partout en Europe. <strong>Oui, l'appel passe si un autre opérateur capte.</strong> Le téléphone emprunte automatiquement le réseau disponible pour un appel d'urgence, même sans forfait. <strong>Attention :</strong> en France, il faut une carte SIM dans le téléphone. Un vieux téléphone sans SIM ne joint pas le 112. S'il n'y a aucun réseau du tout, l'appel ne passe pas.</p>" + fig("communiquer-sans-reseau", "Communiquer quand tout coupe : radio à piles, 112 sur un autre réseau, carte SIM obligatoire, talkies PMR446, SOS par satellite, point de rendez-vous. tousprets.fr")),
  ("Sans réseau mobile : talkies-walkies ou satellite, est-ce utile ?",
   "<p>Les talkies <strong>PMR446</strong> s'utilisent <strong>sans licence ni abonnement</strong> en France et en Europe, avec une puissance limitée à 0,5 W. Ils permettent de garder le contact dans un immeuble, une rue ou un quartier quand le réseau mobile tombe.</p><p><strong>Portée réelle :</strong> les boîtes annoncent 5 à 10 km, mais en ville comptez plutôt quelques centaines de mètres à 1 km. Prévoyez des piles de rechange (l'autonomie baisse au froid) et convenez à l'avance d'un canal. Ce sont des canaux ouverts : n'y donnez pas d'informations sensibles (absence du logement, codes). Ils ne permettent pas de joindre les secours.</p>" + "<p>Oui avec certains téléphones : depuis décembre 2022, les <strong>iPhone 14 et plus récents</strong> peuvent envoyer un message aux secours par satellite en France, et certains Pixel récents proposent le SOS par satellite selon le modèle et le pays : vérifiez dans les réglages de votre téléphone. C'est un dernier recours : composez d'abord le 112, et si l'appel ne passe pas, le téléphone propose le satellite. Il faut être dehors, ciel dégagé. Testez la démonstration dans les réglages.</p>"),
  ("Comment se retrouver en famille sans téléphone ?",
   "<p>Décidez <strong>maintenant</strong> d'un lieu de rassemblement près de chez vous et d'un second hors du quartier, et d'une personne contact qui centralise les nouvelles. Écrivez les numéros importants sur papier, dans le kit et dans chaque sac. Le guide « Tous responsables » demande de prévoir ces lieux et ces numéros dans son plan personnel.</p>"),
 ]),
 ("hygiene", "Eau et hygiène", [
  ("L'eau est coupée : comment faire avec les toilettes (toilettes sèches avec un seau) ?",
   "<p><strong>Si les égouts fonctionnent</strong> (seule l'eau du robinet est coupée) : versez d'un coup un seau d'eau non potable (pluie, eau de bain) au fond de la cuvette pour déclencher la chasse, en restant près de la cuvette pour limiter les éclaboussures. Ne touchez pas à votre réserve d'eau potable.</p><p><strong>Si les égouts sont hors service</strong> (inondation, consigne de la mairie) : n'utilisez plus les toilettes et passez aux toilettes sèches avec un seau, ci-dessous.</p>" + "<ol class=\"steps-list\"><li><strong>Un seau solide de 15 à 20 litres</strong>, avec couvercle, installé dans une pièce aérée (salle de bain, balcon couvert).</li><li><strong>Deux sacs poubelle épais</strong> glissés l'un dans l'autre, rabattus sur le bord du seau.</li><li><strong>Une assise</strong> : une frite de piscine fendue dans la longueur, posée sur le bord et fixée avec du ruban adhésif pour qu'elle ne glisse pas, ou un vieil abattant. Le seau doit être bien stable.</li><li><strong>Une couche de matière sèche au fond</strong>, puis 1 à 2 poignées après chaque passage : sciure de bois non traité, litière végétale, copeaux ou terre sèche. Elle absorbe et limite les odeurs.</li><li><strong>Séparer l'urine</strong> si possible (bouteille, second seau) : beaucoup moins d'odeur et un sac moins lourd.</li><li><strong>Changer le sac à moitié plein</strong> : le nouer, le mettre dans un contenant fermé, au frais et à l'écart du logement, des points d'eau et des potagers. Ne le jetez pas avec les ordures ménagères sans consigne : suivez celles de la mairie.</li><li><strong>Hygiène</strong> : gel hydroalcoolique à chaque passage, couvercle fermé entre deux utilisations. Le gel ne remplace pas le savon sur des mains sales : lavez-les à l'eau et au savon dès que possible.</li></ol><p>À avoir dans le kit : un seau à couvercle, des sacs poubelle épais et des liens, un sac de litière végétale ou de sciure, du papier toilette, du gel hydroalcoolique.</p>" + fig("toilettes-seches-seau", "Toilettes sèches avec un seau en 6 étapes : seau de 15 à 20 litres, deux sacs poubelle, frite de piscine en assise, sciure après chaque passage, changer le sac à moitié plein, séparer l'urine. tousprets.fr")),
  ("Le chauffe-eau peut-il servir de réserve d'eau ?",
   "<p><strong>Oui.</strong> Un chauffe-eau (ballon, cumulus) contient souvent 100 à 300 litres d'eau du réseau. Si l'eau du robinet est coupée, cette eau reste disponible. Encore faut-il savoir la récupérer : <strong>repérez dès aujourd'hui l'arrivée d'eau froide et l'endroit où se fait la vidange</strong>. Sur beaucoup de chauffe-eau, elle passe par le groupe de sécurité, souvent relié à l'évacuation : il faut pouvoir glisser un récipient dessous.</p><ol class=\"steps-list\"><li><strong>Coupez l'alimentation</strong> : le disjoncteur du chauffe-eau (ou le gaz). Un chauffe-eau qui chauffe à vide s'abîme.</li><li><strong>Fermez la vanne d'arrivée d'eau froide</strong> du ballon.</li><li><strong>Ouvrez un robinet d'eau chaude</strong> dans le logement : l'air entre et l'eau peut sortir.</li><li><strong>Laissez refroidir</strong> plusieurs heures si possible : l'eau peut être brûlante.</li><li><strong>Vidangez dans un récipient</strong> par le groupe de sécurité (position vidange) ou par le robinet en bas du ballon, selon le modèle, en vérifiant d'abord qu'un récipient tient dessous. Refermez ensuite.</li></ol><p><strong>Peut-on la boire ?</strong> C'est l'eau du réseau, mais elle peut contenir du calcaire et des dépôts. Utilisez-la d'abord pour l'hygiène et la cuisine ; ne la buvez qu'en dernier recours, après l'avoir laissée reposer et fait bouillir. L'ébullition tue les microbes mais n'enlève pas une pollution chimique. <strong>Jamais pour les biberons</strong> : utilisez une eau en bouteille adaptée aux nourrissons.</p><p><strong>Si les autorités annoncent que l'eau du robinet est polluée</strong>, fermez tout de suite la vanne d'arrivée générale du logement : l'eau propre du ballon ne sera pas remplacée par de l'eau polluée.</p><p>Gardez la notice de votre chauffe-eau, et faites-vous montrer les vannes par un plombier lors d'un entretien si vous avez un doute.</p>" + fig("chauffe-eau-reserve-eau", "Votre chauffe-eau est une réserve d'eau de 100 à 300 litres : couper le courant, fermer l'arrivée d'eau froide, ouvrir un robinet d'eau chaude, vidanger dans un récipient, laisser refroidir. tousprets.fr")),
  ("Comment se laver sans eau courante ?",
   "<p>Lingettes, gel hydroalcoolique pour les mains, et un gant avec un peu d'eau pour le reste. La réserve de 6 litres par personne sert à boire : prévoyez de l'eau en plus pour l'hygiène si vous avez la place. Voir <a href=\"combien-eau-stocker-par-personne.html\">combien d'eau stocker</a>.</p>"),
  ("Filtre à eau ou pastilles : faut-il en avoir ?",
   "<p>La priorité, ce sont les <strong>bouteilles d'eau</strong>. Le guide officiel prévoit les pastilles de décontamination <strong>en dernier recours</strong>, en suivant strictement leur notice. Un filtre de randonnée arrête une partie des microbes mais pas les produits chimiques : après une inondation, l'eau peut être polluée par des hydrocarbures ou des produits ménagers. Suivez les consignes de la mairie avant de boire l'eau du robinet ou une eau filtrée.</p>"),
 ]),
 ("rangement", "Rangement et achats", [
  ("Je vis dans un petit appartement : où ranger le kit ?",
   "<ul class=\"check\"><li><strong>Le sac d'évacuation</strong> près de l'entrée ou dans le placard le plus proche de la porte.</li><li><strong>L'eau</strong> au sol, à l'abri de la lumière : sous le lit, au fond d'un placard. C'est lourd, ne la mettez pas en hauteur.</li><li><strong>Les conserves</strong> sous le lit, dans un bac.</li><li><strong>Le léger</strong> (couverture de survie, piles, lampe, papiers) en hauteur ou dans un range-chaussures à suspendre derrière une porte.</li><li>Évitez la cave si votre logement est en zone inondable, et les endroits chauds (près du four, du radiateur).</li></ul><p>Voir aussi <a href=\"kit-urgence-72h-famille-appartement-voiture.html\">le kit selon votre logement</a>.</p>" + fig("rangement-petit-appartement", "Ranger son kit dans un petit appartement : sac d'évacuation près de l'entrée, eau au sol, réserves sous le lit, objets légers en hauteur, derrière les portes, éviter la cave inondable. tousprets.fr")),
  ("Quels petits objets pas chers oublie-t-on souvent ?",
   "<ul class=\"check\"><li><strong>Un sifflet</strong> : pour signaler sa présence sans s'épuiser à crier.</li><li><strong>Du ruban adhésif solide</strong> : réparer, colmater, étiqueter.</li><li><strong>Des sacs poubelle épais</strong> : toilettes de secours, imperméable, protection des papiers.</li><li><strong>Une couverture de survie</strong> (citée par le guide officiel).</li><li><strong>Des gants de travail</strong> et un poncho de pluie.</li><li><strong>Du gel hydroalcoolique</strong>.</li><li><strong>Un couteau multifonction et un ouvre-boîte</strong> (cités par le guide).</li><li><strong>Des piles</strong> au bon format pour la lampe et la radio.</li></ul><p>La plupart se trouvent pour quelques euros en grande surface. Voir <a href=\"kit-de-survie-72h-pas-cher.html\">le kit pas cher</a>.</p>" + fig("objets-oublies-kit-urgence", "Les objets pas chers qu'on oublie : sifflet, ruban adhésif, sacs poubelle épais, couverture de survie, gants, gel hydroalcoolique, couteau et ouvre-boîte, piles. tousprets.fr")),
  ("Faut-il prévoir plus de 72 heures ?",
   "<p>Le guide français demande <strong>72 heures</strong>, la durée pendant laquelle les secours peuvent être débordés. D'autres pays visent plus long : la Suède, la Norvège ou l'Estonie demandent environ une semaine. Commencez par 72 heures bien faites, puis élargissez petit à petit en achetant un peu plus de ce que vous mangez déjà.</p>"),
  ("Quels aliments sont impérissables ?",
   "<p>Peu d'aliments sont vraiment impérissables. S'ils restent <strong>fermés, au sec, au frais et à l'abri de la lumière et des insectes</strong>, ceux-ci se gardent des années :</p><ul class=\"check\"><li><strong>Quasi illimité</strong> : sel, sucre blanc, miel (il peut cristalliser : c'est normal, il suffit de le tiédir au bain-marie), vinaigre blanc.</li><li><strong>Plusieurs années</strong> : riz blanc, pâtes sèches, légumes secs (lentilles, pois chiches : plus ils sont vieux, plus ils sont longs à cuire), café soluble, thé, cacao en poudre.</li><li><strong>Conserves en boîte métallique</strong> : souvent consommables bien après la date si la boîte est intacte.</li></ul><p><strong>La règle des dates</strong> : « À consommer <em>de préférence</em> avant » (DDM) signale une possible perte de goût ou de texture, pas un danger. On peut manger le produit après cette date. « À consommer <em>jusqu'au</em> » (DLC) est une limite à respecter. Jetez sans goûter toute boîte bombée, rouillée, cabossée ou qui fuit.</p><p><strong>Pour le kit 72 h</strong>, privilégiez ce qui se mange <strong>sans cuisson</strong> : riz, pâtes et légumes secs demandent de l'eau et du feu. Voir <a href=\"aliments-sans-cuisson-kit-urgence.html\">les aliments sans cuisson</a>. Faites tourner votre stock : consommez le plus ancien, remplacez-le, et vérifiez le tout deux fois par an.</p>"),
  ("Quels papiers mettre dans le kit d'urgence ?",
   "<p>Des <strong>photocopies</strong>, dans une pochette étanche : pièces d'identité, livret de famille, carte Vitale, ordonnances, contrat d'assurance habitation, coordonnées bancaires et liste des numéros utiles. Gardez aussi une <strong>copie numérique</strong> dans un espace sécurisé en ligne, et quelques photos de votre logement et de vos biens : elles aident pour la déclaration de sinistre à l'assurance.</p>"),
  ("Le gouvernement distribue-t-il un kit d'urgence ? Combien coûte-t-il ?",
   "<p>Le gouvernement <strong>ne distribue pas de kit</strong> : le guide « Tous responsables » (gratuit) donne une liste à rassembler soi-même. Méfiez-vous des offres payantes présentées comme « kit officiel ». Le coût dépend de ce que vous avez déjà : lampe, couteau, couverture, trousse de secours sont souvent à la maison. Il reste surtout l'eau, quelques conserves, une radio et des piles. Voir <a href=\"kit-de-survie-72h-pas-cher.html\">le kit 72h pas cher</a>.</p>"),
  ("Pourquoi le gouvernement demande-t-il de tenir 72 heures ?",
   "<p>Parce que lors d'une crise majeure (inondation, tempête, panne géante, cyberattaque), les secours ne peuvent pas être partout à la fois : ils vont d'abord aux personnes en danger. Les premiers jours, chaque foyer doit pouvoir boire, manger, avoir chaud et se soigner seul. Voir <a href=\"kit-urgence-72h-gouvernement.html\">ce que dit le guide</a>.</p>"),
  ("Et si le paiement par carte ne fonctionne plus ?",
   "<p>Sans électricité ou sans réseau, les terminaux de paiement et les distributeurs peuvent s'arrêter. Le guide prévoit de l'<strong>argent liquide</strong> dans le kit : gardez de petites coupures et de la monnaie, assez pour quelques jours de courses essentielles.</p>"),
 ]),
 ("securite", "Sécurité et santé pendant la crise", [
  ("L'alerte sonne : faut-il se confiner ou évacuer ?",
   "<p><strong>Par défaut, mettez-vous à l'abri</strong> : rentrez dans le bâtiment le plus proche, fermez portes et fenêtres, arrêtez ventilation et climatisation, et écoutez la radio. <strong>N'évacuez que sur ordre des autorités</strong> (ou si l'eau monte et vous y force). Ne téléphonez pas sauf urgence vitale, pour laisser les lignes aux secours.</p><p><strong>Si l'ordre d'évacuer est donné</strong> : prenez votre <a href=\"sac-de-secours.html\">sac de secours</a>, vos papiers et vos médicaments, coupez le gaz et l'électricité si on vous le demande, fermez à clé et suivez l'itinéraire indiqué. Voir aussi <a href=\"confinement-que-faire.html\">que faire en cas de confinement</a>.</p>"),
  ("Faut-il aller chercher ses enfants à l'école pendant une alerte ?",
   "<p><strong>Non.</strong> L'école a un plan de mise en sûreté (PPMS) et les enseignants protègent les élèves. En vous déplaçant, vous vous exposez au danger et vous encombrez les routes des secours. Restez à l'abri, écoutez la radio et attendez la fin de l'alerte ou les consignes de l'école.</p>"),
  ("Coupure de courant en hiver : comment se chauffer sans danger ?",
   "<p><strong>Danger n°1 : le monoxyde de carbone</strong>, un gaz invisible et sans odeur qui tue chaque hiver.</p><ul class=\"check\"><li><strong>Jamais à l'intérieur</strong> (ni garage, ni cave, ni véranda) : groupe électrogène, barbecue, brasero, réchaud de camping.</li><li>Ne vous chauffez pas avec le four ou la cuisinière. Un chauffage d'appoint à combustion : <strong>pas plus de 2 heures de suite</strong>, pièce aérée.</li><li><strong>Gardez la chaleur</strong> : regroupez-vous dans une seule pièce, fermez portes et rideaux, superposez les couches de vêtements, bonnet, couvertures et couverture de survie.</li><li><strong>Signes d'alerte</strong> : maux de tête, nausées, fatigue, plusieurs personnes malades en même temps. Aérez, sortez et appelez le 15, le 18 ou le 112.</li></ul><p>Voir aussi <a href=\"vague-de-froid-que-faire.html\">vague de froid : que faire</a>.</p>"),
  ("Comment ne pas manquer de médicaments pendant une crise ?",
   "<ul class=\"check\"><li><strong>Ne laissez pas votre traitement tomber à zéro</strong> : renouvelez-le quelques jours avant la fin de la boîte.</li><li>Gardez dans le kit une <strong>copie de vos ordonnances</strong> et la liste écrite de vos traitements, avec les doses.</li><li><strong>Médicaments à garder au froid</strong> (insuline par exemple) : demandez dès maintenant à votre pharmacien combien de temps ils tiennent hors du frigo, et prévoyez une glacière avec des blocs réfrigérants.</li><li><strong>Appareil médical électrique</strong> (oxygène, aspirateur de mucosités…) : signalez-le à votre fournisseur et à votre médecin, et demandez la conduite à tenir en cas de coupure.</li><li>Des lunettes de secours et une trousse de premiers soins complètent le tout.</li></ul>"),
  ("L'eau du robinet est déclarée non potable : que faire ?",
   "<p>Suivez <strong>exactement</strong> les consignes de la mairie ou de l'agence régionale de santé : elles disent si l'eau peut servir à se laver, à cuisiner, ou si elle doit être bouillie. <strong>Ne faites bouillir l'eau que si on vous le dit</strong> : l'ébullition tue les microbes mais n'élimine pas une pollution chimique. Pour boire, et pour les biberons, utilisez votre <a href=\"combien-eau-stocker-par-personne.html\">réserve d'eau en bouteilles</a>.</p>"),
  ("Comment connaître les risques près de chez moi ?",
   "<p>Sur <strong>georisques.gouv.fr</strong>, saisissez votre adresse : le site indique les risques qui concernent votre logement (inondation, séisme, site industriel, feux de forêt…). Votre mairie tient aussi un document d'information sur les risques de la commune (DICRIM). Connaître ses risques permet d'adapter son kit et de savoir à l'avance s'il faudra plutôt se mettre à l'abri ou évacuer.</p>"),
  ("Comment aider un voisin âgé ou isolé ?",
   "<p>Avant la crise : échangez vos numéros, repérez qui vit seul ou dépend d'un appareil médical, et proposez aux personnes fragiles de s'inscrire, avec leur accord, sur le <strong>registre de la mairie</strong> (ou du CCAS), qui sert aux équipes de secours lors des canicules et des grands froids. Pendant la crise : passez frapper à sa porte, vérifiez qu'il a de l'eau, de la chaleur et ses médicaments, et relayez-lui les consignes s'il n'a pas de radio. Voir <a href=\"entraide-voisins-crise.html\">l'entraide entre voisins</a>.</p>"),
 ]),
 ("courant", "Coupure de courant et alertes", [
  ("Comment savoir s'il y a une coupure de courant chez moi ?",
   "<ol class=\"steps-list\"><li><strong>Regardez dehors</strong> : lampadaires, voisins, commerces. S'ils sont aussi dans le noir, la coupure vient du réseau.</li><li><strong>Vérifiez votre disjoncteur</strong> : s'il a sauté alors que les voisins ont du courant, le problème vient de votre logement.</li><li><strong>Consultez le service « Info coupure » d'Enedis</strong> sur enedis.fr : en saisissant votre adresse, vous voyez si un incident touche votre secteur et l'heure estimée de retour du courant.</li><li><strong>Dépannage Enedis</strong>, 24 h/24 : 09 726 750 suivi des 2 chiffres de votre département (par exemple 09 726 750 69 dans le Rhône). En Corse et en outre-mer, le numéro figure sur votre facture.</li></ol><p>Ce n'est pas votre fournisseur (EDF ou autre) qu'il faut appeler pour une panne : c'est le gestionnaire du réseau. Pendant la coupure, suivez <a href=\"coupure-electricite-que-faire.html\">les bons réflexes</a>.</p>"),
  ("Faut-il s'inscrire pour recevoir FR-Alert ?",
   "<p>Non. Aucune application, aucun compte, aucun numéro à donner : tous les téléphones présents dans la zone en danger reçoivent le message, avec un son spécifique même en mode silencieux. Un téléphone éteint ou en mode avion ne le reçoit pas. Voir <a href=\"fr-alert-que-faire.html\">que faire quand FR-Alert sonne</a>.</p>"),
  ("Radio et énergie de secours : piles, manivelle ou solaire ?",
   "<p>Le guide officiel demande une <strong>radio à piles, avec des piles de rechange</strong>. Une radio à manivelle ou solaire a l'avantage de ne jamais tomber à court, mais il faut tourner souvent et le son est parfois faible. Le meilleur compromis : un modèle qui accepte des piles <strong>et</strong> qui se recharge à la manivelle. Voir <a href=\"radio-a-piles-kit-urgence.html\">quelle radio pour le kit d'urgence</a>.</p>" + "<p>Oui, en complément, mais ne comptez pas sur le petit panneau intégré : il recharge très lentement. Le plus efficace : une <strong>batterie externe de bonne capacité, chargée à l'avance</strong> (et rechargée tous les 3 mois), plus, si vous le souhaitez, un panneau solaire pliable séparé. Voir <a href=\"recharger-telephone-coupure-courant.html\">recharger son téléphone sans courant</a>.</p>"),
 ]),
 ("rumeurs", "Rumeurs et contenus alarmistes", [
  ("Je vois des vidéos qui annoncent des pannes géantes : faut-il s'inquiéter ?",
   "<p>Beaucoup de contenus sur les réseaux sociaux sont alarmistes, parfois générés par IA, et servent souvent à vendre du matériel. Se préparer n'a rien à voir avec la panique : un kit de 72 heures suffit à faire face aux situations les plus courantes (tempête, inondation, coupure). Fiez-vous aux sources officielles : <a href=\"https://www.info.gouv.fr/risques\">info.gouv.fr/risques</a>, votre préfecture, votre mairie. Voir <a href=\"sources.html\">nos sources</a>.</p>"),
 ]),
]

FAQ_LD = [(q, re.sub(r"\s+"," ",re.sub(r"<[^>]+>"," ",a)).strip()) for _,_,items in GROUPS for q,a in items]

np.PAGES.clear()
np.page(
 slug="questions-reponses-kit-urgence",
 emoji="❓",
 title="Kit d'urgence : vos questions pratiques, nos réponses",
 desc="Plus de réseau, toilettes sèches avec un seau, chauffe-eau comme réserve d'eau, talkies, rangement : réponses claires et visuels à partager.",
 h1="Kit d'urgence : les questions pratiques, des réponses claires",
 lead="Les questions qu'on se pose vraiment quand on prépare son kit, et que les listes officielles ne détaillent pas : comment communiquer sans réseau, que faire des toilettes sans eau, où ranger tout ça dans un petit appartement. Des réponses courtes, vérifiées, sans dramatiser.",
 source="guide « Tous responsables » (SGDSN, 2025), service-public.fr, Apple, constructeurs PMR446",
 nav_label="Questions pratiques", nav_emoji="❓",
 sections=qa(GROUPS),
 faq=FAQ_LD,
 related=["recharger-telephone-coupure-courant","combien-eau-stocker-par-personne","kit-urgence-72h-famille-appartement-voiture"],
)
p = np.PAGES[0]
html_ = np.build(p).replace('<meta property="og:image" content="https://tousprets.fr/og-image.png">',
  '<meta property="og:image" content="https://tousprets.fr/img/qr/toilettes-seches-seau.png"><meta property="og:image:width" content="2160"><meta property="og:image:height" content="2700"><meta property="og:image:type" content="image/png"><meta property="og:image:alt" content="Infographie : toilettes sèches avec un seau en cas de coupure d\'eau"><meta name="twitter:image" content="https://tousprets.fr/img/qr/toilettes-seches-seau.png"><meta name="twitter:image:alt" content="Infographie : toilettes sèches avec un seau en cas de coupure d\'eau">')
html_ = html_.replace('"image": "https://tousprets.fr/og-image.png"', '"image": "https://tousprets.fr/img/qr/toilettes-seches-seau.png"')
import json as _j
imgs = []
for n,(t,a) in IMG_TITLES.items():
    for ext, w, h, fmt in (("png", 2160, 2700, "image/png"), ("webp", 1080, 1350, "image/webp")):
        imgs.append({"@type": "ImageObject", "@id": f"https://tousprets.fr/img/qr/{n}.{ext}",
          "contentUrl": f"https://tousprets.fr/img/qr/{n}.{ext}", "url": f"https://tousprets.fr/img/qr/{n}.{ext}",
          "name": f"Infographie : {t}", "caption": t, "description": a, "inLanguage": "fr-FR",
          "width": w, "height": h, "encodingFormat": fmt,
          "license": "https://creativecommons.org/licenses/by/4.0/", "acquireLicensePage": "https://tousprets.fr/licence-visuels.html",
          "creditText": "Tous prêts — tousprets.fr", "copyrightNotice": "© 2026 Tous prêts (tousprets.fr), licence CC BY 4.0",
          "creator": {"@type": "Organization", "name": "Tous prêts", "url": "https://tousprets.fr/"},
          "copyrightHolder": {"@type": "Organization", "name": "Tous prêts", "url": "https://tousprets.fr/"},
          "copyrightYear": 2026, "datePublished": "2026-11-23", "isFamilyFriendly": True,
          "contentLocation": {"@type": "Country", "name": "France"}})
m = __import__("re").search(r'<script type="application/ld\+json">(.*?)</script>', html_, __import__("re").S)
data = _j.loads(m.group(1)); data["@graph"].extend(imgs)
data["@graph"][0]["image"] = [{"@id": f"https://tousprets.fr/img/qr/{n}.png"} for n in IMG_TITLES]
html_ = html_.replace(m.group(1), _j.dumps(data, ensure_ascii=False))
# Pas de doublon visible : la FAQ courte ne sert qu'aux données structurées, on retire son bloc affiché
html_ = re.sub(r'<section id="faq" class="faq".*?</section>\n', '', html_, flags=re.S)
html_ = html_.replace('<li><a href="#faq">Questions fréquentes</a></li>', '')
open(f"{np.SITE}/{p['slug']}.html", "w", encoding="utf-8").write(html_)
print("ok", len(p["title"]), len(p["desc"]))
json.dump([{k: p[k] for k in ("slug","nav_label","nav_emoji")}], open("/home/claude/seo/pages_qa.json","w"), ensure_ascii=False)
