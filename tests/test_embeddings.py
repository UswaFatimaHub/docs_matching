# tests/test_embedding.py
from matcher.embeddings import encode_text
import numpy as np
import pytest


def test_embedding_output():
    embedding = encode_text("This is a test")
    assert isinstance(embedding, (list, np.ndarray)) 
    assert len(embedding) > 0
    assert embedding.shape[0] == 768

def test_embedding_empty_string():
    embedding = encode_text("")
    assert isinstance(embedding, (list, np.ndarray))


def test_embedding_consistency():
    text = "Bonjour"
    vec1 = encode_text(text)
    vec2 = encode_text(text)
    assert vec1 == pytest.approx(vec2, rel=1e-5)

def test_embedding_invalid_input_type():
    with pytest.raises(TypeError):
        encode_text(12345)
