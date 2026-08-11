import numpy as np
from PIL import Image


# ==========================================
# MODEL PATH
# ==========================================

import os

MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "best_waste_model.keras"
)


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
# LAZY MODEL
# ==========================================

model = None


def load_model():

    global model

    if model is None:

        print("Loading Waste Classification model...")

        # Import TensorFlow only when prediction is requested
        import tensorflow as tf

        model = tf.keras.models.load_model(
            MODEL_PATH
        )

        print(
            "Waste Classification model loaded successfully."
        )

    return model


# ==========================================
# WASTE PREDICTION
# ==========================================

def predict_waste(image_file):

    waste_model = load_model()

    # Import TensorFlow only when needed
    import tensorflow as tf

    # Open image
    image = Image.open(
        image_file
    ).convert("RGB")

    # Resize
    image = image.resize(
        (224, 224)
    )

    # Convert to numpy
    image = np.array(
        image
    )

    # MobileNetV2 preprocessing
    image = tf.keras.applications.mobilenet_v2.preprocess_input(
        image
    )

    # Add batch dimension
    image = np.expand_dims(
        image,
        axis=0
    )

    # Prediction
    predictions = waste_model.predict(
        image,
        verbose=0
    )

    predicted_index = np.argmax(
        predictions
    )

    confidence = float(
        np.max(predictions)
    )

    return {
        "prediction": CLASS_NAMES[predicted_index],
        "confidence": round(
            confidence * 100,
            2
        )
    }