"""
EdgeVision - Donanım Doğrulama Testleri
Bu testler, modelin farklı donanım yapılandırmalarında (CPU, GPU) 
doğru şekilde yüklendiğini ve çalıştığını doğrular.
"""
import pytest
import onnxruntime as ort
from src.api.model_loader import DetectionModel

def test_onnxruntime_available():
    """ONNX Runtime'ın sistemde kurulu ve çalışır durumda olduğunu doğrular."""
    providers = ort.get_available_providers()
    assert "CPUExecutionProvider" in providers

def test_model_loads_on_cpu():
    """Modelin CPU üzerinde sorunsuz yüklendiğini doğrular."""
    model = DetectionModel("models/yolov8n_fp16.onnx")
    assert model.session is not None
    assert len(model.class_names) == 10

def test_cuda_availability():
    """Eğer CUDA varsa, GPU sağlayıcısının kullanılabilir olduğunu doğrular."""
    providers = ort.get_available_providers()
    if "CUDAExecutionProvider" in providers:
        print("CUDA destekli GPU bulundu.")
    else:
        print("CUDA destekli GPU bulunamadı, CPU kullanılacak.")
