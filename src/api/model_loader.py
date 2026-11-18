"""
EdgeVision - Model Yükleyici ve Çıkarım Sınıfı
Bu modül, ONNX modelini yükler, görüntüyü modele uygun hale getirir (preprocess)
ve modelin çıktısını anlamlı tespitlere dönüştürür (postprocess).
"""
import time
import cv2
import numpy as np
import onnxruntime as ort

class DetectionModel:
    def __init__(self, model_path: str, conf_threshold: float = 0.25, iou_threshold: float = 0.45):
        self.model_path = model_path
        self.conf_threshold = conf_threshold
        self.iou_threshold = iou_threshold
        
        # ONNX Runtime oturumunu başlat (CPU üzerinde)
        self.session = ort.InferenceSession(model_path, providers=["CPUExecutionProvider"])
        self.input_name = self.session.get_inputs()[0].name
        self.input_shape = self.session.get_inputs()[0].shape
        
        # VisDrone sınıf isimleri
        self.class_names = [
            "pedestrian", "people", "bicycle", "car", "van",
            "truck", "tricycle", "awning-tricycle", "bus", "motor",
        ]

    def preprocess(self, image: np.ndarray):
        """Görüntüyü letterbox yöntemiyle yeniden boyutlandırır ve normalize eder."""
        h, w = image.shape[:2]
        target_h, target_w = self.input_shape[2], self.input_shape[3]
        scale = min(target_w / w, target_h / h)
        new_w, new_h = int(w * scale), int(h * scale)
        
        resized = cv2.resize(image, (new_w, new_h))
        canvas = np.full((target_h, target_w, 3), 114, dtype=np.uint8)
        dx, dy = (target_w - new_w) // 2, (target_h - new_h) // 2
        canvas[dy:dy + new_h, dx:dx + new_w] = resized
        
        # BGR -> RGB, HWC -> CHW, normalize
        blob = canvas[:, :, ::-1].transpose(2, 0, 1).astype(np.float32) / 255.0
        return np.expand_dims(blob, 0), (scale, dx, dy)

    def postprocess(self, output: np.ndarray, meta, orig_shape):
        """Model çıktısını NMS uygulayarak tespit kutularına dönüştürür."""
        scale, dx, dy = meta
        preds = output[0].T
        boxes_xywh = preds[:, :4]
        class_scores = preds[:, 4:]
        
        class_ids = class_scores.argmax(axis=1)
        confidences = class_scores.max(axis=1)
        
        # Eşik değerinin altındakileri filtrele
        mask = confidences > self.conf_threshold
        boxes_xywh = boxes_xywh[mask]
        confidences = confidences[mask]
        class_ids = class_ids[mask]
        
        if len(boxes_xywh) == 0:
            return []
            
        # xywh -> xyxy dönüşümü
        x, y, w, h = boxes_xywh.T
        boxes_xyxy = np.stack([x - w / 2, y - h / 2, x + w / 2, y + h / 2], axis=1)
        
        # Orijinal görüntü boyutlarına geri ölçekle
        boxes_xyxy[:, [0, 2]] = (boxes_xyxy[:, [0, 2]] - dx) / scale
        boxes_xyxy[:, [1, 3]] = (boxes_xyxy[:, [1, 3]] - dy) / scale

        # Non-Maximum Suppression (NMS)
        indices = cv2.dnn.NMSBoxes(
            boxes_xyxy.tolist(), confidences.tolist(),
            self.conf_threshold, self.iou_threshold,
        )
        
        results = []
        for i in indices:
            x1, y1, x2, y2 = boxes_xyxy[i].astype(int)
            results.append({
                "bbox": [int(x1), int(y1), int(x2 - x1), int(y2 - y1)],
                "class_id": int(class_ids[i]),
                "class_name": self.class_names[int(class_ids[i])],
                "confidence": float(confidences[i]),
            })
        return results

    def predict(self, image: np.ndarray):
        """Tek bir görüntü üzerinde çıkarım yapar ve süreyi ölçer."""
        blob, meta = self.preprocess(image)
        t0 = time.perf_counter()
        outputs = self.session.run(None, {self.input_name: blob})
        inference_ms = (time.perf_counter() - t0) * 1000
        detections = self.postprocess(outputs[0], meta, image.shape[:2])
        return detections, inference_ms
