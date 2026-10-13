"""
Unit & Integration Tests: Visual Labs Mathematical Correctness
Verifies:
1. Subspace Orthogonal Projection Lab (Week 3):
   - Basis matrix A, Projection matrix P = A(A^T A)^-1 A^T = diag(1, 1, 0)
   - For arbitrary vector b:
     - p = P b in C(A)
     - e = b - p is strictly orthogonal to every column of A: a_1^T e == 0, a_2^T e == 0
     - p^T e == 0
     - Pythagorean identity: ||b||_2^2 == ||p||_2^2 + ||e||_2^2
   - Presets:
     - In-plane vector: e == 0
     - Orthogonal vector: p == 0
2. Gradient Descent Simulation Lab (Week 8):
   - Function f(x, y) = x^2 + 3y^2
   - Gradient grad(f) = [2x, 6y]^T
   - Hessian H = diag(2, 6), Lipschitz constant L = 6
   - Critical learning rate eta_c = 2/L = 1/3 ~ 0.333
   - For eta = 0.15 < eta_c: monotonic convergence to (0, 0), loss drops below 0.01 within 40 steps.
   - For eta = 0.36 > eta_c: divergence in y-coordinate (|y_k| -> inf).
"""
import unittest
import numpy as np


class TestVisualLabsMath(unittest.TestCase):

    def setUp(self):
        # Basis matrix for xy-plane in R^3
        self.A = np.array([
            [1.0, 0.0],
            [0.0, 1.0],
            [0.0, 0.0]
        ])
        # Projection matrix P = A (A^T A)^-1 A^T
        AtA_inv = np.linalg.inv(self.A.T @ self.A)
        self.P = self.A @ AtA_inv @ self.A.T

    def test_projection_matrix_properties(self):
        # P must be idempotent: P^2 = P
        np.testing.assert_allclose(self.P @ self.P, self.P, atol=1e-12)
        # P must be symmetric: P^T = P
        np.testing.assert_allclose(self.P.T, self.P, atol=1e-12)
        # Exact diagonal representation
        expected_P = np.diag([1.0, 1.0, 0.0])
        np.testing.assert_allclose(self.P, expected_P, atol=1e-12)

    def test_arbitrary_projection_orthogonality(self):
        rng = np.random.RandomState(42)
        for _ in range(50):
            b = rng.uniform(-10.0, 10.0, size=(3,))
            p = self.P @ b
            e = b - p

            # p must have z-coordinate = 0 (resides in C(A))
            self.assertAlmostEqual(p[2], 0.0, places=10)

            # e must have x, y coordinates = 0 (purely orthogonal to C(A))
            self.assertAlmostEqual(e[0], 0.0, places=10)
            self.assertAlmostEqual(e[1], 0.0, places=10)

            # a_1^T e == 0 and a_2^T e == 0
            self.assertAlmostEqual(np.dot(self.A[:, 0], e), 0.0, places=10)
            self.assertAlmostEqual(np.dot(self.A[:, 1], e), 0.0, places=10)

            # Orthogonality between p and e: p^T e == 0
            self.assertAlmostEqual(np.dot(p, e), 0.0, places=10)

            # Pythagorean identity: ||b||^2 = ||p||^2 + ||e||^2
            norm_b_sq = np.dot(b, b)
            norm_sum_sq = np.dot(p, p) + np.dot(e, e)
            self.assertAlmostEqual(norm_b_sq, norm_sum_sq, places=10)

    def test_projection_presets(self):
        # Preset 1: In-plane vector b = [3.0, 2.0, 0.0]
        b_inplane = np.array([3.0, 2.0, 0.0])
        p1 = self.P @ b_inplane
        e1 = b_inplane - p1
        np.testing.assert_allclose(p1, b_inplane, atol=1e-12)
        np.testing.assert_allclose(e1, np.zeros(3), atol=1e-12)

        # Preset 2: Pure orthogonal vector b = [0.0, 0.0, 3.5]
        b_orth = np.array([0.0, 0.0, 3.5])
        p2 = self.P @ b_orth
        e2 = b_orth - p2
        np.testing.assert_allclose(p2, np.zeros(3), atol=1e-12)
        np.testing.assert_allclose(e2, b_orth, atol=1e-12)

    def test_gradient_descent_convergence(self):
        # f(x, y) = x^2 + 3y^2
        # grad = [2x, 6y]
        lr = 0.15  # < 0.333
        x, y = 3.5, 2.5
        initial_loss = x**2 + 3 * y**2

        losses = [initial_loss]
        for step in range(40):
            gx = 2 * x
            gy = 6 * y
            x = x - lr * gx
            y = y - lr * gy
            loss = x**2 + 3 * y**2
            losses.append(loss)

        # Monotonically decreasing
        for i in range(len(losses) - 1):
            self.assertLess(losses[i+1], losses[i], f"Step {i+1} did not strictly decrease loss")

        # Converges near minimum (0, 0)
        self.assertLess(losses[-1], 0.01)
        self.assertAlmostEqual(x, 0.0, delta=0.05)
        self.assertAlmostEqual(y, 0.0, delta=0.01)

    def test_gradient_descent_divergence_above_critical_lr(self):
        # With lr = 0.36 > 0.333, y-component oscillates and blows up:
        # y_{k+1} = y_k - 0.36 * (6 y_k) = y_k (1 - 2.16) = -1.16 y_k
        lr = 0.36
        x, y = 3.5, 2.5
        for _ in range(25):
            gx = 2 * x
            gy = 6 * y
            x = x - lr * gx
            y = y - lr * gy

        # y magnitude must explode beyond 20
        self.assertGreater(abs(y), 20.0, "Gradient descent should diverge when eta > 2/L")

    def test_svd_3stage_decomposition(self):
        # 2x2 matrix used in SVD visual lab
        A = np.array([[3.0, 2.0], [2.0, 3.0]])
        U, S, Vt = np.linalg.svd(A)
        V = Vt.T

        # 1. Orthonormality of U and V
        np.testing.assert_allclose(U.T @ U, np.eye(2), atol=1e-12)
        np.testing.assert_allclose(V.T @ V, np.eye(2), atol=1e-12)

        # 2. Singular values match sqrt(eigenvalues(A^T A))
        AtA = A.T @ A
        eigvals = np.sort(np.linalg.eigvalsh(AtA))[::-1]
        np.testing.assert_allclose(S, np.sqrt(eigvals), atol=1e-12)
        self.assertAlmostEqual(S[0], 5.0, places=10)
        self.assertAlmostEqual(S[1], 1.0, places=10)

        # 3. Exact reconstruction: A == U @ diag(S) @ V^T
        A_reconstructed = U @ np.diag(S) @ Vt
        np.testing.assert_allclose(A, A_reconstructed, atol=1e-12)

        # 4. Condition number
        kappa = S[0] / S[1]
        self.assertAlmostEqual(kappa, 5.0, places=10)

        # 5. Eckart-Young Rank-1 approximation error: ||A - A_1||_F == S[1]
        A_1 = S[0] * np.outer(U[:, 0], Vt[0, :])
        fro_err = np.linalg.norm(A - A_1, 'fro')
        self.assertAlmostEqual(fro_err, S[1], places=10)

    def test_pca_variance_and_reconstruction_conservation(self):
        # Deterministic 2D dataset used in PCA visual lab
        X = np.array([
            [-3.0, -1.5],
            [-2.0, -2.0],
            [-1.0, -0.5],
            [ 0.0,  0.0],
            [ 1.0,  0.8],
            [ 2.0,  1.5],
            [ 3.0,  2.2]
        ])
        N = len(X)
        mean = np.mean(X, axis=0)
        np.testing.assert_allclose(mean, np.zeros(2), atol=0.1) # nearly centered
        X_c = X - mean

        # Sample covariance
        cov = (X_c.T @ X_c) / N
        total_variance = np.trace(cov)

        # Eigendecomposition
        eigvals, eigvecs = np.linalg.eigh(cov)
        idx = np.argsort(eigvals)[::-1]
        lambda1, lambda2 = eigvals[idx]
        pc1_vec = eigvecs[:, idx[0]]

        # Conservation test across 100 angles:
        # Projected variance V(theta) + Reconstruction MSE E(theta) == Tr(cov)
        for theta_deg in np.linspace(0, 180, 100):
            theta = np.radians(theta_deg)
            u = np.array([np.cos(theta), np.sin(theta)])

            # Projected coordinates z = X_c @ u
            z = X_c @ u
            proj_var = np.mean(z**2)

            # Reconstructed points: X_hat = np.outer(z, u)
            X_hat = np.outer(z, u)
            recon_mse = np.mean(np.sum((X_c - X_hat)**2, axis=1))

            # Exact conservation
            self.assertAlmostEqual(proj_var + recon_mse, total_variance, places=10)

            # Projected variance must never exceed lambda1 or drop below lambda2
            self.assertLessEqual(proj_var, lambda1 + 1e-10)
            self.assertGreaterEqual(proj_var, lambda2 - 1e-10)

        # Test maximum occurs at principal direction
        pc1_angle = np.arctan2(pc1_vec[1], pc1_vec[0])
        u_star = np.array([np.cos(pc1_angle), np.sin(pc1_angle)])
        max_proj_var = np.mean((X_c @ u_star)**2)
        self.assertAlmostEqual(max_proj_var, lambda1, places=10)


if __name__ == "__main__":
    unittest.main()

