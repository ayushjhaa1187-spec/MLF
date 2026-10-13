/**
 * MLF Progressive Learning Platform - Progress State Store
 * Schema Version: MLF_PROGRESS_V1
 * Backed by localStorage with cross-frame synchronization
 */
(function(window) {
    'use strict';

    const STORAGE_KEY = 'MLF_PROGRESS_V1';

    const defaultState = {
        version: 1,
        lastActive: new Date().toISOString(),
        lessonsRead: {},       // { 'week-1': true, ... }
        problemsSolved: {},    // { 'iitm-w3-q01': true, ... }
        quizAttempts: {},      // { 'quiz-1': [{ score: 14, total: 15, timestamp: '...' }] }
        diagnosticCompleted: false,
        diagnosticScore: null,
        bookmarks: []          // list of concept or problem IDs
    };

    function loadState() {
        try {
            const raw = localStorage.getItem(STORAGE_KEY);
            if (!raw) return { ...defaultState };
            const parsed = JSON.parse(raw);
            return { ...defaultState, ...parsed };
        } catch (e) {
            console.error('Failed to load MLF progress state:', e);
            return { ...defaultState };
        }
    }

    function saveState(state) {
        try {
            state.lastActive = new Date().toISOString();
            localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
            dispatchUpdate(state);
        } catch (e) {
            console.error('Failed to save MLF progress state:', e);
        }
    }

    function dispatchUpdate(state) {
        // Dispatch local event
        window.dispatchEvent(new CustomEvent('mlf-progress-updated', { detail: state }));
        
        // Notify parent if inside iframe
        if (window.parent && window.parent !== window) {
            window.parent.postMessage({ type: 'MLF_PROGRESS_SYNC', state: state }, '*');
        }
        
        // Notify child frames if in top window
        const iframes = document.querySelectorAll('iframe');
        iframes.forEach(frame => {
            try {
                if (frame.contentWindow) {
                    frame.contentWindow.postMessage({ type: 'MLF_PROGRESS_SYNC', state: state }, '*');
                }
            } catch (err) {}
        });
    }

    const MLFProgress = {
        getState: function() {
            return loadState();
        },

        isLessonRead: function(weekId) {
            const state = loadState();
            return !!state.lessonsRead[weekId];
        },

        setLessonRead: function(weekId, isRead) {
            const state = loadState();
            if (isRead) {
                state.lessonsRead[weekId] = true;
            } else {
                delete state.lessonsRead[weekId];
            }
            saveState(state);
            return state.lessonsRead[weekId];
        },

        toggleLessonRead: function(weekId) {
            return this.setLessonRead(weekId, !this.isLessonRead(weekId));
        },

        isProblemSolved: function(problemId) {
            const state = loadState();
            return !!state.problemsSolved[problemId];
        },

        setProblemSolved: function(problemId, isSolved) {
            const state = loadState();
            if (isSolved) {
                state.problemsSolved[problemId] = true;
            } else {
                delete state.problemsSolved[problemId];
            }
            saveState(state);
            return state.problemsSolved[problemId];
        },

        toggleProblemSolved: function(problemId) {
            return this.setProblemSolved(problemId, !this.isProblemSolved(problemId));
        },

        recordQuizAttempt: function(quizId, score, total) {
            const state = loadState();
            if (!state.quizAttempts[quizId]) {
                state.quizAttempts[quizId] = [];
            }
            state.quizAttempts[quizId].push({
                score: score,
                total: total,
                percentage: Math.round((score / total) * 100),
                timestamp: new Date().toISOString()
            });
            saveState(state);
        },

        saveDiagnosticResult: function(score, total) {
            const state = loadState();
            state.diagnosticCompleted = true;
            state.diagnosticScore = {
                score: score,
                total: total,
                percentage: Math.round((score / total) * 100),
                timestamp: new Date().toISOString()
            };
            saveState(state);
        },

        getStats: function() {
            const state = loadState();
            const readCount = Object.keys(state.lessonsRead).length;
            const solvedCount = Object.keys(state.problemsSolved).length;
            return {
                lessonsReadCount: readCount,
                lessonsTotal: 12,
                lessonsPercentage: Math.round((readCount / 12) * 100),
                problemsSolvedCount: solvedCount,
                diagnosticCompleted: state.diagnosticCompleted,
                diagnosticScore: state.diagnosticScore
            };
        },

        reset: function() {
            localStorage.removeItem(STORAGE_KEY);
            dispatchUpdate(defaultState);
        }
    };

    // Cross-frame message listener
    window.addEventListener('message', function(event) {
        if (event.data && event.data.type === 'MLF_PROGRESS_SYNC') {
            window.dispatchEvent(new CustomEvent('mlf-progress-updated', { detail: event.data.state }));
        }
    });

    window.MLFProgress = MLFProgress;
})(window);
