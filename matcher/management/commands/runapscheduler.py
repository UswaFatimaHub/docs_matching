# matcher/management/commands/runapscheduler.py

from django.core.management.base import BaseCommand
from apscheduler.schedulers.blocking import BlockingScheduler
from matcher.embeddings import encode_text
from matcher.db import get_collection, get_documents_without_embeddings_batch, update_embedding_for_doc, mark_embedding_failed
from bs4 import BeautifulSoup
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def clean_html(html_text):
    if not html_text:
        return ""
    soup = BeautifulSoup(html_text, "html.parser")
    return soup.get_text(separator=" ", strip=True)

# def run_embedding_sync(collection, batch_size=1000):
#     logger.info("🌀 Starting embedding sync...")
#     print(f"🔁 [{datetime.now()}] Running embedding sync job...")
#     updated_count = 0
#     skip = 0

#     while True:
#         docs = get_documents_without_embeddings_batch(collection=collection, skip=skip, limit=batch_size)
#         if not docs:
#             break

#         for doc in docs:
#             title = doc.get("title", "")
#             summary = doc.get("summary", "")
#             answer_html = doc.get("answer", "")
#             tags = doc.get("tags", [])

#             cleaned_answer = clean_html(answer_html)
#             tags_text = " ".join(tags) if isinstance(tags, list) else ""

#             combined_text = f"{title} {summary} {cleaned_answer} {tags_text}".strip()
#             if not combined_text:
#                 continue

#             try:
#                 embedding = encode_text(combined_text).tolist()
#             except Exception as e:
#                 logger.warning(f"❌ Failed to encode text for document {doc["_id"]}: {e}")
#                 continue  # skip this document

#             update_embedding_for_doc(collection, doc["_id"], embedding)
#             updated_count += 1

#         skip += batch_size

#     logger.info(f"✅ Sync complete. {updated_count} documents updated.")
#     print(f"✅ [{datetime.now()}] Sync completed. Updated {updated_count} documents.")

def run_embedding_sync(collection, batch_size=1000):
    logger.info("🌀 Starting embedding sync...")
    print(f"🔁 [{datetime.now()}] Running embedding sync job...")
    updated_count = 0

    while True:
        docs = get_documents_without_embeddings_batch(collection=collection, limit=batch_size)
        if not docs:
            break

        for doc in docs:
            title = doc.get("title", "")
            summary = doc.get("summary", "")
            answer_html = doc.get("answer", "")
            tags = doc.get("tags", [])

            cleaned_answer = clean_html(answer_html)
            tags_text = " ".join(tags) if isinstance(tags, list) else ""

            combined_text = f"{title} {summary} {cleaned_answer} {tags_text}".strip()
            if not combined_text:
                continue

            try:
                embedding = encode_text(combined_text).tolist()
            except Exception as e:
                logger.warning(f"❌ Failed to encode text for document {doc['_id']}: {e}")
                mark_embedding_failed(collection, doc["_id"])
                continue  # skip this document

            update_embedding_for_doc(collection, doc["_id"], embedding)
            updated_count += 1

    logger.info(f"✅ Sync complete. {updated_count} documents updated.")
    print(f"✅ [{datetime.now()}] Sync completed. Updated {updated_count} documents.")


class Command(BaseCommand):
    help = "Run APScheduler"

    def handle(self, *args, **options):
        scheduler = BlockingScheduler()
        collection = get_collection()
        scheduler.add_job(lambda: run_embedding_sync(collection=collection), 'interval', hours=6, next_run_time=datetime.now())     
        print("📅 APScheduler started (every 6 hours)")
        try:
            scheduler.start()
        except KeyboardInterrupt:
            scheduler.shutdown()
            print("🛑 Scheduler stopped.")
