/*
  Service worker — Tous prêts 
  - Statiques (icônes, manifest, *) : cache d'abord.
  - Navigation / index.html : réseau d'abord, repli sur le cache hors ligne.
  - Anciens caches supprimés à l'activation.
  IMPORTANT : incrémente CACHE_VERSION à chaque mise à jour.
*/

const CACHE_VERSION = 'tous-prets-v35';
const PRECACHE_URLS = [
  './',
  './index.html',
  './manifest.json',
  './icon-192.png',
  './icon-512.png',
  './icon-512-maskable.png',
  './apple-touch-icon.png',
  './qrcode.min.js',
  './jsQR.js',
  './confidentialite.html',
  './mentions-legales.html',
  './accessibilite.html',
  './sources.html',
'./style.css',
  './privacy.html'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_VERSION).then((cache) => Promise.all(PRECACHE_URLS.map(async (u) => {
      // cache: 'reload' contourne le cache HTTP pour ne pas pré-cacher une version périmée
      const res = await fetch(new Request(u, { cache: 'reload' }));
      if (!res.ok) throw new Error('Précache échoué : ' + u + ' (' + res.status + ')');
      await cache.put(u, await cleanResponse(res));
    }))).then(() => self.skipWaiting())
  );
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
        .then((res) => (res.ok ? putInCache(req, res) : offlinePage(req).then((c) => (c.status === 503 ? res : c))))
        .then((res) => cleanResponse(res))
        .catch(() => offlinePage(req))
    );
    return;
  }

  // Cache d'abord pour les statiques
  event.respondWith(
    caches.match(req, { ignoreSearch: true }).then((cached) => cached || fetch(req).then((res) => putInCache(req, res)))
  );
});
