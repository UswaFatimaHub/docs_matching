# Dockerfile
FROM python:3.12.4-slim-bullseye

# Set workdir
WORKDIR /app

# Install build tools and git (for some pip deps)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential git && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# # Load env vars and preload model
# RUN python -c "\
# import os; \
# from dotenv import load_dotenv; \
# load_dotenv(); \
# from sentence_transformers import SentenceTransformer; \
# model = SentenceTransformer(os.getenv('SENTENCE_TRANSFORMER_MODEL', 'sentence-transformers/LaBSE'))"



# Run using gunicorn
CMD ["gunicorn", "embedding_project.wsgi:application", "--bind", "0.0.0.0:8000", "--workers=2"]

# # Expose the port Django runs on
# EXPOSE 8000

# # Default command (runserver + optional cron)
# CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000 && python manage.py runapscheduler"]
