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
qs = "".join(
 f'<fieldset class="dq" data-k="{k}" data-link="{l}" data-act="{a}"><legend>{i+1}. {q}</legend>'
 f'<label><input type="radio" name="{k}" value="2"> Oui</label><label><input type="radio" name="{k}" value="1"> En partie</label><label><input type="radio" name="{k}" value="0"> Non</label></fieldset>'
 for i,(k,q,l,a) in enumerate(Q))
quiz = f'''<style>.dq{{border:1px solid var(--border);border-radius:var(--r-sm);background:var(--surface);padding:.8rem 1rem;margin:0 0 .7rem}}.dq legend{{font-weight:700;padding:0 .3rem}}.dq label{{display:inline-flex;align-items:center;gap:.35rem;margin:.35rem 1.1rem .1rem 0;cursor:pointer}}.dres{{background:var(--primary-s);border-radius:var(--r);padding:1.2rem 1.25rem;margin-top:1rem}}.dres .big{{font-family:var(--serif);font-size:2.4rem;font-weight:700;color:var(--primary);line-height:1}}</style>
<form id="diag" onsubmit="return false">{qs}<button class="btn" type="button" id="dgo">Voir mon résultat</button></form>
<div id="dres" class="dres" hidden aria-live="polite"></div>
<p class="note">Vos réponses restent sur votre appareil : rien n'est enregistré ni envoyé.</p>
<script>(function(){{var b=document.getElementById('dgo');b.addEventListener('click',function(){{var fs=[].slice.call(document.querySelectorAll('.dq')),tot=0,miss=[],unans=0;fs.forEach(function(f){{var c=f.querySelector('input:checked');if(!c){{unans++;miss.push([0,f]);return;}}var v=+c.value;tot+=v;if(v<2)miss.push([v,f]);}});var pct=Math.round(tot/(fs.length*2)*100);var msg=pct>=80?'Très bien préparé. Pensez à vérifier votre kit deux fois par an.':pct>=50?'Bonne base. Quelques actions simples vous mettront à l\\'abri.':'Vous démarrez : chaque petit pas compte, commencez par l\\'action n° 1.';miss.sort(function(a,b){{return a[0]-b[0]}});var top=miss.slice(0,3).map(function(m){{return '<li><a href="'+m[1].dataset.link+'.html">'+m[1].dataset.act+'</a></li>'}}).join('');var r=document.getElementById('dres');r.hidden=false;r.innerHTML='<p class="big">'+pct+' %</p><p><strong>'+msg+'</strong></p>'+(unans?'<p>'+unans+' question(s) sans réponse, comptée(s) comme « non ».</p>':'')+(top?'<p>Vos 3 prochaines actions :</p><ol>'+top+'</ol>':'<p>Bravo, rien ne manque à l\\'essentiel.</p>')+'<p><a class="btn" href="./">Cocher ma liste dans l\\'appli</a></p>';r.scrollIntoView({{behavior:'smooth',block:'start'}});}});}})();</script>'''
p = dict(
 slug="diagnostic-suis-je-pret", emoji="✅",
 title="Suis-je prêt ? Le test de préparation aux crises (2 min)",
 desc="10 questions pour savoir si votre foyer est prêt à tenir 72 heures : eau, nourriture, santé, papiers, alerte. Score immédiat et 3 actions prioritaires, gratuit.",
 h1="Suis-je prêt à faire face à une crise ? Le test en 10 questions",
 lead="En 2 minutes, mesurez la préparation de votre foyer face à une coupure, une inondation ou une tempête. Le test s'appuie sur le guide officiel « Tous responsables » : vous obtenez un score et les 3 actions les plus utiles à faire en premier. Rien n'est enregistré.",
 source="guide « Tous responsables » (SGDSN, 2025), georisques.gouv.fr",
 nav_label="Suis-je prêt ?", nav_emoji="✅",
 sections=[("test","Le test : 10 questions",quiz),
  ("ensuite","Et ensuite ?","<p>Le score n'est pas une note : c'est un point de départ. Commencez par l'action n° 1, puis avancez semaine après semaine avec le <a href=\"./\">parcours « prêt en 4 semaines »</a> de l'appli. Pour les risques de votre commune, consultez <a href=\"https://www.georisques.gouv.fr\" rel=\"noopener\">georisques.gouv.fr</a>.</p>")],
 faq=[("Combien de temps dure le test ?","Environ 2 minutes : 10 questions, réponse oui, en partie ou non."),
      ("Mes réponses sont-elles enregistrées ?","Non. Le calcul se fait sur votre appareil, rien n'est envoyé ni conservé."),
      ("Sur quoi se base le test ?","Sur le guide officiel « Tous responsables » (kit d'urgence 72 h, alerte, plan familial) et les consignes de georisques.gouv.fr."),
      ("Que faire si mon score est faible ?","Commencez par l'eau, puis suivez les 3 actions proposées. Chaque étape compte, il n'est pas nécessaire de tout faire en une fois.")],
 related=["kit-de-survie-72h","checklist-kit-urgence-72h","plan-familial-mise-en-surete"],
)
N.TITLES[p["slug"]]=p["h1"]
open(f"{N.SITE}/{p['slug']}.html","w",encoding="utf-8").write(N.build(p))
print("ok")
