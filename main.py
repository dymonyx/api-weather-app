import os
from fastapi import FastAPI, HTTPException, Query
from typing import List, Dict, Any
import requests
from datetime import datetime, timedelta
import uvicorn

API_KEY = os.getenv("API_KEY", "unknown")
BASE_URL = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"
PORT = int(os.getenv("PORT", 8000))


class WeatherService:
    def __init__(self, api_key: str, base_url: str):
        self.api_key = api_key
        self.base_url = base_url

    def get_weather_data(self, city: str, date_from: str, date_to: str) -> dict:
        url = f"{self.base_url}/{city}/{date_from}/{date_to}"
        params = {"key": self.api_key, "unitGroup": "metric"}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def extract_temperatures(self, data: dict) -> List[float]:
        temps = [
            hour["temp"]
            for day in data.get("days", [])
            for hour in day.get("hours", [])
        ]
        return temps

    def calculate_statistics(self, temperatures: List[float]) -> dict:
        temperatures.sort()
        length = len(temperatures)
        avg = round(sum(temperatures) / length, 2)
        median = (
            round((temperatures[length // 2] +
                  temperatures[length // 2 - 1]) / 2, 2)
            if length % 2 == 0
            else temperatures[length // 2]
        )

        return {
            "average": avg,
            "median": median,
            "min": min(temperatures),
            "max": max(temperatures)
        }


app = FastAPI()
weather_service = WeatherService(api_key=API_KEY, base_url=BASE_URL)


@app.get("/info")
def get_info():
    return {
        "version": os.getenv("VERSION", "unknown"),
        "service": "weather",
        "author": "y.lapshina"
    }


@app.get("/info/weather")
def get_weather(
        city: str = Query(...),
        date_from: str = Query(
            default=(datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")),
        date_to: str = Query(default=datetime.today().strftime("%Y-%m-%d"))) -> Dict[str, Any]:
    try:
        data = weather_service.get_weather_data(city, date_from, date_to)
        temperatures = weather_service.extract_temperatures(data)
        stats = weather_service.calculate_statistics(temperatures)

        return {
            "service": "weather",
            "data": {
                "temperature_c": stats
            },
        }
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Weather API error: {e}")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT)
