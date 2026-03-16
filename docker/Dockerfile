# FROM python:3.13-slim

# WORKDIR /app

# # Install system dependencies needed by psycopg2 and other packages
# RUN apt-get update && apt-get install -y \
#     gcc \
#     libpq-dev \
#     && rm -rf /var/lib/apt/lists/*

# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# COPY src/ .

# # Setup user (not root)
# RUN mkdir -p /app/.cache/huggingface \
#     && adduser --disabled-password --no-create-home appuser \
#     && chown -R appuser:appuser /app

# # Cache models in /app
# ENV HF_HOME=/app/.cache/huggingface

# USER appuser

# EXPOSE 8000

# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# Stage 1: base
FROM python:3.13-slim AS base

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ .

RUN mkdir -p /app/.cache/huggingface \
    && adduser --disabled-password --no-create-home appuser \
    && chown -R appuser:appuser /app

ENV HF_HOME=/app/.cache/huggingface

# Stage 2: production
FROM base AS production

USER appuser
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# Stage 3: test
FROM base AS test

COPY requirements-tests.txt .
RUN pip install --no-cache-dir -r requirements-tests.txt

ENV PYTHONPATH=/app

USER appuser
CMD ["pytest", "tests/", "-v"]
