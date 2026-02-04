from fastapi import FastAPI, File, UploadFile
from api.model import model, CLASS_NAMES
from api.schemas import PredictionResponse, Detection, BoundingBox
from api.utils import read_image, bbox_area
from api.severity_rules import compute_severity

app = FastAPI(title="Vehicle Damage Detection API")


@app.post("/predict", response_model=PredictionResponse)
async def predict(file: UploadFile = File(...)):
    # Read image
    image_bytes = await file.read()
    image = read_image(image_bytes)

    # Run YOLO inference
    results = model(image)[0]

    detections = []
    image_area = image.shape[0] * image.shape[1]

    for box in results.boxes:
        cls_id = int(box.cls[0])
        confidence = float(box.conf[0])
        x1, y1, x2, y2 = map(float, box.xyxy[0])

        bbox = {
            "x1": x1,
            "y1": y1,
            "x2": x2,
            "y2": y2
        }

        # Compute crop area
        crop_area = bbox_area(bbox)

        # Compute severity (rule-based)
        severity = compute_severity(
            damage_type=CLASS_NAMES[cls_id],
            crop_area=crop_area,
            image_area=image_area
        )

        detections.append(
            Detection(
                damage_type=CLASS_NAMES[cls_id],
                confidence=confidence,
                severity=severity,
                bbox=BoundingBox(
                    x1=x1,
                    y1=y1,
                    x2=x2,
                    y2=y2
                )
            )
        )

    return PredictionResponse(
        detections=detections,
        model_version="yolov8_vehicle_damage_v1",
        severity_mode="rule_based_v1"
    )
