"""EdgeVision API testleri."""
import io
import sys
from pathlib import Path

import numpy as np
import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).parent.parent))
from src.api.main import app


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
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


def test_model_info(client):
    r = client.get("/model/info")
    assert r.status_code == 200
    assert len(r.json()["classes"]) == 10


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
