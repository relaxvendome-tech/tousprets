# Audit initial (phase A) : état au commit 9a77f7c, avant v8

Outils : `_outils/seo_v8_audit.py` (lecture seule, sortie `/tmp/audit_before.json`), `_outils/audit_v5.py`, Lighthouse 12 (4 pages), Playwright. L'audit page par page est dans `TABLEAU_SEO.csv` (colonne « note avant »), et l'inventaire dans `INVENTAIRE_URL.csv`.

## 1. Inventaire réel et écart avec « 73 pages / 112 entrées »

| Élément | Nombre | Détail |
|---|---|---|
| Fichiers HTML à la racine | **73** | 72 pages publiques + `privacy.html` (redirection `meta refresh` et `location.replace` vers confidentialite.html, `noindex,follow`) |
| URL de pages dans sitemap.xml | **72** | les 72 pages publiques ; privacy.html exclue volontairement |
| Entrées image avant v8 | **40** | 30 photos de héros + 10 entrées d'infographies : les 5 PNG de questions-reponses déclarés **deux fois** et leurs 5 versions WebP (doublons) |
| Total avant | **112** | 72 + 40 : c'est le chiffre « 112 entrées » annoncé. Il mélangeait URL de pages et images. |
| Entrées image après v8 | **35** | 30 photos + 5 infographies PNG, chacune une seule fois (les WebP sont la même image) |
| Total après | **107** | 72 URL de pages + 35 images |

Autres URL servies : robots.txt, sitemap.xml, manifest.json, sw.js, les données ouvertes de la checklist (`.json`, `.csv`), search-index.json, 2 fichiers de clé IndexNow, og-image.png, les icônes, img/cards/*.svg (pictogrammes). **Pas de 404.html** : GitHub Pages sert sa page 404 générique, avec le bon code 404.

Pages techniques ou de test exposées : aucune. Le dossier `_outils/` est publié par GitHub Pages, mais il n'est lié nulle part et ne contient pas de HTML indexable utile, à part `landing.html` (fragment) et `template_old.html`. Point à trancher : voir RESTANT.md.

## 2. Ce qui était déjà sain

- 72/72 canonical absolues, uniques, égales à l'URL ; `robots index, follow, max-image-preview:large` ; HTTPS sans www (CNAME).
- 1 seul H1 rendu par page. Sur l'accueil, le 2e `<h1>` détecté dans le source est dans une chaîne JS d'impression, jamais rendu.
- Aucun saut de niveau Hn (H2 → H4) sur les 73 pages.
- robots.txt : `Allow: /` et la ligne Sitemap ; aucune ressource bloquée.
- 0 lien interne mort, 0 page orpheline, toutes les pages à 2 clics maximum de l'accueil.
- Toutes les images ont un attribut alt et des dimensions `width`/`height` ; aucune image LCP en `loading="lazy"`.
- Titles et descriptions uniques ; aucune présentation du site comme officiel. Le bandeau « Appli citoyenne indépendante, pas un service de l'État » est présent partout.
- Lighthouse SEO 100 et Bonnes pratiques 100 sur les 4 pages mesurées.

## 3. Problèmes classés par gravité

### Élevée (fiabilité des signaux envoyés à Google)
1. **Dates fausses dans 21 pages.** Le texte visible indiquait « Mis à jour le 19 novembre 2026 », de même que `dateModified` dans le JSON-LD. Or l'historique git montre que le texte éditorial de ces 21 pages a été modifié le 23 novembre (corrections de contenu v6, refonte v4, v7). De plus, « Vérifié le » est recopié automatiquement depuis « Mis à jour le » par `template_v4.py`.
2. **BreadcrumbList incohérent sur 60 pages.** Le fil visible a 4 niveaux (Tous prêts › Tous les guides › rubrique › page), mais le JSON-LD n'en a que 3 : la rubrique manque. Sur kit-de-survie-72h, la rubrique pointait vers la page elle-même.
3. **Accueil : description ambiguë.** « Checklist interactive du kit d'urgence 72h **(guide officiel)** » pouvait laisser croire que l'outil est officiel.
4. **WebApplication de l'accueil inexact.** On y trouvait `operatingSystem` « Android, iOS, Windows, macOS (navigateur web) », `screenshot` = og-image.png (une bannière, pas une capture), `keywords`.

### Moyenne
5. 7 titles hors 30–62 caractères (accessibilité 26, mentions légales 29, anticiper 66, kit-urgence-72h-gouvernement 64, attaque 63, plan familial 63, accueil 63).
6. 12 descriptions hors 120–160 caractères (161 à 165 : comprendre, cyberattaque, cyclone, groupe électrogène, Guyane, La Réunion, Martinique, voiture, outre-mer, que-mettre, tempête, vague de froid).
7. 71 pages sans `twitter:title` ni `twitter:description` (seul l'accueil les avait) ; 1 og:title différent du title (cyberattaque).
8. 67 ALT d'images de héros non descriptifs (« Inondation : illustration »).
9. Le texte statique de l'accueil (section seo-about) n'énumérait pas le contenu de la checklist. La liste n'existait qu'en JavaScript, dans l'appli.
10. 9 pages avec moins de 3 liens contextuels entrants (Guyane, La Réunion, Saint-Martin, kit 7 jours, tensions internationales, ainsi que des pages légales et hub). Aucun bloc de maillage thématique explicite.
11. Tous les guides : décalage de mise en page CLS 0,111 (> 0,1), parce que le filtre `hidden` était affiché par JavaScript au-dessus des cartes.
12. Article utilisé pour les 7 pages hub, alors que CollectionPage est plus exact.

### Faible
13. `meta keywords` sur 72 pages : ignorée par Google, et sans intérêt.
14. Contraste du titre « À ne surtout pas faire » : 4,49:1, sous le seuil de 4,5:1 (Lighthouse, guides de risque).
15. Accueil : Lighthouse Performance 68 en mobile simulé, LCP 6,5 s simulé (448 ms observé en local). Coût principal : un HTML de 207 Ko et jsQR.js (257 Ko) chargés dès l'ouverture.
16. FAQPage sur 65 pages : le balisage est valide, mais Google ne l'affiche plus en résultat enrichi pour ce type de site (voir DONNEES_STRUCTUREES.md).

## 4. Mesures Lighthouse initiales (mobile simulé, local)

| Page | Perf. | Access. | BP | SEO | LCP | CLS | TBT |
|---|---|---|---|---|---|---|---|
| index.html | 68 | 100 | 100 | 100 | 6,5 s | 0 | 360 ms |
| inondation-que-faire.html | 99 | 96 | 100 | 100 | 2,3 s | 0 | 50 ms |
| tous-les-guides.html | 89 | 100 | 100 | 100 | 3,3 s | 0,111 | 0 ms |
| checklist-kit-urgence-72h.html | 99 | 100 | 100 | 100 | 2,1 s | 0 | 0 ms |

Note moyenne selon la grille de TABLEAU_SEO.csv avant v8 : **86,7/100**, minimum 75.
