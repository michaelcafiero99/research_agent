import os
from tavily import TavilyClient

tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def search_web(query: str):
    try:
        # time_range options: "d" (day), "w" (week), "m" (month), "y" (year)
        response = tavily_client.search(query, max_results=3, search_depth="basic", time_range="w")
        raw_results = response.get("results", [])

        if not raw_results:
            print(f"No results found for: {query}")
            return []

        formatted = []
        for res in raw_results:

            if isinstance(res, dict):
                formatted.append({
                    "title": res.get("title", "Untitled"),
                    "url": res.get("url", "#"),
                    "content": res.get("content", "No content found."),
                })
        return formatted
        
    except Exception as e:
        print(f" Tavily Error: {e}")
        return []