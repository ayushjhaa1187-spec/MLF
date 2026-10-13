/**
 * MLF Assessment Engine
 * Assessment validation, attempt preparation, and evaluation orchestration.
 * Works in both Browser (window.MLFAssessmentEngine) and Node.js.
 */
(function(root, factory) {
    if (typeof define === 'function' && define.amd) {
        define(['./scoring'], factory);
    } else if (typeof module === 'object' && module.exports) {
        const sc = require('./scoring');
        module.exports = factory(sc);
    } else {
        root.MLFAssessmentEngine = factory(root.MLFScoring);
    }
}(typeof self !== 'undefined' ? self : this, function(Scoring) {
    'use strict';

    const scoringEngine = Scoring || (typeof window !== 'undefined' && window.MLFScoring);

    /**
     * Validates that all question references in an assessment definition exist in the question catalog.
     * @param {Object} assessment - Assessment configuration record from data/assessments.json
     * @param {Object} questionsMap - Map of question ID -> Question object
     * @returns {Object} Validation result { valid, missingQuestionIds, duplicateQuestionIds, totalQuestions }
     */
    function validateAssessmentReferences(assessment, questionsMap) {
        if (!assessment || !Array.isArray(assessment.questionIds)) {
            return {
                valid: false,
                missingQuestionIds: [],
                duplicateQuestionIds: [],
                totalQuestions: 0,
                error: 'Invalid assessment structure or missing questionIds array.'
            };
        }

        const missing = [];
        const seen = new Set();
        const duplicates = [];

        assessment.questionIds.forEach(qid => {
            if (!questionsMap || !questionsMap[qid]) {
                missing.push(qid);
            }
            if (seen.has(qid)) {
                duplicates.push(qid);
            }
            seen.add(qid);
        });

        const isValid = missing.length === 0 && duplicates.length === 0 && assessment.questionIds.length > 0;

        return {
            valid: isValid,
            missingQuestionIds: missing,
            duplicateQuestionIds: duplicates,
            totalQuestions: assessment.questionIds.length,
            error: !isValid ? `Assessment validation failed: ${missing.length} missing questions, ${duplicates.length} duplicate references.` : null
        };
    }

    /**
     * Grades an assessment attempt across all questions using MLFScoring.
     * @param {Object} assessment - Assessment definition
     * @param {Object} questionsMap - Catalog map
     * @param {Object} answers - Student answers { [qid]: response }
     * @returns {Object} Full grade report
     */
    function gradeAttempt(assessment, questionsMap, answers) {
        if (!scoringEngine) {
            throw new Error('MLFAssessmentEngine: Scoring engine module is required.');
        }

        const val = validateAssessmentReferences(assessment, questionsMap);
        if (!val.valid) {
            throw new Error(val.error);
        }

        let totalScore = 0;
        let totalMaxScore = 0;
        let correctCount = 0;
        let incorrectCount = 0;
        let unansweredCount = 0;
        let selfAssessedCount = 0;

        const itemScores = {};
        const weakConcepts = new Map();

        assessment.questionIds.forEach(qid => {
            const question = questionsMap[qid];
            const userAns = answers ? answers[qid] : null;
            const evalResult = scoringEngine.scoreItem(question, userAns, assessment.scoring);

            itemScores[qid] = evalResult;
            totalScore += evalResult.score;
            totalMaxScore += evalResult.maxScore;

            if (evalResult.status === 'correct') {
                correctCount++;
            } else if (evalResult.status === 'incorrect') {
                incorrectCount++;
                collectWeakConcepts(question, evalResult.feedback);
            } else if (evalResult.status === 'unanswered') {
                unansweredCount++;
                collectWeakConcepts(question, 'Unanswered in assessment');
            } else if (evalResult.status === 'self-assessed') {
                selfAssessedCount++;
            }
        });

        function collectWeakConcepts(q, reason) {
            const cids = (q.conceptIds && q.conceptIds.length > 0) ? q.conceptIds : [`week-${q.week}`];
            cids.forEach(cid => {
                if (!weakConcepts.has(cid)) {
                    weakConcepts.set(cid, {
                        conceptId: cid,
                        title: q.title || cid,
                        week: q.week || 1,
                        reason: reason,
                        relatedLesson: q.relatedLesson || `week-${q.week}/week-${q.week}.html`,
                        relatedLab: q.relatedLab || null
                    });
                }
            });
        }

        const percentage = totalMaxScore > 0 ? Math.round((totalScore / totalMaxScore) * 100) : 0;

        return {
            score: Math.max(0, totalScore),
            maxScore: totalMaxScore,
            percentage: Math.min(100, Math.max(0, percentage)),
            counts: {
                total: assessment.questionIds.length,
                correct: correctCount,
                incorrect: incorrectCount,
                unanswered: unansweredCount,
                selfAssessed: selfAssessedCount
            },
            itemScores: itemScores,
            weakConcepts: Array.from(weakConcepts.values())
        };
    }

    return {
        validateAssessmentReferences: validateAssessmentReferences,
        gradeAttempt: gradeAttempt
    };
}));
