# Master Implementation Plan & Engineering Roadmap
**Project:** Machine Learning Foundations (MLF) Interactive Learning Platform  
**Target Architecture:** Static GitHub Pages, Vanilla HTML5 / Modern ES6+ / Modular CSS, KaTeX, Prism.js, Zero-Backend  
**Document Version:** 1.0.0  
**Date:** October 2026  

---

## 1. Architectural Vision & Core Principles

The upgraded Machine Learning Foundations platform transforms the repository into an authentic, mathematically sound, practice-rich learning ecosystem matching top academic interactive platforms.

### Core Architectural Decisions:
1. **Static, Zero-Backend Delivery:** 100% hosted on GitHub Pages. No Node.js runtime, Python server, database, or external backend required to read, practice, or run assessments.
2. **Data-Presentation Decoupling:** All curriculum entities (lectures, concepts, practice questions, quizzes) are maintained in structured JSON files (`data/`). Presentation components dynamically render this data while fallback static HTML ensures full search engine indexability.
3. **Client-Side State Persistence:** Student progress (read status, solved questions, quiz history, bookmarks) is managed locally via `localStorage` with explicit schema versioning (`MLF_PROGRESS_V1`).
4. **Seamless Navigation & Hash Deep-Linking:** The top-level application shell (`index.html`) supports hash-based deep linking (e.g. `#week-3`, `#problem-bank?week=3`, `#visual-labs/projection`) to ensure bookmarkability and reload stability.
5. **Dual Release Strategy:**
   - **Initial Usable Release (Phases 1–3):** Complete architectural audit, core data schemas, navigation synchronization, and a gold-standard **Vertical Slice on Week 3** featuring all 18 pedagogical elements and an interactive visual lab.
   - **Complete Target Release (Phases 4–8):** Systematic rollout across all 12 weeks, unified Visual Labs suite, interactive Exam Centre, and complete 12-week NumPy notebook track.

---

## 2. Phase-by-Phase Roadmap

### Phase 1: Audit & Planning Documentation (Current)
- [x] Comprehensive code and asset audit (`docs/audit.md`).
- [x] Complete weekly content and module inventory (`docs/content-inventory.md`).
- [x] Master curriculum crosswalk and source registry (`docs/source-register.md`).
- [x] Master implementation plan and engineering roadmap (`docs/implementation-plan.md`).

---

### Phase 2: Foundations & Data Architecture
**Objective:** Establish the data models, state management, and shared UI utilities.
1. **Structured Data Layer (`data/`):**
   - `data/curriculum.json`: Master syllabus, 12 module definitions, weekly learning goals, prerequisites.
   - `data/lectures.json`: All 93 verified lecture records with YouTube IDs, titles, durations, and concepts.
   - `data/concepts.json`: Master concept atlas taxonomy with dependency directed graph.
   - `data/questions/`: Segmented JSON problem banks for Weeks 1–12, tagged with authentic provenance (`verified-pyq`, `adapted`, `original`, `deepml`, `leetcode`).
   - `data/assessments.json`: Preconfigured Mock Quiz 1, Mock Quiz 2, and Mock End-Term Exam schemas.
2. **Modular Client-Side Engine (`assets/js/`):**
   - `assets/js/progress-store.js`: Singleton `MLFProgress` module managing `localStorage` read states, question checkmarks, quiz attempt logs, and mastery analytics.
   - `assets/js/navigation.js`: Top-level router handling URL hash changes, iframe loading, history pushes, and mobile drawer toggles.
   - `assets/js/math-rendering.js`: KaTeX auto-render helper with standard math delimiters (`$...$`, `$$...$$`).
   - `assets/js/problem-bank.js`: Dynamic filtering, search, solution toggle, and progressive hint disclosure engine.

---

### Phase 3: Vertical Slice Implementation (Week 3: Subspaces, Orthogonality & Least Squares)
**Objective:** Set the gold-standard 18-point textbook chapter implementation.
1. **Chapter Upgrade (`week-3/week-3.html`):**
   - Follow all 18 pedagogical points rigorously:
     1. Module Overview & Learning Objectives
     2. Big Picture & Intuition
     3. Conceptual Derivations (Fundamental Theorem of Linear Algebra, Orthogonality Principle $A^T(b - A\hat{x}) = 0$)
     4. Step-by-Step Worked Examples (2 full numerical walkthroughs: $3 \times 2$ overdetermined system solved by Normal Equations & QR)
     5. Geometric & Visual Intuition
     6. Edge Cases, Pitfalls & Failure Modes (Rank-deficient $A$, multicollinearity, ill-conditioned $A^T A$)
     7. Algorithmic Formulation
     8. Clean Python / NumPy Implementation
     9. Computational Complexity & Efficiency ($O(n p^2 + p^3)$ vs QR vs SVD)
     10. Connection to Real Machine Learning (Ordinary Least Squares, Ridge regression, linear classifiers)
     11. Curated Practice Problems (Progressive hint disclosure)
     12. Deep-ML & LeetCode Alignment (Deep-ML #14 Normal Eq, Deep-ML #48 RREF, LeetCode #50)
     13. Exam-Style Practice (Conceptual, numerical, tricky multiple-choice, derivation)
     14. Interactive Self-Assessment Quiz (Instant feedback, full explanations)
     15. Summary & Formula Sheet
     16. Common Misconceptions Table
     17. Mini-Project or Notebook Lab
     18. Next Week Bridge & Prerequisites Check
2. **Interactive Visual Lab:**
   - Embed an interactive Canvas/SVG visualizer: Orthogonal Projection onto Column Space $C(A)$ with draggable target vector $b$, projected vector $p$, and orthogonal error vector $e = b - p$.
3. **Practice & Testing Assets:**
   - Integrate authentic IITM Week 3 Graded Assignment questions with progressive hints.
   - Upgrade `notebooks/week3_least_squares.py` with standalone unit test assertions verifying both normal equations and QR decomposition.

---

### Phase 4: Core Curriculum Rollout (Weeks 1 to 12)
**Objective:** Upgrade all weekly modules to the 18-point pedagogical standard.
- **Batch 1 (Linear Algebra & Calculus Foundations):** Weeks 1, 2, 4, 5.
- **Batch 2 (SVD, PCA & Optimization):** Weeks 6, 7, 8, 9, 10.
- **Batch 3 (Probability & Advanced Models):** Weeks 11, 12.
- **Deliverables:**
  - Full conceptual derivations with KaTeX rendering.
  - At least 2 step-by-step numerical walkthroughs per week.
  - Misconception tables and formula cheat sheets in `summary.html`.
  - Embedded self-assessment quizzes with feedback.

---

### Phase 5: Practice & Exam Engines
**Objective:** Deliver an authentic practice portal and realistic examination simulator.
1. **Dynamic Problem Bank (`practice/solved_problems.html`):**
   - Replace monolithic HTML cards with dynamic rendering from `data/questions/`.
   - Implement filters by Week (1–12), Platform (IITM BS, Deep-ML, LeetCode), Question Type (Conceptual, Numerical, Coding, Derivation), and Difficulty.
   - Multi-stage progressive hints (Hint 1: Concept, Hint 2: Formula, Hint 3: Intermediate step).
   - "Mark as Solved" persistent checkmarks saved in `localStorage`.
2. **Exam Centre (`exam_centre.html`):**
   - **Mock Quiz 1 (Weeks 1–4):** 20 timed questions covering linear algebra, calculus, and least squares.
   - **Mock Quiz 2 (Weeks 5–8):** 20 timed questions covering spectral theory, SVD, PCA, and gradient descent.
   - **Mock End-Term Exam (Weeks 1–12):** Comprehensive 40-question exam with realistic timing (90 min), score calculation, question-by-question review, and weak concept diagnosis.

---

### Phase 6: Visual Labs Suite
**Objective:** Provide intuitive geometric visualizations for abstract mathematical concepts.
1. **Visual Labs Portal (`visual_labs.html`):**
   - **Lab 1: Vector Transformations & Matrix Action** (Week 1)
   - **Lab 2: 2D/3D Hessian Curvature & Tangent Planes** (Week 2)
   - **Lab 3: Orthogonal Projection & Least Squares** (Week 3)
   - **Lab 4: Eigenvector Stretching & Spectral Decomposition** (Weeks 4 & 5)
   - **Lab 5: SVD Geometric Decomposition & Image Rank Compressor** (Week 6)
   - **Lab 6: PCA Variance Maximization Ellipsoid** (Week 7)
   - **Lab 7: Gradient Descent Landscape & Learning Rate Simulator** (Week 8)
   - **Lab 8: Constrained Optimization & KKT Support Vectors** (Weeks 9 & 10)
   - **Lab 9: Gaussian Mixture Model & EM Clustering** (Weeks 11 & 12)

---

### Phase 7: Coding Tracks & Standalone Python Scripts
**Objective:** Deliver working, self-contained Python scripts for every week.
1. **Complete 12-Week Notebook Inventory (`notebooks/`):**
   - `week1_linear_algebra_basics.py`
   - `week2_multivariate_calculus.py`
   - `week3_least_squares.py` (enhanced with assertions)
   - `week4_eigenvalues_regression.py`
   - `week5_spectral_decomposition.py`
   - `week6_svd_compression.py` (enhanced with assertions)
   - `week7_pca_scratch.py` (enhanced with assertions)
   - `week8_gradient_descent.py` (enhanced with assertions)
   - `week9_constrained_optimization.py`
   - `week10_duality_svm.py`
   - `week11_probability_foundations.py`
   - `week12_gmm_em.py` (enhanced with assertions)
2. **Verification Test Harness:**
   - Python test script `tests/verify_notebooks.py` verifying all 12 scripts execute cleanly with zero exit code.

---

### Phase 8: Quality Assurance, Accessibility & Final Release
**Objective:** Polish UI/UX, verify mathematical accuracy, and validate release readiness.
1. **Automated Link & Math Checker:** Verify all internal relative paths, external links, and KaTeX equations parse without errors.
2. **Accessibility Audit:** Add WCAG AA contrast adjustments, ARIA landmark roles, and keyboard navigation support.
3. **Cross-Browser Verification:** Validate on Chrome, Firefox, Safari, and mobile viewports.
4. **Documentation & User Guide:** Complete `README.md` update with local execution instructions and GitHub Pages deployment validation.
