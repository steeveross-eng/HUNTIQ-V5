/**
 * Service Worker Registration - PHASE F BIONIC ULTIMATE
 * 
 * Enregistre le Service Worker pour le caching et le mode offline
 * 
 * @version 1.0.0
 * @phase F
 */

const isLocalhost = Boolean(
  window.location.hostname === 'localhost' ||
  window.location.hostname === '[::1]' ||
  window.location.hostname.match(/^127(?:\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}$/)
);

/**
 * Register Service Worker
 */
export function register(config) {
  if (process.env.NODE_ENV === 'production' && 'serviceWorker' in navigator) {
    const publicUrl = new URL(process.env.PUBLIC_URL, window.location.href);
    
    if (publicUrl.origin !== window.location.origin) {
      return;
    }

    window.addEventListener('load', () => {
      const swUrl = `${process.env.PUBLIC_URL}/service-worker.js`;

      if (isLocalhost) {
        checkValidServiceWorker(swUrl, config);
        navigator.serviceWorker.ready.then(() => {
          console.log('[SW] Service Worker ready (localhost)');
        });
      } else {
        registerValidSW(swUrl, config);
      }
    });
  }
}

/**
 * Register valid Service Worker
 */
function registerValidSW(swUrl, config) {
  navigator.serviceWorker
    .register(swUrl)
    .then((registration) => {
      console.log('[SW] Service Worker registered successfully');
      
      registration.onupdatefound = () => {
        const installingWorker = registration.installing;
        
        if (installingWorker == null) {
          return;
        }
        
        installingWorker.onstatechange = () => {
          if (installingWorker.state === 'installed') {
            if (navigator.serviceWorker.controller) {
              console.log('[SW] New content available; please refresh.');
              
              if (config && config.onUpdate) {
                config.onUpdate(registration);
              }
            } else {
              console.log('[SW] Content cached for offline use.');
              
              if (config && config.onSuccess) {
                config.onSuccess(registration);
              }
            }
          }
        };
      };
    })
    .catch((error) => {
      console.error('[SW] Service Worker registration failed:', error);
    });
}

/**
 * Check if Service Worker is valid (localhost)
 */
function checkValidServiceWorker(swUrl, config) {
  fetch(swUrl, {
    headers: { 'Service-Worker': 'script' }
  })
    .then((response) => {
      const contentType = response.headers.get('content-type');
      
      if (
        response.status === 404 ||
        (contentType != null && contentType.indexOf('javascript') === -1)
      ) {
        navigator.serviceWorker.ready.then((registration) => {
          registration.unregister().then(() => {
            window.location.reload();
          });
        });
      } else {
        registerValidSW(swUrl, config);
      }
    })
    .catch(() => {
      console.log('[SW] No internet connection. Running in offline mode.');
    });
}

/**
 * Unregister Service Worker
 */
export function unregister() {
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.ready
      .then((registration) => {
        registration.unregister();
        console.log('[SW] Service Worker unregistered');
      })
      .catch((error) => {
        console.error('[SW] Service Worker unregistration failed:', error);
      });
  }
}

/**
 * Check for Service Worker updates
 */
export function checkForUpdates() {
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.ready.then((registration) => {
      registration.update();
    });
  }
}

/**
 * Skip waiting and activate new Service Worker immediately
 */
export function skipWaiting() {
  if ('serviceWorker' in navigator && navigator.serviceWorker.controller) {
    navigator.serviceWorker.controller.postMessage('skipWaiting');
    window.location.reload();
  }
}

/**
 * Clear all caches
 */
export function clearCache() {
  if ('serviceWorker' in navigator && navigator.serviceWorker.controller) {
    navigator.serviceWorker.controller.postMessage('clearCache');
  }
}
