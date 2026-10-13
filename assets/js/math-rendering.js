/**
 * MLF KaTeX Mathematical Typesetting Initialization Helper
 * Handles inline ($...$) and display ($$...$$) KaTeX delimiters safely.
 */
(function(window) {
    'use strict';

    function renderMLFMath(element) {
        if (typeof renderMathInElement !== 'function') {
            return;
        }

        const target = element || document.body;
        try {
            renderMathInElement(target, {
                delimiters: [
                    { left: '$$', right: '$$', display: true },
                    { left: '$', right: '$', display: false },
                    { left: '\\[', right: '\\]', display: true },
                    { left: '\\(', right: '\\)', display: false }
                ],
                throwOnError: false,
                ignoredTags: ['script', 'noscript', 'style', 'textarea', 'pre', 'code']
            });
        } catch (err) {
            console.warn('KaTeX rendering error caught:', err);
        }
    }

    document.addEventListener('DOMContentLoaded', function() {
        renderMLFMath();
    });

    window.renderMLFMath = renderMLFMath;
})(window);
