from sentence_transformers import SentenceTransformer
from env_config import envconfig

envvars = envconfig()

_model = None

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(envvars.SENTENCE_TRANSFORMER_MODEL, device='cpu')
    return _model

def encode_text(text: str):
    model = get_model()
    return model.encode(text)
