"""
EdgeVision - FastAPI Sunucusu
Bu modül, eğitilmiş modeli bir web servisi olarak sunar.
/predict endpoint'i görüntü alır, tespit yapar ve JSON döner.
"""
import os
from contextlib import asynccontextmanager
from pathlib import Path

import cv2
import numpy as np
import pandas as pd
from fastapi import FastAPI, File, HTTPException, UploadFile, Response
from prometheus_client import generate_latest, Counter, Histogram
from fastapi.middleware.cors import CORSMiddleware

from .model_loader import DetectionModel
from .schemas import PredictionResponse

MODEL_PATH = os.getenv("MODEL_PATH", "models/yolov8n_fp16.onnx")
model = None

# Prometheus Metrikleri
REQUEST_COUNT = Counter("edgevision_requests_total", "Toplam istek sayisi", ["endpoint"])
REQUEST_LATENCY = Histogram("edgevision_request_latency_seconds", "Istek gecikmesi", ["endpoint"])


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Sunucu başlarken modeli belleğe yükler."""
    global model
    print(f"Model yükleniyor: {MODEL_PATH}")
    model = DetectionModel(MODEL_PATH)
    print("Model hazır.")
    yield
    model = None

# Prometheus Metrikleri
REQUEST_LATENCY = Histogram("edgevision_request_latency_seconds", "Istek gecikmesi", ["endpoint"])


app = FastAPI(title="EdgeVision API", version="1.0.0", lifespan=lifespan)

# CORS ayarları (Frontend'in erişebilmesi için)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": model is not None}

@app.get("/model/info")
def model_info():
    if model is None:
        raise HTTPException(status_code=503, detail="Model yüklenmedi")
    return {"path": MODEL_PATH, "classes": model.class_names}

@app.get("/stats")
def stats():
    """Benchmark ve analiz sonuçlarını döndürür."""
    results = {}
    base_dir = Path(__file__).parent.parent.parent

    for name, filename in [
        ("comparison", "comparison_table_full.csv"),
        ("benchmark", "benchmark_results.csv"),
        ("edge_benchmark", "edge_benchmark.csv"),
        ("class_analysis", "class_analysis.csv"),
        ("light_conditions", "light_conditions.csv"),
    ]:
        path = base_dir / "results" / filename
        if path.exists():
            results[name] = pd.read_csv(path).to_dict(orient="records")

    return results


@app.get("/metrics")
def metrics():
    """Prometheus formatında uç nokta."""
    return Response(content=generate_latest(), media_type="text/plain")

@app.post("/predict", response_model=PredictionResponse)
async def predict(file: UploadFile = File(...)):
    """Yüklenen görüntü üzerinde nesne tespiti yapar."""
    REQUEST_COUNT.labels(endpoint="/predict").inc()
    with REQUEST_LATENCY.labels(endpoint="/predict").time():
        if model is None:
            raise HTTPException(status_code=503, detail="Model yüklenmedi")
            
        contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if image is None:
        raise HTTPException(status_code=400, detail="Geçersiz görüntü formatı")
        
    detections, inference_ms = model.predict(image)
    h, w = image.shape[:2]
    
    return PredictionResponse(
        detections=detections,
        inference_ms=round(inference_ms, 2),
        image_width=w,
        image_height=h,
        model=Path(MODEL_PATH).name,
    )
