"""
EdgeVision - FastAPI Sunucusu (Production Grade)
"""
import os
from contextlib import asynccontextmanager
from pathlib import Path
from fastapi.concurrency import run_in_threadpool

import cv2
import numpy as np
from fastapi import FastAPI, File, HTTPException, UploadFile, Response, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import generate_latest, Counter, Histogram

from .model_loader import DetectionModel
from .schemas import PredictionResponse
from .database import SessionLocal, PredictionLog

MODEL_PATH = os.getenv("MODEL_PATH", "models/yolov8n_fp32.onnx")
API_KEY = os.getenv("API_KEY", "edgevision-secret-key")
model = None

# Prometheus Metrikleri
REQUEST_COUNT = Counter("edgevision_requests_total", "Toplam istek sayisi", ["endpoint"])
REQUEST_LATENCY = Histogram("edgevision_request_latency_seconds", "Istek gecikmesi", ["endpoint"])

def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Gecersiz API Key")

@asynccontextmanager
async def lifespan(app: FastAPI):
    global model
    print(f"Model yukleniyor: {MODEL_PATH}")
    model = DetectionModel(MODEL_PATH)
    print("Model hazir.")
    yield
    model = None

app = FastAPI(title="EdgeVision API", version="1.1.0", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": model is not None}

@app.get("/metrics")
def metrics():
    return Response(content=generate_latest(), media_type="text/plain")

@app.post("/predict", response_model=PredictionResponse, dependencies=[Depends(verify_api_key)])
async def predict(file: UploadFile = File(...)):
    REQUEST_COUNT.labels(endpoint="/predict").inc()
    with REQUEST_LATENCY.labels(endpoint="/predict").time():
        if model is None:
            raise HTTPException(status_code=503, detail="Model yuklenmedi")
        
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if image is None:
            raise HTTPException(status_code=400, detail="Gecersiz goruntu formati")
            
        # Asenkron yapı: Ağır çıkarım işlemini thread pool'a gönder
        detections, inference_ms = await run_in_threadpool(model.predict, image)
        
        h, w = image.shape[:2]
        
        # Veritabanına logla
        try:
            db = SessionLocal()
            log = PredictionLog(
                model_name=Path(MODEL_PATH).name,
                inference_ms=inference_ms,
                detection_count=len(detections),
                image_width=w,
                image_height=h
            )
            db.add(log)
            db.commit()
            db.close()
        except Exception as e:
            print(f"DB Log Hatasi: {e}")
        
        return PredictionResponse(
            detections=detections,
            inference_ms=round(inference_ms, 2),
            image_width=w,
            image_height=h,
            model=Path(MODEL_PATH).name,
        )
