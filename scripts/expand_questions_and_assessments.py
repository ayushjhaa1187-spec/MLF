"""
Expands question bank and assessments:
- Week 3: adds 9 reviewed original questions (Total: 25)
- Week 6: adds 18 reviewed original questions (Total: 20)
- Week 7: adds 18 reviewed original questions (Total: 20)
- Adds 'week3-mastery', 'week6-mastery', 'week7-mastery' assessments to assessments.json
"""
import json
import os

REPO_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ALL_Q_PATH = os.path.join(REPO_DIR, "data", "questions", "all_questions.json")
W3_Q_PATH = os.path.join(REPO_DIR, "data", "questions", "week3.json")
W6_Q_PATH = os.path.join(REPO_DIR, "data", "questions", "week6.json")
W7_Q_PATH = os.path.join(REPO_DIR, "data", "questions", "week7.json")
ASSESSMENTS_PATH = os.path.join(REPO_DIR, "data", "assessments.json")

# ==============================================================================
# WEEK 3 QUESTIONS (9 new questions, bringing total to 25)
# ==============================================================================
WEEK3_NEW = [
    {
        "id": "w3-orig-q14",
        "version": 1,
        "title": "Properties of Orthogonal Projection Matrices",
        "week": 3,
        "conceptIds": ["projection-matrix", "subspaces"],
        "prerequisiteConceptIds": ["inner-product"],
        "type": "msq",
        "difficulty": "medium",
        "estimatedMinutes": 4,
        "platform": "local",
        "provenance": "original",
        "verificationStatus": "reviewed",
        "source": {"citation": "Original MLF Subspace Geometry Exercise", "url": None},
        "statement": "Let $P \\in \\mathbb{R}^{n \\times n}$ be an orthogonal projection matrix onto a subspace $S \\subset \\mathbb{R}^n$. Which of the following statements are **always** true?",
        "options": [
            {"id": "a", "text": "$P^2 = P$ (Idempotence)"},
            {"id": "b", "text": "$P^T = P$ (Symmetry / Self-adjointness)"},
            {"id": "c", "text": "All eigenvalues of $P$ lie in the discrete set $\\{0, 1\\}$"},
            {"id": "d", "text": "$\\det(P) = 1$ whenever $\\dim(S) < n$"}
        ],
        "answerSpec": {"correctOptionIds": ["a", "b", "c"], "numericValue": None, "tolerance": None},
        "hints": [
            "An orthogonal projection preserves any vector already in the subspace: $P(Pv) = Pv$, so $P^2 = P$.",
            "Orthogonality implies $(Pv)^T(I-P)v = 0$ for all $v$, leading to $P^T = P$.",
            "If $Pv = \\lambda v$, then $P^2 v = \\lambda^2 v = \\lambda v$, which implies $\\lambda(\\lambda - 1) = 0$.",
            "If $\\dim(S) < n$, the nullspace of $P$ contains non-zero vectors, making $\\det(P) = 0$, not 1."
        ],
        "solution": "Orthogonal projection matrices satisfy $P = P^2$ (idempotent) and $P = P^T$ (symmetric). Since $P^2 = P$, any eigenvalue $\\lambda$ must satisfy $\\lambda^2 = \\lambda$, meaning $\\lambda \\in \\{0, 1\\}$. The determinant is the product of eigenvalues, so $\\det(P) = 1^{\\dim(S)} \\cdot 0^{n-\\dim(S)} = 0$ whenever $\\dim(S) < n$. Thus options A, B, and C are correct.",
        "commonMistakes": ["Confusing orthogonal projection ($P^T = P = P^2$) with orthogonal matrix ($Q^T Q = I$)."],
        "relatedLesson": "week-3/week-3.html",
        "relatedLab": "visual_labs.html#lab-projection"
    },
    {
        "id": "w3-orig-q15",
        "version": 1,
        "title": "Normal Equations: One-Parameter Least Squares",
        "week": 3,
        "conceptIds": ["least-squares", "normal-equations"],
        "prerequisiteConceptIds": ["inner-product"],
        "type": "numeric",
        "difficulty": "easy",
        "estimatedMinutes": 3,
        "platform": "local",
        "provenance": "original",
        "verificationStatus": "reviewed",
        "source": {"citation": "Original MLF Linear Regression Exercise", "url": None},
        "statement": "Given three 1D data points $(x_i, y_i) \\in \\{(1, 2), (2, 5), (3, 7)\\}$, we fit the model $y = \\theta x$ passing through the origin using ordinary least squares. Compute the optimal coefficient $\\theta^* = \\frac{\\sum_{i=1}^3 x_i y_i}{\\sum_{i=1}^3 x_i^2}$. Enter your answer rounded to two decimal places.",
        "options": [],
        "answerSpec": {"correctOptionIds": [], "numericValue": 2.36, "tolerance": 0.02},
        "hints": [
            "Compute numerator: $\\sum x_i y_i = 1(2) + 2(5) + 3(7)$.",
            "Compute denominator: $\\sum x_i^2 = 1^2 + 2^2 + 3^2$.",
            "Divide numerator by denominator and round to 2 decimal places."
        ],
        "solution": "$$\\sum_{i=1}^3 x_i y_i = 1(2) + 2(5) + 3(7) = 2 + 10 + 21 = 33.$$\n$$\\sum_{i=1}^3 x_i^2 = 1^2 + 2^2 + 3^2 = 1 + 4 + 9 = 14.$$\n$$\\theta^* = \\frac{33}{14} \\approx 2.35714... \\approx 2.36.$$",
        "commonMistakes": ["Dividing by $N=3$ instead of $\\sum x_i^2$."],
        "relatedLesson": "week-3/week-3.html",
        "relatedLab": "visual_labs.html#lab-projection"
    },
    {
        "id": "w3-orig-q16",
        "version": 1,
        "title": "QR Decomposition vs Normal Equations Numerical Stability",
        "week": 3,
        "conceptIds": ["least-squares", "qr-decomposition", "numerical-stability"],
        "prerequisiteConceptIds": ["least-squares"],
        "type": "mcq",
        "difficulty": "medium",
        "estimatedMinutes": 4,
        "platform": "local",
        "provenance": "original",
        "verificationStatus": "reviewed",
        "source": {"citation": "Original MLF Numerical Linear Algebra Review", "url": None},
        "statement": "When solving the linear least squares problem $\\min_{\\theta} \\|X\\theta - y\\|_2^2$ where design matrix $X$ has condition number $\\kappa(X)$, why is QR factorization ($X = QR$) numerically superior to solving the Normal Equations $(X^T X)\\theta = X^T y$ via Cholesky decomposition?",
        "options": [
            {"id": "a", "text": "The condition number of $X^T X$ is $(\\kappa(X))^2$, squaring the sensitivity to floating-point rounding errors, whereas QR operates directly on $X$ with condition number $\\kappa(X)$."},
            {"id": "b", "text": "QR factorization requires only $O(n)$ operations while Normal Equations require $O(n^4)$ operations."},
            {"id": "c", "text": "The Normal Equations are mathematically invalid whenever $X$ has more rows than columns."},
            {"id": "d", "text": "QR factorization completely guarantees zero residual error $\|X\\theta - y\|_2 = 0$ for any dataset."}
        ],
        "answerSpec": {"correctOptionIds": ["a"], "numericValue": None, "tolerance": None},
        "hints": [
            "Recall that the condition number of a product $A^T A$ is $\\kappa(A^T A) = \\sigma_{\\max}^2 / \\sigma_{\\min}^2 = (\\kappa(A))^2$.",
            "If $\\kappa(X) = 10^4$, then $\\kappa(X^T X) = 10^8$, losing roughly 8 decimal digits of floating-point precision."
        ],
        "solution": "Forming the Gram matrix $X^T X$ squares the condition number: $\\kappa(X^T X) = (\\kappa(X))^2$. When $X$ is ill-conditioned, forming $X^T X$ results in catastrophic loss of precision. QR decomposition $X = QR$ bypasses computing $X^T X$, preserving the original conditioning $\\kappa(X)$. Thus option A is correct.",
        "commonMistakes": ["Believing QR is faster in operations (Normal equations is actually slightly faster in flops, but much less stable)."],
        "relatedLesson": "week-3/week-3.html",
        "relatedLab": "visual_labs.html#lab-projection"
    },
    {
        "id": "w3-orig-q17",
        "version": 1,
        "title": "Trace and Rank of an Orthogonal Projection Matrix",
        "week": 3,
        "conceptIds": ["projection-matrix", "subspaces"],
        "prerequisiteConceptIds": ["rank-nullity"],
        "type": "mcq",
        "difficulty": "easy",
        "estimatedMinutes": 3,
        "platform": "local",
        "provenance": "original",
        "verificationStatus": "reviewed",
        "source": {"citation": "Original MLF Subspace Algebra Problem", "url": None},
        "statement": "Let $X \\in \\mathbb{R}^{m \\times n}$ have rank $k$ (where $m > n > k$). Let $P$ be the orthogonal projection matrix onto the column space $\\text{Col}(X) \\subset \\mathbb{R}^m$. What is the trace $\\text{Tr}(P)$?",
        "options": [
            {"id": "a", "text": "$m$"},
            {"id": "b", "text": "$n$"},
            {"id": "c", "text": "$k$"},
            {"id": "d", "text": "$m - k$"}
        ],
        "answerSpec": {"correctOptionIds": ["c"], "numericValue": None, "tolerance": None},
        "hints": [
            "The trace of any matrix equals the sum of its eigenvalues.",
            "An orthogonal projection onto a subspace of dimension $d$ has $d$ eigenvalues equal to 1 and the rest equal to 0.",
            "The dimension of $\\text{Col}(X)$ is $\\text{rank}(X) = k$."
        ],
        "solution": "The eigenvalues of an orthogonal projection matrix onto a subspace of dimension $k$ consist of $k$ ones and $(m-k)$ zeros. Since the trace equals the sum of all eigenvalues, $\\text{Tr}(P) = k(1) + (m-k)(0) = k$. Therefore, $\\text{Tr}(P) = \\text{rank}(P) = k$ (Option C).",
        "commonMistakes": ["Assuming the trace equals $m$ (matrix dimension) or $n$ (column count)."],
        "relatedLesson": "week-3/week-3.html",
        "relatedLab": "visual_labs.html#lab-projection"
    },
    {
        "id": "w3-orig-q18",
        "version": 1,
        "title": "Fundamental Subspaces and Orthogonal Complements",
        "week": 3,
        "conceptIds": ["subspaces", "orthogonality", "rank-nullity"],
        "prerequisiteConceptIds": ["subspaces"],
        "type": "msq",
        "difficulty": "medium",
        "estimatedMinutes": 4,
        "platform": "local",
        "provenance": "original",
        "verificationStatus": "reviewed",
        "source": {"citation": "Original MLF Fundamental Theorem of Linear Algebra Problem", "url": None},
        "statement": "For any real matrix $A \\in \\mathbb{R}^{m \\times n}$, which of the following orthogonality and dimensional relationships are universally true?",
        "options": [
            {"id": "a", "text": "$(\\text{Col}(A))^\\perp = \\text{Null}(A^T)$ in $\\mathbb{R}^m$"},
            {"id": "b", "text": "$(\\text{Row}(A))^\\perp = \\text{Null}(A)$ in $\\mathbb{R}^n$"},
            {"id": "c", "text": "$\\dim(\\text{Col}(A)) + \\dim(\\text{Null}(A^T)) = m$"},
            {"id": "d", "text": "$\\text{Col}(A) \\cap \\text{Null}(A^T) = \\mathbb{R}^m$"}
        ],
        "answerSpec": {"correctOptionIds": ["a", "b", "c"], "numericValue": None, "tolerance": None},
        "hints": [
            "Recall the Fundamental Theorem of Linear Algebra (Strang).",
            "Row space and nullspace partition $\\mathbb{R}^n$ into orthogonal complements.",
            "Column space and left nullspace partition $\\mathbb{R}^m$ into orthogonal complements.",
            "Orthogonal complements intersect only at the zero vector: $S \\cap S^\\perp = \\{\\mathbf{0}\\}$."
        ],
        "solution": "By the Fundamental Theorem of Linear Algebra: $(\\text{Col}(A))^\\perp = \\text{Null}(A^T)$ and $(\\text{Row}(A))^\\perp = \\text{Null}(A)$. Because $\\text{Col}(A)$ and \\text{Null}(A^T) are orthogonal complements in $\\mathbb{R}^m$, their dimensions sum to $m$, and their intersection is $\\{\\mathbf{0}\\}$, NOT $\\mathbb{R}^m$. Thus A, B, and C are correct.",
        "commonMistakes": ["Thinking orthogonal complements can intersect at anything other than $\\{\\mathbf{0}\\}$."],
        "relatedLesson": "week-3/week-3.html",
        "relatedLab": "visual_labs.html#lab-projection"
    },
    {
        "id": "w3-orig-q19",
        "version": 1,
        "title": "Orthogonal Residual Norm Calculation",
        "week": 3,
        "conceptIds": ["least-squares", "projection-matrix"],
        "prerequisiteConceptIds": ["inner-product"],
        "type": "numeric",
        "difficulty": "easy",
        "estimatedMinutes": 3,
        "platform": "local",
        "provenance": "original",
        "verificationStatus": "reviewed",
        "source": {"citation": "Original MLF Residual Norm Problem", "url": None},
        "statement": "Let target vector $y = \\begin{bmatrix} 3 \\\\ 4 \\\\ 0 \\end{bmatrix}$ and direction vector $u = \\begin{bmatrix} 1 \\\\ 0 \\\\ 0 \\end{bmatrix}$ span 1D subspace $S = \\text{span}(u)$ in $\\mathbb{R}^3$. Calculate the minimum Euclidean distance from $y$ to $S$, given by $\\|y - P_S y\\|_2$.",
        "options": [],
        "answerSpec": {"correctOptionIds": [], "numericValue": 4.0, "tolerance": 0.05},
        "hints": [
            "Compute projection: $P_S y = \\frac{u^T y}{u^T u} u$.",
            "Calculate the residual vector $e = y - P_S y$.",
            "Find the Euclidean norm $\\|e\\|_2 = \\sqrt{e_1^2 + e_2^2 + e_3^2}$."
        ],
        "solution": "$$P_S y = \\frac{1(3) + 0(4) + 0(0)}{1^2 + 0^2 + 0^2} \\begin{bmatrix} 1 \\\\ 0 \\\\ 0 \\end{bmatrix} = 3 \\begin{bmatrix} 1 \\\\ 0 \\\\ 0 \\end{bmatrix} = \\begin{bmatrix} 3 \\\\ 0 \\\\ 0 \\end{bmatrix}.$$\n$$e = y - P_S y = \\begin{bmatrix} 3 \\\\ 4 \\\\ 0 \\end{bmatrix} - \\begin{bmatrix} 3 \\\\ 0 \\\\ 0 \\end{bmatrix} = \\begin{bmatrix} 0 \\\\ 4 \\\\ 0 \\end{bmatrix}.$$\n$$\\|e\\|_2 = \\sqrt{0^2 + 4^2 + 0^2} = 4.0.$$",
        "commonMistakes": ["Entering the length of $y$ ($5$) or the projection length ($3$) instead of the residual norm ($4$)."],
        "relatedLesson": "week-3/week-3.html",
        "relatedLab": "visual_labs.html#lab-projection"
    },
    {
        "id": "w3-orig-q20",
        "version": 1,
        "title": "Statistical Leverage Scores and the Hat Matrix",
        "week": 3,
        "conceptIds": ["least-squares", "projection-matrix"],
        "prerequisiteConceptIds": ["least-squares"],
        "type": "mcq",
        "difficulty": "medium",
        "estimatedMinutes": 4,
        "platform": "local",
        "provenance": "original",
        "verificationStatus": "reviewed",
        "source": {"citation": "Original MLF Regression Diagnostics Exercise", "url": None},
        "statement": "In linear regression $y = X\\theta + \\epsilon$, the projection (hat) matrix is $H = X(X^T X)^{-1} X^T$. The leverage score of observation $i$ is defined as $h_{ii} = H_{ii}$. If $X$ is an $n \\times p$ matrix with full column rank $p$, which property of leverage scores is mathematically guaranteed?",
        "options": [
            {"id": "a", "text": "$\\sum_{i=1}^n h_{ii} = p$, and $0 \\le h_{ii} \\le 1$ for all $i = 1, \\dots, n$."},
            {"id": "b", "text": "$\\sum_{i=1}^n h_{ii} = n$, and $h_{ii} > 1$ for outliers."},
            {"id": "c", "text": "$h_{ii} = 1/p$ uniformly for all data points."},
            {"id": "d", "text": "$\\det(H) = \\sum_{i=1}^n h_{ii}$."}
        ],
        "answerSpec": {"correctOptionIds": ["a"], "numericValue": None, "tolerance": None},
        "hints": [
            "The trace of the projection matrix equals the sum of diagonal entries: $\\text{Tr}(H) = \\sum h_{ii}$.",
            "Since $H$ projects onto a $p$-dimensional subspace, $\\text{Tr}(H) = p$.",
            "Because $H$ is symmetric and idempotent: $h_{ii} = \\sum_{j=1}^n H_{ij}^2 \\ge h_{ii}^2$, so $h_{ii} \\in [0, 1]$."
        ],
        "solution": "$H$ is an orthogonal projection matrix onto the column space of $X$ (dimension $p$). Therefore, $\\text{Tr}(H) = \\sum_{i=1}^n h_{ii} = p$. Furthermore, since $H^2 = H$ and $H = H^T$, $h_{ii} = \\sum_{j=1}^n H_{ij}^2 = h_{ii}^2 + \\sum_{j \\neq i} H_{ij}^2 \\ge h_{ii}^2$, which forces $0 \\le h_{ii} \\le 1$. Thus option A is correct.",
        "commonMistakes": ["Thinking leverage scores can exceed 1."],
        "relatedLesson": "week-3/week-3.html",
        "relatedLab": "visual_labs.html#lab-projection"
    },
    {
        "id": "w3-orig-q21",
        "version": 1,
        "title": "Rank-Nullity Theorem for Tall Matrix Transformation",
        "week": 3,
        "conceptIds": ["rank-nullity", "subspaces"],
        "prerequisiteConceptIds": ["subspaces"],
        "type": "numeric",
        "difficulty": "easy",
        "estimatedMinutes": 2,
        "platform": "local",
        "provenance": "original",
        "verificationStatus": "reviewed",
        "source": {"citation": "Original MLF Rank-Nullity Exercise", "url": None},
        "statement": "Let linear transformation $T: \\mathbb{R}^5 \\to \\mathbb{R}^8$ be represented by matrix $A \\in \\mathbb{R}^{8 \\times 5}$. If the column space $\\text{Col}(A)$ has dimension $3$ ($\text{rank}(A) = 3$), what is the dimension of the null space $\\dim(\\text{Null}(A))$?",
        "options": [],
        "answerSpec": {"correctOptionIds": [], "numericValue": 2, "tolerance": 0},
        "hints": [
            "State the Rank-Nullity Theorem: $\\text{rank}(A) + \\text{nullity}(A) = n$.",
            "Identify $n$: the dimension of the domain $\\mathbb{R}^5$ (number of columns), so $n = 5$."
        ],
        "solution": "By the Rank-Nullity Theorem, for $A \\in \\mathbb{R}^{m \\times n}$:\n$$\\text{rank}(A) + \\text{nullity}(A) = n$$\nHere, domain dimension is $n = 5$, and rank is $3$. Thus:\n$$\\text{nullity}(A) = 5 - 3 = 2.$$",
        "commonMistakes": ["Using $m=8$ (codomain dimension) instead of $n=5$ (domain dimension)."],
        "relatedLesson": "week-3/week-3.html",
        "relatedLab": "visual_labs.html#lab-projection"
    },
    {
        "id": "w3-orig-q22",
        "version": 1,
        "title": "Invertibility of Gram Matrix X^T X and Full Column Rank",
        "week": 3,
        "conceptIds": ["least-squares", "normal-equations"],
        "prerequisiteConceptIds": ["least-squares"],
        "type": "msq",
        "difficulty": "medium",
        "estimatedMinutes": 4,
        "platform": "local",
        "provenance": "original",
        "verificationStatus": "reviewed",
        "source": {"citation": "Original MLF Normal Equations Invertibility Problem", "url": None},
        "statement": "Let $X \\in \\mathbb{R}^{m \\times n}$ with $m \\ge n$. Under which of the following equivalent conditions is the Gram matrix $X^T X$ guaranteed to be strictly positive definite and invertible?",
        "options": [
            {"id": "a", "text": "The columns of $X$ are linearly independent."},
            {"id": "b", "text": "$\\text{rank}(X) = n$ (full column rank)."},
            {"id": "c", "text": "$\\text{Null}(X) = \\{\\mathbf{0}\\}$."},
            {"id": "d", "text": "$\\det(X^T X) > 0$."}
        ],
        "answerSpec": {"correctOptionIds": ["a", "b", "c", "d"], "numericValue": None, "tolerance": None},
        "hints": [
            "Recall that $v^T (X^T X) v = \\|Xv\\|_2^2$.",
            "If $Xv = 0 \\implies v = 0$, then $v^T (X^T X) v > 0$ for all $v \\neq 0$."
        ],
        "solution": "For any real matrix $X \\in \\mathbb{R}^{m \\times n}$ with $m \\ge n$:\n$v^T (X^T X) v = \\|Xv\\|^2 \\ge 0$.\nEquality holds ($Xv = 0$) if and only if $v \\in \\text{Null}(X)$. If columns are linearly independent, $\\text{Null}(X) = \\{\\mathbf{0}\\}$ and $\\text{rank}(X) = n$. This makes $X^T X$ positive definite, which is equivalent to all eigenvalues being positive, and $\\det(X^T X) > 0$. Therefore, all four options are mathematically equivalent.",
        "commonMistakes": ["Thinking $\\det(X^T X)$ could be negative for a Gram matrix."],
        "relatedLesson": "week-3/week-3.html",
        "relatedLab": "visual_labs.html#lab-projection"
    }
]

# ==============================================================================
# WEEK 6 QUESTIONS (18 new questions, bringing total to 20)
# ==============================================================================
WEEK6_NEW = [
    {
        "id": "w6-orig-q01",
        "version": 1,
        "title": "Singular Values Definition via Gram Matrix",
        "week": 6,
        "conceptIds": ["svd", "singular-values"],
        "prerequisiteConceptIds": ["eigenvalues"],
        "type": "mcq",
        "difficulty": "easy",
        "estimatedMinutes": 3,
        "platform": "local",
        "provenance": "original",
        "verificationStatus": "reviewed",
        "source": {"citation": "Original MLF SVD Fundamentals", "url": None},
        "statement": "For any real rectangular matrix $A \\in \\mathbb{R}^{m \\times n}$, how are the singular values $\\sigma_i(A)$ mathematically defined?",
        "options": [
            {"id": "a", "text": "As the non-negative square roots of the eigenvalues of $A^T A$, i.e., $\\sigma_i = \\sqrt{\\lambda_i(A^T A)}$."},
            {"id": "b", "text": "As the absolute values of the diagonal entries of $A$."},
            {"id": "c", "text": "As the eigenvalues of $A$ sorted in descending order."},
            {"id": "d", "text": "As the determinants of all $2 \\times 2$ submatrices of $A$."}
        ],
        "answerSpec": {"correctOptionIds": ["a"], "numericValue": None, "tolerance": None},
        "hints": [
            "Consider the symmetric positive semi-definite matrix $A^T A$.",
            "Its eigenvalues $\\lambda_i \\ge 0$. The singular values are their principal square roots."
        ],
        "solution": "By definition, the singular values of $A \\in \\mathbb{R}^{m \\times n}$ are the non-negative square roots of the eigenvalues of the symmetric matrix $A^T A$ (or equivalently non-zero eigenvalues of $A A^T$): $\\sigma_i = \\sqrt{\\lambda_i(A^T A)}$. Option A is correct.",
        "commonMistakes": ["Equating singular values with eigenvalues of $A$."],
        "relatedLesson": "week-6/week-6.html",
        "relatedLab": "visual_labs.html#lab-svd"
    },
    {
        "id": "w6-orig-q02",
        "version": 1,
        "title": "Singular Values of a Diagonal Matrix",
        "week": 6,
        "conceptIds": ["svd", "singular-values"],
        "prerequisiteConceptIds": ["singular-values"],
        "type": "numeric",
        "difficulty": "easy",
        "estimatedMinutes": 2,
        "platform": "local",
        "provenance": "original",
        "verificationStatus": "reviewed",
        "source": {"citation": "Original MLF SVD Diagonal Exercise", "url": None},
        "statement": "Let $D = \\begin{bmatrix} 5 & 0 \\\\ 0 & -7 \\end{bmatrix}$. What is the largest singular value $\\sigma_1(D)$?",
        "options": [],
        "answerSpec": {"correctOptionIds": [], "numericValue": 7.0, "tolerance": 0.01},
        "hints": [
            "Compute $D^T D$: $\\begin{bmatrix} 25 & 0 \\\\ 0 & 49 \\end{bmatrix}$.",
            "Take square roots of the eigenvalues in descending order: $\\sqrt{49} = 7$."
        ],
        "solution": "$$D^T D = \\begin{bmatrix} 5 & 0 \\\\ 0 & -7 \\end{bmatrix} \\begin{bmatrix} 5 & 0 \\\\ 0 & -7 \\end{bmatrix} = \\begin{bmatrix} 25 & 0 \\\\ 0 & 49 \\end{bmatrix}.$$\nEigenvalues are $49$ and $25$. The singular values are $\\sigma_1 = \\sqrt{49} = 7$ and $\\sigma_2 = \\sqrt{25} = 5$.",
        "commonMistakes": ["Singular values are always non-negative; $-7$ cannot be a singular value."],
        "relatedLesson": "week-6/week-6.html",
        "relatedLab": "visual_labs.html#lab-svd"
    },
    {
        "id": "w6-orig-q03",
        "version": 1,
        "title": "Eckart-Young-Mirsky Low-Rank Approximation Theorem",
        "week": 6,
        "conceptIds": ["svd", "low-rank-approximation"],
        "prerequisiteConceptIds": ["svd"],
        "type": "mcq",
        "difficulty": "medium",
        "estimatedMinutes": 4,
        "platform": "local",
        "provenance": "original",
        "verificationStatus": "reviewed",
        "source": {"citation": "Original MLF Matrix Approximation Theory", "url": None},
        "statement": "According to the Eckart-Young-Mirsky theorem, what is the optimal rank-$k$ approximation $A_k$ of a matrix $A = \\sum_{i=1}^r \\sigma_i u_i v_i^T$ under both the Frobenius norm and the spectral norm?",
        "options": [
            {"id": "a", "text": "The truncated SVD expansion: $A_k = \\sum_{i=1}^k \\sigma_i u_i v_i^T$ retaining the top $k$ singular components."},
            {"id": "b", "text": "The orthogonal projection of $A$ onto its first $k$ columns."},
            {"id": "c", "text": "The upper-triangular factor $R_k$ from the QR decomposition."},
            {"id": "d", "text": "The diagonal matrix consisting of the first $k$ row sums of $A$."}
        ],
        "answerSpec": {"correctOptionIds": ["a"], "numericValue": None, "tolerance": None},
        "hints": [
            "The truncated singular value decomposition minimizes $\\|A - B\\|_F$ over all matrices $B$ with $\\text{rank}(B) \\le k$.",
            "The error equals the remaining singular values: $\\|A - A_k\\|_2 = \\sigma_{k+1}$."
        ],
        "solution": "The Eckart-Young-Mirsky Theorem establishes that for any $k < \\text{rank}(A)$, the optimal rank-$k$ approximation under both the spectral norm $\\|\\cdot\\|_2$ and the Frobenius norm $\\|\\cdot\\|_F$ is given by the truncated SVD: $A_k = \\sum_{i=1}^k \\sigma_i u_i v_i^T$. Option A is correct.",
        "commonMistakes": ["Thinking column truncation without singular vector weighting is optimal."],
        "relatedLesson": "week-6/week-6.html",
        "relatedLab": "visual_labs.html#lab-svd"
    },
    {
        "id": "w6-orig-q04",
        "version": 1,
        "title": "Properties of Left and Right Singular Vectors",
        "week": 6,
        "conceptIds": ["svd", "singular-vectors"],
        "prerequisiteConceptIds": ["orthogonality"],
        "type": "msq",
        "difficulty": "medium",
        "estimatedMinutes": 4,
        "platform": "local",
        "provenance": "original",
        "verificationStatus": "reviewed",
        "source": {"citation": "Original MLF SVD Geometry Problem", "url": None},
        "statement": "Let $A = U \\Sigma V^T$ be the singular value decomposition of $A \\in \\mathbb{R}^{m \\times n}$. Which of the following statements about $U$ and $V$ are true?",
        "options": [
            {"id": "a", "text": "The columns of $U$ are orthonormal eigenvectors of $A A^T$."},
            {"id": "b", "text": "The columns of $V$ are orthonormal eigenvectors of $A^T A$."},
            {"id": "c", "text": "$U^T U = I_m$ and $V^T V = I_n$ (orthogonal matrices)."},
            {"id": "d", "text": "$U$ and $V$ must always be symmetric matrices."}
        ],
        "answerSpec": {"correctOptionIds": ["a", "b", "c"], "numericValue": None, "tolerance": None},
        "hints": [
            "Multiply $A A^T = (U \\Sigma V^T)(V \\Sigma^T U^T) = U \\Sigma \\Sigma^T U^T$.",
            "Multiply $A^T A = (V \\Sigma^T U^T)(U \\Sigma V^T) = V \\Sigma^T \\Sigma V^T$.",
            "Singular vector matrices are orthogonal, not necessarily symmetric."
        ],
        "solution": "$A A^T = U \\Sigma \\Sigma^T U^T$, so the columns of $U$ (left singular vectors) are orthonormal eigenvectors of $A A^T$. Similarly, $A^T A = V \\Sigma^T \\Sigma V^T$, so columns of $V$ (right singular vectors) are orthonormal eigenvectors of $A^T A$. Both $U$ and $V$ are orthogonal matrices ($U^T U = I, V^T V = I$). They are not generally symmetric. Options A, B, C are correct.",
        "commonMistakes": ["Assuming orthogonal matrices must also be symmetric."],
        "relatedLesson": "week-6/week-6.html",
        "relatedLab": "visual_labs.html#lab-svd"
    },
    {
        "id": "w6-orig-q05",
        "version": 1,
        "title": "Hand Computation of Singular Values for 2x2 Matrix",
        "week": 6,
        "conceptIds": ["svd", "singular-values"],
        "prerequisiteConceptIds": ["eigenvalues"],
        "type": "numeric",
        "difficulty": "medium",
        "estimatedMinutes": 4,
        "platform": "local",
        "provenance": "original",
        "verificationStatus": "reviewed",
        "source": {"citation": "Original MLF Hand SVD Walkthrough", "url": None},
        "statement": "Given matrix $A = \\begin{bmatrix} 0 & 3 \\\\ 4 & 0 \\end{bmatrix}$, calculate the product of its singular values $\\sigma_1 \\cdot \\sigma_2$.",
        "options": [],
        "answerSpec": {"correctOptionIds": [], "numericValue": 12.0, "tolerance": 0.05},
        "hints": [
            "For a square matrix, the product of singular values equals the absolute value of the determinant: $\\prod \\sigma_i = |\\det(A)|$.",
            "Alternatively, compute $A^T A = \\begin{bmatrix} 16 & 0 \\\\ 0 & 9 \\end{bmatrix}$, giving singular values $\\sqrt{16}=4$ and $\\sqrt{9}=3$."
        ],
        "solution": "$$A^T A = \\begin{bmatrix} 0 & 4 \\\\ 3 & 0 \\end{bmatrix} \\begin{bmatrix} 0 & 3 \\\\ 4 & 0 \\end{bmatrix} = \\begin{bmatrix} 16 & 0 \\\\ 0 & 9 \\end{bmatrix}.$$\nThe eigenvalues of $A^T A$ are $\\lambda_1 = 16, \\lambda_2 = 9$. Thus $\\sigma_1 = 4, \\sigma_2 = 3$. Their product is $4 \\times 3 = 12$ (which equals $|\\det(A)| = |-12| = 12$).",
        "commonMistakes": ["Confusing determinant sign with singular value product."],
        "relatedLesson": "week-6/week-6.html",
        "relatedLab": "visual_labs.html#lab-svd"
    },
    {
        "id": "w6-orig-q06",
        "version": 1,
        "title": "Moore-Penrose Pseudoinverse via SVD",
        "week": 6,
        "conceptIds": ["svd", "pseudoinverse"],
        "prerequisiteConceptIds": ["svd"],
        "type": "mcq",
        "difficulty": "medium",
        "estimatedMinutes": 3,
        "platform": "local",
        "provenance": "original",
        "verificationStatus": "reviewed",
        "source": {"citation": "Original MLF Pseudoinverse Theory", "url": None},
        "statement": "If $A = U \\Sigma V^T$ with singular values $\\sigma_1 \\ge \\dots \\ge \\sigma_r > 0$, how is the Moore-Penrose pseudoinverse $A^+$ expressed in terms of the SVD components?",
        "options": [
            {"id": "a", "text": "$A^+ = V \\Sigma^+ U^T$, where $\\Sigma^+$ replaces each non-zero $\\sigma_i$ with $1/\\sigma_i$ and transposes the dimensions."},
            {"id": "b", "text": "$A^+ = U \\Sigma^+ V^T$ with no transposition of singular vector matrices."},
            {"id": "c", "text": "$A^+ = (U \\Sigma V^T)^{-1}$ which only exists if $m = n$."},
            {"id": "d", "text": "$A^+ = V^T \\Sigma^+ U$."}
        ],
        "answerSpec": {"correctOptionIds": ["a"], "numericValue": None, "tolerance": None},
        "hints": [
            "Invert the SVD factor by factor: $(U \\Sigma V^T)^+ = (V^T)^+ \\Sigma^+ U^+ = V \\Sigma^+ U^T$.",
            "Remember that $U$ and $V$ are orthogonal, so $U^+ = U^T$ and $(V^T)^+ = V$."
        ],
        "solution": "Taking the pseudoinverse of $A = U \\Sigma V^T$ yields $A^+ = (V^T)^+ \\Sigma^+ U^+ = V \\Sigma^+ U^T$, where $\\Sigma^+$ has diagonal entries $1/\\sigma_i$ for $\\sigma_i > 0$. Option A is correct.",
        "commonMistakes": ["Leaving $U$ on the left and $V$ on the right."],
        "relatedLesson": "week-6/week-6.html",
        "relatedLab": "visual_labs.html#lab-svd"
    },
    {
        "id": "w6-orig-q07",
        "version": 1,
        "title": "Frobenius Norm from Singular Values",
        "week": 6,
        "conceptIds": ["svd", "matrix-norms"],
        "prerequisiteConceptIds": ["singular-values"],
        "type": "numeric",
        "difficulty": "easy",
        "estimatedMinutes": 2,
        "platform": "local",
        "provenance": "original",
        "verificationStatus": "reviewed",
        "source": {"citation": "Original MLF Matrix Norms", "url": None},
        "statement": "A matrix $A$ has non-zero singular values $\\sigma_1 = 4$, $\\sigma_2 = 3$, and $\\sigma_3 = 0$. Calculate the Frobenius norm $\\|A\\|_F$.",
        "options": [],
        "answerSpec": {"correctOptionIds": [], "numericValue": 5.0, "tolerance": 0.05},
        "hints": [
            "The Frobenius norm is unitary invariant: $\\|A\\|_F = \\sqrt{\\sum_{i=1}^r \\sigma_i^2}$.",
            "Calculate $\\sqrt{4^2 + 3^2} = \\sqrt{16 + 9} = \\sqrt{25}$."
        ],
        "solution": "$$\\|A\\|_F = \\sqrt{\\sum_{i=1}^r \\sigma_i^2} = \\sqrt{4^2 + 3^2 + 0^2} = \\sqrt{16 + 9} = \\sqrt{25} = 5.0.$$",
        "commonMistakes": ["Using the spectral norm ($\\|A\\|_2 = \\sigma_1 = 4$) instead of Frobenius norm ($5$)."],
        "relatedLesson": "week-6/week-6.html",
        "relatedLab": "visual_labs.html#lab-svd"
    },
    {
        "id": "w6-orig-q08",
        "version": 1,
        "title": "Positive Definite Matrix Equivalence Conditions",
        "week": 6,
        "conceptIds": ["positive-definite", "eigenvalues"],
        "prerequisiteConceptIds": ["eigenvalues"],
        "type": "msq",
        "difficulty": "medium",
        "estimatedMinutes": 4,
        "platform": "local",
        "provenance": "original",
        "verificationStatus": "reviewed",
        "source": {"citation": "Original MLF Positive Definiteness Review", "url": None},
        "statement": "For a real symmetric matrix $A \\in \\mathbb{R}^{n \\times n}$, which of the following conditions are equivalent to $A$ being strictly positive definite ($A \\succ 0$)?",
        "options": [
            {"id": "a", "text": "$x^T A x > 0$ for all non-zero vectors $x \\in \\mathbb{R}^n \\setminus \\{\\mathbf{0}\\}$."},
            {"id": "b", "text": "All eigenvalues of $A$ are strictly positive: $\\lambda_i(A) > 0$ for all $i$."},
            {"id": "c", "text": "All leading principal minors of $A$ are strictly positive (Sylvester's criterion)."},
            {"id": "d", "text": "There exists a unique lower triangular matrix $L$ with positive diagonal entries such that $A = L L^T$ (Cholesky decomposition)."}
        ],
        "answerSpec": {"correctOptionIds": ["a", "b", "c", "d"], "numericValue": None, "tolerance": None},
        "hints": [
            "Review Sylvester's Criterion and the Cholesky factorization theorem.",
            "All four conditions are foundational definitions and characterizations of positive definiteness."
        ],
        "solution": "All four conditions are standard, universally equivalent characterizations of real symmetric positive definite matrices: quadratic form positivity, strictly positive spectrum, positive leading principal minors (Sylvester), and existence of Cholesky factorization. Options A, B, C, and D are all correct.",
        "commonMistakes": ["Excluding Cholesky decomposition or Sylvester's criterion."],
        "relatedLesson": "week-6/week-6.html",
        "relatedLab": "visual_labs.html#lab-svd"
    },
    {
        "id": "w6-orig-q09",
        "version": 1,
        "title": "Condition Number and Numerical Sensitivity",
        "week": 6,
        "conceptIds": ["condition-number", "svd"],
        "prerequisiteConceptIds": ["singular-values"],
        "type": "mcq",
        "difficulty": "medium",
        "estimatedMinutes": 3,
        "platform": "local",
        "provenance": "original",
        "verificationStatus": "reviewed",
        "source": {"citation": "Original MLF Numerical Stability Analysis", "url": None},
        "statement": "The condition number of a non-singular square matrix $A$ in the $L_2$ norm is given by $\\kappa_2(A) = \\frac{\\sigma_{\\max}}{\\sigma_{\\min}}$. What does $\\kappa_2(A) = 1$ geometrically signify?",
        "options": [
            {"id": "a", "text": "$A$ scales all directions equally (an orthogonal matrix scaled by a scalar), mapping the unit sphere to a perfect sphere."},
            {"id": "b", "text": "$A$ is singular and has no inverse."},
            {"id": "c", "text": "$A$ is severely ill-conditioned and unstable."},
            {"id": "d", "text": "The nullspace of $A$ has dimension 1."}
        ],
        "answerSpec": {"correctOptionIds": ["a"], "numericValue": None, "tolerance": None},
        "hints": [
            "If $\\sigma_{\\max} = \\sigma_{\\min}$, then all singular values are equal: $\\sigma_i = c$.",
            "The image of the unit sphere under $A$ has semi-axes of lengths $\\sigma_i = c$."
        ],
        "solution": "When $\\kappa_2(A) = 1$, $\\sigma_1 = \\sigma_n = c > 0$. Every singular value is equal, meaning $A = c Q$ for some orthogonal matrix $Q$. Geometrically, $A$ preserves angles and scales all vectors by $c$, mapping the unit sphere to a sphere of radius $c$. This represents optimal numerical conditioning. Option A is correct.",
        "commonMistakes": ["Thinking condition number 1 means singular."],
        "relatedLesson": "week-6/week-6.html",
        "relatedLab": "visual_labs.html#lab-svd"
    },
    {
        "id": "w6-orig-q10",
        "version": 1,
        "title": "Condition Number Calculation for Diagonal Matrix",
        "week": 6,
        "conceptIds": ["condition-number", "singular-values"],
        "prerequisiteConceptIds": ["condition-number"],
        "type": "numeric",
        "difficulty": "easy",
        "estimatedMinutes": 2,
        "platform": "local",
        "provenance": "original",
        "verificationStatus": "reviewed",
        "source": {"citation": "Original MLF Numerical Stability Exercise", "url": None},
        "statement": "Compute the $L_2$ condition number $\\kappa_2(A) = \\sigma_{\\max} / \\sigma_{\\min}$ for matrix $A = \\begin{bmatrix} 20 & 0 \\\\ 0 & 4 \\end{bmatrix}$.",
        "options": [],
        "answerSpec": {"correctOptionIds": [], "numericValue": 5.0, "tolerance": 0.05},
        "hints": [
            "Identify the singular values: $\\sigma_{\\max} = 20, \\sigma_{\\min} = 4$.",
            "Divide $\\sigma_{\\max}$ by $\\sigma_{\\min}$."
        ],
        "solution": "$$\\kappa_2(A) = \\frac{\\sigma_{\\max}}{\\sigma_{\\min}} = \\frac{20}{4} = 5.0.$$",
        "commonMistakes": ["Inverting the ratio ($4/20 = 0.2$). Condition number is always $\\ge 1$."],
        "relatedLesson": "week-6/week-6.html",
        "relatedLab": "visual_labs.html#lab-svd"
    },
    {
        "id": "w6-orig-q11",
        "version": 1,
        "title": "Three-Stage Geometric Action of SVD",
        "week": 6,
        "conceptIds": ["svd", "geometry-of-svd"],
        "prerequisiteConceptIds": ["svd"],
        "type": "msq",
        "difficulty": "medium",
        "estimatedMinutes": 3,
        "platform": "local",
        "provenance": "original",
        "verificationStatus": "reviewed",
        "source": {"citation": "Original MLF Geometric Decomposition Exercise", "url": None},
        "statement": "When a vector $x$ is transformed by $A = U \\Sigma V^T$, which geometric interpretations accurately describe the three sequential stages of multiplication $x \\mapsto V^T x \\mapsto \\Sigma(V^T x) \\mapsto U(\\Sigma V^T x)$?",
        "options": [
            {"id": "a", "text": "First, $V^T$ performs a rotation/reflection in the input domain (aligning right singular vectors with standard axes)."},
            {"id": "b", "text": "Second, $\\Sigma$ scales each coordinate axis by the corresponding singular value $\\sigma_i$ (stretching a sphere into a hyper-ellipsoid)."},
            {"id": "c", "text": "Third, $U$ applies a final rotation/reflection in the output space (orienting the hyper-ellipsoid semi-axes along the left singular vectors)."},
            {"id": "d", "text": "The transformation causes non-linear warping and curvature of flat lines."}
        ],
        "answerSpec": {"correctOptionIds": ["a", "b", "c"], "numericValue": None, "tolerance": None},
        "hints": [
            "Orthogonal matrices $V^T$ and $U$ are rigid isometries (rotations/reflections).",
            "Diagonal matrix $\\Sigma$ represents pure axis-aligned coordinate stretching.",
            "Matrix multiplication is strictly linear; it cannot bend lines."
        ],
        "solution": "The geometric decomposition of $A = U \\Sigma V^T$ is famously understood in 3 stages: (1) $V^T$ rotates the input space, (2) $\\Sigma$ stretches the coordinates along cardinal axes by singular values $\\sigma_i$, turning the unit sphere into an ellipsoid, and (3) $U$ rotates the ellipsoid to align with output singular axes. Stage D is false because matrix multiplication is linear. Options A, B, C are correct.",
        "commonMistakes": ["Thinking SVD introduces non-linear curvature."],
        "relatedLesson": "week-6/week-6.html",
        "relatedLab": "visual_labs.html#lab-svd"
    },
    {
        "id": "w6-orig-q12",
        "version": 1,
        "title": "Truncated SVD Frobenius Error Calculation",
        "week": 6,
        "conceptIds": ["svd", "low-rank-approximation"],
        "prerequisiteConceptIds": ["low-rank-approximation"],
        "type": "numeric",
        "difficulty": "medium",
        "estimatedMinutes": 3,
        "platform": "local",
        "provenance": "original",
        "verificationStatus": "reviewed",
        "source": {"citation": "Original MLF Truncation Error Problem", "url": None},
        "statement": "A matrix $A$ has singular values $\\sigma = [10, 6, 8]$ (unsorted). We form the optimal rank-1 approximation $A_1 = \\sigma_{\\max} u_1 v_1^T$. Compute the Frobenius norm of the approximation error $\\|A - A_1\\|_F = \\sqrt{\\sum_{i=2}^3 \\sigma_i^2}$.",
        "options": [],
        "answerSpec": {"correctOptionIds": [], "numericValue": 10.0, "tolerance": 0.05},
        "hints": [
            "Sort singular values in descending order: $\\sigma_1 = 10, \\sigma_2 = 8, \\sigma_3 = 6$.",
            "The rank-1 approximation error in Frobenius norm is $\\sqrt{\\sigma_2^2 + \\sigma_3^2}$.",
            "Compute $\\sqrt{8^2 + 6^2} = \\sqrt{64 + 36} = \\sqrt{100} = 10$."
        ],
        "solution": "Sorted singular values are $\\sigma_1 = 10, \\sigma_2 = 8, \\sigma_3 = 6$.\nThe Frobenius approximation error for rank $k=1$ is:\n$$\\|A - A_1\\|_F = \\sqrt{\\sigma_2^2 + \\sigma_3^2} = \\sqrt{8^2 + 6^2} = \\sqrt{64 + 36} = \\sqrt{100} = 10.0.$$",
        "commonMistakes": ["Using unsorted order and taking $\\sigma_1^2 + \\sigma_2^2$."],
        "relatedLesson": "week-6/week-6.html",
        "relatedLab": "visual_labs.html#lab-svd"
    },
    {
        "id": "w6-orig-q13",
        "version": 1,
        "title": "Spectral Norm via SVD",
        "week": 6,
        "conceptIds": ["matrix-norms", "svd"],
        "prerequisiteConceptIds": ["singular-values"],
        "type": "mcq",
        "difficulty": "easy",
        "estimatedMinutes": 2,
        "platform": "local",
        "provenance": "original",
        "verificationStatus": "reviewed",
        "source": {"citation": "Original MLF Matrix Norms", "url": None},
        "statement": "For any matrix $A$, what is the relationship between the matrix spectral norm (induced $L_2$ operator norm $\\|A\\|_2 = \\max_{\\|x\\|=1} \\|Ax\\|$) and its singular values?",
        "options": [
            {"id": "a", "text": "$\\|A\\|_2 = \\sigma_{\\max}(A) = \\sigma_1$."},
            {"id": "b", "text": "$\\|A\\|_2 = \\sum_{i=1}^r \\sigma_i$."},
            {"id": "c", "text": "$\\|A\\|_2 = \\sqrt{\\sigma_1 \\cdot \\sigma_n}$."},
            {"id": "d", "text": "$\\|A\\|_2 = \\sigma_{\\min}(A)$."}
        ],
        "answerSpec": {"correctOptionIds": ["a"], "numericValue": None, "tolerance": None},
        "hints": [
            "The maximum stretching factor of the unit sphere under transformation $A$ corresponds to the length of the major semi-axis, which is $\\sigma_1$."
        ],
        "solution": "By definition, the induced 2-norm $\\|A\\|_2 = \\max_{\\|x\\|=1} \\|Ax\\|_2$ represents the maximum magnification of any vector, which exactly equals the largest singular value $\\sigma_1(A)$. Option A is correct.",
        "commonMistakes": ["Confusing spectral norm with nuclear norm (sum of singular values)."],
        "relatedLesson": "week-6/week-6.html",
        "relatedLab": "visual_labs.html#lab-svd"
    },
    {
        "id": "w6-orig-q14",
        "version": 1,
        "title": "Matrix Rank from Non-zero Singular Values",
        "week": 6,
        "conceptIds": ["svd", "matrix-rank"],
        "prerequisiteConceptIds": ["singular-values"],
        "type": "numeric",
        "difficulty": "easy",
        "estimatedMinutes": 2,
        "platform": "local",
        "provenance": "original",
        "verificationStatus": "reviewed",
        "source": {"citation": "Original MLF Rank Theorem", "url": None},
        "statement": "If a $10 \\times 6$ matrix $A$ has exactly four singular values strictly greater than zero ($\\{12.5, 7.2, 3.1, 0.4\\}$) and all other singular values equal zero, what is the mathematical rank of $A$?",
        "options": [],
        "answerSpec": {"correctOptionIds": [], "numericValue": 4, "tolerance": 0},
        "hints": [
            "The rank of any matrix equals the number of non-zero singular values."
        ],
        "solution": "The rank of a matrix equals the dimension of its image, which exactly equals the count of its strictly positive singular values: $\\text{rank}(A) = \\#\\{\\sigma_i > 0\\} = 4$.",
        "commonMistakes": ["Guessing min dimension (6) instead of non-zero count (4)."],
        "relatedLesson": "week-6/week-6.html",
        "relatedLab": "visual_labs.html#lab-svd"
    },
    {
        "id": "w6-orig-q15",
        "version": 1,
        "title": "Fundamental Differences: SVD vs Eigenvalue Decomposition",
        "week": 6,
        "conceptIds": ["svd", "eigenvalues"],
        "prerequisiteConceptIds": ["eigenvalues"],
        "type": "msq",
        "difficulty": "medium",
        "estimatedMinutes": 4,
        "platform": "local",
        "provenance": "original",
        "verificationStatus": "reviewed",
        "source": {"citation": "Original MLF Spectral Comparison", "url": None},
        "statement": "Which of the following highlight fundamental differences between Singular Value Decomposition (SVD) and Eigenvalue Decomposition (EVD)?",
        "options": [
            {"id": "a", "text": "SVD exists for **any** rectangular $m \\times n$ matrix, while EVD only exists for square $n \\times n$ diagonalizable matrices."},
            {"id": "b", "text": "Singular values are always real and non-negative, whereas eigenvalues can be complex or negative."},
            {"id": "c", "text": "The left and right singular vectors in SVD form orthonormal bases in two different spaces ($\mathbb{R}^m$ and $\mathbb{R}^n$), whereas eigenvectors in EVD belong to the same space."},
            {"id": "d", "text": "SVD can only be computed if the matrix is invertible."}
        ],
        "answerSpec": {"correctOptionIds": ["a", "b", "c"], "numericValue": None, "tolerance": None},
        "hints": [
            "Does SVD require squareness? No.",
            "Can singular values be negative? Never.",
            "Can SVD be computed for singular matrices? Absolutely."
        ],
        "solution": "SVD is universally defined for all $m \\times n$ matrices regardless of rank or shape. Its singular values are always real and $\\ge 0$. EVD requires square matrices and can have complex or negative eigenvalues. SVD spans domain and codomain through orthonormal bases $V$ and $U$. Option D is false. Options A, B, C are correct.",
        "commonMistakes": ["Thinking SVD requires invertibility."],
        "relatedLesson": "week-6/week-6.html",
        "relatedLab": "visual_labs.html#lab-svd"
    },
    {
        "id": "w6-orig-q16",
        "version": 1,
        "title": "Singular Values of Pseudoinverse",
        "week": 6,
        "conceptIds": ["pseudoinverse", "svd"],
        "prerequisiteConceptIds": ["pseudoinverse"],
        "type": "mcq",
        "difficulty": "medium",
        "estimatedMinutes": 3,
        "platform": "local",
        "provenance": "original",
        "verificationStatus": "reviewed",
        "source": {"citation": "Original MLF Pseudoinverse SVD Relations", "url": None},
        "statement": "If a matrix $A$ of rank $r$ has non-zero singular values $\\sigma_1 \\ge \\sigma_2 \\ge \\dots \\ge \\sigma_r > 0$, what are the non-zero singular values of its Moore-Penrose pseudoinverse $A^+$?",
        "options": [
            {"id": "a", "text": "$\\frac{1}{\\sigma_r} \\ge \\frac{1}{\\sigma_{r-1}} \\ge \\dots \\ge \\frac{1}{\\sigma_1} > 0$"},
            {"id": "b", "text": "$-\\sigma_1, -\\sigma_2, \\dots, -\\sigma_r$"},
            {"id": "c", "text": "$\\sigma_1^2, \\sigma_2^2, \\dots, \\sigma_r^2$"},
            {"id": "d", "text": "$\\sqrt{\\sigma_1}, \\sqrt{\\sigma_2}, \\dots, \\sqrt{\\sigma_r}$"}
        ],
        "answerSpec": {"correctOptionIds": ["a"], "numericValue": None, "tolerance": None},
        "hints": [
            "In $A^+ = V \\Sigma^+ U^T$, $\\Sigma^+$ has entries $1/\\sigma_i$.",
            "Sorted in descending order, the largest singular value of $A^+$ is $1/\\sigma_r$."
        ],
        "solution": "Since $A^+ = V \\Sigma^+ U^T$ and $\\Sigma^+$ contains the reciprocal non-zero entries $1/\\sigma_i$, sorting them in descending order yields $\\sigma_1(A^+) = 1/\\sigma_r(A) \\ge \\dots \\ge \\sigma_r(A^+) = 1/\\sigma_1(A) > 0$. Option A is correct.",
        "commonMistakes": ["Leaving order unreversed ($1/\\sigma_1$ is the smallest non-zero singular value, not the largest)."],
        "relatedLesson": "week-6/week-6.html",
        "relatedLab": "visual_labs.html#lab-svd"
    },
    {
        "id": "w6-orig-q17",
        "version": 1,
        "title": "Largest Singular Value of Rank-1 All-Ones Matrix",
        "week": 6,
        "conceptIds": ["svd", "singular-values"],
        "prerequisiteConceptIds": ["singular-values"],
        "type": "numeric",
        "difficulty": "medium",
        "estimatedMinutes": 3,
        "platform": "local",
        "provenance": "original",
        "verificationStatus": "reviewed",
        "source": {"citation": "Original MLF Hand SVD Exercise", "url": None},
        "statement": "Compute the largest singular value $\\sigma_1$ of the $2 \\times 2$ matrix $J = \\begin{bmatrix} 1 & 1 \\\\ 1 & 1 \\end{bmatrix}$.",
        "options": [],
        "answerSpec": {"correctOptionIds": [], "numericValue": 2.0, "tolerance": 0.05},
        "hints": [
            "Compute $J^T J = \\begin{bmatrix} 1 & 1 \\\\ 1 & 1 \\end{bmatrix} \\begin{bmatrix} 1 & 1 \\\\ 1 & 1 \\end{bmatrix} = \\begin{bmatrix} 2 & 2 \\\\ 2 & 2 \\end{bmatrix}$.",
            "Eigenvalues of $J^T J$: trace is $4$, determinant is $0$. So $\\lambda_1 = 4, \\lambda_2 = 0$.",
            "Singular value $\\sigma_1 = \\sqrt{4} = 2$."
        ],
        "solution": "$$J^T J = \\begin{bmatrix} 2 & 2 \\\\ 2 & 2 \\end{bmatrix}.$$\nThe eigenvalues of $J^T J$ are $\\lambda_1 = 4, \\lambda_2 = 0$. Hence the singular values are $\\sigma_1 = \\sqrt{4} = 2.0$ and $\\sigma_2 = 0$.",
        "commonMistakes": ["Confusing $\\lambda_1(J^T J) = 4$ with singular value $\\sigma_1 = \\sqrt{4} = 2$."],
        "relatedLesson": "week-6/week-6.html",
        "relatedLab": "visual_labs.html#lab-svd"
    },
    {
        "id": "w6-orig-q18",
        "version": 1,
        "title": "SVD and the Four Fundamental Subspaces",
        "week": 6,
        "conceptIds": ["svd", "subspaces"],
        "prerequisiteConceptIds": ["subspaces"],
        "type": "msq",
        "difficulty": "hard",
        "estimatedMinutes": 5,
        "platform": "local",
        "provenance": "original",
        "verificationStatus": "reviewed",
        "source": {"citation": "Original MLF Four Subspaces SVD Synthesis", "url": None},
        "statement": "Let $A = U \\Sigma V^T \\in \\mathbb{R}^{m \\times n}$ have rank $r$. Which orthonormal bases for the four fundamental subspaces of $A$ are directly provided by the columns of $U = [u_1, \\dots, u_m]$ and $V = [v_1, \\dots, v_n]$?",
        "options": [
            {"id": "a", "text": "$\\{u_1, \\dots, u_r\\}$ forms an orthonormal basis for the Column Space $\\text{Col}(A)$."},
            {"id": "b", "text": "$\\{u_{r+1}, \\dots, u_m\\}$ forms an orthonormal basis for the Left Nullspace $\\text{Null}(A^T)$."},
            {"id": "c", "text": "$\\{v_1, \\dots, v_r\\}$ forms an orthonormal basis for the Row Space $\\text{Row}(A)$."},
            {"id": "d", "text": "$\\{v_{r+1}, \\dots, v_n\\}$ forms an orthonormal basis for the Nullspace $\\text{Null}(A)$."}
        ],
        "answerSpec": {"correctOptionIds": ["a", "b", "c", "d"], "numericValue": None, "tolerance": None},
        "hints": [
            "Consider the action of $A$ on $v_i$: $A v_i = \\sigma_i u_i$ for $i \\le r$, and $A v_i = 0$ for $i > r$.",
            "This directly establishes that $v_{r+1} \\dots v_n$ are in the nullspace.",
            "All four fundamental subspaces are completely diagonalized by SVD."
        ],
        "solution": "One of the crowning achievements of SVD is providing explicit orthonormal bases for all four fundamental subspaces:\n1. $\\text{Col}(A) = \\text{span}(u_1, \\dots, u_r)$\n2. $\\text{Null}(A^T) = \\text{span}(u_{r+1}, \\dots, u_m)$\n3. $\\text{Row}(A) = \\text{span}(v_1, \\dots, v_r)$\n4. $\\text{Null}(A) = \\text{span}(v_{r+1}, \\dots, v_n)$\nAll four statements are universally true.",
        "commonMistakes": ["Swapping row space with column space singular vectors."],
        "relatedLesson": "week-6/week-6.html",
        "relatedLab": "visual_labs.html#lab-svd"
    }
]

# ==============================================================================
# WEEK 7 QUESTIONS (18 new questions, bringing total to 20)
# ==============================================================================
WEEK7_NEW = [
    {
        "id": "w7-orig-q01",
        "version": 1,
        "title": "Mean Centering as a PCA Prerequisite",
        "week": 7,
        "conceptIds": ["pca", "covariance-matrix"],
        "prerequisiteConceptIds": ["pca"],
        "type": "mcq",
        "difficulty": "easy",
        "estimatedMinutes": 3,
        "platform": "local",
        "provenance": "original",
        "verificationStatus": "reviewed",
        "source": {"citation": "Original MLF PCA Principles", "url": None},
        "statement": "Why must the data matrix $X$ always be mean-centered (subtracting column means $\\bar{x}_j$) before computing Principal Component Analysis?",
        "options": [
            {"id": "a", "text": "Because without centering, the first principal component points toward the mean of the data cloud rather than along the axis of maximum variance."},
            {"id": "b", "text": "Because the covariance matrix cannot be inverted unless data is centered."},
            {"id": "c", "text": "Because centering forces all eigenvalues to be non-zero."},
            {"id": "d", "text": "Because non-centered data prevents computing the matrix determinant."}
        ],
        "answerSpec": {"correctOptionIds": ["a"], "numericValue": None, "tolerance": None},
        "hints": [
            "Consider a tight cluster centered at $(100, 100)$.",
            "Variance is measured about the mean: $\\text{Var}(u^T X) = u^T \\mathbb{E}[(X - \\mu)(X - \\mu)^T] u$."
        ],
        "solution": "PCA finds directions maximizing variance around the mean. If the data is not centered, maximizing $u^T (X^T X) u$ maximizes the second raw moment $\\mathbb{E}[(u^T x)^2] = \\text{Var}(u^T x) + (u^T \\mu)^2$. If $\\mu$ is far from the origin, the first component simply points from the origin to the center of the cloud, failing to capture internal variance. Option A is correct.",
        "commonMistakes": ["Believing centering is required for matrix invertibility."],
        "relatedLesson": "week-7/week-7.html",
        "relatedLab": "visual_labs.html#lab-pca"
    },
    {
        "id": "w7-orig-q02",
        "version": 1,
        "title": "Sample Covariance Between Two 2D Features",
        "week": 7,
        "conceptIds": ["covariance-matrix", "pca"],
        "prerequisiteConceptIds": ["covariance-matrix"],
        "type": "numeric",
        "difficulty": "easy",
        "estimatedMinutes": 3,
        "platform": "local",
        "provenance": "original",
        "verificationStatus": "reviewed",
        "source": {"citation": "Original MLF Covariance Calculation", "url": None},
        "statement": "Given three 2D observations: $(x_1, y_1) = (1, 1)$, $(x_2, y_2) = (2, 3)$, and $(x_3, y_3) = (3, 5)$. Notice that the mean is $(\\bar{x}, \\bar{y}) = (2, 3)$. Compute the sample covariance $\\text{Cov}(X, Y) = \\frac{1}{N} \\sum_{i=1}^3 (x_i - \\bar{x})(y_i - \\bar{y})$ using $N = 3$.",
        "options": [],
        "answerSpec": {"correctOptionIds": [], "numericValue": 1.33, "tolerance": 0.03},
        "hints": [
            "Deviations for $x$: $1-2 = -1$, $2-2 = 0$, $3-2 = 1$.",
            "Deviations for $y$: $1-3 = -2$, $3-3 = 0$, $5-3 = 2$.",
            "Sum of products: $(-1)(-2) + (0)(0) + (1)(2) = 2 + 0 + 2 = 4$.",
            "Divide by $N=3$: $4/3 \\approx 1.333$."
        ],
        "solution": "$$\\text{Deviations}: x - \\bar{x} = [-1, 0, 1], \\quad y - \\bar{y} = [-2, 0, 2].$$\n$$\\sum_{i=1}^3 (x_i - \\bar{x})(y_i - \\bar{y}) = (-1)(-2) + (0)(0) + (1)(2) = 2 + 2 = 4.$$\n$$\\text{Cov}(X, Y) = \\frac{4}{3} \\approx 1.33.$$",
        "commonMistakes": ["Dividing by $N-1=2$ instead of population formula $N=3$ specified in problem."],
        "relatedLesson": "week-7/week-7.html",
        "relatedLab": "visual_labs.html#lab-pca"
    },
    {
        "id": "w7-orig-q03",
        "version": 1,
        "title": "Lagrangian Optimization for First Principal Component",
        "week": 7,
        "conceptIds": ["pca", "lagrangian-optimization"],
        "prerequisiteConceptIds": ["pca"],
        "type": "mcq",
        "difficulty": "medium",
        "estimatedMinutes": 4,
        "platform": "local",
        "provenance": "original",
        "verificationStatus": "reviewed",
        "source": {"citation": "Original MLF Principal Component Derivation", "url": None},
        "statement": "When deriving the first principal component direction $u_1$, we formulate the constrained optimization problem $\\max_{u} u^T \\Sigma u$ subject to $u^T u = 1$. Using the Lagrangian $\\mathcal{L}(u, \\lambda) = u^T \\Sigma u - \\lambda(u^T u - 1)$, setting $\\nabla_u \\mathcal{L} = 0$ leads directly to which fundamental equation?",
        "options": [
            {"id": "a", "text": "$\\Sigma u = \\lambda u$, the eigenvalue equation for sample covariance matrix $\\Sigma$."},
            {"id": "b", "text": "$\\Sigma^{-1} u = \\lambda u$."},
            {"id": "c", "text": "$u^T \\Sigma = \\lambda I$."},
            {"id": "d", "text": "$\\nabla_u \\Sigma = 0$."}
        ],
        "answerSpec": {"correctOptionIds": ["a"], "numericValue": None, "tolerance": None},
        "hints": [
            "Compute vector derivative $\\nabla_u (u^T \\Sigma u) = 2 \\Sigma u$ (since $\\Sigma$ is symmetric).",
            "Compute $\\nabla_u (u^T u) = 2 u$.",
            "Set $2 \\Sigma u - 2 \\lambda u = 0$."
        ],
        "solution": "Taking gradient with respect to $u$:\n$$\\nabla_u \\mathcal{L} = 2 \\Sigma u - 2 \\lambda u = 0 \\implies \\Sigma u = \\lambda u.$$\nThis proves that the direction of maximum projected variance must be an eigenvector of the covariance matrix $\\Sigma$, and the projected variance $u^T \\Sigma u = u^T (\\lambda u) = \\lambda$ is maximized by choosing the eigenvector corresponding to the largest eigenvalue $\\lambda_1$. Option A is correct.",
        "commonMistakes": ["Thinking the Lagrangian leads to a linear system rather than an eigenvalue problem."],
        "relatedLesson": "week-7/week-7.html",
        "relatedLab": "visual_labs.html#lab-pca"
    },
    {
        "id": "w7-orig-q04",
        "version": 1,
        "title": "Properties of the Sample Covariance Matrix",
        "week": 7,
        "conceptIds": ["covariance-matrix", "pca"],
        "prerequisiteConceptIds": ["covariance-matrix"],
        "type": "msq",
        "difficulty": "medium",
        "estimatedMinutes": 4,
        "platform": "local",
        "provenance": "original",
        "verificationStatus": "reviewed",
        "source": {"citation": "Original MLF Covariance Matrix Properties", "url": None},
        "statement": "Let $\\Sigma = \\frac{1}{N} X_c^T X_c \\in \\mathbb{R}^{d \\times d}$ be the sample covariance matrix of centered data $X_c$. Which of the following statements are always mathematically true?",
        "options": [
            {"id": "a", "text": "$\\Sigma$ is symmetric: $\\Sigma^T = \\Sigma$."},
            {"id": "b", "text": "$\\Sigma$ is positive semi-definite: $u^T \\Sigma u \\ge 0$ for all $u \\in \\mathbb{R}^d$."},
            {"id": "c", "text": "All eigenvalues of $\\Sigma$ are real and non-negative: $\\lambda_i \\ge 0$."},
            {"id": "d", "text": "$\\Sigma$ is always strictly invertible, even when $N < d$."}
        ],
        "answerSpec": {"correctOptionIds": ["a", "b", "c"], "numericValue": None, "tolerance": None},
        "hints": [
            "Consider $u^T \\Sigma u = \\frac{1}{N} \\|X_c u\\|_2^2 \\ge 0$.",
            "If $N < d$, $\\text{rank}(\\Sigma) \\le N < d$, so $\\Sigma$ is singular."
        ],
        "solution": "$\\Sigma$ is symmetric and positive semi-definite because $u^T \\Sigma u = \\frac{1}{N} \\|X_c u\\|^2 \\ge 0$. By the Spectral Theorem, its eigenvalues are real and non-negative. However, if sample size $N < d$, the rank of $\\Sigma$ is at most $N < d$, so $\\det(\\Sigma) = 0$ and it is NOT invertible. Therefore A, B, and C are correct, while D is false.",
        "commonMistakes": ["Assuming covariance matrices are always full rank when $N < d$."],
        "relatedLesson": "week-7/week-7.html",
        "relatedLab": "visual_labs.html#lab-pca"
    },
    {
        "id": "w7-orig-q05",
        "version": 1,
        "title": "Total Variance and Trace of Covariance Matrix",
        "week": 7,
        "conceptIds": ["pca", "covariance-matrix"],
        "prerequisiteConceptIds": ["covariance-matrix"],
        "type": "numeric",
        "difficulty": "easy",
        "estimatedMinutes": 2,
        "platform": "local",
        "provenance": "original",
        "verificationStatus": "reviewed",
        "source": {"citation": "Original MLF Total Variance Exercise", "url": None},
        "statement": "The covariance matrix of a 3D dataset has eigenvalues $\\lambda_1 = 8.0$, $\\lambda_2 = 3.5$, and $\\lambda_3 = 0.5$. What is the total variance of the dataset, given by $\\text{Tr}(\\Sigma) = \\sum_{i=1}^3 \\lambda_i$?",
        "options": [],
        "answerSpec": {"correctOptionIds": [], "numericValue": 12.0, "tolerance": 0.05},
        "hints": [
            "Total variance equals the trace of $\\Sigma$, which equals the sum of its eigenvalues: $8.0 + 3.5 + 0.5$."
        ],
        "solution": "$$\\text{Total Variance} = \\text{Tr}(\\Sigma) = \\sum_{i=1}^3 \\lambda_i = 8.0 + 3.5 + 0.5 = 12.0.$$",
        "commonMistakes": ["Multiplying eigenvalues instead of summing."],
        "relatedLesson": "week-7/week-7.html",
        "relatedLab": "visual_labs.html#lab-pca"
    },
    {
        "id": "w7-orig-q06",
        "version": 1,
        "title": "Explained Variance Ratio Calculation",
        "week": 7,
        "conceptIds": ["pca", "explained-variance"],
        "prerequisiteConceptIds": ["pca"],
        "type": "numeric",
        "difficulty": "easy",
        "estimatedMinutes": 2,
        "platform": "local",
        "provenance": "original",
        "verificationStatus": "reviewed",
        "source": {"citation": "Original MLF Explained Variance Problem", "url": None},
        "statement": "A covariance matrix has eigenvalues $\\lambda = [6, 2, 2]$. Compute the percentage of total variance explained by the first principal component ($k=1$), given by $\\frac{\\lambda_1}{\\sum \\lambda_i} \\times 100$. Enter as an integer percentage.",
        "options": [],
        "answerSpec": {"correctOptionIds": [], "numericValue": 60, "tolerance": 0.5},
        "hints": [
            "Total variance = $6 + 2 + 2 = 10$.",
            "Proportion for component 1: $6 / 10 = 0.60 = 60\\%$."
        ],
        "solution": "$$\\text{Explained Variance Ratio} = \\frac{6}{6 + 2 + 2} = \\frac{6}{10} = 0.60 = 60\\%.$$",
        "commonMistakes": ["Dividing by the count of features (3) instead of total eigenvalue sum (10)."],
        "relatedLesson": "week-7/week-7.html",
        "relatedLab": "visual_labs.html#lab-pca"
    },
    {
        "id": "w7-orig-q07",
        "version": 1,
        "title": "Dual Views: Max Variance vs Min Reconstruction Error",
        "week": 7,
        "conceptIds": ["pca", "reconstruction-error"],
        "prerequisiteConceptIds": ["pca"],
        "type": "mcq",
        "difficulty": "medium",
        "estimatedMinutes": 4,
        "platform": "local",
        "provenance": "original",
        "verificationStatus": "reviewed",
        "source": {"citation": "Original MLF Dual Formulation of PCA", "url": None},
        "statement": "In PCA, the maximum projected variance formulation and the minimum mean squared reconstruction error formulation are mathematically equivalent. Why?",
        "options": [
            {"id": "a", "text": "By the Pythagorean theorem, for any projection $P_U x$, $\\|x\\|^2 = \\|P_U x\\|^2 + \\|x - P_U x\\|^2$. Since $\\|x\\|^2$ is fixed, maximizing projection variance $\\|P_U x\\|^2$ directly minimizes reconstruction error $\\|x - P_U x\\|^2$."},
            {"id": "b", "text": "Because reconstruction error is defined to be zero for any orthogonal transformation."},
            {"id": "c", "text": "Because covariance matrices are always symmetric and positive definite."},
            {"id": "d", "text": "Because the eigenvalues of a projection matrix always sum to zero."}
        ],
        "answerSpec": {"correctOptionIds": ["a"], "numericValue": None, "tolerance": None},
        "hints": [
            "Decompose each vector $x = P x + (I - P)x$ into orthogonal components.",
            "Sum of squared norms is constant: Total Variance = Captured Variance + Residual Error."
        ],
        "solution": "For orthogonal projection $P$, the Pythagorean theorem yields $\\|x\\|^2 = \\|P x\\|^2 + \\|x - P x\\|^2$. Averaging over all samples: $\\text{Total Variance} = \\text{Projected Variance} + \\text{Reconstruction Error}$. Because total variance is an invariant property of the original dataset, maximizing the projected variance is mathematically equivalent to minimizing the reconstruction error. Option A is correct.",
        "commonMistakes": ["Thinking the two formulations optimize different subspaces."],
        "relatedLesson": "week-7/week-7.html",
        "relatedLab": "visual_labs.html#lab-pca"
    },
    {
        "id": "w7-orig-q08",
        "version": 1,
        "title": "Exact Mathematical Connection: PCA and SVD",
        "week": 7,
        "conceptIds": ["pca", "svd"],
        "prerequisiteConceptIds": ["svd", "pca"],
        "type": "msq",
        "difficulty": "medium",
        "estimatedMinutes": 4,
        "platform": "local",
        "provenance": "original",
        "verificationStatus": "reviewed",
        "source": {"citation": "Original MLF PCA-SVD Equivalence", "url": None},
        "statement": "Let centered data matrix $X_c \\in \\mathbb{R}^{N \\times d}$ have SVD $X_c = U \\Sigma V^T$. How do the PCA components and eigenvalues relate to this SVD?",
        "options": [
            {"id": "a", "text": "The right singular vectors (columns of $V$) are the principal component loading directions."},
            {"id": "b", "text": "The sample covariance matrix eigenvalues relate to singular values via $\\lambda_i = \\frac{\\sigma_i^2}{N}$."},
            {"id": "c", "text": "The projected principal component scores are given by $Z = X_c V = U \\Sigma$."},
            {"id": "d", "text": "The left singular vectors (columns of $U$) represent the feature weights."}
        ],
        "answerSpec": {"correctOptionIds": ["a", "b", "c"], "numericValue": None, "tolerance": None},
        "hints": [
            "Covariance $\\Sigma_X = \\frac{1}{N} X_c^T X_c = \\frac{1}{N} (V \\Sigma U^T)(U \\Sigma V^T) = \\frac{1}{N} V \\Sigma^2 V^T$.",
            "Projected scores: $Z = X_c V = (U \\Sigma V^T) V = U \\Sigma$."
        ],
        "solution": "Substituting SVD $X_c = U \\Sigma V^T$ into the sample covariance matrix yields $\\frac{1}{N} X_c^T X_c = V (\\frac{\\Sigma^2}{N}) V^T$. Thus the right singular vectors $V$ are the principal eigenvectors (loadings), and eigenvalues are $\\lambda_i = \\sigma_i^2 / N$. The projected coordinates (scores) are $X_c V = U \\Sigma$. Columns of $U$ are normalized score directions across samples, not feature weights. Options A, B, C are correct.",
        "commonMistakes": ["Confusing $U$ (sample space) with $V$ (feature space)."],
        "relatedLesson": "week-7/week-7.html",
        "relatedLab": "visual_labs.html#lab-pca"
    },
    {
        "id": "w7-orig-q09",
        "version": 1,
        "title": "Scree Plot and the Elbow Criterion",
        "week": 7,
        "conceptIds": ["pca", "scree-plot"],
        "prerequisiteConceptIds": ["pca"],
        "type": "mcq",
        "difficulty": "easy",
        "estimatedMinutes": 3,
        "platform": "local",
        "provenance": "original",
        "verificationStatus": "reviewed",
        "source": {"citation": "Original MLF Scree Plot Analysis", "url": None},
        "statement": "What is a Scree Plot in PCA, and how is the 'elbow criterion' used to select the number of retained principal components $k$?",
        "options": [
            {"id": "a", "text": "A plot of eigenvalues $\\lambda_i$ in descending order against component index $i$; the elbow is the point where the eigenvalues level off, indicating subsequent components represent primarily noise."},
            {"id": "b", "text": "A scatter plot of the first two features against each other to identify clusters."},
            {"id": "c", "text": "A histogram of the residuals to verify Gaussian assumptions."},
            {"id": "d", "text": "A plot of sample sizes versus computational runtime."}
        ],
        "answerSpec": {"correctOptionIds": ["a"], "numericValue": None, "tolerance": None},
        "hints": [
            "'Scree' is a geological term for the rubble at the base of a cliff.",
            "The steep cliff represents major variance components; the rubble represents insignificant noise dimensions."
        ],
        "solution": "A scree plot plots the eigenvalues $\\lambda_i$ (or explained variance ratio) against the component index $i$ in descending order. The 'elbow' is the point of inflection where the sharp decline transitions into a shallow horizontal slope. Components before the elbow capture true signal, while components after it represent noise. Option A is correct.",
        "commonMistakes": ["Confusing a scree plot with a 2D scatter plot."],
        "relatedLesson": "week-7/week-7.html",
        "relatedLab": "visual_labs.html#lab-pca"
    },
    {
        "id": "w7-orig-q10",
        "version": 1,
        "title": "Reconstruction Error Formula from Discarded Eigenvalues",
        "week": 7,
        "conceptIds": ["pca", "reconstruction-error"],
        "prerequisiteConceptIds": ["reconstruction-error"],
        "type": "numeric",
        "difficulty": "medium",
        "estimatedMinutes": 3,
        "platform": "local",
        "provenance": "original",
        "verificationStatus": "reviewed",
        "source": {"citation": "Original MLF Reconstruction Error Calculation", "url": None},
        "statement": "A 4-dimensional centered dataset has covariance matrix eigenvalues $\\lambda = [14, 5, 2, 1]$. If we compress the data to $k = 2$ dimensions using PCA, what is the expected mean squared reconstruction error $\\frac{1}{N} \\sum_{i=1}^N \\|x_i - \\hat{x}_i\\|_2^2 = \\sum_{j=k+1}^d \\lambda_j$?",
        "options": [],
        "answerSpec": {"correctOptionIds": [], "numericValue": 3.0, "tolerance": 0.05},
        "hints": [
            "Retained components are $k=1, 2$ with eigenvalues $14$ and $5$.",
            "Discarded components are $j=3, 4$ with eigenvalues $2$ and $1$.",
            "Sum the discarded eigenvalues: $2 + 1 = 3$."
        ],
        "solution": "The mean squared reconstruction error in PCA equals the sum of the discarded eigenvalues:\n$$\\text{MSE} = \\sum_{j=k+1}^d \\lambda_j = \\lambda_3 + \\lambda_4 = 2 + 1 = 3.0.$$",
        "commonMistakes": ["Summing the retained eigenvalues ($14 + 5 = 19$) instead of discarded ones."],
        "relatedLesson": "week-7/week-7.html",
        "relatedLab": "visual_labs.html#lab-pca"
    },
    {
        "id": "w7-orig-q11",
        "version": 1,
        "title": "Mutual Orthogonality of Principal Directions",
        "week": 7,
        "conceptIds": ["pca", "orthogonality"],
        "prerequisiteConceptIds": ["pca"],
        "type": "msq",
        "difficulty": "medium",
        "estimatedMinutes": 3,
        "platform": "local",
        "provenance": "original",
        "verificationStatus": "reviewed",
        "source": {"citation": "Original MLF PCA Orthogonality Review", "url": None},
        "statement": "Let $u_1, u_2, \\dots, u_d$ be the principal component direction vectors obtained from covariance matrix $\\Sigma$. Which orthogonality properties are guaranteed?",
        "options": [
            {"id": "a", "text": "They are mutually orthogonal: $u_i^T u_j = 0$ for all $i \\neq j$."},
            {"id": "b", "text": "They are mutually conjugate with respect to $\\Sigma$: $u_i^T \\Sigma u_j = 0$ for all $i \\neq j$."},
            {"id": "c", "text": "Each direction vector has unit length: $\\|u_i\\|_2 = 1$."},
            {"id": "d", "text": "They must all lie strictly in the positive orthant ($u_{ik} \\ge 0$)." }
        ],
        "answerSpec": {"correctOptionIds": ["a", "b", "c"], "numericValue": None, "tolerance": None},
        "hints": [
            "Because $\\Sigma$ is symmetric, eigenvectors corresponding to distinct eigenvalues are mutually orthogonal.",
            "Also $u_i^T \\Sigma u_j = u_i^T (\\lambda_j u_j) = \\lambda_j (u_i^T u_j) = 0$ for $i \\neq j$."
        ],
        "solution": "Eigenvectors of any real symmetric matrix can be chosen to be orthonormal ($u_i^T u_j = \\delta_{ij}$) and mutually conjugate ($u_i^T \\Sigma u_j = \\lambda_j \\delta_{ij} = 0$ for $i \\neq j$). Eigenvectors can contain negative numbers and are defined only up to sign flip. Options A, B, and C are correct.",
        "commonMistakes": ["Believing principal components must be strictly non-negative (that is NMF, not PCA)."],
        "relatedLesson": "week-7/week-7.html",
        "relatedLab": "visual_labs.html#lab-pca"
    },
    {
        "id": "w7-orig-q12",
        "version": 1,
        "title": "Projection of Data Point onto Principal Component",
        "week": 7,
        "conceptIds": ["pca", "projection-matrix"],
        "prerequisiteConceptIds": ["pca"],
        "type": "numeric",
        "difficulty": "medium",
        "estimatedMinutes": 3,
        "platform": "local",
        "provenance": "original",
        "verificationStatus": "reviewed",
        "source": {"citation": "Original MLF PCA Projection Arithmetic", "url": None},
        "statement": "A centered data observation is $x = \\begin{bmatrix} 3 \\\\ 4 \\end{bmatrix}$. The first principal component unit direction is $u_1 = \\begin{bmatrix} 0.6 \\\\ 0.8 \\end{bmatrix}$. Compute the 1D principal component score (coordinate) $z_1 = u_1^T x$.",
        "options": [],
        "answerSpec": {"correctOptionIds": [], "numericValue": 5.0, "tolerance": 0.05},
        "hints": [
            "Compute dot product: $z_1 = (0.6)(3) + (0.8)(4)$.",
            "$1.8 + 3.2 = 5.0$."
        ],
        "solution": "$$z_1 = u_1^T x = 0.6(3) + 0.8(4) = 1.8 + 3.2 = 5.0.$$",
        "commonMistakes": ["Multiplying matrices in wrong order."],
        "relatedLesson": "week-7/week-7.html",
        "relatedLab": "visual_labs.html#lab-pca"
    },
    {
        "id": "w7-orig-q13",
        "version": 1,
        "title": "Scale Sensitivity of PCA and Feature Standardization",
        "week": 7,
        "conceptIds": ["pca", "standardization"],
        "prerequisiteConceptIds": ["pca"],
        "type": "mcq",
        "difficulty": "easy",
        "estimatedMinutes": 3,
        "platform": "local",
        "provenance": "original",
        "verificationStatus": "reviewed",
        "source": {"citation": "Original MLF Preprocessing for PCA", "url": None},
        "statement": "Why is PCA generally **not scale-invariant**, making feature standardization ($z = \\frac{x - \\mu}{\\sigma}$) necessary when features are measured in different physical units (e.g., kilograms vs milligrams)?",
        "options": [
            {"id": "a", "text": "Because features with artificially large numerical variances (e.g. milligrams) will dominate the covariance matrix and hijack the principal components, regardless of their actual informative content."},
            {"id": "b", "text": "Because the covariance matrix becomes non-symmetric if units differ."},
            {"id": "c", "text": "Because eigenvalues cannot be computed if feature scales are unequal."},
            {"id": "d", "text": "Because standardization turns non-linear manifolds into linear hyperplanes."}
        ],
        "answerSpec": {"correctOptionIds": ["a"], "numericValue": None, "tolerance": None},
        "hints": [
            "Multiplying a feature by 1000 multiplies its variance by $10^6$.",
            "PCA maximizes raw variance. A feature scaled in millimeters will appear $10^6$ times more 'important' than one scaled in meters."
        ],
        "solution": "PCA maximizes variance. If one variable has an arbitrary large scale (e.g. income in cents vs age in years), its raw variance will dwarf other variables, causing PC1 to align almost entirely with that single variable. Standardizing features to unit variance (correlation matrix PCA) removes this scale dependency. Option A is correct.",
        "commonMistakes": ["Thinking PCA is inherently scale-invariant like Mahalanobis distance."],
        "relatedLesson": "week-7/week-7.html",
        "relatedLab": "visual_labs.html#lab-pca"
    },
    {
        "id": "w7-orig-q14",
        "version": 1,
        "title": "Uncorrelated Nature of Principal Component Scores",
        "week": 7,
        "conceptIds": ["pca", "covariance-matrix"],
        "prerequisiteConceptIds": ["pca"],
        "type": "msq",
        "difficulty": "medium",
        "estimatedMinutes": 3,
        "platform": "local",
        "provenance": "original",
        "verificationStatus": "reviewed",
        "source": {"citation": "Original MLF Decorrelation Property", "url": None},
        "statement": "Let $Z = X_c U$ be the transformed data points in the principal component coordinate system. Which properties of the transformed coordinates $Z$ are guaranteed?",
        "options": [
            {"id": "a", "text": "The sample covariance matrix of $Z$ is diagonal: $\\text{Cov}(Z_i, Z_j) = 0$ for all $i \\neq j$ (complete decorrelation)."},
            {"id": "b", "text": "The variance of the $i$-th principal component is $\\text{Var}(Z_i) = \\lambda_i$."},
            {"id": "c", "text": "The total variance is preserved: $\\sum_{i=1}^d \\text{Var}(Z_i) = \\sum_{j=1}^d \\text{Var}(X_j)$."},
            {"id": "d", "text": "$Z_i$ and $Z_j$ are always statistically independent, even if the data distribution is non-Gaussian."}
        ],
        "answerSpec": {"correctOptionIds": ["a", "b", "c"], "numericValue": None, "tolerance": None},
        "hints": [
            "Covariance of $Z$ is $\\frac{1}{N} Z^T Z = U^T (\\frac{1}{N} X_c^T X_c) U = U^T \\Sigma U = \\Lambda$ (diagonal).",
            "Zero correlation implies statistical independence ONLY for Gaussian distributions."
        ],
        "solution": "PCA diagonalizes the covariance matrix: $\\text{Cov}(Z) = \\Lambda = \\text{diag}(\\lambda_1, \\dots, \\lambda_d)$. Thus all components are uncorrelated, $\\text{Var}(Z_i) = \\lambda_i$, and total variance is conserved. However, uncorrelatedness implies statistical independence ONLY for multivariate normal distributions. For general distributions, higher-order non-linear dependencies may persist. Options A, B, C are correct.",
        "commonMistakes": ["Confusing zero covariance (uncorrelated) with full statistical independence."],
        "relatedLesson": "week-7/week-7.html",
        "relatedLab": "visual_labs.html#lab-pca"
    },
    {
        "id": "w7-orig-q15",
        "version": 1,
        "title": "Eigenvalues of 2x2 Covariance Matrix",
        "week": 7,
        "conceptIds": ["covariance-matrix", "eigenvalues"],
        "prerequisiteConceptIds": ["eigenvalues"],
        "type": "numeric",
        "difficulty": "medium",
        "estimatedMinutes": 3,
        "platform": "local",
        "provenance": "original",
        "verificationStatus": "reviewed",
        "source": {"citation": "Original MLF 2x2 Spectral Calculation", "url": None},
        "statement": "Given 2D covariance matrix $\\Sigma = \\begin{bmatrix} 5 & 2 \\\\ 2 & 2 \\end{bmatrix}$, calculate the largest eigenvalue $\\lambda_1$.",
        "options": [],
        "answerSpec": {"correctOptionIds": [], "numericValue": 6.0, "tolerance": 0.05},
        "hints": [
            "Characteristic polynomial: $\\det(\\Sigma - \\lambda I) = (5 - \\lambda)(2 - \\lambda) - 4 = \\lambda^2 - 7\\lambda + 6 = 0$.",
            "Factor the polynomial: $(\\lambda - 6)(\\lambda - 1) = 0$."
        ],
        "solution": "$$\\det(\\Sigma - \\lambda I) = (5 - \\lambda)(2 - \\lambda) - 4 = \\lambda^2 - 7\\lambda + 10 - 4 = \\lambda^2 - 7\\lambda + 6 = 0.$$\n$$(\\lambda - 6)(\\lambda - 1) = 0 \\implies \\lambda_1 = 6.0, \\quad \\lambda_2 = 1.0.$$",
        "commonMistakes": ["Calculating the trace (7) instead of the largest root (6)."],
        "relatedLesson": "week-7/week-7.html",
        "relatedLab": "visual_labs.html#lab-pca"
    },
    {
        "id": "w7-orig-q16",
        "version": 1,
        "title": "High-Dimensional PCA Trick When N < D",
        "week": 7,
        "conceptIds": ["pca", "computational-complexity"],
        "prerequisiteConceptIds": ["pca"],
        "type": "mcq",
        "difficulty": "hard",
        "estimatedMinutes": 4,
        "platform": "local",
        "provenance": "original",
        "verificationStatus": "reviewed",
        "source": {"citation": "Original MLF High-Dimensional PCA Method", "url": None},
        "statement": "In genomic and facial image datasets where feature count $D = 100,000$ vastly exceeds sample size $N = 50$, computing the full $D \\times D$ covariance matrix is computationally prohibitive ($O(D^2)$ memory). How does the 'high-dimensional PCA trick' (Gram matrix trick) solve this?",
        "options": [
            {"id": "a", "text": "It computes the $N \\times N$ Gram matrix $K = X_c X_c^T$ instead. If $K v = \\mu v$, then $u = X_c^T v$ is an eigenvector of $X_c^T X_c$ with the same eigenvalue $\\mu$."},
            {"id": "b", "text": "It discards the first 99,950 features randomly before running standard PCA."},
            {"id": "c", "text": "It replaces PCA with simple feature standardization."},
            {"id": "d", "text": "It computes the inverse covariance matrix using gradient descent."}
        ],
        "answerSpec": {"correctOptionIds": ["a"], "numericValue": None, "tolerance": None},
        "hints": [
            "Multiply $X_c X_c^T v = \\mu v$ on the left by $X_c^T$:",
            "$X_c^T (X_c X_c^T v) = X_c^T (\\mu v) \\implies (X_c^T X_c)(X_c^T v) = \\mu (X_c^T v)$."
        ],
        "solution": "When $N \\ll D$, $X_c X_c^T$ is only $N \\times N$ (e.g. $50 \\times 50$), which is trivial to diagonalize. If $v$ is an eigenvector of $X_c X_c^T$ with eigenvalue $\\mu$, multiplying by $X_c^T$ gives $(X_c^T X_c)(X_c^T v) = \\mu (X_c^T v)$. Thus $u = X_c^T v$ (normalized) is an exact eigenvector of the huge $D \\times D$ matrix $X_c^T X_c$. This reduces complexity from $O(D^3)$ to $O(N^3 + D N^2)$. Option A is correct.",
        "commonMistakes": ["Thinking $X_c^T X_c$ must always be directly formed."],
        "relatedLesson": "week-7/week-7.html",
        "relatedLab": "visual_labs.html#lab-pca"
    },
    {
        "id": "w7-orig-q17",
        "version": 1,
        "title": "Minimum Components for Target Variance Threshold",
        "week": 7,
        "conceptIds": ["pca", "explained-variance"],
        "prerequisiteConceptIds": ["pca"],
        "type": "numeric",
        "difficulty": "easy",
        "estimatedMinutes": 2,
        "platform": "local",
        "provenance": "original",
        "verificationStatus": "reviewed",
        "source": {"citation": "Original MLF Dimension Selection Exercise", "url": None},
        "statement": "A dataset has covariance matrix eigenvalues $\\lambda = [5.0, 3.0, 1.0, 1.0]$. How many principal components $k$ are needed to explain at least 80% of the total variance?",
        "options": [],
        "answerSpec": {"correctOptionIds": [], "numericValue": 2, "tolerance": 0},
        "hints": [
            "Total variance = $5.0 + 3.0 + 1.0 + 1.0 = 10.0$.",
            "80% threshold = $0.80 \\times 10.0 = 8.0$.",
            "Cumulative sums: $k=1 \\implies 5.0$ (50%), $k=2 \\implies 5.0 + 3.0 = 8.0$ (80%)."
        ],
        "solution": "Total eigenvalue sum is $10.0$. 80% of total variance is $8.0$.\nWith $k=1$, variance captured is $5.0$ ($50\\%$).\nWith $k=2$, variance captured is $5.0 + 3.0 = 8.0$ ($80\\%$).\nThus exactly $k=2$ components are required.",
        "commonMistakes": ["Counting 3 components instead of 2."],
        "relatedLesson": "week-7/week-7.html",
        "relatedLab": "visual_labs.html#lab-pca"
    },
    {
        "id": "w7-orig-q18",
        "version": 1,
        "title": "Inherent Assumptions and Limitations of PCA",
        "week": 7,
        "conceptIds": ["pca", "limitations-of-pca"],
        "prerequisiteConceptIds": ["pca"],
        "type": "msq",
        "difficulty": "medium",
        "estimatedMinutes": 4,
        "platform": "local",
        "provenance": "original",
        "verificationStatus": "reviewed",
        "source": {"citation": "Original MLF PCA Limitations Analysis", "url": None},
        "statement": "Which of the following are recognized mathematical limitations and assumptions of standard Principal Component Analysis?",
        "options": [
            {"id": "a", "text": "Linearity assumption: PCA can only discover linear subspaces and fails on non-linear manifolds (such as a Swiss roll)."},
            {"id": "b", "text": "Unsupervised nature: PCA maximizes overall variance, which does not necessarily align with class separability (unlike LDA)."},
            {"id": "c", "text": "Sensitivity to outliers: Because variance is based on squared Euclidean distances, extreme outliers disproportionately distort principal axes."},
            {"id": "d", "text": "Inability to work on datasets where sample size $N$ is smaller than feature count $d$."}
        ],
        "answerSpec": {"correctOptionIds": ["a", "b", "c"], "numericValue": None, "tolerance": None},
        "hints": [
            "Consider non-linear dimensionality reduction (Kernel PCA, t-SNE, UMAP).",
            "Consider PCA vs LDA (unsupervised vs supervised).",
            "Remember that PCA works fine when $N < d$ (yielding at most $N$ non-zero components)."
        ],
        "solution": "Standard PCA assumes linear combinations, is unsupervised (variance $\\neq$ discrimination), and is vulnerable to outliers due to $L_2$ squared distance penalties. However, PCA works perfectly well when $N < d$ (producing $\\min(N-1, d)$ components). Options A, B, and C are correct.",
        "commonMistakes": ["Believing PCA cannot be applied when $N < d$."],
        "relatedLesson": "week-7/week-7.html",
        "relatedLab": "visual_labs.html#lab-pca"
    }
]


def main():
    # 1. Load existing questions
    with open(ALL_Q_PATH, "r", encoding="utf-8") as f:
        all_questions = json.load(f)

    with open(W3_Q_PATH, "r", encoding="utf-8") as f:
        w3_questions = json.load(f)

    all_ids = {q["id"] for q in all_questions}

    # Add Week 3 questions
    w3_ids = {q["id"] for q in w3_questions}
    for q in WEEK3_NEW:
        if q["id"] not in w3_ids:
            w3_questions.append(q)
            w3_ids.add(q["id"])
        if q["id"] not in all_ids:
            all_questions.append(q)
            all_ids.add(q["id"])

    # Add Week 6 questions
    w6_questions = [q for q in all_questions if q["week"] == 6]
    for q in WEEK6_NEW:
        if q["id"] not in all_ids:
            all_questions.append(q)
            all_ids.add(q["id"])
            w6_questions.append(q)

    # Add Week 7 questions
    w7_questions = [q for q in all_questions if q["week"] == 7]
    for q in WEEK7_NEW:
        if q["id"] not in all_ids:
            all_questions.append(q)
            all_ids.add(q["id"])
            w7_questions.append(q)

    # Save question files
    with open(W3_Q_PATH, "w", encoding="utf-8") as f:
        json.dump(w3_questions, f, indent=2)

    with open(W6_Q_PATH, "w", encoding="utf-8") as f:
        json.dump(w6_questions, f, indent=2)

    with open(W7_Q_PATH, "w", encoding="utf-8") as f:
        json.dump(w7_questions, f, indent=2)

    with open(ALL_Q_PATH, "w", encoding="utf-8") as f:
        json.dump(all_questions, f, indent=2)

    print(f"Updated all_questions.json: {len(all_questions)} total questions.")
    print(f"Week 3 questions: {len(w3_questions)}")
    print(f"Week 6 questions: {len(w6_questions)}")
    print(f"Week 7 questions: {len(w7_questions)}")

    # 2. Update assessments.json
    with open(ASSESSMENTS_PATH, "r", encoding="utf-8") as f:
        assessments = json.load(f)

    # Define week3-mastery (15 questions)
    assessments["week3-mastery"] = {
        "id": "week3-mastery",
        "version": 1,
        "title": "Week 3 Mastery Assessment: Subspaces, Projections & Least Squares",
        "origin": "original",
        "coverageStatus": "mastery-check",
        "description": "Timed mastery assessment testing vector subspaces, projection matrices, Gram-Schmidt orthogonality, and least squares normal equations.",
        "durationSeconds": 1500,
        "instructions": [
            "Dedicated Week 3 mastery assessment containing 15 curated questions.",
            "Includes conceptual multiple choice, multi-select, and numerical calculation items.",
            "Time limit is 25 minutes with automatic browser-persisted state.",
            "Submission updates your mastery analytics and flags any weak concepts for targeted review."
        ],
        "questionIds": [
            "iitm-w3-q01",
            "iitm-w3-q02",
            "iitm-w3-q03",
            "iitm-w3-q04",
            "iitm-w3-q06",
            "iitm-w3-q08",
            "iitm-w3-q11",
            "iitm-w3-q12",
            "w3-orig-q14",
            "w3-orig-q15",
            "w3-orig-q16",
            "w3-orig-q17",
            "w3-orig-q18",
            "w3-orig-q19",
            "w3-orig-q21"
        ],
        "scoring": {
            "mcq": {"correct": 1, "incorrect": 0},
            "msq": {"mode": "exact-set", "correct": 1, "incorrect": 0},
            "numeric": {"correct": 1, "incorrect": 0},
            "unanswered": 0
        }
    }

    # Define week6-mastery (15 questions)
    assessments["week6-mastery"] = {
        "id": "week6-mastery",
        "version": 1,
        "title": "Week 6 Mastery Assessment: Singular Value Decomposition & Positive Definite Matrices",
        "origin": "original",
        "coverageStatus": "mastery-check",
        "description": "Timed mastery assessment covering SVD geometry, truncated SVD approximations, condition numbers, and positive definiteness.",
        "durationSeconds": 1500,
        "instructions": [
            "Dedicated Week 6 mastery assessment containing 15 curated questions.",
            "Covers Eckart-Young-Mirsky theorem, singular vectors, condition numbers, and pseudoinverses.",
            "Time limit is 25 minutes."
        ],
        "questionIds": [
            "q-w6-iitm-20",
            "w6-orig-q01",
            "w6-orig-q02",
            "w6-orig-q03",
            "w6-orig-q04",
            "w6-orig-q05",
            "w6-orig-q06",
            "w6-orig-q07",
            "w6-orig-q08",
            "w6-orig-q09",
            "w6-orig-q10",
            "w6-orig-q11",
            "w6-orig-q12",
            "w6-orig-q13",
            "w6-orig-q15"
        ],
        "scoring": {
            "mcq": {"correct": 1, "incorrect": 0},
            "msq": {"mode": "exact-set", "correct": 1, "incorrect": 0},
            "numeric": {"correct": 1, "incorrect": 0},
            "unanswered": 0
        }
    }

    # Define week7-mastery (15 questions)
    assessments["week7-mastery"] = {
        "id": "week7-mastery",
        "version": 1,
        "title": "Week 7 Mastery Assessment: Principal Component Analysis & Dimensionality Reduction",
        "origin": "original",
        "coverageStatus": "mastery-check",
        "description": "Timed mastery assessment covering sample covariance, maximum variance derivation, explained variance ratios, and PCA reconstruction error.",
        "durationSeconds": 1500,
        "instructions": [
            "Dedicated Week 7 mastery assessment containing 15 curated questions.",
            "Covers mean centering, covariance spectrum, scree plot analysis, and PCA-SVD connections.",
            "Time limit is 25 minutes."
        ],
        "questionIds": [
            "q-w7-iitm-22",
            "w7-orig-q01",
            "w7-orig-q02",
            "w7-orig-q03",
            "w7-orig-q04",
            "w7-orig-q05",
            "w7-orig-q06",
            "w7-orig-q07",
            "w7-orig-q08",
            "w7-orig-q09",
            "w7-orig-q10",
            "w7-orig-q11",
            "w7-orig-q12",
            "w7-orig-q13",
            "w7-orig-q14"
        ],
        "scoring": {
            "mcq": {"correct": 1, "incorrect": 0},
            "msq": {"mode": "exact-set", "correct": 1, "incorrect": 0},
            "numeric": {"correct": 1, "incorrect": 0},
            "unanswered": 0
        }
    }

    with open(ASSESSMENTS_PATH, "w", encoding="utf-8") as f:
        json.dump(assessments, f, indent=2)

    print(f"Updated assessments.json with week3-mastery, week6-mastery, week7-mastery.")


if __name__ == "__main__":
    main()
