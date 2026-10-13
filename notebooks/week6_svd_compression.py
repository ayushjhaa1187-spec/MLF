"""
Week 6: Singular Value Decomposition (SVD) & Low-Rank Approximation
IIT Madras - Machine Learning Foundations
"""
import numpy as np

def low_rank_svd_approx(A, k):
    """
    Computes optimal rank-k approximation under Frobenius norm (Eckart-Young Theorem)
    """
    U, S, Vt = np.linalg.svd(A, full_matrices=False)
    A_k = (U[:, :k] * S[:k]) @ Vt[:k, :]
    error = np.linalg.norm(A - A_k, 'fro')
    theoretical_error = np.sqrt(np.sum(S[k:]**2))
    return A_k, error, theoretical_error

if __name__ == "__main__":
    np.random.seed(42)
    # Simulate a 100 x 80 matrix
    data_matrix = np.random.randn(100, 80)
    
    k = 10
    A_approx, empirical_err, theoretical_err = low_rank_svd_approx(data_matrix, k)
    print(f"Rank-{k} Approximation Completed.")
    print(f"Empirical Frobenius Error: {empirical_err:.4f}")
    print(f"Theoretical Error from Singular Values: {theoretical_err:.4f}")
    assert np.isclose(empirical_err, theoretical_err)
