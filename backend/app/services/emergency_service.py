from ultralytics import YOLO
from PIL import Image
import os
import uuid

from ..database.database import SessionLocal
from ..database.crud import save_prediction

# ==========================================
# Load YOLO Model (Loads only once)
# ==========================================

MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "ml_models",
    "emergency.pt"
)

model = YOLO(MODEL_PATH)

# ==========================================
# Output Folder
# ==========================================

OUTPUT_FOLDER = os.path.join(
    os.path.dirname(__file__),
    "..",
    "static",
    "predictions"
)

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# ==========================================
# Emergency Detection Function
# ==========================================

def detect_emergency(image_path: str):

    # Run YOLO prediction
    results = model(image_path)

    result = results[0]

    detections = []

    # ==========================================
    # Extract Detected Objects
    # ==========================================

    for box in result.boxes:

        class_id = int(box.cls[0])
        confidence = float(box.conf[0])

        detections.append(
            {
                "class": model.names[class_id],
                "confidence": round(confidence, 2),
            }
        )

    # ==========================================
    # Save Detection to Database
    # ==========================================

    if len(detections) == 0:
        status = "Safe"
        value = "No Detection"

    else:
        detected_classes = list(set([d["class"].title() for d in detections]))
        status = ", ".join(detected_classes)
        value = f"{len(detections)} Object(s)"

    db = SessionLocal()

    try:
        save_prediction(
            db=db,
            module="Emergency",
            status=status,
            value=value
        )
    finally:
        db.close()

    # ==========================================
    # Save Image with Bounding Boxes
    # ==========================================

    output_filename = f"{uuid.uuid4().hex}.jpg"
    output_path = os.path.join(OUTPUT_FOLDER, output_filename)

    plotted_image = result.plot()

    Image.fromarray(plotted_image).save(output_path)

    image_url = f"http://127.0.0.1:8000/static/predictions/{output_filename}"

    return {
        "detections": detections,
        "image_url": image_url,
    }