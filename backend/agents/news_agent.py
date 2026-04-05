import asyncio
import feedparser
from typing import Any, List, Optional
from .base_agent import BaseAgent

RSS_FEEDS = [
    {"url": "http://feeds.bbci.co.uk/news/rss.xml", "source": "BBC News"},
    {"url": "https://feeds.reuters.com/reuters/topNews", "source": "Reuters"},
    {"url": "http://rss.cnn.com/rss/edition.rss", "source": "CNN"},
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
        articles.sort(key=lambda a: a.get("published", ""), reverse=True)
        return articles
