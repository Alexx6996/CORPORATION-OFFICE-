# Base image: Python 3.11 slim
FROM python:3.11-slim

# Disable buffering for Python logs
ENV PYTHONUNBUFFERED=1

# Workdir inside container
WORKDIR /app

# Copy dependency list first (for layer caching in future CI)
COPY requirements-ci.txt /app/requirements.txt

# Install build deps (if needed for wheels) and python deps
RUN apt-get update && apt-get install -y --no-install-recommends build-essential && \
    pip install --no-cache-dir -r /app/requirements.txt && \
    apt-get purge -y build-essential && apt-get autoremove -y && rm -rf /var/lib/apt/lists/*

# Copy the whole project
COPY . /app

# Expose the service port used by observability.metrics_app
EXPOSE 8001

# Default command:
# run the aioffice probe (healthz + metrics) via uvicorn
CMD ["uvicorn", "observability.metrics_app:app", "--host", "0.0.0.0", "--port", "8001"]
