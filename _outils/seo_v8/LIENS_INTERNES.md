# Liens internes (après v8)

Mesure : `_outils/seo_v8_audit.py` (liens `href` vers des pages .html du site). « Contextuels » = liens dans `<main>` hors fil d'Ariane et hors précédent/suivant ; « tous » inclut l'en-tête, le menu et le pied de page.

## Synthèse

- Pages orphelines (aucun lien entrant) : **0** parmi les 72 pages publiques (privacy.html, redirection noindex, n'est volontairement liée de nulle part).
- Profondeur depuis l'accueil : {0: 1, 1: 46, 2: 25} (clics) ; toutes les pages publiques sont à 2 clics maximum.
- Pages avec moins de 3 liens contextuels entrants : avant 8, après 3 (accessibilite.html, mentions-legales.html, tous-les-guides.html) : pages légales et hub liés depuis le pied de page et le menu de toutes les pages.
- Blocs « Guides complémentaires » posés : **57** (3 à 5 liens, ancres descriptives, jamais en double avec « À lire aussi », le précédent/suivant ou le fil d'Ariane ; sélection manuelle dans `seo_v8.json`, complétée par la famille éditoriale seulement s'il reste moins de 3 liens).
- Chaque guide de risque (rubrique Réagir et Outre-mer) renvoie vers l'appli ou la checklist (boutons du héros), vers la page eau et vers au moins une page d'équipement (contrôle automatique : 0 exception).
- Fil d'Ariane : kit-de-survie-72h.html se citait elle-même (rubrique = page) : niveau retiré. BreadcrumbList JSON-LD reconstruit depuis le fil visible sur 71 pages (60 incohérents avant : niveau « rubrique » absent).

## Tableau par page

| Page | Entrants contextuels avant → après | Sortants contextuels | Profondeur | Guides complémentaires |
|---|---|---|---|---|
| accessibilite.html | 1 → 1 | 0 | 1 | — |
| accident-nucleaire-iode.html | 5 → 7 | 14 | 1 | combien-eau-stocker-par-personne, radio-a-piles-kit-urgence, inondation-que-faire, seisme-que-faire, cyclone-que-faire |
| aliments-sans-cuisson-kit-urgence.html | 9 → 18 | 11 | 1 | kit-urgence-bebe, kit-7-jours-strategie-europeenne-72h, kit-urgence-72h-gouvernement, checklist-kit-urgence-72h, que-mettre-dans-un-kit-d-urgence |
| anticiper-s-entraider.html | 3 → 3 | 8 | 2 | — |
| arnaque-kit-urgence-gratuit.html | 4 → 8 | 12 | 2 | kit-de-survie-gouvernement-pdf, fr-alert-que-faire, cyberattaque-que-faire, kit-de-survie-72h-pas-cher |
| attaque-terroriste-que-faire.html | 3 → 5 | 12 | 2 | fr-alert-que-faire, trousse-de-secours-kit-urgence, plan-familial-mise-en-surete, combien-eau-stocker-par-personne, signal-alerte-sirene |
| batterie-externe-station-electrique.html | 3 → 8 | 11 | 2 | groupe-electrogene-securite, kit-urgence-handicap, radio-a-piles-kit-urgence, lampe-frontale-lanterne-kit-urgence, couverture-de-survie |
| canicule-que-faire.html | 8 → 10 | 13 | 1 | combien-eau-stocker-par-personne, trousse-de-secours-kit-urgence, kit-urgence-animaux |
| charte-editoriale.html | 67 → 67 | 5 | 1 | — |
| checklist-kit-urgence-72h.html | 67 → 67 | 13 | 1 | aliments-sans-cuisson-kit-urgence, kit-urgence-72h-famille-appartement-voiture, sac-de-secours, kit-de-survie-72h-pas-cher, kit-7-jours-strategie-europeenne-72h |
| combien-eau-stocker-par-personne.html | 15 → 41 | 13 | 1 | coupure-electricite-que-faire, kit-7-jours-strategie-europeenne-72h, kit-urgence-72h-gouvernement, checklist-kit-urgence-72h, sac-de-secours |
| comprendre-s-informer.html | 7 → 7 | 10 | 1 | — |
| confidentialite.html | 3 → 3 | 1 | 1 | — |
| confinement-que-faire.html | 11 → 12 | 13 | 1 | combien-eau-stocker-par-personne, radio-a-piles-kit-urgence, aliments-sans-cuisson-kit-urgence |
| coupure-electricite-que-faire.html | 22 → 24 | 14 | 1 | frigo-congelateur-coupure-electricite, recharger-telephone-coupure-courant, combien-eau-stocker-par-personne, radio-a-piles-kit-urgence |
| couverture-de-survie.html | 4 → 8 | 9 | 2 | kit-urgence-voiture, sac-de-secours, kit-de-survie-72h |
| cyberattaque-que-faire.html | 3 → 5 | 12 | 1 | recharger-telephone-coupure-courant, radio-a-piles-kit-urgence, combien-eau-stocker-par-personne, arnaque-kit-urgence-gratuit |
| cyclone-que-faire.html | 11 → 13 | 13 | 1 | combien-eau-stocker-par-personne, radio-a-piles-kit-urgence, preparation-outre-mer, purifier-eau-pastilles-filtre, kit-urgence-saint-martin-saint-barthelemy |
| detecteur-de-fumee.html | 3 → 9 | 11 | 2 | feu-de-foret-que-faire, groupe-electrogene-securite, lampe-frontale-lanterne-kit-urgence, plan-familial-mise-en-surete, piles-kit-urgence |
| diagnostic-suis-je-pret.html | 12 → 13 | 16 | 1 | combien-eau-stocker-par-personne, aliments-sans-cuisson-kit-urgence, trousse-de-secours-kit-urgence, fr-alert-que-faire |
| entraide-voisins-crise.html | 10 → 12 | 12 | 1 | kit-urgence-handicap, kit-7-jours-strategie-europeenne-72h, arnaque-kit-urgence-gratuit |
| feu-de-foret-que-faire.html | 6 → 9 | 13 | 1 | combien-eau-stocker-par-personne, sac-de-secours, radio-a-piles-kit-urgence, canicule-que-faire, detecteur-de-fumee |
| fr-alert-que-faire.html | 17 → 23 | 17 | 1 | combien-eau-stocker-par-personne, plan-familial-mise-en-surete, attaque-terroriste-que-faire, accident-nucleaire-iode, feu-de-foret-que-faire |
| frigo-congelateur-coupure-electricite.html | 8 → 9 | 12 | 2 | recharger-telephone-coupure-courant, radio-a-piles-kit-urgence, lampe-frontale-lanterne-kit-urgence, piles-kit-urgence, batterie-externe-station-electrique |
| glossaire-preparation-crise.html | 4 → 4 | 24 | 2 | fr-alert-que-faire, signal-alerte-sirene, accident-nucleaire-iode, kit-urgence-enfants-ecole |
| groupe-electrogene-securite.html | 7 → 9 | 13 | 1 | batterie-externe-station-electrique, detecteur-de-fumee, radio-a-piles-kit-urgence, lampe-frontale-lanterne-kit-urgence, piles-kit-urgence |
| guide-tous-responsables-resume.html | 9 → 9 | 13 | 2 | kit-de-survie-72h, plan-familial-mise-en-surete, entraide-voisins-crise, signal-alerte-sirene, combien-eau-stocker-par-personne |
| index.html | 0 → 0 | 46 | 0 | — |
| inondation-que-faire.html | 16 → 20 | 14 | 1 | combien-eau-stocker-par-personne, radio-a-piles-kit-urgence, purifier-eau-pastilles-filtre, sac-de-secours, kit-urgence-guyane |
| kit-7-jours-strategie-europeenne-72h.html | 2 → 7 | 11 | 2 | combien-eau-stocker-par-personne, aliments-sans-cuisson-kit-urgence, tensions-internationales-se-preparer, piles-kit-urgence |
| kit-de-survie-72h-pas-cher.html | 4 → 10 | 9 | 1 | piles-kit-urgence, combien-eau-stocker-par-personne, aliments-sans-cuisson-kit-urgence, arnaque-kit-urgence-gratuit |
| kit-de-survie-72h.html | 37 → 40 | 12 | 1 | aliments-sans-cuisson-kit-urgence, radio-a-piles-kit-urgence, trousse-de-secours-kit-urgence, sac-de-secours, kit-de-survie-72h-pas-cher |
| kit-de-survie-gouvernement-pdf.html | 4 → 5 | 16 | 1 | arnaque-kit-urgence-gratuit, combien-eau-stocker-par-personne, aliments-sans-cuisson-kit-urgence, sac-de-secours, kit-de-survie-72h-pas-cher |
| kit-urgence-72h-famille-appartement-voiture.html | 10 → 14 | 15 | 1 | combien-eau-stocker-par-personne, plan-familial-mise-en-surete, sac-de-secours, aliments-sans-cuisson-kit-urgence |
| kit-urgence-72h-gouvernement.html | 8 → 10 | 13 | 1 | combien-eau-stocker-par-personne, que-mettre-dans-un-kit-d-urgence, aliments-sans-cuisson-kit-urgence, sac-de-secours, kit-de-survie-72h-pas-cher |
| kit-urgence-animaux.html | 10 → 13 | 10 | 1 | sac-de-secours, plan-familial-mise-en-surete, canicule-que-faire |
| kit-urgence-bebe.html | 11 → 15 | 12 | 1 | aliments-sans-cuisson-kit-urgence, trousse-de-secours-kit-urgence, kit-urgence-personne-agee, kit-urgence-handicap, kit-urgence-voiture |
| kit-urgence-enfants-ecole.html | 8 → 9 | 13 | 1 | kit-urgence-72h-famille-appartement-voiture, signal-alerte-sirene, kit-urgence-handicap, kit-urgence-animaux, kit-urgence-voiture |
| kit-urgence-guadeloupe.html | 4 → 6 | 12 | 2 | seisme-que-faire, combien-eau-stocker-par-personne, kit-urgence-saint-martin-saint-barthelemy, purifier-eau-pastilles-filtre |
| kit-urgence-guyane.html | 2 → 4 | 14 | 2 | purifier-eau-pastilles-filtre, combien-eau-stocker-par-personne, kit-urgence-guadeloupe, kit-urgence-mayotte, kit-urgence-saint-martin-saint-barthelemy |
| kit-urgence-handicap.html | 6 → 10 | 13 | 1 | recharger-telephone-coupure-courant, batterie-externe-station-electrique, kit-urgence-72h-famille-appartement-voiture, kit-urgence-bebe, kit-urgence-enfants-ecole |
| kit-urgence-la-reunion.html | 2 → 4 | 11 | 2 | seisme-que-faire, combien-eau-stocker-par-personne, radio-a-piles-kit-urgence |
| kit-urgence-martinique.html | 4 → 5 | 17 | 2 | seisme-que-faire, combien-eau-stocker-par-personne, kit-urgence-la-reunion, kit-urgence-mayotte, kit-urgence-saint-martin-saint-barthelemy |
| kit-urgence-mayotte.html | 3 → 6 | 14 | 2 | seisme-que-faire, purifier-eau-pastilles-filtre, kit-urgence-guadeloupe, kit-urgence-martinique, kit-urgence-guyane |
| kit-urgence-personne-agee.html | 7 → 9 | 13 | 1 | entraide-voisins-crise, combien-eau-stocker-par-personne, kit-urgence-72h-famille-appartement-voiture, kit-urgence-bebe, kit-urgence-animaux |
| kit-urgence-saint-martin-saint-barthelemy.html | 2 → 6 | 11 | 2 | seisme-que-faire, combien-eau-stocker-par-personne, purifier-eau-pastilles-filtre |
| kit-urgence-voiture.html | 5 → 9 | 11 | 1 | couverture-de-survie, sac-de-secours, inondation-que-faire |
| lampe-frontale-lanterne-kit-urgence.html | 5 → 13 | 9 | 2 | coupure-electricite-que-faire, detecteur-de-fumee, batterie-externe-station-electrique |
| licence-visuels.html | 5 → 5 | 7 | 1 | — |
| mentions-legales.html | 2 → 2 | 2 | 1 | — |
| piles-kit-urgence.html | 5 → 11 | 11 | 1 | kit-de-survie-72h-pas-cher, detecteur-de-fumee, recharger-telephone-coupure-courant, couverture-de-survie, trousse-de-secours-kit-urgence |
| plan-familial-mise-en-surete.html | 11 → 19 | 11 | 1 | fr-alert-que-faire, sac-de-secours, diagnostic-suis-je-pret |
| pourquoi.html | 67 → 67 | 6 | 1 | — |
| preparation-catastrophe-naturelle.html | 7 → 7 | 15 | 2 | combien-eau-stocker-par-personne, radio-a-piles-kit-urgence, plan-familial-mise-en-surete |
| preparation-outre-mer.html | 6 → 7 | 11 | 2 | — |
| proteger-son-foyer.html | 8 → 8 | 13 | 2 | — |
| purifier-eau-pastilles-filtre.html | 4 → 11 | 10 | 1 | inondation-que-faire, cyclone-que-faire, kit-urgence-mayotte, questions-reponses-kit-urgence |
| que-mettre-dans-un-kit-d-urgence.html | 14 → 16 | 9 | 2 | aliments-sans-cuisson-kit-urgence, trousse-de-secours-kit-urgence, radio-a-piles-kit-urgence |
| questions-reponses-kit-urgence.html | 7 → 8 | 24 | 1 | purifier-eau-pastilles-filtre, aliments-sans-cuisson-kit-urgence, kit-de-survie-72h |
| radio-a-piles-kit-urgence.html | 16 → 29 | 14 | 1 | fr-alert-que-faire, batterie-externe-station-electrique, couverture-de-survie, detecteur-de-fumee, trousse-de-secours-kit-urgence |
| reagir-en-cas-de-crise.html | 17 → 17 | 21 | 1 | — |
| recharger-telephone-coupure-courant.html | 8 → 12 | 12 | 2 | cyberattaque-que-faire, piles-kit-urgence, lampe-frontale-lanterne-kit-urgence, detecteur-de-fumee, trousse-de-secours-kit-urgence |
| s-equiper-kit-urgence.html | 11 → 11 | 16 | 2 | — |
| sac-de-secours.html | 8 → 20 | 11 | 1 | kit-urgence-voiture, trousse-de-secours-kit-urgence, lampe-frontale-lanterne-kit-urgence, plan-familial-mise-en-surete, kit-urgence-animaux |
| seisme-que-faire.html | 4 → 11 | 13 | 1 | combien-eau-stocker-par-personne, sac-de-secours, trousse-de-secours-kit-urgence, lampe-frontale-lanterne-kit-urgence, kit-urgence-la-reunion |
| signal-alerte-sirene.html | 8 → 12 | 13 | 1 | combien-eau-stocker-par-personne, accident-nucleaire-iode, attaque-terroriste-que-faire, feu-de-foret-que-faire, inondation-que-faire |
| sources.html | 8 → 8 | 0 | 1 | — |
| tempete-que-faire.html | 16 → 16 | 13 | 1 | combien-eau-stocker-par-personne, lampe-frontale-lanterne-kit-urgence, radio-a-piles-kit-urgence, frigo-congelateur-coupure-electricite |
| tensions-internationales-se-preparer.html | 2 → 3 | 13 | 2 | kit-7-jours-strategie-europeenne-72h, combien-eau-stocker-par-personne, radio-a-piles-kit-urgence, entraide-voisins-crise, guide-tous-responsables-resume |
| tous-les-guides.html | 2 → 2 | 61 | 1 | — |
| trousse-de-secours-kit-urgence.html | 5 → 15 | 10 | 1 | kit-urgence-bebe, sac-de-secours, seisme-que-faire, attaque-terroriste-que-faire |
| vague-de-froid-que-faire.html | 8 → 8 | 16 | 2 | combien-eau-stocker-par-personne, kit-urgence-personne-agee, signal-alerte-sirene, fr-alert-que-faire, confinement-que-faire |
