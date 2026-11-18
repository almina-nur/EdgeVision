"""
EdgeVision - TensorRT Export ve Benchmark Modülü
Bu modül, eğitilmiş ONNX modellerini NVIDIA donanımlarında (Jetson vb.) 
maksimum performans için TensorRT formatına dönüştürür.
Kullanım: python -m src.export_tensorrt --weights models/yolov8n_fp16.onnx
"""
import argparse
import os
import tensorrt as trt

def main():
    parser = argparse.ArgumentParser(description="EdgeVision TensorRT Export")
    parser.add_argument("--weights", default="models/yolov8n_fp16.onnx", help="ONNX model dosyası")
    args = parser.parse_args()

    if not os.path.exists(args.weights):
        raise FileNotFoundError(f"Model bulunamadı: {args.weights}")

    print(f"TensorRT Export başlatılıyor: {args.weights}")
    
    # TensorRT Logger
    TRT_LOGGER = trt.Logger(trt.Logger.WARNING)
    
    # Builder ve Network oluşturma
    builder = trt.Builder(TRT_LOGGER)
    network = builder.create_network(1 << int(trt.NetworkDefinitionCreationFlag.EXPLICIT_BATCH))
    parser = trt.OnnxParser(network, TRT_LOGGER)

    # ONNX dosyasını oku
    with open(args.weights, 'rb') as model:
        if not parser.parse(model.read()):
            print("HATA: ONNX dosyası ayrıştırılamadı.")
            for error in range(parser.num_errors):
                print(parser.get_error(error))
            return

    # Builder Config
    config = builder.create_builder_config()
    config.set_memory_pool_limit(trt.MemoryPoolType.WORKSPACE, 1 << 30) # 1GB workspace

    # FP16 desteği varsa etkinleştir
    if builder.platform_has_fast_fp16:
        config.set_flag(trt.BuilderFlag.FP16)
        print("FP16 optimizasyonu etkinleştirildi.")

    # Motoru oluştur
    print("TensorRT motoru derleniyor... (Bu işlem birkaç dakika sürebilir)")
    serialized_engine = builder.build_serialized_network(network, config)
    
    if serialized_engine is None:
        print("HATA: TensorRT motoru oluşturulamadı.")
        return

    # Kaydet
    engine_path = args.weights.replace(".onnx", ".trt")
    with open(engine_path, "wb") as f:
        f.write(serialized_engine)
    
    print(f"TensorRT motoru kaydedildi: {engine_path}")
