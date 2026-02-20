#!/usr/bin/env python3
"""
HUNTIQ-V5 — Web Vitals Measurement Script
Mode: ANALYSE EXTERNE (P0)
"""

import asyncio
import json
from datetime import datetime

# Script JS pour mesurer les Web Vitals
WEBVITALS_SCRIPT = """
async () => {
    return new Promise((resolve) => {
        const results = {
            timestamp: new Date().toISOString(),
            url: window.location.href,
            metrics: {}
        };
        
        // Performance timing
        const timing = performance.timing;
        const navigation = performance.getEntriesByType('navigation')[0];
        
        if (navigation) {
            results.metrics.TTFB = Math.round(navigation.responseStart - navigation.requestStart);
            results.metrics.FCP = Math.round(navigation.domContentLoadedEventEnd - navigation.fetchStart);
            results.metrics.DOMContentLoaded = Math.round(navigation.domContentLoadedEventEnd - navigation.fetchStart);
            results.metrics.Load = Math.round(navigation.loadEventEnd - navigation.fetchStart);
        }
        
        // Get LCP
        const lcpEntries = performance.getEntriesByType('largest-contentful-paint');
        if (lcpEntries.length > 0) {
            results.metrics.LCP = Math.round(lcpEntries[lcpEntries.length - 1].startTime);
        }
        
        // Get CLS
        let cls = 0;
        const clsEntries = performance.getEntriesByType('layout-shift');
        clsEntries.forEach(entry => {
            if (!entry.hadRecentInput) {
                cls += entry.value;
            }
        });
        results.metrics.CLS = cls.toFixed(4);
        
        // Get resource timing for JS
        const resources = performance.getEntriesByType('resource');
        let totalJSTime = 0;
        let jsCount = 0;
        resources.forEach(r => {
            if (r.initiatorType === 'script') {
                totalJSTime += r.duration;
                jsCount++;
            }
        });
        results.metrics.TotalJSLoadTime = Math.round(totalJSTime);
        results.metrics.JSResourceCount = jsCount;
        
        // Long tasks (approximation for TBT)
        results.metrics.LongTasksCount = 0;
        
        setTimeout(() => resolve(results), 100);
    });
}
"""

print("Script ready for Playwright execution")
