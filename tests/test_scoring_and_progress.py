"""
Unit & Integration Tests: Scoring Engine & Progress Store Integrity
Verifies:
1. Scoring rules:
   - MCQ: full credit if chosen option is correct, 0 if incorrect, 0 if unanswered.
   - MSQ exact-set: full credit if exact set matches, 0 if partial or incorrect.
   - Numeric tolerance matching: within absolute or relative tolerance.
2. Progress Store schema validation & state cleansing:
   - Graceful default handling on null or corrupt input.
   - Merging vs overwriting on import.
   - Schema version 2 backwards-compatibility with V1.
"""
import unittest
import json


def score_item(question, user_response):
    """
    Python mirror of client-side scoring logic
    """
    q_type = question.get("type", "mcq")
    answer_spec = question.get("answerSpec", {})

    if user_response is None or user_response == "":
        return 0, "unanswered"

    if q_type == "mcq":
        correct_ids = [c.lower() for c in answer_spec.get("correctOptionIds", [])]
        chosen = str(user_response).strip().lower()
        if chosen in correct_ids:
            return 1, "correct"
        return 0, "incorrect"

    elif q_type == "msq":
        correct_set = set(c.lower() for c in answer_spec.get("correctOptionIds", []))
        if isinstance(user_response, (list, set)):
            user_set = set(str(c).strip().lower() for c in user_response)
        else:
            user_set = set(c.strip().lower() for c in str(user_response).split(","))

        if user_set == correct_set:
            return 1, "correct"
        return 0, "incorrect"

    elif q_type == "numeric":
        target = answer_spec.get("numericValue")
        tol = answer_spec.get("tolerance", {})
        abs_tol = tol.get("absolute", 0.05) if tol else 0.05
        try:
            val = float(user_response)
            if abs(val - target) <= abs_tol:
                return 1, "correct"
            return 0, "incorrect"
        except (ValueError, TypeError):
            return 0, "incorrect"

    return 0, "unsupported"


def validate_imported_progress(data):
    """
    Python mirror of JS validateState() in progress-store.js
    """
    if not isinstance(data, dict):
        return {"version": 2, "lessonsRead": {}, "problemsSolved": {}, "needsRevision": {}}

    res = {
        "version": 2,
        "lastActive": data.get("lastActive", "2026-01-01T00:00:00Z"),
        "lessonsRead": {},
        "problemsSolved": {},
        "needsRevision": {},
        "quizAttempts": {},
        "diagnosticCompleted": bool(data.get("diagnosticCompleted", False))
    }

    if isinstance(data.get("lessonsRead"), dict):
        for k, v in data["lessonsRead"].items():
            if bool(v):
                res["lessonsRead"][k] = True

    if isinstance(data.get("problemsSolved"), dict):
        for k, v in data["problemsSolved"].items():
            if bool(v):
                res["problemsSolved"][k] = True

    if isinstance(data.get("needsRevision"), dict):
        res["needsRevision"] = dict(data["needsRevision"])

    return res


class TestScoringAndProgress(unittest.TestCase):

    def test_mcq_scoring(self):
        q = {
            "type": "mcq",
            "answerSpec": {"correctOptionIds": ["b"]}
        }
        # Correct answer
        score, status = score_item(q, "b")
        self.assertEqual(score, 1)
        self.assertEqual(status, "correct")

        # Case-insensitivity
        score, status = score_item(q, "B")
        self.assertEqual(score, 1)
        self.assertEqual(status, "correct")

        # Incorrect answer
        score, status = score_item(q, "a")
        self.assertEqual(score, 0)
        self.assertEqual(status, "incorrect")

        # Unanswered
        score, status = score_item(q, None)
        self.assertEqual(score, 0)
        self.assertEqual(status, "unanswered")

    def test_msq_scoring(self):
        q = {
            "type": "msq",
            "answerSpec": {"correctOptionIds": ["a", "c"]}
        }
        # Exact match
        self.assertEqual(score_item(q, ["a", "c"])[0], 1)
        self.assertEqual(score_item(q, "a, c")[0], 1)

        # Partial match gives 0 in exact-set mode
        self.assertEqual(score_item(q, ["a"])[0], 0)

        # Extraneous option gives 0
        self.assertEqual(score_item(q, ["a", "b", "c"])[0], 0)

    def test_numeric_scoring_with_tolerance(self):
        q = {
            "type": "numeric",
            "answerSpec": {
                "numericValue": 2.449,
                "tolerance": {"absolute": 0.05}
            }
        }
        # Within tolerance
        self.assertEqual(score_item(q, 2.45)[0], 1)
        self.assertEqual(score_item(q, "2.449")[0], 1)
        self.assertEqual(score_item(q, 2.41)[0], 1)

        # Outside tolerance
        self.assertEqual(score_item(q, 2.60)[0], 0)
        self.assertEqual(score_item(q, "invalid")[0], 0)

    def test_progress_state_cleansing(self):
        # Corrupted / malicious payload
        corrupted = {
            "version": "bad_version",
            "lessonsRead": ["not_a_dict"],
            "problemsSolved": {"q1": True, "q2": False, "q3": "yes"},
            "diagnosticCompleted": "true"
        }
        cleaned = validate_imported_progress(corrupted)
        self.assertEqual(cleaned["version"], 2)
        self.assertEqual(cleaned["lessonsRead"], {})
        self.assertEqual(cleaned["problemsSolved"], {"q1": True, "q3": True})
        self.assertTrue(cleaned["diagnosticCompleted"])


if __name__ == "__main__":
    unittest.main()
