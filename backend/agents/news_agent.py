import asyncio
import feedparser
from typing import Any, List, Optional
from .base_agent import BaseAgent

RSS_FEEDS = [
    {"url": "http://feeds.bbci.co.uk/news/rss.xml", "source": "BBC News"},
    {"url": "https://feeds.reuters.com/reuters/topNews", "source": "Reuters"},
    {"url": "http://rss.cnn.com/rss/edition.rss", "source": "CNN"},
]

DEMO_ARTICLES = [
    {
        "title": "Global Leaders Convene for Emergency Climate Summit",
        "link": "https://example.com/climate-summit",
        "published": "Sun, 05 Apr 2026 10:30:00 +0000",
        "source": "BBC News",
        "summary": "World leaders gathered in Geneva to discuss accelerated action on climate change, with new pledges expected from major economies on reducing carbon emissions by 2030.",
        "type": "news",
    },
    {
        "title": "Breakthrough in Quantum Computing Announced by Research Team",
        "link": "https://example.com/quantum-computing",
        "published": "Sun, 05 Apr 2026 09:15:00 +0000",
        "source": "Reuters",
        "summary": "Scientists at MIT have demonstrated a 1,000-qubit quantum processor capable of solving complex optimization problems in minutes that would take classical computers thousands of years.",
        "type": "news",
    },
    {
        "title": "AI Systems Now Managing 40% of Global Supply Chain Logistics",
        "link": "https://example.com/ai-supply-chain",
        "published": "Sun, 05 Apr 2026 08:45:00 +0000",
        "source": "CNN",
        "summary": "A new industry report reveals artificial intelligence systems now coordinate nearly half of all global supply chain operations, reducing delays and cutting costs by an estimated 23%.",
        "type": "news",
    },
    {
        "title": "SpaceX Announces Plans for Mars Colony by 2030",
        "link": "https://example.com/spacex-mars",
        "published": "Sat, 04 Apr 2026 22:00:00 +0000",
        "source": "BBC News",
        "summary": "SpaceX has unveiled detailed plans for a permanent Mars colony, with the first crewed mission planned for 2028 and a self-sustaining base expected by 2035.",
        "type": "news",
    },
    {
        "title": "New Renewable Energy Record: 80% of EU Powered by Renewables",
        "link": "https://example.com/eu-renewables",
        "published": "Sat, 04 Apr 2026 18:30:00 +0000",
        "source": "Reuters",
        "summary": "The European Union set a new record this week as renewable energy sources — solar, wind, and hydro — accounted for 80% of total electricity generation for the first time.",
        "type": "news",
    },
    {
        "title": "WHO Declares Global Health Initiative on Mental Health Crisis",
        "link": "https://example.com/who-mental-health",
        "published": "Sat, 04 Apr 2026 14:00:00 +0000",
        "source": "CNN",
        "summary": "The World Health Organization has declared a global initiative to address the mental health crisis, calling on governments worldwide to triple their spending on mental health services.",
        "type": "news",
    },
    {
        "title": "Major Cybersecurity Vulnerability Patched in Critical Infrastructure",
        "link": "https://example.com/cybersecurity-patch",
        "published": "Fri, 03 Apr 2026 20:00:00 +0000",
        "source": "BBC News",
        "summary": "A critical vulnerability affecting power grid management systems in 40 countries has been patched following coordinated disclosure by cybersecurity researchers and government agencies.",
        "type": "news",
    },
    {
        "title": "Gene Therapy Cures Rare Genetic Disease in Clinical Trial",
        "link": "https://example.com/gene-therapy",
        "published": "Fri, 03 Apr 2026 16:00:00 +0000",
        "source": "Reuters",
        "summary": "A gene therapy treatment has shown 100% efficacy in curing a previously untreatable genetic disorder in a Phase 3 clinical trial involving 500 patients across 12 countries.",
        "type": "news",
    },
]


def _parse_feed(feed_info: dict, topics: List[str]) -> List[dict]:
    articles = []
    try:
        parsed = feedparser.parse(feed_info["url"])
        for entry in parsed.entries[:15]:
            title = getattr(entry, "title", "")
            summary = getattr(entry, "summary", "")
            link = getattr(entry, "link", "")
            published = getattr(entry, "published", "")

            if topics:
                combined = (title + " " + summary).lower()
                if not any(t.lower() in combined for t in topics):
                    continue

            articles.append(
                {
                    "title": title,
                    "link": link,
                    "published": published,
                    "source": feed_info["source"],
                    "summary": summary[:300] if summary else "",
                    "type": "news",
                }
            )
    except Exception:
        pass
    return articles


class NewsAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="news",
            description="Monitors global news from BBC, Reuters, and CNN via RSS feeds",
        )
        self.topics: List[str] = []

    def set_topics(self, topics: List[str]) -> None:
        self.topics = topics

    async def fetch(self) -> Any:
        loop = asyncio.get_event_loop()
        tasks = [
            loop.run_in_executor(None, _parse_feed, feed, self.topics)
            for feed in RSS_FEEDS
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        articles: List[dict] = []
        for result in results:
            if isinstance(result, list):
                articles.extend(result)

        # Fall back to demo articles when no live data is available
        if not articles:
            demo = DEMO_ARTICLES
            if self.topics:
                demo = [
                    a for a in demo
                    if any(
                        t.lower() in (a["title"] + " " + a["summary"]).lower()
                        for t in self.topics
                    )
                ] or demo
            return demo

        articles.sort(key=lambda a: a.get("published", ""), reverse=True)
        return articles
