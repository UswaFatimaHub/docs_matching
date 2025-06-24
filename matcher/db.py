from pymongo import MongoClient
from bson import ObjectId
import logging
from env_config import envconfig

envvars = envconfig()
logger = logging.getLogger(__name__)

# client = MongoClient(envvars.MONGO_URI)
# db = client[envvars.MONGO_DB]
# collection = db[envvars.MONGO_COLLECTION]

def get_collection():
    client = MongoClient(envvars.MONGO_URI)
    db = client[envvars.MONGO_DB]
    return db[envvars.MONGO_COLLECTION]



def get_documents_without_embeddings_batch(collection, skip: int = 0, limit: int = 1000):
    logger.info(f"Fetching documents without embeddings, skip: {skip}, limit: {limit}")
    return list(collection.find(
        {
            "status": "Published",
            "embedding": {"$exists": False}
        }
    ).skip(skip).limit(limit))

def get_documents_batch(collection, skip: int = 0, limit: int = 10):
    logger.info(f"Fetching documents, skip: {skip}, limit: {limit}")
    return list(collection.find(
        {"embedding": {"$exists": True}}
    ).skip(skip).limit(limit))

def update_embedding_for_doc(collection, doc_id, embedding):
    logger.info(f"Updating embedding for document ID: {doc_id}")
    collection.update_one(
        {"_id": ObjectId(doc_id)},
        {"$set": {"embedding": embedding}}
    )
