# Comprehensive Repository Audit & Architectural Evaluation
**Project:** Machine Learning Foundations (MLF) Interactive Learning Platform  
**Target Course:** IIT Madras BS in Data Science & Applications — BSCS2004  
**Audit Date:** October 2026  
**Auditor Persona:** Senior Frontend Engineer, Educational Product Designer, Mathematical Content Editor, QA Engineer  
**Repository Working Directory:** `C:\Users\DELL\.gemini\antigravity\scratch\ml-foundations`  
**Remote Git Origin:** `https://github.com/ayushjhaa1187-spec/MLF.git` (`main` branch)  
**Live Site URL:** `https://ayushjhaa1187-spec.github.io/MLF/`  

---

## 1. Executive Summary

This audit assesses the current state of the Machine Learning Foundations (MLF) repository against the rigorous requirements of a complete, mathematically sound, practice-rich educational platform. 

The repository currently provides an initial static website skeleton comprising:
- An `index.html` layout shell utilizing a fixed sidebar and an `<iframe>` container.
- A `home.html` course overview outlining twelve weekly modules and foundational pillars.
- Twelve weekly module folders (`week-1/` through `week-12/`), each containing a chapter lesson (`week-X.html`) and a summary page (`summary.html`).
- A practice portal (`practice/solved_problems.html`) featuring search and filter UI controls with 34 parsed question cards.
- Five standalone Python scripts in `notebooks/`.
- Embedded KaTeX (v0.16.8) and Prism.js (v1.29.0) assets for mathematical typesetting and syntax highlighting.

While the skeleton functions cleanly without external build tools, significant structural, pedagogical, and technical gaps exist between the current state and a premier, university-grade interactive platform. This document categorizes all empirical findings, identifies architectural debt, and lays out the release gates required for modernization.

---

## 2. Entry Points, Routing, and Navigation Architecture

### 2.1 Top-Level Layout (`index.html`)
- **Structure:** Standard HTML5 shell with a fixed top header (`56px`), a collapsible sidebar navigation (`width: 300px`), and a main viewport executing an `<iframe>` (`name="content-frame"`, `src="home.html"`).
- **Navigation Flow:** Anchor links in the sidebar specify `target="content-frame"`. JavaScript event listeners on `.nav-link` manage the `.active` class toggle and auto-collapse the sidebar on mobile viewports ($\le 900\text{px}$).
- **Limitations & Architectural Debt:**
  1. **URL & History Synchronization:** Navigating inside the `<iframe>` does not update the browser address bar's URL or browser history state (`pushState`/`replaceState`). If a user reloads the page while on `week-7/week-7.html`, the browser reloads `index.html` with the iframe reset to `home.html`. Deep-linking to specific chapters or problem sets is impaired.
  2. **Cross-Frame Bookmarkability:** Users cannot directly copy or bookmark the exact lesson URL from the browser URL bar unless they open the iframe source in a new tab.
  3. **Mobile Scroll Jitter & Fullscreen Constraints:** On iOS Safari and Chrome Android, nested iframes cause scroll elasticity issues and prevent standard touch gestures.
  4. **State Isolation:** Client-side progress tracking (e.g., questions solved, quiz scores, bookmarked concepts) stored in `localStorage` requires explicit same-origin postMessage bridging or direct parent-child window communication to maintain seamless synchronization across iframes.

### 2.2 Course Dashboard (`home.html`)
- **Structure:** Metric badges (93 Lectures, 12 Weeks, 4 Pillars), four foundational pillars (Linear Algebra, Multivariate Calculus, Constrained Optimization, Probability & Statistics), and a 12-week syllabus grid.
- **Verification:** All 12 cards link to their respective `week-X/week-X.html` pages.
- **Gaps:** The dashboard lacks a student progress indicator (e.g. "0/12 weeks completed", diagnostic score status), a quick jump to bookmarked formulas, and direct entry into practice tracks.

---

## 3. Weekly Curriculum Content Audit (Weeks 1 to 12)

Every weekly module was inspected for content volume, mathematical completeness, visual illustrations, code examples, and practice integration.

| Week | Directory & Lesson File | Lesson Size | Summary Size | Video Cards | Sections Present | KaTeX Render | Code Snippets | Rigorous 18-Pt Compliance |
|:---:|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **1** | `week-1/week-1.html` | 23.7 KB | 4.1 KB | 9 | 5 | Yes | 1 (NumPy arrays) | ❌ Incomplete (5/18) |
| **2** | `week-2/week-2.html` | 18.3 KB | 4.0 KB | 7 | 5 | Yes | 1 (Taylor series) | ❌ Incomplete (5/18) |
| **3** | `week-3/week-3.html` | 20.3 KB | 3.9 KB | 8 | 5 | Yes | 1 (Least squares) | ❌ Incomplete (6/18) |
| **4** | `week-4/week-4.html` | 18.1 KB | 3.9 KB | 7 | 4 | Yes | 1 (Eigendecomp) | ❌ Incomplete (5/18) |
| **5** | `week-5/week-5.html` | 16.9 KB | 3.9 KB | 6 | 4 | Yes | 1 (Rayleigh/Spectral)| ❌ Incomplete (5/18) |
| **6** | `week-6/week-6.html` | 19.3 KB | 3.9 KB | 7 | 5 | Yes | 1 (SVD compression)| ❌ Incomplete (5/18) |
| **7** | `week-7/week-7.html` | 17.3 KB | 4.0 KB | 6 | 4 | Yes | 1 (PCA from scratch)| ❌ Incomplete (5/18) |
| **8** | `week-8/week-8.html` | 19.3 KB | 4.0 KB | 8 | 4 | Yes | 1 (Gradient descent)| ❌ Incomplete (5/18) |
| **9** | `week-9/week-9.html` | 20.5 KB | 4.0 KB | 8 | 4 | Yes | 1 (Projected GD) | ❌ Incomplete (5/18) |
| **10**| `week-10/week-10.html`| 19.4 KB | 4.0 KB | 7 | 4 | Yes | 1 (Dual SVM) | ❌ Incomplete (5/18) |
| **11**| `week-11/week-11.html`| 28.8 KB | 4.0 KB | 15| 4 | Yes | 1 (Probability dist)| ❌ Incomplete (5/18) |
| **12**| `week-12/week-12.html`| 17.5 KB | 4.0 KB | 5 | 4 | Yes | 1 (GMM & EM) | ❌ Incomplete (5/18) |

### 3.1 Content Analysis & Gaps
1. **Mathematical Depth vs. 18-Point Standard:**
   - Current chapters provide high-level theoretical overviews (approx. 4-5 thematic sections each).
   - They lack full, step-by-step mathematical proofs (e.g. proof of the Orthogonality Principle in Week 3, proof that real symmetric matrices have orthogonal eigenvectors in Week 5, derivation of the KKT conditions in Week 10).
   - They lack detailed numerical walkthroughs with explicit step-by-step arithmetic matrices (e.g. solving $A^T A \hat{x} = A^T b$ by Gaussian elimination, computing $U \Sigma V^T$ step-by-step for a concrete $3 \times 2$ matrix).
2. **Visual & Geometric Intuition:**
   - Visualizations are currently limited to CSS-styled layout cards and SVG icon placeholders.
   - None of the chapters currently include interactive Canvas/SVG visualizers (e.g., interactive column space projection where the user drags vector $b$, or interactive 2D Gaussian contour plots).
3. **Practice & Self-Assessment:**
   - The weekly chapters embed external link cards to `solved_problems.html?week=X`, but lack inline self-assessment quizzes with immediate feedback and progressive hints.
4. **Summary Pages (`summary.html`):**
   - The weekly summary pages are terse (~4 KB each) and repeat high-level bullet points rather than acting as a high-density, formula-rich cheat sheet with common misconception warnings.

---

## 4. Practice Portal & Question Bank Audit (`practice/solved_problems.html`)

### 4.1 Quantitative Inventory
- **Hardcoded Header Metric:** Displays `34 Curated Questions`.
- **Actual Parsed DOM Cards:** Exactly **34** `.problem-card` elements:
  - **IITM Exam/Assignment Questions:** **17** items.
  - **Deep-ML Questions:** **12** items.
  - **LeetCode Questions:** **5** items.
- **Weekly Distribution:**
  - Week 1: 3 problems
  - Week 2: 3 problems
  - Week 3: 3 problems
  - Week 4: 3 problems
  - Week 5: 3 problems
  - Week 6: 3 problems
  - Week 7: 3 problems
  - Week 8: 3 problems
  - Week 9: 3 problems
  - Week 10: 3 problems
  - Week 11: 4 problems
  - Week 12: 3 problems

### 4.2 Provenance & Authenticity Assessment
- **Current State:** The 17 questions marked with the `iitm` platform badge are styled with an "IITM BS Exam" badge. However, they lack explicit provenance metadata (e.g., term, year, whether it is an official Graded Assignment, Mock Quiz, or synthetic exam-style practice problem).
- **Audit Rule Compliance:** Under our working rules, unverified items must never be deceptively labeled as "Official IITM PYQs".
- **Remediation & Available Data:** We have extracted authentic graded assignment PDFs from IIT Madras MLF (Weeks 1 to 11) in our scratch repository (`iitm_mlf_questions.json`). These authentic items must be integrated into the data schema with verified provenance tags (`verified-pyq`), while existing synthetic items must be relabeled as `adapted` or `original`.

### 4.3 Deep-ML & LeetCode Link Verification
- **Deep-ML URL Resolution:**
  - *Audit Finding:* Deep-ML previously failed when using `/problem/<slug>`. All 12 links in `solved_problems.html` now use the verified numeric schema `https://www.deep-ml.com/problems/<id>` (e.g. ID `#14`, `#1`, `#48`, `#6`, `#32`, `#35`, `#12`, `#19`, `#15`, `#17`, `#21`, `#23`).
  - *Status:* **Verified Active**.
- **LeetCode URL Resolution:**
  - *Audit Finding:* The 5 LeetCode links point to standard problems (`sqrtx`, `transpose-matrix`, `powx-n`, `peak-index-in-a-mountain-array`, `random-pick-with-weight`).
  - *Status:* **Verified Active**.

---

## 5. Notebooks & Python Code Assets (`notebooks/`)

### 5.1 Existing Files
1. `notebooks/week3_least_squares.py` (30 lines, 962 bytes) — Computes least squares via normal equation and NumPy `lstsq`.
2. `notebooks/week6_svd_compression.py` (27 lines, 991 bytes) — Performs SVD low-rank image approximation on synthetic matrix.
3. `notebooks/week7_pca_scratch.py` (38 lines, 1,248 bytes) — Computes PCA from scratch using covariance eigendecomposition.
4. `notebooks/week8_gradient_descent.py` (27 lines, 857 bytes) — Implements gradient descent on quadratic bowl $f(x_1, x_2) = x_1^2 + 2x_2^2$.
5. `notebooks/week12_gmm_em.py` (38 lines, 1,356 bytes) — Implements 1D Gaussian Mixture Model Expectation-Maximization.

### 5.2 Deficiencies
- **Curriculum Gaps:** Weeks 1, 2, 4, 5, 9, 10, and 11 have **no standalone script** in `notebooks/`.
- **Quality & Testing:** Existing scripts lack docstrings, input assertions, unit tests, and CLI execution verification.
- **No In-Browser Runner:** Scripts are static text files without an interactive execution harness or Pyodide integration.

---

## 6. External Dependencies, CSS, and Asset Organization

### 6.1 Dependency Inventory
- **Bootstrap 5.3.0:** Loaded via jsDelivr CDN (`bootstrap.min.css`, `bootstrap.bundle.min.js`).
- **FontAwesome 6.4.0:** Loaded via Cloudflare cdnjs (`all.min.css`).
- **Google Fonts:** Inter & JetBrains Mono loaded via `fonts.googleapis.com`.
- **KaTeX 0.16.8:** Loaded via jsDelivr CDN (`katex.min.css`, `katex.min.js`, `auto-render.min.js`).
- **Prism.js 1.29.0:** Loaded via Cloudflare cdnjs (`prism.min.js`, `prism-python.min.js`, `prism-tomorrow.min.css`).

### 6.2 Asset Organization
- `assets/style.css` contains 254 lines of custom CSS covering color variables (`--primary: #0284c7`, `--secondary: #0ea5e9`, `--dark: #0f172a`), card styling, badge design, and KaTeX overrides.
- **Issues:**
  - CSS is monolithic; no modular organization for components (e.g. `components.css`, `layout.css`).
  - Dark mode variables are partially declared in root but lack a toggle system and contrast tokens.
  - No print stylesheets for students printing weekly summaries.

---

## 7. Accessibility (a11y) and Quality Assurance

1. **Semantic HTML & ARIA:**
   - Sidebar lacks `role="navigation"` and proper `aria-expanded` attributes on the mobile hamburger button.
   - `<iframe>` has an accessible name in `index.html` (`title="Course Content Viewport"` is missing; only `name` and `id` are present).
2. **Color Contrast:**
   - Gray text `#94a3b8` on dark background `#0f172a` passes WCAG AA for normal text (contrast ratio ~4.8:1), but some badge combinations (`rgba(56, 189, 248, 0.15)` with light cyan text) require validation on pure white backgrounds.
3. **Keyboard Navigation:**
   - Expandable solution accordions in `solved_problems.html` use Bootstrap collapse, which supports basic keyboard focus, but filter pills are generic `button` elements that lack `aria-pressed` state attributes.

---

## 8. Technical Debt & Risk Matrix

| Risk / Debt Item | Severity | Impact | Mitigation Plan |
|:---|:---:|:---|:---|
| **Iframe State De-synchronization** | Medium | User reloads page and loses location | Add hash/query router in `index.html` + postMessage bridge to iframe |
| **Incomplete Weekly Content (5/18 points)** | High | Inadequate learning experience | Upgrade all 12 chapters to rigorous 18-point textbook standard |
| **Missing Provenance on Practice Items** | High | Misleads students regarding official IITM questions | Categorize all items as `verified-pyq`, `adapted`, or `original` with metadata |
| **Missing Notebooks (7 weeks absent)** | Medium | Students cannot practice Python implementations | Author comprehensive, self-contained Python scripts for all 12 weeks |
| **Lack of Interactive Visual Labs** | High | Misses visual intuition pillar | Build dedicated Canvas/SVG interactive labs (e.g. Projection, SVD, PCA, GD) |
| **Hardcoded Question List in Single HTML** | High | Unmaintainable, cannot support randomized tests or progress tracking | Migrate problem data to structured JSON (`data/questions/`) with dynamic engine |

---

## 9. Conclusion & Release Gate Criteria

The current repository provides a solid aesthetic foundation and playlist coverage, but requires systematic data-driven refactoring to fulfill the 18-point pedagogical standard.

### Release Gate Checklist:
- [x] Phase 1: Comprehensive repository audit and documentation completed.
- [ ] Phase 2: Schema architecture (`data/curriculum.json`, `data/questions/`, `data/concepts.json`) and shared JS utilities deployed.
- [ ] Phase 3: Vertical slice implementation of Week 3 with complete 18-point textbook chapter, interactive visual lab, progressive hints, and unit-tested notebook.
- [ ] Phase 4: Core curriculum upgrade across all 12 modules.
- [ ] Phase 5: Dynamic practice and mock examination portal with authentic IITM questions.
- [ ] Phase 6: Interactive visualizer suite.
- [ ] Phase 7: Complete 12-week NumPy notebook track.
- [ ] Phase 8: Accessibility, cross-browser, and performance verification.
