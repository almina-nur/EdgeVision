"""EdgeVision - CLI çıkarım."""
import argparse
import json
import cv2
from src.api.model_loader import DetectionModel


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", required=True)
    parser.add_argument("--model", default="models/yolov8s_int8.onnx")
    parser.add_argument("--conf", type=float, default=0.25)
    args = parser.parse_args()

    image = cv2.imread(args.image)
    if image is None:
        raise SystemExit(f"Görüntü okunamadı: {args.image}")

    model = DetectionModel(args.model, conf_threshold=args.conf)
    detections, ms = model.predict(image)
    print(json.dumps({"inference_ms": round(ms, 2), "detections": detections}, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
