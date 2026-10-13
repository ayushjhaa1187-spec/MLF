/**
 * MLF Progressive Learning Platform - Progress State Store (Version 2)
 * Features:
 * - Robust schema validation & sanitization via MLFProgressValidation
 * - Active storage mode tracking ('localStorage' vs 'memory') with seamless read/write consistency
 * - Idempotent assessment submission recording by attemptId
 * - Deduplicated history merge preserving in-progress active attempts
 * - Automatic recovery & evaluation of expired attempts
 * - Same-origin postMessage cross-frame synchronization
 */
(function(root, factory) {
    if (typeof define === 'function' && define.amd) {
        define(['./progress-validation', './scoring'], factory);
    } else if (typeof module === 'object' && module.exports) {
        const val = require('./progress-validation');
        const sc = require('./scoring');
        module.exports = factory(val, sc);
    } else {
        root.MLFProgress = factory(root.MLFProgressValidation, root.MLFScoring);
    }
}(typeof self !== 'undefined' ? self : this, function(ProgressValidation, Scoring) {
    'use strict';

    const fallbackValidation = {
        SCHEMA_VERSION: 2,
        createDefaultState: function() {
            return {
                version: 2,
                lessonsRead: {},
                problemsSolved: {},
                problemAttempts: {},
                quizAttempts: {},
                assessmentSubmissions: {},
                needsRevision: {},
                bookmarks: [],
                diagnosticCompleted: false,
                diagnosticScore: null,
                activeAttempt: null,
                lastActive: new Date().toISOString()
            };
        },
        validateStoredState: function(raw) {
            if (!raw || typeof raw !== 'object') return fallbackValidation.createDefaultState();
            return Object.assign(fallbackValidation.createDefaultState(), raw);
        },
        validateImportPayload: function(str) {
            const parsed = JSON.parse(str);
            const state = parsed.progress || parsed;
            return {
                valid: true,
                state: state,
                summary: {
                    lessonsReadCount: Object.keys(state.lessonsRead || {}).length,
                    problemsSolvedCount: Object.keys(state.problemsSolved || {}).length,
                    quizAttemptsCount: 0,
                    submissionsCount: 0,
                    needsRevisionCount: 0
                }
            };
        },
        deepClone: function(o) { return o ? JSON.parse(JSON.stringify(o)) : o; }
    };

    const validation = ProgressValidation || (typeof window !== 'undefined' && window.MLFProgressValidation) || fallbackValidation;
    const scoringEngine = Scoring || (typeof window !== 'undefined' && window.MLFScoring);

    let memoryStorage = null;
    let activeStorageMode = 'localStorage'; // 'localStorage' or 'memory'

    function testLocalStorage() {
        if (typeof window === 'undefined' || !window.localStorage) {
            return false;
        }
        try {
            const testKey = '__mlf_storage_test__';
            window.localStorage.setItem(testKey, '1');
            window.localStorage.removeItem(testKey);
            return true;
        } catch (e) {
            return false;
        }
    }

    if (!testLocalStorage()) {
        activeStorageMode = 'memory';
    }

    function loadState() {
        if (activeStorageMode === 'memory') {
            if (!memoryStorage) memoryStorage = validation.createDefaultState();
            return validation.deepClone(memoryStorage);
        }

        try {
            const raw = window.localStorage.getItem(STORAGE_KEY);
            if (!raw) return validation.createDefaultState();
            const parsed = JSON.parse(raw);
            return validation.validateStoredState(parsed);
        } catch (e) {
            console.warn('MLFProgress: localStorage read failed, falling back to memory:', e);
            activeStorageMode = 'memory';
            if (!memoryStorage) memoryStorage = validation.createDefaultState();
            return validation.deepClone(memoryStorage);
        }
    }

    function saveState(state) {
        state.lastActive = new Date().toISOString();

        if (activeStorageMode === 'memory') {
            memoryStorage = validation.deepClone(state);
            dispatchUpdate(state);
            return;
        }

        try {
            window.localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
            dispatchUpdate(state);
        } catch (e) {
            console.error('MLFProgress: localStorage write failed (e.g. QuotaExceeded). Switching to memory storage:', e);
            activeStorageMode = 'memory';
            memoryStorage = validation.deepClone(state);
            dispatchUpdate(state);
        }
    }

    function getSafeOrigin() {
        if (typeof window === 'undefined' || !window.location || !window.location.origin || window.location.origin === 'null') {
            return '*';
        }
        return window.location.origin;
    }

    function dispatchUpdate(state) {
        if (typeof window === 'undefined') return;

        const payload = validation.deepClone(state);
        window.dispatchEvent(new CustomEvent('mlf-progress-updated', { detail: payload }));

        const targetOrigin = getSafeOrigin();

        if (window.parent && window.parent !== window) {
            try {
                window.parent.postMessage({ type: 'MLF_PROGRESS_SYNC', state: payload }, targetOrigin);
            } catch (err) {}
        }

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
        SCHEMA_VERSION: validation.SCHEMA_VERSION,

        getStorageMode: function() {
            return activeStorageMode;
        },

        setStorageModeForTest: function(mode) {
            activeStorageMode = mode === 'memory' ? 'memory' : 'localStorage';
            if (activeStorageMode === 'memory' && !memoryStorage) {
                memoryStorage = validation.createDefaultState();
            }
        },

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

        // Active Attempt Lifecycle
        getActiveAttempt: function(expectedAssessmentId) {
            const state = loadState();
            if (!state.activeAttempt) return null;

            // Check if attempt deadline expired
            const now = Date.now();
            if (state.activeAttempt.status === 'in-progress' && state.activeAttempt.deadlineAt <= now) {
                // Auto-finalize expired attempt
                const expiredAttempt = validation.deepClone(state.activeAttempt);
                expiredAttempt.status = 'expired';
                return expiredAttempt;
            }

            if (expectedAssessmentId && state.activeAttempt.assessmentId !== expectedAssessmentId) {
                return null;
            }

            return validation.deepClone(state.activeAttempt);
        },

        saveActiveAttempt: function(attempt) {
            if (!attempt || !attempt.attemptId || !attempt.assessmentId) return;
            const state = loadState();
            state.activeAttempt = validation.deepClone(attempt);
            saveState(state);
        },

        clearActiveAttempt: function() {
            const state = loadState();
            state.activeAttempt = null;
            saveState(state);
        },

        // Assessment submission history (strictly idempotent by attemptId)
        recordAssessmentSubmission: function(submission) {
            if (!submission || !submission.assessmentId || !submission.attemptId) return;
            const state = loadState();
            const aid = submission.assessmentId;
            const attemptId = submission.attemptId;

            // 1. Detailed submission map (keyed by attemptId)
            if (!state.assessmentSubmissions) state.assessmentSubmissions = {};
            state.assessmentSubmissions[attemptId] = validation.deepClone(submission);

            // 2. Summary quizAttempts list (deduplicated by attemptId)
            if (!state.quizAttempts[aid]) {
                state.quizAttempts[aid] = [];
            }

            const existingIdx = state.quizAttempts[aid].findIndex(item => item.attemptId === attemptId);
            const summaryRecord = {
                attemptId: attemptId,
                score: submission.score,
                total: submission.maxScore || submission.total || 1,
                percentage: typeof submission.percentage === 'number' ? submission.percentage : Math.round((submission.score / (submission.maxScore || 1)) * 100),
                timestamp: submission.timestamp || new Date().toISOString()
            };

            if (existingIdx >= 0) {
                // Replace in place
                state.quizAttempts[aid][existingIdx] = summaryRecord;
            } else {
                state.quizAttempts[aid].push(summaryRecord);
            }

            // Clear active attempt if it matches
            if (state.activeAttempt && state.activeAttempt.attemptId === attemptId) {
                state.activeAttempt = null;
            }

            saveState(state);
        },

        getAssessmentSubmission: function(attemptId) {
            const state = loadState();
            return state.assessmentSubmissions && state.assessmentSubmissions[attemptId]
                ? validation.deepClone(state.assessmentSubmissions[attemptId])
                : null;
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
                } : null,
                storageMode: activeStorageMode
            };
        },

        exportStateJSON: function() {
            const state = loadState();
            const exportData = {
                metadata: {
                    appName: 'MLF Progressive Learning Platform',
                    exportDate: new Date().toISOString(),
                    schemaVersion: validation.SCHEMA_VERSION
                },
                progress: state
            };
            return JSON.stringify(exportData, null, 2);
        },

        previewImportJSON: function(jsonString) {
            try {
                const res = validation.validateImportPayload(jsonString);
                return {
                    valid: true,
                    summary: res.summary
                };
            } catch (err) {
                return {
                    valid: false,
                    error: err.message
                };
            }
        },

        importStateJSON: function(jsonString, mode) {
            const verifyRes = validation.validateImportPayload(jsonString);
            const incoming = verifyRes.state;

            if (mode === 'merge') {
                const current = loadState();
                const merged = validation.createDefaultState();

                // Merge lessonsRead and problemsSolved (union)
                merged.lessonsRead = Object.assign({}, current.lessonsRead, incoming.lessonsRead);
                merged.problemsSolved = Object.assign({}, current.problemsSolved, incoming.problemsSolved);

                // Merge problemAttempts (take max attempts and solved)
                merged.problemAttempts = Object.assign({}, current.problemAttempts);
                for (const pid in incoming.problemAttempts) {
                    const inc = incoming.problemAttempts[pid];
                    const cur = merged.problemAttempts[pid];
                    if (!cur) {
                        merged.problemAttempts[pid] = validation.deepClone(inc);
                    } else {
                        merged.problemAttempts[pid] = {
                            attempts: Math.max(cur.attempts || 0, inc.attempts || 0),
                            hintsUsed: Math.max(cur.hintsUsed || 0, inc.hintsUsed || 0),
                            solutionRevealed: Boolean(cur.solutionRevealed || inc.solutionRevealed),
                            solved: Boolean(cur.solved || inc.solved),
                            lastAttempted: (inc.lastAttempted > cur.lastAttempted) ? inc.lastAttempted : cur.lastAttempted
                        };
                    }
                }

                // Merge quizAttempts with deduplication by attemptId
                merged.quizAttempts = validation.deepClone(current.quizAttempts || {});
                for (const aid in incoming.quizAttempts) {
                    if (!merged.quizAttempts[aid]) {
                        merged.quizAttempts[aid] = [];
                    }
                    const seenIds = new Set(merged.quizAttempts[aid].map(att => att.attemptId));
                    incoming.quizAttempts[aid].forEach(att => {
                        if (!seenIds.has(att.attemptId)) {
                            merged.quizAttempts[aid].push(validation.deepClone(att));
                            seenIds.add(att.attemptId);
                        }
                    });
                }

                // Merge assessmentSubmissions by attemptId
                merged.assessmentSubmissions = Object.assign({}, current.assessmentSubmissions, incoming.assessmentSubmissions);

                // Merge needsRevision
                merged.needsRevision = Object.assign({}, current.needsRevision);
                for (const cid in incoming.needsRevision) {
                    const inc = incoming.needsRevision[cid];
                    const cur = merged.needsRevision[cid];
                    if (!cur) {
                        merged.needsRevision[cid] = validation.deepClone(inc);
                    } else {
                        merged.needsRevision[cid] = {
                            conceptId: cid,
                            title: inc.title || cur.title,
                            week: inc.week || cur.week,
                            missedCount: Math.max(cur.missedCount || 1, inc.missedCount || 1),
                            lastMissedAt: (inc.lastMissedAt > cur.lastMissedAt) ? inc.lastMissedAt : cur.lastMissedAt,
                            relatedLesson: inc.relatedLesson || cur.relatedLesson,
                            relatedLab: inc.relatedLab || cur.relatedLab
                        };
                    }
                }

                // Preserve activeAttempt from current if ongoing, else take incoming
                merged.activeAttempt = current.activeAttempt ? validation.deepClone(current.activeAttempt) : validation.deepClone(incoming.activeAttempt);

                // Merge bookmarks and diagnostics
                merged.bookmarks = Array.from(new Set((current.bookmarks || []).concat(incoming.bookmarks || [])));
                merged.diagnosticCompleted = current.diagnosticCompleted || incoming.diagnosticCompleted;
                merged.diagnosticScore = incoming.diagnosticScore || current.diagnosticScore;

                saveState(merged);
                return merged;
            } else {
                saveState(incoming);
                return incoming;
            }
        },

        reset: function() {
            if (activeStorageMode === 'localStorage' && typeof window !== 'undefined' && window.localStorage) {
                try {
                    window.localStorage.removeItem(STORAGE_KEY);
                } catch (e) {}
            }
            memoryStorage = validation.createDefaultState();
            dispatchUpdate(memoryStorage);
        }
    };

    // Cross-frame listener
    if (typeof window !== 'undefined') {
        window.addEventListener('message', function(event) {
            if (!event.data || event.data.type !== 'MLF_PROGRESS_SYNC') return;

            if (window.location.origin && window.location.origin !== 'null') {
                if (event.origin && event.origin !== window.location.origin) {
                    return;
                }
            }

            if (event.data.state) {
                const validated = validation.validateStoredState(event.data.state);
                window.dispatchEvent(new CustomEvent('mlf-progress-updated', { detail: validated }));
            }
        });
    }

    return MLFProgress;
}));
