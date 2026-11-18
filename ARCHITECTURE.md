# EdgeVision - Proje Mimarisi

Bu dosya, projedeki her klasörün ve dosyanın ne işe yaradığını açıklar.

## models/
Eğitilmiş model dosyaları. İki model (YOLOv8n, YOLOv8s) ve dört format (PyTorch, ONNX FP32, FP16, INT8) bulunur.

| Dosya | Açıklama |
|---|---|
| yolov8n_best.pt | YOLOv8n PyTorch ağırlıkları |
| yolov8n_fp32.onnx | FP32 ONNX modeli |
| yolov8n_fp16.onnx | FP16 ONNX modeli (Edge için en iyi seçim) |
| yolov8n_int8.onnx | INT8 ONNX modeli |
| yolov8s_* | YOLOv8s varyantları (daha yüksek doğruluk, daha yavaş) |

## src/
Kaynak kodlar.

| Dosya | Açıklama |
|---|---|
| train.py | Model eğitimi |
| export_onnx.py | ONNX export ve INT8 quantization |
| export_tensorrt.py | TensorRT export (NVIDIA Jetson için) |
| inference.py | Tek görüntü çıkarımı |
| video_inference.py | Video üzerinden tespit ve FPS ölçümü |
| benchmark.py | FPS, gecikme ve bellek ölçümü |
| tile_inference.py | Tile-Based Inference (SAHI mantığı) |
| api/database.py | PostgreSQL bağlantısı ve loglama (SQLAlchemy) |
| api/main.py | FastAPI servisi (/predict, /stats, /metrics, /health) |
| api/model_loader.py | ONNX Runtime model yükleme ve ön/son işleme |
| api/schemas.py | Pydantic veri şemaları |

## frontend/
React ve TypeScript dashboard.

| Dosya | Açıklama |
|---|---|
| src/App.tsx | Ana sayfa, sekme sistemi |
| src/components/ImageUploader.tsx | Görüntü yükleme alanı |
| src/components/DetectionCanvas.tsx | Tespit kutularını çizme |
| src/components/Stats.tsx | Benchmark tabloları |

## results/
Deney sonuçları.

| Dosya | Açıklama |
|---|---|
| comparison_table_full.csv | 8 format karşılaştırması |
| benchmark_results.csv | Normal CPU benchmark sonuçları |
| edge_benchmark.csv | Edge simülasyonu (1-thread CPU) |
| class_analysis.csv | Sınıf bazında mAP değerleri |
| light_conditions.csv | Işık koşulları dağılımı |
| figures/ | 7 adet grafik (PNG) |

## tests/
Pytest testleri.

| Dosya | Açıklama |
|---|---|
| test_api.py | API testleri |
| test_hardware.py | Donanım doğrulama testleri |

## Kök Dizin

| Dosya | Açıklama |
|---|---|
| Dockerfile | Multi-stage, non-root (appuser), healthcheck içerir. |
| docker-compose.yml | Backend, frontend, PostgreSQL, MLflow, Prometheus, Grafana |
| prometheus.yml | Prometheus konfigürasyonu |
| requirements.txt | Python bağımlılıkları |
| README.md | Proje tanıtımı (İngilizce) |
| README.tr.md | Proje tanıtımı (Türkçe) |
| ARCHITECTURE.md | Bu dosya |
| GETTING_STARTED.md | Kurulum kılavuzu |

## İstek Akışı
1. Kullanıcı tarayıcıda görüntü yükler.
2. React, FastAPI'ye POST /api/predict isteği gönderir.
3. FastAPI, ONNX Runtime ile çıkarım yapar (asenkron thread pool).
4. Sonuç veritabanına (PostgreSQL) loglanır.
5. Sonuç JSON olarak React'e döner.
6. React, tespit kutularını canvas üzerine çizer.
