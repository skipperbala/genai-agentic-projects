from ultralytics import YOLO

class FaultDetector:
    def __init__(self, model_path="yolov8n.pt"):
        self.model = YOLO(model_path)

    def detect(self, image_path: str):
        results = self.model(image_path)
        return results