FROM python:3.11-slim

WORKDIR /app

# OpenCV için sistem bağımlılıkları (garantiye alalım)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libgomp1 \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ZORLA: opencv-python'ı kaldır, headless kur (libGL sorununu kesin çözer)
RUN pip uninstall -y opencv-python opencv-contrib-python opencv-python-headless && \
    pip install --no-cache-dir opencv-python-headless

COPY src ./src
COPY models ./models

ENV MODEL_PATH=models/yolov8s_int8.onnx
ENV PYTHONPATH=/app

EXPOSE 8000

CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
