import numpy as np
import tensorflow as tf
from PIL import Image

# Load the trained model
model = tf.keras.models.load_model("app/ml_models/best_waste_model.keras")

CLASS_NAMES = [
    "Cardboard",
    "Glass",
    "Metal",
    "Paper",
    "Plastic",
    "Trash"
]


def predict_waste(image_file):

    # Open image
    image = Image.open(image_file).convert("RGB")

    # Resize
    image = image.resize((224, 224))

    # Convert to numpy
    image = np.array(image)

    # MobileNetV2 preprocessing
    image = tf.keras.applications.mobilenet_v2.preprocess_input(image)

    # Add batch dimension
    image = np.expand_dims(image, axis=0)

    # Prediction
    predictions = model.predict(image, verbose=0)

    predicted_index = np.argmax(predictions)

    confidence = float(np.max(predictions))

    return {
        "prediction": CLASS_NAMES[predicted_index],
        "confidence": round(confidence * 100, 2)
    }