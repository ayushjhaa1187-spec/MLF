import test from 'node:test';
import assert from 'node:assert/strict';
import ProgressValidation from '../../assets/js/progress-validation.js';
import MLFProgress from '../../assets/js/progress-store.js';

test('MLFProgressValidation - Tolerant Recovery for Corrupt Data', async (t) => {
    await t.test('null or undefined raw data yields clean defaults', () => {
        const state = ProgressValidation.validateStoredState(null);
        assert.equal(state.version, 2);
        assert.deepEqual(state.lessonsRead, {});
        assert.deepEqual(state.problemsSolved, {});
        assert.equal(state.activeAttempt, null);
    });

    await t.test('malformed nested types are safely sanitized', () => {
        const corrupted = {
            lessonsRead: 'not_an_object',
            problemsSolved: { q1: 1, q2: true, q3: false },
            problemAttempts: {
                q1: { attempts: 'invalid', hintsUsed: -3, solved: 1 }
            },
            quizAttempts: {
                quiz1: [{ score: 'not_number', total: 10 }, { score: 8, total: 10 }]
            },
            needsRevision: {
                'concept-1': { week: 'invalid_week', missedCount: -2 }
            }
        };

        const cleaned = ProgressValidation.validateStoredState(corrupted);
        assert.deepEqual(cleaned.lessonsRead, {});
        assert.deepEqual(cleaned.problemsSolved, { q1: true, q2: true });
        assert.equal(cleaned.problemAttempts.q1.attempts, 0);
        assert.equal(cleaned.problemAttempts.q1.hintsUsed, 0);
        assert.equal(cleaned.problemAttempts.q1.solved, true);

        // quizAttempts filtered to valid items
        assert.equal(cleaned.quizAttempts.quiz1.length, 1);
        assert.equal(cleaned.quizAttempts.quiz1[0].score, 8);

        // needsRevision week bounded and missedCount >= 1
        assert.equal(cleaned.needsRevision['concept-1'].week, 1);
        assert.equal(cleaned.needsRevision['concept-1'].missedCount, 1);
    });
});

test('MLFProgressValidation - Strict Validation for Import Backups', async (t) => {
    await t.test('rejects empty, non-string, or non-object imports', () => {
        assert.throws(() => ProgressValidation.validateImportPayload(''), /empty/);
        assert.throws(() => ProgressValidation.validateImportPayload('[]'), /root must be a valid JSON object/);
        assert.throws(() => ProgressValidation.validateImportPayload('{ bad json'), /SyntaxError/);
    });

    await t.test('rejects objects lacking recognizable progress structures', () => {
        const arbitraryObj = JSON.stringify({ name: 'random', items: [1, 2, 3] });
        assert.throws(() => ProgressValidation.validateImportPayload(arbitraryObj), /recognizable MLF progress/);
    });

    await t.test('rejects unsupported future schema versions', () => {
        const futureVersion = JSON.stringify({
            version: 99,
            lessonsRead: { 'week-1': true }
        });
        assert.throws(() => ProgressValidation.validateImportPayload(futureVersion), /Unsupported schema version/);
    });

    await t.test('accepts valid backup and extracts accurate summary', () => {
        const validBackup = JSON.stringify({
            version: 2,
            lessonsRead: { 'week-1': true, 'week-2': true },
            problemsSolved: { 'q-1': true },
            quizAttempts: {
                quiz1: [{ attemptId: 'att-1', score: 9, total: 10, timestamp: '2026-10-10' }]
            }
        });
        const res = ProgressValidation.validateImportPayload(validBackup);
        assert.equal(res.valid, true);
        assert.equal(res.summary.lessonsReadCount, 2);
        assert.equal(res.summary.problemsSolvedCount, 1);
        assert.equal(res.summary.quizAttemptsCount, 1);
    });
});

test('MLFProgress - Storage Mode & In-Memory Read/Write Consistency', async (t) => {
    MLFProgress.setStorageModeForTest('memory');
    assert.equal(MLFProgress.getStorageMode(), 'memory');

    await t.test('read-after-write in memory mode is completely consistent', () => {
        MLFProgress.reset();
        MLFProgress.setLessonRead('week-3', true);
        assert.equal(MLFProgress.isLessonRead('week-3'), true);
        assert.equal(MLFProgress.isLessonRead('week-4'), false);

        const stats = MLFProgress.getStats();
        assert.equal(stats.lessonsReadCount, 1);
        assert.equal(stats.storageMode, 'memory');
    });
});

test('MLFProgress - Idempotent Assessment Submission Recording', async (t) => {
    MLFProgress.setStorageModeForTest('memory');
    MLFProgress.reset();

    const submission = {
        attemptId: 'att-fixed-101',
        assessmentId: 'quiz1',
        score: 8,
        maxScore: 10,
        percentage: 80,
        answers: { 'q1': 'b' }
    };

    await t.test('first recording adds submission and summary', () => {
        MLFProgress.recordAssessmentSubmission(submission);
        const state = MLFProgress.getState();
        assert.equal(state.quizAttempts.quiz1.length, 1);
        assert.equal(state.quizAttempts.quiz1[0].attemptId, 'att-fixed-101');
    });

    await t.test('duplicate recording with same attemptId does not duplicate history', () => {
        // Record identical attempt again
        MLFProgress.recordAssessmentSubmission(submission);
        const state = MLFProgress.getState();
        assert.equal(state.quizAttempts.quiz1.length, 1, 'History length must remain 1');
    });
});

test('MLFProgress - Import Merge Policy & Active Attempt Preservation', async (t) => {
    MLFProgress.setStorageModeForTest('memory');
    MLFProgress.reset();

    // 1. Current local state has an ongoing active attempt and 1 lesson read
    MLFProgress.setLessonRead('week-1', true);
    MLFProgress.saveActiveAttempt({
        attemptId: 'active-att-in-progress',
        assessmentId: 'quiz1',
        startedAt: Date.now(),
        deadlineAt: Date.now() + 600000,
        questionIds: ['q1', 'q2'],
        answers: { 'q1': 'a' },
        flags: ['q2'],
        status: 'in-progress'
    });

    // 2. Incoming import document with lesson-2 read and an attempt
    const incomingData = JSON.stringify({
        version: 2,
        lessonsRead: { 'week-2': true },
        problemsSolved: { 'p-10': true },
        quizAttempts: {
            quiz1: [{ attemptId: 'att-incoming-1', score: 10, total: 10, timestamp: '2026-10-12' }]
        },
        bookmarks: ['concept-svd']
    });

    await t.test('merge preserves current active attempt and deduplicates history', () => {
        const merged = MLFProgress.importStateJSON(incomingData, 'merge');

        // Both lessons read
        assert.equal(merged.lessonsRead['week-1'], true);
        assert.equal(merged.lessonsRead['week-2'], true);

        // Problem solved preserved
        assert.equal(merged.problemsSolved['p-10'], true);

        // Ongoing active attempt preserved!
        assert.notEqual(merged.activeAttempt, null);
        assert.equal(merged.activeAttempt.attemptId, 'active-att-in-progress');
        assert.deepEqual(merged.activeAttempt.answers, { 'q1': 'a' });

        // Importing same document a second time does not duplicate quiz attempts
        const mergedAgain = MLFProgress.importStateJSON(incomingData, 'merge');
        assert.equal(mergedAgain.quizAttempts.quiz1.length, 1);
    });
});
