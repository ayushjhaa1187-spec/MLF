# Machine Learning Foundations (BSCS2004) — Interactive Learning Platform & Textbook
#DIPLOMA IN PROGRAMMING!

[![IIT Madras BS Degree](https://img.shields.io/badge/IIT%20Madras-BS%20Degree%20%7C%20BSCS2004-blue)](https://study.iitm.ac.in/ds/course_pages/BSCS2004.html)
[![Playlist Coverage](https://img.shields.io/badge/Lectures-93%20Verified%20Videos-red)](https://youtube.com/playlist?list=PLZ2ps__7DhBammhVmBE9f5eezTj2kDfTN)
[![Interactive Visual Labs](https://img.shields.io/badge/Visual%20Labs-4%20Canvas%20Engines-success)](visual_labs.html)
[![Problem Bank](https://img.shields.io/badge/Problem%20Bank-98%20Curated%20Questions-orange)](practice/solved_problems.html)
[![Tests Passing](https://img.shields.io/badge/Master%20Test%20Suite-6%2F6%20Passing-brightgreen)](tests/run_all_tests.py)
[![Unit Tests](https://img.shields.io/badge/Node.js%20Tests-47%2F47%20Passing-brightgreen)](tests/unit/)

> An authentic, mathematically sound, practice-rich interactive learning platform for the **IIT Madras BS Degree in Data Science & Applications — Machine Learning Foundations (BSCS2004)** curriculum.

Live Platform: [https://ayushjhaa1187-spec.github.io/MLF/](https://ayushjhaa1187-spec.github.io/MLF/)  
Primary Lecture Playlist: [YouTube 93-Lecture Series](https://youtube.com/playlist?list=PLZ2ps__7DhBammhVmBE9f5eezTj2kDfTN)

---

## 🏛️ Platform Architecture & 10 Core Destinations

The platform implements a closed-loop 6-stage mastery cycle:  
**Lesson $\longrightarrow$ Visual Lab $\longrightarrow$ Practice $\longrightarrow$ Assessment $\longrightarrow$ Submitted Review $\longrightarrow$ Targeted Revision**.

```
ml-foundations/
├── index.html                   # Master Shell (10-Section Navigation + Top Header + Responsive Viewport)
├── home.html                    # Course Dashboard, 93-video Syllabus Matrix, 4 Foundational Pillars
├── start_here.html              # Course Orientation, 8-Question Prerequisite Diagnostic, Notation Guide
├── visual_labs.html             # 4 Interactive Visual Labs (Projection, Gradient Descent, SVD, PCA)
├── concept_atlas.html           # Concept Atlas & Dependency Graph across all 4 Pillars
├── exam_centre.html             # Timed Examination Simulator (7 Assessments, Resumable Attempts, Review)
├── revision.html                # Master Formula Vault & Active Personalized Revision Queue
├── progress.html                # Student Progress Dashboard (Memory Fallback Alert, JSON Import/Export)
├── README.md                    # Platform documentation
│
├── data/                        # Structured JSON Data Layer
│   ├── curriculum.json          # Syllabus metadata, learning outcomes, foundational pillars
│   ├── lectures.json            # 93 verified lecture records with YouTube IDs, durations, syllabus tags
│   ├── concepts.json            # Master concept ontology and dependency hierarchy
│   ├── assessments.json         # 7 assessments (Diagnostic, Quiz 1, Quiz 2, End-term, Week 3/6/7 Mastery)
│   └── questions/               # Curated Problem Banks (98 Total Canonical Questions)
│       ├── week3.json           # 25 High-yield Week 3 questions (Course Practice, Deep-ML, LeetCode)
│       ├── week6.json           # 20 High-yield Week 6 questions (SVD, Eckart-Young, Pseudoinverse)
│       ├── week7.json           # 20 High-yield Week 7 questions (PCA, Covariance, Variance Optimization)
│       └── all_questions.json   # 98 Master curated canonical questions across all 12 weeks
│
├── assets/                      # Shared Static Assets & Modular Engine
│   ├── style.css                # CSS Variables, dark header, cards, callout alerts, responsive drawer
│   └── js/
│       ├── scoring.js           # Universal scoring engine (MCQ, MSQ, Numeric tolerance, Derivation)
│       ├── progress-validation.js # Schema V2 validation and tolerant storage sanitization
│       ├── progress-store.js    # Singleton state store with active storage mode tracking & memory fallback
│       ├── assessment-engine.js # Pre-validation reference checker and attempt grading engine
│       ├── navigation.js        # Hash-based deep link router and iframe history synchronizer
│       ├── math-rendering.js    # KaTeX auto-render helper ($...$ and $$...$$ delimiters)
│       └── problem-bank.js      # Dynamic problem bank engine with progressive hints and filters
│
├── week-1/ ... week-12/
│   ├── week-X.html              # Comprehensive textbook chapters (18-point rubric on Weeks 3, 6, and 7)
│   └── summary.html             # High-yield revision formula cheat sheets
│
├── notebooks/                   # Standalone, runnable Python implementations with test assertions
│   ├── week1_linear_algebra_basics.py
│   ├── week2_multivariate_calculus.py
│   ├── week3_least_squares.py
│   ├── week4_eigenvalues_regression.py
│   ├── week5_spectral_decomposition.py
│   ├── week6_svd_compression.py
│   ├── week7_pca_scratch.py
│   ├── week8_gradient_descent.py
│   ├── week9_constrained_optimization.py
│   ├── week10_duality_svm.py
│   ├── week11_probability_foundations.py
│   └── week12_gmm_em.py
│
├── tests/                       # Automated Verification Test Suite
│   ├── run_all_tests.py         # Master test runner (Node JS, Data, Math, Scoring, Links, Notebooks)
│   ├── test_data_validation.py  # Canonical schema integrity and honest question count asserts
│   ├── test_labs_math.py        # Subspace orthogonality, SVD errors, PCA Pythagorean conservation
│   ├── test_scoring_and_progress.py # Python baseline tests for scoring & progress cleansing
│   ├── verify_all.py            # Executes all 12 Python notebooks and asserts mathematical correctness
│   ├── verify_links.py          # Verifies internal links and JSON files with zero broken paths
│   └── unit/                    # Production JavaScript Node Unit Tests (node --test)
│       ├── scoring.test.mjs     # 14 tests covering MCQ, MSQ, Numeric tolerances, Derivations
│       ├── progress.test.mjs    # 21 tests covering schema V2, import validation, storage fallbacks
│       ├── assessment-engine.test.mjs # 12 tests covering reference checking & grading
│       └── data-integrity.test.mjs   # Production JSON integrity tests
│
└── docs/                        # Formal Audit, Status & Evidence Documentation
    ├── current-status.md        # Detailed findings resolution matrix and test execution report
    ├── evidence-matrix.md       # Two-tier evidence verification register
    ├── audit.md                 # Technical audit of navigation, routing, iframes, dependencies
    ├── content-inventory.md     # Module-by-module content verification analysis
    ├── source-register.md       # Master crosswalk for all 93 playlist videos
    └── implementation-plan.md   # Phased engineering roadmap
```

---

## 🎯 The 18-Point Textbook Chapter Rubric (Weeks 3, 6, and 7)

Every comprehensive textbook chapter adheres to the rigorous 18-point standard:
1. **Module Overview & Objectives:** Syllabus scope and formal learning goals.
2. **Big Picture & Intuition:** Geometric motivation in data science and machine learning.
3. **Conceptual Derivations:** Mathematical foundations and first-principles proofs (e.g. $A^T(b - A\hat{x}) = 0$, $A = U \Sigma V^T$, Lagrangian variance optimization).
4. **Step-by-Step Worked Examples:** 2 full numerical walkthroughs with complete intermediate arithmetic.
5. **Interactive Visual Lab:** Embedded real-time Canvas 3D or 2D transformation engine.
6. **Edge Cases, Pitfalls & Failures:** Degenerate scenarios, condition numbers, zero variance, and numerical stability.
7. **Algorithmic Formulation:** Clear step-by-step pseudo-code and numerical approaches.
8. **Clean Python / NumPy Implementation:** Self-contained code with automated test assertions.
9. **Computational Complexity & Efficiency:** Flop counts and memory footprint.
10. **Connection to Real Machine Learning:** Direct applications to modern data science algorithms.
11. **Curated Practice Problems:** Multi-stage questions with progressive hints.
12. **Deep-ML & LeetCode Alignment:** Verified links to authentic platform problem sets.
13. **Exam-Style Practice:** Authentic IIT Madras Graded Assignment style questions.
14. **Interactive Self-Assessment Quiz:** Instant scoring and feedback.
15. **Summary & Formula Sheet:** High-yield printable cheat sheet.
16. **Common Misconceptions Table:** Detailed mathematical fallacies vs. rigorous facts.
17. **Mini-Project / Notebook Lab:** Applied computational exercise.
18. **Next Week Bridge:** Prerequisite checklist leading into the subsequent week.

---

## 💻 Running the Test Suite Locally

Run all automated test suites with a single command:

```bash
# Run Master Test Runner (executes Node JS unit tests + all 5 Python test suites)
python tests/run_all_tests.py
```

Or execute individual test suites:

```bash
# 1. Native Node.js Unit Tests for production JavaScript modules (47 tests)
node --test tests/unit/*.test.mjs

# 2. Canonical question schema and assessment reference validation
python tests/test_data_validation.py

# 3. Mathematical physics and convergence proofs for visual labs
python tests/test_labs_math.py

# 4. Scoring rules and progress state cleansing tests
python tests/test_scoring_and_progress.py

# 5. Internal relative links and JSON parse validation
python tests/verify_links.py

# 6. Algorithmic Python notebook execution (12/12 passing)
python tests/verify_all.py
```

---

## 🌐 Running the Platform Locally

Launch the local static server:

```bash
# Start local HTTP server
python -m http.server 8000
```

Open your browser at: `http://localhost:8000`

---

## 🎓 Verified Problem Provenance & Platforms

- **IIT Madras BS Graded Assignments & Course Practice:** Transcribed from course archives with verified step-by-step arithmetic explanations and canonical multiple-choice options.
- **Deep-ML Challenges:** Verified numeric URLs:
  - `#1`: Matrix-Vector Dot Product
  - `#2`: Transpose of a Matrix
  - `#6`: Calculate Eigenvalues of a 2x2 Matrix
  - `#12`: SVD of 2x2 Matrix
  - `#14`: Linear Regression Using Normal Equation
  - `#15`: Linear Regression Using Gradient Descent
  - `#17`: K-Means Clustering
  - `#19`: Principal Component Analysis (PCA)
  - `#21`: Pegasos Kernel SVM
  - `#23`: Softmax Activation Function
  - `#32`: Polynomial Features
  - `#35`: Vector to Diagonal Matrix
  - `#48`: Reduced Row Echelon Form (RREF)
- **LeetCode Algorithmic Math:** Verified problem slugs (`powx-n`, `sqrtx`, `transpose-matrix`, `peak-index-in-a-mountain-array`, `random-pick-with-weight`).
