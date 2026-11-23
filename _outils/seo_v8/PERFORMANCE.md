# Performance (Lighthouse et images)

Mesure : Lighthouse (`/home/claude/v4/agent4/node_modules`), Chrome headless, profil mobile par défaut (throttling simulé, Moto G Power), serveur local `python3 -m http.server`. Script : `/tmp/lh.sh`. Rapports JSON : `/tmp/lh_before/` et `/tmp/lh_after/`. Ce sont des valeurs de **laboratoire**. Les Core Web Vitals réels (75e percentile, CrUX) ne seront visibles dans Search Console qu'avec assez de trafic. En local, il n'y a ni latence réseau réelle ni compression gzip de GitHub Pages.

## Avant / après

| Page | Perf. | Access. | BP | SEO | LCP | CLS | TBT | Poids |
|---|---|---|---|---|---|---|---|---|
| Accueil : avant | 68 | 100 | 100 | 100 | 6,5 s | 0 | 360 ms | 1 372 Ko |
| Accueil : après | 70 | 100 | 100 | 100 | 6,5 s | 0 | 300 ms | 1 375 Ko |
| Guide inondation : avant | 99 | 96 | 100 | 100 | 2,3 s | 0 | 50 ms | 213 Ko |
| Guide inondation : après | 99 | **100** | 100 | 100 | 2,3 s | 0 | 0 ms | 215 Ko |
| Tous les guides : avant | 89 | 100 | 100 | 100 | 3,3 s | **0,111** | 0 ms | 991 Ko |
| Tous les guides : après | **97** | 100 | 100 | 100 | 2,6 s | **0** | 0 ms | 932 Ko |
| Checklist : avant | 99 | 100 | 100 | 100 | 2,1 s | 0 | 0 ms | 183 Ko |
| Checklist : après | 99 | 100 | 100 | 100 | 2,1 s | 0 | 40 ms | 185 Ko |

Mesure « après » refaite sur l'état final (rapports : `/tmp/lh_final/`). Sur le guide, l'accessibilité passe de 96 à 100 grâce à la correction du contraste. Sur l'accueil, l'écart de score et de TBT (68 → 70, 360 → 300 ms) reste dans la variabilité habituelle de Lighthouse : je ne l'attribue pas à mes modifications.

## Corrections sûres appliquées

1. **CLS de Tous les guides : 0,111 → 0.** Le filtre est rendu dans le HTML au lieu d'être révélé par JavaScript au-dessus des 61 cartes, et il est masqué sans JS (`<noscript>`).
2. **Préchargement de l'image LCP de l'accueil.** Aucun gain mesurable : en local, l'image démarre déjà à 82 ms et le LCP observé est de 448 ms. Le LCP simulé de 6,7 s vient du modèle de Lighthouse, qui compte comme chemin critique le HTML de 207 Ko et les scripts différés. Je la conserve parce qu'elle est sans risque et peut aider sur un réseau réel lent.
3. Contraste corrigé sur l'encadré « À ne surtout pas faire » (accessibilité).
4. Les ressources externes restent à 0 (CSP `'self'`). Aucune police tierce, aucun script tiers.

## Images

- Toutes les images ont `width` et `height`. Aucune image LCP n'est en `loading="lazy"`, et les héros sont en `fetchpriority="high"`. Les cartes sont en lazy, sauf les 4 premières de Tous les guides.
- WebP déjà servi via `<picture>` pour les 30 photos et les 5 infographies : infographies PNG de 480 à 590 Ko → WebP de 70 à 90 Ko.
- **AVIF : non adopté.** J'ai testé l'encodage AVIF des 30 photos avec Pillow, en exigeant un PSNR au moins égal à celui du WebP actuel par rapport au JPEG source. Résultat : 1 406 Ko contre 1 561 Ko, soit **−9,9 %** (environ 5 Ko par photo de héros). Ce gain ne justifie pas un troisième jeu de fichiers (+1,4 Mo dans le dépôt), une balise `<source>` de plus sur 70 pages et un rendu qui ne serait pas strictement identique.
- Point faible repéré : `img/photos/tempete-que-faire.webp` pèse 202 Ko, autant que le JPEG, car la photo est très détaillée (feuillage). Elle est chargée comme carte sur plusieurs pages. La recompresser changerait le rendu. Je ne l'ai pas fait : c'est à décider (RESTANT.md).

## Restant, par gain estimé (non traité)

1. **Accueil : charger `jsQR.js` (257 Ko non minifié) et `qrcode.min.js` (20 Ko) seulement à l'ouverture du scanner ou de l'affichage d'un QR code.** Ils sont aujourd'hui chargés en `defer` à chaque visite. Pour l'accueil, c'est le gain le plus important (environ −277 Ko sur un premier chargement de 1,37 Mo). Il demande de modifier le code de l'appli (hors `<head>` et hors sections statiques), ce qui était exclu de cette mission.
2. HTML de l'accueil : 207 Ko (CSS et JS en ligne). On pourrait l'externaliser pour profiter du cache, mais cela touche à l'appli et au service worker.
3. style.css : 52 Ko, dont 65 % inutilisés sur une page donnée (Lighthouse). Le scinder n'en vaut pas la peine tant que le cache du service worker s'en charge.
4. Mesurer les Core Web Vitals réels après publication : Search Console > Signaux Web essentiels, ou PageSpeed Insights sur l'URL publique.
