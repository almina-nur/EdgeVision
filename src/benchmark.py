"""EdgeVision - Model benchmark (FPS, latency, memory)."""
import argparse
import os
import time
from pathlib import Path

import cv2
import psutil

from src.api.model_loader import DetectionModel


def benchmark_model(model_path: str, image_path: str, n_runs: int = 50):
    model = DetectionModel(model_path)
    image = cv2.imread(image_path)
    if image is None:
        raise SystemExit(f"Görüntü okunamadı: {image_path}")

    process = psutil.Process(os.getpid())
    mem_start = process.memory_info().rss / (1024**2)

    for _ in range(5):
        model.predict(image)

    times = []
    t_total = time.perf_counter()
    for _ in range(n_runs):
        t0 = time.perf_counter()
        model.predict(image)
        times.append((time.perf_counter() - t0) * 1000)
    t_total = time.perf_counter() - t_total

    mem_end = process.memory_info().rss / (1024**2)
    times.sort()

    return {
        "model": Path(model_path).name,
        "size_mb": round(os.path.getsize(model_path) / (1024**2), 2),
        "runs": n_runs,
        "fps": round(n_runs / t_total, 2),
        "latency_avg_ms": round(sum(times) / len(times), 2),
        "latency_p50_ms": round(times[len(times) // 2], 2),
        "latency_p95_ms": round(times[int(len(times) * 0.95)], 2),
        "latency_min_ms": round(times[0], 2),
        "latency_max_ms": round(times[-1], 2),
        "memory_mb": round(mem_end - mem_start, 2),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", default="test_image.jpg")
    parser.add_argument("--runs", type=int, default=30)
    args = parser.parse_args()

    models = [
        "models/yolov8n_fp32.onnx",
        "models/yolov8n_int8.onnx",
        "models/yolov8s_fp32.onnx",
        "models/yolov8s_int8.onnx",
    ]

    results = []
    for m in models:
        if not os.path.exists(m):
            print(f" {m} bulunamadı, atlanıyor")
            continue
        print(f"Benchmark: {m} ({args.runs} runs)...")
        r = benchmark_model(m, args.image, args.runs)
        results.append(r)
        print(f"  FPS: {r['fps']:.2f}, Avg: {r['latency_avg_ms']:.1f} ms, P95: {r['latency_p95_ms']:.1f} ms")

    import csv
    out = "results/benchmark_results.csv"
    if results:
        with open(out, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=results[0].keys())
            w.writeheader()
            w.writerows(results)
        print(f"\n {out} kaydedildi")

        print(f"\n{'Model':<25} {'Size':<10} {'FPS':<8} {'Avg':<10} {'P95':<10}")
        print("-" * 65)
        for r in results:
            print(f"{r['model']:<25} {r['size_mb']:.2f} MB  {r['fps']:.2f}    {r['latency_avg_ms']:.1f} ms  {r['latency_p95_ms']:.1f} ms")


if __name__ == "__main__":
    main()
