from pymongo import MongoClient
from bson import ObjectId
import os
from env_config import envconfig

envvars = envconfig()



client = MongoClient(envvars.MONGO_URI)
db = client[envvars.MONGO_DB]
collection = db[envvars.MONGO_COLLECTION]

def get_documents_without_embeddings():
    query = {
        "embedding": {"$exists": False}
    }
    return list(collection.find(query))

def get_all_documents():
    query = {}
    return list(collection.find(query))

def insert_document(document, embedding):
    collection.insert_one({"document": document, "embedding": embedding})

def update_embedding_for_doc(doc_id, embedding):
    collection.update_one(
        {"_id": ObjectId(doc_id)},
        {"$set": {"embedding": embedding}}
    )
