# Ordre de régénération (v4)
Après tout générateur de pages (newpages, qa, hub, univers…) :
1. python3 redesign.py
2. python3 _outils/nav_v4.py .
3. python3 _outils/template_v4.py .
4. python3 _outils/essentiels.py .   (lit essentiels.json à côté)
5. python3 _outils/merge_now.py .
6. python3 _outils/template_v4.py .  (temps de lecture à jour)
7. python3 _outils/webp.py . --lazy
8. python3 _outils/typo_fr.py .
Accueil : python3 _outils/apply_landing.py index.html (landing.html / landing.css).
Tous les scripts sont idempotents. Incrémenter CACHE_VERSION dans sw.js à chaque publication.
redesign.py enchaîne désormais automatiquement les étapes 2 à 8.
