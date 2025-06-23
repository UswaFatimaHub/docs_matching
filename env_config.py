import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

class envconfig:
    MONGO_URI = os.getenv("MONGO_URI")
    MONGO_DB = os.getenv("MONGO_DB", "embedding_db")
    MONGO_COLLECTION = os.getenv("MONGO_COLLECTION", "articles")
    SENTENCE_TRANSFORMER_MODEL = os.getenv("SENTENCE_TRANSFORMER_MODEL", "all-MiniLM-L6-v2")
