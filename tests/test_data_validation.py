"""
Unit & Integration Tests: Data Validation & Canonical Schema Integrity
Verifies:
1. All question IDs in data/questions/all_questions.json are unique.
2. Every question conforms to the canonical schema (week, type, difficulty, platform, provenance, answerSpec).
3. Option IDs are valid and answerSpec.correctOptionIds matches options.
4. data/assessments.json references existing question IDs and question counts are exact.
5. data/questions/week3.json is a valid subset of all_questions.json.
"""
import os
import json
import unittest

REPO_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ALL_Q_PATH = os.path.join(REPO_DIR, "data", "questions", "all_questions.json")
W3_Q_PATH = os.path.join(REPO_DIR, "data", "questions", "week3.json")
ASSESSMENTS_PATH = os.path.join(REPO_DIR, "data", "assessments.json")


class TestDataValidation(unittest.TestCase):

    def setUp(self):
        with open(ALL_Q_PATH, encoding="utf-8") as f:
            self.all_questions = json.load(f)
        with open(W3_Q_PATH, encoding="utf-8") as f:
            self.w3_questions = json.load(f)
        with open(ASSESSMENTS_PATH, encoding="utf-8") as f:
            self.assessments = json.load(f)

    def test_unique_question_ids(self):
        seen = set()
        duplicates = []
        for q in self.all_questions:
            qid = q.get("id")
            self.assertTrue(qid, "Every question must have an ID")
            if qid in seen:
                duplicates.append(qid)
            seen.add(qid)
        self.assertEqual(duplicates, [], f"Found duplicate question IDs: {duplicates}")

    def test_question_schema_fields(self):
        valid_types = {"mcq", "msq", "numeric", "derivation", "coding"}
        valid_difficulties = {"easy", "medium", "hard"}
        valid_platforms = {"local", "deepml", "leetcode"}
        valid_provenances = {"verified-pyq", "adapted", "original", "deepml", "leetcode"}

        for q in self.all_questions:
            qid = q["id"]
            self.assertIn("week", q, f"{qid} missing week")
            self.assertTrue(1 <= q["week"] <= 12, f"{qid} week {q['week']} not in 1..12")

            self.assertIn(q.get("type"), valid_types, f"{qid} has invalid type: {q.get('type')}")
            self.assertIn(q.get("difficulty"), valid_difficulties, f"{qid} has invalid difficulty: {q.get('difficulty')}")
            self.assertIn(q.get("platform"), valid_platforms, f"{qid} has invalid platform: {q.get('platform')}")
            self.assertIn(q.get("provenance"), valid_provenances, f"{qid} has invalid provenance: {q.get('provenance')}")

            # Statement and solution
            stmt = q.get("statement") or q.get("question")
            self.assertTrue(stmt and len(stmt.strip()) > 0, f"{qid} missing statement")

            # Check options for MCQ
            if q.get("type") == "mcq":
                opts = q.get("options", [])
                self.assertTrue(len(opts) >= 2, f"{qid} mcq has fewer than 2 options")
                opt_ids = {opt["id"] for opt in opts if isinstance(opt, dict)}
                correct = q.get("answerSpec", {}).get("correctOptionIds", [])
                self.assertTrue(len(correct) > 0, f"{qid} has no correctOptionIds")
                for c in correct:
                    self.assertIn(c, opt_ids, f"{qid} correct option '{c}' not in options {opt_ids}")

    def test_week3_subset_consistency(self):
        all_q_map = {q["id"]: q for q in self.all_questions}
        for q3 in self.w3_questions:
            qid = q3["id"]
            self.assertIn(qid, all_q_map, f"Week 3 question {qid} not in all_questions.json")
            self.assertEqual(q3["week"], 3, f"Week 3 question {qid} does not have week 3")

    def test_assessments_integrity(self):
        all_q_ids = {q["id"] for q in self.all_questions}
        for aid, a in self.assessments.items():
            qids = a.get("questionIds", [])
            self.assertTrue(len(qids) > 0, f"Assessment {aid} has no questionIds")
            missing = [qid for qid in qids if qid not in all_q_ids]
            self.assertEqual(missing, [], f"Assessment {aid} references missing questions: {missing}")
            # Ensure duration is positive
            self.assertTrue(a.get("durationSeconds", 0) > 0, f"Assessment {aid} invalid durationSeconds")

    def test_honest_assessment_counts(self):
        # Diagnostic: 8 questions
        # Quiz 1: 10 questions
        # Quiz 2: 10 questions
        # End-term: 15 questions
        self.assertEqual(len(self.assessments["diagnostic"]["questionIds"]), 8)
        self.assertEqual(len(self.assessments["quiz1"]["questionIds"]), 10)
        self.assertEqual(len(self.assessments["quiz2"]["questionIds"]), 10)
        self.assertEqual(len(self.assessments["endterm"]["questionIds"]), 15)


if __name__ == "__main__":
    unittest.main()
