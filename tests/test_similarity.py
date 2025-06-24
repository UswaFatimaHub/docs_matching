# tests/test_similarity.py
import pytest
from matcher.services import cosine_similarity

def test_cosine_similarity_identity():
    vec = [1, 0, 0]
    assert cosine_similarity(vec, vec) == pytest.approx(1.0)

def test_cosine_similarity_orthogonal():
    a = [1, 0]
    b = [0, 1]
    assert cosine_similarity(a, b) == pytest.approx(0.0)


def test_cosine_similarity_random():
    a = [1, 2, 3]
    b = [4, 5, 6]
    result = cosine_similarity(a, b)
    assert isinstance(result, float)

