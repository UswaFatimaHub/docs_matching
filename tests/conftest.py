import pytest
import mongomock
from unittest.mock import patch

@pytest.fixture(scope="function")
def mock_mongo():
    client = mongomock.MongoClient()
    db = client["testdb"]
    return db["articles"]

# @pytest.fixture(scope="function")
# def patched_get_collection(mock_mongo):
#     """Patch get_collection() to return our in-memory collection."""
#     with patch("matcher.db.get_collection", return_value=mock_mongo):
#         yield mock_mongo
