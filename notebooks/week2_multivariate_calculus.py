"""
Week 2: Multivariable Calculus, Gradients, Hessians & Taylor Series
Machine Learning Foundations - IIT Madras BS in Data Science (BSCS2004)
"""
import numpy as np

def numerical_gradient(f, x: np.ndarray, eps: float = 1e-6) -> np.ndarray:
    """Computes finite-difference approximation of gradient vector grad f(x)."""
    grad = np.zeros_like(x)
    for i in range(len(x)):
        x_plus = x.copy()
        x_minus = x.copy()
        x_plus[i] += eps
        x_minus[i] -= eps
        grad[i] = (f(x_plus) - f(x_minus)) / (2 * eps)
    return grad

def numerical_hessian(f, x: np.ndarray, eps: float = 1e-5) -> np.ndarray:
    """Computes finite-difference approximation of Hessian matrix H_ij = d^2 f / dx_i dx_j."""
    n = len(x)
    H = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            x_pp = x.copy(); x_pp[i] += eps; x_pp[j] += eps
            x_pm = x.copy(); x_pm[i] += eps; x_pm[j] -= eps
            x_mp = x.copy(); x_mp[i] -= eps; x_mp[j] += eps
            x_mm = x.copy(); x_mm[i] -= eps; x_mm[j] -= eps
            H[i, j] = (f(x_pp) - f(x_pm) - f(x_mp) + f(x_mm)) / (4 * eps * eps)
    return H

def run_tests():
    # Test function: f(x, y) = x^2 * y + 3 * y^2
    # grad f = [2*x*y, x^2 + 6*y]
    # At (1, 2): grad f = [4, 1 + 12] = [4, 13]
    f = lambda v: v[0]**2 * v[1] + 3 * v[1]**2
    x0 = np.array([1.0, 2.0])
    
    grad_num = numerical_gradient(f, x0)
    expected_grad = np.array([4.0, 13.0])
    np.testing.assert_allclose(grad_num, expected_grad, rtol=1e-4)

    # Hessian: [ [2*y, 2*x], [2*x, 6] ] -> At (1, 2): [ [4, 2], [2, 6] ]
    H_num = numerical_hessian(f, x0)
    expected_H = np.array([[4.0, 2.0], [2.0, 6.0]])
    np.testing.assert_allclose(H_num, expected_H, rtol=1e-3)
    
    print("[PASS] Week 2 numerical gradient and Hessian verified successfully!")

if __name__ == "__main__":
    run_tests()
