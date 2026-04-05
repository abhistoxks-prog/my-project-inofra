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

DEMO_MARKET_NEWS = [
    {
        "title": "Fed Signals Potential Rate Cuts in Second Half of 2026",
        "link": "https://example.com/fed-rate-cuts",
        "published": "Sun, 05 Apr 2026 11:00:00 +0000",
        "source": "Yahoo Finance",
        "summary": "Federal Reserve officials signaled openness to cutting interest rates in the second half of 2026 if inflation continues its downward trend toward the 2% target.",
        "type": "market",
    },
    {
        "title": "Tech Giants Report Record Q1 Earnings, Beating Analyst Expectations",
        "link": "https://example.com/tech-earnings",
        "published": "Sat, 04 Apr 2026 17:00:00 +0000",
        "source": "Yahoo Finance",
        "summary": "Major technology companies reported record first-quarter earnings this week, with combined profits up 34% year-over-year, driven by AI infrastructure spending and cloud services growth.",
        "type": "market",
    },
    {
        "title": "Oil Prices Stabilize as OPEC+ Agrees to Maintain Production Cuts",
        "link": "https://example.com/oil-opec",
        "published": "Fri, 03 Apr 2026 15:00:00 +0000",
        "source": "Yahoo Finance",
        "summary": "OPEC+ members agreed to maintain their current production cut agreement through Q3 2026, providing stability to crude oil markets after weeks of volatility driven by geopolitical uncertainty.",
        "type": "market",
    },
    {
        "title": "Electric Vehicle Sales Surpass Internal Combustion for First Time in Europe",
        "link": "https://example.com/ev-sales-europe",
        "published": "Fri, 03 Apr 2026 09:00:00 +0000",
        "source": "Yahoo Finance",
        "summary": "Electric vehicle registrations in the European Union exceeded those of gasoline and diesel vehicles for the first time in Q1 2026, marking a historic milestone in the automotive industry transition.",
        "type": "market",
    },
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
        if not news:
            news = DEMO_MARKET_NEWS
        return {
            "indices": MOCK_INDICES,
            "indices_note": "Demo data for visualization purposes",
            "news": news,
        }
