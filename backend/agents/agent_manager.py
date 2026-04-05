import asyncio
from typing import Any, Dict, List, Optional
from .news_agent import NewsAgent
from .weather_agent import WeatherAgent
from .market_agent import MarketAgent


class AgentManager:
    def __init__(self):
        self.news_agent = NewsAgent()
        self.weather_agent = WeatherAgent()
        self.market_agent = MarketAgent()
        self._agents = {
            "news": self.news_agent,
            "weather": self.weather_agent,
            "market": self.market_agent,
        }
        self._results: Dict[str, Any] = {}
        self._config: Dict[str, Any] = {
            "topics": [],
            "location": {"lat": 40.71, "lon": -74.01, "name": "New York"},
            "refresh_interval": 300,
        }
        self._refresh_task: Optional[asyncio.Task] = None

    def apply_config(self) -> None:
        self.news_agent.set_topics(self._config["topics"])
        loc = self._config["location"]
        self.weather_agent.set_location(loc["lat"], loc["lon"], loc["name"])

    async def run_all(self) -> Dict[str, Any]:
        results = await asyncio.gather(
            *[agent.run() for agent in self._agents.values()],
            return_exceptions=True,
        )
        for name, result in zip(self._agents.keys(), results):
            if not isinstance(result, Exception):
                self._results[name] = result
        return self._results

    async def run_agent(self, name: str) -> Any:
        agent = self._agents.get(name)
        if agent is None:
            raise ValueError(f"Unknown agent: {name}")
        result = await agent.run()
        self._results[name] = result
        return result

    def get_status(self) -> List[dict]:
        return [agent.get_info() for agent in self._agents.values()]

    def get_results(self) -> Dict[str, Any]:
        return self._results

    def get_agent_result(self, name: str) -> Any:
        return self._results.get(name)

    def get_config(self) -> Dict[str, Any]:
        return self._config

    def update_config(self, config: Dict[str, Any]) -> None:
        self._config.update(config)
        self.apply_config()

    async def _background_refresh(self) -> None:
        while True:
            try:
                interval = self._config.get("refresh_interval", 300)
                await asyncio.sleep(interval)
                await self.run_all()
            except asyncio.CancelledError:
                break
            except Exception:
                pass

    def start_background_refresh(self) -> None:
        self._refresh_task = asyncio.create_task(self._background_refresh())

    def stop_background_refresh(self) -> None:
        if self._refresh_task:
            self._refresh_task.cancel()
