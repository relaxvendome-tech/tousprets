# Rapport v13 : technique et confiance (23 novembre 2026)

Rien n'est commité ni poussé. Aucune clé localStorage ni aucun texte du corps des pages kit-*, outre-mer et kit-7-jours n'a été modifié. Tous les changements de rendu passent par `_outils/v13.py`, dernier maillon de `redesign.py`, avec une copie dans `/home/claude/seo/`.

## 1. Pages et fichiers modifiés

| Fichier | Avant | Après |
|---|---|---|
| `.nojekyll` | présent : `_outils/` (scripts, rapports, JSON) servi publiquement | supprimé |
| `_config.yml` (nouveau) | — | Jekyll exclut `_outils/` et tout ce qui commence par `_` ou `.` ; `include: .well-known` (assetlinks.json reste servi) ; `exclude: README.md, img/photos/credits.json` |
| `robots.txt` | `Disallow: /_outils/` (révélait le dossier) | ligne retirée |
| `index.html` (via `landing.html` et v13.py) | animation fadeIn à l'ouverture ; vignettes en 960 px ; famille après les guides ; « Voir mon niveau de préparation » | aucune animation au chargement (rétablie au premier clic) ; vignettes 480 px en `srcset` ; ordre : kit 72 h → famille → risques et réflexes → confidentialité → sources ; lien « Suis-je prêt ? » à côté de « Découvrir les bons réflexes » |
| `img/photos/480/` (nouveau) | — | 14 vignettes WebP, 218 Ko au total (tempête : 197 → 41 Ko) |
| `charte-editoriale.html` | — | section « Journal des corrections » : 7 entrées datées, tirées de `git log` |
| 74 pages avec GoatCounter | le script comptait aussi dans l'appli Android | aucun comptage sur `appassets.androidplatform.net`, comme l'annonce confidentialite.html |
| `style.css` | les boutons du héros (`.hero-cta noprint`) restaient visibles à l'impression | bloc v13 `@media print` |
| `sw.js` | `tous-prets-v80` | `tous-prets-v81` |
| `_outils/redesign.py`, `PIPELINE_V4.md` | — | v13.py branché après droits_v11.py |

Vérifications faites pour Jekyll :
- aucun fichier publié ne commence par un front matter `---` ;
- aucun ne contient `{{` ou `{%` ;
- sans front matter, Jekyll copie les HTML tels quels ;
- aucune page ne référence `_outils/`, sauf dans deux commentaires CSS ;
- les fichiers utiles restent servis : `CNAME`, `.well-known/assetlinks.json`, les deux `.txt` de vérification, `checklist-kit-urgence-72h.json/.csv` (données ouvertes), `*.LICENSE`, `LICENSE`, `manifest.json`, `search-index.json`, `sitemap.xml` ;
- `credits.json` n'est lié par aucune page ;
- `README.md` serait converti en page par le plugin optional-front-matter de GitHub Pages ;
- la chaîne de génération lit `_outils/` en local et ne dépend pas du site.

## 2. Lighthouse mobile (accueil, 3 passages alternés, médiane)

| | Perf. | LCP | FCP | TBT | CLS | Poids |
|---|---|---|---|---|---|---|
| Avant (HEAD) | 84 (84/86/84) | 3,7 s | 1,8 s | 230 ms | 0 | 962 Ko |
| Après | **93** (93/93/95) | **2,9 s** | 1,7 s | 150 ms | 0 | **544 Ko** |

Accessibilité, bonnes pratiques et SEO restent à 100.

Cause trouvée : l'animation `fadeIn` (opacité 0 → 1) de `.screen.active` retardait le LCP après l'événement load. Le LCP observé passait de 190 à 376 ms, et Lighthouse imputait alors toutes les images au LCP.

Pistes mesurées puis écartées :
- CSS de l'appli (37 Ko) dans un fichier externe : médiane 90, LCP 3,4 s, moins bien que le CSS en ligne, car la feuille externe bloque l'affichage à la première visite ;
- JS en ligne (115 Ko) dans un fichier différé : résultats instables (83/83/99, LCP 4,4 s).

## 3. Tests chiffrés (état final)

- **Pages** : 75 pages × 8 largeurs (320 à 1920 px) = 600 chargements, plus 75 chargements à 640 px (zoom 200 %). 0 erreur JS, 0 débordement, 1 H1 par page, 0 JSON-LD invalide.
- **Liens** : 6 967 références internes (liens, ancres, src, srcset), 0 morte. audit_v5 : 0 erreur, 0 avertissement.
- **axe-core** : 16 écrans × (320, 640 ×2, 1366 px) × (clair, sombre), avec réduction des animations, soit 96 audits.
  - 0 défaut sérieux ou critique.
  - 18 alertes « modérées » `page-has-heading-one` : sur les onglets 2, 4 et 5 de l'appli, le H1 de l'accueil est masqué. Ce défaut existait déjà.
- **Réduction des animations** : durée 0,01 ms. Aucune animation résiduelle sur un guide.
- **Appli** (`/home/claude/v13test/apptest13.py`) : 33/33.
  - Premier écran : H1 conservé, « kit d'urgence 72 h » sous le titre, lien « Suis-je prêt ? » visible, un seul bouton principal.
  - Navigation et données : 7 onglets ; ajout d'un membre ; quantités ; persistance après rechargement.
  - Sauvegarde : export JSON, effacement puis import à l'identique.
  - Impression : `window.print` appelé une fois ; 18 lignes imprimées, sans en-tête ni boutons.
  - Hors ligne : accueil, guide et checklist.
  - Mise à jour du service worker de v81 à v82 : un seul cache restant, localStorage identique, membres conservés.
  - 0 erreur JS. Clés : `checklist_kit72, food_stock_v1, profiles_v1, theme_v1`, inchangées.
- **Idempotence** : deux passages de `redesign.py` donnent des md5 identiques sur 356 fichiers.

## 4. Confiance

- **Journal des corrections** : il couvre les 7 commits de correction de contenu (183 corrections, 25 consignes dont le 114, sécurité alimentaire et bébé, hébergeur, titre altéré, droits d'auteur). **Aucun commit ne concerne les montants d'argent liquide** : rien n'a été inventé. Si cette correction est faite par une autre IA, ajoutez une ligne à `JOURNAL` dans v13.py.
- **Nature des informations (4 b)** : non appliqué.
  - `essentiels.json` n'indique pas l'origine de chaque consigne. Une étiquette « Consigne officielle » automatique serait donc invérifiable.
  - 68 pages ont déjà la mention « Informations pratiques, sources officielles (…) ».
  - Proposition : ajouter un champ `source` (URL officielle) par consigne dans `essentiels.json`, puis afficher « Consigne officielle (source) » seulement quand ce champ est rempli.
- **Cohérence (4 c)** :
  - confidentialite, aide-application et mentions-legales concordent : GoatCounter sans cookie, stockage local, GitHub Pages, pas de compte ni de publicité. accessibilite.html n'en parle pas, ce qui est normal.
  - privacy.html redirige bien (refresh, `location.replace`, noindex).
  - Seul écart corrigé : la phrase « L'application Android n'envoie aucune statistique » n'était pas garantie par le code.

## 5. Non résolu

1. **Build Jekyll** : il n'a pas pu être testé en local, car rubygems est bloqué par le proxy. Après publication, vérifier :
   - `/_outils/LISEZMOI.md` → 404 ;
   - `/.well-known/assetlinks.json` → 200 ;
   - `/README.html` → 404 ;
   - aucune page modifiée.
2. **H1 masqué dans les onglets de l'appli** : alerte axe modérée. La correction touche le JS de navigation.
3. **Ordre de l'accueil** : les réflexes viennent après les risques, dans « Les guides principaux ». L'entraide est dans la section famille. Une section entraide dédiée n'existe pas.
4. **Poids de l'accueil** : index.html pèse toujours 218 Ko, dont 115 Ko de JS en ligne. Il faudra un vrai découpage en modules, testé onglet par onglet.
5. **Variabilité Lighthouse** : le processeur est partagé avec d'autres agents, ce qui donne ±4 points d'un passage à l'autre.

## 6. Feuille de route sur 90 jours

- **J+7** :
  - publier ;
  - contrôler les URL du point 5.1 ;
  - Search Console : vérifier que `_outils/` disparaît de l'index (demande de suppression si besoin) ;
  - Lighthouse sur le site réel (PageSpeed Insights, données terrain CrUX quand elles existent).
- **J+30** :
  - ajouter un champ `source` dans `essentiels.json` et les étiquettes « Consigne officielle » ;
  - H1 visible pour chaque onglet de l'appli (titre de l'écran actif) ;
  - mettre à jour le journal des corrections à chaque correction de fond.
- **J+45** :
  - sortir le JS de l'appli en modules différés, avec des tests appli à chaque étape (l'objectif est un LCP inférieur à 2,5 s de façon stable) ;
  - vignettes 480 px pour « Tous les guides ».
- **J+60** :
  - tests avec lecteurs d'écran (NVDA, TalkBack, VoiceOver) ;
  - audit RGAA par un tiers ;
  - mise à jour de la déclaration d'accessibilité.
- **J+90** :
  - relecture humaine des consignes de sécurité par un professionnel (secourisme ou sécurité civile) ;
  - section entraide dédiée sur l'accueil ;
  - bilan GoatCounter pour prioriser les guides.
