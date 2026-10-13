import test from 'node:test';
import assert from 'node:assert/strict';
import Scoring from '../../assets/js/scoring.js';

test('MLFScoring - MCQ Evaluation', async (t) => {
    const question = {
        id: 'q-mcq-1',
        type: 'mcq',
        options: [
            { id: 'a', text: 'Option A' },
            { id: 'b', text: 'Option B' },
            { id: 'c', text: 'Option C' }
        ],
        answerSpec: { correctOptionIds: ['b'] }
    };

    await t.test('correct selection returns full score', () => {
        const res = Scoring.scoreItem(question, 'b');
        assert.equal(res.status, 'correct');
        assert.equal(res.score, 1);
        assert.equal(res.maxScore, 1);
        assert.equal(res.earnedPercentage, 100);
    });

    await t.test('case-insensitivity and whitespace trimming', () => {
        const res = Scoring.scoreItem(question, '  B  ');
        assert.equal(res.status, 'correct');
        assert.equal(res.score, 1);
    });

    await t.test('incorrect selection returns penalty/0', () => {
        const res = Scoring.scoreItem(question, 'a');
        assert.equal(res.status, 'incorrect');
        assert.equal(res.score, 0);
        assert.equal(res.earnedPercentage, 0);
    });

    await t.test('unanswered returns 0 and unanswered status', () => {
        const resNull = Scoring.scoreItem(question, null);
        assert.equal(resNull.status, 'unanswered');
        assert.equal(resNull.score, 0);

        const resEmpty = Scoring.scoreItem(question, '');
        assert.equal(resEmpty.status, 'unanswered');
        assert.equal(resEmpty.score, 0);
    });

    await t.test('assessment-configured custom marks and penalties', () => {
        const scoringRules = {
            mcq: { correct: 3, incorrect: -1 }
        };
        const correctRes = Scoring.scoreItem(question, 'b', scoringRules);
        assert.equal(correctRes.score, 3);
        assert.equal(correctRes.maxScore, 3);

        const wrongRes = Scoring.scoreItem(question, 'c', scoringRules);
        assert.equal(wrongRes.score, -1);
        assert.equal(wrongRes.maxScore, 3);
    });
});

test('MLFScoring - MSQ Evaluation', async (t) => {
    const question = {
        id: 'q-msq-1',
        type: 'msq',
        answerSpec: {
            correctOptionIds: ['a', 'c'],
            mode: 'exact-set'
        }
    };

    await t.test('exact-set mode: exact match passes', () => {
        const res = Scoring.scoreItem(question, ['a', 'c']);
        assert.equal(res.status, 'correct');
        assert.equal(res.score, 1);
    });

    await t.test('exact-set mode: case-insensitivity and comma-separated string', () => {
        const res = Scoring.scoreItem(question, 'A, c');
        assert.equal(res.status, 'correct');
        assert.equal(res.score, 1);
    });

    await t.test('exact-set mode: missing option fails', () => {
        const res = Scoring.scoreItem(question, ['a']);
        assert.equal(res.status, 'incorrect');
        assert.equal(res.score, 0);
    });

    await t.test('exact-set mode: extraneous option fails', () => {
        const res = Scoring.scoreItem(question, ['a', 'b', 'c']);
        assert.equal(res.status, 'incorrect');
        assert.equal(res.score, 0);
    });

    await t.test('empty MSQ array returns unanswered', () => {
        const res = Scoring.scoreItem(question, []);
        assert.equal(res.status, 'unanswered');
        assert.equal(res.score, 0);
    });

    await t.test('partial-credit mode awards proportional points', () => {
        const partialQuestion = {
            id: 'q-msq-2',
            type: 'msq',
            answerSpec: {
                correctOptionIds: ['a', 'b', 'c'],
                mode: 'partial-credit'
            }
        };
        const res = Scoring.scoreItem(partialQuestion, ['a', 'b']);
        assert.equal(res.status, 'partial');
        assert.equal(res.score, 0.67);
        assert.equal(res.earnedPercentage, 67);
    });

    await t.test('partial-credit mode penalizes incorrect choices', () => {
        const partialQuestion = {
            id: 'q-msq-2',
            type: 'msq',
            answerSpec: {
                correctOptionIds: ['a', 'b'],
                mode: 'partial-credit'
            }
        };
        const res = Scoring.scoreItem(partialQuestion, ['a', 'd']);
        assert.equal(res.status, 'incorrect');
        assert.equal(res.score, 0);
    });
});

test('MLFScoring - Numeric Evaluation', async (t) => {
    const question = {
        id: 'q-num-1',
        type: 'numeric',
        answerSpec: {
            numericValue: 4.5,
            tolerance: { absolute: 0.1, relative: 0.05 }
        }
    };

    await t.test('exact numeric match passes', () => {
        const res = Scoring.scoreItem(question, 4.5);
        assert.equal(res.status, 'correct');
        assert.equal(res.score, 1);
    });

    await t.test('numeric string format parsed correctly', () => {
        const res = Scoring.scoreItem(question, '4.50');
        assert.equal(res.status, 'correct');
    });

    await t.test('within absolute tolerance passes', () => {
        const res = Scoring.scoreItem(question, 4.42);
        assert.equal(res.status, 'correct');
    });

    await t.test('outside tolerance fails', () => {
        const res = Scoring.scoreItem(question, 5.0);
        assert.equal(res.status, 'incorrect');
        assert.equal(res.score, 0);
    });

    await t.test('target zero (0) handled correctly', () => {
        const zeroQuestion = {
            id: 'q-num-zero',
            type: 'numeric',
            answerSpec: {
                numericValue: 0.0,
                tolerance: { absolute: 0.05 }
            }
        };
        const resZero = Scoring.scoreItem(zeroQuestion, 0);
        assert.equal(resZero.status, 'correct');

        const resNearZero = Scoring.scoreItem(zeroQuestion, '0.02');
        assert.equal(resNearZero.status, 'correct');

        const resOffZero = Scoring.scoreItem(zeroQuestion, '0.1');
        assert.equal(resOffZero.status, 'incorrect');
    });

    await t.test('rejection of NaN, Infinity, -Infinity and invalid syntax', () => {
        assert.equal(Scoring.scoreItem(question, 'NaN').status, 'incorrect');
        assert.equal(Scoring.scoreItem(question, 'Infinity').status, 'incorrect');
        assert.equal(Scoring.scoreItem(question, '-Infinity').status, 'incorrect');
        assert.equal(Scoring.scoreItem(question, '1.2.3.4').status, 'incorrect');
        assert.equal(Scoring.scoreItem(question, 'not_a_number').status, 'incorrect');
    });
});

test('MLFScoring - Derivation & Self-Assessed Questions', async (t) => {
    const question = {
        id: 'q-deriv-1',
        type: 'derivation',
        answerSpec: {}
    };

    await t.test('unanswered open derivation returns self-assessed with 0 score', () => {
        const res = Scoring.scoreItem(question, null);
        assert.equal(res.status, 'unanswered');
    });

    await t.test('student self-assessed score bounded to maxScore', () => {
        const res = Scoring.scoreItem(question, { selfEvalScore: 1 });
        assert.equal(res.status, 'self-assessed');
        assert.equal(res.score, 1);

        const resExceeded = Scoring.scoreItem(question, { selfEvalScore: 10 });
        assert.equal(resExceeded.score, 1); // bounded to maxScore 1
    });
});
