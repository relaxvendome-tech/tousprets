# -*- coding: utf-8 -*-
import sys; sys.path.insert(0, "/home/claude/seo")
import newpages as N
Q = [
 ("eau","Avez-vous au moins 6 litres d'eau en bouteille par personne du foyer ?","combien-eau-stocker-par-personne","Stocker 6 L d'eau par personne"),
 ("food","Avez-vous de quoi manger 3 jours sans cuisson ni frigo ?","aliments-sans-cuisson-kit-urgence","Prévoir 3 jours de repas sans cuisson"),
 ("light","Avez-vous une lampe et une radio qui marchent sans électricité ?","radio-a-piles-kit-urgence","S'équiper d'une lampe et d'une radio à piles"),
 ("health","Avez-vous une trousse de secours et quelques jours d'avance de vos traitements ?","trousse-de-secours-kit-urgence","Compléter la trousse et la réserve de médicaments"),
 ("papers","Vos papiers importants sont-ils copiés, avec un peu d'argent liquide ?","que-mettre-dans-un-kit-d-urgence","Copier vos papiers et garder de l'argent liquide"),
 ("contacts","Vos numéros importants sont-ils notés sur papier, et votre famille a-t-elle un point de rendez-vous ?","plan-familial-mise-en-surete","Faire votre plan familial de mise en sûreté"),
 ("cut","Savez-vous où couper l'eau, le gaz et l'électricité chez vous ?","coupure-electricite-que-faire","Repérer compteur, robinet d'eau et vanne de gaz"),
 ("alert","Savez-vous reconnaître la sirène d'alerte et un message FR-Alert ?","signal-alerte-sirene","Connaître la sirène et FR-Alert"),
 ("bag","Avez-vous un sac prêt à emporter si l'on vous demande d'évacuer ?","sac-de-secours","Préparer un sac de secours"),
 ("risks","Connaissez-vous les risques qui concernent votre commune ?","preparation-catastrophe-naturelle","Consulter les risques de votre commune sur georisques.gouv.fr"),
]
import html as _h
qs = "".join(
 f'<fieldset class="dq" id="dq-{i+1}" data-k="{k}" data-link="{l}" data-act="{_h.escape(a)}"><legend tabindex="-1"><span class="dq-n">{i+1}.</span> {q}</legend>'
 f'<div class="dq-opts"><label><input type="radio" name="{k}" value="2"> <span>Oui</span></label><label><input type="radio" name="{k}" value="1"> <span>En partie</span></label><label><input type="radio" name="{k}" value="0"> <span>Non</span></label></div></fieldset>'
 for i,(k,q,l,a) in enumerate(Q))
nojs = "".join(f'<li><a href="{l}.html">{_h.escape(a)}</a></li>' for k,q,l,a in Q)
# v6 : une question à la fois (pages.js), barre de progression, Précédent / Suivant, résultat en mots.
# Sans JavaScript, toutes les questions restent affichées. Rien n'est stocké.
quiz = f'''<form id="diag" class="diag" action="#" novalidate>
<div class="dg-top" hidden><p class="dg-count" id="dg-count">Question 1 sur {len(Q)}</p><div class="dg-bar" role="progressbar" aria-labelledby="dg-count" aria-valuemin="1" aria-valuemax="{len(Q)}" aria-valuenow="1"><span></span></div></div>
{qs}
<p class="dg-err" id="dg-err" role="alert" hidden></p>
<div class="dg-nav" hidden><button type="button" class="btn btn-2" id="dg-prev">Précédent</button><button type="submit" class="btn" id="dg-next">Suivant</button></div>
</form>
<noscript><div class="dres"><p><strong>Le résultat se calcule avec JavaScript, désactivé sur votre navigateur.</strong> Pour chaque question où vous avez répondu « non » ou « en partie », voici l'action correspondante :</p><ol>{nojs}</ol><p><a class="btn" href="checklist-kit-urgence-72h.html">Ouvrir la checklist à imprimer</a></p></div></noscript>
<div id="dres" class="dres" hidden></div>
<p class="note">Vos réponses restent sur votre appareil : rien n'est enregistré ni envoyé.</p>'''
p = dict(
 slug="diagnostic-suis-je-pret", emoji="✅",
 title="Suis-je prêt ? Le test de préparation aux crises (2 min)",
 desc="10 questions pour savoir si votre foyer est prêt à tenir 72 heures : eau, nourriture, santé, papiers, alerte. Votre niveau et 3 actions prioritaires, gratuit.",
 h1="Suis-je prêt à faire face à une crise ? Le test en 10 questions",
 lead="En 2 minutes, mesurez la préparation de votre foyer face à une coupure, une inondation ou une tempête. Le test s'appuie sur le guide officiel « Tous responsables » : vous obtenez votre niveau de préparation et les 3 actions les plus utiles à faire en premier. Rien n'est enregistré.",
 source="guide « Tous responsables » (SGDSN, 2025), georisques.gouv.fr",
 nav_label="Suis-je prêt ?", nav_emoji="✅",
 sections=[("test","Le test : 10 questions",quiz),
  ("ensuite","Et ensuite ?","<p>Le résultat n'est pas une note : c'est un point de départ. Commencez par l'action n° 1, puis avancez semaine après semaine avec le <a href=\"./\">parcours « prêt en 4 semaines »</a> de l'appli. Pour les risques de votre commune, consultez <a href=\"https://www.georisques.gouv.fr\" rel=\"noopener\">georisques.gouv.fr</a>.</p>")],
 faq=[("Combien de temps dure le test ?","Environ 2 minutes : 10 questions, réponse oui, en partie ou non."),
      ("Mes réponses sont-elles enregistrées ?","Non. Le calcul se fait sur votre appareil, rien n'est envoyé ni conservé."),
      ("Sur quoi se base le test ?","Sur le guide officiel « Tous responsables » (kit d'urgence 72 h, alerte, plan familial) et les consignes de georisques.gouv.fr."),
      ("Que faire si je débute ?","Commencez par l'eau, puis suivez les 3 actions proposées. Chaque étape compte, il n'est pas nécessaire de tout faire en une fois.")],
 related=["kit-de-survie-72h","checklist-kit-urgence-72h","plan-familial-mise-en-surete"],
)
N.TITLES[p["slug"]]=p["h1"]
open(f"{N.SITE}/{p['slug']}.html","w",encoding="utf-8").write(N.build(p))
print("ok")
