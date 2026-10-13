"""
Week 3: Subspaces, Orthogonal Projections & Least Squares Regression
Machine Learning Foundations - IIT Madras BS in Data Science (BSCS2004)

This module provides verified, production-grade implementations of:
1. Normal Equations: (A^T A) x = A^T b
2. Numerically stable QR Factorization: A = Q R, R x = Q^T b
3. Subspace Projection Matrix: P = A (A^T A)^{-1} A^T
4. Orthogonality verification: A^T (b - A x_hat) == 0
5. Leverage score computation: h_ii = P_{ii}
"""

import numpy as np


def solve_least_squares_normal(A: np.ndarray, b: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Solves overdetermined linear system Ax = b using the classical Normal Equations.
    
    Parameters:
        A: Design matrix of shape (m, n) with m >= n.
        b: Observation vector of shape (m,) or (m, 1).
        
    Returns:
        x_hat: Optimal least squares parameter vector of shape (n,).
        P: Orthogonal projection matrix onto C(A) of shape (m, m).
        p: Projected vector on C(A) of shape (m,).
        e: Residual error vector (b - p) of shape (m,).
    """
    m, n = A.shape
    if m < n:
        raise ValueError(f"System is underdetermined: rows {m} < cols {n}")

    # Condition number check
    cond_num = np.linalg.cond(A)
    if cond_num > 1e12:
        print(f"Warning: Matrix A is severely ill-conditioned (kappa={cond_num:.2e}). Use QR instead.")

    # Form ATA and ATb
    ATA = A.T @ A
    ATb = A.T @ b

    # Solve ATA @ x_hat = ATb using Cholesky / LU without explicit inversion
    x_hat = np.linalg.solve(ATA, ATb)

    # Subspace Projection matrix P = A (A^T A)^(-1) A^T
    # Verify symmetry and idempotency
    ATA_inv = np.linalg.inv(ATA)
    P = A @ ATA_inv @ A.T

    p = P @ b
    e = b - p

    return x_hat, P, p, e


def solve_least_squares_qr(A: np.ndarray, b: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Solves Ax = b using thin QR decomposition: A = Q R.
    Numerically stable against condition squaring.
    
    Returns:
        x_hat: Optimal parameters
        p: Projected vector
        e: Residual error vector
    """
    Q, R = np.linalg.qr(A, mode='reduced')
    Qty = Q.T @ b
    x_hat = np.linalg.solve(R, Qty)

    p = A @ x_hat
    e = b - p
    return x_hat, p, e


def compute_leverage_scores(P: np.ndarray) -> np.ndarray:
    """
    Extracts hat matrix diagonal leverage scores: h_ii = P_ii.
    Observations with h_ii > 2*p/n are high-leverage points.
    """
    return np.diag(P)


def run_test_suite():
    """Runs automated unit test assertions verifying mathematical properties."""
    print("Running Week 3 Mathematical Verification Test Suite...")

    # Test 1: Worked Example 1 from Textbook
    # Points: (1, 2), (2, 2), (3, 4) -> Model: y = theta_1 * x + theta_2
    A_ex1 = np.array([
        [1.0, 1.0],
        [2.0, 1.0],
        [3.0, 1.0]
    ])
    b_ex1 = np.array([2.0, 2.0, 4.0])

    x_hat, P, p, e = solve_least_squares_normal(A_ex1, b_ex1)
    x_qr, p_qr, e_qr = solve_least_squares_qr(A_ex1, b_ex1)

    # Analytical values: theta_1 = 1.0, theta_2 = 2/3 = 0.666667
    expected_theta = np.array([1.0, 2.0 / 3.0])
    np.testing.assert_allclose(x_hat, expected_theta, rtol=1e-5, err_msg="Normal equation theta mismatch")
    np.testing.assert_allclose(x_qr, expected_theta, rtol=1e-5, err_msg="QR factorization theta mismatch")

    # Property 1: Orthogonality Principle: A^T @ e == 0
    ortho_check = A_ex1.T @ e
    np.testing.assert_allclose(ortho_check, [0.0, 0.0], atol=1e-10, err_msg="Orthogonality principle failed!")

    # Property 2: Symmetry of P: P^T == P
    np.testing.assert_allclose(P, P.T, atol=1e-10, err_msg="Projection matrix is not symmetric!")

    # Property 3: Idempotency of P: P @ P == P
    np.testing.assert_allclose(P @ P, P, atol=1e-10, err_msg="Projection matrix is not idempotent!")

    # Property 4: Trace of P equals rank(A) = 2
    np.testing.assert_allclose(np.trace(P), 2.0, atol=1e-10, err_msg="Trace(P) does not equal rank!")

    # Property 5: Pythagoras Theorem: ||b||^2 == ||p||^2 + ||e||^2
    norm_b_sq = np.sum(b_ex1 ** 2)
    norm_p_sq = np.sum(p ** 2)
    norm_e_sq = np.sum(e ** 2)
    np.testing.assert_allclose(norm_b_sq, norm_p_sq + norm_e_sq, atol=1e-10, err_msg="Pythagorean theorem failed!")

    print("[PASS] All Week 3 mathematical test assertions verified successfully!")
    print(f"Optimal Parameters: slope={x_hat[0]:.4f}, intercept={x_hat[1]:.4f}")
    print(f"Residual Sum of Squares (RSS): {norm_e_sq:.4f}")
    print(f"Leverage Scores: {np.round(compute_leverage_scores(P), 4)}")


if __name__ == "__main__":
    run_test_suite()
