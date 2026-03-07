import json
import urllib.request
import concurrent.futures
import ssl

def get_item(item_id, context):
    """Fetches a single item from the HN API."""
    url = f"https://hacker-news.firebaseio.com/v0/item/{item_id}.json"
    try:
        with urllib.request.urlopen(url, context=context) as response:
            if response.status == 200:
                return json.loads(response.read().decode())
    except Exception:
        return None
    return None

def search_hackernews(query: str, max_results: int = 3):
    """
    Fetches top stories from Hacker News.
    Ignores the query to return the most trending topics.
    """
    # Create unverified context to avoid SSL errors on some systems
    context = ssl._create_unverified_context()
    
    top_stories_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    
    try:
        with urllib.request.urlopen(top_stories_url, context=context) as response:
            ids = json.loads(response.read().decode())
    except Exception as e:
        print(f"HN API Error: {e}")
        return []

    # Fetch a few more than max_results in case some are not stories (e.g. jobs)
    ids_to_check = ids[:max_results + 5]
    
    results = []
    
    # Use threads to fetch item details in parallel for speed
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_id = {executor.submit(get_item, item_id, context): item_id for item_id in ids_to_check}
        
        for future in concurrent.futures.as_completed(future_to_id):
            item = future.result()
            if not item or item.get('type') != 'story':
                continue
            
            title = item.get('title', 'Untitled')
            
            # Return top stories regardless of query
            results.append({
                "title": title,
                "url": item.get('url', f"https://news.ycombinator.com/item?id={item['id']}"),
                "content": f"Hacker News Story. Score: {item.get('score', 0)} | Comments: {item.get('descendants', 0)}"
            })
            
            if len(results) >= max_results:
                break
    
    return results[:max_results]