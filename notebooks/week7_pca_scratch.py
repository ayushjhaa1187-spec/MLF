"""
Week 7: Principal Component Analysis (PCA) from Scratch
IIT Madras - Machine Learning Foundations
"""
import numpy as np

class PCA:
    def __init__(self, n_components):
        self.n_components = n_components
        self.mean = None
        self.components = None
        self.explained_variance_ratio = None
        
    def fit(self, X):
        self.mean = np.mean(X, axis=0)
        X_centered = X - self.mean
        cov = (X_centered.T @ X_centered) / (len(X) - 1)
        eigvals, eigvecs = np.linalg.eigh(cov)
        
        idx = np.argsort(eigvals)[::-1]
        eigvals = eigvals[idx]
        eigvecs = eigvecs[:, idx]
        
        self.components = eigvecs[:, :self.n_components]
        self.explained_variance_ratio = eigvals[:self.n_components] / np.sum(eigvals)
        return self
        
    def transform(self, X):
        return (X - self.mean) @ self.components

if __name__ == "__main__":
    np.random.seed(42)
    X = np.random.randn(200, 5) @ np.random.randn(5, 5)
    pca = PCA(n_components=2)
    pca.fit(X)
    X_reduced = pca.transform(X)
    print("Reduced shape:", X_reduced.shape)
    print("Explained variance ratio of top 2 PCs:", pca.explained_variance_ratio)
