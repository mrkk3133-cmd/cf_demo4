import json
from config import WEATHER_API_KEY, WEATHER_API_URL, DF_PARAM_LOCATION, DF_RESP_PARAM, DF_STATUS_PARAM
from utils import http_get, df_success, BadRequestError, UpstreamError


def handle_getweather(parameters: dict) -> dict:
    """Handler for the 'getweather' webhook tag."""
    location = (parameters.get(DF_PARAM_LOCATION) or "").strip() if parameters else ""
    if not location:
        raise BadRequestError(f"Missing or invalid location in parameter: {DF_PARAM_LOCATION}")

    if not WEATHER_API_KEY:
        raise BadRequestError("WEATHER_API_KEY is not configured")

    # Call upstream Weather API
    resp = http_get(WEATHER_API_URL, {"query": location, "access_key": WEATHER_API_KEY})

    # Validate provider response
    try:
        data = resp.json()
    except ValueError:
        raise UpstreamError("Invalid JSON from weather provider")

    if not isinstance(data, dict) or "current" not in data or "location" not in data:
        # Some providers return error envelopes like {"success":false, "error":{...}}
        provider_msg = (data.get("error") or {}).get("info") if isinstance(data, dict) else None
        raise UpstreamError(f"Invalid response from provider: {provider_msg}")

    current = data["current"] or {}
    loc = data["location"] or {}

    payload = {
        DF_STATUS_PARAM: 200,
        "location": loc.get("name"),
        "region": loc.get("region"),
        "country": loc.get("country"),
        "temperature": f"{current.get('temperature')}°C" if current.get("temperature") is not None else None,
        "feelslike": f"{current.get('feelslike')}°C" if current.get("feelslike") is not None else None,
        "weather_descriptions": ", ".join(current.get("weather_descriptions", []) or []),
        "observation_time": current.get("observation_time"),
    }

    # Return in a DF-friendly envelope under DF_RESP_PARAM
    return df_success({DF_RESP_PARAM: payload})
