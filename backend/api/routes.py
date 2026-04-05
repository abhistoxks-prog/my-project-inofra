from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from agents.agent_manager import AgentManager

router = APIRouter()
manager: Optional[AgentManager] = None


def set_manager(m: AgentManager) -> None:
    global manager
    manager = m


class ConfigUpdate(BaseModel):
    topics: Optional[List[str]] = None
    location: Optional[dict] = None
    refresh_interval: Optional[int] = None


@router.get("/agents")
async def list_agents():
    return {"agents": manager.get_status()}


@router.get("/agents/{name}/run")
async def run_agent(name: str):
    try:
        result = await manager.run_agent(name)
        return {"status": "success", "agent": name, "result": result}
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/agents/{name}/results")
async def agent_results(name: str):
    result = manager.get_agent_result(name)
    if result is None:
        raise HTTPException(status_code=404, detail="No results yet for this agent")
    return {"agent": name, "result": result}


@router.get("/feed")
async def get_feed():
    results = manager.get_results()
    feed_items = []

    news = results.get("news", [])
    if isinstance(news, list):
        feed_items.extend(news)

    market = results.get("market", {})
    if isinstance(market, dict):
        feed_items.extend(market.get("news", []))

    feed_items.sort(key=lambda x: x.get("published", ""), reverse=True)
    return {"items": feed_items, "total": len(feed_items)}


@router.get("/weather")
async def get_weather():
    result = manager.get_agent_result("weather")
    if result is None:
        try:
            result = await manager.run_agent("weather")
        except Exception as exc:
            raise HTTPException(status_code=503, detail=str(exc))
    return result


@router.get("/status")
async def system_status():
    agents = manager.get_status()
    results = manager.get_results()
    return {
        "agents": agents,
        "data_available": list(results.keys()),
        "total_feed_items": len(results.get("news", []))
        + len((results.get("market") or {}).get("news", [])),
    }


@router.get("/config")
async def get_config():
    return manager.get_config()


@router.post("/config")
async def update_config(config: ConfigUpdate):
    updates: dict = {}
    if config.topics is not None:
        updates["topics"] = config.topics
    if config.location is not None:
        updates["location"] = config.location
    if config.refresh_interval is not None:
        updates["refresh_interval"] = config.refresh_interval
    manager.update_config(updates)
    return {"status": "updated", "config": manager.get_config()}
