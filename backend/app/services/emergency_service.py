import os
import uuid
import time
import gc

from PIL import Image

from ..database.database import SessionLocal
from ..database.crud import save_prediction


# =========================================================
# YOLO MODEL PATH
# =========================================================

MODEL_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "ml_models",
        "emergency.onnx"
    )
)


# =========================================================
# OUTPUT FOLDER
# =========================================================

OUTPUT_FOLDER = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "static",
        "predictions"
    )
)

os.makedirs(
    OUTPUT_FOLDER,
    exist_ok=True
)


# =========================================================
# LAZY YOLO MODEL
# =========================================================

model = None


def load_model():

    global model

    if model is None:

        print(
            "Loading Emergency YOLO ONNX model..."
        )

        from ultralytics import YOLO

        model = YOLO(MODEL_PATH)

        print(
            "Emergency YOLO ONNX model loaded successfully."
        )

    return model


# =========================================================
# EMERGENCY DETECTION
# =========================================================

def detect_emergency(image_path: str):

    print(
        "Starting Emergency Detection..."
    )

    # =====================================================
    # LOAD MODEL
    # =====================================================

    emergency_model = load_model()

    print(
        "Running lightweight Emergency YOLO ONNX..."
    )

    start_time = time.time()

    # =====================================================
    # YOLO INFERENCE
    # =====================================================

    results = emergency_model.predict(
        source=image_path,

        # Lightweight inference
        imgsz=320,

        # Confidence threshold
        conf=0.30,

        # Render CPU
        device="cpu",

        # Limit detections
        max_det=10,

        # No progress output
        verbose=False
    )

    inference_time = (
        time.time() - start_time
    )

    print(
        f"Emergency YOLO ONNX inference completed "
        f"in {inference_time:.2f} seconds"
    )

    result = results[0]


    # =====================================================
    # EXTRACT DETECTIONS
    # =====================================================

    detections = []

    for box in result.boxes:

        class_id = int(
            box.cls[0]
        )

        confidence = float(
            box.conf[0]
        )

        class_name = (
            emergency_model.names[class_id]
        )

        detections.append(
            {
                "class": class_name,
                "confidence": round(
                    confidence,
                    2
                )
            }
        )


    print(
        f"Detected {len(detections)} object(s)"
    )


    # =====================================================
    # DATABASE
    # =====================================================

    if len(detections) == 0:

        status = "Safe"
        value = "No Detection"

    else:

        detected_classes = list(
            set(
                detection["class"].title()
                for detection in detections
            )
        )

        status = ", ".join(
            detected_classes
        )

        value = (
            f"{len(detections)} Object(s)"
        )


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


    # =====================================================
    # CREATE DETECTION IMAGE
    # =====================================================

    output_filename = (
        f"emergency_{uuid.uuid4().hex}.jpg"
    )

    output_path = os.path.join(
        OUTPUT_FOLDER,
        output_filename
    )

    print(
        "Creating detection result image..."
    )


    # =====================================================
    # DRAW YOLO BOXES
    # =====================================================

    plotted_image = result.plot()


    # =====================================================
    # REDUCE OUTPUT IMAGE SIZE
    # =====================================================

    result_image = Image.fromarray(
        plotted_image
    )

    result_image.thumbnail(
        (1280, 1280)
    )


    # =====================================================
    # SAVE COMPRESSED IMAGE
    # =====================================================

    result_image.save(
        output_path,
        format="JPEG",
        quality=75,
        optimize=True
    )


    print(
        f"Detection image saved: "
        f"{output_path}"
    )


    # =====================================================
    # CLEAN TEMPORARY OBJECTS
    # =====================================================

    del plotted_image
    del result_image
    del results
    del result

    gc.collect()


    # =====================================================
    # RESPONSE URL
    # =====================================================

    backend_url = os.getenv(
        "BACKEND_URL"
    )

    if not backend_url:

        backend_url = (
            "http://127.0.0.1:8000"
        )

    backend_url = (
        backend_url.rstrip("/")
    )


    image_url = (
        f"{backend_url}"
        f"/static/predictions/"
        f"{output_filename}"
    )


    # =====================================================
    # FINAL RESPONSE
    # =====================================================

    print(
        "Emergency detection completed."
    )

    print(
        f"Image URL: {image_url}"
    )


    return {
        "detections": detections,
        "image_url": image_url
    }