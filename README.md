# FastAPI Weather Service

## Overview
This is a FastAPI-based weather service that retrieves weather data from the Visual Crossing Weather API. It provides temperature statistics for a given city and date range.

## Features
- Fetches weather data for a specified city and date range.
- Calculates temperature statistics (average, median, min, max).
- Uses environment variables for API configuration.
- Provides basic service information.

## Endpoints

### `GET /info`
Returns basic service information.

#### Response:
```json
{
    "version": "0.1.0",
    "service": "weather",
    "author": "y.lapshina"
}
```

### `GET /info/weather`
Retrieves weather statistics for a given city and date range.

#### Query Parameters:
- `city` (str, required): Country, city, address or coordinates.
- `date_from` (date*, optional): Start date (default: yesterday).
- `date_to` (date*, optional): End date (default: today).

*class from datetime

#### Example Request:
```bash
curl 'http://localhost:8000/info/weather?city=Saint-Petersburg&date_from=2024-02-19&date_to=2024-02-20'

```

#### Example Response:
```json
{
  "service": "weather",
  "data": {
    "temperature_c": {
      "average": -4.120833333333334,
      "median": -3,
      "min": -11,
      "max": -0.9
    }
  }
}
```

## **Requirements**
- Python 3.12
- `fastapi`, `Requests`


## Environment Variables
- `API_KEY`: The API key for Visual Crossing Weather API (required).
- `VERSION`: Application version (optional).
- `PORT`: Application port.