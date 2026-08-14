import os
import uuid
import time

import cv2
import numpy as np
import onnxruntime as ort

from PIL import Image

from ..database.database import SessionLocal
from ..database.crud import save_prediction


# =========================================================
# MODEL PATH
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
# MODEL SETTINGS
# =========================================================

INPUT_SIZE = 416

CONF_THRESHOLD = 0.30

IOU_THRESHOLD = 0.45


# =========================================================
# CLASS NAMES
# =========================================================

CLASS_NAMES = [
    "fire",
    "smoke"
]


# =========================================================
# LAZY ONNX MODEL
# =========================================================

session = None


def load_model():

    global session

    if session is None:

        print(
            "Loading Emergency ONNX Runtime model..."
        )

        session = ort.InferenceSession(
            MODEL_PATH,
            providers=[
                "CPUExecutionProvider"
            ]
        )

        print(
            "Emergency ONNX Runtime model "
            "loaded successfully."
        )

    return session


# =========================================================
# LETTERBOX
# =========================================================

def letterbox(image):

    original_height, original_width = image.shape[:2]

    scale = min(
        INPUT_SIZE / original_width,
        INPUT_SIZE / original_height
    )

    new_width = int(
        original_width * scale
    )

    new_height = int(
        original_height * scale
    )

    resized = cv2.resize(
        image,
        (new_width, new_height),
        interpolation=cv2.INTER_LINEAR
    )

    canvas = np.full(
        (
            INPUT_SIZE,
            INPUT_SIZE,
            3
        ),
        114,
        dtype=np.uint8
    )

    pad_x = (
        INPUT_SIZE - new_width
    ) // 2

    pad_y = (
        INPUT_SIZE - new_height
    ) // 2

    canvas[
        pad_y:pad_y + new_height,
        pad_x:pad_x + new_width
    ] = resized

    return (
        canvas,
        scale,
        pad_x,
        pad_y
    )


# =========================================================
# IOU
# =========================================================

def calculate_iou(box1, box2):

    x1 = max(
        box1[0],
        box2[0]
    )

    y1 = max(
        box1[1],
        box2[1]
    )

    x2 = min(
        box1[2],
        box2[2]
    )

    y2 = min(
        box1[3],
        box2[3]
    )

    intersection_width = max(
        0,
        x2 - x1
    )

    intersection_height = max(
        0,
        y2 - y1
    )

    intersection = (
        intersection_width *
        intersection_height
    )

    area1 = (
        max(0, box1[2] - box1[0]) *
        max(0, box1[3] - box1[1])
    )

    area2 = (
        max(0, box2[2] - box2[0]) *
        max(0, box2[3] - box2[1])
    )

    union = (
        area1 +
        area2 -
        intersection
    )

    if union <= 0:
        return 0.0

    return intersection / union


# =========================================================
# NMS
# =========================================================

def non_max_suppression(
    boxes,
    scores,
    class_ids
):

    if not boxes:

        return []

    keep = []

    unique_classes = set(
        class_ids
    )

    for class_id in unique_classes:

        indices = [
            i
            for i, cid in enumerate(class_ids)
            if cid == class_id
        ]

        indices.sort(
            key=lambda i: scores[i],
            reverse=True
        )

        while indices:

            current = indices.pop(0)

            keep.append(
                current
            )

            remaining = []

            for index in indices:

                iou = calculate_iou(
                    boxes[current],
                    boxes[index]
                )

                if iou < IOU_THRESHOLD:

                    remaining.append(
                        index
                    )

            indices = remaining

    keep.sort(
        key=lambda i: scores[i],
        reverse=True
    )

    return keep


# =========================================================
# EMERGENCY DETECTION
# =========================================================

def detect_emergency(
    image_path: str
):

    print(
        "Starting Emergency Detection..."
    )

    # =====================================================
    # LOAD ONNX SESSION
    # =====================================================

    emergency_model = load_model()

    # =====================================================
    # READ IMAGE
    # =====================================================

    image = cv2.imread(
        image_path
    )

    if image is None:

        raise ValueError(
            "Unable to read uploaded image."
        )

    original = image.copy()

    original_height, original_width = (
        original.shape[:2]
    )

    # =====================================================
    # PREPROCESS
    # =====================================================

    print(
        "Preprocessing Emergency image..."
    )

    processed, scale, pad_x, pad_y = (
        letterbox(image)
    )

    processed = cv2.cvtColor(
        processed,
        cv2.COLOR_BGR2RGB
    )

    processed = (
        processed.astype(
            np.float32
        ) / 255.0
    )

    processed = np.transpose(
        processed,
        (2, 0, 1)
    )

    processed = np.expand_dims(
        processed,
        axis=0
    )

    # =====================================================
    # ONNX INFERENCE
    # =====================================================

    print(
        "Running direct ONNX Runtime inference..."
    )

    start_time = time.time()

    input_name = (
        emergency_model
        .get_inputs()[0]
        .name
    )

    outputs = emergency_model.run(
        None,
        {
            input_name: processed
        }
    )

    inference_time = (
        time.time() - start_time
    )

    print(
        f"Emergency ONNX inference "
        f"completed in "
        f"{inference_time:.2f} seconds"
    )

    # =====================================================
    # OUTPUT
    # =====================================================

    output = outputs[0]

    # Expected:
    # [1, 6, 3549]

    output = np.squeeze(
        output,
        axis=0
    )

    # Convert:
    # [6, 3549]
    #
    # to:
    # [3549, 6]

    output = output.T

    boxes = []
    scores = []
    class_ids = []

    # =====================================================
    # EXTRACT DETECTIONS
    # =====================================================

    for detection in output:

        center_x = float(
            detection[0]
        )

        center_y = float(
            detection[1]
        )

        width = float(
            detection[2]
        )

        height = float(
            detection[3]
        )

        class_scores = detection[4:]

        class_id = int(
            np.argmax(
                class_scores
            )
        )

        confidence = float(
            class_scores[class_id]
        )

        if confidence < CONF_THRESHOLD:

            continue

        # =================================================
        # YOLO BOX
        # =================================================

        x1 = (
            center_x -
            width / 2
        )

        y1 = (
            center_y -
            height / 2
        )

        x2 = (
            center_x +
            width / 2
        )

        y2 = (
            center_y +
            height / 2
        )

        # =================================================
        # REMOVE LETTERBOX PADDING
        # =================================================

        x1 = (
            x1 - pad_x
        ) / scale

        y1 = (
            y1 - pad_y
        ) / scale

        x2 = (
            x2 - pad_x
        ) / scale

        y2 = (
            y2 - pad_y
        ) / scale

        # =================================================
        # CLAMP
        # =================================================

        x1 = max(
            0,
            min(
                original_width - 1,
                x1
            )
        )

        y1 = max(
            0,
            min(
                original_height - 1,
                y1
            )
        )

        x2 = max(
            0,
            min(
                original_width - 1,
                x2
            )
        )

        y2 = max(
            0,
            min(
                original_height - 1,
                y2
            )
        )

        boxes.append(
            [
                x1,
                y1,
                x2,
                y2
            ]
        )

        scores.append(
            confidence
        )

        class_ids.append(
            class_id
        )

    # =====================================================
    # NMS
    # =====================================================

    keep_indices = (
        non_max_suppression(
            boxes,
            scores,
            class_ids
        )
    )

    # =====================================================
    # FINAL DETECTIONS
    # =====================================================

    detections = []

    for index in keep_indices:

        class_id = (
            class_ids[index]
        )

        confidence = (
            scores[index]
        )

        class_name = (
            CLASS_NAMES[class_id]
            if class_id < len(CLASS_NAMES)
            else f"class_{class_id}"
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
        f"Detected "
        f"{len(detections)} object(s)"
    )

    # =====================================================
    # DATABASE
    # =====================================================

    if not detections:

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
    # DRAW DETECTIONS
    # =====================================================

    result_image = original.copy()

    for index in keep_indices:

        x1, y1, x2, y2 = (
            boxes[index]
        )

        class_id = (
            class_ids[index]
        )

        confidence = (
            scores[index]
        )

        class_name = (
            CLASS_NAMES[class_id]
            if class_id < len(CLASS_NAMES)
            else f"class_{class_id}"
        )

        x1 = int(x1)
        y1 = int(y1)
        x2 = int(x2)
        y2 = int(y2)

        cv2.rectangle(
            result_image,
            (x1, y1),
            (x2, y2),
            (0, 0, 255),
            2
        )

        label = (
            f"{class_name} "
            f"{confidence * 100:.1f}%"
        )

        cv2.putText(
            result_image,
            label,
            (x1, max(25, y1 - 8)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 0, 255),
            2
        )

    # =====================================================
    # OUTPUT IMAGE
    # =====================================================

    output_filename = (
        f"emergency_"
        f"{uuid.uuid4().hex}.jpg"
    )

    output_path = os.path.join(
        OUTPUT_FOLDER,
        output_filename
    )

    result_pil = Image.fromarray(
        cv2.cvtColor(
            result_image,
            cv2.COLOR_BGR2RGB
        )
    )

    result_pil.thumbnail(
        (1280, 1280)
    )

    result_pil.save(
        output_path,
        format="JPEG",
        quality=75,
        optimize=True
    )

    # =====================================================
    # IMAGE URL
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