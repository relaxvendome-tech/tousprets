# Corrections apportées (phases B, C, D)

Toutes les modifications de pages passent par **`_outils/seo_v8.py`**, un post-traitement idempotent branché en dernier dans `redesign.py`, après `brand_v7`. La même liste est copiée dans `/home/claude/seo/redesign.py`. Ses données sont dans **`_outils/seo_v8.json`**. Je n'ai relancé ni `qa.py` ni les générateurs. Deux passages successifs de `redesign.py` donnent des empreintes md5 identiques sur les 289 fichiers (voir TESTS.md).

Fichiers modifiés hors pages : `sitemap.xml` (régénéré), `robots.txt`, `style.css` (bloc « v8 » en fin de fichier), `sw.js` (`CACHE_VERSION = 'tous-prets-v71'`), `_outils/redesign.py` et sa copie dans `/home/claude/seo/`.
Nouveaux fichiers : `_outils/seo_v8.py`, `seo_v8.json`, `seo_v8_audit.py` (audit en lecture seule), `seo_v8_rapport.py` (notes et CSV) et le dossier `_outils/seo_v8/`.

Aucune page n'a été supprimée ni créée, et aucune URL renommée. Aucune clé localStorage n'a changé, aucune consigne de sécurité n'a été touchée, et aucune ressource externe n'a été ajoutée.

## Phase B : fondations techniques

| # | Correction | Pages |
|---|---|---|
| B1 | Sitemap régénéré à chaque passage : seulement les pages indexables dont la canonical est leur propre URL (privacy.html est exclue d'office, car elle est en noindex avec meta refresh). Ordre conservé. `lastmod` = `git log -1 --format=%cs` du fichier. Images : la photo du héros et les infographies PNG originales, sans doublons ni WebP (40 → 35 entrées). | sitemap.xml |
| B2 | Pas de sitemap index : 72 URL et 35 images tiennent largement dans un seul fichier (limite : 50 000). Le scinder n'apporterait rien. | — |
| B3 | robots.txt : ajout de `Disallow: /_outils/`. Le dossier de travail est publié par GitHub Pages (`.nojekyll`), il n'est lié nulle part et aucune page n'en charge de ressource (vérifié). CSS, JS et images restent autorisés. | robots.txt |
| B4 | Canonical : déjà absolues et correctes sur les 72 pages publiques. `og:url` est réaligné sur la canonical. | 72 |
| B5 | JSON-LD de l'accueil réécrit : WebSite avec SearchAction (`tous-les-guides.html?q=`, testé : préremplit le champ et filtre), Organization (logo ImageObject et mention « Ce n'est pas un service de l'État ») et WebApplication exact (`operatingSystem` « Web », gratuit, `featureList` vérifiable). Retrait de `keywords` et de `screenshot` (og-image.png n'est pas une capture d'écran). Aucune note ni aucun avis. | index.html |
| B6 | Article : `headline` = H1, `description` = meta description, `datePublished` = date du premier commit, `dateModified` = date du dernier commit qui a modifié le texte éditorial (hors navigation et maillage), `author` et `publisher` = Organization « Tous prêts » (`@id` #org). | 60 pages (guides et pages éditoriales) |
| B7 | CollectionPage au lieu d'Article pour les 7 hubs (tous-les-guides et les 6 pages rubriques). | 7 |
| B8 | BreadcrumbList reconstruit à partir du fil d'Ariane visible (60 étaient incohérents). Sur kit-de-survie-72h, le niveau qui renvoyait à la page elle-même est retiré du fil visible et du JSON-LD. | 71 |
| B9 | Suppression des doublons de schéma (contrôle par type) : aucun doublon restant. Les 10 ImageObject de questions-réponses décrivent 10 visuels différents ; ils sont conservés. | — |
| B10 | `meta keywords` supprimée (ignorée par Google). | 72 |
| B11 | Tous les guides : le filtre est présent dans le HTML (et non plus révélé par JS), et masqué sans JS par `<noscript><style>`. Résultat : CLS 0,111 → 0. | tous-les-guides.html |
| B12 | Accueil : `<link rel="preload">` de l'image du héros (LCP). Aucun gain mesurable en simulation (voir PERFORMANCE.md), mais sans effet négatif. | index.html |
| B13 | Contraste du titre « À ne surtout pas faire » : #C0392B → #B8352A en thème clair (4,49 → 4,85:1). | style.css |

## Phase C : éditorial

| # | Correction | Pages |
|---|---|---|
| C1 | Titles : 8 corrigés (7 hors 30–62 caractères, plus la checklist pour viser « checklist gratuite »). Les 64 autres sont conservés, car valides, concrets et cohérents avec le H1 : le brouillon Gemini perdait souvent des précisions utiles. Détail de l'origine de chaque title dans `seo_v8.json` (`source_title`) et TABLEAU_SEO.csv. | 8 |
| C2 | Descriptions : 14 corrigées. 12 étaient hors 120–160 caractères (6 propositions Gemini retenues telles quelles, 6 raccourcies à la main). L'accueil et la checklist mettent en avant leurs vrais atouts : checklist interactive et gratuite, quantités selon le foyer, hors ligne, aucune donnée envoyée. La mention « (guide officiel) » de l'accueil a été retirée, car elle était ambiguë. | 14 |
| C3 | og:title, og:description, twitter:title, twitter:description et twitter:image alignés sur le title, la description et l'og:image. | 72 |
| C4 | Date visible « Mis à jour le » = `dateModified` réelle : 21 pages passent du 19 au 23 novembre 2026, car leur texte a changé ce jour-là. « Vérifié le » n'est plus recopié de la date de mise à jour. Il vaut le 23 novembre seulement si le texte actuel vient d'un commit de vérification (5d6783d « 183 corrections vérifiées » ou 7b29401) ; sinon, la date d'origine (19 novembre) est conservée. C'est le cas pour 6 pages : attaque terroriste, confinement, cyberattaque, entraide, kit-urgence-72h-gouvernement et tensions internationales. | 67 |
| C5 | Accueil, section statique `seo-about` réécrite. Elle est lisible sans JS (test). Elle contient : le fonctionnement de la checklist en 3 étapes, la confidentialité, l'usage hors ligne, les 20 éléments du kit en 6 catégories (générés depuis `checklist-kit-urgence-72h.json`, la même source que la checklist imprimable), les liens vers la liste complète, l'eau, les aliments, la famille, la coupure, l'inondation et les questions, ainsi que la source et la mention « pas un service de l'État ». L'accroche du héros devient « Kit d'urgence 72 h · checklist gratuite pour tous les foyers ». | index.html |
| C6 | H1 et Hn : déjà conformes (1 H1, aucun saut). Le H1 de l'accueil, « Être prêt change tout. », est un slogan peu explicite : je l'ai laissé tel quel, c'est un point à trancher (RESTANT.md). | — |
| C7 | Réponse directe en tête : présente partout (chapô `lead` et bloc « L'essentiel » sur les guides). Je n'ai rien ajouté de redondant. | — |
| C8 | ALT : les 30 photos de héros reçoivent une description de ce qu'elles montrent, établie en regardant chaque image, sans mot-clé et sans chiffre. Les pictogrammes SVG des héros sans photo passent en `alt=""`, car ils sont décoratifs et le H1 suit. La légende ImageObject reprend l'ALT. Le héros de l'accueil garde `alt=""`. | 30 photos + 37 pictogrammes |

## Phase D : architecture et maillage

| # | Correction | Pages |
|---|---|---|
| D1 | Bloc « Guides complémentaires » (`<nav id="guides-compl">`, H2, 3 à 5 liens aux ancres descriptives) sur 57 guides. Il est placé avant « À lire aussi », sans aucun lien en double avec ce bloc, le précédent/suivant ou le fil d'Ariane. Sélection manuelle par page dans `seo_v8.json`, complétée par la famille éditoriale seulement s'il reste moins de 3 liens. | 57 |
| D2 | Chaque guide de risque renvoie vers l'appli ou la checklist, vers la page eau et vers un équipement pertinent (par exemple, pour l'inondation : eau, radio à piles, purifier l'eau, sac de secours). Vérification automatique : 0 exception. | 22 |
| D3 | Pages peu liées renforcées : Guyane 2 → 4, La Réunion 2 → 4, Saint-Martin 2 → 6, kit 7 jours 2 → 7, tensions internationales 2 → 3 liens contextuels entrants (voir LIENS_INTERNES.md). | — |
| D4 | Aucune page orpheline ; toutes les pages publiques sont à 2 clics maximum de l'accueil. | — |

## Ce que je n'ai pas fait, volontairement

- Aucun ajout de HowTo : il n'y en avait aucun, et Google ne l'affiche plus.
- Aucun texte rallongé artificiellement, aucun mot-clé ajouté dans le corps des guides.
- Pas d'AVIF : gain d'environ 10 % seulement, à qualité égale (voir PERFORMANCE.md).
- Aucune nouvelle page : les propositions sont dans RESTANT.md et PLAN_90_JOURS.md.
