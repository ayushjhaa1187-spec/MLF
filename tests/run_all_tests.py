"""
Master Automated Test Suite for Machine Learning Foundations (MLF)
Executes:
1. Data Validation & Canonical Schema Integrity (tests/test_data_validation.py)
2. Mathematical Correctness of Visual Labs (tests/test_labs_math.py)
3. Scoring Engine & Progress State Cleansing (tests/test_scoring_and_progress.py)
4. Internal Link & Asset Resolution Checker (tests/verify_links.py)
5. Algorithmic Python Notebook Verification (tests/verify_all.py)
"""
import os
import sys
import subprocess
import time

REPO_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TESTS_DIR = os.path.join(REPO_DIR, "tests")

SUITES = [
    ("Canonical Data Validation", os.path.join(TESTS_DIR, "test_data_validation.py")),
    ("Visual Labs Mathematics", os.path.join(TESTS_DIR, "test_labs_math.py")),
    ("Scoring & Progress Store Logic", os.path.join(TESTS_DIR, "test_scoring_and_progress.py")),
    ("Internal Relative Links & Assets", os.path.join(TESTS_DIR, "verify_links.py")),
    ("Algorithmic Python Notebooks", os.path.join(TESTS_DIR, "verify_all.py"))
]

def run_suite(name, script_path):
    print(f"\n>> Running Suite: {name} ({os.path.basename(script_path)})")
    t0 = time.time()
    res = subprocess.run([sys.executable, script_path], cwd=REPO_DIR, capture_output=True, text=True)
    dt = time.time() - t0

    if res.returncode == 0:
        print(f"   [PASS] {name} passed in {dt:.2f}s")
        return True, res.stdout
    else:
        print(f"   [FAIL] {name} failed in {dt:.2f}s")
        print(f"--- STDOUT ---\n{res.stdout}")
        print(f"--- STDERR ---\n{res.stderr}")
        return False, res.stderr

def main():
    print("=" * 75)
    print("Machine Learning Foundations (MLF) - Master Automated Test Runner")
    print(f"Root: {REPO_DIR}")
    print("=" * 75)

    all_passed = True
    results = []

    for name, path in SUITES:
        passed, out = run_suite(name, path)
        results.append((name, passed))
        if not passed:
            all_passed = False

    print("\n" + "=" * 75)
    print("FINAL SUMMARY REPORT:")
    print("=" * 75)
    for name, passed in results:
        status_str = "[PASS]" if passed else "[FAIL]"
        print(f"  {status_str} {name}")
    print("=" * 75)

    if all_passed:
        print("SUCCESS: All automated validation, math, data, link, and algorithm suites PASSED!")
        sys.exit(0)
    else:
        print("FAILURE: One or more test suites failed.")
        sys.exit(1)

if __name__ == "__main__":
    main()
