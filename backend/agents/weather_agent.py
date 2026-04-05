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

DEMO_WEATHER = {
    "current": {
        "temperature": 18.4,
        "wind_speed": 12.3,
        "weather_code": 2,
        "weather_description": "Partly cloudy",
    },
    "daily": [
        {"date": "2026-04-05", "temp_max": 21.0, "temp_min": 12.5, "precipitation": 0.0},
        {"date": "2026-04-06", "temp_max": 19.5, "temp_min": 11.0, "precipitation": 2.1},
        {"date": "2026-04-07", "temp_max": 16.8, "temp_min": 10.2, "precipitation": 5.4},
        {"date": "2026-04-08", "temp_max": 14.3, "temp_min": 9.0, "precipitation": 8.2},
        {"date": "2026-04-09", "temp_max": 17.1, "temp_min": 10.5, "precipitation": 0.5},
        {"date": "2026-04-10", "temp_max": 20.4, "temp_min": 12.0, "precipitation": 0.0},
        {"date": "2026-04-11", "temp_max": 22.7, "temp_min": 13.5, "precipitation": 0.0},
    ],
    "location": "New York",
    "demo": True,
}


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
        try:
            async with httpx.AsyncClient(timeout=10) as client:
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
        except Exception:
            # Return demo data when network is unavailable
            demo = dict(DEMO_WEATHER)
            demo["location"] = self.location_name
            return demo
