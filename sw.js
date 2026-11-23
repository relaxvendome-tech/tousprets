/*
  Service worker — Tous prêts 
  - Statiques (icônes, manifest, *) : cache d'abord.
  - Navigation / index.html : réseau d'abord, repli sur le cache hors ligne.
  - Anciens caches supprimés à l'activation.
  IMPORTANT : incrémente CACHE_VERSION à chaque mise à jour.
*/

const CACHE_VERSION = 'tous-prets-v79';
// Indispensables au démarrage hors ligne : leur échec fait échouer l'installation (l'ancien SW reste actif).
const CRITICAL_URLS = [
  './',
  './index.html',
  './manifest.json',
  './logo.svg',
  './style.css',
  './fonts/inter-latin-wght-normal.woff2',
  './icon-192.png'
];
// Utiles mais non bloquants : mis en cache un par un, un échec est consigné sans bloquer l'installation.
const OPTIONAL_URLS = [
  './share.js',
  './nav.js',
  './search.js',
  './pages.js',
  './search-index.json',
  './icon-512.png',
  './icon-512-maskable.png',
  './apple-touch-icon.png',
  './qrcode.min.js',
  './jsQR.js',
  './confidentialite.html',
  './mentions-legales.html',
  './accessibilite.html',
  './sources.html',
  './privacy.html',
  './diagnostic-suis-je-pret.html',
  './checklist-kit-urgence-72h.html',
  './tous-les-guides.html'
];
const PRECACHE_URLS = CRITICAL_URLS.concat(OPTIONAL_URLS);

async function precacheOne(cache, u) {
  // cache: 'reload' contourne le cache HTTP pour ne pas pré-cacher une version périmée
  const res = await fetch(new Request(u, { cache: 'reload' }));
  if (!res.ok) throw new Error(u + ' (' + res.status + ')');
  await cache.put(u, await cleanResponse(res));
}

self.addEventListener('install', (event) => {
  event.waitUntil((async () => {
    const cache = await caches.open(CACHE_VERSION);
    // 1. Fichiers critiques : tous requis.
    await Promise.all(CRITICAL_URLS.map((u) => precacheOne(cache, u)));
    // 2. Fichiers optionnels : un par un, échecs consignés (non bloquants).
    const failed = [];
    for (const u of OPTIONAL_URLS) {
      try { await precacheOne(cache, u); } catch (e) { failed.push(String(e && e.message || u)); }
    }
    if (failed.length) console.warn('[SW ' + CACHE_VERSION + '] précache partiel, fichiers ignorés :', failed);
    await self.skipWaiting();
  })());
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k !== CACHE_VERSION).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

// Une réponse « redirected » ne peut pas servir une navigation (erreur Chrome) : on la reconstruit.
async function cleanResponse(res) {
  if (!res.redirected) return res;
  const body = await res.blob();
  return new Response(body, { status: res.status, statusText: res.statusText, headers: res.headers });
}

function putInCache(request, response) {
  if (response && response.ok && response.status === 200 && response.type === 'basic') {
    const copy = response.clone();
    caches.open(CACHE_VERSION).then(async (cache) => cache.put(request, await cleanResponse(copy))).catch(() => {});
  }
  return response;
}

function offlinePage(req) {
  return caches.match(req, { ignoreSearch: true })
    .then((c) => c || caches.match('./index.html'))
    .then((c) => c || new Response('<!doctype html><meta charset="utf-8"><title>Hors ligne</title><p>Hors ligne.</p>',
      { status: 503, headers: { 'Content-Type': 'text/html; charset=utf-8' } }));
}

self.addEventListener('fetch', (event) => {
  const req = event.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return;

  const isPage = req.mode === 'navigate' || url.pathname.endsWith('/') || url.pathname.endsWith('/index.html');

  if (isPage) {
    // Réseau d'abord, repli cache
    event.respondWith(
      fetch(req)
        // En ligne, une erreur HTTP (404…) reste une erreur : on ne sert une copie que pour CETTE page
        // (jamais index.html à la place d'une page inexistante). Hors ligne : repli inchangé (catch).
        .then((res) => (res.ok ? putInCache(req, res) : caches.match(req, { ignoreSearch: true }).then((c) => c || res)))
        .then((res) => cleanResponse(res))
        .catch(() => offlinePage(req))
    );
    return;
  }

  // CSS / JS / JSON : réseau d'abord (évite une page neuve avec un style périmé), repli cache hors ligne
  if (/\.(css|js|json)$/.test(url.pathname)) {
    event.respondWith(
      fetch(req).then((res) => (res.ok ? putInCache(req, res) : res))
        .catch(() => caches.match(req, { ignoreSearch: true }).then((c) => c || Response.error()))
    );
    return;
  }

  // Cache d'abord pour les autres statiques (images, polices)
  event.respondWith(
    caches.match(req, { ignoreSearch: true }).then((cached) => cached || fetch(req).then((res) => putInCache(req, res)))
  );
});
