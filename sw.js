// Keep Seeing Numbers app: offline shell + fresh data.
const V = "ksn-app-v1";
const SHELL = ["/app/", "/app/manifest.webmanifest", "/app/icon-192.png", "/angel-numbers/numbers.json"];
self.addEventListener("install", e => { e.waitUntil(caches.open(V).then(c => c.addAll(SHELL)).then(() => self.skipWaiting())); });
self.addEventListener("activate", e => {
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== V).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener("fetch", e => {
  const u = new URL(e.request.url);
  if (e.request.method !== "GET" || u.origin !== location.origin) return;
  if (u.pathname.startsWith("/api/")) return;
  // Network first, cache as fallback (content changes daily).
  e.respondWith(fetch(e.request).then(r => {
    if (r.ok && (u.pathname.startsWith("/app/") || u.pathname.startsWith("/angel-numbers/"))) {
      const copy = r.clone(); caches.open(V).then(c => c.put(e.request, copy));
    }
    return r;
  }).catch(() => caches.match(e.request).then(m => m || caches.match("/app/"))));
});
