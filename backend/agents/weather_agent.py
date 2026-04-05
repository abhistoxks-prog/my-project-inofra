import httpx
from typing import Any
from .base_agent import BaseAgent

WMO_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Foggy",
    48: "Icy fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    71: "Slight snow",
    73: "Moderate snow",
    75: "Heavy snow",
    77: "Snow grains",
    80: "Slight showers",
    81: "Moderate showers",
    82: "Violent showers",
    85: "Slight snow showers",
    86: "Heavy snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm with hail",
    99: "Thunderstorm with heavy hail",
}

BASE_URL = "https://api.open-meteo.com/v1/forecast"


class WeatherAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="weather",
            description="Provides real-time weather and 7-day forecast via Open-Meteo",
        )
        self.lat: float = 40.71
        self.lon: float = -74.01
        self.location_name: str = "New York"

    def set_location(self, lat: float, lon: float, name: str) -> None:
        self.lat = lat
        self.lon = lon
        self.location_name = name

    async def fetch(self) -> Any:
        params = {
            "latitude": self.lat,
            "longitude": self.lon,
            "current": "temperature_2m,wind_speed_10m,weather_code",
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
            "timezone": "auto",
        }
        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.get(BASE_URL, params=params)
            resp.raise_for_status()
            data = resp.json()

        current = data.get("current", {})
        daily = data.get("daily", {})

        weather_code = current.get("weather_code", 0)
        forecast = []
        dates = daily.get("time", [])
        for i, date in enumerate(dates):
            forecast.append(
                {
                    "date": date,
                    "temp_max": daily.get("temperature_2m_max", [])[i]
                    if i < len(daily.get("temperature_2m_max", []))
                    else None,
                    "temp_min": daily.get("temperature_2m_min", [])[i]
                    if i < len(daily.get("temperature_2m_min", []))
                    else None,
                    "precipitation": daily.get("precipitation_sum", [])[i]
                    if i < len(daily.get("precipitation_sum", []))
                    else None,
                }
            )

        return {
            "current": {
                "temperature": current.get("temperature_2m"),
                "wind_speed": current.get("wind_speed_10m"),
                "weather_code": weather_code,
                "weather_description": WMO_CODES.get(weather_code, "Unknown"),
            },
            "daily": forecast,
            "location": self.location_name,
        }
