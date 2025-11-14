// NCTracker Theme Toggle Handler
// Manages dark/light mode with localStorage persistence

(function() {
    'use strict';
    
    // Get theme from localStorage or default to dark
    function getStoredTheme() {
        return localStorage.getItem('nctracker-theme') || 'dark';
    }
    
    // Set theme on document
    function setTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('nctracker-theme', theme);
        
        // Notify Streamlit
        if (window.parent && window.parent.postMessage) {
            window.parent.postMessage({
                type: 'streamlit:setComponentValue',
                value: theme
            }, '*');
        }
    }
    
    // Initialize theme on load
    function initTheme() {
        const theme = getStoredTheme();
        setTheme(theme);
    }
    
    // Listen for theme change messages from Streamlit
    window.addEventListener('message', function(event) {
        if (event.data && event.data.type === 'nctracker:setTheme') {
            setTheme(event.data.theme);
        }
    });
    
    // Initialize on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initTheme);
    } else {
        initTheme();
    }
    
    // Expose toggle function
    window.toggleTheme = function() {
        const current = getStoredTheme();
        const newTheme = current === 'dark' ? 'light' : 'dark';
        setTheme(newTheme);
        return newTheme;
    };
    
    // Expose getter
    window.getCurrentTheme = getStoredTheme;
})();
