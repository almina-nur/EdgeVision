"""
EdgeVision - Tile-Based Inference (Parçalı Çıkarım)
VisDrone gibi yüksek çözünürlüklü İHA görüntülerinde küçük nesnelerin 
kaçırılmasını önlemek için görüntüyü üst üste binen parçalara (tile) böler.
"""
import cv2
import numpy as np
from src.api.model_loader import DetectionModel

class TileInference:
    def __init__(self, model_path: str, tile_size: int = 640, overlap: float = 0.2):
        self.model = DetectionModel(model_path)
        self.tile_size = tile_size
        self.overlap = overlap

    def predict(self, image: np.ndarray):
        """Görüntüyü parçalara bölerek çıkarım yapar ve sonuçları birleştirir."""
        h, w = image.shape[:2]
        stride = int(self.tile_size * (1 - self.overlap))
        
        all_detections = []
        total_inference_time = 0

        # Görüntüyü kaydırarak parçalara böl
        for y in range(0, h, stride):
            for x in range(0, w, stride):
                # Parça sınırlarını belirle
                x1, y1 = x, y
                x2, y2 = min(x + self.tile_size, w), min(y + self.tile_size, h)
                
                tile = image[y1:y2, x1:x2]
                
                # Parça çok küçükse atla
                if tile.shape[0] < 32 or tile.shape[1] < 32:
                    continue

                detections, ms = self.model.predict(tile)
                total_inference_time += ms

                # Tespitleri orijinal görüntü koordinatlarına kaydır
                for det in detections:
                    bx, by, bw, bh = det["bbox"]
                    det["bbox"] = [bx + x1, by + y1, bw, bh]
                    all_detections.append(det)

        # Basit bir NMS (Non-Maximum Suppression) ile çakışan kutuları temizle
        if all_detections:
            boxes = [[d["bbox"][0], d["bbox"][1], d["bbox"][0]+d["bbox"][2], d["bbox"][1]+d["bbox"][3]] for d in all_detections]
            scores = [d["confidence"] for d in all_detections]
            indices = cv2.dnn.NMSBoxes(boxes, scores, 0.25, 0.45)
            
            final_detections = [all_detections[i] for i in indices]
        else:
            final_detections = []

        return final_detections, total_inference_time
