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
COPY . /app/

# Preload model
RUN python scripts/download_model.py


COPY entrypoint.sh /app/
RUN chmod +x /app/entrypoint.sh
CMD ["/app/entrypoint.sh"]
