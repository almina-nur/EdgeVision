FROM python:3.11-slim-bookworm

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends libgomp1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements-api.txt .
RUN pip install --no-cache-dir -r requirements-api.txt

RUN useradd -m -u 1000 appuser
COPY src/ ./src/
COPY models/ ./models/

USER appuser

ENV MODEL_PATH=models/yolov8n_fp32.onnx
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

HEALTHCHECK --interval=5s --timeout=5s --start-period=10s --retries=12 \
  CMD ["python", "-c", "from urllib.request import urlopen; urlopen('http://127.0.0.1:8000/health', timeout=4).close()"]

CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
