import os
import sys
import django

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "embedding_project.settings")
django.setup()

from matcher.db import get_all_documents, update_embedding_for_doc
from matcher.embeddings import encode_text


documents = get_all_documents()
total = len(documents)
updated_count = 0

for doc in documents:
    if "embedding" not in doc:
        title = doc.get("title", "")
        summary = doc.get("summary", "")
        combined_text = f"{title.strip()} {summary.strip()}".strip()

        if not combined_text:
            continue  # skip empty docs

        embedding = encode_text(combined_text).tolist()
        update_embedding_for_doc(doc["_id"], embedding)
        updated_count += 1

print(f"Processed {total} published documents. Updated {updated_count} with new embeddings.")

