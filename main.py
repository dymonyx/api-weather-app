import os
from fastapi import FastAPI
API_KEY = os.getenv("API_KEY", "unknown")
BASE_URL = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"


app = FastAPI()


@app.get("/info")
def get_info():
    return {
        "version": os.getenv("VERSION", "unknown"),
        "service": "weather",
        "author": "y.lapshina"
    }
