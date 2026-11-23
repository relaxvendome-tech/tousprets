# Données structurées (JSON-LD) après v8

Un seul bloc `<script type="application/ld+json">` par page (`@graph`). Le bloc est généré ou corrigé par `seo_v8.py`.

## Inventaire (73 pages)

| Type | Nombre | Pages | Remarques |
|---|---|---|---|
| WebSite | 1 | accueil | `@id` #site, `publisher` → #org, `SearchAction` vers `tous-les-guides.html?q={search_term_string}` |
| Organization | 1 | accueil | `@id` #org, logo ImageObject 512×512, description « initiative citoyenne indépendante… Ce n'est pas un service de l'État » |
| WebApplication | 1 | accueil | sous-type de SoftwareApplication. Gratuit (`offers` 0 EUR, `isAccessibleForFree`), `applicationCategory` LifestyleApplication, `operatingSystem` « Web », `featureList` limitée aux fonctions vérifiées dans le code. **Sans `aggregateRating` ni `review`** : il n'en existe pas. |
| Article | 60 | guides et pages éditoriales | `headline` = H1, `datePublished` / `dateModified` réelles (git), `author` = `publisher` = Organization « Tous prêts », `image` (photo sous licence CC0 avec crédit, ou image de partage par défaut og-image.png pour les pages sans photo) |
| CollectionPage | 7 | tous-les-guides et les 6 pages rubriques | même jeu de propriétés, `name` = H1 |
| WebPage | 4 | sources, mentions légales, confidentialité, accessibilité | `dateModified` |
| BreadcrumbList | 71 | toutes les pages avec un fil d'Ariane | reconstruit depuis le fil visible, positions 1…n, aucune URL en double, le dernier élément = la canonical |
| FAQPage | 65 | guides | questions identiques aux `<summary>` visibles (contrôle automatique : 0 écart) |
| ItemList | 1 | kit-de-survie-72h | contenu du kit |
| ImageObject | 10 | questions-reponses | 10 visuels distincts (pas des doublons) |

Doublons de schéma : **0**. JSON invalide : **0** (contrôle par JSON.parse sur 146 chargements dans Chrome et en Python).

## Choix et points d'attention

1. **FAQPage (65 pages)** : je l'ai conservé, car il est valide et cohérent avec le contenu visible, et les moteurs le lisent. Mais depuis août 2023, Google n'affiche plus le résultat enrichi FAQ que pour des sites gouvernementaux ou de santé faisant autorité. Tous prêts n'en fait pas partie, et ne doit pas se présenter comme tel. **Il ne faut donc attendre aucun résultat enrichi FAQ.** Le garder ne présente aucun risque. Le supprimer allégerait un peu les pages : c'est à trancher.
2. **HowTo** : il n'en existe aucun sur le site et je n'en ai pas ajouté. Google ne l'affiche plus en résultat enrichi depuis septembre 2023.
3. **SearchAction** : la recherche `?q=` fonctionne (test Playwright : `?q=radio` préremplit le champ et filtre 4 cartes sur 61). Le balisage est donc exact. Google a cependant retiré l'affichage de la « sitelinks search box » fin 2024 : ce balisage ne produira probablement aucun affichage particulier.
4. **Dates** :
   - `datePublished` = date du premier commit du fichier : 28 pages au 19 novembre 2026, 45 au 23 novembre 2026.
   - `dateModified` = date du dernier commit qui a modifié le texte éditorial, hors navigation, maillage, fil d'Ariane et blocs automatiques : 23 novembre 2026 pour toutes les pages.
   - Ces dates sont stockées dans `seo_v8.json`. Il faudra les mettre à jour lors d'une vraie modification de texte (voir RESTANT.md, point « dates »).
5. **Auteur** : l'auteur est l'Organization « Tous prêts ». Aucune personne, aucun expert et aucune qualification n'ont été inventés.
6. **Images d'Article** : le crédit (`creditText`, `creator`) et la licence CC0 viennent de `img/photos/credits.json`. La légende reprend l'ALT descriptif.
7. **Pas de LocalBusiness, Review, Rating, Event, GovernmentService** : rien de tout cela ne correspond à la réalité du site.

## Validation officielle à faire (pas d'accès réseau ici)

Je n'ai pas pu lancer les outils Google depuis cet environnement. À faire après publication :
1. Test des résultats enrichis (https://search.google.com/test/rich-results) sur l'accueil, kit-de-survie-72h.html, inondation-que-faire.html et tous-les-guides.html. Résultats attendus : fil d'Ariane, Article et Organization valides. FAQ peut apparaître « valide » mais ne sera pas affiché.
2. Schema Markup Validator (https://validator.schema.org) sur les mêmes URL, pour vérifier les types non reconnus par Google : WebApplication, CollectionPage.
3. Dans Search Console, rapports « Améliorations » > Fils d'Ariane, à suivre 2 à 4 semaines après la publication.
