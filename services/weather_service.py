from typing import List
from fastapi import HTTPException
import requests

from config import API_KEY, BASE_URL
from utils.logger import logger


class WeatherService:
    def __init__(self):
        self.api_key = API_KEY
        self.base_url = BASE_URL

    def get_weather_data(self, city: str, date_from: str, date_to: str) -> dict:
        url = f"{self.base_url}/{city}/{date_from}/{date_to}"
        params = {"key": self.api_key, "unitGroup": "metric"}
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(
                f"Error get weather data: {e}, city: {city}, date_from: {date_from}, date_to: {date_to}")
            raise HTTPException(
                status_code=500, detail="Internal server error.")

    def extract_temperatures(self, data: dict) -> List[float]:
        temps = [
            hour["temp"]
            for day in data.get("days", [])
            for hour in day.get("hours", [])
        ]
        return temps

    def calculate_statistics(self, temperatures: List[float]) -> dict:
        length = len(temperatures)
        avg = round(sum(temperatures) / length, 2)
        median = (
            round((sorted(temperatures)[length // 2] +
                  sorted(temperatures)[length // 2 - 1]) / 2, 2)
            if length % 2 == 0
            else sorted(temperatures)[length // 2]
        )

        return {
            "average": avg,
            "median": median,
            "min": min(temperatures),
            "max": max(temperatures)
        }
