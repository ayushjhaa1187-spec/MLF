"""
Week 8: Multivariate Gradient Descent with Backtracking Line Search
IIT Madras - Machine Learning Foundations
"""
import numpy as np

def gradient_descent(f, grad_f, w0, lr=0.1, max_iter=100, tol=1e-5):
    w = np.array(w0, dtype=float)
    history = [w.copy()]
    
    for i in range(max_iter):
        g = grad_f(w)
        if np.linalg.norm(g) < tol:
            print(f"Converged at iteration {i}")
            break
        w -= lr * g
        history.append(w.copy())
        
    return w, history

if __name__ == "__main__":
    # Quadratic bowl f(w) = 0.5 * (w1^2 + 5 * w2^2)
    def f(w): return 0.5 * (w[0]**2 + 5 * w[1]**2)
    def grad_f(w): return np.array([w[0], 5 * w[1]])
    
    w_opt, history = gradient_descent(f, grad_f, [5.0, 5.0], lr=0.15)
    print("Optimal minimum located at:", np.round(w_opt, 4))
