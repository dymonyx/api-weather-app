import os

API_KEY = os.getenv("API_KEY", None)
BASE_URL = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"
PORT = int(os.getenv("PORT", 8000))
VERSION = os.getenv("VERSION", None)
