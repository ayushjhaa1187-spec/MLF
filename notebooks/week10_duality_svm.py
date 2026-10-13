"""
Week 10: Lagrangian Duality & Linear Support Vector Machine (Pegasos Algorithm)
Machine Learning Foundations - IIT Madras BS in Data Science (BSCS2004)
"""
import numpy as np

def pegasos_svm_train(X: np.ndarray, y: np.ndarray, lambda_reg: float = 0.01, epochs: int = 200) -> tuple[np.ndarray, float]:
    """
    Trains linear SVM with bias using Pegasos subgradient descent.
    Augments features with a bias coordinate: [x, 1].
    Minimizes: (lambda/2) * ||w||^2 + (1/N) * sum max(0, 1 - y_i * (w^T x_i + b))
    """
    n, d = X.shape
    # Feature augmentation with bias coordinate
    X_aug = np.hstack([X, np.ones((n, 1))])
    w_aug = np.zeros(d + 1)
    
    t = 0
    for epoch in range(1, epochs + 1):
        for i in range(n):
            t += 1
            eta = 1.0 / (lambda_reg * t)
            margin = y[i] * np.dot(w_aug, X_aug[i])
            if margin < 1.0:
                # Subgradient step on hinge loss
                w_aug = (1.0 - eta * lambda_reg) * w_aug + eta * y[i] * X_aug[i]
            else:
                w_aug = (1.0 - eta * lambda_reg) * w_aug

    w = w_aug[:-1]
    b = float(w_aug[-1])
    return w, b

def predict(X: np.ndarray, w: np.ndarray, b: float) -> np.ndarray:
    return np.sign(X @ w + b)

def run_tests():
    # Linearly separable 2D dataset with offset
    X = np.array([[1.0, 2.0], [2.0, 3.0], [3.0, 1.0], [5.0, 5.0], [6.0, 7.0], [7.0, 5.0]])
    y = np.array([-1.0, -1.0, -1.0, 1.0, 1.0, 1.0])
    
    w, b = pegasos_svm_train(X, y, lambda_reg=0.005, epochs=500)
    preds = predict(X, w, b)
    np.testing.assert_array_equal(preds, y, err_msg="SVM misclassified training points")
    print("[PASS] Week 10 linear SVM duality verified successfully!")

if __name__ == "__main__":
    run_tests()
