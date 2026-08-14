import os
import numpy as np
from PIL import Image
import onnxruntime as ort

from ..database.database import SessionLocal
from ..database.crud import save_prediction


# =========================================================
# MODEL PATH
# =========================================================

MODEL_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "waste.onnx"
    )
)


# =========================================================
# CLASS NAMES
# =========================================================

CLASS_NAMES = [
    "Cardboard",
    "Glass",
    "Metal",
    "Paper",
    "Plastic",
    "Trash"
]


# =========================================================
# MODEL SETTINGS
# =========================================================

INPUT_SIZE = (224, 224)

session = None


# =========================================================
# LOAD ONNX MODEL
# =========================================================

def load_model():

    global session

    if session is None:

        print(
            "Loading Waste ONNX model..."
        )

        session = ort.InferenceSession(
            MODEL_PATH,
            providers=[
                "CPUExecutionProvider"
            ]
        )

        print(
            "Waste ONNX model loaded successfully."
        )

    return session


# =========================================================
# WASTE PREDICTION
# =========================================================

def predict_waste(image_file):

    print(
        "Starting Waste ONNX Classification..."
    )

    # =====================================================
    # LOAD MODEL
    # =====================================================

    waste_model = load_model()

    # =====================================================
    # OPEN IMAGE
    # =====================================================

    image = Image.open(
        image_file
    ).convert("RGB")

    # =====================================================
    # RESIZE
    # =====================================================

    image = image.resize(
        INPUT_SIZE,
        Image.Resampling.BILINEAR
    )

    # =====================================================
    # NUMPY
    # =====================================================

    image = np.asarray(
        image,
        dtype=np.float32
    )

    # =====================================================
    # MOBILENETV2 PREPROCESSING
    #
    # Same preprocessing used by the
    # original TensorFlow model.
    # =====================================================

    image = (
        image / 127.5
    ) - 1.0

    # =====================================================
    # BATCH DIMENSION
    #
    # ONNX model expects:
    # [batch, 224, 224, 3]
    # =====================================================

    image = np.expand_dims(
        image,
        axis=0
    )

    # =====================================================
    # RUN ONNX INFERENCE
    # =====================================================

    print(
        "Running Waste ONNX inference..."
    )

    input_name = (
        waste_model
        .get_inputs()[0]
        .name
    )

    output_name = (
        waste_model
        .get_outputs()[0]
        .name
    )

    prediction = waste_model.run(
        [output_name],
        {
            input_name: image
        }
    )[0]

    # =====================================================
    # GET CLASS
    # =====================================================

    prediction = np.asarray(
        prediction
    )

    scores = prediction[0]

    index = int(
        np.argmax(
            scores
        )
    )

    confidence = round(
        float(
            scores[index] * 100
        ),
        2
    )

    # =====================================================
    # CLASS NAME
    # =====================================================

    if index < len(CLASS_NAMES):

        waste_type = (
            CLASS_NAMES[index]
        )

    else:

        waste_type = "Unknown"

    print(
        f"Waste Prediction: "
        f"{waste_type} | "
        f"{confidence}%"
    )

    # =====================================================
    # DATABASE
    # =====================================================

    db = SessionLocal()

    try:

        save_prediction(
            db=db,
            module="Waste",
            status=waste_type,
            value=(
                f"{confidence}% Confidence"
            )
        )

    finally:

        db.close()

    # =====================================================
    # FINAL RESPONSE
    # =====================================================

    print(
        "Waste ONNX classification completed."
    )

    return {
        "prediction": waste_type,
        "confidence": confidence
    }