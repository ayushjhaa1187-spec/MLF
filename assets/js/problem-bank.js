/**
 * MLF Dynamic Problem Bank Engine
 * Handles:
 * - Multi-criteria filtering (Week, Platform, Difficulty, Search)
 * - Progressive hint disclosure (cumulative visibility)
 * - Self-checking options with granular attempt logging via MLFProgress
 * - Transparent provenance badges (verified-pyq, adapted, original)
 * - KaTeX and Prism highlighting
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
        // Read URL query parameters (?week=X, ?platform=Y, ?diff=Z)
        const params = new URLSearchParams(window.location.search);
        if (params.get('week')) currentWeek = params.get('week');
        if (params.get('platform')) currentPlatform = params.get('platform');
        if (params.get('diff')) currentDifficulty = params.get('diff').toLowerCase();

        // Fetch canonical questions data
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
                console.warn('Could not fetch questions JSON (likely file:// protocol or offline).', err);
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
            const val = btn.getAttribute('data-val');
            if (val === currentPlatform || (currentPlatform === 'local' && val === 'iitm')) {
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

        // Difficulty filter pills
        const diffBtns = document.querySelectorAll('#difficultyFilter button');
        diffBtns.forEach(btn => {
            if (btn.getAttribute('data-val') === currentDifficulty) {
                diffBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
            }
            btn.addEventListener('click', () => {
                diffBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                currentDifficulty = btn.getAttribute('data-val');
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
            // Week match
            const matchWeek = (currentWeek === 'all' || String(q.week) === currentWeek);

            // Platform match (handle local/iitm aliases)
            let qPlat = (q.platform || 'local').toLowerCase();
            if (qPlat === 'iitm') qPlat = 'local';
            let targetPlat = currentPlatform.toLowerCase();
            if (targetPlat === 'iitm') targetPlat = 'local';
            const matchPlat = (targetPlat === 'all' || qPlat === targetPlat);

            // Difficulty match
            const qDiff = (q.difficulty || 'medium').toLowerCase();
            const matchDiff = (currentDifficulty === 'all' || qDiff === currentDifficulty);

            // Search match
            const statementText = q.statement || q.question || '';
            const citationText = (q.source && q.source.citation) || q.citation || '';
            const textToSearch = (q.title + ' ' + statementText + ' ' + citationText).toLowerCase();
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

        // Platform badge
        let platformBadge = '<span class="badge bg-primary">🎓 Course Practice</span>';
        if (q.platform === 'deepml') {
            platformBadge = '<span class="badge bg-success">🤖 Deep-ML</span>';
        } else if (q.platform === 'leetcode') {
            platformBadge = '<span class="badge bg-warning text-dark">💻 LeetCode</span>';
        }

        // Provenance badge
        let provBadge = '';
        if (q.provenance === 'verified-pyq') {
            provBadge = '<span class="badge bg-info text-dark ms-1" title="Curated from previous IITM term materials"><i class="fas fa-check-circle me-1"></i>Verified PYQ</span>';
        } else if (q.provenance === 'adapted') {
            provBadge = '<span class="badge bg-secondary ms-1" title="Adapted from standard course exercise">Adapted</span>';
        } else if (q.provenance === 'original') {
            provBadge = '<span class="badge bg-light text-dark border ms-1" title="Original conceptual practice problem">Original Practice</span>';
        }

        // Difficulty badge
        const diff = (q.difficulty || 'medium').toLowerCase();
        let diffBadge = '<span class="badge bg-light text-muted border">Medium</span>';
        if (diff === 'easy') diffBadge = '<span class="badge bg-success-subtle text-success border border-success-subtle">Easy</span>';
        if (diff === 'hard') diffBadge = '<span class="badge bg-danger-subtle text-danger border border-danger-subtle">Hard</span>';

        // External Link button
        let externalUrl = (q.source && q.source.url) || q.url;
        let externalLinkBtn = '';
        if (externalUrl) {
            let label = 'Resource';
            if (q.platform === 'deepml') label = 'Deep-ML';
            else if (q.platform === 'leetcode') label = 'LeetCode';
            externalLinkBtn = `
                <a href="${externalUrl}" target="_blank" rel="noopener noreferrer" class="btn btn-sm btn-outline-primary ms-auto">
                    <i class="fas fa-external-link-alt me-1"></i> Open on ${label}
                </a>`;
        }

        // Standardize options
        let options = [];
        if (Array.isArray(q.options)) {
            options = q.options.map((opt, i) => {
                if (typeof opt === 'object' && opt !== null) {
                    return { id: opt.id || String.fromCharCode(97 + i), text: opt.text };
                }
                const optStr = String(opt);
                const m = optStr.match(/^([A-Da-d])[\.\)]\s*(.*)$/);
                if (m) {
                    return { id: m[1].toLowerCase(), text: m[2] };
                }
                return { id: String.fromCharCode(97 + i), text: optStr };
            });
        }

        // Correct answer specification
        let correctIds = [];
        if (q.answerSpec && Array.isArray(q.answerSpec.correctOptionIds)) {
            correctIds = q.answerSpec.correctOptionIds;
        } else if (q.answer) {
            correctIds = [String(q.answer).trim().toLowerCase()];
        }

        let optionsHTML = '';
        if (options.length > 0) {
            optionsHTML = `
                <div class="mcq-options mt-3" data-qid="${q.id}" data-correct="${correctIds.join(',')}">
                    ${options.map(opt => `
                        <button class="btn btn-outline-secondary btn-sm d-block text-start w-100 mb-2 mcq-opt-btn" data-opt="${opt.id}">
                            <strong class="me-2">${opt.id.toUpperCase()}.</strong> ${opt.text}
                        </button>
                    `).join('')}
                    <div class="mcq-feedback mt-2 d-none fw-semibold"></div>
                </div>
            `;
        }

        // Cumulative Progressive Hints HTML
        let hintsHTML = '';
        const hints = q.hints || [];
        if (hints.length > 0) {
            hintsHTML = `
                <div class="hints-container mt-3" data-total="${hints.length}">
                    <button class="btn btn-sm btn-outline-warning show-hint-btn" data-unlocked="0">
                        <i class="fas fa-lightbulb me-1"></i> Need a Hint? (1/${hints.length})
                    </button>
                    <div class="hints-list mt-2 d-none">
                        <!-- Unlocked hints rendered here -->
                    </div>
                </div>
            `;
        }

        // Solution content
        let solutionContent = q.solution || q.explanation || '';
        let solutionCode = (q.answerSpec && q.answerSpec.solutionCode) || q.solution_code;
        if (solutionCode) {
            solutionContent += `
                <div class="mt-3">
                    <pre><code class="language-python">${escapeHTML(solutionCode)}</code></pre>
                </div>
            `;
        }

        const citation = (q.source && q.source.citation) || q.citation;
        const statement = q.statement || q.question || '';

        return `
            <div class="card problem-card mb-4 border-0 shadow-sm ${isSolved ? 'solved-card' : ''}" id="card-${q.id}" data-id="${q.id}" data-week="${q.week}" data-platform="${q.platform || 'local'}">
                <div class="card-header bg-white py-3 d-flex flex-wrap align-items-center gap-2 border-bottom">
                    ${platformBadge}
                    ${provBadge}
                    <span class="badge bg-light text-dark border">Week ${q.week}</span>
                    ${diffBadge}
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
                    ${citation ? `<div class="text-muted small mb-3 fst-italic"><i class="fas fa-bookmark me-1 text-primary"></i>${escapeHTML(citation)}</div>` : ''}
                    <div class="problem-statement mb-3 fs-6">
                        ${statement}
                    </div>
                    ${optionsHTML}
                    ${hintsHTML}
                    <div class="mt-4 pt-3 border-top d-flex justify-content-between align-items-center flex-wrap gap-2">
                        <div class="d-flex gap-2">
                            <button class="btn btn-sm btn-outline-secondary toggle-sol-btn" type="button" data-bs-toggle="collapse" data-bs-target="#sol-${q.id}">
                                <i class="fas fa-eye me-1"></i> Reveal Derivation & Solution
                            </button>
                            <button class="btn btn-sm btn-outline-warning save-rev-btn" data-qid="${q.id}" data-week="${q.week}" data-title="${escapeHTML(q.title)}">
                                <i class="fas fa-bookmark me-1"></i> Save to Vault
                            </button>
                        </div>
                        <div class="d-flex gap-2">
                            ${q.relatedLesson ? `<a href="../${q.relatedLesson}" class="btn btn-sm btn-link text-decoration-none"><i class="fas fa-book me-1"></i> Lesson</a>` : ''}
                            ${q.relatedLab ? `<a href="../${q.relatedLab}" class="btn btn-sm btn-link text-decoration-none"><i class="fas fa-cube me-1"></i> Lab</a>` : ''}
                        </div>
                    </div>
                    <div class="collapse mt-3" id="sol-${q.id}">
                        <div class="p-3 bg-light rounded border solution-body">
                            <h6 class="fw-bold text-success mb-2"><i class="fas fa-check-circle me-1"></i> Mathematical Derivation & Solution</h6>
                            <div>${solutionContent}</div>
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

        // Save to Revision Vault buttons
        document.querySelectorAll('.save-rev-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const qid = btn.getAttribute('data-qid');
                const week = parseInt(btn.getAttribute('data-week'), 10) || 1;
                const title = btn.getAttribute('data-title') || qid;
                if (window.MLFProgress) {
                    window.MLFProgress.markNeedsRevision(qid, {
                        title: title,
                        week: week,
                        relatedLesson: `week-${week}/week-${week}.html`
                    });
                }
                btn.classList.remove('btn-outline-warning');
                btn.classList.add('btn-warning', 'text-dark');
                btn.innerHTML = '<i class="fas fa-check me-1"></i> Saved to Vault';
            });
        });

        // MCQ check buttons
        document.querySelectorAll('.mcq-options').forEach(group => {
            const rawCorrect = group.getAttribute('data-correct') || '';
            const correctOpts = rawCorrect.split(',').map(s => s.trim().toLowerCase());
            const feedback = group.querySelector('.mcq-feedback');
            const qid = group.getAttribute('data-qid');

            group.querySelectorAll('.mcq-opt-btn').forEach(btn => {
                btn.addEventListener('click', () => {
                    const chosen = (btn.getAttribute('data-opt') || '').toLowerCase();
                    group.querySelectorAll('.mcq-opt-btn').forEach(b => {
                        b.classList.remove('btn-success', 'btn-danger');
                        b.classList.add('btn-outline-secondary');
                    });

                    const isCorrect = correctOpts.includes(chosen);
                    if (isCorrect) {
                        btn.classList.remove('btn-outline-secondary');
                        btn.classList.add('btn-success');
                        feedback.innerHTML = '<span class="text-success"><i class="fas fa-check me-1"></i> Correct! Well done.</span>';
                        feedback.classList.remove('d-none');

                        // Record in progress store
                        if (window.MLFProgress) {
                            window.MLFProgress.recordProblemAttempt(qid, true, 0, false);
                        }

                        // Auto-check solved checkbox
                        const cb = document.getElementById('check-' + qid);
                        if (cb && !cb.checked) {
                            cb.checked = true;
                            const card = document.getElementById('card-' + qid);
                            if (card) card.classList.add('solved-card');
                            updateStats();
                        }
                    } else {
                        btn.classList.remove('btn-outline-secondary');
                        btn.classList.add('btn-danger');
                        feedback.innerHTML = '<span class="text-danger"><i class="fas fa-times me-1"></i> Incorrect. Review the hints or full derivation below!</span>';
                        feedback.classList.remove('d-none');

                        // Record attempt without marking solved
                        if (window.MLFProgress) {
                            window.MLFProgress.recordProblemAttempt(qid, false, 0, false);
                        }
                    }
                });
            });
        });

        // Cumulative Progressive Hints
        document.querySelectorAll('.hints-container').forEach(hc => {
            const btn = hc.querySelector('.show-hint-btn');
            const listEl = hc.querySelector('.hints-list');
            const card = hc.closest('.problem-card');
            const qid = card ? card.getAttribute('data-id') : null;
            const q = allQuestions.find(item => item.id === qid);
            if (!q || !q.hints || q.hints.length === 0) return;

            let unlockedCount = 0;
            btn.addEventListener('click', () => {
                if (unlockedCount < q.hints.length) {
                    const nextHintText = q.hints[unlockedCount];
                    unlockedCount++;

                    listEl.classList.remove('d-none');
                    const hintDiv = document.createElement('div');
                    hintDiv.className = 'alert alert-warning p-2 small mb-2';
                    hintDiv.innerHTML = `<strong>Hint ${unlockedCount}:</strong> ${nextHintText}`;
                    listEl.appendChild(hintDiv);

                    if (window.renderMLFMath) window.renderMLFMath(hintDiv);

                    // Record hint in progress store
                    if (window.MLFProgress) {
                        window.MLFProgress.recordProblemAttempt(qid, false, unlockedCount, false);
                    }

                    if (unlockedCount < q.hints.length) {
                        btn.innerHTML = `<i class="fas fa-lightbulb me-1"></i> Next Hint (${unlockedCount + 1}/${q.hints.length})`;
                    } else {
                        btn.classList.add('d-none');
                    }
                }
            });
        });
    }

    function bindStaticCardInteractions() {
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
        return String(str).replace(/[&<>'"]/g, 
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
