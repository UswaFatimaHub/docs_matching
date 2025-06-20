# matcher/management/commands/runapscheduler.py

from django.core.management.base import BaseCommand
from apscheduler.schedulers.blocking import BlockingScheduler
from matcher.embeddings import encode_text
from matcher.db import get_documents_without_embeddings, update_embedding_for_doc
from datetime import datetime

def run_embedding_sync():
    print("🔁 Running embedding sync job...")

    docs = get_documents_without_embeddings()
    updated = 0

    for doc in docs:
        if "embedding" not in doc:
            text = f"{doc.get('title', '')} {doc.get('summary', '')}".strip()
            if not text:
                continue
            emb = encode_text(text).tolist()
            update_embedding_for_doc(doc["_id"], emb)
            updated += 1

    print(f"✅ Finished embedding sync. Updated {updated} documents.")

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
