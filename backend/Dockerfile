FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY Procfile ./Procfile

# Bundle the pre-built ChromaDB corpus into the image at build time - see
# README's deployment notes for why (Railway's free tier filesystem isn't
# guaranteed to persist across redeploys, and re-seeding needs live Google
# Places API calls we're avoiding). The travel_knowledge collection is
# already committed to the repo under data/chroma.
COPY data ./data

ENV PORT=8000
EXPOSE 8000

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT}"]
