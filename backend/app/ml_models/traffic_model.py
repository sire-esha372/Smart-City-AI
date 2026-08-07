import os
import joblib

# -----------------------------
# Project Root
# -----------------------------

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..")
)

MODELS_DIR = os.path.join(BASE_DIR, "models")

# -----------------------------
# Load Model
# -----------------------------

traffic_model = joblib.load(
    os.path.join(MODELS_DIR, "traffic_model.pkl")
)

holiday_encoder = joblib.load(
    os.path.join(MODELS_DIR, "holiday_encoder.pkl")
)

weather_main_encoder = joblib.load(
    os.path.join(MODELS_DIR, "weather_main_encoder.pkl")
)

weather_description_encoder = joblib.load(
    os.path.join(MODELS_DIR, "weather_description_encoder.pkl")
)


# -----------------------------
# Encoder Functions
# -----------------------------

def encode_holiday(value):
    return holiday_encoder.transform([value])[0]


def encode_weather_main(value):
    return weather_main_encoder.transform([value])[0]


def encode_weather_description(value):
    return weather_description_encoder.transform([value])[0]


# -----------------------------
# Prediction
# -----------------------------

def predict(features):
    prediction = traffic_model.predict([features])
    return float(prediction[0])