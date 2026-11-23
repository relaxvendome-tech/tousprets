# Ordre de régénération (v4 + v5)
Après tout générateur de pages (newpages, qa, hub, univers…) : `cd _outils && python3 redesign.py`
redesign.py transforme les pages puis enchaîne automatiquement (tous idempotents) :
1. legal_v5.py      — en-tête / pied communs pour les pages sans en-tête (légales, privacy) [v5]
2. nav_v4.py        — en-tête et menu (7 rubriques + « Tous les guides » + Outils pratiques)
3. template_v4.py   — méta, partage, temps de lecture
4. essentiels.py    — blocs L'essentiel (lit essentiels.json)
5. merge_now.py
6. template_v4.py   — temps de lecture à jour
7. prevnext_v5.py   — « Guide précédent / suivant » dans l'ordre de UNIV (redesign.py) [v5]
7 bis. v6_structure.py — outils des pages test, tous les guides, questions-réponses, glossaire, checklist ; privacy.html ; sitemap sans privacy [v6]
8. apply_landing.py index.html — accueil #landing depuis landing.html / landing.css [v5 : branché]
9. webp.py --lazy
10. typo_fr.py
Contrôle : python3 audit_v5.py ..  (SEO, liens, sitemap, robots ; code 1 si défaut).
Le CSS du menu, des pages légales (.pg-legal) et du bloc .pn est dans style.css (bloc « v5 »).
Incrémenter CACHE_VERSION dans sw.js à chaque publication (v69 au 2026-11-23, installation tolérante depuis v69).
v6 : le JS des pages outils est dans pages.js (s'appuie sur window.TPSearch exposé par search.js) ; CSS dans le bloc « v6 » de style.css.
ATTENTION : diag.py, hub.py, univers.py, qa.py importent /home/claude/seo/newpages.py, qui réécrit 6 pages à l'import ; garder /home/claude/seo synchronisé avec _outils (cp _outils/*.py /home/claude/seo/).
v8 (2026-11-23) : 13. seo_v8.py — dernier maillon de redesign.py. Titles, descriptions, og/twitter, JSON-LD (dates réelles, BreadcrumbList depuis le fil visible, CollectionPage pour les hubs), « Guides complémentaires », ALT des héros, section seo-about de l'accueil, sitemap (lastmod git). Données : seo_v8.json (modifier là, pas dans les pages). Contrôles : seo_v8_audit.py (audit), seo_v8_rapport.py (notes /100, CSV). Rapports : _outils/seo_v8/. CACHE_VERSION v71.
v9 (2026-11-23) : 14. lisibilite_v9.py — dernier maillon. Bloc CSS v9 de style.css (source lisibilite_v9.css), CSS appli (lisibilite_v9_app.css), FAQ de sécurité ouvertes, sources avant la FAQ, rattachement des pages ajoutées aux hubs (NEW) et liens croisés (XREF). Tokens uniques en tête de style.css. Rapport : RAPPORT_V9_LISIBILITE.md. CACHE_VERSION v75.
v13 (2026-11-23) : 18. v13.py — dernier maillon (après droits_v11.py). Accueil : pas d'animation fadeIn sur l'écran affiché au chargement (LCP), vignettes 480 px img/photos/480/ en srcset ; GoatCounter coupé dans l'appli Android ; « Journal des corrections » de la charte (liste JOURNAL dans v13.py) ; impression : .noprint/.hero-cta masqués. Publication : .nojekyll supprimé, _config.yml (Jekyll ne publie plus _outils/). Rapport : RAPPORT_V13.md. CACHE_VERSION v81.
