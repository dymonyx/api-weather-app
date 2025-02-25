from datetime import datetime, timedelta, date
from typing import Any, Dict
from fastapi import APIRouter, HTTPException, Query
import requests

from utils.logger import logger
from config import VERSION
from services.weather_service import WeatherService


weather_router = APIRouter()
weather_service = WeatherService()


@weather_router.get("/info")
def get_info():
    return {
        "version": VERSION,
        "service": "weather",
        "author": "y.lapshina"
    }


@weather_router.get("/info/weather")
def get_weather(
        city: str = Query(...),
        date_from: date = Query(
            default_factory=lambda: (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")),
        date_to: date = Query(default_factory=lambda: datetime.today().strftime("%Y-%m-%d"))) -> Dict[str, Any]:
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
        logger.error(
            f"Error get weather data: {e}, city: {city}, date_from: {date_from}, date_to: {date_to}")
        raise HTTPException(
            status_code=500, detail="Internal server error.")
