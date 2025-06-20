# matcher/management/commands/runapscheduler.py

from django.core.management.base import BaseCommand
from apscheduler.schedulers.blocking import BlockingScheduler
from matcher.embeddings import encode_text
from matcher.db import get_documents_without_embeddings_batch, update_embedding_for_doc
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# def run_embedding_sync():
#     print("🔁 Running embedding sync job...")

#     docs = get_documents_without_embeddings()
#     updated = 0

#     for doc in docs:
#         if "embedding" not in doc:
#             text = f"{doc.get('title', '')} {doc.get('summary', '')}".strip()
#             if not text:
#                 continue
#             emb = encode_text(text).tolist()
#             update_embedding_for_doc(doc["_id"], emb)
#             updated += 1

#     print(f"✅ Finished embedding sync. Updated {updated} documents.")


def run_embedding_sync(batch_size=1000):
    logger.info("🌀 Starting embedding sync...")
    print(f"🔁 [{datetime.now()}] Running embedding sync job...")
    updated_count = 0
    skip = 0

    while True:
        docs = get_documents_without_embeddings_batch(skip=skip, limit=batch_size)
        if not docs:
            break

        for doc in docs:
            text = f"{doc.get('title', '')} {doc.get('summary', '')}".strip()
            if not text:
                continue
            embedding = encode_text(text).tolist()
            update_embedding_for_doc(doc["_id"], embedding)
            updated_count += 1

        skip += batch_size  # Move to next batch
    logger.info(f"✅ Sync complete. {updated_count} documents updated.")
    print(f"✅ [{datetime.now()}] Sync completed. Updated {updated_count} documents.")




class Command(BaseCommand):
    help = "Run APScheduler"

    def handle(self, *args, **options):
        scheduler = BlockingScheduler()
        scheduler.add_job(run_embedding_sync, 'interval', hours=6, next_run_time=datetime.now())
        print("📅 APScheduler started (every 6 hours)")
        try:
            scheduler.start()
        except KeyboardInterrupt:
            scheduler.shutdown()
            print("🛑 Scheduler stopped.")
