from ultralytics import YOLO

MODEL_PATH = "models/yolov8_vehicle_damage_v1.pt"

model = YOLO(MODEL_PATH)

CLASS_NAMES = [
    "dent",
    "scratch",
    "broken_glass",
    "bumper_damage",
    "headlight_damage"
]
