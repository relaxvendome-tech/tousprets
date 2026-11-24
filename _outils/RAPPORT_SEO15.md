# Mission SEO « référence française » : rapport (24 novembre 2026)

Rien n'est publié tant que la mise en ligne n'est pas validée. Sauvegarde de la version de départ : commit `a092572` (dépôt GitHub) et copie `/home/claude/seo15/base`.

## 1. Ce qui a été examiné

- **75 fichiers HTML**, sitemap (74 URL), robots.txt, données structurées (JSON-LD), liens internes, canonicals, titres, descriptions, H1/H2/H3, nombre de mots, pages à faible maillage.
- **Lighthouse mobile** (page d'accueil, avant et après), axe-core, 66 tests fonctionnels de l'appli, 225 chargements (75 pages × 320, 390, 1366 px).
- **Concurrence** (Perplexity) : sur « kit d'urgence 72h », « checklist kit d'urgence », « que mettre dans un kit d'urgence », les résultats sont dominés par ecologie.gouv.fr, georisques.gouv.fr, info.gouv.fr, des PDF de préfectures et de communes, puis quelques sites marchands. Format gagnant : page courte + **PDF imprimable**. Aucun résultat observé ne propose de checklist interactive, personnalisée et hors ligne : c'est l'angle différenciant de Tous prêts. Perplexity n'a pas pu relever les positions exactes de Google : ces observations ne sont pas un classement.

## 2. Constats

| Niveau | Constat | Statut |
|---|---|---|
| P0 | Aucun blocage d'indexation : 0 erreur, robots.txt ouvert, 74 URL canoniques et indexables dans le sitemap, 0 canonical incohérent, 0 JSON-LD invalide, 0 lien cassé. | Vérifié |
| P0 | `privacy.html` : volontairement en `noindex`, canonical vers `confidentialite.html`, hors sitemap (adresse de la politique de confidentialité déclarée sur Google Play). | Conservé tel quel |
| P1 | Accueil : 2 balises `<h1>` dans le code source (la 2e dans un script d'impression du mode exercice). | Corrigé |
| P1 | Accueil : titre de 63 caractères, H1 sans mot-clé (« Être prêt change tout. »). | Corrigé |
| P1 | Accueil : ne disait pas ce qu'est un kit 72 h, pourquoi 72 h, ni les 8 indispensables ; pas de réponse à « kit d'urgence gouvernement gratuit ». | Corrigé |
| P1 | Pas de **checklist en PDF**, alors que c'est le format qui domine les résultats. | Corrigé |
| P1 | Titre du congélateur : 61 caractères. Sac de secours : « sac d'évacuation » absent du titre. | Corrigé |
| P2 | Image du héros de l'accueil servie en 960 px sur mobile (93 Ko évitables d'après Lighthouse). | Corrigé (640 px) |
| P2 | 5 pages de moins de 500 mots : privacy (redirection), licence-visuels, sources, mentions-legales, anticiper-s-entraider (page carrefour). Pages utiles par nature : à ne pas gonfler artificiellement. | Conservées |
| P2 | Données structurées : Article, BreadcrumbList, Organization, WebSite, FAQPage (66 pages), WebApplication. Les « Person » sont les auteurs réels des photos. Aucune note, aucun avis, aucun auteur inventé. | Conforme |

## 3. Modifications (script `_outils/seo15.py`, dernier maillon de `redesign.py`)

- **Accueil**
  - Titre : « Kit d'urgence 72h : checklist gratuite | Tous prêts » (51 caractères).
  - Description : « Préparez votre foyer avec une checklist 72h gratuite, interactive et utilisable hors ligne. Guides pratiques et conseils pour toute la famille. » (143 caractères). Open Graph et Twitter alignés.
  - **H1** : « Kit d'urgence 72 h : préparez votre famille sereinement ». Le slogan « Être prêt change tout. » est conservé juste au-dessus, en surtitre.
  - Un seul `<h1>` dans le source (le titre du bilan imprimé passe en `<h2>`).
  - Nouvelle section **« Le kit d'urgence 72 h, en bref »** : ce que c'est, pourquoi 72 h (guide SGDSN du 20/11/2025, stratégie européenne du 26/03/2025), pour qui, les 8 indispensables avec un lien vers chaque guide, la checklist en 3 étapes, 4 questions (dont « le gouvernement distribue-t-il un kit gratuit ? » → non, et lien vers la page arnaque), sources.
  - Image du héros en 640 px sur mobile.
- **Checklist PDF** : `checklist-kit-urgence-72h.pdf` (A4, 2 pages), avec un bouton sur la page à imprimer et un lien depuis l'accueil.
- **Titres** : « Congélateur sans courant : combien de temps ? (frigo 4 h) » (57) ; « Sac de secours (sac d'évacuation) : que mettre dedans ? ».
- **Sitemap** : dates de mise à jour actualisées pour les 6 pages modifiées.
- **Cache hors ligne** : version v87.

Les sessions précédentes du jour avaient déjà ajouté : la navigation en 4 entrées, « Ma préparation », la checklist en 3 états, les menus harmonisés, la FAQ batterie / station, 13 photos et la section solaire.

## 4. Tests

| Contrôle | Avant | Après |
|---|---|---|
| Lighthouse mobile, accueil (serveur local sans compression*) : performance | 82 | 89 |
| LCP | 3,5 s | 2,8 s |
| Temps de blocage total (TBT) | 310 ms | 260 ms |
| CLS | 0,018 | 0,014 |
| Accessibilité / bonnes pratiques / SEO | 100 / 100 / 100 | 100 / 100 / 100 |
| H1 multiples dans le source | 1 page | 0 |
| Titres > 60 caractères | 2 | 0 |
| audit_v5 (liens, ancres, métadonnées, sitemap) | 0 erreur | 0 erreur |
| Appli (apptest14) | 66/66 | 66/66 |
| Pages × largeurs sans erreur JS ni débordement | 225/225 | 225/225 |
| axe-core (accueil, Ma préparation, checklist, Bons réflexes) | 0 défaut sérieux | 0 défaut sérieux |

\* GitHub Pages compresse les pages : en production, le LCP sera meilleur. À mesurer avec PageSpeed Insights après mise en ligne.

## 5. Ce qui reste (et pourquoi)

- **Search Console** : non connectée, je n'ai aucune donnée Google (indexation, positions, clics). Rien dans ce rapport ne prétend le contraire.
- **Positions réelles** : non mesurées. Aucune position n'est garantie.
- **Backlinks** : 14 domaines référents d'après ton audit OpenSEO. La liste de cibles ci-dessous est à démarcher par toi : je n'envoie aucun e-mail.
- **« kit d'urgence 72h Croix-Rouge »** (390 recherches/mois) : pas de page dédiée. Il faut d'abord vérifier ce que la Croix-Rouge française publie réellement, sans rien inventer.
- **Réécriture éditoriale page par page** des 74 guides (raccourcir, sourcer chaque consigne) : chantier de plusieurs semaines, prévu dans la feuille de route.

## 6. Après la mise en ligne (à faire par toi, 15 minutes)

1. Search Console → ajouter la propriété « Domaine » tousprets.fr (validation par enregistrement DNS TXT chez ton registraire).
2. Envoyer `https://tousprets.fr/sitemap.xml`.
3. Inspection d'URL → « Demander une indexation » pour : l'accueil, `checklist-kit-urgence-72h.html`, `kit-urgence-72h-gouvernement.html`, `que-mettre-dans-un-kit-d-urgence.html`, `sac-de-secours.html`.
4. PageSpeed Insights sur l'accueil (mobile) : noter LCP, INP, CLS.
5. Relier Search Console à OpenSEO.

## 7. Feuille de route 90 jours

| Semaines | Action | Mesure |
|---|---|---|
| 1 | Search Console, sitemap, demandes d'indexation, PageSpeed réel | Pages indexées / découvertes non indexées |
| 1-2 | Démarcher 10 premières cibles (liste ci-dessous), en commençant par les communes à risque (pages DICRIM) et les associations de secourisme | Réponses, liens obtenus |
| 2-4 | Réécrire les 10 pages du pilier 1 (kit 72 h, checklist, que mettre, gouvernement, PDF, pas cher, 7 jours, eau, aliments, sac de secours) : réponse en 2 phrases en tête, une source par consigne, date de vérification | Position moyenne et CTR par page |
| 4-6 | Pilier 3 (famille) : bébé, enfants, personnes âgées, handicap, animaux, appartement/voiture : vérifier les consignes, ajouter les liens vers la checklist adaptée | Impressions des requêtes familiales |
| 6-8 | Pilier 4 (risques) : inondation, séisme, tempête, cyclone, feu, canicule, coupure : encadré « à faire / à ne pas faire / sources » sur toutes les fiches (16 déjà faites) | Requêtes « que faire » |
| 8-10 | Ressource à citer : « Guide familial 72 h » imprimable (PDF A4 recto-verso) pour écoles, mairies, associations ; 2e vague de démarchage (médias régionaux avant l'hiver) | Domaines référents |
| 10-12 | Bilan Search Console : pages en progression/recul, cannibalisation (accueil ↔ kit-de-survie-72h ↔ que-mettre), ajustement des titres sur les pages à fort affichage et faible CTR | Top 100 / 20 / 10 / 3 |

Indicateurs du tableau de bord mensuel : requêtes positionnées, nombre dans le top 100/20/10/3, clics organiques, ouvertures de la checklist (GoatCounter : événement à ajouter), domaines référents pertinents.

## 8. Cibles de liens éditoriaux (proposées par Gemini, à vérifier avant tout envoi)

Croix-Rouge française, Protection Civile, FFSS, AFPCN, IRMa (Grenoble) ; pages « risques majeurs » / DICRIM de Paris, Lyon, Bordeaux, Nantes, Grenoble, Nice, Marseille ; FCPE, PEEP, UNAF ; APF France handicap, Unapei ; Petits Frères des Pauvres, Générations Mouvement ; bibliothèques de Paris, BM Lyon, médiathèque de l'Isère ; Outre-mer la 1ère, Ouest-France, Sud Ouest.

Modèle d'e-mail (corrigé : Tous prêts n'est pas « basé exclusivement » sur la Croix-Rouge) :

> Objet : Une ressource gratuite pour votre page « [risques majeurs] »
>
> Bonjour, en lisant votre page [titre], j'ai pensé qu'un outil gratuit et sans publicité pourrait aider vos lecteurs. Tous prêts (https://tousprets.fr) traduit le guide officiel « Tous responsables » (SGDSN) en actions concrètes : une checklist du kit d'urgence 72 h qui calcule les quantités pour le foyer et fonctionne sans réseau, et des fiches par risque [et par profil]. Aucune inscription, aucune donnée envoyée. Si vous la jugez utile, elle pourrait figurer dans vos liens. Bien cordialement, [Prénom Nom], Tous prêts.

## 9. Inventaire des 75 pages

| Page | Titre | Car. | Mots | Liens entrants |
|---|---|---|---|---|
| accessibilite.html | Déclaration d'accessibilité / Tous prêts | 40 | 940 | 73 |
| accident-nucleaire-iode.html | Accident nucléaire : comprimés d'iode et confinement | 52 | 999 | 10 |
| aide-application.html | Aide : application Tous prêts, hors ligne, installation | 55 | 1368 | 5 |
| aliments-sans-cuisson-kit-urgence.html | Aliments sans cuisson pour le kit d'urgence : la liste | 54 | 719 | 73 |
| anticiper-s-entraider.html | Anticiper et s'entraider : en famille et entre voisins | 54 | 457 | 73 |
| arnaque-kit-urgence-gratuit.html | Arnaque au faux kit d'urgence gratuit : vérifier et signaler | 60 | 873 | 9 |
| attaque-terroriste-que-faire.html | Attaque terroriste : s'échapper, se cacher, alerter | 51 | 742 | 72 |
| batterie-externe-station-electrique.html | Batterie externe et station électrique : mAh, Wh, sécurité | 58 | 1664 | 12 |
| canicule-que-faire.html | Canicule : que faire pour se protéger (gestes officiels) | 56 | 845 | 73 |
| charte-editoriale.html | Charte éditoriale de Tous prêts : sources, vérification | 55 | 936 | 73 |
| checklist-kit-urgence-72h.html | Checklist kit d'urgence 72h à imprimer, gratuite | 48 | 709 | 74 |
| combien-eau-stocker-par-personne.html | Combien de litres d'eau stocker par personne ? (72 h) | 53 | 730 | 73 |
| comprendre-s-informer.html | Comprendre la préparation aux crises : guide, glossaire | 55 | 515 | 74 |
| confidentialite.html | Confidentialité – Tous prêts (zéro donnée collectée) | 52 | 1079 | 74 |
| confinement-que-faire.html | Confinement et mise à l’abri : que faire en cas d’alerte ? | 58 | 796 | 73 |
| coupure-electricite-que-faire.html | Coupure d’électricité : que faire heure par heure + kit 72h | 59 | 834 | 73 |
| couverture-de-survie.html | Couverture de survie : usage réel et limites | 44 | 758 | 10 |
| cyberattaque-que-faire.html | Cyberattaque : que faire ? Les bons réflexes au quotidien | 57 | 749 | 73 |
| cyclone-que-faire.html | Cyclone outre-mer : alertes Météo-France et protection | 54 | 1085 | 14 |
| detecteur-de-fumee.html | Détecteur de fumée : obligation et entretien | 44 | 813 | 11 |
| diagnostic-suis-je-pret.html | Suis-je prêt ? Le test de préparation aux crises (2 min) | 56 | 792 | 74 |
| entraide-voisins-crise.html | Entraide entre voisins en crise : s’organiser avant | 51 | 596 | 73 |
| feu-de-foret-que-faire.html | Feu de forêt : débroussaillement et réflexes de protection | 58 | 1113 | 11 |
| fr-alert-que-faire.html | FR-Alert : que faire quand l'alerte sonne sur le téléphone ? | 60 | 1206 | 73 |
| frigo-congelateur-coupure-electricite.html | Congélateur sans courant : combien de temps ? (frigo 4 h) | 57 | 799 | 72 |
| glossaire-preparation-crise.html | Glossaire de la préparation aux crises : 30 termes clés | 55 | 1707 | 73 |
| groupe-electrogene-securite.html | Groupe électrogène : sécurité et risque monoxyde de carbone | 59 | 1008 | 12 |
| guide-tous-responsables-resume.html | Guide « Tous responsables » : le résumé clair et pratique | 57 | 734 | 72 |
| index.html | Kit d'urgence 72h : checklist gratuite / Tous prêts | 51 | 2498 | 74 |
| inondation-que-faire.html | Inondation : les bons réflexes (avant, pendant, après) | 54 | 772 | 73 |
| kit-7-jours-strategie-europeenne-72h.html | Kit 7 jours : aller au-delà des 72 h de l'UE | 44 | 1082 | 9 |
| kit-de-survie-72h-pas-cher.html | Kit de survie 72h pas cher : le faire soi-même | 46 | 647 | 73 |
| kit-de-survie-72h.html | Kit de survie 72h : liste complète (guide Tous responsables) | 60 | 947 | 74 |
| kit-de-survie-gouvernement-pdf.html | Kit de survie gouvernement PDF : guide officiel et liste 72h | 60 | 1497 | 73 |
| kit-urgence-72h-famille-appartement-voiture.html | Kit d’urgence 72h : famille, bébé, appartement ou voiture | 57 | 769 | 73 |
| kit-urgence-72h-gouvernement.html | Kit d'urgence 72h du gouvernement : ce que dit le guide | 55 | 658 | 73 |
| kit-urgence-animaux.html | Kit d'urgence pour chien et chat : la liste | 43 | 684 | 73 |
| kit-urgence-bebe.html | Kit d'urgence bébé : la liste pour 72h | 38 | 828 | 73 |
| kit-urgence-enfants-ecole.html | Kit urgence 72 h et enfants à l'école : règles et réflexes | 58 | 959 | 11 |
| kit-urgence-guadeloupe.html | Kit d'urgence Guadeloupe : cyclones, séismes, volcan | 52 | 1059 | 6 |
| kit-urgence-guyane.html | Kit d'urgence Guyane : inondations, orages, coupures | 52 | 938 | 6 |
| kit-urgence-handicap.html | Kit urgence 72 h et handicap : 114, matériel et aidants | 55 | 1093 | 12 |
| kit-urgence-la-reunion.html | Kit d'urgence La Réunion : cyclones, volcan, séismes | 52 | 970 | 6 |
| kit-urgence-martinique.html | Kit d'urgence Martinique : cyclone, séisme, Pelée | 49 | 957 | 6 |
| kit-urgence-mayotte.html | Kit d'urgence Mayotte : cyclones, séismes, eau | 46 | 1005 | 7 |
| kit-urgence-personne-agee.html | Kit urgence 72 h et personne âgée : santé, CCAS et météo | 56 | 1027 | 11 |
| kit-urgence-saint-martin-saint-barthelemy.html | Kit 72 h Saint-Martin et Saint-Barthélemy | 41 | 1017 | 7 |
| kit-urgence-voiture.html | Kit urgence voiture : gilet, triangle, loi Montagne et neige | 60 | 902 | 11 |
| lampe-frontale-lanterne-kit-urgence.html | Lampe frontale et lanterne : éclairer sans risque | 49 | 798 | 14 |
| licence-visuels.html | Droits d'auteur et réutilisation des contenus / Tous prêts | 58 | 280 | 73 |
| mentions-legales.html | Mentions légales du site Tous prêts | 35 | 450 | 73 |
| panne-numerique-cyberattaque-72h.html | Panne numérique, cyberattaque : tenir 72 h sans réseau | 54 | 1415 | 4 |
| piles-kit-urgence.html | Piles du kit d'urgence : types et stockage | 42 | 821 | 12 |
| plan-familial-mise-en-surete.html | Plan familial de mise en sûreté (PFMS) : rôles et contacts | 58 | 872 | 74 |
| pourquoi.html | Pourquoi Tous prêts existe : appli citoyenne gratuite | 53 | 517 | 73 |
| preparation-catastrophe-naturelle.html | Catastrophe naturelle : comment se préparer en famille | 54 | 821 | 72 |
| preparation-outre-mer.html | Kit d'urgence en outre-mer : cyclones, séismes, volcans | 55 | 501 | 73 |
| privacy.html | Confidentialité – Tous prêts (aucune donnée personnelle) | 56 | 20 | 0 |
| proteger-son-foyer.html | Protéger son foyer : enfants, aînés, handicap, animaux | 54 | 592 | 73 |
| purifier-eau-pastilles-filtre.html | Purifier l'eau : ébullition, pastilles, filtres | 47 | 891 | 13 |
| que-mettre-dans-un-kit-d-urgence.html | Que mettre dans un kit d’urgence ? La liste essentielle | 55 | 706 | 73 |
| questions-reponses-kit-urgence.html | Kit d'urgence : vos questions pratiques, nos réponses | 53 | 6018 | 73 |
| radio-a-piles-kit-urgence.html | Radio à piles kit d’urgence : pourquoi c’est indispensable | 58 | 600 | 73 |
| reagir-en-cas-de-crise.html | Réagir en cas de crise : les bons réflexes par situation | 56 | 814 | 74 |
| recharger-telephone-coupure-courant.html | Recharger son téléphone pendant une coupure de courant | 54 | 664 | 72 |
| s-equiper-kit-urgence.html | S'équiper pour une crise : le matériel utile, sans gadgets | 58 | 626 | 11 |
| sac-de-secours.html | Sac de secours (sac d’évacuation) : que mettre dedans ? | 55 | 906 | 73 |
| seisme-que-faire.html | Séisme : que faire pendant et après une secousse | 48 | 1088 | 13 |
| signal-alerte-sirene.html | Signal national d'alerte (sirène) : son, durée et FR-Alert | 58 | 1003 | 13 |
| sources.html | Sources et méthode – Tous prêts (transparence totale) | 53 | 386 | 73 |
| tempete-que-faire.html | Tempête : que faire avant, pendant et après ? Bons réflexes | 59 | 856 | 73 |
| tensions-internationales-se-preparer.html | Tensions internationales : se préparer sans paniquer | 52 | 761 | 72 |
| tous-les-guides.html | Kit d'urgence 72h : tous nos guides pratiques | 45 | 1670 | 74 |
| trousse-de-secours-kit-urgence.html | Trousse de secours : contenu et formation | 41 | 852 | 17 |
| vague-de-froid-que-faire.html | Vague de froid : que faire pour se protéger ? Grand froid | 57 | 809 | 72 |