# EdgeVision — Proje Mimarisi

Bu dosya, projedeki her klasörün ve dosyanın ne işe yaradığını açıklar.

## Klasör Yapısı

### models/ — Eğitilmiş Modeller
| Dosya | Ne? | Ne Zaman Kullanılır? |
|---|---|---|
| yolov8n_best.pt | YOLOv8n PyTorch | Yeniden export için |
| yolov8n_fp32.onnx | FP32 ONNX (12.19 MB) | Baseline |
| yolov8n_fp16.onnx | FP16 ONNX (6.13 MB) | Edge için en iyi |
| yolov8n_int8.onnx | INT8 ONNX (3.32 MB) | Bellek kısıtlı |
| yolov8s_* | Aynı formatlar, büyük model | Yüksek doğruluk |

### src/ — Kaynak Kod
| Dosya | Ne Yapar? |
|---|---|
| train.py | Model eğitimi |
| export_onnx.py | ONNX export + quantization |
| inference.py | Tek görüntü çıkarımı |
| video_inference.py | Video tespiti + FPS |
| benchmark.py | FPS/latency/memory |
| api/main.py | FastAPI servisi |

### frontend/ — React Dashboard
| Dosya | Ne Yapar? |
|---|---|
| src/App.tsx | Ana sayfa, tab sistemi |
| src/components/ImageUploader.tsx | Görüntü yükleme |
| src/components/DetectionCanvas.tsx | Bounding box çizimi |
| src/components/Stats.tsx | Benchmark tabloları |

### results/ — Deney Sonuçları
| Dosya | Ne İçerir? |
|---|---|
| comparison_table_full.csv | 8 format karşılaştırması |
| benchmark_results.csv | FPS/latency/memory |
| edge_benchmark.csv | Edge simülasyonu |
| class_analysis.csv | Sınıf bazında mAP |
| light_conditions.csv | Işık koşulları |
| figures/*.png | 7 grafik |

### Kök Dizin
| Dosya | Ne Yapar? |
|---|---|
| Dockerfile | Backend container |
| docker-compose.yml | Backend + Frontend |
| requirements.txt | Python bağımlılıkları |
| README.md | Proje tanıtımı |
| ARCHITECTURE.md | Bu dosya |

## Akış

Kullanıcı tarayıcıda görüntü yükler → React, FastAPI'ye istek atar → FastAPI, ONNX modeliyle tespit yapar → Sonuç React'e döner → Canvas üzerine çizilir.
