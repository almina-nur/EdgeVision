# --- Builder Aşaması ---
FROM python:3.11-slim AS builder

WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libglib2.0-0 libsm6 libxext6 libxrender1 libgomp1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# --- Runtime Aşaması ---
FROM python:3.11-slim

WORKDIR /app

# Non-root kullanıcı oluştur
RUN useradd -m -u 1000 appuser

# Sadece çalışması için gerekli kütüphaneler
RUN apt-get update && apt-get install -y --no-install-recommends \
    libglib2.0-0 libsm6 libxext6 libxrender1 libgomp1 \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .
RUN pip install --no-cache /wheels/*

# Uygulama kodlarını ve modelleri kopyala
COPY src/ ./src/
COPY models/ ./models/

# Kullanıcıya yetki ver
RUN chown -R appuser:appuser /app
USER appuser

ENV MODEL_PATH=models/yolov8n_fp16.onnx
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
