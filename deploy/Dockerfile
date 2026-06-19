# Qalqan AI — backend image for VPS (Hetzner CX22 etc.)
# Long-lived process: real cron, warm cache, no serverless cold starts.
FROM python:3.11-slim

WORKDIR /app

# System libs for matplotlib/reportlab PDF report generation (lazy-imported)
RUN apt-get update && apt-get install -y --no-install-recommends \
        libfreetype6 fonts-dejavu-core curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps first for layer caching
COPY api/requirements.txt ./api/requirements.txt
RUN pip install --no-cache-dir -r api/requirements.txt \
        "gunicorn>=22.0" "uvicorn[standard]>=0.29"

# App code (only api/ is needed at runtime — data files load relative to it)
COPY api ./api

ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
    CMD curl -fsS http://localhost:8000/health || exit 1

# 2 workers is plenty for a CX22 (2 vCPU). UvicornWorker = async FastAPI.
CMD ["gunicorn", "api.index:app", \
     "-k", "uvicorn.workers.UvicornWorker", \
     "-w", "2", "-b", "0.0.0.0:8000", \
     "--timeout", "120", "--graceful-timeout", "30", \
     "--access-logfile", "-"]
