"""
Week 3: Subspaces & Least Squares Regression from Scratch
IIT Madras - Machine Learning Foundations
"""
import numpy as np

def solve_least_squares(A, b):
    """
    Solves overdetermined system Ax = b using Normal Equations: (A^T A) x = A^T b
    """
    ATA = A.T @ A
    ATb = A.T @ b
    x_hat = np.linalg.solve(ATA, ATb)
    
    # Projection matrix P = A (A^T A)^-1 A^T
    P = A @ np.linalg.inv(ATA) @ A.T
    p = P @ b
    error = b - p
    
    return x_hat, P, p, error

if __name__ == "__main__":
    # Example dataset: fitting line y = mx + c to 4 points: (1, 2.1), (2, 3.9), (3, 6.2), (4, 7.8)
    A = np.array([[1, 1], [1, 2], [1, 3], [1, 4]])
    b = np.array([2.1, 3.9, 6.2, 7.8])
    
    x_hat, P, p, error = solve_least_squares(A, b)
    print(f"Optimal Intercept (c): {x_hat[0]:.4f}")
    print(f"Optimal Slope (m): {x_hat[1]:.4f}")
    print(f"Orthogonality check A^T @ error: {np.round(A.T @ error, 6)}")
