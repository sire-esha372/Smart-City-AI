from fastapi import APIRouter
import joblib
import pandas as pd
import os

from ..database.database import SessionLocal
from ..database.crud import save_prediction

from ..schemas.pollution_schema import PollutionInput
from ..services.air_quality_service import get_air_quality

router = APIRouter(
    prefix="/predict/pollution",
    tags=["Pollution Prediction"]
)

# ==========================================
# LOAD MODEL
# ==========================================

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..")
)

MODELS_DIR = os.path.join(BASE_DIR, "models")

model_path = os.path.join(
    MODELS_DIR,
    "pollution_model.pkl"
)

model = joblib.load(model_path)


@router.post("/")
def predict_pollution(data: PollutionInput):

    air = get_air_quality(data.city)

    input_data = pd.DataFrame([{
        "PM2.5": air["PM2_5"],
        "PM10": air["PM10"],
        "NO": air["NO"],
        "NO2": air["NO2"],
        "NOx": air["NOx"],
        "NH3": air["NH3"],
        "CO": air["CO"],
        "SO2": air["SO2"],
        "O3": air["O3"],
        "Benzene": air["Benzene"],
        "Toluene": air["Toluene"]
    }])

    prediction = round(float(model.predict(input_data)[0]), 2)

    if prediction <= 50:
        level = "Good"
    elif prediction <= 100:
        level = "Satisfactory"
    elif prediction <= 200:
        level = "Moderate"
    elif prediction <= 300:
        level = "Poor"
    elif prediction <= 400:
        level = "Very Poor"
    else:
        level = "Severe"

    # ==========================================
    # SAVE TO DATABASE
    # ==========================================

    db = SessionLocal()

    try:
        save_prediction(
            db=db,
            module="Pollution",
            status=level,
            value=f"AQI {prediction}"
        )
    finally:
        db.close()

    # ==========================================
    # RESPONSE
    # ==========================================

    return {
        "success": True,

        "location": {
            "city": air["city"],
            "country": air["country"]
        },

        "air_quality": {
            "PM2.5": air["PM2_5"],
            "PM10": air["PM10"],
            "NO": air["NO"],
            "NO2": air["NO2"],
            "CO": air["CO"],
            "SO2": air["SO2"],
            "O3": air["O3"]
        },

        "prediction": {
            "aqi": prediction,
            "level": level
        }
    }