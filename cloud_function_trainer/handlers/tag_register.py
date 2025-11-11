from handlers.weather_handler import handle_getweather


# Register handlers by webhook tag
HANDLERS = {
    "getweather": handle_getweather,
}