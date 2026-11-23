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
