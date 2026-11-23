# Rapport refonte v6 : structure et code (23 novembre 2026)

Rien n'est commité ni poussé. Aucune page, URL, fonctionnalité ou clé localStorage existante n'a été supprimée ou renommée. Le texte des guides de risques et d'équipement n'a pas été modifié : les 183 remplacements de `/home/claude/v6_accepted.json` gardent exactement le même statut qu'à HEAD (145 applicables, les 38 qui échouaient déjà échouent toujours, 0 régression).

## Statut par tâche

| # | Tâche | Statut |
|---|---|---|
| 1 | diagnostic-suis-je-pret.html | **CORRIGÉ** |
| 2 | tous-les-guides.html | **CORRIGÉ** |
| 3 | questions-reponses-kit-urgence.html | **CORRIGÉ** |
| 4 | glossaire-preparation-crise.html | **CORRIGÉ** |
| 5 | checklist-kit-urgence-72h.html | **CORRIGÉ** (impression vérifiée en PDF Chrome, pas sur imprimante réelle) |
| 6 | privacy.html | **CORRIGÉ**, avec un point **À VÉRIFIER** (Play Store) |
| 7 | accessibilite.html et mentions-legales.html | **CORRIGÉ** |
| 8 | confidentialite.html | **CORRIGÉ**, avec un point **À VÉRIFIER** (appli Android) |
| 9 | sitemap.xml et robots.txt | **CORRIGÉ** (vérifié, rien à changer) |
| 10 | Hubs des 6 univers | **CORRIGÉ**, avec une limite pour l'outre-mer |
| 11 | sw.js | **CORRIGÉ** (v69) |

### 1. Test « Suis-je prêt ? » (diag.py et pages.js)
- Une question à la fois, avec « Question n sur 10 » et une barre `role=progressbar`. Boutons Précédent et Suivant. Entrée passe à la question suivante. Le focus se place sur chaque nouvelle question.
- Les réponses sont des radios natives. Une réponse manquante affiche un message `role=alert`.
- Le résultat donne un niveau en mots : « Bien préparé », « En bonne voie » ou « Premiers pas ». Il n'affiche plus de pourcentage. Il propose jusqu'à 3 actions, d'abord les « non », puis les « en partie », chacune avec la réponse donnée.
- Liens « Ouvrir la checklist à imprimer » et « Cocher ma liste dans l'appli ». Boutons « Modifier mes réponses » (les réponses sont conservées) et « Recommencer ».
- Rien n'est stocké : le nombre de clés localStorage est identique avant et après le test.
- Sans JavaScript, les 10 questions restent visibles, et un `<noscript>` liste les 10 actions.
- Le mot « score » a été retiré du titre, de la description, de l'introduction, de la FAQ du test et de la FAQ du hub « Anticiper ».

### 2. Tous les guides (hub.py)
- Le champ de recherche est en tête. Les cartes de rendu court sont alignées.
- search.js expose désormais `window.TPSearch` (normalisation, synonymes, score), et pages.js le réutilise sans dupliquer la logique. L'index est enrichi par les questions de search-index.json quand le fichier est disponible.
- Deux rangées de puces `aria-pressed` :
  - Rubrique : les 7 univers ;
  - Public : Familles et enfants, Aînés et handicap, Animaux, En voiture, Outre-mer. Ce sont uniquement des regroupements de pages existantes.
- Un état vide explique quoi faire et propose un bouton d'effacement. Un lien « Tout afficher » apparaît dès qu'un filtre est actif. Le paramètre `?q=` préremplit le champ.
- 61 cartes, sans doublon : le « À lire aussi » qui créait 3 doublons a été retiré, ainsi que le sommaire, remplacé par les puces.
- Les 4 premières images sont en `loading="eager"`, les autres en `lazy`.

### 3. Questions-réponses (post-traitement v6_structure.py)
- Le sommaire est remplacé par une navigation par thème : 6 ancres, chacune avec son nombre de questions.
- Un filtre insensible aux accents gère l'état vide et masque les thèmes sans résultat.
- Un encadré « Appelez le … » est ajouté seulement sur les 3 réponses qui demandent déjà d'appeler. Les numéros sont repris de leur texte : 15 / 17 / 18 / 112, puis 112, puis 15 / 18 / 112.
- Le JSON-LD FAQPage est identique aux 27 questions affichées.

### 4. Glossaire
- Barre alphabétique : `id="lettre-x"` sur le premier `<dt>` de chaque lettre, les lettres absentes sont grisées.
- Filtre des 30 termes. Cliquer une lettre masquée par le filtre efface ce filtre.

### 5. Checklist
- Cases natives ajoutées en JavaScript, sans changer le texte des `<li>`.
- Barre de progression conservée sous la nouvelle clé **`tp_print_checklist_v1`**. Elle est distincte : la page n'avait aucun stockage auparavant.
- Boutons Imprimer, Partager et « Tout décocher » (avec confirmation). Le partage passe par share.js, devenu capable de gérer plusieurs boutons.
- Impression A4 sur 2 pages : en-tête avec l'URL, catégories encadrées sur 2 colonnes et jamais coupées, cases de 5 mm, éléments d'interface masqués.

### 6. privacy.html
- La redirection se fait par `meta refresh 0`, puis par `location.replace` (la page n'a pas de CSP, donc le script en ligne est autorisé), avec en plus un lien visible.
- `robots noindex,follow`, canonical vers confidentialite.html, contenu réduit à un H1 et une phrase.
- Absente du sitemap.
- Elle reste accessible et elle est précachée.
- **À VÉRIFIER** : si la fiche Play Store pointe vers `/privacy.html`, l'examinateur Google arrivera sur la politique en français. Mieux vaut mettre directement `https://tousprets.fr/confidentialite.html` dans la Play Console.

### 7. Accessibilité et mentions légales
- La conformité est déjà annoncée « partielle ». La formulation devient « partiellement conforme au RGAA 4.1 (auto-évaluation, non auditée) ».
- Nouvelle section avec les résultats réels du 23 novembre (axe-core, Playwright, clavier, sans JavaScript) et 2 limites connues de plus.
- Meta descriptions : 152 caractères (accessibilité) et 150 caractères (mentions légales), contre 95 et 56 avant. Les informations de l'éditeur n'ont pas été touchées.

### 8. Confidentialité
Chaque affirmation a été vérifiée dans le code. Corrections :
- « notes » retiré : cette fonction n'existe pas ;
- l'export se fait par un fichier de sauvegarde à restaurer en collant son contenu (Réglages) ; le code et le QR code ne concernent que le groupe de voisinage ;
- la copie hors ligne comprend aussi les pages déjà consultées.

Ajouts :
- un tableau des 21 clés, relevées dans index.html et dans pages.js ;
- « Le test n'enregistre rien » ;
- une section « Tout effacer » : données du site dans le navigateur, effacement des données Android, ou désinstallation. **L'appli n'a pas de bouton « tout effacer »** ;
- « Aucune ressource externe » : vérifié sur les 73 pages et les fichiers JS, aucun `src` ni `href` de ressource externe.

Points confirmés :
- la caméra n'est utilisée que pour le scan, et ses pistes sont arrêtées ;
- le presse-papiers est en écriture seule ;
- aucune géolocalisation, notification, cookie ni appel `fetch` externe.

**À VÉRIFIER** : la phrase « L'application Android … n'envoie aucune statistique » ne peut pas être vérifiée ici, car l'enveloppe Android n'est pas dans le dépôt.

### 9. Sitemap et robots.txt
- 72 `<loc>`, tous uniques, tous en HTML indexable. Le canonical de chaque page correspond exactement à son `<loc>`.
- 40 images, toutes présentes. Le XML est valide. privacy.html n'y figure pas.
- robots.txt est cohérent (`Allow: /` et ligne Sitemap).
- Le post-traitement retire désormais privacy.html du sitemap si elle y réapparaît.

### 10. Hubs (univers.py et redesign.py)
- Cartes homogènes, avec un aperçu court tiré de la meta description existante (première phrase, sinon coupure au mot). Sur mobile, elles passent en format compact horizontal.
- « Réagir » :
  - le groupe « Alerte et danger immédiat » vient en premier (sirène, FR-Alert, confinement, attaque, nucléaire, feu de forêt, inondation, séisme), puis « Les autres situations » ;
  - l'ordre UNIV a été changé en conséquence, et le précédent/suivant des 16 guides suit ce nouvel ordre.
- « S'équiper » : Eau et aliments, Lumière et énergie, Communication, Soins, Chaleur, et Sécurité incendie (pour le détecteur de fumée, qui n'entre dans aucune des 5 familles demandées).
- Outre-mer : 6 cartes, une par page existante. **Limite** : Saint-Martin et Saint-Barthélemy partagent une seule page. Aucune page n'a été inventée.

### 11. sw.js
- `CACHE_VERSION = 'tous-prets-v69'`.
- 6 fichiers critiques, requis en parallèle. 18 fichiers optionnels, mis en cache un par un, chaque échec étant consigné par `console.warn` sans bloquer.
- Nouveaux fichiers précachés : pages.js, diagnostic-suis-je-pret.html, checklist-kit-urgence-72h.html et tous-les-guides.html.
- Test sur une copie du site :
  - sans 8 fichiers optionnels, le service worker est activé avec 16 entrées ;
  - sans style.css, l'installation échoue et l'ancien service worker reste en place.

## Tests réels (Playwright, /usr/bin/google-chrome, http://localhost)
- 73 pages × 6 largeurs (320, 375, 390, 430, 768 et 1366 px), soit **438 chargements** : 0 erreur JavaScript, 0 débordement, 1 H1 partout, 0 JSON-LD invalide.
- 6 521 liens internes et ancres vérifiés : 0 lien mort. audit_v5 : 0 erreur, 0 avertissement.
- **54 / 54 contrôles fonctionnels**, au clic et au clavier :
  - test : tout oui, tout non, mixte, retour arrière puis modification, réponse manquante, clavier, sans JavaScript ;
  - hub : accents, synonymes, puces, combinaison de filtres, état vide, `?q=` ;
  - questions-réponses, glossaire ;
  - checklist : persistance, impression, deux boutons de partage, tout décocher ;
  - redirection privacy, avec et sans JavaScript.
- Appli : 3/3 (7 onglets, ajout d'un membre 1 → 2, persistance après rechargement, 0 erreur JavaScript).
- Hors ligne : 3/3 (cache v69 avec 24 entrées ; accueil, guide visité, test, checklist, tous les guides et confidentialité ; le filtre du hub fonctionne hors ligne).
- file:// : 0 erreur JavaScript sur les pages outils, hors la requête CORS vers search-index, qui est interceptée.
- axe-core 4.14.1, clair et sombre, 28 écrans :
  - 31 nœuds en défaut avant correction ; 0 après ;
  - corrections : bouton « Kit 72 h » de l'en-tête en blanc sur orange, présent sur tout le site (texte passé en #0F2440) ; légendes d'images en thème sombre ; liens de l'encadré secours ; repère de recherche en double.
- Idempotence : `redesign.py` lancé deux fois donne des empreintes md5 identiques. Les générateurs diag, hub et univers suivis de redesign reproduisent exactement l'état livré.

## Fichiers
- **Nouveaux** : `pages.js`, `_outils/v6_structure.py` (branché dans redesign.py après prevnext_v5), ce rapport.
- **Modifiés** :
  - scripts : `search.js`, `_outils/share.js` (source recopiée vers share.js), `sw.js`, `style.css` (bloc v6) ;
  - générateurs : `_outils/diag.py`, `hub.py`, `univers.py`, `redesign.py`, `PIPELINE_V4.md`, recopiés dans `/home/claude/seo` (anciennes versions sauvegardées dans `/tmp/seo_backup`) ;
  - pages : 31 pages HTML régénérées ou post-traitées, dont 16 guides « Réagir » où seul le bloc précédent/suivant change, ainsi que `search-index.json`.

## Points à trancher
1. **Générateurs et texte** : importer `newpages.py` (fait par diag, hub, univers et qa) réécrit 6 pages. Pour kit-urgence-bebe, seul le temps de lecture diffère (4 → 3 min), et je l'ai restauré. En revanche, `qa.py` contient pour questions-reponses un texte plus récent que le HTML publié (commit 7b29401 : « restent », « partout en Europe », « en suivant strictement leur notice »). Je n'ai pas lancé qa.py. Il faut choisir laquelle des deux versions fait foi avant le prochain passage de l'agent quotidien.
2. **URL de confidentialité dans la Play Console** (voir tâche 6).
3. **Statistiques de l'appli Android** : la phrase n'est pas vérifiable ici (voir tâche 8).
4. **Ordre « Réagir »** : le classement entre « urgent » et « autre » est un choix éditorial, à valider (par exemple pour le cyclone, rangé dans « autres » parce qu'il est annoncé à l'avance).
