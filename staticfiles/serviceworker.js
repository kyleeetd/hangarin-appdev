const CACHE_NAME = 'hangarin-cache-v1';
const urlsToCache = [
  '/',          // Homepage
  '/tasks/',    // Your list pages
  '/static/',   // Cache CSS/JS automatically
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(urlsToCache))
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request).then(response => response || fetch(event.request))
  );
});
