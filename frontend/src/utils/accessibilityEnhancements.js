/**
 * Accessibility Enhancements - BRANCHE 1 POLISH FINAL
 * 
 * WCAG 2.2 AAA Polish - Focus states, contrastes, ARIA, navigation clavier
 * Conforme aux exigences BIONIC V5
 * 
 * @module accessibilityEnhancements
 * @version 1.0.0
 * @phase POLISH_FINAL
 */

/**
 * Focus Management
 * Améliore la visibilité du focus pour la navigation clavier
 */
export const enhanceFocusVisibility = () => {
  if (typeof document === 'undefined') return;

  // Add focus-visible polyfill behavior
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Tab') {
      document.body.classList.add('keyboard-navigation');
    }
  });

  document.addEventListener('mousedown', () => {
    document.body.classList.remove('keyboard-navigation');
  });

  // Inject enhanced focus styles
  const style = document.createElement('style');
  style.textContent = `
    /* WCAG AAA Focus Enhancement */
    .keyboard-navigation *:focus {
      outline: 3px solid #f5a623 !important;
      outline-offset: 2px !important;
      box-shadow: 0 0 0 6px rgba(245, 166, 35, 0.3) !important;
    }
    
    .keyboard-navigation *:focus:not(:focus-visible) {
      outline: none !important;
      box-shadow: none !important;
    }
    
    .keyboard-navigation *:focus-visible {
      outline: 3px solid #f5a623 !important;
      outline-offset: 2px !important;
      box-shadow: 0 0 0 6px rgba(245, 166, 35, 0.3) !important;
    }
    
    /* Skip Link Enhancement */
    .skip-link {
      position: absolute;
      top: -40px;
      left: 0;
      background: #f5a623;
      color: #000;
      padding: 8px 16px;
      z-index: 10000;
      font-weight: bold;
      transition: top 0.2s;
    }
    
    .skip-link:focus {
      top: 0;
    }
    
    /* High Contrast Mode Support */
    @media (prefers-contrast: high) {
      *:focus {
        outline: 4px solid currentColor !important;
        outline-offset: 3px !important;
      }
      
      button, a, input, select, textarea {
        border: 2px solid currentColor !important;
      }
    }
    
    /* Reduced Motion Support */
    @media (prefers-reduced-motion: reduce) {
      *, *::before, *::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
        scroll-behavior: auto !important;
      }
    }
  `;
  document.head.appendChild(style);
};

/**
 * Skip Link Injection
 * Ajoute un lien "Skip to main content" pour la navigation clavier
 */
export const injectSkipLink = () => {
  if (typeof document === 'undefined') return;
  
  // Check if skip link already exists
  if (document.querySelector('.skip-link')) return;

  const skipLink = document.createElement('a');
  skipLink.href = '#main-content';
  skipLink.className = 'skip-link';
  skipLink.textContent = 'Aller au contenu principal';
  skipLink.setAttribute('aria-label', 'Aller au contenu principal');
  
  document.body.insertBefore(skipLink, document.body.firstChild);
  
  // Ensure main content has id
  const main = document.querySelector('main') || document.querySelector('[role="main"]');
  if (main && !main.id) {
    main.id = 'main-content';
  }
};

/**
 * ARIA Live Region Manager
 * Gère les annonces dynamiques pour les screen readers
 */
class AriaLiveAnnouncer {
  constructor() {
    this.container = null;
    this.init();
  }

  init() {
    if (typeof document === 'undefined') return;
    
    // Create live region container
    this.container = document.createElement('div');
    this.container.setAttribute('role', 'status');
    this.container.setAttribute('aria-live', 'polite');
    this.container.setAttribute('aria-atomic', 'true');
    this.container.className = 'sr-only';
    this.container.style.cssText = `
      position: absolute;
      width: 1px;
      height: 1px;
      padding: 0;
      margin: -1px;
      overflow: hidden;
      clip: rect(0, 0, 0, 0);
      white-space: nowrap;
      border: 0;
    `;
    
    document.body.appendChild(this.container);
  }

  announce(message, priority = 'polite') {
    if (!this.container) return;
    
    this.container.setAttribute('aria-live', priority);
    this.container.textContent = '';
    
    // Use setTimeout to ensure the change is announced
    setTimeout(() => {
      this.container.textContent = message;
    }, 100);
  }

  announcePolite(message) {
    this.announce(message, 'polite');
  }

  announceAssertive(message) {
    this.announce(message, 'assertive');
  }
}

export const ariaAnnouncer = new AriaLiveAnnouncer();

/**
 * Keyboard Navigation Enhancements
 * Améliore la navigation clavier sur les composants interactifs
 */
export const enhanceKeyboardNavigation = () => {
  if (typeof document === 'undefined') return;

  // Handle Escape key to close modals/dialogs
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      // Find and close any open modal
      const modals = document.querySelectorAll('[role="dialog"][aria-modal="true"]');
      modals.forEach(modal => {
        const closeBtn = modal.querySelector('[aria-label*="fermer"], [aria-label*="close"], .close-button');
        if (closeBtn) {
          closeBtn.click();
        }
      });
    }
  });

  // Arrow key navigation for menus
  document.addEventListener('keydown', (e) => {
    const activeElement = document.activeElement;
    const menu = activeElement?.closest('[role="menu"], [role="menubar"], [role="listbox"]');
    
    if (!menu) return;
    
    const items = Array.from(menu.querySelectorAll('[role="menuitem"], [role="option"]:not([aria-disabled="true"])'));
    const currentIndex = items.indexOf(activeElement);
    
    if (currentIndex === -1) return;
    
    let nextIndex;
    switch (e.key) {
      case 'ArrowDown':
      case 'ArrowRight':
        e.preventDefault();
        nextIndex = (currentIndex + 1) % items.length;
        items[nextIndex]?.focus();
        break;
      case 'ArrowUp':
      case 'ArrowLeft':
        e.preventDefault();
        nextIndex = (currentIndex - 1 + items.length) % items.length;
        items[nextIndex]?.focus();
        break;
      case 'Home':
        e.preventDefault();
        items[0]?.focus();
        break;
      case 'End':
        e.preventDefault();
        items[items.length - 1]?.focus();
        break;
    }
  });
};

/**
 * Color Contrast Enhancement
 * Détecte et avertit sur les problèmes de contraste
 */
export const checkContrastRatio = (foreground, background) => {
  const getLuminance = (hex) => {
    const rgb = hex.match(/^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i);
    if (!rgb) return 0;
    
    const [, r, g, b] = rgb.map(x => {
      const val = parseInt(x, 16) / 255;
      return val <= 0.03928 ? val / 12.92 : Math.pow((val + 0.055) / 1.055, 2.4);
    });
    
    return 0.2126 * r + 0.7152 * g + 0.0722 * b;
  };

  const l1 = getLuminance(foreground);
  const l2 = getLuminance(background);
  const ratio = (Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05);

  return {
    ratio: ratio.toFixed(2),
    passesAA: ratio >= 4.5,
    passesAALarge: ratio >= 3,
    passesAAA: ratio >= 7,
    passesAAALarge: ratio >= 4.5
  };
};

/**
 * Form Accessibility Enhancement
 * Améliore l'accessibilité des formulaires
 */
export const enhanceFormAccessibility = () => {
  if (typeof document === 'undefined') return;

  // Auto-associate labels with inputs
  const inputs = document.querySelectorAll('input:not([aria-label]):not([aria-labelledby])');
  
  inputs.forEach(input => {
    // Find associated label
    const id = input.id;
    if (id) {
      const label = document.querySelector(`label[for="${id}"]`);
      if (label) {
        // Already properly associated
        return;
      }
    }
    
    // Check for wrapping label
    const parentLabel = input.closest('label');
    if (parentLabel && !input.id) {
      const labelId = `label-${Math.random().toString(36).slice(2, 9)}`;
      parentLabel.id = labelId;
      input.setAttribute('aria-labelledby', labelId);
    }
    
    // Check placeholder and add aria-label if needed
    const placeholder = input.getAttribute('placeholder');
    if (placeholder && !input.getAttribute('aria-label')) {
      input.setAttribute('aria-label', placeholder);
    }
  });

  // Add required indicators
  const requiredInputs = document.querySelectorAll('[required]:not([aria-required])');
  requiredInputs.forEach(input => {
    input.setAttribute('aria-required', 'true');
  });
};

/**
 * Initialize All Accessibility Enhancements
 */
export const initAccessibilityEnhancements = () => {
  if (typeof window === 'undefined') return;

  // Run on DOM ready
  const init = () => {
    enhanceFocusVisibility();
    injectSkipLink();
    enhanceKeyboardNavigation();
    enhanceFormAccessibility();
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
};

export default {
  enhanceFocusVisibility,
  injectSkipLink,
  ariaAnnouncer,
  enhanceKeyboardNavigation,
  checkContrastRatio,
  enhanceFormAccessibility,
  initAccessibilityEnhancements
};
