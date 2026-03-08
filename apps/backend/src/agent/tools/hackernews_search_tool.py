import json
import urllib.request
import urllib.parse
import ssl

def search_hackernews(query: str, max_results: int = 3):
    """
    Searches Hacker News stories using the Algolia HN Search API.
    """
    context = ssl._create_unverified_context()
    params = urllib.parse.urlencode({
        "query": query,
        "tags": "story",
        "hitsPerPage": max_results,
    })
    url = f"https://hn.algolia.com/api/v1/search?{params}"

    try:
        with urllib.request.urlopen(url, context=context) as response:
            data = json.loads(response.read().decode())
    except Exception as e:
        print(f"HN API Error: {e}")
        return []

    results = []
    for hit in data.get("hits", []):
        results.append({
            "title": hit.get("title", "Untitled"),
            "url": hit.get("url") or f"https://news.ycombinator.com/item?id={hit.get('objectID')}",
            "content": f"Hacker News Story. Points: {hit.get('points', 0)} | Comments: {hit.get('num_comments', 0)}",
        })

    return results
