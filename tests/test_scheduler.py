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

def test_scheduler_handles_failed_embedding(monkeypatch, mock_mongo):
    mock_mongo.insert_one({
        "title": "Bad",
        "summary": "Test",
        "answer": "Failing",
        "tags": [],
        "status": "Published"
    })

    # Patch where encode_text is used, not where it's defined
    monkeypatch.setattr(
        "matcher.management.commands.runapscheduler.encode_text",
        lambda x: (print("PATCHED!") or (_ for _ in ()).throw(RuntimeError("fail")))

    )
    
    run_embedding_sync(mock_mongo, batch_size=1)

    doc = mock_mongo.find_one()
    print(doc)
    assert "embedding" not in doc  # Should not update due to error
