"""EdgeVision - Video üzerinden gerçek zamanlı nesne tespiti."""
import argparse
import time
import cv2
from src.api.model_loader import DetectionModel


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", required=True)
    parser.add_argument("--model", default="models/yolov8s_int8.onnx")
    parser.add_argument("--output", default="output_video.mp4")
    parser.add_argument("--conf", type=float, default=0.25)
    parser.add_argument("--max-frames", type=int, default=0)
    args = parser.parse_args()

    model = DetectionModel(args.model, conf_threshold=args.conf)
    cap = cv2.VideoCapture(args.video)
    if not cap.isOpened():
        raise SystemExit(f"Video açılamadı: {args.video}")

    fps_in = cap.get(cv2.CAP_PROP_FPS)
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"Video: {w}x{h} @ {fps_in:.1f} FPS, {total} kare")

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(args.output, fourcc, fps_in, (w, h))

    frame_count = 0
    total_ms = 0.0
    total_det = 0
    t_start = time.perf_counter()

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        detections, ms = model.predict(frame)
        total_ms += ms
        total_det += len(detections)
        for det in detections:
            x, y, bw, bh = det["bbox"]
            cv2.rectangle(frame, (x, y), (x + bw, y + bh), (0, 255, 0), 2)
            label = f"{det['class_name']} {det['confidence']:.2f}"
            cv2.putText(frame, label, (x, y - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        out.write(frame)
        frame_count += 1
        if frame_count % 10 == 0:
            print(f"  Kare: {frame_count}/{total}")
        if args.max_frames > 0 and frame_count >= args.max_frames:
            break

    elapsed = time.perf_counter() - t_start
    cap.release()
    out.release()

    print(f"\n{'='*60}")
    print(f"Video Inference Sonuçları")
    print(f"{'='*60}")
    print(f"İşlenen kare: {frame_count}")
    print(f"Toplam süre: {elapsed:.2f} s")
    print(f"Ortalama FPS: {frame_count / elapsed:.2f}")
    print(f"Ortalama çıkarım: {total_ms / frame_count:.2f} ms")
    print(f"Toplam tespit: {total_det}")
    print(f"Kare başına tespit: {total_det / frame_count:.2f}")
    print(f"Çıktı: {args.output}")


if __name__ == "__main__":
    main()
