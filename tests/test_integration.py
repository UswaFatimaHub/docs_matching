import pytest
import mongomock
from bson import ObjectId
from unittest.mock import patch
from django.test import Client
import uuid
from matcher import db, views, services

from matcher.management.commands.runapscheduler import run_embedding_sync

@pytest.fixture
def isolated_mock_collection(monkeypatch):
    mock_client = mongomock.MongoClient()
    mock_db = mock_client[str(uuid.uuid4())]
    mock_collection = mock_db["articles"]

    # Patch everywhere get_collection is used
    monkeypatch.setattr(db, "get_collection", lambda: mock_collection)
    monkeypatch.setattr(views, "get_collection", lambda: mock_collection)
    monkeypatch.setattr(services, "get_collection", lambda: mock_collection)

    return mock_collection

@pytest.mark.django_db
def test_full_pipeline_match(isolated_mock_collection):

    client = Client()

    # Step 2: Insert doc without embedding
    doc = {
        "_id": ObjectId(),
        "title": "Pipeline Test Doc",
        "summary": "This is a test of full pipeline.",
        "answer": "<p>Pipeline content</p>",
        "tags": ["test", "integration"],
        "status": "Published"
    }
    isolated_mock_collection.insert_one(doc)

    # Step 3: Run embedding sync to generate embedding
    run_embedding_sync(isolated_mock_collection, batch_size=10)

    # Ensure document was updated with embedding
    updated_doc = isolated_mock_collection.find_one({"_id": doc["_id"]})
    assert "embedding" in updated_doc and isinstance(updated_doc["embedding"], list)

    # Step 4: Query the matcher endpoint
    response = client.get("/matcher/match/?q=pipeline")
    assert response.status_code == 200
    results = response.json()["results"]

    # Step 5: Validate match result
    assert isinstance(results, list)
    assert any("Pipeline Test Doc" in r["title"] for r in results)

@pytest.mark.django_db
def test_pipeline_multiple_docs(isolated_mock_collection):
    client = Client()


    docs = [
        {"_id": ObjectId(), "title": "Match A", "summary": "This is relevant", "answer": "<p>content A</p>", "tags": [], "status": "Published"},
        {"_id": ObjectId(), "title": "Match B", "summary": "Less relevant", "answer": "<p>content B</p>", "tags": [], "status": "Published"},
        {"_id": ObjectId(), "title": "Unrelated", "summary": "Irrelevant stuff", "answer": "<p>content C</p>", "tags": [], "status": "Published"},
    ]
    isolated_mock_collection.insert_many(docs)

    run_embedding_sync(collection=isolated_mock_collection)

    response = client.get("/matcher/match/?q=relevant")
    assert response.status_code == 200
    results = response.json()["results"]
    print(results)
    assert results[0]["title"] in ["Match A", "Match B"]

@pytest.mark.django_db
def test_pipeline_no_match(isolated_mock_collection):
    client = Client()

    # Insert docs with no embeddings
    isolated_mock_collection.insert_many([
        {"_id": ObjectId(), "title": "No Embedding", "summary": "", "answer": "", "tags": [], "status": "Published"}
    ])

    response = client.get("/matcher/match/?q=irrelevant")
    assert response.status_code == 200
    results = response.json()["results"]
    assert results == []

@pytest.mark.django_db
def test_pipeline_empty_query(isolated_mock_collection):
    client = Client()

    response = client.get("/matcher/match/?q=")
    assert response.status_code == 400  # or 200 with empty results, depending on implementation

@pytest.mark.django_db
def test_pipeline_partial_document(isolated_mock_collection):
    client = Client()

    doc = {
        "_id": ObjectId(),
        "title": "Partial Doc",
        "summary": "",
        "answer": "",
        "status": "Published"
    }
    isolated_mock_collection.insert_one(doc)

    run_embedding_sync(isolated_mock_collection)

    response = client.get("/matcher/match/?q=partial")
    assert response.status_code == 200
    results = response.json()["results"]
    assert any("Partial Doc" in r["title"] for r in results)

@pytest.mark.django_db
def test_pipeline_batching(isolated_mock_collection):

    # Insert 25 dummy docs
    for i in range(25):
        isolated_mock_collection.insert_one({
            "_id": ObjectId(),
            "title": f"Doc {i}",
            "summary": "summary",
            "answer": "<p>text</p>",
            "status": "Published"
        })

    # Run sync with small batch size to test batching logic
    run_embedding_sync(isolated_mock_collection, batch_size=5)

    # All should be embedded
    assert isolated_mock_collection.count_documents({"embedding": {"$exists": True}}) == 25
