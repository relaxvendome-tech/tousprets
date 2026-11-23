# -*- coding: utf-8 -*-
import sys; sys.path.insert(0, "/home/claude/seo")
import newpages as N
p = dict(
 slug="charte-editoriale", emoji="🧭",
 title="Charte éditoriale de Tous prêts : sources, vérification",
 desc="Comment Tous prêts rédige et vérifie ses guides : sources officielles, dates de mise à jour, consignes officielles distinguées de nos conseils, corrections.",
 h1="Notre charte éditoriale : comment nous vérifions chaque conseil",
 lead="Tous prêts traite de sujets où une erreur peut avoir des conséquences. Chaque guide s'appuie sur des sources officielles citées, affiche sa date de mise à jour et distingue la consigne officielle de nos conseils pratiques. Une erreur ? Signalez-la : nous la corrigeons.",
 source="guide « Tous responsables » (SGDSN, 2025) et sites officiels",
 nav_label="Charte éditoriale", nav_emoji="🧭",
 sections=[
  ("regles","Nos six règles",'''<ol class="steps-list">
<li><strong>Une source officielle pour chaque conseil sensible</strong> : guide « Tous responsables », info.gouv.fr, georisques.gouv.fr, service-public.fr, ministères, Météo-France, Santé publique France, Vigicrues et intérieur.gouv.fr (alerte et FR-Alert). Les sources sont citées en haut de chaque guide et sur la page <a href="sources.html">Sources et méthode</a>.</li>
<li><strong>Une date de mise à jour visible</strong> sur chaque page.</li>
<li><strong>La consigne officielle d'abord.</strong> Quand nous ajoutons un conseil pratique qui ne vient pas d'un texte officiel, nous le présentons comme un conseil de Tous prêts. En cas de doute, la consigne des autorités fait foi.</li>
<li><strong>Pas d'affirmation non vérifiée.</strong> Si un fait ne peut pas être confirmé par une source fiable, il n'est pas publié. Pas de chiffres inventés, pas d'alarmisme.</li>
<li><strong>Indépendance.</strong> Tous prêts est une initiative citoyenne : pas de publicité, pas de liens sponsorisés, aucune marque mise en avant, aucun lien avec l'État.</li>
<li><strong>Corrections rapides.</strong> Toute erreur signalée est vérifiée puis corrigée, et la date de mise à jour de la page change.</li></ol>'''),
  ("redaction","Comment les guides sont rédigés",'''<p>Les guides sont rédigés par l'équipe de Tous prêts, avec l'aide d'outils d'intelligence artificielle pour la mise en forme. Chaque fait (quantités, numéros, obligations, consignes) est vérifié sur une source officielle avant publication. Les photos sont libres de droits (domaine public) et créditées sur la page <a href="licence-visuels.html">Licence des visuels</a>.</p>
<p class="note">Tous prêts ne remplace ni les consignes des autorités ni un avis médical. En cas de danger immédiat, appelez le 112 (ou le 114 par SMS).</p>'''),
  ("signaler","Signaler une erreur",'''<p>Une information vous semble fausse ou dépassée ? Écrivez-nous en précisant la page et, si possible, la source officielle : relaxvendome@gmail.com. Vous pouvez aussi signaler une erreur d'information sur un site public concerné (service-public.fr ou le site de la préfecture). Chaque page comporte aussi un lien « Signaler une erreur ».</p>'''),
 ],
 faq=[("Tous prêts est-il un site officiel ?","Non. C'est une initiative citoyenne indépendante qui s'appuie sur le guide officiel « Tous responsables » et cite ses sources."),
      ("Comment signaler une erreur ?","Par e-mail, via le lien « Signaler une erreur » présent sur chaque page. Nous vérifions puis corrigeons."),
      ("Le site gagne-t-il de l'argent avec des produits ?","Non. Pas de publicité, pas d'affiliation, aucune marque mise en avant.")],
 related=["sources","pourquoi","licence-visuels"],
)
N.TITLES[p["slug"]]=p["h1"]
open(f"{N.SITE}/{p['slug']}.html","w",encoding="utf-8").write(N.build(p)); print("ok")
