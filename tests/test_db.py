from matcher.db import get_documents_without_embeddings_batch, update_embedding_for_doc
import numpy as np

# Simulated embedding vector for test
mock_embedding = np.random.rand(768).tolist()

def test_db_filters_docs_without_embeddings(mock_mongo):

    mock_mongo.insert_many([
        {"title": "A", "embedding": mock_embedding, "status": "Published"},
        {"title": "B", "status": "Published"},
        {"title": "C", "status": "Draft"}
    ])
    result = get_documents_without_embeddings_batch(mock_mongo)
    assert len(result) == 1
    assert result[0]["title"] == "B"

def test_update_embedding_for_doc(mock_mongo):
    doc = mock_mongo.insert_one({"title": "Test"}).inserted_id
    update_embedding_for_doc(mock_mongo, doc, mock_embedding)
    updated = mock_mongo.find_one({"_id": doc})
    assert updated["embedding"] == mock_embedding

def test_get_documents_batch_returns_limited_docs(mock_mongo):
    docs = [{"title": f"Doc {i}", "embedding": [0.1] * 768} for i in range(15)]
    mock_mongo.insert_many(docs)
    
    from matcher.db import get_documents_batch
    batch = get_documents_batch(collection=mock_mongo, skip=0, limit=10)
    
    assert len(batch) == 10

def test_get_documents_batch_skips_correctly(mock_mongo):
    docs = [{"title": f"Doc {i}", "embedding": [0.1] * 768} for i in range(5)]
    mock_mongo.insert_many(docs)

    from matcher.db import get_documents_batch
    batch = get_documents_batch(collection=mock_mongo, skip=3, limit=10)

    titles = [doc["title"] for doc in batch]
    assert all(title in ["Doc 3", "Doc 4"] for title in titles)

