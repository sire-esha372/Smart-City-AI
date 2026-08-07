import os
import numpy as np
import tensorflow as tf
from PIL import Image

from ..database.database import SessionLocal
from ..database.crud import save_prediction

# ==========================================
# LOAD MODEL
# ==========================================

MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "ml_models",
    "best_waste_model.keras"
)

model = tf.keras.models.load_model(MODEL_PATH)

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

    image = Image.open(image_file).convert("RGB")
    image = image.resize((224, 224))

    image = np.array(image)

    image = tf.keras.applications.mobilenet_v2.preprocess_input(image)

    image = np.expand_dims(image, axis=0)

    prediction = model.predict(image, verbose=0)

    index = np.argmax(prediction)
    confidence = round(float(np.max(prediction) * 100), 2)

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