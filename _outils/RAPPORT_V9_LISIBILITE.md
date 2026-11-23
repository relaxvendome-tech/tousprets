# Rapport v9 : lisibilité, ergonomie et charge cognitive (23 novembre 2026)

Rien n'est commité ni poussé. Aucune URL, aucun title, aucune description, aucun canonical ni aucun JSON-LD des pages existantes n'a changé (contrôle automatique sur les 73 pages, par rapport à HEAD). Aucune consigne de sécurité n'a été modifiée. Aucune clé localStorage ni aucune logique de l'appli n'a été touchée. Aucune ressource externe n'a été ajoutée.

## 1. Problèmes constatés avant
- **Feuille de style** : 52,6 Ko et 8 blocs empilés. Il y avait 7 déclarations `:root` contradictoires (refonte, v2, palette v3, v4), avec deux palettes successives (verte puis bleue). On y trouvait 3 échelles de titres concurrentes, une police serif encore déclarée et 54 sélecteurs morts : barre latérale `.risks`, `.layout`, `.topnav`, `.now`, `.box--*` jamais utilisés, `.brand-s`.
- **Tailles** : 59 règles sous 15,5 px. Exemples : méta du héros 13 px, en-têtes de tableau 13 px, titres d'encadrés 13 px, légendes 13,6 px, filtres 12,8 px, catégorie de recherche 11,5 px.
- **Appli** : titres en Georgia (serif) et texte en police système. On trouvait des textes de 10 à 13,5 px : notes, sous-titres, unités, barre du bas à 10 px. Les boutons de quantité faisaient 27 px et les cases 18 px. Les champs étaient à 13 px, ce qui force le zoom sur iPhone. Le bouton Réglages n'avait qu'une icône. Deux boutons ✕ n'avaient pas de nom accessible. L'état vide des contacts était peu utile. Les liens des notes s'affichaient en bleu navigateur (#0000EE) en mode sombre (contraste 1,65:1).
- **Guides** : sur mobile, la photo venait avant le titre. Il y avait 2 boutons d'égale force. La méta était présentée en 3 pastilles. L'avis « sources » s'intercalait avant « L'essentiel ». On notait plusieurs effets décoratifs (dégradés, ombres, cartes qui se soulèvent) et des réponses de FAQ en gris atténué. Le H1 était centré par erreur dans le héros mobile.
- **Accordéons** : 41 réponses de FAQ contenant une consigne de sécurité (« jamais », « monoxyde », « appelez le 112 », « évacuation »…) étaient fermées par défaut.
- **Accueil** : 2 boutons de même poids et la promesse en petites capitales. La présentation de la checklist n'arrivait qu'en 4e section, à environ 3 600 px de haut sur mobile. Trois « portes d'entrée » faisaient concurrence au bouton principal.

## 2. Choix et justification cognitive
- **Un seul jeu de tokens** en tête de style.css. Une seule police (Inter) et une seule échelle. Une même valeur produit le même rendu partout, ce qui réduit l'effort de décodage visuel.
- **Largeur de lecture de 68ch** pour les paragraphes et les listes des guides. Au-delà de 75 caractères, l'œil perd la ligne suivante.
- **Ordre des guides** : titre, résumé, méta, une action principale, L'essentiel, sommaire, contenu, erreurs à éviter, sources, FAQ, liens connexes. La réponse arrive avant le détail (divulgation progressive). Le second bouton devient un lien, pour n'imposer qu'une décision. La photo passe sous le texte sur mobile, au format 2:1.
- **4 niveaux visuels**, sans nouveau composant :
  1. **essentiel** (`.essentiel`, `.start`) : fond bleu pâle et filet bleu de 5 px ;
  2. **important** (`.card`, `.steps-list`, `.box.warn`) : surface blanche et bordure fine ;
  3. **complémentaire** (`.note`, `.box`, `.disclaimer`) : fond neutre, sans couleur d'alerte ;
  4. **pour aller plus loin** (`.gcompl`, À lire aussi, signalement, partage) : sans fond, séparé par un filet.

  **Le rouge** ne sert plus qu'aux vrais dangers (`.card.danger`, `.box--interdit`, `.urgence`, `.qa-sos`). L'orange des `.note` a été retiré, parce qu'une note n'est pas une alerte. Cette hiérarchie évite de transformer chaque information en alerte.
- **FAQ** : les réponses passent en texte plein contraste. Une question dont la réponse contient une consigne de sécurité reste ouverte (attribut `open`, 41 cas) : on ne cache jamais une consigne. La question reste repliable.
- **Tableaux** : défilement horizontal signalé par une ombre aux bords (effet fonctionnel, pas décoratif), lignes alternées, en-têtes de 14 px non coupés. Les régions défilables étaient déjà focusables.
- **Accueil** (landing.html et landing.css), dans l'ordre :
  1. H1 conservé « Être prêt change tout. », suivi de la ligne visible « Checklist gratuite du kit d'urgence 72 h, calculée pour votre foyer, utilisable hors ligne. » (19 à 22 px) ;
  2. **un seul bouton** « Préparer mon foyer », avec en dessous 2 liens texte (urgence en cours, niveau de préparation) ;
  3. **3 bénéfices** numérotés ;
  4. présentation de la checklist ;
  5. guides principaux et bons réflexes ;
  6. profils du foyer ;
  7. hors ligne et confidentialité ;
  8. sources et engagements ;
  9. appel final.

  Les « trois portes » ont été fondues dans les sections. Aucun lien n'est perdu : chaque ancien lien est toujours présent.
- **Checklist de l'appli** : petits ajustements de balisage via lisibilite_v9.py, sans toucher à la logique.
  - Lignes de 56 px, cases de 26 px, boutons ± de 44 px, puces de 44 px, champs à 16 px.
  - Un élément coché prend un fond vert pâle et la mention « · fait ». L'état ne passe donc pas par la seule couleur, et le texte barré, peu lisible, est supprimé.
  - Bloc de progression : « N faits sur M · R à faire » et « Prochaine étape : … (phase) ».
  - Confirmation discrète « Enregistré sur cet appareil » (`role=status`, 1,6 s).
  - État vide des contacts devenu utile.
  - Libellé visible « Réglages » et noms accessibles des boutons ✕.

  Le script `v9-js` lit le DOM et n'écrit aucune clé.
- **Performance** : Inter est chargée par le script `v9-js` après l'événement load sur l'accueil, pour que la photo du héros (LCP) passe d'abord. La police de repli « Inter Fallback » (Arial ajusté) évite tout décalage (CLS 0).

## 3. Tokens (style.css, en tête)
| Famille | Valeurs |
|---|---|
| Fonds, texte | --bg #F3F6FA, --surface #FFF, --alt #EAF0F7, --text #14233A, --muted **#4A5B72** (était #51627A), --border #D6DEE8 |
| Principale, secondaire | --primary #1E4F8C (-h, -s), --night/--band #0F2440, --accent/--focus #D9731A |
| Sens | --danger **#B8352A** (valeur AA déjà imposée en v8), --warn #A4500F, --ok **#256B42** (était #2E7D4F : 4,39:1 sur --alt) |
| Sombre | mêmes noms. Retouches : --muted #A9B7CB, --border #2A3B57, --danger #F09488 |
| Espacements | --s1 à --s16 (4 à 64 px) |
| Rayons | --r-xs 6, --r-sm 10, --r 16, --r-lg **20** (était 24), --r-pill |
| Ombres | --sh-1/2/3. **--shadow = --sh-1** (était --sh-2) |

`--serif` a été supprimé et toutes ses utilisations remplacées par `--sans`.

## 4. Échelle typographique (clamp, mobile → ordinateur)
| Niveau | Mobile 320 px | Ordinateur |
|---|---|---|
| H1 | 28 px (36 px dès 640 px) | 48 px |
| H2 | 24 px | 34 px (28 px dès 830 px) |
| H3 | 20 px | 25 px |
| H4 | 18 px | 20 px |
| Corps | 17 px | 19 px |
| Chapeau | 18 px | 21 px |
| Secondaire | 15 px | 16 px |
| Métadonnées | 14 px (plancher) | 14 px |

Interlignes : 1,65 pour le corps et 1,2 pour les titres. L'H1 mobile descend à 28 px parce que la contrainte de largeur prime (« Saint-Barthélemy » déborderait à 36 px sur 320 px). Dans l'appli, le texte est à 17 px, les notes à 15 px, les métadonnées et les unités à 14 px. Seule exception : la barre du bas à 12 px (11 px sous 360 px), parce que 7 onglets doivent tenir sur 320 px.

## 5. Tests chiffrés (état final)
- **style.css** : 52 604 → 59 084 octets. Le socle consolidé passe de 52 604 à 48 171 octets (−8,4 % : 7 `:root` → 1 jeu de tokens, 54 sélecteurs morts retirés). Le bloc v9 ajoute 10 913 octets.
- **index.html** : 209 933 → 217 830 octets. Le CSS appli injecté est compacté ; la source commentée reste dans _outils.
- **Playwright** : 518 chargements (74 pages × 320, 375, 390, 430, 768, 1366 et 1920 px). Résultat : 0 erreur JS, 0 débordement, 1 H1 par page, 0 JSON-LD invalide.
- **Liens** : 0 lien interne ou ancre morte. `audit_v5.py` : 0 erreur, 0 avertissement.
- **SEO** : title, description, canonical, robots et JSON-LD identiques à HEAD sur les 73 pages existantes. Aucun mot indexable perdu sur les guides, sauf le compteur « 16 », passé à 17 avec la nouvelle page. Sur l'accueil, seuls des intitulés de landing ont été reformulés ; la section seo-about est intacte.
- **axe-core 4** (WCAG 2.2 AA et bonnes pratiques) :
  - 14 écrans (accueil, 3 onglets de l'appli, 10 pages) × clair et sombre × 390 et 1366 px = 56 audits ;
  - **0 défaut sérieux ou critique** (avant correction : 18, dont `.hm-ok` à 4,39:1 et les liens #0000EE en sombre dans l'appli) ;
  - restent 12 « page-has-heading-one » modérés sur les onglets de l'appli, où le H1 de l'accueil est masqué. Ce défaut existait déjà.
- **Appli** : 23/23 contrôles réussis :
  - 7 onglets ;
  - ajout d'un membre ;
  - quantités ;
  - cochage, puis progression ;
  - rechargement : coches, quantités et foyer conservés ;
  - clés localStorage identiques (checklist_kit72, food_stock_v1, profiles_v1, theme_v1) ;
  - toutes les cibles ≥ 44 px ;
  - cache tous-prets-v75 ;
  - accueil et guide hors ligne ;
  - 0 erreur JS.
- **Lighthouse mobile**, 2 à 3 passages par page, Perf/Access/BP/SEO :

| Page | Avant (HEAD) | Après |
|---|---|---|
| Accueil | 86–89 / 100 / 100 / 100, LCP 3,5 s | 83–87 / 100 / 100 / 100, LCP 3,7–3,8 s, CLS 0 |
| Guide inondation | 98 / 100 / 100 / 100 | 97–98 / 100 / 100 / 100 |
| Tous les guides | 91–94 / 100 / 100 / 100 | 94–97 / 100 / 100 / 100 |
| Checklist | 99 / 100 / 100 / 100 | 98–99 / 100 / 100 / 100 |

  Sur l'accueil, le LCP simulé augmente de 0,2 à 0,3 s (« render delay »). Le passage d'Inter après le chargement n'a pas réduit cet écart. Il est très probablement lié aux 8 Ko de HTML en plus (CSS et JS en ligne), sans que cela ait été isolé. Le score reste dans la variabilité habituelle.
- **Idempotence** : deux passages de redesign.py donnent des md5 identiques (html, css, json, xml).
- **Captures regardées** : accueil 390 et 1366, inondation et kit 72 h en 375, appli (scénarios, stock, contacts) en 390 clair et sombre, mentions légales. Trois défauts vus et corrigés : H1 centré par erreur, « 72 h » coupé en fin de ligne, retrait du lien secondaire.

## 6. Nouvelle page : panne-numerique-cyberattaque-72h.html
- Créée depuis `_outils/panne-numerique-72h.md`, version à jour (70 € par adulte, 30 € par enfant, source DNB), sur le gabarit de cyberattaque-que-faire. Aucune consigne ni aucun chiffre modifié.
- Structure :
  - H1 tiré du Markdown ;
  - 4 H2 ;
  - réflexes et questions de FAQ en H3 (le H3 est placé dans `<summary>`) ;
  - encadré `.urgence` 112 en tête ;
  - « Pendant et après » en `.box.warn` ;
  - FAQ en details/summary, avec JSON-LD FAQPage, Article et BreadcrumbList.
- Le lien `./#app-start` est conservé. Les sources sont en bas, juste avant la FAQ, selon l'ordre v9.
- « L'essentiel » reprend mot pour mot les 4 titres de réflexes.
- Photo de héros : celle de cyberattaque.
- Rattachement :
  - redesign.py (CAT, UNIV reagir après cyberattaque, EXTRA_REL), copié dans /home/claude/seo ;
  - seo_v8.json (page, ancre, famille, complémentaires) ;
  - sitemap (73 URL) et search-index.json ;
  - hub Réagir et Tous les guides (compteur 62), par lisibilite_v9.py (NEW) ;
  - lien croisé « Panne générale du réseau ou du paiement par carte : voir … » sur cyberattaque (XREF) ;
  - sur la nouvelle page, liens vers cyberattaque, coupure d'électricité, radio à piles et batterie externe.
- sw.js : les guides n'y sont pas précachés, donc rien n'a été ajouté.
- Tests : 320, 390 et 1366 px, avec 0 erreur, 1 H1 et un JSON-LD valide. axe clair et sombre : 0 défaut. Liens valides.
- Convergence : au premier passage, il a fallu 2 exécutions de redesign.py (l'index de recherche est construit avant seo_v8). Depuis, tout est stable.

## 7. Ce qui reste / à trancher
1. **Guides rapides de l'appli** : l'accordéon `.guide-item` contient des consignes de sécurité et reste fermé. Modifier son comportement touche au JS de l'appli. Faut-il l'ouvrir ?
2. **Accueil** : le LCP simulé a pris 0,2 à 0,3 s. Piste : sortir le CSS de l'appli de index.html dans un fichier mis en cache.
3. **Barre du bas** : 12 px. Passer à 14 px imposerait des icônes seules ou 2 lignes.
4. **Bouton de recherche de l'en-tête** : icône seule (avec aria-label). On pourrait y ajouter le mot « Rechercher ».
5. **Temps de lecture de la nouvelle page** : 7 min selon template_v4. Le calcul compte probablement aussi les blocs de maillage.
6. **Révision manuelle** : la liste des 41 FAQ ouvertes vient d'une détection par mots-clés (`SAFE` dans lisibilite_v9.py). Le titre de « L'essentiel » de la nouvelle page est à relire.
7. **H1 sur les onglets de l'appli** : défaut modéré, déjà présent avant v9.

## Fichiers
- **Nouveaux** :
  - `_outils/lisibilite_v9.py` ;
  - `_outils/lisibilite_v9.css` ;
  - `_outils/lisibilite_v9_app.css` ;
  - `panne-numerique-cyberattaque-72h.html` ;
  - `img/cards/panne-numerique-cyberattaque-72h.svg`.
- **Modifiés** :
  - `style.css` (tokens + bloc v9), `_outils/landing.html`, `_outils/landing.css` ;
  - `_outils/redesign.py` et `/home/claude/seo/redesign.py`, `_outils/seo_v8.json`, `_outils/PIPELINE_V4.md` ;
  - `sw.js` (v75), `index.html`, 70 pages par la chaîne, `sitemap.xml`, `search-index.json`.
- **Outils de test** (hors dépôt) : `/home/claude/v9test/`, qui contient fulltest, axe, apptest, seocheck et les captures avant/après.
