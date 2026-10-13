"""
Week 1: Vector Arithmetic, Inner Products & Linear Algebra Foundations
Machine Learning Foundations - IIT Madras BS in Data Science (BSCS2004)
"""
import numpy as np

def vector_dot_product(u: np.ndarray, v: np.ndarray) -> float:
    """Computes standard Euclidean inner product <u, v> = u^T v."""
    return float(np.dot(u, v))

def vector_cosine_similarity(u: np.ndarray, v: np.ndarray) -> float:
    """Computes cosine of angle theta between non-zero vectors u and v."""
    norm_u = np.linalg.norm(u)
    norm_v = np.linalg.norm(v)
    if norm_u == 0 or norm_v == 0:
        raise ValueError("Cannot compute angle with zero vector")
    return float(np.dot(u, v) / (norm_u * norm_v))

def run_tests():
    u = np.array([1.0, 2.0, 3.0])
    v = np.array([4.0, -1.0, 2.0])
    dot = vector_dot_product(u, v)
    assert np.isclose(dot, 1.0 * 4.0 - 2.0 * 1.0 + 3.0 * 2.0), "Dot product failed"
    
    # Orthogonal vectors check
    a = np.array([1.0, 0.0])
    b = np.array([0.0, 1.0])
    assert np.isclose(vector_cosine_similarity(a, b), 0.0), "Orthogonal cosine should be 0"
    print("[PASS] Week 1 vector operations verified successfully!")

if __name__ == "__main__":
    run_tests()
