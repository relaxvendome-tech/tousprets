# Ce qui reste à faire et points à trancher

## Points à trancher (décision de l'éditeur)

1. **Le H1 de l'accueil, « Être prêt change tout. »** C'est un slogan qui ne dit pas ce que fait la page. Option proposée : le garder comme accroche visuelle et mettre en H1 « Kit d'urgence 72 h : la checklist gratuite pour préparer votre foyer ». Cela touche au design de `landing.html` et `landing.css`, donc je ne l'ai pas fait. J'ai seulement rendu l'accroche (kicker) explicite.
2. **« Vérifié le »** était recopié automatiquement de « Mis à jour le » par `template_v4.py`. Désormais, `seo_v8.json` (`date_verifiee`) fixe cette date : 23 novembre si le texte vient des commits de vérification v6, 19 novembre sinon (6 pages). À l'avenir, ne mettre à jour `date_verifiee` qu'après une vraie relecture des consignes contre les sources.
3. **FAQPage sur 65 pages** : à garder (aucun risque) ou à retirer (pages plus légères). Aucun résultat enrichi n'est à attendre (DONNEES_STRUCTUREES.md).
4. **kit-de-survie-72h et que-mettre-dans-un-kit-d-urgence sont proches.** Sans 301 possible sur GitHub Pages, je recommande de surveiller les deux dans Search Console pendant 6 à 8 semaines avant toute fusion.
5. **Le dossier `_outils/` est public** (`.nojekyll`) : il contient les scripts, les rapports, et l'adresse de contact déjà visible sur le site. J'ai ajouté `Disallow: /_outils/` dans robots.txt, mais les fichiers restent accessibles par leur URL. Option : sortir `_outils/` du dépôt publié, ou publier depuis un dossier `docs/`.
6. **Photo `tempete-que-faire.webp` (202 Ko)** : la recompresser en qualité 65 environ ferait gagner beaucoup de poids, mais le rendu change un peu. C'est à valider visuellement.
7. **Lien « Signaler une erreur »** : il pointe vers une adresse Gmail personnelle. Ce n'est pas un problème SEO, mais une adresse dédiée au projet renforcerait la crédibilité (page Contact, voir le plan sur 90 jours).

## Restant technique (non fait, avec justification)

| Sujet | Pourquoi ce n'est pas fait | Gain attendu |
|---|---|---|
| Accueil : charger jsQR.js (257 Ko) et qrcode.min.js à la demande | Modifie le code de l'appli, hors du périmètre « head et sections statiques » | −277 Ko au premier chargement ; LCP simulé nettement meilleur |
| Page 404 personnalisée (`404.html`) | Nouvelle page : je la propose sans la créer. GitHub Pages la sert automatiquement avec le code 404 ; elle aiderait à remettre l'internaute sur un guide (recherche, liens vers le kit et les situations d'urgence) | UX, pas de soft-404 |
| `dateModified` automatique | Les dates sont figées dans `seo_v8.json`. Après une vraie modification de texte, il faut mettre à jour `date_modifiee`, ou relancer le calcul git décrit dans `seo_v8.json` (_doc) | Exactitude des dates |
| Redirections http → https, www → non-www, codes 200 | Pas d'accès réseau ici. À vérifier avec `curl -I` après publication (SEARCH_CONSOLE.md, étape 0) | Contrôle |
| AVIF | Gain de 9,9 % seulement à qualité égale | Faible |
| sources.html (373 mots, sans chapô) | C'est la page la moins bien notée (81). L'enrichir demande du texte éditorial vérifié : date de vérification par source, ce que chaque source couvre | Confiance (E-E-A-T) |

## Contenus proposés (à ne PAS créer sans validation)

Méthode : une page n'est proposée que si aucune page existante ne répond déjà à l'intention (voir MOTS_CLES.md).

| # | Proposition | Intention / requêtes | Pourquoi ce n'est pas de la cannibalisation | Verdict |
|---|---|---|---|---|
| 1 | **Coupure d'eau : que faire ?** (`coupure-eau-que-faire.html`) | panne d'eau que faire, coupure d'eau potable, eau non potable au robinet | Aucune page ne traite la coupure du réseau d'eau. Aujourd'hui, seules 2 réponses de la page questions-réponses (chauffe-eau, toilettes sèches) l'abordent, et la page renverrait vers elles | **Recommandée** |
| 2 | **Se chauffer sans électricité, sans danger** | chauffage sans électricité, garder la chaleur pendant une coupure | vague-de-froid traite le grand froid, groupe-electrogene traite le monoxyde de carbone. Il n'existe pas de page « logement froid pendant une coupure ». Les consignes monoxyde de carbone doivent être reprises mot pour mot des sources officielles | Recommandée, avec relecture des consignes de sécurité |
| 3 | **Communiquer sans réseau** | communiquer sans réseau, téléphone sans réseau urgence, talkie-walkie PMR446 | Le sujet existe en une réponse et une infographie dans questions-réponses. Une page dédiée devrait reprendre ce contenu, et la réponse renverrait vers elle | Possible ; à arbitrer avec questions-réponses |
| 4 | **Entretenir et faire tourner son kit** (dates, piles, eau, calendrier sur 2 ans) | vérifier son kit d'urgence, renouveler eau stockée, rotation stock | L'entretien n'est qu'une ligne dans chaque liste. Un calendrier pratique est différenciant | Recommandée |
| 5 | « Frigo : combien de temps sans électricité » | — | **Déjà couverte** par frigo-congelateur-coupure-electricite (H1 et description : frigo 4 h, congélateur 48 h / 24 h) | Pas de nouvelle page |
| 6 | « Purifier l'eau sans pastilles » | — | **Déjà couverte** par purifier-eau-pastilles-filtre (ébullition, filtres) | Pas de nouvelle page ; un H2 « Sans pastilles » est possible |
| 7 | « Kit d'urgence en appartement » | — | Couverte par la section appartement de kit-urgence-72h-famille-appartement-voiture | Pas de nouvelle page ; enrichir la section (rangement : réutiliser l'infographie « petit appartement ») |
| 8 | **Checklist interactive ou liste PDF officielle : laquelle choisir ?** | checklist kit urgence gratuite, liste pdf kit 72h | Risque de doublon avec kit-de-survie-gouvernement-pdf. À traiter sans dénigrer le PDF officiel : il est la référence, l'appli en est une mise en pratique | Plutôt une section dans kit-de-survie-gouvernement-pdf qu'une nouvelle page |
| 9 | Rubrique « Vigilances » (météo, crues, alertes du moment) | vigilance orange, alerte en cours | **Déconseillée.** Ce type de contenu n'a de valeur que s'il est à jour en temps réel. Une page obsolète sur un sujet de sécurité serait trompeuse et dangereuse. Les sources officielles (Météo-France, Vigicrues) le font mieux. Mieux vaut un lien clair vers elles depuis chaque guide | Non |

## Crédibilité (cahier des charges, § 7), état actuel

| Élément demandé | État |
|---|---|
| Page À propos | `pourquoi.html` |
| Méthodologie éditoriale | `charte-editoriale.html` |
| Sources officielles | `sources.html` (à enrichir) |
| Page Contact | **absente** (seulement un lien mailto « Signaler une erreur ») : page à proposer |
| Politique de correction | dans la charte éditoriale et via « Signaler une erreur » |
| Dates de vérification | « Vérifié le » sur chaque guide (voir le point 2) |
| Auteurs et relecteurs | « la rédaction de Tous prêts ». Aucun auteur nommé : c'est volontaire, je n'ai rien inventé. Si l'éditeur souhaite se nommer, il faut le faire avec ses vraies qualifications, sans titre d'expert non justifié |
