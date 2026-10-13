# Machine Learning Foundations (BSCS2004) — Interactive Learning Platform & Textbook

[![IIT Madras BS Degree](https://img.shields.io/badge/IIT%20Madras-BS%20Degree%20%7C%20BSCS2004-blue)](https://study.iitm.ac.in/ds/course_pages/BSCS2004.html)
[![Playlist Coverage](https://img.shields.io/badge/Lectures-93%20Verified%20Videos-red)](https://youtube.com/playlist?list=PLZ2ps__7DhBammhVmBE9f5eezTj2kDfTN)
[![Interactive Visual Labs](https://img.shields.io/badge/Visual%20Labs-3D%20Canvas%20Engine-success)](visual_labs.html)
[![Problem Bank](https://img.shields.io/badge/Problem%20Bank-Authentic%20PYQs%20%26%20Deep--ML-orange)](practice/solved_problems.html)
[![Tests Passing](https://img.shields.io/badge/Algorithm%20Tests-12%2F12%20Passing-brightgreen)](tests/verify_all.py)

> An authentic, mathematically sound, practice-rich interactive learning platform for the **IIT Madras BS Degree in Data Science & Applications — Machine Learning Foundations (BSCS2004)** curriculum.

Live Platform: [https://ayushjhaa1187-spec.github.io/MLF/](https://ayushjhaa1187-spec.github.io/MLF/)  
Primary Lecture Playlist: [YouTube 93-Lecture Series](https://youtube.com/playlist?list=PLZ2ps__7DhBammhVmBE9f5eezTj2kDfTN)

---

## 🏛️ Platform Architecture & 10 Core Destinations

The platform is designed around the 7-step mastery cycle:  
**Learn $\to$ Visualize $\to$ Calculate $\to$ Practice $\to$ Implement $\to$ Revise $\to$ Test**.

```
ml-foundations/
├── index.html                   # Master Shell (10-Section Navigation + Top Header + Responsive Iframe Viewport)
├── home.html                    # Course Dashboard, 93-video Syllabus Matrix, 4 Foundational Pillars
├── start_here.html              # Course Orientation, 15-Question Prerequisite Diagnostic, Notation Guide
├── visual_labs.html             # Interactive Visual Labs (3D Subspace Projection, Gradient Descent Simulator)
├── concept_atlas.html           # Concept Atlas & Dependency Graph across all 4 Pillars
├── exam_centre.html             # Timed Examination Simulator (Mock Quiz 1, Mock Quiz 2, End-Term)
├── revision.html                # Master Formula Vault & Common Misconceptions Matrix
├── progress.html                # Student Progress Dashboard & Local Analytics Engine
├── README.md                    # Comprehensive platform documentation
│
├── data/                        # Structured JSON Data Layer
│   ├── curriculum.json          # Syllabus metadata, learning outcomes, foundational pillars
│   ├── lectures.json            # 93 verified lecture records with YouTube IDs, durations, syllabus tags
│   ├── concepts.json            # Master concept ontology and dependency hierarchy
│   ├── assessments.json         # Diagnostic and mock assessment schemas
│   └── questions/               # Curated Problem Banks
│       ├── week3.json           # 16 High-yield Week 3 questions (Authentic IITM GA3, Deep-ML, LeetCode)
│       └── all_questions.json   # 45 Master curated questions across all weeks
│
├── assets/                      # Shared Static Assets & Modular Engine
│   ├── style.css                # CSS Variables, dark header, cards, callout alerts, responsive drawer
│   └── js/
│       ├── progress-store.js    # Singleton localStorage state store (MLF_PROGRESS_V1) & cross-frame sync
│       ├── navigation.js        # Hash-based deep link router and iframe history synchronizer
│       ├── math-rendering.js    # KaTeX auto-render helper ($...$ and $$...$$ delimiters)
│       └── problem-bank.js      # Dynamic problem bank engine with multi-stage hints and filters
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
│   ├── verify_all.py            # Executes all 12 Python notebooks and asserts mathematical correctness
│   └── verify_links.py          # Verifies all 213+ internal links and JSON files with zero broken paths
│
└── docs/                        # Formal Audit & Curriculum Crosswalk Documentation
    ├── audit.md                 # Technical audit of navigation, routing, iframes, dependencies, accessibility
    ├── content-inventory.md     # Module-by-module content verification analysis (PV / PI / PU / M)
    ├── source-register.md       # Master crosswalk for all 93 playlist videos and authentic IITM PYQ provenance
    └── implementation-plan.md   # Phased engineering roadmap
```

---

## 🎯 The 18-Point Textbook Chapter Rubric (Week 3 Vertical Slice)

Every comprehensive textbook chapter adheres to the rigorous 18-point standard:
1. **Module Overview & Objectives:** Syllabus scope and formal learning goals.
2. **Big Picture & Intuition:** Geometric motivation in data science and machine learning.
3. **Conceptual Derivations:** Four fundamental subspaces, direct sums, orthogonality principle $A^T(b - A\hat{x}) = 0$, projection operator $P = A(A^T A)^{-1} A^T$.
4. **Step-by-Step Worked Examples:** At least 2 full numerical walkthroughs with intermediate matrix arithmetic.
5. **Interactive Visual Lab:** Embedded real-time Canvas 3D engine demonstrating $p \in C(A)$ and $e \perp C(A)$.
6. **Edge Cases, Pitfalls & Failures:** Rank deficiency, multicollinearity, condition number squaring $\kappa(A^T A) = \kappa(A)^2$.
7. **Algorithmic Formulation:** Normal Equations vs. QR Factorization ($R \hat{x} = Q^T b$) vs. SVD.
8. **Clean Python / NumPy Implementation:** Self-contained code comparing Normal Equations and QR with test assertions.
9. **Computational Complexity & Efficiency:** Flop counts and memory requirements.
10. **Connection to Real Machine Learning:** Ordinary Least Squares, Ridge Regularization, and Kernel Ridge Regression.
11. **Curated Practice Problems:** Multi-stage hints (Hint 1: Concept, Hint 2: Formula, Hint 3: Intermediate computation).
12. **Deep-ML & LeetCode Alignment:** Verified links to Deep-ML #14 (Normal Eq), Deep-ML #48 (RREF), LeetCode #50.
13. **Exam-Style Practice:** Authentic IIT Madras Graded Assignment questions.
14. **Interactive Self-Assessment Quiz:** Instant scoring and feedback.
15. **Summary & Formula Sheet:** High-yield printable cheat sheet.
16. **Common Misconceptions Table:** Detailed mathematical fallacies vs. reality.
17. **Mini-Project / Notebook Lab:** Outlier detection via leverage scores $h_{ii} = P_{ii}$.
18. **Next Week Bridge:** Prerequisite checklist leading into Week 4.

---

## 💻 Running the Test Suite Locally

Verify all Python algorithms and link integrity locally:

```bash
# 1. Run algorithm test suite (Verifies 12/12 notebooks)
python tests/verify_all.py

# 2. Run link integrity and JSON data validation
python tests/verify_links.py
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

- **IIT Madras BS Graded Assignments:** Transcribed directly from official course archives with verified step-by-step arithmetic explanations.
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
