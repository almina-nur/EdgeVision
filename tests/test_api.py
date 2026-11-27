"""EdgeVision API testleri."""
import io
import sys
from pathlib import Path
from unittest.mock import Mock

import numpy as np
import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).parent.parent))
@pytest.fixture(scope="module")
def client(tmp_path_factory):
    db_path = tmp_path_factory.mktemp("db") / "edgevision.db"
    with pytest.MonkeyPatch.context() as patch:
        patch.setenv("DATABASE_URL", f"sqlite:///{db_path.as_posix()}")
        from src.api import main

        model = Mock()
        model.predict.return_value = ([], 1.25)
        patch.setattr(main, "DetectionModel", Mock(return_value=model))
        with TestClient(main.app, headers={"X-API-Key": main.API_KEY}) as c:
            yield c


def _fake_image_bytes():
    import cv2
    img = np.zeros((512, 512, 3), dtype=np.uint8)
    ok, buf = cv2.imencode(".png", img)
    assert ok
    return buf.tobytes()


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_metrics(client):
    r = client.get("/metrics")
    assert r.status_code == 200
    assert "edgevision_requests_total" in r.text


def test_predict_valid(client):
    files = {"file": ("test.png", io.BytesIO(_fake_image_bytes()), "image/png")}
    r = client.post("/predict", files=files)
    assert r.status_code == 200
    data = r.json()
    assert "detections" in data
    assert "inference_ms" in data
    assert data["image_width"] == 512


def test_predict_invalid(client):
    files = {"file": ("test.txt", io.BytesIO(b"not an image"), "text/plain")}
    r = client.post("/predict", files=files)
    assert r.status_code == 400

def test_nms_keeps_separate_boxes():
    from src.api.model_loader import DetectionModel

    model = DetectionModel.__new__(DetectionModel)
    model.conf_threshold = 0.25
    model.iou_threshold = 0.45
    model.class_names = ["car"]
    output = np.array([[[110, 135], [110, 110], [20, 20], [20, 20], [0.9, 0.8]]])

    detections = model.postprocess(output, (1.0, 0, 0), (256, 256))

    assert [item["bbox"] for item in detections] == [
        [100, 100, 20, 20],
        [125, 100, 20, 20],
    ]
