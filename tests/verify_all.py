"""
Comprehensive Automated Test Runner for Machine Learning Foundations Platform
Verifies that all Python notebooks execute without errors and pass mathematical assertions.
"""
import os
import subprocess
import sys

repo_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
nb_dir = os.path.join(repo_dir, "notebooks")

def main():
    print("=" * 70)
    print("ML Foundations Automated Test Suite - Algorithm Verification")
    print(f"Target Directory: {nb_dir}")
    print("=" * 70)

    notebook_files = sorted([f for f in os.listdir(nb_dir) if f.endswith(".py")])
    if not notebook_files:
        print("ERROR: No Python notebooks found!")
        sys.exit(1)

    passed = 0
    failed = 0

    for idx, fname in enumerate(notebook_files, 1):
        fpath = os.path.join(nb_dir, fname)
        print(f"[{idx:02d}/{len(notebook_files):02d}] Testing {fname} ...", end=" ")
        
        res = subprocess.run([sys.executable, fpath], capture_output=True, text=True)
        if res.returncode == 0:
            print("PASSED")
            passed += 1
        else:
            print("FAILED")
            print(f"--- STDOUT ---\n{res.stdout}")
            print(f"--- STDERR ---\n{res.stderr}")
            failed += 1

    print("=" * 70)
    print(f"Test Summary: {passed} PASSED, {failed} FAILED out of {len(notebook_files)} scripts.")
    print("=" * 70)

    if failed > 0:
        sys.exit(1)
    else:
        print("All machine learning and linear algebra algorithm tests passed successfully!")
        sys.exit(0)

if __name__ == "__main__":
    main()
