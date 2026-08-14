import os

# =========================================================
# FORCE TENSORFLOW TO USE CPU ONLY
# =========================================================

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

# Keep CPU usage small for Render Free
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["TF_NUM_INTRAOP_THREADS"] = "1"
os.environ["TF_NUM_INTEROP_THREADS"] = "1"


import numpy as np
from PIL import Image

from ..database.database import SessionLocal
from ..database.crud import save_prediction


# =========================================================
# MODEL PATH
# =========================================================

MODEL_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "best_waste_model.keras"
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
# LAZY MODEL
# =========================================================

model = None
tf = None


def load_model():

    global model
    global tf

    if model is None:

        print(
            "Loading Waste TensorFlow model "
            "in CPU-only mode..."
        )

        # Import TensorFlow only when Waste
        # prediction is requested
        import tensorflow as tensorflow

        tf = tensorflow

        # Explicitly disable GPU
        try:

            tf.config.set_visible_devices(
                [],
                "GPU"
            )

        except RuntimeError:

            # GPU configuration was already initialized.
            # CUDA_VISIBLE_DEVICES=-1 still prevents GPU use.
            pass

        # Limit TensorFlow CPU threads
        try:

            tf.config.threading.set_intra_op_parallelism_threads(
                1
            )

            tf.config.threading.set_inter_op_parallelism_threads(
                1
            )

        except RuntimeError:

            pass

        print(
            "Loading Waste Keras model..."
        )

        model = tf.keras.models.load_model(
            MODEL_PATH,
            compile=False
        )

        print(
            "Waste TensorFlow model "
            "loaded successfully."
        )

    return model


# =========================================================
# WASTE PREDICTION
# =========================================================

def predict_waste(image_file):

    print(
        "Starting Waste Classification..."
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
        (224, 224),
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
    # =====================================================

    image = tf.keras.applications.mobilenet_v2.preprocess_input(
        image
    )

    # =====================================================
    # BATCH DIMENSION
    # =====================================================

    image = np.expand_dims(
        image,
        axis=0
    )

    # =====================================================
    # DIRECT MODEL INFERENCE
    # =====================================================

    print(
        "Running CPU-only Waste inference..."
    )

    prediction = waste_model(
        image,
        training=False
    )

    # Convert TensorFlow tensor to NumPy
    prediction = prediction.numpy()

    # =====================================================
    # RESULT
    # =====================================================

    index = int(
        np.argmax(
            prediction[0]
        )
    )

    confidence = round(
        float(
            np.max(
                prediction[0]
            ) * 100
        ),
        2
    )

    # Safety check
    if index >= len(CLASS_NAMES):

        waste_type = "Unknown"

    else:

        waste_type = CLASS_NAMES[index]

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
            value=f"{confidence}% Confidence"
        )

    finally:

        db.close()

    # =====================================================
    # FINAL RESPONSE
    # =====================================================

    print(
        "Waste classification completed."
    )

    return {
        "prediction": waste_type,
        "confidence": confidence
    }