import React from "react";
import ReactDOM from "react-dom/client";
import "@/index.css";
import App from "@/App";
import { initWebVitals } from "@/utils/webVitals";
import * as serviceWorkerRegistration from "./serviceWorkerRegistration";

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);

// PHASE D: Initialize Web Vitals reporting
initWebVitals();

// PHASE F: Register Service Worker for caching
serviceWorkerRegistration.register({
  onUpdate: (registration) => {
    console.log('[App] New version available. Refresh to update.');
  },
  onSuccess: (registration) => {
    console.log('[App] Content cached for offline use.');
  }
});

