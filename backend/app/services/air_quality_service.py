import requests

from .weather_service import get_weather

import os

API_KEY = os.getenv("OPENWEATHER_API_KEY")


def get_air_quality(city: str):

    # Get latitude & longitude
    weather = get_weather(city)

    lat = weather["lat"]
    lon = weather["lon"]

    url = "https://api.openweathermap.org/data/2.5/air_pollution"

    params = {
    "lat": lat,
    "lon": lon,
    "appid": API_KEY
}

    response = requests.get(
        url,
        params=params,
        timeout=10
    )

    if response.status_code != 200:
        raise Exception(
            f"Air Quality API Error: {response.text}"
        )

    data = response.json()

    components = data["list"][0]["components"]

    return {

        "city": weather["city"],
        "country": weather["country"],

        "PM2_5": components.get("pm2_5", 0),
        "PM10": components.get("pm10", 0),
        "NO": components.get("no", 0),
        "NO2": components.get("no2", 0),
        "NH3": components.get("nh3", 0),
        "CO": components.get("co", 0),
        "SO2": components.get("so2", 0),
        "O3": components.get("o3", 0),

        # Estimated values for your existing model
        "NOx": components.get("no", 0) + components.get("no2", 0),
        "Benzene": 0,
        "Toluene": 0
    }