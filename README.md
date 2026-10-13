# Machine Learning Foundations - Online Textbook & Companion

> A comprehensive, mathematically rigorous, and code-complete companion textbook for the **IIT Madras BS Degree - Machine Learning Foundations** curriculum.

Inspired by [pdsaiitm.github.io](https://github.com/pdsaiitm/pdsaiitm.github.io), this repository structures the complete **93-video lecture series** into 12 self-contained weekly modules combining theory, LaTeX mathematical derivations, interactive video cards, runnable Python/NumPy implementations, and high-yield revision summaries.

---

## 📚 Curriculum Structure (93 Videos Across 12 Weeks)

| Week | Module Title | Videos | Key Mathematical & Algorithmic Concepts |
| :---: | :--- | :---: | :--- |
| **[Week 1](week-1/week-1.html)** | **Intro to ML & Taxonomy** | 9 | Supervised (Regression vs Classification), Unsupervised (Dim. Reduction, Density Estimation), Empirical Risk Minimization. |
| **[Week 2](week-2/week-2.html)** | **Calculus for ML** | 7 | Sets, Functions, Continuity, Univariate & Multivariate Derivatives, Gradients, Tangent Hyperplanes in $\mathbb{R}^d$. |
| **[Week 3](week-3/week-3.html)** | **Subspaces & Least Squares** | 8 | 4 Fundamental Subspaces ($\text{Col}(A), \text{Row}(A), \text{Null}(A), \text{Null}(A^T)$), Orthogonal Projections, Normal Equations $A^TA\hat{x}=A^Tb$. |
| **[Week 4](week-4/week-4.html)** | **Regression & Eigenvalues** | 7 | Polynomial feature maps, Eigenvalues/Eigenvectors, Diagonalization $A=P\Lambda P^{-1}$, Matrix powers, Fibonacci closed-form. |
| **[Week 5](week-5/week-5.html)** | **Hermitian & Spectral Theory**| 6 | Complex vector spaces, Hermitian matrices ($A=A^*$), Unitary matrices, Spectral Theorem, Rayleigh quotient. |
| **[Week 6](week-6/week-6.html)** | **SVD & Positive Definiteness** | 7 | Singular Value Decomposition ($A=U\Sigma V^T$), Geometry of SVD, Positive Definite matrices ($x^TAx > 0$), Eckart-Young Theorem. |
| **[Week 7](week-7/week-7.html)** | **PCA & Dimensionality Reduction** | 6 | Maximizing projected variance, Covariance matrix eigendecomposition, Scree plots, Reconstruction error minimization. |
| **[Week 8](week-8/week-8.html)** | **Gradient Descent & Optimization** | 8 | First & Second-order optimality conditions, Multivariate Taylor expansions, Hessian curvature, Learning rate dynamics. |
| **[Week 9](week-9/week-9.html)** | **Constrained Opt. & Convexity** | 8 | Equality constraints, Method of Lagrange Multipliers, Projected Gradient Descent, Convex sets & functions (Jensen's inequality). |
| **[Week 10](week-10/week-10.html)**| **Duality & KKT Conditions** | 7 | Primal & Dual problems, Weak/Strong duality, Karush-Kuhn-Tucker (KKT) conditions, Support Vector Machines (SVM). |
| **[Week 11](week-11/week-11.html)**| **Probability Foundations** | 15 | Probability spaces, Bayes' Theorem, Discrete (Bernoulli, Binomial, Poisson, Geometric) & Continuous (Uniform, Gaussian) RVs. |
| **[Week 12](week-12/week-12.html)**| **Gaussians, GMMs & EM** | 5 | Multivariate Normal $\mathcal{N}(\mu, \Sigma)$, MLE, Gaussian Mixture Models, Expectation-Maximization (EM), CLT & Markov/Chebyshev bounds. |

---

## 🛠️ Repository Architecture & Tech Stack

```
ml-foundations/
├── index.html                   # Master Shell (Sidebar TOC + Top Header + Responsive Iframe Viewport)
├── home.html                    # Course Dashboard, 93-video Syllabus Matrix, Learning Pillars
├── README.md                    # Full documentation & syllabus guide
├── assets/
│   └── style.css                # Global stylesheet (Inter font, callouts, cards, mobile drawer)
├── week-1/ ... week-12/
│   ├── week-X.html              # Full textbook chapter with theory, KaTeX, Python code, video cards
│   └── summary.html             # High-yield exam revision sheet & formula summary
├── notebooks/                   # Standalone runnable Python code from scratch
│   ├── week3_least_squares.py
│   ├── week6_svd_compression.py
│   ├── week7_pca_scratch.py
│   ├── week8_gradient_descent.py
│   └── week12_gmm_em.py
└── practice/
    └── solved_problems.html     # Step-by-step solved assignment & exam problems
```

- **Zero Build Overhead**: Pure client-side HTML5, CSS3, and JavaScript. Ready for instant GitHub Pages deployment with zero compilation steps.
- **Client-Side KaTeX**: Fast, crisp rendering of LaTeX mathematics.
- **Prism.js Syntax Highlighting**: Clean Python code blocks.
- **Embedded YouTube Player Cards**: Toggle embedded players or watch directly on YouTube for all 93 videos.

---

## 🚀 How to Run Locally

You can preview the textbook locally using Python's built-in HTTP server:

```bash
cd ml-foundations
python -m http.server 8000
```

Then open your browser at:
```
http://localhost:8000
```

---

## 🌐 Deploying to GitHub Pages

1. Create a new repository on GitHub (e.g. `ml-foundations` or `<your-username>.github.io`).
2. Push this directory to GitHub:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Machine Learning Foundations course textbook"
   git branch -M main
   git remote add origin https://github.com/<your-username>/<repo-name>.git
   git push -u origin main
   ```
3. In your GitHub repository settings:
   - Navigate to **Settings** $\to$ **Pages**.
   - Under **Build and deployment** $\to$ **Source**, choose **Deploy from a branch**.
   - Select the `main` branch and `/ (root)` directory, then click **Save**.
4. Your website will be live at `https://<your-username>.github.io/<repo-name>/`.
