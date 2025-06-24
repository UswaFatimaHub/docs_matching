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
