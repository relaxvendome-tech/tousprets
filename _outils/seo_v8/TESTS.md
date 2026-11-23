# Tests de non-régression (phase F)

Tests lancés sur l'état final, après le dernier passage de `redesign.py`, dans Chrome headless via Playwright, à la fois en `http://localhost` et en `file://`.

| Contrôle | Résultat | Outil |
|---|---|---|
| 73 pages × 2 largeurs (360 et 1366 px) = 146 chargements : erreurs JS | **0** | `/tmp/t8/test_all.py sweep` |
| Débordement horizontal | **0** | idem |
| Un seul H1 rendu par page | **73/73** | idem |
| JSON-LD invalide (JSON.parse dans le navigateur) | **0** | idem |
| JSON-LD : propriétés requises d'Article, BreadcrumbList cohérent (positions, dernier élément = canonical, aucun doublon), questions FAQ visibles | **0 écart** sur 71 BreadcrumbList, 60 Article et 65 FAQPage | script Python ad hoc (DONNEES_STRUCTUREES.md) |
| Liens internes morts et ancres | **0** | `audit_v5.py` (0 erreur, 0 avertissement) et `seo_v8_audit.py` |
| Titles et descriptions uniques, dans les longueurs cibles (30–62 / 120–160) | **72/72** | `seo_v8_audit.py`, TABLEAU_SEO.csv |
| Canonical absolue = URL, une seule par page | **72/72** pages publiques | idem |
| Sitemap : XML valide, 72 URL, toutes indexables et canoniques, privacy.html absente, 35 images existantes | OK | `xml.dom.minidom` et `audit_v5.py` |
| robots.txt : `Allow: /`, Sitemap, `Disallow: /_outils/` uniquement (aucune page publique, aucun CSS, JS ni image bloqué) | OK | `audit_v5.py` |
| Contrôles fonctionnels (test « Suis-je prêt ? », hub, questions-réponses, glossaire, checklist, privacy, sans JS, appli, hors ligne, v8) | **64/64** | `/tmp/t8/test_all.py` (54 contrôles v6 et 10 contrôles ajoutés) |
| Appli : 7 onglets (accueil, scénarios, guides, stock, profils, contacts, voisinage) | OK | idem |
| Appli : ajout d'un membre, persistance après rechargement, compteur à 2 | OK (`profiles_v1` : 0 → 2 → 2) | idem |
| Appli : quantités, 2 personnes → « 12 L (2 L/pers/jour × 2 pers. × 3 j) » | OK | idem |
| Appli : 0 erreur JS | OK | idem |
| Hors ligne : service worker actif, cache `tous-prets-v71` (25 entrées) ; accueil, guide visité, test, checklist, Tous les guides, confidentialité ; filtre du hub hors ligne | OK | idem |
| v8 : `tous-les-guides.html?q=radio` préremplit le champ et filtre (4 cartes sur 61) | OK | idem |
| v8 : accueil sans JavaScript, explication et 20 éléments de la checklist visibles | OK | idem |
| v8 : « Guides complémentaires » visible sans JavaScript | OK | idem |
| Sans JS, Tous les guides : 61 cartes visibles et filtre masqué (`<noscript>`) | OK | idem |
| Maillage des guides de risque (appli ou checklist + eau + équipement) | 22/22 | script Python (LIENS_INTERNES.md) |
| Idempotence : 2 passages successifs de `redesign.py`, md5 identiques | **289/289 fichiers** | `find … md5sum`, puis `diff` |
| Lighthouse sur 4 pages | voir PERFORMANCE.md (Access. 100 / BP 100 / SEO 100 partout) | Lighthouse |

## Faux positifs connus de `/tmp/fulltest.py` (file://)

Ce script signale 2 « problèmes » sur index.html, aussi bien avant qu'après v8 :
- `lien mort manifest.js` : son expression régulière coupe `manifest.json` après « .js ». Le fichier existe bien.
- `h1 2` : il compte dans le source un `<h1>` qui se trouve dans une chaîne JavaScript (le bilan d'exercice imprimable). Dans le DOM rendu, il n'y a qu'un H1 (contrôle Playwright ci-dessus).

## Non testé ici (honnêtement)

- Les codes HTTP réels de GitHub Pages et les redirections http → https et www → non-www : pas d'accès réseau. Procédure dans SEARCH_CONSOLE.md.
- Le test des résultats enrichis de Google et la validation schema.org en ligne.
- L'impression papier réelle de la checklist (déjà testée en PDF en v6, rien n'a changé sur cette page).
- Les Core Web Vitals réels (CrUX).
