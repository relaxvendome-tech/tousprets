# Plan de progression SEO sur 90 jours

Principes : aucune position n'est garantie. On améliore d'abord les pages existantes, on ne crée une page que si elle a une valeur propre, et on ne fabrique aucune donnée ni aucun lien artificiel. Chaque action se mesure dans Search Console (SEARCH_CONSOLE.md).

## Jours 1 à 14 : publier, vérifier, mesurer

| Action | Responsable | Mesure de succès |
|---|---|---|
| Relire le diff v8, commit, push | éditeur | site en ligne, `sw.js` en v71 |
| Étape 0 de SEARCH_CONSOLE.md (curl : 200, 301 https, 404) | éditeur | tous les codes attendus |
| Propriété Domaine, sitemap, inspection des 9 URL de priorité 1 et 2 | éditeur | sitemap « Opération effectuée », 72 URL détectées |
| Bing : import depuis Search Console, une notification IndexNow | éditeur | sitemap importé |
| Test des résultats enrichis sur 4 URL | éditeur | fil d'Ariane, Article et Organization valides |
| Trancher les points 1 à 7 de RESTANT.md | éditeur | décisions notées |

## Jours 15 à 45 : qualité et confiance

| Action | Pourquoi |
|---|---|
| Charger jsQR et qrcode à la demande dans l'appli | gain de performance mobile le plus important de l'accueil |
| Enrichir `sources.html` : pour chaque source, ce qu'elle couvre, son lien direct et sa date de consultation | page la plus faible (81/100) et la plus importante pour la confiance |
| Créer une page Contact (adresse dédiée au projet, délai de réponse, politique de correction) | demandée par le cahier des charges (§ 7), absente aujourd'hui |
| Relecture humaine datée des consignes de sécurité des guides de risque, contre les sources officielles, puis mise à jour de `date_verifiee` | c'est le seul contrôle de la grille que je n'ai pas pu faire (2 points sur chaque page) |
| Créer `404.html` (recherche et liens vers le kit et les situations d'urgence) | expérience utilisateur |
| Premier bilan Performances : pages à fortes impressions et faible CTR → retoucher le title ou la description (en mettant à jour `seo_v8.json`) | CTR |

## Jours 46 à 90 : contenus utiles et notoriété

| Action | Condition |
|---|---|
| Rédiger et vérifier « Coupure d'eau : que faire ? » et « Entretenir et faire tourner son kit » (RESTANT.md, propositions 1 et 4) | validation éditeur ; sources officielles citées ; ajout dans `UNIV` (redesign.py), dans `seo_v8.json` et dans le maillage |
| « Se chauffer sans électricité, sans danger » (proposition 2) | relecture des consignes contre les sources officielles avant publication |
| Section « Sans pastilles » dans purifier-eau, section rangement dans la page famille/appartement, section « checklist interactive ou PDF » dans kit-de-survie-gouvernement-pdf | enrichissement de l'existant, pas de nouvelle URL |
| Lancer la stratégie de notoriété (NOTORIETE.md) : 10 premiers contacts personnalisés | aucun lien acheté ni échangé |
| Bilan à 90 jours : pages indexées, requêtes nouvelles, clics par page, comparaison des notes de TABLEAU_SEO.csv (`python3 _outils/seo_v8_audit.py . /tmp/a.json && python3 _outils/seo_v8_rapport.py /tmp/a.json`) | rapport mensuel |

## Indicateurs suivis (sans objectif chiffré inventé)

- Pages indexées / 72.
- Impressions et clics par univers (kit, risques, foyer, équipement, outre-mer).
- Nombre de requêtes distinctes qui génèrent des impressions.
- CTR moyen des 10 pages qui ont le plus d'impressions.
- Nombre de domaines référents réels (rapport « Liens » de Search Console).
- Core Web Vitals réels, quand ils sont disponibles.
