import React from "react";
import ReactDOM from "react-dom/client";

// BRANCHE 2: Inject Critical CSS BEFORE main styles
import { injectCriticalCSS, removeCriticalCSS } from "@/utils/criticalCSS";
injectCriticalCSS();

import "@/index.css";
import App from "@/App";
import { initWebVitals } from "@/utils/webVitals";
import { initPerformanceOptimizations } from "@/utils/performanceOptimizations";
import { initAccessibilityEnhancements } from "@/utils/accessibilityEnhancements";
import * as serviceWorkerRegistration from "./serviceWorkerRegistration";

// BRANCHE 3: Import advanced optimizations
import { initImageOptimization } from "@/utils/imageCDN";
import { initHTTP3Optimization } from "@/utils/http3Optimization";
import { initSSRConfig } from "@/utils/ssrConfig";
import { preloadCriticalRoutes } from "@/utils/routePreloader";

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);

// BRANCHE 2: Remove Critical CSS after main styles load
removeCriticalCSS();

// PHASE D: Initialize Web Vitals reporting
initWebVitals();

// POLISH FINAL: Performance optimizations
initPerformanceOptimizations();

// POLISH FINAL: Accessibility enhancements (WCAG AAA)
initAccessibilityEnhancements();

// BRANCHE 3: Advanced optimizations
initImageOptimization();
initHTTP3Optimization();
initSSRConfig();
preloadCriticalRoutes();

// BRANCHE 3: Register Service Worker V2 for advanced caching
serviceWorkerRegistration.register({
  onUpdate: (registration) => {
    console.log('[App] New version available. Refresh to update.');
  },
  onSuccess: (registration) => {
    console.log('[App] Content cached for offline use.');
  }
});
