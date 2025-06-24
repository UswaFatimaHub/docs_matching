import pytest
import mongomock

@pytest.fixture
def mock_mongo():
    client = mongomock.MongoClient()
    db = client["testdb"]
    return db["articles"]
