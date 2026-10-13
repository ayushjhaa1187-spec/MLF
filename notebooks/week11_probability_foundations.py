"""
Week 11: Probability Foundations & Bayesian Posterior Updating
Machine Learning Foundations - IIT Madras BS in Data Science (BSCS2004)
"""
import numpy as np

def bayes_posterior(prior: float, likelihood: float, evidence: float) -> float:
    """Computes posterior P(A | B) = P(B | A) * P(A) / P(B)."""
    return (likelihood * prior) / evidence

def sample_moments(samples: np.ndarray) -> tuple[float, float]:
    """Computes sample mean and unbiased sample variance."""
    mean = float(np.mean(samples))
    var = float(np.var(samples, ddof=1))
    return mean, var

def run_tests():
    # Medical test example: Prior P(D) = 0.01, Sensitivity P(+ | D) = 0.99, P(+ | not D) = 0.05
    prior = 0.01
    sens = 0.99
    fp = 0.05
    evidence = sens * prior + fp * (1.0 - prior)
    post = bayes_posterior(prior, sens, evidence)
    # Expected: (0.99 * 0.01) / (0.0099 + 0.0495) = 0.0099 / 0.0594 = 1/6 = 0.166667
    np.testing.assert_allclose(post, 1.0 / 6.0, rtol=1e-4)

    # Law of large numbers sample test
    np.random.seed(42)
    data = np.random.normal(loc=5.0, scale=2.0, size=10000)
    mean, var = sample_moments(data)
    assert np.isclose(mean, 5.0, atol=0.05), "LLN mean failed"
    assert np.isclose(var, 4.0, atol=0.15), "LLN variance failed"
    print("[PASS] Week 11 probability foundations verified successfully!")

if __name__ == "__main__":
    run_tests()
