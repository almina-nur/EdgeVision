# EdgeVision

**Intelligent Aerial Perception & Edge AI Platform**

## Hızlı Başlangıç

### 1. Repoyu klonla

git clone https://github.com/almina-nur/EdgeVision.git
cd EdgeVision

### 2. Modelleri indir

python download_models.py

### 3. Docker ile başlat

docker compose up --build

### 4. Uygulamayı Tarayıcıda Aç 🚀

Docker başladıktan sonra tarayıcınızda şu adresleri açın:

| Ne? | Adres |
|-----|-------|
| 🎨 Web Arayüzü | http://localhost:3000 |
| 📚 API Dokümantasyonu | http://localhost:8000/docs |
| ❤️ Sistem Sağlığı | http://localhost:8000/health |

> Not: Docker terminali açık kalmalıdır. Arka planda çalıştırmak için: docker compose up -d

## Projenin Amacı

Bu proje, İHA'lardan alınan görüntülerde insan, araç ve diğer nesneleri tespit edebilen; kaynakları kısıtlı uç cihazlarda (Edge AI) maksimum verimlilikle çalışmayı hedefleyen bir yapay zekâ platformudur.

## Karşılaştırma Tablosu

| Model | Format | Boyut (MB) | mAP50 |
|---|---|---|---|
| YOLOv8n | PyTorch | 6.18 | 0.2754 |
| YOLOv8n | ONNX FP32 | 12.19 | 0.2658 |
| YOLOv8n | ONNX INT8 | 3.32 | 0.2545 |
| YOLOv8s | PyTorch | 21.46 | 0.3555 |
| YOLOv8s | ONNX FP32 | 42.69 | 0.3523 |
| YOLOv8s | ONNX INT8 | 10.96 | 0.3401 |
