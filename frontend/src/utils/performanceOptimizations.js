/**
 * Performance Optimizations - BRANCHE 1 POLISH FINAL
 * 
 * Micro-optimisations CPU Main Thread et détection des tâches longues
 * Conforme aux exigences BIONIC V5
 * 
 * @module performanceOptimizations
 * @version 1.0.0
 * @phase POLISH_FINAL
 */

/**
 * Long Task Observer
 * Détecte et rapporte les tâches > 50ms qui bloquent le main thread
 */
export const initLongTaskObserver = () => {
  if (typeof window === 'undefined' || !('PerformanceObserver' in window)) {
    return;
  }

  try {
    const observer = new PerformanceObserver((list) => {
      for (const entry of list.getEntries()) {
        // Log long tasks in development
        if (process.env.NODE_ENV === 'development') {
          console.warn('[Performance] Long task detected:', {
            duration: `${entry.duration.toFixed(2)}ms`,
            startTime: `${entry.startTime.toFixed(2)}ms`,
            name: entry.name
          });
        }
      }
    });

    observer.observe({ entryTypes: ['longtask'] });
  } catch {
    // PerformanceObserver for longtask not supported
  }
};

/**
 * Passive Event Listeners
 * Améliore le scroll performance en rendant les listeners passifs
 */
export const upgradePassiveListeners = () => {
  if (typeof window === 'undefined') return;

  // Test passive support
  let supportsPassive = false;
  try {
    const opts = Object.defineProperty({}, 'passive', {
      get: function() {
        supportsPassive = true;
        return true;
      }
    });
    window.addEventListener('testPassive', null, opts);
    window.removeEventListener('testPassive', null, opts);
  } catch (e) {
    supportsPassive = false;
  }

  // Upgrade scroll, wheel, and touch listeners
  if (supportsPassive) {
    const originalAddEventListener = EventTarget.prototype.addEventListener;
    
    EventTarget.prototype.addEventListener = function(type, listener, options) {
      const passiveEvents = ['scroll', 'wheel', 'touchstart', 'touchmove'];
      
      if (passiveEvents.includes(type)) {
        const newOptions = typeof options === 'object' 
          ? { ...options, passive: options.passive !== false }
          : { passive: true, capture: options };
        
        return originalAddEventListener.call(this, type, listener, newOptions);
      }
      
      return originalAddEventListener.call(this, type, listener, options);
    };
  }
};

/**
 * Defer Non-Critical Scripts
 * Utilise requestIdleCallback pour les scripts non critiques
 */
export const deferNonCritical = (callback, timeout = 2000) => {
  if (typeof window === 'undefined') {
    return callback();
  }

  if ('requestIdleCallback' in window) {
    return window.requestIdleCallback(callback, { timeout });
  } else {
    return setTimeout(callback, 1);
  }
};

/**
 * Preload Critical Resources
 * Précharge dynamiquement les ressources critiques
 */
export const preloadCriticalResources = () => {
  if (typeof document === 'undefined') return;

  const criticalResources = [
    { href: '/logos/bionic-logo.svg', as: 'image', type: 'image/svg+xml' },
  ];

  criticalResources.forEach(({ href, as, type }) => {
    const link = document.createElement('link');
    link.rel = 'preload';
    link.href = href;
    link.as = as;
    if (type) link.type = type;
    document.head.appendChild(link);
  });
};

/**
 * Image Loading Optimization
 * Applique le lazy loading natif aux images non-critiques
 */
export const optimizeImageLoading = () => {
  if (typeof document === 'undefined') return;

  // Find all images without explicit loading attribute
  const images = document.querySelectorAll('img:not([loading])');
  
  images.forEach((img, index) => {
    // First 3 images are considered above-the-fold
    if (index < 3) {
      img.setAttribute('loading', 'eager');
      img.setAttribute('fetchpriority', 'high');
    } else {
      img.setAttribute('loading', 'lazy');
      img.setAttribute('decoding', 'async');
    }
  });
};

/**
 * Connection-Aware Loading
 * Adapte le chargement selon la connexion
 */
export const getConnectionQuality = () => {
  if (typeof navigator === 'undefined' || !('connection' in navigator)) {
    return 'unknown';
  }

  const connection = navigator.connection;
  
  if (connection.saveData) return 'save-data';
  if (connection.effectiveType === '4g' && connection.downlink > 5) return 'fast';
  if (connection.effectiveType === '4g') return 'good';
  if (connection.effectiveType === '3g') return 'moderate';
  return 'slow';
};

/**
 * Reduce Motion Check
 * Respecte les préférences utilisateur pour les animations
 */
export const prefersReducedMotion = () => {
  if (typeof window === 'undefined') return false;
  return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
};

/**
 * Initialize All Performance Optimizations
 */
export const initPerformanceOptimizations = () => {
  // Defer non-critical optimizations
  deferNonCritical(() => {
    initLongTaskObserver();
    optimizeImageLoading();
  });

  // Critical optimizations immediately
  upgradePassiveListeners();
  preloadCriticalResources();

  // Log connection quality
  if (process.env.NODE_ENV === 'development') {
    console.log('[Performance] Connection quality:', getConnectionQuality());
    console.log('[Performance] Prefers reduced motion:', prefersReducedMotion());
  }
};

export default {
  initLongTaskObserver,
  upgradePassiveListeners,
  deferNonCritical,
  preloadCriticalResources,
  optimizeImageLoading,
  getConnectionQuality,
  prefersReducedMotion,
  initPerformanceOptimizations
};
