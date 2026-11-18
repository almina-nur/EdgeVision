"""
EdgeVision - ONNX Export ve Quantization Modülü
Bu modül, eğitilmiş PyTorch modellerini ONNX formatına dönüştürür ve INT8 quantization uygular.
Kullanım: python -m src.export_onnx --weights models/yolov8n_best.pt
"""
import argparse
import os
from ultralytics import YOLO
from onnxruntime.quantization import quantize_dynamic, QuantType

def main():
    parser = argparse.ArgumentParser(description="EdgeVision ONNX Export")
    parser.add_argument("--weights", default="models/yolov8n_best.pt", help="PyTorch ağırlık dosyası")
    parser.add_argument("--imgsz", type=int, default=640, help="Giriş görüntü boyutu")
    args = parser.parse_args()

    # 1. FP32 ONNX export
    model = YOLO(args.weights)
    onnx_path = model.export(format="onnx", imgsz=args.imgsz, simplify=True, opset=12)

    # 2. INT8 Dynamic Quantization
    int8_path = onnx_path.replace(".onnx", "_int8.onnx")
    quantize_dynamic(
        model_input=onnx_path,
        model_output=int8_path,
        weight_type=QuantType.QInt8,
    )

    # Boyut raporlaması
    fp32_mb = os.path.getsize(onnx_path) / (1024 * 1024)
    int8_mb = os.path.getsize(int8_path) / (1024 * 1024)
    print(f"FP32 ONNX Boyutu: {fp32_mb:.2f} MB")
    print(f"INT8 ONNX Boyutu: {int8_mb:.2f} MB")
    print(f"Sıkıştırma Oranı: %{100 * (1 - int8_mb / fp32_mb):.1f}")

if __name__ == "__main__":
    main()
