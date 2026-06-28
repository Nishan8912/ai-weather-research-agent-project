from langchain_core.tools import tool
import requests

@tool
def get_weather(city: str) -> str:
    """Fetch current weather conditions for a given city."""
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
    geo = requests.get(geo_url).json()

    if not geo.get("results"):
        return f"Could not find location: {city}"

    lat = geo["results"][0]["latitude"]
    lon = geo["results"][0]["longitude"]
    name = geo["results"][0]["name"]
    country = geo["results"][0].get("country", "")

    weather_url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        f"&current_weather=true"
        f"&hourly=relative_humidity_2m,apparent_temperature"
    )
    data = requests.get(weather_url).json()
    w = data["current_weather"]

    return (
        f"Weather in {name}, {country}:\n"
        f"Temperature: {w['temperature']}°C\n"
        f"Wind Speed: {w['windspeed']} km/h\n"
        f"Wind Direction: {w['winddirection']}°\n"
        f"Weather Code: {w['weathercode']}"
    )
