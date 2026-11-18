# EdgeVision

**Intelligent Aerial Perception & Edge AI Platform**

## Projenin Amacı

Bu proje, İHA'lardan (İnsansız Hava Araçları) alınan yüksek çözünürlüklü görüntülerde insan, araç ve diğer nesneleri tespit edebilen; ancak bunu yaparken yüksek işlem gücüne sahip sunuculara bağımlı kalmayan, aksine kaynakları kısıtlı uç cihazlarda (Edge AI) maksimum verimlilikle çalışmayı hedefleyen bir yapay zekâ platformudur.

Bizim için mesele sadece bir YOLO modelini eğitip yüksek doğruluk (mAP) almak değil; aynı zamanda o modelin gecikmesini (latency), saniyedeki kare hızını (FPS), bellek tüketimini ve farklı donanım formatlarındaki (FP32, FP16, INT8, TensorRT) davranışını bilimsel ve ölçülebilir deneylerle analiz etmektir.

## Çözdüğümüz Problem

Yüksek işlem gücüne sahip bir bilgisayarda yüksek doğrulukla çalışan bir model, düşük kaynaklı bir uç cihazda aynı performansı göstermeyebilir. Model yüksek FPS'e ulaşamayabilir, bellek tüketimi artabilir, görüntü işleme gecikebilir veya küçük/uzaktaki nesneler kaçırılabilir.

Bu projede, bu problemleri karşılaştırmalı benchmark'lar, parçalı çıkarım (tile inference) ve donanım hızlandırma teknikleriyle çözmeyi hedefliyoruz.

## Öne Çıkan Teknik Bulgular

1. FP16, Edge Cihazlarda FP32'den 2 Kat Daha Hızlı ve Stabil: Uç cihaz simülasyonunda (1 CPU thread) FP32 modeli 4.66 FPS alırken ve gecikmesi 737 ms'ye kadar çıkarken (tutarsız), FP16 modeli 9.04 FPS hızında ve 123 ms stabil bir gecikmeyle çalışmıştır.
2. INT8 Dinamik Kuantalama, VNNI Olmayan CPU'larda Yavaşlatıyor: Model boyutunu %72 küçültmesine rağmen, donanımsal VNNI desteği olmayan genel amaçlı CPU'larda INT8 model, dekuantalizasyon maliyeti nedeniyle hızı düşürmektedir.
3. VisDrone'da Küçük Nesne Sorunu Hâlâ Ciddi: Büyük nesnelerde mAP50 0.535 iken, küçük nesnelerde bu oran 0.168'e kadar düşmektedir. Bu sorunu aşmak için projede Tile-Based Inference (SAHI) mimarisi desteklenmektedir.

## Karşılaştırma Tablosu

| Model | Format | Boyut (MB) | mAP50 | FPS (CPU) | FPS (Edge) |
|---|---|---|---|---|---|
| YOLOv8n | PyTorch | 6.18 | 0.2754 | - | - |
| YOLOv8n | ONNX FP32 | 12.19 | 0.2658 | 7.25 | 4.66 |
| YOLOv8n | ONNX FP16 | 6.13 | 0.2655 | 8.93 | 9.04 |
| YOLOv8n | ONNX INT8 | 3.32 | 0.2545 | 1.23 | 1.29 |
| YOLOv8s | PyTorch | 21.46 | 0.3555 | - | - |
| YOLOv8s | ONNX FP32 | 42.69 | 0.3523 | 2.81 | 2.62 |
| YOLOv8s | ONNX FP16 | 21.38 | 0.3491 | 2.82 | - |
| YOLOv8s | ONNX INT8 | 10.96 | 0.3401 | 0.43 | 0.45 |

## Geliştirilen Özellikler

- Data Pipeline: VisDrone veri seti yönetimi.
- Object Detection: YOLOv8 ailesi (n ve s modelleri).
- Model Benchmark: Farklı formatların doğruluk, hız ve bellek karşılaştırması.
- Edge Optimization: ONNX FP32/FP16/INT8 and TensorRT Export.
- Real-Time Inference: Video üzerinden gerçek zamanlı tespit ve FPS ölçümü.
- Advanced Inference: Tile-Based Inference (SAHI) ile küçük nesne kaybını azaltma.
- Monitoring: Prometheus formatında /metrics endpoint'i.
- API: FastAPI ile asenkron çıkarım servisi.
- Dashboard: React + TypeScript ile görselleştirme.
- Deployment: Docker Compose ile tek komutta kalkış.

## Hızlı Başlangıç

```bash
git clone https://github.com/almina-nur/EdgeVision.git
cd EdgeVision
docker compose up --build
```


## Yol Haritası (Gelecek Çalışmalar)

Rapor doğrultusunda öncelikli geliştirme adımları:
- [ ] Gerçek donanım (Jetson Orin Nano) üzerinde TensorRT testleri.
- [ ] MLflow ile deney takibi ve model versiyonlama.
- [ ] Statik INT8 quantization ve QAT (Quantization Aware Training) karşılaştırması.
- [ ] PostgreSQL ile çıkarım loglarının tutulması.
