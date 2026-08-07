from datetime import datetime

from ..database.database import SessionLocal
from ..database.crud import save_prediction

from ..ml_models.traffic_model import (
    predict,
    encode_holiday,
    encode_weather_main,
    encode_weather_description
)

from .weather_service import get_weather


def predict_traffic(data):

    weather = get_weather(data.city)

    selected_datetime = datetime.strptime(
        f"{data.date} {data.time}",
        "%Y-%m-%d %H:%M"
    )

    hour = selected_datetime.hour
    day = selected_datetime.day
    month = selected_datetime.month
    weekday = selected_datetime.weekday()

    holiday = "None"

    features = [
        encode_holiday(holiday),
        weather["temp"],
        weather["rain_1h"],
        weather["snow_1h"],
        weather["clouds_all"],
        encode_weather_main(weather["weather_main"]),
        encode_weather_description(weather["weather_description"]),
        hour,
        day,
        month,
        weekday
    ]

    prediction = round(float(predict(features)), 2)

    if prediction < 2000:
        level = "Low"
    elif prediction < 4000:
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
            module="Traffic",
            status=level,
            value=f"{prediction} Vehicles/hr"
        )
    finally:
        db.close()

    return {
        "success": True,
        "location": {
            "city": weather["city"],
            "country": weather["country"]
        },
        "weather": {
            "temperature": weather["temp_celsius"],
            "weather": weather["weather_main"],
            "description": weather["weather_description"],
            "clouds": weather["clouds_all"],
            "rain": weather["rain_1h"]
        },
        "prediction": {
            "traffic_volume": prediction,
            "traffic_level": level
        }
    }