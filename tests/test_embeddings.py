# tests/test_embedding.py
from matcher.embeddings import encode_text
import numpy as np

def test_embedding_output():
    embedding = encode_text("This is a test")
    assert isinstance(embedding, (list, np.ndarray)) 
    assert len(embedding) > 0
    assert embedding.shape[0] == 768

def test_embedding_empty_string():
    embedding = encode_text("")
    assert isinstance(embedding, (list, np.ndarray))