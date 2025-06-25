from matcher.services import get_top_matches, encode_text

def test_get_top_matches_returns_sorted_results(mock_mongo):
    # Generate real embedding for one doc

    # Insert test docs
    mock_mongo.insert_many([
        {
            "title": "Doc 1",
            "summary": "Test summary 1",
            "answer": "<p>Hello World</p>",
            "tags": ["tag1", "tag2"],
            "embedding": encode_text("Doc 1 Test summary 1 Hello World tag1 tag2").tolist()
        },
        {
            "title": "Doc 2",
            "summary": "Test summary 2",
            "status": "Published",
            "embedding": encode_text("Doc 2 Test summary 2").tolist()
        }
    ])
    
    result = get_top_matches("Hello world", top_k=2, collection=mock_mongo)
    
    assert len(result) == 2
    assert result[0]["score"] >= result[1]["score"]

def test_get_top_matches_empty_collection(mock_mongo):
    from matcher.services import get_top_matches
    result = get_top_matches("query", collection=mock_mongo)
    assert result == []

def test_get_top_matches_less_than_top_k(mock_mongo):
    from matcher.embeddings import encode_text
    from matcher.services import get_top_matches
    
    mock_mongo.insert_one({
        "title": "Only Doc",
        "summary": "Minimal",
        "answer": "Just one",
        "tags": [],
        "embedding": encode_text("Only Doc Minimal Just one").tolist()
    })

    result = get_top_matches("Only", top_k=5, collection=mock_mongo)
    assert len(result) == 1

