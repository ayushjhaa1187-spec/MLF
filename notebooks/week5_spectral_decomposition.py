"""
Week 5: Spectral Theorem & Rayleigh Quotient for Real Symmetric Matrices
Machine Learning Foundations - IIT Madras BS in Data Science (BSCS2004)
"""
import numpy as np

def spectral_decomposition(A: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """
    For real symmetric A (A = A^T), computes orthogonal factorization A = Q Lambda Q^T.
    Q has orthonormal columns (Q^T Q = I).
    """
    if not np.allclose(A, A.T):
        raise ValueError("Matrix A must be symmetric")
    eigenvalues, Q = np.linalg.eigh(A)
    return eigenvalues, Q

def rayleigh_quotient(A: np.ndarray, x: np.ndarray) -> float:
    """Computes R_A(x) = (x^T A x) / (x^T x)."""
    return float((x.T @ A @ x) / (x.T @ x))

def run_tests():
    A = np.array([[4.0, 2.0], [2.0, 3.0]])
    eigenvalues, Q = spectral_decomposition(A)
    
    # Verify orthogonality of Q: Q^T Q == I
    np.testing.assert_allclose(Q.T @ Q, np.eye(2), atol=1e-10)
    
    # Verify reconstruction: Q Lambda Q^T == A
    reconstructed = Q @ np.diag(eigenvalues) @ Q.T
    np.testing.assert_allclose(reconstructed, A, atol=1e-10)
    
    # Verify Rayleigh quotient at eigenvector equals eigenvalue
    v_max = Q[:, -1]
    rq = rayleigh_quotient(A, v_max)
    np.testing.assert_allclose(rq, eigenvalues[-1], atol=1e-10)
    print("[PASS] Week 5 spectral decomposition verified successfully!")

if __name__ == "__main__":
    run_tests()
