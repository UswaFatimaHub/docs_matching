import heapq
import numpy as np
from .db import get_documents_batch
from .embeddings import encode_text
import logging

logger = logging.getLogger(__name__)

def cosine_similarity(a, b):
    a, b = np.array(a), np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def get_top_matches(question: str, top_k: int = 5, batch_size: int = 1000):
    logger.info(f"🔍 Matching question: {question}")
    question_embedding = encode_text(question)
    heap = []  # Min-heap to store top_k matches
    offset = 0

    while True:
        batch = get_documents_batch(skip=offset, limit=batch_size)
        logger.debug(f"Fetched {len(batch)} documents from database")
        if not batch:
            break

        for doc in batch:
            if "embedding" not in doc:
                continue
            score = cosine_similarity(question_embedding, doc["embedding"])
            result = {
                "document_id": str(doc["_id"]),
                "match_score": float(score),
                "document": {
                    "title": doc.get("title", ""),
                    "summary": doc.get("summary", "")
                }
            }
            if len(heap) < top_k:
                heapq.heappush(heap, (score, result))
            else:
                heapq.heappushpop(heap, (score, result))

        offset += batch_size

    # Return top_k in descending order
    logger.debug(f"Keeping top {top_k} matches")
    return [item[1] for item in sorted(heap, key=lambda x: x[0], reverse=True)]