[English](README.md) | [Türkçe](README.tr.md)

# EdgeVision - Türkçe

**Intelligent Aerial Perception & Edge AI Platform**

## Projenin Amacı
Bu proje, İHA'lardan alınan görüntülerde insan, araç ve diğer nesneleri tespit edebilen; ancak bunu yaparken yüksek işlem gücüne sahip sunuculara bağımlı kalmayan, aksine kaynakları kısıtlı uç cihazlarda (Edge AI) maksimum verimlilikle çalışmayı hedefleyen bir platformdur.

## Çözdüğümüz Problem
Yüksek işlem gücüne sahip bir bilgisayarda yüksek doğrulukla çalışan bir model, düşük kaynaklı bir uç cihazda aynı performansı göstermeyebilir. Bu projede, bu problemleri karşılaştırmalı benchmark'lar ve donanım hızlandırma teknikleriyle çözmeyi hedefliyoruz.

## Temel Bulgu
YOLOv8n FP16 modeli, edge simülasyonunda (1 CPU thread) FP32 modelinden 2 kat daha hızlı ve çok daha stabil çalışır.

## Karşılaştırma Tablosu
| Model | Format | Boyut (MB) | mAP50 | FPS (CPU) |
|---|---|---|---|---|
| YOLOv8n | ONNX FP32 | 12.19 | 0.2658 | 7.25 |
| YOLOv8n | ONNX FP16 | 6.13 | 0.2655 | 8.93 |
| YOLOv8n | ONNX INT8 | 3.32 | 0.2545 | 1.23 |

## Hızlı Başlangıç
```bash
git clone https://github.com/almina-nur/EdgeVision.git
docker compose up --build
```
