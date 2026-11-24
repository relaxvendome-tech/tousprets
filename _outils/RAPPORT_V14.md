# Rapport v14 : refonte ergonomique et psychologique (24 novembre 2026)

Rien n'est publié. Les modifications sont dans le dépôt local (76 fichiers). Aucune clé localStorage existante n'a été renommée ni supprimée. Toutes les URL sont conservées.

## 1. Organisation du travail

| Contributeur | Mission | Ce qui a été retenu |
|---|---|---|
| Claude (superviseur) | Audit du code, arbitrages, intégration, tests, rapport | Tout le code (`_outils/v14.py`, `v14.js`, `v14.css`) |
| Gemini | Audit UX comparatif tousprets.fr / kitdurgence72h.org (mobile) | 7 onglets → 4 ; premier écran trop chargé ; séparer le minimum 72 h du reste ; composition du foyer ; rappel de vérification ; libellés ARIA des boutons + / − |
| Perplexity | Vérification des sources officielles | Guide « Tous responsables » du 20/11/2025 toujours la version en vigueur ; 6 L d'eau par personne ; vérification du kit **deux fois par an** (SGDSN) ; lait infantile, petits pots et nourriture pour animaux dans la liste officielle |
| DeepSeek | Textes d'interface (niveaux, 3 états, prochaines actions, foyer) | Libellés de niveau (« À commencer », « Premiers pas », « En progrès », « Presque prêt », « Prêt »), ton non culpabilisant, actions du jour ; réécrits pour intégrer les quantités calculées |
| ChatGPT | Jetons de design (palette institutionnelle, sombre, texte agrandi) | Comparé à la palette existante (déjà bleu institutionnel, contrastes vérifiés) : on garde l'existante ; repris : cible tactile 48 px, ambre doux pour « En partie » |
| Mistral | Protocole de tests pour 6 profils | Grille de tâches et pièges utilisée pour les tests ci-dessous |
| Grok | — | Non connecté dans Chrome (page de connexion) : remplacé par Mistral |

## 2. Audit : principaux problèmes trouvés (avant)

- 7 onglets en bas d'écran (Accueil, Scénarios, Guides, Stock, Foyer, Contacts, Voisins) : libellés de 10 px, trop de choix.
- Accueil = vitrine + application mélangées sur un seul écran très long (tableau de bord, parcours, axes, scénarios, exercice).
- Deux « prochaine étape » concurrentes (note du score et parcours) ; « Très bien préparé » possible avec des indispensables manquants.
- Checklist kit 72 h : 40 cases binaires au même niveau ; long paragraphe d'introduction ; 9 boutons de scénario empilés en pleine largeur sur mobile.
- Pas de besoins particuliers du foyer (bébé, animaux, personne dépendante, traitement).
- Boutons + / − du stock sans nom accessible.
- Bugs : nom « Tous prêts » illisible en thème sombre choisi manuellement ; débordement horizontal à 320 px en très grand texte (accueil, cartes chiffrées) ; débordement sur le guide cyberattaque (URL longue).
- Guides : « L'essentiel » ne donnait que « à faire » ; « à ne pas faire » et sources dispersés plus bas.

## 3. Ce qui a changé

| Zone | Après |
|---|---|
| Accueil | Titre « Être prêt change tout. », sous-titre demandé, 2 boutons (Préparer mon foyer / Découvrir les bons réflexes), 5 engagements discrets, 3 portes PRÉPARER / AGIR / ANTICIPER. Le contenu éditorial (familles, guides, sources) reste en dessous pour le SEO. |
| Navigation | 4 entrées : Accueil, Ma préparation, Bons réflexes, Guides. Barre fixe en bas sur mobile, horizontale dans l'en-tête dès 900 px. Icônes SVG homogènes. Bouton retour Android et navigateur pris en charge (historique). Liens profonds `#ma-preparation`, `#screen-scenarios`. |
| Ma préparation | Tableau de bord : niveau + phrase, **une prochaine action** avec bouton, 8 indispensables (état visible, cliquables), besoins du foyer, enregistrement automatique, dernière sauvegarde, prochaine vérification du kit (+6 mois, bouton « J'ai vérifié mon kit »). Raccourcis : checklist, foyer, stock, contacts, voisins, par situation, mode exercice. Axes du guide officiel repliés. |
| Checklist kit 72 h | Étapes 1 Foyer → 2 Indispensables → 3 Compléments → 4 Suivi. Les 8 indispensables d'abord, avec quantités calculées (ex. « 18 L en bouteilles » pour 3 personnes). Matériel en **3 états** (À prévoir / En partie / Disponible) ; gestes et réflexes en cases simples. Catégories repliables avec compteur. Carte « Pour votre foyer » selon les besoins cochés (source affichée : guide officiel ou conseil Tous prêts). |
| Progression sincère | « En partie » compte pour moitié ; un indispensable vaut « disponible » s'il l'est dans la checklist ou dans le stock (indiqué « D'après votre stock ») ; jamais « Prêt » ni 100 % tant qu'un indispensable manque. |
| Foyer | Besoins particuliers : bébé, enfants, animaux, personne âgée ou dépendante, traitement ou matériel médical, avec conseil et lien vers le guide. |
| Bons réflexes | Écran renommé, accès direct à « Réagir en cas de crise » et « Reconnaître l'alerte », recherche hors ligne conservée. |
| Guides (16 fiches risques) | « L'essentiel » : ce qu'il faut savoir, ce qu'il faut faire, ce qu'il ne faut pas faire, sources officielles + date de vérification + lien méthode. L'encadré « À ne surtout pas faire » situé plus bas est déplacé (pas de doublon). Aucun texte de consigne ajouté : tout vient des pages existantes et de `essentiels.json`. |
| 68 guides | Le bouton « Cocher ma liste dans l'appli » ouvre directement la checklist. |
| Accessibilité | Noms accessibles des + / − ; groupes radio natifs pour les 3 états (lisibles au clavier et au lecteur d'écran, libellé texte en plus de la couleur) ; focus déplacé sur le titre à chaque écran ; correctifs de contraste et de débordement ci-dessus. |
| Données | Nouvelles clés sauvegardées dans l'export : `tp_needs_v1`, `tp_kit_check_v1`. Techniques (non exportées) : `tp_last_change_v1`, `tp_last_backup_v1`. Rien n'est envoyé. |
| Service worker | `tous-prets-v83`. |

## 4. Tests (état final)

- **Application** (`/home/claude/v14test/apptest14.py`) : **61/61**. Accueil, navigation, tableau de bord, foyer et besoins, 3 états et persistance, retour à « À prévoir », catégories, 7/8 indispensables ≠ « Prêt », vérification du kit, rechargement, export → effacement → import identique, Bons réflexes et recherche, urgence, autres scénarios inchangés, retour, mode exercice, thème sombre, 320 px en très grand texte (5 écrans), bureau, clavier, lien profond, bouton des guides, hors ligne (accueil, checklist, guide).
- **axe-core** (WCAG 2.0/2.1/2.2 A et AA) : 0 défaut sérieux ou critique sur accueil, Ma préparation, checklist (clair et sombre), Bons réflexes.
- **Toutes les pages** : 75 pages × 3 largeurs (320, 390, 1366) = 225 chargements, 0 erreur JS, 0 débordement.
- **SEO** : `audit_v5.py` 0 erreur, 0 avertissement ; un seul H1 par page ; titres, descriptions, canonical, sitemap inchangés.
- **Poids** : index.html 220 → 258 Ko non compressé (≈ +8 Ko en gzip). Lighthouse non relancé dans cette session.

### Profils simulés (protocole Mistral)

| Profil | Comprendre | Démarrer | Foyer | Cocher | Manquants | Guide | Mobile |
|---|---|---|---|---|---|---|---|
| Personne âgée | ✓ titre + 2 boutons | ✓ 1 geste | ✓ boutons + / − 44 px | ✓ 3 boutons texte 48 px | ✓ « Prochaine action » | ✓ onglet Guides | ✓ très grand texte sans débordement |
| Parent de 2 enfants | ✓ | ✓ | ✓ + besoins bébé / enfants | ✓ | ✓ 8 pastilles | ✓ | ✓ |
| Peu habitué au numérique | ✓ | ✓ | ✓ | ✓ libellés en toutes lettres | ✓ | ⚠ « Bons réflexes » / « Guides » à distinguer : sous-titres ajoutés | ✓ |
| Lecteur d'écran | ✓ H1 | ✓ | ✓ | ✓ radios natives | ✓ texte « : Disponible » | ✓ | ✓ (non testé avec un vrai NVDA/VoiceOver) |
| Utilisateur pressé | ✓ < 5 s | ✓ | ✓ | ✓ | ✓ | ✓ recherche | ✓ |
| Nouveau visiteur | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ retour arrière | ✓ hors ligne |

Ces profils sont **simulés** (automates), pas des personnes réelles. Un test avec 5 vraies personnes reste recommandé.

## 5. Limites et suites

- Pas encore publié : l'envoi sur GitHub a été refusé à cette session. À valider avant mise en ligne.
- Le guide Gemini suggère aussi un rappel exportable dans l'agenda (.ics) : non fait.
- Les 58 autres guides gardent leur « L'essentiel » actuel ; la structure 3 parties est appliquée aux 16 fiches risques qui ont des données vérifiées (`essentiels.json`).
- Avant / après : `avant-apres-v14.png`.
