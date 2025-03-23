FROM python:3.9-slim

WORKDIR /app

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Add a script to handle port environment variable
RUN echo '#!/bin/bash\nPORT=${PORT:-8080}\npython -m uvicorn app.main:app --host 0.0.0.0 --port $PORT' > start.sh && \
    chmod +x start.sh

# Add healthcheck
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl --fail http://localhost:8080/health || exit 1

# Use a script that properly handles the environment variable
CMD ["./start.sh"] 