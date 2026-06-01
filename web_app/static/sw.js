/**
 * AlocasiaTrack service worker — minimal offline shell.
 *
 * Strategy: Network-first for all requests.
 * If the network fails, return a cached copy if available.
 * This lets the app work on spotty Wi-Fi (common in greenhouses).
 */

const CACHE = "alocasiatrack-v1";

// Static assets to pre-cache (Bootstrap CDN omitted — too large).
const PRECACHE = ["/", "/stock", "/sales", "/species", "/plants"];

self.addEventListener("install", event => {
  self.skipWaiting();
  event.waitUntil(
    caches.open(CACHE).then(cache => cache.addAll(PRECACHE).catch(() => {}))
  );
});

self.addEventListener("activate", event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
    )
  );
  self.clients.claim();
});

self.addEventListener("fetch", event => {
  // Only handle same-origin GET requests
  if (event.request.method !== "GET") return;
  const url = new URL(event.request.url);
  if (url.origin !== self.location.origin) return;

  event.respondWith(
    fetch(event.request)
      .then(response => {
        // Cache successful HTML responses
        if (response.ok && response.headers.get("content-type")?.includes("text/html")) {
          const clone = response.clone();
          caches.open(CACHE).then(cache => cache.put(event.request, clone));
        }
        return response;
      })
      .catch(() => caches.match(event.request))
  );
});
