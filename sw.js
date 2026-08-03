// Service worker：讓 App 在沒有網路時仍可開啟（PRD 12 離線能力）。
// 改動 index.html 之後要把 CACHE 版本號往上加，使用者才會拿到新版。
const CACHE = 'ingredient-manager-v32';
const ASSETS = ['./', './index.html', './manifest.webmanifest', './icon-192.png', './icon-512.png'];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE)
      .then(cache => cache.addAll(ASSETS))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(key => key !== CACHE).map(key => caches.delete(key))))
      .then(() => self.clients.claim())
  );
});

function cachePut(request, response) {
  const copy = response.clone();
  caches.open(CACHE).then(cache => cache.put(request, copy));
  return response;
}

self.addEventListener('fetch', event => {
  const request = event.request;
  if (request.method !== 'GET') return;

  // 只處理自己網域的請求。同步用的 api.github.com 一律直接走網路，
  // 絕不能被快取，否則會拿到過期的雲端資料。
  if (new URL(request.url).origin !== self.location.origin) return;

  // 頁面本身採 network-first，確保一有新版就會更新；離線時退回快取。
  if (request.mode === 'navigate') {
    event.respondWith(
      fetch(request)
        .then(response => cachePut(request, response))
        .catch(() => caches.match(request).then(hit => hit || caches.match('./index.html')))
    );
    return;
  }

  // 圖示等靜態資源採 cache-first。
  event.respondWith(
    caches.match(request).then(hit => hit || fetch(request).then(response => cachePut(request, response)))
  );
});
