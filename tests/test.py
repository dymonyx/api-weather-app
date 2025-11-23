import pytest
import requests
from typing import List, Dict, Any
from fastapi.testclient import TestClient
from main import app
import services.weather_service as weather_service

client = TestClient(app)


class DummyResponse:
    def __init__(self, status_code: int = 200, json_data: Dict[str, Any] | None = None):
        self.status_code = status_code
        self._json_data = json_data or {}

    def json(self) -> Dict[str, Any]:
        return self._json_data

    def raise_for_status(self) -> None:
        if self.status_code >= 400:
            raise requests.exceptions.HTTPError(f"Status code: {self.status_code}")


def patch_requests_get_success(monkeypatch, recorded_calls: List[Dict[str, Any]]):
    def _fake_get(url, params=None, timeout=None):
        recorded_calls.append({"url": url, "params": params, "timeout": timeout})
        return DummyResponse(
            status_code=200,
            json_data={
                "days": [
                    {"hours": [{"temp": 10.0}]},
                    {"hours": [{"temp": 20.0}]},
                    {"hours": [{"temp": 30.0}]},
                ]
            },
        )
    monkeypatch.setattr(weather_service.requests, "get", _fake_get)


def patch_requests_get_error(monkeypatch):
    def _fake_get(url, params=None, timeout=None):
        raise requests.exceptions.RequestException("upstream error")
    monkeypatch.setattr(weather_service.requests, "get", _fake_get)


def test_info_returns_metadata():
    response = client.get("/info")
    assert response.status_code == 200
    body = response.json()
    assert body["service"] == "weather"
    assert "version" in body
    assert "author" in body


def test_weather_stats_integration_success(monkeypatch):
    recorded_calls: List[Dict[str, Any]] = []
    patch_requests_get_success(monkeypatch, recorded_calls)

    response = client.get(
        "/info/weather",
        params={
            "city": "Berlin",
            "date_from": "2024-02-19",
            "date_to": "2024-02-21",
        },
    )

    assert response.status_code == 200
    body = response.json()

    stats = body["data"]["temperature_c"]

    assert stats["min"] == pytest.approx(10.0)
    assert stats["max"] == pytest.approx(30.0)
    assert stats["average"] == pytest.approx(20.0)
    assert stats["median"] == pytest.approx(20.0)

    assert len(recorded_calls) == 1
    call = recorded_calls[0]
    assert "Berlin" in call["url"]


def test_weather_default_dates_propagated_to_external_api(monkeypatch):
    recorded_calls: List[Dict[str, Any]] = []
    patch_requests_get_success(monkeypatch, recorded_calls)

    response = client.get("/info/weather", params={"city": "Berlin"})
    assert response.status_code == 200

    call = recorded_calls[0]
    url = call["url"]

    assert "Berlin" in url
    after_city = url.split("Berlin/")[1]
    assert "/" in after_city


def test_weather_requires_city_query_param():
    response = client.get("/info/weather")
    assert response.status_code == 422
    body = response.json()
    assert "detail" in body
    assert any("city" in str(err["loc"]) for err in body["detail"])


def test_weather_handles_external_api_error(monkeypatch):
    patch_requests_get_error(monkeypatch)

    response = client.get(
        "/info/weather",
        params={
            "city": "Berlin",
            "date_from": "2024-02-19",
            "date_to": "2024-02-21",
        },
    )

    assert response.status_code == 500
    body = response.json()
    assert "detail" in body
