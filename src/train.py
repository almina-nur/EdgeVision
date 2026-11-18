"""
EdgeVision - Model Eğitim Modülü
Bu modül, VisDrone veri seti üzerinde YOLO modellerinin eğitimini gerçekleştirir.
Kullanım: python -m src.train --model yolov8n.pt --epochs 15
"""
import argparse
from ultralytics import YOLO

def main():
    # Komut satırı argümanlarını ayrıştır
    parser = argparse.ArgumentParser(description="EdgeVision Model Eğitimi")
    parser.add_argument("--model", default="yolov8n.pt", help="Kullanılacak YOLO modeli")
    parser.add_argument("--data", default="VisDrone.yaml", help="Veri seti yapılandırma dosyası")
    parser.add_argument("--epochs", type=int, default=15, help="Eğitim epoch sayısı")
    parser.add_argument("--imgsz", type=int, default=640, help="Giriş görüntü boyutu")
    parser.add_argument("--batch", type=int, default=16, help="Batch boyutu")
    parser.add_argument("--device", default="0", help="Kullanılacak cihaz (0=GPU, cpu=CPU)")
    parser.add_argument("--name", default="baseline_yolov8n_15ep", help="Deney adı")
    args = parser.parse_args()

    # Modeli yükle ve eğitimi başlat
    model = YOLO(args.model)
    model.train(
        data=args.data,
        epochs=args.epochs,
        imgsz=args.imgsz,
        batch=args.batch,
        device=args.device,
        project="EdgeVision",
        name=args.name,
        exist_ok=True,
    )

if __name__ == "__main__":
    main()
