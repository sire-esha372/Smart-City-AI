import os
import requests
from dotenv import load_dotenv


# ==========================================
# LOAD ENVIRONMENT VARIABLES
# ==========================================

load_dotenv()

OPENWEATHER_API_KEY = os.getenv(
    "OPENWEATHER_API_KEY"
)


# ==========================================
# GET WEATHER
# ==========================================

def get_weather(city: str):

    # --------------------------------------
    # Validate API key
    # --------------------------------------

    if not OPENWEATHER_API_KEY:

        raise Exception(
            "OPENWEATHER_API_KEY is not configured. "
            "Please add it to your .env file."
        )

    # --------------------------------------
    # Clean city input
    # --------------------------------------

    city = city.strip()

    if not city:

        raise Exception(
            "Please enter a city name."
        )

    # --------------------------------------
    # OpenWeather API
    # --------------------------------------

    url = (
        "https://api.openweathermap.org/"
        "data/2.5/weather"
    )

    params = {
        "q": city,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric"
    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=15
        )

    except requests.exceptions.Timeout:

        raise Exception(
            "Weather service timed out. "
            "Please try again."
        )

    except requests.exceptions.RequestException as e:

        raise Exception(
            f"Unable to connect to weather service: {e}"
        )

    # --------------------------------------
    # Handle API responses
    # --------------------------------------

    if response.status_code == 404:

        raise Exception(
            f"City '{city}' was not found. "
            "Please enter a valid city name."
        )

    if response.status_code == 401:

        raise Exception(
            "Invalid OpenWeather API Key. "
            "Please check OPENWEATHER_API_KEY."
        )

    if response.status_code != 200:

        try:

            error_data = response.json()

            message = error_data.get(
                "message",
                "Unknown weather API error"
            )

        except Exception:

            message = response.text

        raise Exception(
            f"OpenWeather API error: {message}"
        )

    # --------------------------------------
    # Parse response
    # --------------------------------------

    data = response.json()

    weather = data["weather"][0]

    # --------------------------------------
    # Return weather information
    # --------------------------------------

    return {

        "city": data["name"],

        "country": data["sys"]["country"],

        "lat": data["coord"]["lat"],

        "lon": data["coord"]["lon"],

        "temp": data["main"]["temp"],

        "temp_celsius": round(
            float(data["main"]["temp"]),
            1
        ),

        "clouds_all": data["clouds"]["all"],

        "rain_1h": data.get(
            "rain",
            {}
        ).get(
            "1h",
            0
        ),

        "snow_1h": data.get(
            "snow",
            {}
        ).get(
            "1h",
            0
        ),

        "weather_main": weather["main"],

        "weather_description": weather["description"]
    }