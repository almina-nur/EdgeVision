%%writefile README.md
<div align="center">

# 🛰️ EdgeVision

**Aerial small-object detection, benchmarked honestly for the edge.**

YOLOv8 · ONNX (FP32 / FP16 / INT8) · FastAPI · React + TypeScript · PostgreSQL · MLflow · Prometheus

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)
![ONNX Runtime](https://img.shields.io/badge/ONNX-Runtime-005CED?logo=onnx&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-TypeScript-61DAFB?logo=react&logoColor=black)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)

[Quick start](#-quick-start) · [Results](#-results) · [Architecture](#-architecture) · [Roadmap](#-roadmap) · [Türkçe](README.tr.md)

<img src="assets/test_image.jpg" alt="EdgeVision detections on a VisDrone image" width="85%">

</div>

---

## Why this project exists

A model that scores well on a workstation GPU often falls apart on a resource-constrained device: lower FPS, unstable latency, higher memory use, and small, distant objects slipping through. This is especially true for drone imagery.

EdgeVision is an engineering study of that gap. Instead of only chasing mAP on [VisDrone](https://github.com/VisDrone/VisDrone-Dataset), it measures **accuracy, latency, FPS, and model size together**, across model variants and numeric precisions, and reports negative results too.

## ✨ Highlights

| | |
|---|---|
| 🎯 **Detection** | YOLOv8n / YOLOv8s trained on VisDrone |
| ⚙️ **Export & quantization** | PyTorch → ONNX FP32, FP16 and INT8 (dynamic) |
| 📊 **Benchmarking** | mAP50, FPS, latency and memory per format, plus class-level and lighting-condition analysis |
| 🌐 **Web dashboard** | Upload an image, see boxes drawn on a canvas, browse benchmark tables |
| 🔌 **REST API** | FastAPI service with interactive docs and a health endpoint |
| 🧪 **MLOps stack** | PostgreSQL + MLflow for experiment tracking |
| 📈 **Observability** | Prometheus `/metrics` endpoint and a Grafana dashboard |
| 🐳 **One-command deploy** | Docker Compose for the whole stack |

## 🚀 Quick start

**Requirements:** Git, Docker with Compose, and Python 3 (only for the model download script).

```bash
# 1. Clone
git clone https://github.com/almina-nur/EdgeVision.git
cd EdgeVision

# 2. Configure secrets (never commit .env)
cp .env.example .env        # then edit the passwords

# 3. Download trained models from the v0.1.0 release
python download_models.py

# 4. Launch everything
docker compose up --build

flowchart LR
    U([User]) --> FE[React + TypeScript<br/>dashboard]
    FE -->|HTTP| API[FastAPI backend]

    subgraph Inference
        API --> PRE[Preprocess] --> ORT[ONNX Runtime<br/>YOLOv8] --> POST[Postprocess + NMS]
    end

    POST --> API
    API --> DB[(PostgreSQL)]
    API -->|tracking| ML[MLflow]
    ML --> DB
    PROM[Prometheus] -->|scrapes /metrics| API
    GRAF[Grafana] --> PROM
