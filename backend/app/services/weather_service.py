import os

API_KEY = os.getenv("OPENWEATHER_API_KEY")
def get_weather(city: str):

    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": city,
        "appid": OPENWEATHER_API_KEY
    }

    response = requests.get(
        url,
        params=params,
        timeout=10
    )

    if response.status_code == 404:
        raise Exception("City not found.")

    if response.status_code == 401:
        raise Exception("Invalid OpenWeather API Key.")

    if response.status_code != 200:
        raise Exception(response.text)

    data = response.json()

    weather = data["weather"][0]

    return {

        "city": data["name"],

        "country": data["sys"]["country"],

        "lat": data["coord"]["lat"],

        "lon": data["coord"]["lon"],

        "temp": data["main"]["temp"],

        "temp_celsius": round(
            data["main"]["temp"] - 273.15,
            1
        ),

        "clouds_all": data["clouds"]["all"],

        "rain_1h": data.get("rain", {}).get("1h", 0),

        "snow_1h": data.get("snow", {}).get("1h", 0),

        "weather_main": weather["main"],

        "weather_description": weather["description"]
    }