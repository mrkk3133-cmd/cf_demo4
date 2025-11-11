import time
import logging
import requests

# --- Minimal custom errors for clean control flow ---
class BadRequestError(Exception):
    pass

class UpstreamError(Exception):
    pass

# --- Dialogflow CX response helpers ---
def df_success(parameters: dict) -> dict:
    return {"sessionInfo": {"parameters": parameters}}

def df_error(status: int, message: str, extra_params: dict | None = None) -> dict:
    params = {"weather_api_status": status, "message": message}
    if extra_params:
        params.update(extra_params)
    return {"sessionInfo": {"parameters": params}}

# --- Lightweight HTTP GET with retries ---
def http_get(url: str, params: dict, timeout: float = 10.0, retries: int = 2, backoff: float = 0.6):
    """Simple GET with basic retry/backoff. Raises UpstreamError after retries."""
    logger = logging.getLogger("dfcx-webhook")
    last_exc = None
    for attempt in range(1, retries + 2):  # e.g., retries=2 -> attempts: 1,2,3
        try:
            resp = requests.get(url, params=params, timeout=timeout)
            return resp
        except requests.RequestException as exc:
            last_exc = exc
            sleep_for = backoff * attempt
            logger.warning("GET failed (attempt %s). Retrying in %.1fs", attempt, sleep_for)
            time.sleep(sleep_for)
    raise UpstreamError(f"Upstream request failed after retries: {last_exc}")