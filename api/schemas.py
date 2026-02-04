from pydantic import BaseModel
from typing import List

class BoundingBox(BaseModel):
    x1: float
    y1: float
    x2: float
    y2: float

class Detection(BaseModel):
    damage_type: str
    confidence: float
    severity: str
    bbox: BoundingBox

class PredictionResponse(BaseModel):
    detections: List[Detection]
    model_version: str
    severity_mode: str

