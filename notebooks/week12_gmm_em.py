"""
Week 12: Gaussian Mixture Model (GMM) with Expectation-Maximization
IIT Madras - Machine Learning Foundations
"""
import numpy as np

def run_em_gmm_1d(data, k=2, max_iter=30):
    # Initialize
    mu = np.linspace(np.min(data), np.max(data), k)
    sigma = np.ones(k) * np.std(data)
    pi = np.ones(k) / k
    
    def norm_pdf(x, m, s):
        return (1.0 / (np.sqrt(2 * np.pi) * s)) * np.exp(-0.5 * ((x - m) / s)**2)
        
    for step in range(max_iter):
        # E-step
        resp = np.zeros((len(data), k))
        for j in range(k):
            resp[:, j] = pi[j] * norm_pdf(data, mu[j], sigma[j])
        resp /= np.sum(resp, axis=1, keepdims=True)
        
        # M-step
        Nk = np.sum(resp, axis=0)
        for j in range(k):
            mu[j] = np.sum(resp[:, j] * data) / Nk[j]
            sigma[j] = np.sqrt(np.sum(resp[:, j] * (data - mu[j])**2) / Nk[j])
        pi = Nk / len(data)
        
    return mu, sigma, pi

if __name__ == "__main__":
    np.random.seed(42)
    samples = np.concatenate([np.random.normal(-3, 1, 300), np.random.normal(4, 1.5, 400)])
    mu_est, sigma_est, pi_est = run_em_gmm_1d(samples, k=2)
    print("Estimated Means:", np.round(mu_est, 2))
    print("Estimated Stds:", np.round(sigma_est, 2))
    print("Estimated Mixing Weights:", np.round(pi_est, 2))
