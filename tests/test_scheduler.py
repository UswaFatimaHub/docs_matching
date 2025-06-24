# tests/test_scheduler.py
from matcher.management.commands.runapscheduler import run_embedding_sync

def test_scheduler_embedding_sync(mock_mongo):
    mock_mongo.insert_many([
        {"title": "Doc A", "summary": "Some summary", "answer": "<p>Answer</p>", "tags": ["tag1"], "status": "Published"},
        {"title": "Doc B", "summary": "", "status": "Published"},
    ])
    run_embedding_sync(mock_mongo, batch_size=1)
    docs_with_embeddings = list(mock_mongo.find({"embedding": {"$exists": True}}))
    assert len(docs_with_embeddings) >= 1
