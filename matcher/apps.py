from django.apps import AppConfig
import logging

logger = logging.getLogger(__name__)


class MatcherConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'matcher'

    # def ready(self):
    #     from matcher.embeddings import encode_text
    #     try:
    #         encode_text("warmup")  # Trigger model load
    #         logger.info("✅ SentenceTransformer model loaded and ready for requests.")
    #     except Exception as e:
    #         logger.exception("❌ Failed to load SentenceTransformer model at startup: %s", e)