# -*- coding: utf-8 -*-
import importlib.util, re
spec = importlib.util.spec_from_file_location("np", "/home/claude/seo/newpages.py")
np = importlib.util.module_from_spec(spec); spec.loader.exec_module(np)
np.PAGES.clear()
names = [("toilettes-seches-seau","Toilettes sèches avec un seau"),("chauffe-eau-reserve-eau","Le chauffe-eau, une réserve d'eau"),
         ("communiquer-sans-reseau","Communiquer sans réseau"),("rangement-petit-appartement","Ranger son kit d'urgence sans cave"),
         ("objets-oublies-kit-urgence","8 objets qu'on oublie dans le kit d'urgence")]
liste = "".join(f'<li><a href="img/qr/{n}.png" download>{t}</a> (PNG 2160 × 2700)</li>' for n,t in names)
np.page(
 slug="licence-visuels", emoji="🖼️",
 title="Infographies libres de droits : conditions de réutilisation",
 desc="Les infographies Tous prêts sont sous licence CC BY 4.0 : réutilisation libre, y compris imprimée, en citant tousprets.fr. Formulation à copier.",
 h1="Réutiliser nos infographies : c'est libre, il suffit de citer la source",
 lead="Mairies, associations, écoles, journaux, particuliers : vous pouvez réutiliser, imprimer et partager les infographies de Tous prêts, y compris dans un bulletin ou sur les réseaux sociaux. Une seule condition : citer la source.",
 source="licence Creative Commons Attribution 4.0 International",
 nav_label="Licence des visuels", nav_emoji="🖼️",
 sections=[
  ("licence","La licence", '<p>Les infographies sont publiées sous licence <a href="https://creativecommons.org/licenses/by/4.0/deed.fr" rel="license">Creative Commons Attribution 4.0 International (CC BY 4.0)</a>. Vous pouvez les partager, les imprimer et les adapter, pour tout usage, à condition de créditer Tous prêts et d\'indiquer si vous les avez modifiées.</p>'),
  ("citer","Comment citer", '<p>Formulation à copier sous l\'image :</p><p class="note"><strong>Infographie : Tous prêts — tousprets.fr, licence CC BY 4.0</strong></p><p>Sur un site, ajoutez un lien vers <a href="https://tousprets.fr/">https://tousprets.fr/</a>. Les fichiers contiennent déjà ces informations dans leurs métadonnées.</p>'),
  ("fichiers","Télécharger les fichiers", f'<ul class="check">{liste}</ul><p>Toutes les fiches sont aussi visibles dans la page <a href="questions-reponses-kit-urgence.html">Questions pratiques</a>.</p>'),
  ("limites","Les limites", '<p>Ne présentez pas Tous prêts comme un service de l\'État et ne laissez pas croire qu\'il approuve votre publication. Les consignes des autorités priment toujours sur ces fiches générales.</p>'),
 ],
 faq=[("Puis-je imprimer les infographies pour ma mairie ou mon association ?","Oui, librement, en citant « Tous prêts — tousprets.fr, licence CC BY 4.0 »."),
      ("Puis-je modifier une infographie ?","Oui, en citant la source et en indiquant que vous l'avez modifiée.")],
 related=["questions-reponses-kit-urgence","kit-de-survie-72h","sources"],
)
p = np.PAGES[0]
open(f"{np.SITE}/{p['slug']}.html","w",encoding="utf-8").write(np.build(p))
print("ok")
