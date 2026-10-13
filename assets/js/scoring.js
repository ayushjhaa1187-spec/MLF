/**
 * MLF Production Scoring Engine
 * Universal evaluation logic for MCQ, MSQ, Numeric, and Self-Assessed questions.
 * Works in both Browser (window.MLFScoring) and Node.js (CommonJS / ES Module).
 */
(function(root, factory) {
    if (typeof define === 'function' && define.amd) {
        define([], factory);
    } else if (typeof module === 'object' && module.exports) {
        module.exports = factory();
    } else {
        root.MLFScoring = factory();
    }
}(typeof self !== 'undefined' ? self : this, function() {
    'use strict';

    /**
     * Evaluates a single student response against a question's answer specification.
     * @param {Object} question - The canonical question record.
     * @param {any} userResponse - The student's submitted response.
     * @param {Object} [assessmentScoring] - Optional assessment-level scoring rules.
     * @returns {Object} Evaluation result { status, score, maxScore, earnedPercentage, feedback }
     */
    function scoreItem(question, userResponse, assessmentScoring) {
        if (!question) {
            throw new Error('MLFScoring: Question definition is required.');
        }

        const qType = (question.type || 'mcq').toLowerCase();
        const answerSpec = question.answerSpec || {};
        const scoringRules = assessmentScoring || {};

        // Configure default mark and penalty values
        const typeRule = scoringRules[qType] || {};
        const maxScore = typeof typeRule.correct === 'number' ? typeRule.correct : 1;
        const penalty = typeof typeRule.incorrect === 'number' ? typeRule.incorrect : 0;

        // 1. Check for Unanswered
        if (isUnansweredResponse(userResponse)) {
            return {
                status: 'unanswered',
                score: 0,
                maxScore: maxScore,
                earnedPercentage: 0,
                feedback: 'No response submitted.'
            };
        }

        // 2. Multiple Choice Question (Single selection)
        if (qType === 'mcq') {
            const correctIds = (answerSpec.correctOptionIds || []).map(id => String(id).trim().toLowerCase());
            const chosen = String(userResponse).trim().toLowerCase();

            if (correctIds.includes(chosen)) {
                return {
                    status: 'correct',
                    score: maxScore,
                    maxScore: maxScore,
                    earnedPercentage: 100,
                    feedback: 'Correct selection.'
                };
            } else {
                return {
                    status: 'incorrect',
                    score: penalty,
                    maxScore: maxScore,
                    earnedPercentage: 0,
                    feedback: 'Incorrect option selected.'
                };
            }
        }

        // 3. Multiple Select Question (Multi-selection)
        if (qType === 'msq') {
            const correctSet = new Set((answerSpec.correctOptionIds || []).map(id => String(id).trim().toLowerCase()));
            let userSet = new Set();

            if (Array.isArray(userResponse)) {
                userResponse.forEach(id => {
                    if (id !== null && id !== undefined && String(id).trim() !== '') {
                        userSet.add(String(id).trim().toLowerCase());
                    }
                });
            } else if (typeof userResponse === 'string') {
                userResponse.split(',').forEach(id => {
                    const cleaned = id.trim().toLowerCase();
                    if (cleaned) userSet.add(cleaned);
                });
            }

            if (userSet.size === 0) {
                return {
                    status: 'unanswered',
                    score: 0,
                    maxScore: maxScore,
                    earnedPercentage: 0,
                    feedback: 'No options selected.'
                };
            }

            const scoringMode = typeRule.mode || answerSpec.mode || 'exact-set';

            if (scoringMode === 'exact-set') {
                const isExact = setsAreEqual(correctSet, userSet);
                if (isExact) {
                    return {
                        status: 'correct',
                        score: maxScore,
                        maxScore: maxScore,
                        earnedPercentage: 100,
                        feedback: 'All correct options identified.'
                    };
                } else {
                    return {
                        status: 'incorrect',
                        score: penalty,
                        maxScore: maxScore,
                        earnedPercentage: 0,
                        feedback: 'Incorrect set of options selected.'
                    };
                }
            } else if (scoringMode === 'partial-credit') {
                let correctCount = 0;
                let incorrectCount = 0;

                userSet.forEach(id => {
                    if (correctSet.has(id)) correctCount++;
                    else incorrectCount++;
                });

                if (incorrectCount > 0) {
                    return {
                        status: 'incorrect',
                        score: penalty,
                        maxScore: maxScore,
                        earnedPercentage: 0,
                        feedback: 'Penalty applied for incorrect option selections.'
                    };
                }

                const partialScore = correctSet.size > 0 ? (correctCount / correctSet.size) * maxScore : 0;
                const isFull = correctCount === correctSet.size;

                return {
                    status: isFull ? 'correct' : 'partial',
                    score: Math.max(0, parseFloat(partialScore.toFixed(2))),
                    maxScore: maxScore,
                    earnedPercentage: Math.round((partialScore / maxScore) * 100),
                    feedback: isFull ? 'Complete set selected.' : `Partial credit: ${correctCount} of ${correctSet.size} options.`
                };
            }
        }

        // 4. Numeric Value Question
        if (qType === 'numeric') {
            const rawVal = typeof userResponse === 'number' ? userResponse : String(userResponse).trim();
            const parsedNum = typeof rawVal === 'number' ? rawVal : parseFloat(rawVal);

            if (isNaN(parsedNum) || !isFinite(parsedNum) || rawVal === '') {
                return {
                    status: 'incorrect',
                    score: penalty,
                    maxScore: maxScore,
                    earnedPercentage: 0,
                    feedback: 'Invalid numeric input format.'
                };
            }

            const targetVal = answerSpec.numericValue;
            if (typeof targetVal !== 'number' || isNaN(targetVal)) {
                throw new Error(`MLFScoring: Numeric question ${question.id} lacks valid target numericValue.`);
            }

            const tol = answerSpec.tolerance || {};
            const absTol = typeof tol.absolute === 'number' ? tol.absolute : 0.05;
            const relTol = typeof tol.relative === 'number' ? tol.relative : null;

            const diff = Math.abs(parsedNum - targetVal);
            let withinTolerance = diff <= absTol;

            if (!withinTolerance && relTol !== null && targetVal !== 0) {
                const relDiff = diff / Math.abs(targetVal);
                if (relDiff <= relTol) {
                    withinTolerance = true;
                }
            }

            if (withinTolerance) {
                return {
                    status: 'correct',
                    score: maxScore,
                    maxScore: maxScore,
                    earnedPercentage: 100,
                    feedback: `Value ${parsedNum} is within accepted tolerance of ${targetVal}.`
                };
            } else {
                return {
                    status: 'incorrect',
                    score: penalty,
                    maxScore: maxScore,
                    earnedPercentage: 0,
                    feedback: `Value ${parsedNum} is outside accepted tolerance.`
                };
            }
        }

        // 5. Derivation / Coding / Self-Assessed Questions
        if (qType === 'derivation' || qType === 'coding') {
            if (typeof userResponse === 'object' && userResponse !== null && userResponse.selfEvalScore !== undefined) {
                const selfScore = Number(userResponse.selfEvalScore);
                const bounded = Math.min(maxScore, Math.max(0, isNaN(selfScore) ? 0 : selfScore));
                return {
                    status: bounded > 0 ? 'self-assessed' : 'unanswered',
                    score: bounded,
                    maxScore: maxScore,
                    earnedPercentage: Math.round((bounded / maxScore) * 100),
                    feedback: 'Self-assessed against reference derivation rubric.'
                };
            }

            return {
                status: 'self-assessed',
                score: 0,
                maxScore: maxScore,
                earnedPercentage: 0,
                feedback: 'Open derivation requires student self-assessment rubric review.'
            };
        }

        return {
            status: 'unsupported',
            score: 0,
            maxScore: maxScore,
            earnedPercentage: 0,
            feedback: `Unsupported question type: ${qType}`
        };
    }

    function isUnansweredResponse(resp) {
        if (resp === null || resp === undefined) return true;
        if (typeof resp === 'string' && resp.trim() === '') return true;
        if (Array.isArray(resp) && resp.length === 0) return true;
        return false;
    }

    function setsAreEqual(setA, setB) {
        if (setA.size !== setB.size) return false;
        for (const item of setA) {
            if (!setB.has(item)) return false;
        }
        return true;
    }

    return {
        scoreItem: scoreItem,
        isUnansweredResponse: isUnansweredResponse
    };
}));
