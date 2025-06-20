import numpy as np
from .db import get_all_documents
from .embeddings import encode_text

def cosine_similarity(a, b):
    a, b = np.array(a), np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def get_top_matches(question: str, top_k: int = 5):
    question_embedding = encode_text(question)
    documents = get_all_documents()

    scored_docs = []
    for doc in documents:
        score = cosine_similarity(question_embedding, doc["embedding"])
        scored_docs.append({
            "document_id": str(doc["_id"]),
            "match_score": float(score),
            "document": {
                "title": doc.get("title", ""),
                "summary": doc.get("summary", "")
            }
        })

    return sorted(scored_docs, key=lambda x: x["match_score"], reverse=True)[:top_k]
