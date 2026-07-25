#  Car Detection — Vehicle Damage Detection

A **FastAPI** service that detects vehicle damage from a single uploaded photo.
A **YOLOv8** model localizes the damage, and a rule-based severity engine turns
each detection into an insurance-style **minor / moderate / severe** rating —
no manual adjuster needed for the first pass.

![python](https://img.shields.io/badge/python-3.10-3776ab) ![backend](https://img.shields.io/badge/backend-FastAPI-009688) ![model](https://img.shields.io/badge/model-YOLOv8%20(Ultralytics)-00FFFF) ![docker](https://img.shields.io/badge/container-Docker-2496ED) ![ci](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-2088FF)

---

## What it does

- **Upload a photo, get structured damage data** — `POST /predict` accepts an
  image and returns every detected damage region as JSON: type, confidence,
  bounding box, and severity.
- **5 damage classes** — `dent`, `scratch`, `broken_glass`, `bumper_damage`,
  `headlight_damage`.
- **Rule-based severity scoring** — severity isn't just the model's confidence;
  it's derived from damage type plus how much of the frame the damage covers
  (`crop_area / image_area`). Scratches are always cosmetic ("minor"), while
  safety-relevant damage (glass, headlights, bumper) escalates to "severe" once
  it passes an area threshold.
- **Single-endpoint, stateless design** — one YOLO model loaded once at
  startup, inference is synchronous per request, no database required.

---

## How severity is computed

| Damage type | Rule |
| --- | --- |
| `scratch` | Always `minor` (cosmetic only) |
| `dent` | `minor` if area ratio < 4%, else `moderate` |
| `broken_glass`, `headlight_damage` | `moderate` if area ratio < 2%, else `severe` |
| `bumper_damage` | `moderate` if area ratio < 3%, else `severe` |
| anything else | `minor` (safe fallback) |

`area_ratio` is the detected bounding-box area divided by the total image area —
a deliberately simple, explainable heuristic rather than a learned severity
model, so every score can be justified to an underwriter.

---

## Repository layout

```
├── api/
│   ├── main.py              # FastAPI app + /predict endpoint
│   ├── model.py              # Loads the YOLOv8 weights + class names
│   ├── schemas.py             # Pydantic response models (Detection, BoundingBox, ...)
│   ├── severity_rules.py      # Rule-based severity engine
│   └── utils.py                # Image decoding + bbox-area helpers
├── models/
│   └── yolov8_vehicle_damage_v1.pt   # Trained YOLOv8 weights
├── .github/workflows/
│   └── deploy.yml            # Build → push to Docker Hub → deploy to EC2 on push to main
├── Dockerfile
└── requirements.txt
```

---

## API

| Method | Path       | Description                                  |
| ------ | ---------- | --------------------------------------------- |
| POST   | `/predict` | Upload an image, get back detections + severity |

**Request:** `multipart/form-data` with a `file` field (image).

```bash
curl -X POST http://localhost:8000/predict \
  -F "file=@/path/to/car_photo.jpg"
```

**Response:**

```json
{
  "detections": [
    {
      "damage_type": "bumper_damage",
      "confidence": 0.91,
      "severity": "severe",
      "bbox": { "x1": 120.4, "y1": 88.0, "x2": 430.1, "y2": 260.7 }
    }
  ],
  "model_version": "yolov8_vehicle_damage_v1",
  "severity_mode": "rule_based_v1"
}
```

Interactive Swagger docs are available at `/docs` once the server is running.

---

## Quickstart

### Local (Python)

```bash
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

- API root: <http://localhost:8000>
- Interactive docs: <http://localhost:8000/docs>

### Docker

```bash
docker build -t car-detection-api .
docker run -d -p 8000:8000 --name car-detection car-detection-api
```

---

## Deployment

`deploy.yml` runs on every push to `main`: it builds the Docker image, pushes
it to Docker Hub as `bhavuk1409/car-detection-api:latest`, then SSHes into an
EC2 instance to pull the new image and restart the `car-detection` container
on port 80. Required GitHub secrets: `DOCKERHUB_USERNAME`, `DOCKERHUB_TOKEN`,
`EC2_HOST`, `EC2_USER`, `EC2_SSH_KEY`.

---

## Tech stack

- **FastAPI** + **Uvicorn** — HTTP API
- **Ultralytics YOLOv8** — object detection
- **OpenCV (headless)** + **NumPy** — image decoding
- **PyTorch / TorchVision** — model backend
- **Docker** + **GitHub Actions** — build and deploy pipeline

---

## License

No license specified yet — add one (e.g. MIT) if you plan to share or accept
contributions.
