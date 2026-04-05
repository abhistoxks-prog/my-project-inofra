import asyncio
import feedparser
from typing import Any, List
from .base_agent import BaseAgent

YAHOO_FINANCE_RSS = "https://finance.yahoo.com/news/rssindex"

MOCK_INDICES = [
    {"name": "S&P 500", "value": 4783.45, "change": 23.12, "change_percent": 0.49},
    {"name": "NASDAQ", "value": 14972.76, "change": -45.33, "change_percent": -0.30},
    {"name": "DOW", "value": 37305.16, "change": 56.81, "change_percent": 0.15},
    {"name": "BTC/USD", "value": 43250.00, "change": 812.50, "change_percent": 1.92},
]


def _parse_finance_feed() -> List[dict]:
    articles = []
    try:
        parsed = feedparser.parse(YAHOO_FINANCE_RSS)
        for entry in parsed.entries[:15]:
            title = getattr(entry, "title", "")
            summary = getattr(entry, "summary", "")
            link = getattr(entry, "link", "")
            published = getattr(entry, "published", "")
            articles.append(
                {
                    "title": title,
                    "link": link,
                    "published": published,
                    "source": "Yahoo Finance",
                    "summary": summary[:300] if summary else "",
                    "type": "market",
                }
            )
    except Exception:
        pass
    return articles


class MarketAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="market",
            description="Tracks financial markets and news via Yahoo Finance RSS",
        )

    async def fetch(self) -> Any:
        loop = asyncio.get_event_loop()
        news = await loop.run_in_executor(None, _parse_finance_feed)
        return {
            "indices": MOCK_INDICES,
            "indices_note": "Demo data for visualization purposes",
            "news": news,
        }
