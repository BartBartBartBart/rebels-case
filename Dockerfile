# Base image — Python version
FROM python:3.13-slim

# Set working directory inside container
WORKDIR /app

# Copy and install dependencies first (layer caching — faster rebuilds)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

# Setup an app user so the container doesn't run as the root user
RUN mkdir -p /app/.cache/huggingface \
    && adduser --disabled-password --no-create-home appuser \
    && chown -R appuser:appuser /app

# Cache models in /app
ENV HF_HOME=/app/.cache/huggingface

USER appuser

# Expose the port
EXPOSE 8000

# Command to run the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]