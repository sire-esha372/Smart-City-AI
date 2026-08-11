import os
import joblib


# ---------------------------------------------------------
# Project Root
# ---------------------------------------------------------

BASE_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "..",
        ".."
    )
)

MODELS_DIR = os.path.join(
    BASE_DIR,
    "models"
)


# ---------------------------------------------------------
# Lazy Model Loading
# ---------------------------------------------------------

traffic_model = None
holiday_encoder = None
weather_main_encoder = None
weather_description_encoder = None


def load_models():

    global traffic_model
    global holiday_encoder
    global weather_main_encoder
    global weather_description_encoder

    # Already loaded
    if (
        traffic_model is not None
        and holiday_encoder is not None
        and weather_main_encoder is not None
        and weather_description_encoder is not None
    ):
        return

    print("Loading Traffic ML models...")

    traffic_model = joblib.load(
        os.path.join(
            MODELS_DIR,
            "traffic_model.pkl"
        )
    )

    holiday_encoder = joblib.load(
        os.path.join(
            MODELS_DIR,
            "holiday_encoder.pkl"
        )
    )

    weather_main_encoder = joblib.load(
        os.path.join(
            MODELS_DIR,
            "weather_main_encoder.pkl"
        )
    )

    weather_description_encoder = joblib.load(
        os.path.join(
            MODELS_DIR,
            "weather_description_encoder.pkl"
        )
    )

    print("Traffic ML models loaded successfully.")


# ---------------------------------------------------------
# Encoder Functions
# ---------------------------------------------------------

def encode_holiday(value):

    load_models()

    return holiday_encoder.transform([value])[0]


def encode_weather_main(value):

    load_models()

    return weather_main_encoder.transform([value])[0]


def encode_weather_description(value):

    load_models()

    return weather_description_encoder.transform([value])[0]


# ---------------------------------------------------------
# Prediction
# ---------------------------------------------------------

def predict(features):

    load_models()

    prediction = traffic_model.predict(
        [features]
    )

    return float(prediction[0])