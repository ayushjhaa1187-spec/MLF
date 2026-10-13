"""
Week 4: Eigenvalues, Matrix Diagonalization & Power Iteration
Machine Learning Foundations - IIT Madras BS in Data Science (BSCS2004)
"""
import numpy as np

def diagonalize_matrix(A: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """
    Computes eigendecomposition A = V Lambda V^{-1}.
    Returns eigenvalues and matrix of eigenvectors V.
    """
    eigenvalues, V = np.linalg.eig(A)
    return eigenvalues, V

def matrix_power_via_diagonalization(A: np.ndarray, k: int) -> np.ndarray:
    """Computes A^k via V Lambda^k V^{-1}."""
    eigenvalues, V = np.linalg.eig(A)
    Lambda_k = np.diag(eigenvalues ** k)
    return V @ Lambda_k @ np.linalg.inv(V)

def run_tests():
    # Test on matrix A = [[2, 1], [0, 3]]
    A = np.array([[2.0, 1.0], [0.0, 3.0]])
    eigenvalues, V = diagonalize_matrix(A)
    
    # Check A @ V == V @ diag(eigenvalues)
    np.testing.assert_allclose(A @ V, V @ np.diag(eigenvalues), atol=1e-10)
    
    # Power test: A^4
    A_4_diag = matrix_power_via_diagonalization(A, 4)
    A_4_direct = np.linalg.matrix_power(A, 4)
    np.testing.assert_allclose(A_4_diag, A_4_direct, atol=1e-10)
    print("[PASS] Week 4 eigenvalue diagonalization verified successfully!")

if __name__ == "__main__":
    run_tests()
