# Google Search Console et Bing Webmaster Tools : procédure

Je n'ai aucun accès à Search Console ni à Bing depuis cet environnement. **Rien n'a été soumis ni inspecté, et aucune indexation n'est confirmée.** Ce document est une procédure à suivre après la publication de la v8 (commit et push vers GitHub Pages).

## Étape 0 : vérifier la publication (5 min, depuis un terminal)

```
curl -sI https://tousprets.fr/ | head -1                    # attendu : HTTP/2 200
curl -sI http://tousprets.fr/ | grep -i location            # attendu : https://tousprets.fr/
curl -sI https://www.tousprets.fr/ | grep -i location       # attendu : https://tousprets.fr/ (si le www est configuré)
curl -sI https://tousprets.fr/inondation-que-faire.html | head -1   # 200
curl -sI https://tousprets.fr/page-inexistante | head -1    # 404
curl -s https://tousprets.fr/robots.txt
curl -s https://tousprets.fr/sitemap.xml | grep -c '<url>'  # 72
curl -s https://tousprets.fr/sw.js | grep CACHE_VERSION     # tous-prets-v71
```

## Étape 1 : propriété

1. https://search.google.com/search-console → « Ajouter une propriété » → type **Domaine** : `tousprets.fr`. Ce type couvre http, https, www et non-www.
2. Ajouter l'enregistrement **TXT** fourni par Google dans la zone DNS du registrar, puis cliquer sur « Valider ». La propagation peut prendre de quelques minutes à quelques heures.
3. Si une propriété « Préfixe d'URL » existe déjà, la garder : les données ne sont pas fusionnées.

## Étape 2 : sitemap

Menu **Sitemaps** → saisir `sitemap.xml` → Envoyer. Contrôler ensuite que l'état est « Opération effectuée » et qu'il y a **72 pages détectées**. Les 35 images sont déclarées dans le même fichier ; elles ne sont pas comptées comme des pages.

## Étape 3 : inspection des URL prioritaires

Pour chaque URL : **Inspection de l'URL** → « Tester l'URL en direct » → vérifier « L'URL est disponible pour Google », la canonical sélectionnée par Google (doit être l'URL elle-même), le rendu (capture) et les données structurées détectées. Ne cliquer sur **« Demander l'indexation »** que pour ces URL, **une seule fois chacune**, après publication. Pas d'automatisation : le quota est limité et c'est inutile.

| Priorité | URL | Pourquoi |
|---|---|---|
| 1 | https://tousprets.fr/ | title, description, JSON-LD et texte statique modifiés |
| 1 | https://tousprets.fr/checklist-kit-urgence-72h.html | title et description modifiés |
| 1 | https://tousprets.fr/kit-de-survie-72h.html | page pivot du kit, fil d'Ariane corrigé |
| 1 | https://tousprets.fr/tous-les-guides.html | hub, CollectionPage, CLS corrigé |
| 2 | https://tousprets.fr/combien-eau-stocker-par-personne.html | cible de maillage de tous les guides de risque |
| 2 | https://tousprets.fr/que-mettre-dans-un-kit-d-urgence.html | description modifiée, risque de cannibalisation à surveiller |
| 2 | https://tousprets.fr/kit-urgence-72h-gouvernement.html | title modifié |
| 2 | https://tousprets.fr/coupure-electricite-que-faire.html | requête à fort potentiel |
| 2 | https://tousprets.fr/inondation-que-faire.html | requête à fort potentiel |
| 3 | https://tousprets.fr/tempete-que-faire.html, vague-de-froid-que-faire.html, cyberattaque-que-faire.html, cyclone-que-faire.html | descriptions modifiées |
| 3 | https://tousprets.fr/kit-urgence-guyane.html, kit-urgence-la-reunion.html, kit-urgence-martinique.html, kit-urgence-voiture.html | descriptions modifiées, pages auparavant peu liées |
| 3 | https://tousprets.fr/accessibilite.html, mentions-legales.html, anticiper-s-entraider.html, plan-familial-mise-en-surete.html, attaque-terroriste-que-faire.html | titles modifiés |

Les autres pages seront recrawlées naturellement grâce au sitemap et au maillage.

## Étape 4 : suivi de l'indexation (hebdomadaire les 4 premières semaines)

- **Indexation > Pages** :
  - nombre de pages « Indexées » (objectif : 72) ;
  - lire chaque motif d'exclusion. « Explorée, actuellement non indexée » ou « Détectée, actuellement non indexée » sont normaux pour un site jeune. « Page en double sans URL canonique sélectionnée par l'utilisateur » doit rester à 0. privacy.html doit apparaître en « Exclue par la balise noindex » : c'est voulu.
- **Paramètres > Statistiques sur l'exploration** : erreurs serveur ou DNS, temps de réponse.
- **Améliorations** : fils d'Ariane (71 attendus). FAQ peut apparaître ; c'est sans effet d'affichage.
- **Expérience > Signaux Web essentiels** : données réelles dès qu'il y a assez de trafic.

## Étape 5 : performances de recherche (à partir de la 3e semaine)

**Performances > Résultats de recherche**, cocher Clics, Impressions, CTR et Position.
1. Onglet **Requêtes** : exporter chaque mois et comparer avec la colonne « requête principale » de TABLEAU_SEO.csv.
2. Onglet **Pages** : repérer les pages à fortes impressions et faible CTR (< 2 % en position < 10). Leur title ou leur description est à retravailler.
3. **Cannibalisation** : filtrer « Requête contient : kit », puis l'onglet Pages. Si kit-de-survie-72h et que-mettre-dans-un-kit-d-urgence se partagent les mêmes requêtes avec des positions qui alternent, voir RESTANT.md, point 4.
4. **Pertes** : utiliser « Comparer » sur 28 jours contre les 28 jours précédents, onglet Pages, trier par différence de clics. Toute page en baisse de plus de 30 % est à inspecter (indexation, canonical, concurrence).
5. Ne pas tirer de conclusion sur moins de 4 semaines de données.

## Bing Webmaster Tools

1. https://www.bing.com/webmasters → « Importer depuis Google Search Console ». Cela importe les sites vérifiés et les sitemaps, sans nouvelle vérification DNS. Sinon, vérifier par enregistrement CNAME ou TXT.
2. **Sitemaps** → soumettre `https://tousprets.fr/sitemap.xml` (ou vérifier qu'il a bien été importé).
3. **IndexNow est déjà en place** : deux fichiers de clé sont à la racine (`aea1717efb494432bd8e77addca31ca4.txt` et `aedc9fa8342fb41dae2eeebaf120a911.txt`, commit « IndexNow key »). Après publication de la v8, il suffit de notifier **une fois** les URL modifiées, par exemple les priorités 1 et 2 ci-dessus. Pas de notifications répétées.
4. Bing fournit aussi un rapport SEO automatique (« Recommandations ») : utile pour recouper l'audit.
