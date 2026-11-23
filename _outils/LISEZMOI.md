# Outils de génération du site (tousprets.fr)

Scripts Python utilisés pour produire les pages éditoriales. Ils supposent :
- le dépôt cloné dans `/home/claude/tousprets` ;
- ces scripts copiés dans `/home/claude/seo` (`cp _outils/* /home/claude/seo/`) ;
- les icônes Lucide (licence ISC) : `mkdir -p /home/claude/icons && cd /home/claude/icons && npm i lucide-static`.

Ordre :
1. `python3 qa.py` (régénère aussi les pages de `newpages.py`), `python3 pdfpage.py`, `python3 fralert.py`, `python3 hub.py` selon les pages modifiées ;
2. **toujours ensuite** `python3 redesign.py` : applique la présentation (en-tête, menu, héros, cartes) et refait `search-index.json` ;
3. ajouter la page au sitemap, à `CAT` dans `redesign.py` (catégorie + icône), incrémenter `CACHE_VERSION` dans `sw.js`.
