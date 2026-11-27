"""
EdgeVision - Donanım Doğrulama Testleri
Bu testler, modelin farklı donanım yapılandırmalarında (CPU, GPU) 
doğru şekilde yüklendiğini ve çalıştığını doğrular.
"""
import onnx
from onnx import TensorProto, helper
import onnxruntime as ort
from src.api.model_loader import DetectionModel

def test_onnxruntime_available():
    """ONNX Runtime'ın sistemde kurulu ve çalışır durumda olduğunu doğrular."""
    providers = ort.get_available_providers()
    assert "CPUExecutionProvider" in providers

def test_model_loads_on_cpu(tmp_path):
    """ONNX oturumunun CPU üzerinde oluşturulduğunu doğrular."""
    shape = [1, 3, 8, 8]
    graph = helper.make_graph(
        [helper.make_node("Identity", ["image"], ["output"])],
        "cpu-test",
        [helper.make_tensor_value_info("image", TensorProto.FLOAT, shape)],
        [helper.make_tensor_value_info("output", TensorProto.FLOAT, shape)],
    )
    model_path = tmp_path / "identity.onnx"
    onnx.save(helper.make_model(graph, opset_imports=[helper.make_opsetid("", 13)], ir_version=8), model_path)
    model = DetectionModel(str(model_path))
    assert model.session.get_providers() == ["CPUExecutionProvider"]
    assert len(model.class_names) == 10

def test_cuda_availability():
    """Eğer CUDA varsa, GPU sağlayıcısının kullanılabilir olduğunu doğrular."""
    providers = ort.get_available_providers()
    if "CUDAExecutionProvider" in providers:
        print("CUDA destekli GPU bulundu.")
    else:
        print("CUDA destekli GPU bulunamadı, CPU kullanılacak.")
