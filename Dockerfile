FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y libglib2.0-0 libsm6 libxext6 libxrender1 libgomp1 && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ ./src/
COPY models/ ./models/
ENV MODEL_PATH=models/yolov8s_int8.onnx
ENV PYTHONUNBUFFERED=1
EXPOSE 8000
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
