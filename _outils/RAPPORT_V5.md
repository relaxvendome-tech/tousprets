# Rapport refonte v5 — 23 novembre 2026

**Pages** : 73 avant, 73 après (aucune supprimée, aucune URL changée). 72 publiques + privacy.html (redirection noindex).

## Fonctionnalités
- **Conservées** : appli complète (7 onglets, foyer, stock, checklists, contacts, voisins, sauvegarde), clés localStorage inchangées, recherche, partage, WebP, CSP 'self'.
- **Améliorées** : accueil (héros « Être prêt change tout. », 2 boutons, ligne d'engagements, « Nos engagements », situations : Confinement et Feu de forêt/incendie explicites), menu à 8 liens (« Tous les guides » sorti du sous-menu), contraste bouton orange (#0F2440 sur #D9731A = 4,77:1 ; survol #E8873A = 5,91:1, la source landing.css était restée en blanc).
- **Nouvelles** : section « Commencer simplement » (3 parcours), appel final, bloc précédent/suivant sur 60 guides, en-tête/menu/pied communs sur sources, mentions légales, confidentialité, accessibilité, privacy (H1 ajouté), audit SEO automatisé.

## Problèmes corrigés
- 5 liens cassés `vendor/*.LICENSE` (mentions légales, sources) → fichiers à la racine.
- privacy.html : 2 canonical (dont un relatif) → 1 ; 0 H1 → 1.
- Pages légales sans og:*, JSON-LD, menu ni pied commun → ajoutés (legal_v5.py).
- landing.css désynchronisé de index.html (couleur du bouton) → resynchronisé ; apply_landing branché dans redesign.py.

## Tests réels (Playwright, Chrome, http://localhost)
- 73 pages × 7 largeurs (320→1920) = 511 chargements : 0 erreur JS, 0 débordement horizontal, 1 H1 partout (aussi en file://).
- Appli : 32/32 contrôles (7 onglets, ajout d'un membre 1→2, eau 12 L = 2 L × 2 pers. × 3 j, score 10 % → 30 %, case cochée persistante après rechargement, export JSON puis restauration après effacement).
- Clavier : tiroir mobile atteint en 9 Tab, focus dans le tiroir, Échap ferme et rend le focus ; sous-menu bureau ouvert/fermé (Entrée/Échap).
- Hors ligne : SW actif, cache v66 (30 entrées), index + appli, guide déjà visité et page légale OK hors ligne.
- Mise à jour SW (copie du site, v67-test) : ancien cache supprimé en 1,5 s, données localStorage conservées.

## SEO (audit_v5.py)
0 erreur : titles et descriptions uniques, 1 H1, canonical exact, og complets, JSON-LD valides, alt partout, liens et ancres internes OK, 72/72 pages publiques dans le sitemap (lastmod 2026-11-23), robots.txt cohérent.

## Performance (local, 390 px)
index.html 206 Ko HTML, 12 ressources, ~1,09 Mo décodés, FCP 188 ms ; guide 21 Ko HTML, 212 Ko, FCP 160 ms ; page légale 13 Ko, 133 Ko.

## Restant
- Un guide jamais visité hors ligne affiche l'accueil (pas de précache de tous les guides) — d'où la mention « après une première visite ».
- index.html reste la page la plus lourde (~1,09 Mo décodés au premier chargement) : optimisation non traitée.
- Entre 901 et 1000 px, les libellés du menu passent sur 2 lignes (sans débordement).
