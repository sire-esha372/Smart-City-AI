from fastapi import APIRouter
import joblib
import pandas as pd
from pathlib import Path
from datetime import datetime

from ..database.database import SessionLocal
from ..database.crud import save_prediction

from ..schemas.power_schema import PowerInput

router = APIRouter(
    prefix="/predict",
    tags=["Power Prediction"]
)

# Load trained model
MODEL_PATH = Path(__file__).parent.parent / "ml_models" / "power_model.pkl"
power_model = joblib.load(MODEL_PATH)


@router.post("/power")
def predict_power(data: PowerInput):

    dt = datetime.strptime(
        f"{data.date} {data.time}",
        "%Y-%m-%d %H:%M"
    )

    year = dt.year
    month = dt.month
    day = dt.day
    hour = dt.hour
    day_of_week = dt.weekday()

    quarter = (month - 1) // 3 + 1

    is_weekend = 1 if day_of_week >= 5 else 0

    input_data = pd.DataFrame([{
        "Year": year,
        "Month": month,
        "Day": day,
        "Hour": hour,
        "DayOfWeek": day_of_week,
        "Quarter": quarter,
        "IsWeekend": is_weekend
    }])

    prediction = power_model.predict(input_data)[0]

    if prediction < 15000:
        level = "Low"

    elif prediction < 25000:
        level = "Medium"

    else:
        level = "High"

    # ==========================================
    # SAVE TO DATABASE
    # ==========================================

    db = SessionLocal()

    try:
        save_prediction(
            db=db,
            module="Energy",
            status=level,
            value=f"{round(float(prediction), 2)} MW"
        )
    finally:
        db.close()

    return {
        "success": True,
        "prediction": {
            "power_consumption": round(float(prediction), 2),
            "level": level
        }
    }