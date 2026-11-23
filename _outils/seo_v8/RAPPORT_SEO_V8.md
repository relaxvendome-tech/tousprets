# Rapport SEO v8 : tousprets.fr (23 novembre 2026)

Rien n'est commité ni poussé. Aucune page, URL, fonctionnalité, clé localStorage ou consigne de sécurité n'a été supprimée ou modifiée sur le fond. Aucune page n'a été créée.

## Chiffres réels
- **73 fichiers HTML** : 72 pages publiques et privacy.html (redirection noindex).
- **Sitemap** : 72 URL de pages et 35 images, soit 107 entrées. Avant : 72 + 40 = 112. L'écart vient de 5 PNG d'infographies déclarés deux fois et de 5 copies WebP, supprimés. `lastmod` provient de git.
- **Note moyenne** : 86,7 → **92,6/100**. **Minimum** : 75 → 81 (sources.html). Maximum : 98. Aucune page n'atteint 100, car la relecture humaine des consignes n'a pas été faite et la performance n'est mesurée que sur 4 pages. Grille dans `seo_v8_rapport.py`, détail par page dans TABLEAU_SEO.csv.
- **Tests** :
  - 146 chargements (73 pages × 360/1366 px) : 0 erreur JS, 0 débordement, 1 H1 par page, 0 JSON-LD invalide ;
  - 64/64 contrôles fonctionnels (appli, quantités, persistance, hors ligne v71, `?q=`, sans JS) ;
  - 0 lien mort ;
  - idempotence md5 vérifiée sur 289 fichiers.
- **Lighthouse mobile** (Perf./Access./BP/SEO) :
  - accueil 70/100/100/100 ;
  - guide inondation 99/100/100/100 ;
  - Tous les guides 97/100/100/100 (CLS 0,111 → 0) ;
  - checklist 99/100/100/100.

## Fichiers
| Document | Contenu |
|---|---|
| [AUDIT_INITIAL.md](AUDIT_INITIAL.md) | inventaire, écart 73/112, problèmes classés par gravité |
| [INVENTAIRE_URL.csv](INVENTAIRE_URL.csv) | toutes les URL (pages, images, fichiers techniques) |
| [TABLEAU_SEO.csv](TABLEAU_SEO.csv) | une ligne par page : requête principale et secondaires, title, description, H1, maillage, dates, note avant/après, problèmes |
| [MOTS_CLES.md](MOTS_CLES.md) | cartographie, cannibalisation, couverture des requêtes du cahier des charges |
| [CORRECTIONS.md](CORRECTIONS.md) | toutes les corrections, phases B, C et D |
| [DONNEES_STRUCTUREES.md](DONNEES_STRUCTUREES.md) | schémas par page, FAQPage, HowTo, SearchAction |
| [PERFORMANCE.md](PERFORMANCE.md) | Lighthouse avant/après, images, décision sur l'AVIF |
| [LIENS_INTERNES.md](LIENS_INTERNES.md) | maillage page par page, profondeur, Guides complémentaires |
| [TESTS.md](TESTS.md) | non-régression |
| [RESTANT.md](RESTANT.md) | points à trancher, restant technique, contenus proposés |
| [SEARCH_CONSOLE.md](SEARCH_CONSOLE.md) | procédure Google et Bing, URL prioritaires |
| [PLAN_90_JOURS.md](PLAN_90_JOURS.md) | plan de progression |
| [NOTORIETE.md](NOTORIETE.md) | ressources citables, cibles par type, sans partenariat inventé |

## Mise en œuvre
- `_outils/seo_v8.py`, piloté par `_outils/seo_v8.json`, branché en dernier dans `redesign.py` (copie identique dans `/home/claude/seo/`).
- Outils de contrôle : `seo_v8_audit.py` et `seo_v8_rapport.py`.
- Autres fichiers modifiés : sitemap.xml, robots.txt (`Disallow: /_outils/`), style.css (bloc v8), sw.js (v71), PIPELINE_V4.md.

## Principaux points à trancher (détail dans RESTANT.md)
1. Le H1 de l'accueil, « Être prêt change tout. », n'est pas explicite.
2. Charger jsQR (257 Ko) à la demande : c'est le principal gain de performance de l'accueil.
3. Garder ou retirer FAQPage : aucun résultat enrichi n'est à attendre.
4. Le dossier `_outils/` est public.
5. Contenus proposés : coupure d'eau, chauffage sans électricité, entretien du kit.
