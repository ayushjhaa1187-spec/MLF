/**
 * MLF Dynamic Problem Bank Engine
 * Handles filtering, progressive hint disclosure, solution toggling,
 * multiple-choice self-checking, and persistent progress via MLFProgress.
 */
(function(window) {
    'use strict';

    let allQuestions = [];
    let currentWeek = 'all';
    let currentPlatform = 'all';
    let currentDifficulty = 'all';
    let searchKeyword = '';

    const container = document.getElementById('problemsContainer');
    const totalCountEl = document.getElementById('totalQuestionsCount');
    const solvedCountEl = document.getElementById('solvedQuestionsCount');
    const noResultsEl = document.getElementById('noResults');

    function initProblemBank() {
        // Read URL query parameters (?week=X, ?platform=Y)
        const params = new URLSearchParams(window.location.search);
        if (params.get('week')) currentWeek = params.get('week');
        if (params.get('platform')) currentPlatform = params.get('platform');

        // Fetch questions data
        fetch('../data/questions/all_questions.json')
            .then(res => {
                if (!res.ok) throw new Error('Network response not ok');
                return res.json();
            })
            .then(data => {
                allQuestions = data;
                setupFilters();
                renderQuestions();
            })
            .catch(err => {
                console.warn('Could not fetch questions JSON (likely file:// protocol or offline). Loading fallback.', err);
                // If DOM already contains fallback cards, bind interactions to them
                bindStaticCardInteractions();
            });

        // Listen for progress store updates
        window.addEventListener('mlf-progress-updated', updateStats);
    }

    function setupFilters() {
        // Week filter pills
        const weekBtns = document.querySelectorAll('#weekFilter button');
        weekBtns.forEach(btn => {
            if (btn.getAttribute('data-val') === currentWeek) {
                weekBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
            }
            btn.addEventListener('click', () => {
                weekBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                currentWeek = btn.getAttribute('data-val');
                renderQuestions();
            });
        });

        // Platform filter pills
        const platBtns = document.querySelectorAll('#platformFilter button');
        platBtns.forEach(btn => {
            if (btn.getAttribute('data-val') === currentPlatform) {
                platBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
            }
            btn.addEventListener('click', () => {
                platBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                currentPlatform = btn.getAttribute('data-val');
                renderQuestions();
            });
        });

        // Search input
        const searchInput = document.getElementById('searchInput');
        if (searchInput) {
            searchInput.addEventListener('input', (e) => {
                searchKeyword = e.target.value.toLowerCase().trim();
                renderQuestions();
            });
        }
    }

    function renderQuestions() {
        if (!container) return;

        const filtered = allQuestions.filter(q => {
            const matchWeek = (currentWeek === 'all' || String(q.week) === currentWeek);
            const matchPlat = (currentPlatform === 'all' || q.platform === currentPlatform);
            const matchDiff = (currentDifficulty === 'all' || q.difficulty === currentDifficulty);
            const textToSearch = (q.title + ' ' + q.question + ' ' + (q.citation || '')).toLowerCase();
            const matchSearch = (!searchKeyword || textToSearch.includes(searchKeyword));
            return matchWeek && matchPlat && matchDiff && matchSearch;
        });

        if (filtered.length === 0) {
            container.innerHTML = '';
            if (noResultsEl) noResultsEl.classList.remove('d-none');
        } else {
            if (noResultsEl) noResultsEl.classList.add('d-none');
            container.innerHTML = filtered.map(q => createQuestionCardHTML(q)).join('');
            bindDynamicCardEvents();
            
            // Typeset KaTeX
            if (window.renderMLFMath) {
                window.renderMLFMath(container);
            }
            // Highlight Prism code
            if (window.Prism) {
                window.Prism.highlightAllUnder(container);
            }
        }

        if (totalCountEl) totalCountEl.innerText = filtered.length;
        updateStats();
    }

    function createQuestionCardHTML(q) {
        const isSolved = window.MLFProgress ? window.MLFProgress.isProblemSolved(q.id) : false;
        
        let platformBadge = '<span class="badge bg-primary">IIT Madras BS</span>';
        if (q.platform === 'deepml') {
            platformBadge = '<span class="badge bg-success">🤖 Deep-ML</span>';
        } else if (q.platform === 'leetcode') {
            platformBadge = '<span class="badge bg-warning text-dark">💻 LeetCode</span>';
        }

        let provBadge = '';
        if (q.provenance === 'verified-pyq') {
            provBadge = '<span class="badge bg-info text-dark ms-1"><i class="fas fa-check-circle me-1"></i>Verified PYQ</span>';
        } else if (q.provenance === 'adapted') {
            provBadge = '<span class="badge bg-secondary ms-1">Adapted</span>';
        }

        const externalLinkBtn = q.url ? `
            <a href="${q.url}" target="_blank" rel="noopener noreferrer" class="btn btn-sm btn-outline-primary ms-auto">
                <i class="fas fa-external-link-alt me-1"></i> Open on ${q.platform === 'deepml' ? 'Deep-ML' : 'LeetCode'}
            </a>` : '';

        // Options HTML if MCQ
        let optionsHTML = '';
        if (q.options && q.options.length > 0) {
            optionsHTML = `
                <div class="mcq-options mt-3" data-qid="${q.id}" data-correct="${q.answer}">
                    ${q.options.map(opt => {
                        const optKey = opt.trim().charAt(0);
                        return `
                            <button class="btn btn-outline-secondary btn-sm d-block text-start w-100 mb-2 mcq-opt-btn" data-opt="${optKey}">
                                ${opt}
                            </button>
                        `;
                    }).join('')}
                    <div class="mcq-feedback mt-2 d-none fw-semibold"></div>
                </div>
            `;
        }

        // Hints HTML
        let hintsHTML = '';
        if (q.hints && q.hints.length > 0) {
            hintsHTML = `
                <div class="hints-container mt-3">
                    <button class="btn btn-sm btn-outline-warning show-hint-btn" data-hint-idx="0">
                        <i class="fas fa-lightbulb me-1"></i> Need a Hint? (1/${q.hints.length})
                    </button>
                    <div class="hint-box alert alert-warning mt-2 d-none p-2 small"></div>
                </div>
            `;
        }

        // Solution block
        let solutionContent = q.explanation || '';
        if (q.solution_code) {
            solutionContent += `
                <div class="mt-2">
                    <pre><code class="language-python">${escapeHTML(q.solution_code)}</code></pre>
                </div>
            `;
        }

        return `
            <div class="card problem-card mb-4 border-0 shadow-sm ${isSolved ? 'solved-card' : ''}" id="card-${q.id}" data-id="${q.id}" data-week="${q.week}" data-platform="${q.platform}">
                <div class="card-header bg-white py-3 d-flex flex-wrap align-items-center gap-2 border-bottom">
                    ${platformBadge}
                    ${provBadge}
                    <span class="badge bg-light text-dark border">Week ${q.week}</span>
                    <span class="badge bg-light text-muted border">${q.difficulty || 'Medium'}</span>
                    ${externalLinkBtn}
                    <div class="form-check ms-auto">
                        <input class="form-check-input solve-checkbox" type="checkbox" id="check-${q.id}" ${isSolved ? 'checked' : ''} data-qid="${q.id}">
                        <label class="form-check-label small fw-semibold text-muted" for="check-${q.id}">
                            Solved
                        </label>
                    </div>
                </div>
                <div class="card-body p-4">
                    <h5 class="fw-bold mb-2">${escapeHTML(q.title)}</h5>
                    ${q.citation ? `<div class="text-muted small mb-3 fst-italic"><i class="fas fa-bookmark me-1 text-primary"></i>${escapeHTML(q.citation)}</div>` : ''}
                    <div class="problem-statement mb-3">
                        ${q.question}
                    </div>
                    ${optionsHTML}
                    ${hintsHTML}
                    <div class="mt-4 pt-3 border-top">
                        <button class="btn btn-sm btn-outline-secondary toggle-sol-btn" type="button" data-bs-toggle="collapse" data-bs-target="#sol-${q.id}">
                            <i class="fas fa-eye me-1"></i> Reveal Derivation & Solution
                        </button>
                        <div class="collapse mt-3" id="sol-${q.id}">
                            <div class="p-3 bg-light rounded border border-light-subtle solution-body">
                                <h6 class="fw-bold text-success mb-2"><i class="fas fa-check-circle me-1"></i> Complete Solution & Derivation</h6>
                                ${solutionContent}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    function bindDynamicCardEvents() {
        // Solved checkboxes
        document.querySelectorAll('.solve-checkbox').forEach(cb => {
            cb.addEventListener('change', (e) => {
                const qid = e.target.getAttribute('data-qid');
                if (window.MLFProgress) {
                    window.MLFProgress.setProblemSolved(qid, e.target.checked);
                }
                const card = document.getElementById('card-' + qid);
                if (card) card.classList.toggle('solved-card', e.target.checked);
                updateStats();
            });
        });

        // MCQ check buttons
        document.querySelectorAll('.mcq-options').forEach(group => {
            const correctOpt = group.getAttribute('data-correct');
            const feedback = group.querySelector('.mcq-feedback');
            group.querySelectorAll('.mcq-opt-btn').forEach(btn => {
                btn.addEventListener('click', () => {
                    const chosen = btn.getAttribute('data-opt');
                    group.querySelectorAll('.mcq-opt-btn').forEach(b => {
                        b.classList.remove('btn-success', 'btn-danger');
                        b.classList.add('btn-outline-secondary');
                    });
                    if (chosen === correctOpt) {
                        btn.classList.remove('btn-outline-secondary');
                        btn.classList.add('btn-success');
                        feedback.innerHTML = '<span class="text-success"><i class="fas fa-check me-1"></i> Correct!</span>';
                        feedback.classList.remove('d-none');
                        // auto check solved
                        const qid = group.getAttribute('data-qid');
                        const cb = document.getElementById('check-' + qid);
                        if (cb && !cb.checked) {
                            cb.checked = true;
                            cb.dispatchEvent(new Event('change'));
                        }
                    } else {
                        btn.classList.remove('btn-outline-secondary');
                        btn.classList.add('btn-danger');
                        feedback.innerHTML = '<span class="text-danger"><i class="fas fa-times me-1"></i> Incorrect. Review the hints or derivation!</span>';
                        feedback.classList.remove('d-none');
                    }
                });
            });
        });

        // Progressive Hints
        document.querySelectorAll('.hints-container').forEach(hc => {
            const btn = hc.querySelector('.show-hint-btn');
            const hintBox = hc.querySelector('.hint-box');
            const card = hc.closest('.problem-card');
            const qid = card ? card.getAttribute('data-id') : null;
            const q = allQuestions.find(item => item.id === qid);
            if (!q || !q.hints) return;

            let currentIdx = 0;
            btn.addEventListener('click', () => {
                hintBox.classList.remove('d-none');
                hintBox.innerHTML = `<strong>Hint ${currentIdx + 1}:</strong> ${q.hints[currentIdx]}`;
                if (window.renderMLFMath) window.renderMLFMath(hintBox);
                
                currentIdx++;
                if (currentIdx < q.hints.length) {
                    btn.innerHTML = `<i class="fas fa-lightbulb me-1"></i> Next Hint (${currentIdx + 1}/${q.hints.length})`;
                } else {
                    btn.classList.add('d-none');
                }
            });
        });
    }

    function bindStaticCardInteractions() {
        // Fallback for static cards in HTML if JSON fetch fails
        document.querySelectorAll('.problem-card').forEach(card => {
            const qid = card.id || 'stat-' + Math.random().toString(36).substr(2, 5);
            const isSolved = window.MLFProgress ? window.MLFProgress.isProblemSolved(qid) : false;
            if (isSolved) card.classList.add('solved-card');
        });
    }

    function updateStats() {
        if (!window.MLFProgress || !solvedCountEl) return;
        const stats = window.MLFProgress.getStats();
        solvedCountEl.innerText = stats.problemsSolvedCount;
    }

    function escapeHTML(str) {
        if (!str) return '';
        return str.replace(/[&<>'"]/g, 
            tag => ({
                '&': '&amp;',
                '<': '&lt;',
                '>': '&gt;',
                "'": '&#39;',
                '"': '&quot;'
            }[tag] || tag)
        );
    }

    document.addEventListener('DOMContentLoaded', initProblemBank);
})(window);
