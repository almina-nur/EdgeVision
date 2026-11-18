"""EdgeVision - Model ve veri seti indirme script'i.

Kullanım:
    python download_models.py            # Sadece modeller
    python download_models.py --all      # Modeller + veri seti
"""
import argparse
import os
import sys
import urllib.request

MODELS_DIR = "models"
MODEL_URLS = {
    "yolov8n_best.pt":    "https://github.com/almina-nur/EdgeVision/releases/download/v0.1.0/yolov8n_best.pt",
    "yolov8n_fp32.onnx":  "https://github.com/almina-nur/EdgeVision/releases/download/v0.1.0/yolov8n_fp32.onnx",
    "yolov8n_int8.onnx":  "https://github.com/almina-nur/EdgeVision/releases/download/v0.1.0/yolov8n_int8.onnx",
    "yolov8s_best.pt":    "https://github.com/almina-nur/EdgeVision/releases/download/v0.1.0/yolov8s_best.pt",
    "yolov8s_fp32.onnx":  "https://github.com/almina-nur/EdgeVision/releases/download/v0.1.0/yolov8s_fp32.onnx",
    "yolov8s_int8.onnx":  "https://github.com/almina-nur/EdgeVision/releases/download/v0.1.0/yolov8s_int8.onnx",
}


def download_file(url, dest):
    """Dosyayı indir; zaten varsa atla."""
    if os.path.exists(dest) and os.path.getsize(dest) > 0:
        size_mb = os.path.getsize(dest) / (1024 * 1024)
        print(f"  ✓ {os.path.basename(dest)} zaten var ({size_mb:.2f} MB)")
        return True

    print(f"  ↓ İndiriliyor: {os.path.basename(dest)}")
    try:
        urllib.request.urlretrieve(url, dest)
        size_mb = os.path.getsize(dest) / (1024 * 1024)
        print(f"  ✓ Tamamlandı ({size_mb:.2f} MB)")
        return True
    except Exception as e:
        print(f"  ✗ Hata: {e}")
        return False


def download_models():
    """Tüm modelleri indir."""
    os.makedirs(MODELS_DIR, exist_ok=True)
    print(f"\n📦 Modeller indiriliyor -> {MODELS_DIR}/")
    print("=" * 60)

    success = 0
    for filename, url in MODEL_URLS.items():
        dest = os.path.join(MODELS_DIR, filename)
        if download_file(url, dest):
            success += 1

    print("=" * 60)
    print(f"✓ {success}/{len(MODEL_URLS)} model hazır")
    return success == len(MODEL_URLS)


def download_dataset():
    """VisDrone veri setini indir (Ultralytics otomatik indirir)."""
    print("\n📥 VisDrone veri seti kontrol ediliyor...")
    try:
        from ultralytics import YOLO
        # Küçük bir eğitim başlatarak veri setini indir
        model = YOLO("yolov8n.pt")
        model.train(
            data="VisDrone.yaml", epochs=1, imgsz=640, batch=16,
            device="cpu", project="EdgeVision", name="_dataset_warmup",
            exist_ok=True,
        )
        print("✓ VisDrone veri seti hazır")
    except Exception as e:
        print(f"⚠️ Veri seti indirilemedi: {e}")
        print("  Not: Sadece inference için gerekli değil, atlayabilirsiniz.")


def main():
    parser = argparse.ArgumentParser(description="EdgeVision model/veri indirici")
    parser.add_argument("--all", action="store_true", help="Model + veri seti")
    parser.add_argument("--dataset", action="store_true", help="Sadece veri seti")
    args = parser.parse_args()

    if not args.dataset:
        ok = download_models()
        if not ok:
            sys.exit(1)

    if args.all or args.dataset:
        download_dataset()

    print("\n✅ İşlem tamamlandı. Şimdi: docker compose up --build")


if __name__ == "__main__":
    main()
