/**
 * Antigravity Web UI Translator (MutationObserver)
 * This script is injected into the preload.js of the main window.
 * It observes DOM changes and translates predefined English strings to Chinese.
 * Updated to support Shadow DOM and input values.
 */

(function () {
  // Wait for the window to load before starting the observer
  window.addEventListener('DOMContentLoaded', () => {
    // These translations will be injected by the patcher script
    const TRANSLATIONS = window.__AGY_WEBUI_TRANSLATIONS || { exact: {}, regex: {} };
    
    // Compile regexes
    const regexes = [];
    for (const [pattern, replacement] of Object.entries(TRANSLATIONS.regex || {})) {
      try {
        regexes.push({
          re: new RegExp(pattern),
          rep: replacement
        });
      } catch (e) {
        console.warn('Invalid translation regex:', pattern);
      }
    }

    const MARKER = '__agy_translated';

    function translateText(text) {
      if (!text || typeof text !== 'string') return text;
      const t = text.trim();
      if (!t) return text;

      // Exact match
      if (TRANSLATIONS.exact && TRANSLATIONS.exact[t]) {
        return text.replace(t, TRANSLATIONS.exact[t]);
      }

      // Regex match
      for (const item of regexes) {
        if (item.re.test(text)) {
          return text.replace(item.re, item.rep);
        }
      }

      return text;
    }

    function translateNode(node) {
      if (node.nodeType === Node.TEXT_NODE) {
        const parent = node.parentElement;
        if (parent && parent.tagName !== 'SCRIPT' && parent.tagName !== 'STYLE') {
          const newText = translateText(node.nodeValue);
          if (newText !== node.nodeValue) {
            node.nodeValue = newText;
          }
        }
      } else if (node.nodeType === Node.ELEMENT_NODE) {
        if (node[MARKER] || node.tagName === 'SCRIPT' || node.tagName === 'STYLE') return;
        node[MARKER] = true;

        // Translate standard attributes
        ['placeholder', 'title', 'aria-label', 'data-tooltip', 'aria-description'].forEach(attr => {
          if (node.hasAttribute(attr)) {
            const val = node.getAttribute(attr);
            const newVal = translateText(val);
            if (newVal !== val) {
              node.setAttribute(attr, newVal);
            }
          }
        });

        // Translate button values
        if (node.tagName === 'INPUT' && ['button', 'submit', 'reset'].includes(node.type)) {
          const val = node.value;
          const newVal = translateText(val);
          if (newVal !== val) {
            node.value = newVal;
          }
        }

        // Recursively translate children
        if (node.childNodes) {
          node.childNodes.forEach(translateNode);
        }
        
        // Translate existing shadow roots
        if (node.shadowRoot) {
          observeRoot(node.shadowRoot);
          node.shadowRoot.childNodes.forEach(translateNode);
        }
      }
    }

    const observer = new MutationObserver((mutations) => {
      // Disconnect temporarily to avoid infinite loops when we modify text
      observer.disconnect();
      
      for (const mutation of mutations) {
        if (mutation.type === 'childList') {
          mutation.addedNodes.forEach(node => translateNode(node));
        } else if (mutation.type === 'characterData') {
          translateNode(mutation.target);
        }
      }
      
      // Reconnect to all observed roots
      observedRoots.forEach(root => {
        observer.observe(root, {
          childList: true,
          subtree: true,
          characterData: true
        });
      });
    });

    const observedRoots = new Set();
    
    function observeRoot(root) {
      if (observedRoots.has(root)) return;
      observedRoots.add(root);
      observer.observe(root, {
        childList: true,
        subtree: true,
        characterData: true
      });
    }

    // Hook attachShadow to automatically observe new shadow roots
    const originalAttachShadow = Element.prototype.attachShadow;
    Element.prototype.attachShadow = function() {
      const shadowRoot = originalAttachShadow.apply(this, arguments);
      observeRoot(shadowRoot);
      return shadowRoot;
    };

    // Initial translation pass
    translateNode(document.body);

    // Start observing document body
    observeRoot(document.body);
    
    console.log('[Antigravity-Chinese-Patch] Web UI translator initialized (with Shadow DOM support).');
  });
})();
