/**
 * MLF Progressive Learning Platform - Progress State Store
 * Schema Version: MLF_PROGRESS_V2 (backward-compatible with V1)
 * Features:
 * - Robust schema validation & deep cloning
 * - Resumable active exam attempts with deadline persistence
 * - Granular problem attempts, hint usage, & solution reveals
 * - Targeted revision queue keyed by concept
 * - Safe fallback in-memory storage if localStorage is blocked
 * - Same-origin postMessage cross-frame synchronization
 * - Full JSON export, import preview, and merge/overwrite
 */
(function(window) {
    'use strict';

    const STORAGE_KEY = 'MLF_PROGRESS_V1'; // keep key for seamless continuity
    const SCHEMA_VERSION = 2;

    let memoryStorage = null;

    function hasLocalStorage() {
        try {
            const testKey = '__mlf_storage_test__';
            window.localStorage.setItem(testKey, '1');
            window.localStorage.removeItem(testKey);
            return true;
        } catch (e) {
            return false;
        }
    }

    const storageAvailable = hasLocalStorage();

    function createDefaultState() {
        return {
            version: SCHEMA_VERSION,
            lastActive: new Date().toISOString(),
            lessonsRead: {},            // { 'week-1': true, ... }
            problemsSolved: {},         // { [problemId]: true }
            problemAttempts: {},       // { [problemId]: { attempts: 1, hintsUsed: 0, solutionRevealed: false, solved: true } }
            quizAttempts: {},           // { [assessmentId]: [{ score, total, percentage, timestamp, attemptId }] }
            activeAttempt: null,        // { attemptId, assessmentId, version, questionIds: [], startedAt, deadlineAt, answers: {}, flags: [], status }
            assessmentSubmissions: {},  // { [attemptId]: { attemptId, assessmentId, score, maxScore, percentage, answers, itemScores, timestamp } }
            needsRevision: {},          // { [conceptId]: { conceptId, title, week, missedCount, lastMissedAt, relatedLesson, relatedLab } }
            diagnosticCompleted: false,
            diagnosticScore: null,
            bookmarks: []
        };
    }

    function deepClone(obj) {
        if (obj === null || typeof obj !== 'object') return obj;
        try {
            return JSON.parse(JSON.stringify(obj));
        } catch (e) {
            return Object.assign({}, obj);
        }
    }

    function validateState(raw) {
        if (!raw || typeof raw !== 'object' || Array.isArray(raw)) {
            return createDefaultState();
        }

        const state = createDefaultState();

        if (typeof raw.lastActive === 'string') state.lastActive = raw.lastActive;
        if (raw.lessonsRead && typeof raw.lessonsRead === 'object' && !Array.isArray(raw.lessonsRead)) {
            for (const k in raw.lessonsRead) {
                if (Boolean(raw.lessonsRead[k])) state.lessonsRead[k] = true;
            }
        }
        if (raw.problemsSolved && typeof raw.problemsSolved === 'object' && !Array.isArray(raw.problemsSolved)) {
            for (const k in raw.problemsSolved) {
                if (Boolean(raw.problemsSolved[k])) state.problemsSolved[k] = true;
            }
        }
        if (raw.problemAttempts && typeof raw.problemAttempts === 'object' && !Array.isArray(raw.problemAttempts)) {
            state.problemAttempts = deepClone(raw.problemAttempts);
        }
        if (raw.quizAttempts && typeof raw.quizAttempts === 'object' && !Array.isArray(raw.quizAttempts)) {
            state.quizAttempts = deepClone(raw.quizAttempts);
        }
        if (raw.assessmentSubmissions && typeof raw.assessmentSubmissions === 'object' && !Array.isArray(raw.assessmentSubmissions)) {
            state.assessmentSubmissions = deepClone(raw.assessmentSubmissions);
        }
        if (raw.needsRevision && typeof raw.needsRevision === 'object' && !Array.isArray(raw.needsRevision)) {
            state.needsRevision = deepClone(raw.needsRevision);
        }
        if (Array.isArray(raw.bookmarks)) {
            state.bookmarks = raw.bookmarks.filter(b => typeof b === 'string');
        }
        if (typeof raw.diagnosticCompleted === 'boolean') {
            state.diagnosticCompleted = raw.diagnosticCompleted;
        }
        if (raw.diagnosticScore && typeof raw.diagnosticScore === 'object') {
            state.diagnosticScore = deepClone(raw.diagnosticScore);
        }
        if (raw.activeAttempt && typeof raw.activeAttempt === 'object') {
            const att = raw.activeAttempt;
            if (att.attemptId && att.assessmentId && Array.isArray(att.questionIds) && typeof att.deadlineAt === 'number') {
                state.activeAttempt = deepClone(att);
            }
        }

        return state;
    }

    function loadState() {
        if (!storageAvailable) {
            if (!memoryStorage) memoryStorage = createDefaultState();
            return deepClone(memoryStorage);
        }
        try {
            const raw = window.localStorage.getItem(STORAGE_KEY);
            if (!raw) return createDefaultState();
            const parsed = JSON.parse(raw);
            return validateState(parsed);
        } catch (e) {
            console.warn('MLFProgress: failed to load state from localStorage, falling back to default:', e);
            return createDefaultState();
        }
    }

    function saveState(state) {
        state.lastActive = new Date().toISOString();
        if (!storageAvailable) {
            memoryStorage = deepClone(state);
            dispatchUpdate(state);
            return;
        }
        try {
            window.localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
            dispatchUpdate(state);
        } catch (e) {
            console.error('MLFProgress: failed to save state to localStorage:', e);
            // fallback to memory
            memoryStorage = deepClone(state);
            dispatchUpdate(state);
        }
    }

    function getSafeOrigin() {
        if (!window.location.origin || window.location.origin === 'null') {
            return '*';
        }
        return window.location.origin;
    }

    function dispatchUpdate(state) {
        const payload = deepClone(state);
        window.dispatchEvent(new CustomEvent('mlf-progress-updated', { detail: payload }));

        const targetOrigin = getSafeOrigin();

        // Notify parent iframe
        if (window.parent && window.parent !== window) {
            try {
                window.parent.postMessage({ type: 'MLF_PROGRESS_SYNC', state: payload }, targetOrigin);
            } catch (err) {}
        }

        // Notify child iframes
        const iframes = document.querySelectorAll('iframe');
        iframes.forEach(frame => {
            try {
                if (frame.contentWindow) {
                    frame.contentWindow.postMessage({ type: 'MLF_PROGRESS_SYNC', state: payload }, targetOrigin);
                }
            } catch (err) {}
        });
    }

    const MLFProgress = {
        SCHEMA_VERSION: SCHEMA_VERSION,

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
            return !!state.lessonsRead[weekId];
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
                if (!state.problemAttempts[problemId]) {
                    state.problemAttempts[problemId] = {
                        attempts: 1,
                        hintsUsed: 0,
                        solutionRevealed: false,
                        solved: true,
                        lastAttempted: new Date().toISOString()
                    };
                } else {
                    state.problemAttempts[problemId].solved = true;
                }
            } else {
                delete state.problemsSolved[problemId];
                if (state.problemAttempts[problemId]) {
                    state.problemAttempts[problemId].solved = false;
                }
            }
            saveState(state);
            return !!state.problemsSolved[problemId];
        },

        toggleProblemSolved: function(problemId) {
            return this.setProblemSolved(problemId, !this.isProblemSolved(problemId));
        },

        recordProblemAttempt: function(problemId, isCorrect, hintsCount, solutionRevealed) {
            const state = loadState();
            const prev = state.problemAttempts[problemId] || {
                attempts: 0,
                hintsUsed: 0,
                solutionRevealed: false,
                solved: false
            };

            const updated = {
                attempts: (prev.attempts || 0) + 1,
                hintsUsed: Math.max(prev.hintsUsed || 0, Number(hintsCount) || 0),
                solutionRevealed: Boolean(prev.solutionRevealed || solutionRevealed),
                solved: Boolean(prev.solved || isCorrect),
                lastAttempted: new Date().toISOString()
            };

            state.problemAttempts[problemId] = updated;
            if (updated.solved) {
                state.problemsSolved[problemId] = true;
            }
            saveState(state);
            return updated;
        },

        // Active exam attempt lifecycle
        getActiveAttempt: function(expectedAssessmentId) {
            const state = loadState();
            if (!state.activeAttempt) return null;
            if (expectedAssessmentId && state.activeAttempt.assessmentId !== expectedAssessmentId) {
                return null;
            }
            return deepClone(state.activeAttempt);
        },

        saveActiveAttempt: function(attempt) {
            if (!attempt || !attempt.attemptId || !attempt.assessmentId) return;
            const state = loadState();
            state.activeAttempt = deepClone(attempt);
            saveState(state);
        },

        clearActiveAttempt: function() {
            const state = loadState();
            state.activeAttempt = null;
            saveState(state);
        },

        // Assessment submission history
        recordAssessmentSubmission: function(submission) {
            if (!submission || !submission.assessmentId) return;
            const state = loadState();
            const aid = submission.assessmentId;

            // Legacy array record
            if (!state.quizAttempts[aid]) {
                state.quizAttempts[aid] = [];
            }
            state.quizAttempts[aid].push({
                attemptId: submission.attemptId || 'att-' + Date.now(),
                score: submission.score,
                total: submission.maxScore || submission.total,
                percentage: submission.percentage,
                timestamp: submission.timestamp || new Date().toISOString()
            });

            // Detailed submission object
            if (submission.attemptId) {
                if (!state.assessmentSubmissions) state.assessmentSubmissions = {};
                state.assessmentSubmissions[submission.attemptId] = deepClone(submission);
            }

            // Clear active attempt if it matches
            if (state.activeAttempt && state.activeAttempt.attemptId === submission.attemptId) {
                state.activeAttempt = null;
            }

            saveState(state);
        },

        getAssessmentSubmission: function(attemptId) {
            const state = loadState();
            return state.assessmentSubmissions && state.assessmentSubmissions[attemptId]
                ? deepClone(state.assessmentSubmissions[attemptId])
                : null;
        },

        recordQuizAttempt: function(quizId, score, total) {
            const perc = total > 0 ? Math.round((score / total) * 100) : 0;
            this.recordAssessmentSubmission({
                attemptId: 'att-legacy-' + Date.now(),
                assessmentId: quizId,
                score: score,
                maxScore: total,
                percentage: perc,
                timestamp: new Date().toISOString()
            });
        },

        saveDiagnosticResult: function(score, total) {
            const state = loadState();
            state.diagnosticCompleted = true;
            state.diagnosticScore = {
                score: score,
                total: total,
                percentage: total > 0 ? Math.round((score / total) * 100) : 0,
                timestamp: new Date().toISOString()
            };
            saveState(state);
        },

        // Revision queue
        markNeedsRevision: function(conceptId, metadata) {
            if (!conceptId) return;
            const state = loadState();
            if (!state.needsRevision) state.needsRevision = {};

            const prev = state.needsRevision[conceptId] || {
                conceptId: conceptId,
                missedCount: 0
            };

            state.needsRevision[conceptId] = {
                conceptId: conceptId,
                title: (metadata && metadata.title) || prev.title || conceptId,
                week: (metadata && metadata.week) || prev.week || 1,
                missedCount: (prev.missedCount || 0) + 1,
                lastMissedAt: new Date().toISOString(),
                relatedLesson: (metadata && metadata.relatedLesson) || prev.relatedLesson || null,
                relatedLab: (metadata && metadata.relatedLab) || prev.relatedLab || null
            };
            saveState(state);
        },

        clearNeedsRevision: function(conceptId) {
            const state = loadState();
            if (state.needsRevision && state.needsRevision[conceptId]) {
                delete state.needsRevision[conceptId];
                saveState(state);
            }
        },

        getRevisionList: function() {
            const state = loadState();
            if (!state.needsRevision) return [];
            return Object.values(state.needsRevision).sort((a, b) => (b.missedCount || 0) - (a.missedCount || 0));
        },

        // Summary statistics
        getStats: function() {
            const state = loadState();
            const readCount = Object.keys(state.lessonsRead || {}).length;
            const solvedCount = Object.keys(state.problemsSolved || {}).length;
            const revisionCount = Object.keys(state.needsRevision || {}).length;

            return {
                lessonsReadCount: readCount,
                lessonsTotal: 12,
                lessonsPercentage: Math.round((readCount / 12) * 100),
                problemsSolvedCount: solvedCount,
                needsRevisionCount: revisionCount,
                diagnosticCompleted: Boolean(state.diagnosticCompleted),
                diagnosticScore: state.diagnosticScore,
                activeAttempt: state.activeAttempt ? {
                    assessmentId: state.activeAttempt.assessmentId,
                    deadlineAt: state.activeAttempt.deadlineAt
                } : null
            };
        },

        // Export & Import
        exportStateJSON: function() {
            const state = loadState();
            const exportData = {
                metadata: {
                    appName: 'MLF Progressive Learning Platform',
                    exportDate: new Date().toISOString(),
                    schemaVersion: SCHEMA_VERSION
                },
                progress: state
            };
            return JSON.stringify(exportData, null, 2);
        },

        previewImportJSON: function(jsonString) {
            try {
                const parsed = JSON.parse(jsonString);
                const data = parsed.progress ? parsed.progress : parsed;
                const validated = validateState(data);
                return {
                    valid: true,
                    lessonsReadCount: Object.keys(validated.lessonsRead).length,
                    problemsSolvedCount: Object.keys(validated.problemsSolved).length,
                    quizAttemptsCount: Object.values(validated.quizAttempts).reduce((acc, arr) => acc + (Array.isArray(arr) ? arr.length : 0), 0),
                    needsRevisionCount: Object.keys(validated.needsRevision).length,
                    hasDiagnostic: validated.diagnosticCompleted,
                    lastActive: validated.lastActive
                };
            } catch (err) {
                return {
                    valid: false,
                    error: err.message
                };
            }
        },

        importStateJSON: function(jsonString, mode) {
            // mode: 'overwrite' (default) or 'merge'
            const preview = this.previewImportJSON(jsonString);
            if (!preview.valid) {
                throw new Error('Invalid JSON format: ' + preview.error);
            }

            const parsed = JSON.parse(jsonString);
            const incoming = validateState(parsed.progress ? parsed.progress : parsed);

            if (mode === 'merge') {
                const current = loadState();
                const merged = createDefaultState();

                merged.lessonsRead = Object.assign({}, current.lessonsRead, incoming.lessonsRead);
                merged.problemsSolved = Object.assign({}, current.problemsSolved, incoming.problemsSolved);
                merged.problemAttempts = Object.assign({}, current.problemAttempts, incoming.problemAttempts);
                merged.needsRevision = Object.assign({}, current.needsRevision, incoming.needsRevision);

                // Merge quizAttempts
                for (const qid in current.quizAttempts) {
                    merged.quizAttempts[qid] = deepClone(current.quizAttempts[qid]);
                }
                for (const qid in incoming.quizAttempts) {
                    if (!merged.quizAttempts[qid]) merged.quizAttempts[qid] = [];
                    merged.quizAttempts[qid] = merged.quizAttempts[qid].concat(deepClone(incoming.quizAttempts[qid]));
                }

                // Submissions
                merged.assessmentSubmissions = Object.assign({}, current.assessmentSubmissions, incoming.assessmentSubmissions);

                // Diagnostic
                merged.diagnosticCompleted = current.diagnosticCompleted || incoming.diagnosticCompleted;
                merged.diagnosticScore = incoming.diagnosticScore || current.diagnosticScore;
                merged.bookmarks = Array.from(new Set((current.bookmarks || []).concat(incoming.bookmarks || [])));

                saveState(merged);
                return merged;
            } else {
                saveState(incoming);
                return incoming;
            }
        },

        reset: function() {
            if (storageAvailable) {
                window.localStorage.removeItem(STORAGE_KEY);
            }
            memoryStorage = createDefaultState();
            dispatchUpdate(memoryStorage);
        }
    };

    // Cross-frame message listener with safe origin filtering
    window.addEventListener('message', function(event) {
        if (!event.data || event.data.type !== 'MLF_PROGRESS_SYNC') return;

        // If not in local file: protocol, verify origin match
        if (window.location.origin && window.location.origin !== 'null') {
            if (event.origin && event.origin !== window.location.origin) {
                console.warn('MLFProgress: rejected cross-origin message from:', event.origin);
                return;
            }
        }

        if (event.data.state) {
            const validated = validateState(event.data.state);
            window.dispatchEvent(new CustomEvent('mlf-progress-updated', { detail: validated }));
        }
    });

    window.MLFProgress = MLFProgress;

})(typeof window !== 'undefined' ? window : this);
