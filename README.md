# Machine Learning Foundations (BSCS2004) — Interactive Learning Platform & Textbook

[![IIT Madras BS Degree](https://img.shields.io/badge/IIT%20Madras-BS%20Degree%20%7C%20BSCS2004-blue)](https://study.iitm.ac.in/ds/course_pages/BSCS2004.html)
[![Playlist Coverage](https://img.shields.io/badge/Lectures-93%20Verified%20Videos-red)](https://youtube.com/playlist?list=PLZ2ps__7DhBammhVmBE9f5eezTj2kDfTN)
[![Interactive Visual Labs](https://img.shields.io/badge/Visual%20Labs-3D%20Canvas%20Engine-success)](visual_labs.html)
[![Problem Bank](https://img.shields.io/badge/Problem%20Bank-53%20Curated%20Questions-orange)](practice/solved_problems.html)
[![Tests Passing](https://img.shields.io/badge/Master%20Test%20Suite-5%2F5%20Passing-brightgreen)](tests/run_all_tests.py)

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
├── visual_labs.html             # Interactive Visual Labs (3D Subspace Projection, Gradient Descent Simulator)
├── concept_atlas.html           # Concept Atlas & Dependency Graph across all 4 Pillars
├── exam_centre.html             # Timed Examination Simulator (Resumable Attempts, Review & Revision Links)
├── revision.html                # Master Formula Vault & Active Personalized Revision Queue
├── progress.html                # Student Progress Dashboard & Local Analytics Engine (Import/Export JSON)
├── README.md                    # Platform documentation
│
├── data/                        # Structured JSON Data Layer
│   ├── curriculum.json          # Syllabus metadata, learning outcomes, foundational pillars
│   ├── lectures.json            # 93 verified lecture records with YouTube IDs, durations, syllabus tags
│   ├── concepts.json            # Master concept ontology and dependency hierarchy
│   ├── assessments.json         # Diagnostic, Quiz 1, Quiz 2, End-term assessment schemas
│   └── questions/               # Curated Problem Banks
│       ├── week3.json           # 16 High-yield Week 3 questions (Course Practice, Deep-ML, LeetCode)
│       └── all_questions.json   # 53 Master curated canonical questions across all 12 weeks
│
├── assets/                      # Shared Static Assets & Modular Engine
│   ├── style.css                # CSS Variables, dark header, cards, callout alerts, responsive drawer
│   └── js/
│       ├── progress-store.js    # Singleton localStorage state store (MLF_PROGRESS_V2) with memory fallback
│       ├── navigation.js        # Hash-based deep link router and iframe history synchronizer
│       ├── math-rendering.js    # KaTeX auto-render helper ($...$ and $$...$$ delimiters)
│       └── problem-bank.js      # Dynamic problem bank engine with progressive hints and filters
│
├── week-1/ ... week-12/
│   ├── week-X.html              # Comprehensive textbook chapters (Gold-standard 18-point rubric on Week 3)
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
│   ├── run_all_tests.py         # Master test runner (Data, Math, Scoring, Links, Notebooks)
│   ├── test_data_validation.py  # Canonical schema integrity and honest question count asserts
│   ├── test_labs_math.py        # Subspace orthogonality and gradient descent convergence proofs
│   ├── test_scoring_and_progress.py # MCQ/MSQ scoring rules and progress store state cleansing
│   ├── verify_all.py            # Executes all 12 Python notebooks and asserts mathematical correctness
│   └── verify_links.py          # Verifies internal links and JSON files with zero broken paths
│
└── docs/                        # Formal Audit & Curriculum Crosswalk Documentation
    ├── current-status.md        # Detailed findings resolution matrix and test execution report
    ├── audit.md                 # Technical audit of navigation, routing, iframes, dependencies
    ├── content-inventory.md     # Module-by-module content verification analysis
    ├── source-register.md       # Master crosswalk for all 93 playlist videos
    └── implementation-plan.md   # Phased engineering roadmap
```

---

## 🎯 The 18-Point Textbook Chapter Rubric (Week 3 Vertical Slice)

Every comprehensive textbook chapter adheres to the rigorous 18-point standard:
1. **Module Overview & Objectives:** Syllabus scope and formal learning goals.
2. **Big Picture & Intuition:** Geometric motivation in data science and machine learning.
3. **Conceptual Derivations:** Four fundamental subspaces, direct sums, orthogonality principle $A^T(b - A\hat{x}) = 0$, projection operator $P = A(A^T A)^{-1} A^T$.
4. **Step-by-Step Worked Examples:** 2 full numerical walkthroughs with intermediate matrix arithmetic.
5. **Interactive Visual Lab:** Embedded real-time Canvas 3D engine demonstrating $p \in C(A)$ and $e \perp C(A)$.
6. **Edge Cases, Pitfalls & Failures:** Rank deficiency, multicollinearity, condition number squaring $\kappa(A^T A) = \kappa(A)^2$.
7. **Algorithmic Formulation:** Normal Equations vs. QR Factorization ($R \hat{x} = Q^T b$) vs. SVD.
8. **Clean Python / NumPy Implementation:** Self-contained code comparing Normal Equations and QR with test assertions.
9. **Computational Complexity & Efficiency:** Flop counts and memory requirements.
10. **Connection to Real Machine Learning:** Ordinary Least Squares, Ridge Regularization, and Kernel Ridge Regression.
11. **Curated Practice Problems:** Multi-stage cumulative hints.
12. **Deep-ML & LeetCode Alignment:** Verified links to Deep-ML #14 (Normal Eq), Deep-ML #48 (RREF), LeetCode #50.
13. **Exam-Style Practice:** Authentic IIT Madras Graded Assignment questions.
14. **Interactive Self-Assessment Quiz:** Instant scoring and feedback.
15. **Summary & Formula Sheet:** High-yield printable cheat sheet.
16. **Common Misconceptions Table:** Detailed mathematical fallacies vs. reality.
17. **Mini-Project / Notebook Lab:** Outlier detection via leverage scores $h_{ii} = P_{ii}$.
18. **Next Week Bridge:** Prerequisite checklist leading into Week 4.

---

## 💻 Running the Test Suite Locally

Run all automated test suites with a single command:

```bash
# Run Master Test Runner (executes all 5 test suites)
python tests/run_all_tests.py
```

Or execute individual test suites:

```bash
# 1. Canonical question schema and assessment reference validation
python tests/test_data_validation.py

# 2. Mathematical physics and convergence proofs for visual labs
python tests/test_labs_math.py

# 3. Scoring rules and progress state cleansing tests
python tests/test_scoring_and_progress.py

# 4. Internal relative links and JSON parse validation
python tests/verify_links.py

# 5. Algorithmic Python notebook execution (12/12 passing)
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
