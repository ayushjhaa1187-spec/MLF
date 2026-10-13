"""
Week 9: Constrained Optimization & Projected Gradient Descent
Machine Learning Foundations - IIT Madras BS in Data Science (BSCS2004)
"""
import numpy as np

def project_onto_l2_ball(x: np.ndarray, radius: float = 1.0) -> np.ndarray:
    """Projects vector x onto Euclidean ball {v : ||v||_2 <= radius}."""
    norm = np.linalg.norm(x)
    if norm <= radius:
        return x
    return (radius / norm) * x

def projected_gradient_descent(grad_f, x0: np.ndarray, lr: float = 0.1, radius: float = 1.0, max_iter: int = 50) -> np.ndarray:
    """Solves min f(x) subject to ||x||_2 <= radius using PGD."""
    x = x0.copy()
    for _ in range(max_iter):
        x = x - lr * grad_f(x)
        x = project_onto_l2_ball(x, radius)
    return x

def run_tests():
    # Minimize f(x) = (x[0] - 3)^2 + (x[1] - 4)^2 subject to ||x|| <= 2
    # Unconstrained minimum is (3, 4) with norm 5.
    # Constrained minimum must lie on boundary with norm 2: x* = (2/5)*(3, 4) = (1.2, 1.6)
    grad_f = lambda x: np.array([2 * (x[0] - 3.0), 2 * (x[1] - 4.0)])
    x_opt = projected_gradient_descent(grad_f, np.zeros(2), lr=0.1, radius=2.0, max_iter=100)
    
    expected_opt = np.array([1.2, 1.6])
    np.testing.assert_allclose(x_opt, expected_opt, atol=1e-3)
    assert np.linalg.norm(x_opt) <= 2.0001, "Constraint violated"
    print("[PASS] Week 9 projected gradient descent verified successfully!")

if __name__ == "__main__":
    run_tests()
