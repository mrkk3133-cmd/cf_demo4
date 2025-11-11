import os
from dotenv import load_dotenv

# Load .env for local development. In production, rely on real env vars.
load_dotenv()

# Environment configuration
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
WEATHER_API_URL = os.getenv("WEATHER_API_URL", "https://api.weatherstack.com/current")

# Dialogflow parameter names (customize via .env without touching code)
DF_PARAM_LOCATION = os.getenv("DF_PARAM_LOCATION", "p_location")
DF_RESP_PARAM = os.getenv("DF_RESP_PARAM", "getWeather_resp")
DF_STATUS_PARAM = os.getenv("DF_STATUS_PARAM", "weather_api_status")

