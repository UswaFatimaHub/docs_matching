# scripts/download_model.py
from sentence_transformers import SentenceTransformer
import os
from dotenv import load_dotenv
load_dotenv()


if __name__ == "__main__":
    print("⏬ Downloading model...")
    SentenceTransformer(os.getenv('SENTENCE_TRANSFORMER_MODEL', 'sentence-transformers/LaBSE'))
    print("✅ Model downloaded and cached.")
