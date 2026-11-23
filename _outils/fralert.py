# -*- coding: utf-8 -*-
import sys; sys.path.insert(0, "/home/claude/seo")
import newpages as N
p = dict(
 slug="fr-alert-que-faire",
 emoji="📲",
 title="FR-Alert : que faire quand l'alerte sonne sur le téléphone ?",
 desc="Message FR-Alert reçu ? Ce que signifie l'alerte, pourquoi elle sonne même en silencieux, les bons réflexes et pourquoi ne pas la désactiver.",
 h1="FR-Alert : que faire quand l'alerte sonne sur votre téléphone ?",
 lead="FR-Alert est le système officiel d'alerte des populations. En cas de danger, votre téléphone affiche un message et émet un son strident, même en mode silencieux. Ce n'est ni une arnaque ni une publicité : lisez le message, suivez la consigne (se mettre à l'abri, évacuer, éviter une zone) et écoutez la radio.",
 source="ministère de l'Intérieur, service-public.gouv.fr, guide « Tous responsables »",
 nav_label="Alerte FR-Alert", nav_emoji="📲",
 sections=[
  ("reflexes", "Les bons réflexes quand vous recevez FR-Alert", """
<ol class="steps-list">
<li><strong>Lisez le message en entier.</strong> Il indique la nature du danger, la zone concernée et la conduite à tenir.</li>
<li><strong>Appliquez la consigne tout de suite</strong> : se mettre à l'abri, évacuer, ou éviter un secteur.</li>
<li><strong>Écoutez la radio</strong> (radio locale « ici », ex-France Bleu, ou France Info) pour suivre l'évolution. Une <a href="radio-a-piles-kit-urgence.html">radio à piles</a> fonctionne même sans courant ni réseau.</li>
<li><strong>Ne téléphonez pas aux secours sans urgence vitale : laissez les lignes libres. Si vous êtes sourd ou malentendant, utilisez le 114, joignable par SMS. N'allez pas chercher les enfants à l'école : l'école les protège.</li>
<li><strong>Prévenez vos proches et voisins, surtout les personnes âgées ou isolées sans smartphone. Prévoyez aussi un moyen d'alerte de remplacement (radio à piles, sirène locale) pour les foyers sans téléphone portable.</li>
<li><strong>Ne relayez que des informations officielles.</strong></li>
</ol>"""),
  ("comment", "Comment fonctionne FR-Alert ?", """
<ul class="check">
<li><strong>Aucune application à installer</strong> : le message est diffusé par les antennes relais à tous les téléphones présents dans la zone en danger.</li>
<li><strong>Son spécifique et vibration</strong>, même en mode silencieux, et affichage même écran verrouillé.</li>
<li><strong>Pas de réception si le téléphone est éteint ou en mode avion. FR-Alert passe par le réseau mobile : si les antennes relais sont hors service, le message n'arrive pas non plus.</li>
<li><strong>Qui déclenche ?</strong> Le préfet, éventuellement à la demande du maire.</li>
<li><strong>Où ?</strong> Partout en France, métropole et outre-mer, y compris pour les visiteurs étrangers en itinérance.</li>
<li><strong>Depuis quand ?</strong> Opérationnel depuis le 21 juin 2022.</li>
</ul>
<p>Les alertes peuvent concerner un risque naturel (inondation, feu de forêt, tempête), un accident industriel ou technologique, ou un grave événement de sécurité publique, comme un attentat.</p>"""),
  ("desactiver", "Faut-il désactiver FR-Alert ?", """
<p>Non. Le son est volontairement fort pour réveiller et attirer l'attention en quelques secondes : c'est ce qui le rend utile la nuit. Vérifiez que les alertes d'urgence sont activées dans les réglages de votre téléphone. Le nom exact du menu varie selon les modèles et les versions : cherchez « alertes d'urgence » dans les notifications.</p>
<p class="note">Un vrai message FR-Alert ne demande jamais de cliquer sur un lien pour payer ou donner vos coordonnées. Un SMS qui le fait est une arnaque.</p>"""),
  ("avant", "Se préparer avant l'alerte", """
<p>Une alerte peut imposer de rester chez soi plusieurs jours, ou de partir en quelques minutes. Préparez :</p>
<ul><li>un <a href="kit-de-survie-72h.html">kit d'urgence pour 72 heures</a> à la maison ;</li>
<li>un <a href="sac-de-secours.html">sac de secours</a> prêt à emporter en cas d'évacuation ;</li>
<li>les consignes par situation : <a href="inondation-que-faire.html">inondation</a>, <a href="tempete-que-faire.html">tempête</a>, <a href="confinement-que-faire.html">confinement</a>, <a href="attaque-terroriste-que-faire.html">attaque terroriste</a>.</li></ul>"""),
 ],
 faq=[
  ("Qu'est-ce que FR-Alert ?", "Le dispositif national d'alerte des populations : un message envoyé sur les téléphones présents dans une zone en danger, avec un son spécifique, même en mode silencieux."),
  ("Faut-il installer une application pour recevoir FR-Alert ?", "Non. Aucune application, aucun compte, aucun numéro à donner. Tous les téléphones présents dans la zone le reçoivent."),
  ("Pourquoi FR-Alert sonne même en mode silencieux ?", "C'est voulu : l'alerte doit être perçue immédiatement, y compris la nuit."),
  ("Reçoit-on FR-Alert en mode avion ?", "Non. Un téléphone éteint ou en mode avion ne reçoit pas l'alerte. Gardez une radio à piles."),
  ("Qui envoie les alertes FR-Alert ?", "Le préfet, qui peut agir à la demande du maire."),
  ("Que faire après avoir reçu FR-Alert ?", "Suivre la consigne du message, écouter la radio, ne pas encombrer les lignes d'urgence et prévenir ses voisins vulnérables."),
 ],
 related=["kit-de-survie-72h", "radio-a-piles-kit-urgence", "inondation-que-faire", "confinement-que-faire"],
)
N.TITLES[p["slug"]] = p["h1"]
open(f"{N.SITE}/{p['slug']}.html", "w", encoding="utf-8").write(N.build(p))
print("ok", len(p["title"]), len(p["desc"]))
