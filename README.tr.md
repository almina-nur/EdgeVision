<div align="center">

# 🛰️ EdgeVision

**Havadan küçük nesne tespiti, kenar cihazlar için dürüstçe test edildi.**

YOLOv8 · ONNX (FP32 / FP16 / INT8) · FastAPI · React + TypeScript · PostgreSQL · MLflow · Prometheus

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)
![ONNX Runtime](https://img.shields.io/badge/ONNX-Runtime-005CED?logo=onnx&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-TypeScript-61DAFB?logo=react&logoColor=black)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)

<img src="assets/test_image.jpg" alt="EdgeVision VisDrone görseli üzerindeki tespitler" width="85%">

</div>

---

## Bu proje neden var?

Bir iş istasyonu GPU'sunda iyi sonuç veren bir model, kaynak kısıtlı bir cihazda genellikle çöküşe uğrar: daha düşük FPS, istikrarsız gecikme, daha yüksek bellek kullanımı ve küçük, uzaktaki nesnelerin gözden kaçması. Bu özellikle drone görüntüleri için geçerlidir.

EdgeVision, bu uçurumun mühendislik odaklı bir incelemesidir. Sadece [VisDrone](https://github.com/VisDrone/VisDrone-Dataset) üzerinde mAP kovalamak yerine, **doğruluk, gecikme, FPS ve model boyutunu bir arada** ölçer, model varyantları ve sayısal hassasiyetler arasında karşılaştırma yapar ve olumsuz sonuçları da raporlar.

## ✨ Öne Çıkanlar

| | |
|---|---|
| 🎯 **Tespit** | VisDrone üzerinde eğitilmiş YOLOv8n / YOLOv8s |
| ⚙️ **Dışa Aktarma & Niceleme** | PyTorch → ONNX FP32, FP16 ve INT8 (dinamik) |
| 📊 **Kıyaslama** | Format başına mAP50, FPS, gecikme ve bellek; sınıf düzeyi ve ışık koşulu analizleri |
| 🌐 **Web Paneli** | Görsel yükleyin, tuvale çizilen kutuları görün, kıyaslama tablolarına göz atın |
| 🔌 **REST API** | Etkileşimli dokümantasyon ve sağlık uç noktası içeren FastAPI servisi |
| 🧪 **MLOps Altyapısı** | Deney takibi için PostgreSQL + MLflow |
| 📈 **Gözlemlenebilirlik** | Prometheus `/metrics` uç noktası ve Grafana paneli |
| 🐳 **Tek Komutla Dağıtım** | Tüm yığın için Docker Compose |

## 🚀 Hızlı Başlangıç

**Gereksinimler:** Git, Compose içeren Docker ve Python 3 (sadece model indirme betiği için).

```bash
# 1. Klonlayın
git clone https://github.com/almina-nur/EdgeVision.git
cd EdgeVision

# 2. Sırları yapılandırın (.env dosyasını asla commit'lemeyin)
cp .env.example .env        # ardından şifreleri düzenleyin

# 3. v0.1.0 sürümünden eğitilmiş modelleri indirin
python download_models.py

# 4. Her şeyi başlatın
docker compose up --build
