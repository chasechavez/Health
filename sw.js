// Chase 2026 Training — Service Worker
// Enables offline access and Android PWA installation

const CACHE_NAME = 'chase-training-2026-v1';

// Core assets to cache for offline use
const PRECACHE_URLS = [
  './',
  './index.html',
  './manifest.json'
];

// External CDN scripts — cache on first use
const CDN_ORIGINS = [
  'https://unpkg.com',
  'https://unpkg.co',
  'https://cdnjs.cloudflare.com',
  'https://cdn.jsdelivr.net',
  'https://www.gstatic.com',
  'https://www.googleapis.com'
];

// Install: pre-cache local assets
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(PRECACHE_URLS))
      .then(() => self.skipWaiting())
  );
});

// Activate: clean up old caches
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys()
      .then(keys => Promise.all(
        keys
          .filter(key => key !== CACHE_NAME)
          .map(key => caches.delete(key))
      ))
      .then(() => self.clients.claim())
  );
});

// Fetch strategy:
// - Firebase API calls: network only (always need live data)
// - CDN scripts: cache first, fallback to network
// - Local files: network first, fallback to cache (so updates deploy instantly)
self.addEventListener('fetch', event => {
  const url = new URL(event.request.url);

  // Firebase — always network, never cache (real-time data)
  if (url.hostname.includes('firebaseio.com') ||
      url.hostname.includes('googleapis.com') ||
      url.hostname.includes('firebase')) {
    event.respondWith(fetch(event.request));
    return;
  }

  // CDN assets — cache first (they're versioned/stable)
  if (CDN_ORIGINS.some(origin => event.request.url.startsWith(origin))) {
    event.respondWith(
      caches.match(event.request).then(cached => {
        if (cached) return cached;
        return fetch(event.request).then(response => {
          if (response.ok) {
            const clone = response.clone();
            caches.open(CACHE_NAME).then(cache => cache.put(event.request, clone));
          }
          return response;
        });
      })
    );
    return;
  }

  // Local files — network first so new deployments are picked up,
  // fall back to cache if offline
  event.respondWith(
    fetch(event.request)
      .then(response => {
        if (response.ok) {
          const clone = response.clone();
          caches.open(CACHE_NAME).then(cache => cache.put(event.request, clone));
        }
        return response;
      })
      .catch(() => caches.match(event.request))
  );
});

// Push message from app to force cache refresh after update
self.addEventListener('message', event => {
  if (event.data === 'skipWaiting') self.skipWaiting();
});
