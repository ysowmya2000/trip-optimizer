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

# Pre-warm both ML models into the image at build time instead of on the
# first live request. Without this, ChromaDB's default embedding function
# (all-MiniLM-L6-v2 ONNX, ~79MB) and the cross-encoder reranker both
# download from the network on first use - discovered by reproducing a
# free-tier deploy crash locally with `docker run --memory=512m`: the first
# real trip request triggered both downloads plus two separate ML runtimes
# (onnxruntime + full PyTorch) initializing concurrently, OOM-killing the
# container mid-request. Baking the weights in at build time removes the
# live-download spike; it doesn't eliminate the models' resident memory
# once loaded, but that alone was enough to keep it under 512MB in testing.
RUN python -c "\
from app.db.vector_store import travel_kb; \
travel_kb.search(query='warm up', n_results=1); \
from sentence_transformers import CrossEncoder; \
CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2').predict([('warm up', 'warm up')])"

# Cap BLAS/OMP thread counts - default multi-threaded matrix ops from
# onnxruntime/PyTorch spike peak memory on tiny containers; single-threaded
# is slower per-inference but keeps peak RSS well under free-tier limits.
ENV OMP_NUM_THREADS=1
ENV OPENBLAS_NUM_THREADS=1
ENV MKL_NUM_THREADS=1

ENV PORT=8000
EXPOSE 8000

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT}"]
