import os
from typing import List, Dict
# Try this instead
from langchain_community.tools.tavily_search import TavilySearchResults


tavily_engine = TavilySearchResults(max_results=3, search_depth="basic")

def search_web(query: str):
    try:
        # Run the search
        raw_results = tavily_engine.invoke({"query": query})

        if not raw_results:
            print(f"No results found for: {query}")
            return []

        formatted = []
        for res in raw_results:
            # Handle cases where result might be a string or a dict
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