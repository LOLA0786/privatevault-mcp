FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY pyproject.toml .
RUN pip install --no-cache-dir -e .

# Copy source
COPY src/ ./src/
COPY alembic.ini .

# Expose FastAPI + MCP ports
EXPOSE 8000 8080

# Run with uvicorn (production ready with --workers)
CMD ["uvicorn", "privatevault_mcp.api.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
EOF