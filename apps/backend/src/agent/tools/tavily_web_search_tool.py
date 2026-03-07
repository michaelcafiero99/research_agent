import os
from tavily import TavilyClient
from src.agent.config import settings
from src.agent.logging_config import get_logger

logger = get_logger(__name__)

tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


def search_web(query: str) -> list:
    try:
        response = tavily_client.search(
            query,
            max_results=settings.max_results,
            search_depth=settings.search_depth,
            time_range="w",
        )
        raw_results = response.get("results", [])

        if not raw_results:
            logger.warning("No results found for: %s", query)
            return []

        return [
            {
                "title": res.get("title", "Untitled"),
                "url": res.get("url", "#"),
                "content": res.get("content", "No content found."),
            }
            for res in raw_results
            if isinstance(res, dict)
        ]

    except Exception as e:
        logger.error("Tavily search failed for '%s': %s", query, e)
        return []
