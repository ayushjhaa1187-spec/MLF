/**
 * MLF Top-Level Navigation Router & Frame Synchronizer
 * Enables deep-linking, URL hash preservation, and cross-frame state tracking.
 */
(function() {
    'use strict';

    const iframe = document.getElementById('contentFrame');
    const sidebar = document.getElementById('sidebar');
    const menuToggle = document.getElementById('menuToggle');
    const navLinks = document.querySelectorAll('.nav-link');

    // Route map from hash to iframe URL
    const routeMap = {
        'home': 'home.html',
        'start-here': 'start_here.html',
        'visual-labs': 'visual_labs.html',
        'concept-atlas': 'concept_atlas.html',
        'problem-bank': 'practice/solved_problems.html',
        'exam-centre': 'exam_centre.html',
        'revision': 'revision.html',
        'progress': 'progress.html'
    };

    // Add week routes
    for (let i = 1; i <= 12; i++) {
        routeMap[`week-${i}`] = `week-${i}/week-${i}.html`;
        routeMap[`week-${i}-summary`] = `week-${i}/summary.html`;
    }

    function parseHash() {
        const hash = window.location.hash.replace(/^#\/?/, '').trim();
        if (!hash) return { route: 'home', params: '' };
        
        const [route, params] = hash.split('?');
        return { route, params: params ? '?' + params : '' };
    }

    function navigateToHash() {
        if (!iframe) return;
        const { route, params } = parseHash();
        let targetUrl = routeMap[route] || 'home.html';
        
        if (params) {
            targetUrl += params;
        }

        // Avoid reloading if iframe is already on target
        try {
            const currentIframePath = iframe.contentWindow.location.pathname;
            if (!currentIframePath.endsWith(targetUrl.split('?')[0])) {
                iframe.src = targetUrl;
            }
        } catch (e) {
            // cross-origin or initial load
            iframe.src = targetUrl;
        }

        updateActiveSidebar(route);
    }

    function updateActiveSidebar(route) {
        navLinks.forEach(link => {
            const href = link.getAttribute('href') || '';
            const dataRoute = link.getAttribute('data-route') || '';
            
            const isMatch = (dataRoute && dataRoute === route) ||
                            (routeMap[route] && href.includes(routeMap[route].split('?')[0])) ||
                            (route === 'home' && href.endsWith('home.html'));

            if (isMatch) {
                link.classList.add('active');
            } else {
                link.classList.remove('active');
            }
        });
    }

    // Hash change event listener
    window.addEventListener('hashchange', navigateToHash);

    // Initial navigation on load
    window.addEventListener('DOMContentLoaded', () => {
        navigateToHash();

        // Listen for postMessage from child frames to update parent hash
        window.addEventListener('message', (event) => {
            if (event.data && event.data.type === 'MLF_NAVIGATE') {
                const targetHash = event.data.hash;
                if (targetHash) {
                    window.location.hash = targetHash;
                }
            }
        });

        // Sidebar link clicks update hash directly
        navLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                const dataRoute = link.getAttribute('data-route');
                if (dataRoute) {
                    e.preventDefault();
                    window.location.hash = dataRoute;
                }
                if (window.innerWidth <= 900 && sidebar) {
                    sidebar.classList.remove('show');
                }
            });
        });

        // Mobile drawer toggle
        if (menuToggle && sidebar) {
            menuToggle.addEventListener('click', () => {
                sidebar.classList.toggle('show');
            });
        }
    });

})();
