/**
 * MLF Progress State Validation & Sanitization Module
 * Implements:
 * 1. Tolerant recovery for stored localStorage data.
 * 2. Strict verification for imported JSON backups.
 * 3. Deep validation of nested problemAttempts, quizAttempts, assessmentSubmissions, needsRevision, and activeAttempt.
 */
(function(root, factory) {
    if (typeof define === 'function' && define.amd) {
        define([], factory);
    } else if (typeof module === 'object' && module.exports) {
        module.exports = factory();
    } else {
        root.MLFProgressValidation = factory();
    }
}(typeof self !== 'undefined' ? self : this, function() {
    'use strict';

    const SCHEMA_VERSION = 2;
    const MAX_IMPORT_SIZE_BYTES = 5 * 1024 * 1024; // 5 MB ceiling

    function createDefaultState() {
        return {
            version: SCHEMA_VERSION,
            lastActive: new Date().toISOString(),
            lessonsRead: {},
            problemsSolved: {},
            problemAttempts: {},
            quizAttempts: {},
            activeAttempt: null,
            assessmentSubmissions: {},
            needsRevision: {},
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

    /**
     * Tolerant sanitization of browser storage (never throws, recovers what it can).
     */
    function validateStoredState(raw) {
        if (!raw || typeof raw !== 'object' || Array.isArray(raw)) {
            return createDefaultState();
        }

        const state = createDefaultState();

        if (typeof raw.lastActive === 'string') {
            state.lastActive = raw.lastActive;
        }

        // Lessons read
        if (raw.lessonsRead && typeof raw.lessonsRead === 'object' && !Array.isArray(raw.lessonsRead)) {
            for (const k in raw.lessonsRead) {
                if (Boolean(raw.lessonsRead[k])) state.lessonsRead[k] = true;
            }
        }

        // Problems solved
        if (raw.problemsSolved && typeof raw.problemsSolved === 'object' && !Array.isArray(raw.problemsSolved)) {
            for (const k in raw.problemsSolved) {
                if (Boolean(raw.problemsSolved[k])) state.problemsSolved[k] = true;
            }
        }

        // Problem attempts
        if (raw.problemAttempts && typeof raw.problemAttempts === 'object' && !Array.isArray(raw.problemAttempts)) {
            for (const pid in raw.problemAttempts) {
                const item = raw.problemAttempts[pid];
                if (item && typeof item === 'object') {
                    state.problemAttempts[pid] = {
                        attempts: Math.max(0, parseInt(item.attempts, 10) || 0),
                        hintsUsed: Math.max(0, parseInt(item.hintsUsed, 10) || 0),
                        solutionRevealed: Boolean(item.solutionRevealed),
                        solved: Boolean(item.solved),
                        lastAttempted: typeof item.lastAttempted === 'string' ? item.lastAttempted : new Date().toISOString()
                    };
                }
            }
        }

        // Quiz attempts (summary history)
        if (raw.quizAttempts && typeof raw.quizAttempts === 'object' && !Array.isArray(raw.quizAttempts)) {
            for (const qid in raw.quizAttempts) {
                if (Array.isArray(raw.quizAttempts[qid])) {
                    state.quizAttempts[qid] = raw.quizAttempts[qid].filter(att => (
                        att && typeof att === 'object' &&
                        typeof att.score === 'number' && !isNaN(att.score) &&
                        typeof att.total === 'number' && att.total > 0
                    )).map(att => ({
                        attemptId: att.attemptId || 'att-legacy-' + Math.random().toString(36).substr(2, 6),
                        score: att.score,
                        total: att.total,
                        percentage: typeof att.percentage === 'number' ? att.percentage : Math.round((att.score / att.total) * 100),
                        timestamp: typeof att.timestamp === 'string' ? att.timestamp : new Date().toISOString()
                    }));
                }
            }
        }

        // Detailed assessment submissions
        if (raw.assessmentSubmissions && typeof raw.assessmentSubmissions === 'object' && !Array.isArray(raw.assessmentSubmissions)) {
            for (const attId in raw.assessmentSubmissions) {
                const sub = raw.assessmentSubmissions[attId];
                if (sub && typeof sub === 'object' && typeof sub.score === 'number') {
                    state.assessmentSubmissions[attId] = {
                        attemptId: attId,
                        assessmentId: sub.assessmentId || 'assessment',
                        score: sub.score,
                        maxScore: sub.maxScore || sub.total || 1,
                        percentage: typeof sub.percentage === 'number' ? sub.percentage : 0,
                        timestamp: typeof sub.timestamp === 'string' ? sub.timestamp : new Date().toISOString(),
                        answers: sub.answers && typeof sub.answers === 'object' ? deepClone(sub.answers) : {},
                        itemScores: sub.itemScores && typeof sub.itemScores === 'object' ? deepClone(sub.itemScores) : {},
                        status: sub.status || 'submitted'
                    };
                }
            }
        }

        // Needs revision
        if (raw.needsRevision && typeof raw.needsRevision === 'object' && !Array.isArray(raw.needsRevision)) {
            for (const cid in raw.needsRevision) {
                const item = raw.needsRevision[cid];
                if (item && typeof item === 'object') {
                    state.needsRevision[cid] = {
                        conceptId: cid,
                        title: typeof item.title === 'string' ? item.title : cid,
                        week: Math.min(12, Math.max(1, parseInt(item.week, 10) || 1)),
                        missedCount: Math.max(1, parseInt(item.missedCount, 10) || 1),
                        lastMissedAt: typeof item.lastMissedAt === 'string' ? item.lastMissedAt : new Date().toISOString(),
                        relatedLesson: typeof item.relatedLesson === 'string' ? item.relatedLesson : null,
                        relatedLab: typeof item.relatedLab === 'string' ? item.relatedLab : null
                    };
                }
            }
        }

        // Bookmarks
        if (Array.isArray(raw.bookmarks)) {
            state.bookmarks = Array.from(new Set(raw.bookmarks.filter(b => typeof b === 'string')));
        }

        // Diagnostic
        if (typeof raw.diagnosticCompleted === 'boolean') {
            state.diagnosticCompleted = raw.diagnosticCompleted;
        }
        if (raw.diagnosticScore && typeof raw.diagnosticScore === 'object' && typeof raw.diagnosticScore.score === 'number') {
            state.diagnosticScore = {
                score: raw.diagnosticScore.score,
                total: raw.diagnosticScore.total || 8,
                percentage: typeof raw.diagnosticScore.percentage === 'number' ? raw.diagnosticScore.percentage : 0,
                timestamp: typeof raw.diagnosticScore.timestamp === 'string' ? raw.diagnosticScore.timestamp : new Date().toISOString()
            };
        }

        // Active Attempt
        if (raw.activeAttempt && typeof raw.activeAttempt === 'object') {
            const att = raw.activeAttempt;
            if (att.attemptId && att.assessmentId && Array.isArray(att.questionIds) && typeof att.deadlineAt === 'number') {
                state.activeAttempt = {
                    attemptId: String(att.attemptId),
                    assessmentId: String(att.assessmentId),
                    version: parseInt(att.version, 10) || 1,
                    startedAt: typeof att.startedAt === 'number' ? att.startedAt : Date.now(),
                    deadlineAt: att.deadlineAt,
                    questionIds: att.questionIds.map(String),
                    answers: att.answers && typeof att.answers === 'object' ? deepClone(att.answers) : {},
                    flags: Array.isArray(att.flags) ? att.flags.map(String) : [],
                    status: att.status || 'in-progress'
                };
            }
        }

        return state;
    }

    /**
     * Strict verification of an external JSON backup file.
     * Throws an error with descriptive message if payload is invalid.
     */
    function validateImportPayload(jsonString) {
        if (typeof jsonString !== 'string' || jsonString.trim() === '') {
            throw new Error('Import payload cannot be empty.');
        }

        if (jsonString.length > MAX_IMPORT_SIZE_BYTES) {
            throw new Error(`Import payload exceeds maximum size limit of ${MAX_IMPORT_SIZE_BYTES / (1024 * 1024)} MB.`);
        }

        let parsed;
        try {
            parsed = JSON.parse(jsonString);
        } catch (e) {
            throw new Error('Invalid JSON format: SyntaxError ' + e.message);
        }

        if (!parsed || typeof parsed !== 'object' || Array.isArray(parsed)) {
            throw new Error('Import payload root must be a valid JSON object.');
        }

        // Unwrap metadata/progress envelope if present
        const progressData = parsed.progress ? parsed.progress : parsed;

        if (!progressData || typeof progressData !== 'object' || Array.isArray(progressData)) {
            throw new Error('Missing progress data object in import document.');
        }

        // Verify version support
        const ver = progressData.version !== undefined ? progressData.version : (parsed.metadata && parsed.metadata.schemaVersion);
        if (ver !== undefined && (typeof ver !== 'number' || ver < 1 || ver > SCHEMA_VERSION)) {
            throw new Error(`Unsupported schema version: ${ver}. Supported versions are 1 to ${SCHEMA_VERSION}.`);
        }

        // Must contain at least one recognizable progress property to be considered a genuine backup
        const knownKeys = ['lessonsRead', 'problemsSolved', 'problemAttempts', 'quizAttempts', 'assessmentSubmissions', 'needsRevision', 'diagnosticScore', 'bookmarks'];
        const hasAnyKnown = knownKeys.some(k => progressData[k] !== undefined);
        if (!hasAnyKnown) {
            throw new Error('JSON object does not contain recognizable MLF progress data structures.');
        }

        // Run through sanitization to build clean object
        const validated = validateStoredState(progressData);

        return {
            valid: true,
            state: validated,
            summary: {
                lessonsReadCount: Object.keys(validated.lessonsRead).length,
                problemsSolvedCount: Object.keys(validated.problemsSolved).length,
                quizAttemptsCount: Object.values(validated.quizAttempts).reduce((acc, arr) => acc + (Array.isArray(arr) ? arr.length : 0), 0),
                submissionsCount: Object.keys(validated.assessmentSubmissions).length,
                needsRevisionCount: Object.keys(validated.needsRevision).length,
                hasDiagnostic: validated.diagnosticCompleted,
                hasActiveAttempt: Boolean(validated.activeAttempt),
                lastActive: validated.lastActive
            }
        };
    }

    return {
        SCHEMA_VERSION: SCHEMA_VERSION,
        createDefaultState: createDefaultState,
        validateStoredState: validateStoredState,
        validateImportPayload: validateImportPayload,
        deepClone: deepClone
    };
}));
