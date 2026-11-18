"""EdgeVision - API şemaları."""
from pydantic import BaseModel


class Detection(BaseModel):
    bbox: list[int]
    class_id: int
    class_name: str
    confidence: float


class PredictionResponse(BaseModel):
    detections: list[Detection]
    inference_ms: float
    image_width: int
    image_height: int
    model: str
