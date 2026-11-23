# -*- coding: utf-8 -*-
"""Page « kit de survie gouvernement pdf » (réutilise le moteur de newpages.py)."""
import sys; sys.path.insert(0, "/home/claude/seo")
import newpages as N

OFF = "https://www.info.gouv.fr/actualite/tous-responsables-un-guide-pour-mieux-faire-face-aux-risques"
OFF2 = "https://www.info.gouv.fr/risques/se-preparer-a-une-situation-durgence"
SG = "https://www.sgdsn.gouv.fr/publications/guide-tous-responsables"

p = dict(
 slug="kit-de-survie-gouvernement-pdf",
 emoji="📄",
 title="Kit de survie gouvernement PDF : guide officiel et liste 72h",
 desc="Où télécharger le PDF officiel du guide « Tous responsables » (kit d'urgence 72h), ce qu'il contient, et une checklist gratuite à imprimer et cocher.",
 h1="Kit de survie du gouvernement en PDF : le guide officiel et la liste à imprimer",
 lead="Le « kit de survie » du gouvernement est le guide « Tous responsables », publié par le SGDSN le 20 novembre 2025. Le PDF officiel est gratuit sur sgdsn.gouv.fr et info.gouv.fr, en version standard, FALC, impression et anglais. Il demande un kit pour tenir 72 heures, dont 6 litres d'eau par personne. Liens officiels et checklist à imprimer ci-dessous.",
 source="guide « Tous responsables » (SGDSN, 2025), info.gouv.fr",
 nav_label="Guide officiel en PDF", nav_emoji="📄",
 sections=[
  ("telecharger", "Télécharger le PDF officiel « Tous responsables »", f"""
<div class="cards"><div class="card"><h3><span class="ic" aria-hidden="true">🏛️</span>Le guide officiel (État)</h3>
<p>Le PDF est publié par le Gouvernement. Téléchargez-le uniquement sur un site en <strong>.gouv.fr</strong> :</p>
<ul><li><a href="{OFF}" rel="noopener">info.gouv.fr : page du guide « Tous responsables »</a> (lien de téléchargement du PDF)</li>
<li><a href="{SG}" rel="noopener">sgdsn.gouv.fr : page de publication du guide</a> (les 4 versions PDF)</li>
<li><a href="{OFF2}" rel="noopener">info.gouv.fr : se préparer à une situation d'urgence</a> (infographie du kit)</li></ul></div>
<div class="card"><h3><span class="ic" aria-hidden="true">✅</span>Notre liste à imprimer (gratuite)</h3>
<p>Une page A4 à cocher, reprenant les catégories du guide, avec les quantités calculées pour votre foyer.</p>
<ul><li><a href="checklist-kit-urgence-72h.html">Checklist du kit d'urgence 72h à imprimer</a></li>
<li><a href="./">Version appli : cochez, adaptez au nombre de personnes, même hors ligne</a></li></ul></div></div>
<p class="note">Tous prêts est une initiative citoyenne indépendante, sans lien avec l'État. Nous ne republions pas le PDF officiel : nous renvoyons vers lui et proposons un outil pratique en complément. En cas de doute, le guide officiel et les consignes des autorités font foi.</p>"""),
  ("fiche", "Fiche d'identité du PDF officiel", f"""
<table class="tbl"><tbody>
<tr><th scope="row">Titre exact</th><td>« Tous responsables. Face aux risques, agissons. »</td></tr>
<tr><th scope="row">Éditeur</th><td>Secrétariat général de la défense et de la sécurité nationale (SGDSN), services du Premier ministre</td></tr>
<tr><th scope="row">Date de publication</th><td>20 novembre 2025</td></tr>
<tr><th scope="row">Prix</th><td>Gratuit</td></tr>
<tr><th scope="row">Versions</th><td>PDF standard (environ 13,7 Mo), version <strong>FALC</strong> « facile à lire et à comprendre » (moins de 1 Mo), version <strong>pour impression</strong> (environ 15 Mo), version anglaise <em>All Responsible Guide</em></td></tr>
<tr><th scope="row">Où le télécharger</th><td><a href="{SG}" rel="noopener">sgdsn.gouv.fr</a> et <a href="{OFF}" rel="noopener">info.gouv.fr</a></td></tr>
</tbody></table>
<p>Petit téléphone ou connexion lente ? Prenez la version FALC, la plus légère. Pour une impression papier à garder dans le kit, prenez la version « pour impression ».</p>"""),
  ("contenu", "Ce que contient le guide « kit de survie » du gouvernement", """
<p>Le guide est organisé en trois parties :</p>
<table class="tbl"><thead><tr><th>Partie</th><th>Ce qu'on y trouve</th></tr></thead><tbody>
<tr><td><strong>Bien préparés</strong></td><td>Le kit d'urgence 72 h, la check-list, qui prévenir, les numéros d'urgence</td></tr>
<tr><td><strong>Bien protégés</strong></td><td>Les risques (inondation, tempête, accident industriel, cyberattaque…), les signaux d'alerte (sirène, FR-Alert) et les bons réflexes</td></tr>
<tr><td><strong>Tous engagés</strong></td><td>Se former aux gestes qui sauvent, devenir bénévole ou réserviste, aider ses voisins</td></tr></tbody></table>
<p>Le guide part d'un constat simple : pendant une crise majeure, les secours peuvent être saturés. Chaque foyer doit donc pouvoir tenir seul environ <strong>72 heures</strong>. Notre <a href="guide-tous-responsables-resume.html">résumé du guide</a> et notre page <a href="kit-urgence-72h-gouvernement.html">ce que dit le guide sur le kit 72h</a> détaillent chaque partie.</p>"""),
  ("liste", "La liste du kit d'urgence 72h du gouvernement", """
<ul class="check">
<li><strong>Eau</strong> : 6 litres par personne (2 litres par jour pendant 3 jours), en bouteilles. Pastilles de décontamination en dernier recours.</li>
<li><strong>Nourriture</strong> : conserves et aliments qui se mangent sans cuisson ni frigo, ouvre-boîte.</li>
<li><strong>Avoir chaud</strong> : couverture de survie, vêtements chauds.</li>
<li><strong>Se soigner</strong> : trousse de premiers secours, médicaments habituels, copies d'ordonnances.</li>
<li><strong>S'informer</strong> : radio à piles avec piles de rechange, pour suivre les consignes des autorités.</li>
<li><strong>S'éclairer</strong> : lampe de poche ou frontale, piles.</li>
<li><strong>Argent liquide</strong> : en cas de panne des paiements par carte.</li>
<li><strong>Outils de base</strong> : couteau multifonction, briquet ou allumettes, chargeur de téléphone.</li>
<li><strong>Papiers</strong> : copies des documents importants, doubles des clés, liste des numéros utiles sur papier.</li>
</ul>
<p>Le guide recommande de placer le kit dans un endroit facile d'accès et de <strong>vérifier son contenu deux fois par an</strong> (dates de péremption, piles). La fiche « Se préparer à une situation d'urgence » d'info.gouv.fr dit « une fois par an » : deux contrôles par an restent le plus sûr. Pour aller plus loin : <a href="combien-eau-stocker-par-personne.html">combien d'eau stocker</a>, <a href="aliments-sans-cuisson-kit-urgence.html">aliments sans cuisson</a>, <a href="radio-a-piles-kit-urgence.html">quelle radio choisir</a>.</p>"""),
  ("numeros", "Numéros d'urgence à garder sur papier dans le kit", """
<p>Le guide demande de garder une liste des numéros utiles <strong>sur papier</strong> : en cas de panne, le téléphone peut être déchargé. Les numéros d'urgence rappelés par info.gouv.fr :</p>
<table class="tbl"><thead><tr><th>Numéro</th><th>Service</th></tr></thead><tbody>
<tr><td><strong>112</strong></td><td>Numéro d'urgence européen</td></tr>
<tr><td><strong>15</strong></td><td>Samu</td></tr>
<tr><td><strong>17</strong></td><td>Police ou gendarmerie</td></tr>
<tr><td><strong>18</strong></td><td>Pompiers</td></tr>
<tr><td><strong>114</strong></td><td>Personnes sourdes, malentendantes ou ne pouvant pas parler (SMS, appli, fax)</td></tr>
<tr><td><strong>196</strong></td><td>Urgences en mer</td></tr>
<tr><td><strong>191</strong></td><td>Urgences aéronautiques</td></tr></tbody></table>
<p>Pour reconnaître une alerte : <a href="signal-alerte-sirene.html">le signal de la sirène</a> et <a href="fr-alert-que-faire.html">les messages FR-Alert sur le téléphone</a>.</p>"""),
  ("adapter", "Adapter le kit à votre foyer", """
<p>La liste officielle est une base. Elle ne dit pas combien acheter pour <em>votre</em> foyer. Ajoutez selon votre situation :</p>
<ul><li><strong>Bébé</strong> : lait infantile, couches, eau adaptée aux biberons (<a href="kit-urgence-bebe.html">kit bébé</a>)</li>
<li><strong>Animaux</strong> : nourriture, eau, laisse ou caisse de transport (<a href="kit-urgence-animaux.html">kit animaux</a>)</li>
<li><strong>Appartement ou voiture</strong> : volume et rangement différents (<a href="kit-urgence-72h-famille-appartement-voiture.html">famille, appartement, voiture</a>)</li>
<li><strong>Évacuation</strong> : un <a href="sac-de-secours.html">sac de secours</a> léger, prêt à emporter</li></ul>
<p>L'appli Tous prêts calcule les quantités selon le nombre de personnes et la durée choisie (72 heures jusqu'à 3 mois).</p>"""),
 ],
 faq=[
  ("Où télécharger le PDF du kit de survie du gouvernement ?", "Sur sgdsn.gouv.fr (page de publication du guide « Tous responsables ») ou sur info.gouv.fr. Téléchargez-le uniquement depuis un site en .gouv.fr."),
  ("Le kit de survie du gouvernement est-il gratuit ?", "Oui. Le guide « Tous responsables » est un document public gratuit. Il ne vend aucun kit : il dit quoi rassembler chez soi."),
  ("Combien d'eau prévoir pour 72 heures ?", "6 litres par personne, soit 2 litres par jour pendant 3 jours. Pour une famille de 4 personnes : 24 litres."),
  ("Existe-t-il un « kit officiel » du gouvernement à acheter ?", "Non. Le guide donne une liste à constituer soi-même. Méfiez-vous des offres payantes présentées comme « kit officiel »."),
  ("Tous prêts est-il le site officiel ?", "Non. Tous prêts est une initiative citoyenne indépendante. Nous renvoyons vers le PDF officiel et proposons une checklist gratuite pour passer à l'action."),
  ("Existe-t-il une version simplifiée ou en anglais du guide ?", "Oui. Le SGDSN publie aussi une version FALC (facile à lire et à comprendre), une version pour impression et une version anglaise, All Responsible Guide, sur sgdsn.gouv.fr."),
  ("Faut-il vérifier son kit d'urgence ?", "Oui. Le guide « Tous responsables » conseille deux fois par an, la fiche d'info.gouv.fr au moins une fois par an : dates de péremption des aliments et des médicaments, et piles."),
 ],
 related=["guide-tous-responsables-resume", "kit-urgence-72h-gouvernement", "checklist-kit-urgence-72h", "que-mettre-dans-un-kit-d-urgence"],
)
N.TITLES[p["slug"]] = p["h1"]
open(f"{N.SITE}/{p['slug']}.html", "w", encoding="utf-8").write(N.build(p))
print("ok", len(p["title"]), len(p["desc"]), len(p["lead"].split()))
