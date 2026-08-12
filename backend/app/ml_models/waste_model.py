import os
import numpy as np
from PIL import Image

from ..database.database import SessionLocal
from ..database.crud import save_prediction


# ==========================================
# MODEL PATH
# ==========================================

MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "ml_models",
    "best_waste_model.keras"
)


# ==========================================
# LAZY MODEL
# ==========================================

model = None


def load_model():

    global model

    if model is None:

        print("Loading Waste TensorFlow model...")

        # Import TensorFlow only when Waste
        # prediction is actually requested
        import tensorflow as tf

        model = tf.keras.models.load_model(
            MODEL_PATH
        )

        print(
            "Waste TensorFlow model loaded successfully."
        )

    return model


# ==========================================
# CLASS NAMES
# ==========================================

CLASS_NAMES = [
    "Cardboard",
    "Glass",
    "Metal",
    "Paper",
    "Plastic",
    "Trash"
]


# ==========================================
# WASTE PREDICTION
# ==========================================

def predict_waste(image_file):

    # ==========================================
    # LOAD MODEL ONLY WHEN NEEDED
    # ==========================================

    waste_model = load_model()

    # Import TensorFlow here as well so that
    # TensorFlow is not loaded during startup
    import tensorflow as tf

    # ==========================================
    # OPEN IMAGE
    # ==========================================

    image = Image.open(
        image_file
    ).convert("RGB")

    # ==========================================
    # RESIZE
    # ==========================================

    image = image.resize(
        (224, 224)
    )

    # ==========================================
    # CONVERT TO NUMPY
    # ==========================================

    image = np.array(
        image
    )

    # ==========================================
    # MOBILENETV2 PREPROCESSING
    # ==========================================

    image = tf.keras.applications.mobilenet_v2.preprocess_input(
        image
    )

    # ==========================================
    # ADD BATCH DIMENSION
    # ==========================================

    image = np.expand_dims(
        image,
        axis=0
    )

    # ==========================================
    # PREDICTION
    # ==========================================

    prediction = waste_model.predict(
        image,
        verbose=0
    )

    index = np.argmax(
        prediction
    )

    confidence = round(
        float(
            np.max(prediction) * 100
        ),
        2
    )

    waste_type = CLASS_NAMES[index]

    # ==========================================
    # SAVE TO DATABASE
    # ==========================================

    db = SessionLocal()

    try:

        save_prediction(
            db=db,
            module="Waste",
            status=waste_type,
            value=f"{confidence}% Confidence"
        )

    finally:

        db.close()

    # ==========================================
    # RESPONSE
    # ==========================================

    return {
        "prediction": waste_type,
        "confidence": confidence
    }