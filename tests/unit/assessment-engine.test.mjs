import test from 'node:test';
import assert from 'node:assert/strict';
import AssessmentEngine from '../../assets/js/assessment-engine.js';

test('MLFAssessmentEngine - Reference Validation', async (t) => {
    const catalog = {
        'q1': { id: 'q1', type: 'mcq' },
        'q2': { id: 'q2', type: 'mcq' },
        'q3': { id: 'q3', type: 'numeric' }
    };

    await t.test('passes when all question references exist without duplicates', () => {
        const assessment = {
            id: 'quiz-valid',
            questionIds: ['q1', 'q2', 'q3']
        };
        const res = AssessmentEngine.validateAssessmentReferences(assessment, catalog);
        assert.equal(res.valid, true);
        assert.equal(res.missingQuestionIds.length, 0);
        assert.equal(res.duplicateQuestionIds.length, 0);
    });

    await t.test('detects missing question IDs and blocks invalid assessment', () => {
        const assessment = {
            id: 'quiz-missing',
            questionIds: ['q1', 'missing-q99', 'q3', 'missing-q100']
        };
        const res = AssessmentEngine.validateAssessmentReferences(assessment, catalog);
        assert.equal(res.valid, false);
        assert.deepEqual(res.missingQuestionIds, ['missing-q99', 'missing-q100']);
    });

    await t.test('detects duplicate question IDs in definition', () => {
        const assessment = {
            id: 'quiz-duplicates',
            questionIds: ['q1', 'q2', 'q1']
        };
        const res = AssessmentEngine.validateAssessmentReferences(assessment, catalog);
        assert.equal(res.valid, false);
        assert.deepEqual(res.duplicateQuestionIds, ['q1']);
    });
});

test('MLFAssessmentEngine - Full Attempt Grading & Weak Concept Diagnostics', async (t) => {
    const catalog = {
        'q-mcq': {
            id: 'q-mcq',
            title: 'Matrix Trace',
            week: 1,
            type: 'mcq',
            conceptIds: ['trace-properties'],
            answerSpec: { correctOptionIds: ['b'] },
            relatedLesson: 'week-1/week-1.html'
        },
        'q-msq': {
            id: 'q-msq',
            title: 'Symmetric Matrix Properties',
            week: 5,
            type: 'msq',
            conceptIds: ['spectral-theorem'],
            answerSpec: { correctOptionIds: ['a', 'c'], mode: 'exact-set' },
            relatedLesson: 'week-5/week-5.html'
        },
        'q-num': {
            id: 'q-num',
            title: 'Orthogonal Projection Length',
            week: 3,
            type: 'numeric',
            conceptIds: ['subspace-projection'],
            answerSpec: { numericValue: 3.5, tolerance: { absolute: 0.1 } },
            relatedLesson: 'week-3/week-3.html',
            relatedLab: 'visual_labs.html#lab-projection'
        }
    };

    const assessment = {
        id: 'mock-mixed',
        questionIds: ['q-mcq', 'q-msq', 'q-num'],
        scoring: {
            mcq: { correct: 1, incorrect: 0 },
            msq: { correct: 2, incorrect: 0 },
            numeric: { correct: 2, incorrect: 0 }
        }
    };

    await t.test('grades mixed answers accurately and aggregates diagnostics', () => {
        const answers = {
            'q-mcq': 'b',        // Correct (+1)
            'q-msq': ['a'],      // Incorrect/Partial in exact-set (+0)
            'q-num': null        // Unanswered (+0)
        };

        const report = AssessmentEngine.gradeAttempt(assessment, catalog, answers);
        assert.equal(report.score, 1);
        assert.equal(report.maxScore, 5); // 1 + 2 + 2
        assert.equal(report.percentage, 20);
        assert.equal(report.counts.correct, 1);
        assert.equal(report.counts.incorrect, 1);
        assert.equal(report.counts.unanswered, 1);

        // Weak concepts should include missed q-msq and unanswered q-num
        const weakIds = report.weakConcepts.map(c => c.conceptId);
        assert.ok(weakIds.includes('spectral-theorem'));
        assert.ok(weakIds.includes('subspace-projection'));
        assert.ok(!weakIds.includes('trace-properties')); // correctly answered, not weak
    });
});

test('MLFAssessmentEngine - Production Data Integrity', async (t) => {
    const fs = await import('node:fs');
    const path = await import('node:path');
    const fileURLToPath = (await import('node:url')).fileURLToPath;
    const dirname = path.dirname(fileURLToPath(import.meta.url));

    const assessmentsPath = path.resolve(dirname, '../../data/assessments.json');
    const allQuestionsPath = path.resolve(dirname, '../../data/questions/all_questions.json');

    const assessments = JSON.parse(fs.readFileSync(assessmentsPath, 'utf8'));
    const questionsArr = JSON.parse(fs.readFileSync(allQuestionsPath, 'utf8'));
    const catalog = {};
    questionsArr.forEach(q => { catalog[q.id] = q; });

    await t.test('all production assessments validate with 100% reference integrity', () => {
        const assessmentKeys = Object.keys(assessments);
        assert.ok(assessmentKeys.length >= 7, 'Must have at least 7 assessments configured');
        assert.ok(assessmentKeys.includes('week3-mastery'));
        assert.ok(assessmentKeys.includes('week6-mastery'));
        assert.ok(assessmentKeys.includes('week7-mastery'));

        for (const key of assessmentKeys) {
            const a = assessments[key];
            const val = AssessmentEngine.validateAssessmentReferences(a, catalog);
            assert.equal(val.valid, true, `Assessment ${key} failed validation: missing ${val.missingQuestionIds}`);
            assert.equal(val.missingQuestionIds.length, 0, `Assessment ${key} has missing questions`);
            assert.equal(val.duplicateQuestionIds.length, 0, `Assessment ${key} has duplicate questions`);
        }
    });
});

