import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import ssl
from datetime import datetime, timedelta, timezone

def search_arxiv(query: str, max_results: int = 3):
    """
    Searches the Arxiv API for the given query and returns formatted results.
    Only returns papers submitted in the last 2 months, enforced by post-filtering
    the <published> date from the Atom feed (the API date filter is unreliable with
    sortBy=relevance).
    """
    base_url = "http://export.arxiv.org/api/query?"

    cutoff = datetime.now(timezone.utc) - timedelta(days=60)

    # Fetch extra results so we still have enough after the date post-filter
    fetch_count = max_results * 5

    params = {
        "search_query": f"all:{query}",
        "start": 0,
        "max_results": fetch_count,
        "sortBy": "relevance",
        "sortOrder": "descending",
    }

    query_string = urllib.parse.urlencode(params)
    url = base_url + query_string

    try:
        with urllib.request.urlopen(url, context=ssl._create_unverified_context()) as response:
            data = response.read()

        # Parse the Atom XML response
        root = ET.fromstring(data)
        ns = {'atom': 'http://www.w3.org/2005/Atom'}

        formatted_results = []

        for entry in root.findall('atom:entry', ns):
            # Hard date gate — parse <published> which holds the original submission date
            published_elem = entry.find('atom:published', ns)
            if published_elem is not None:
                try:
                    published_dt = datetime.fromisoformat(
                        published_elem.text.strip().replace("Z", "+00:00")
                    )
                    if published_dt < cutoff:
                        continue  # Skip papers older than 2 months
                except ValueError:
                    pass  # If we can't parse the date, let it through

            title_elem = entry.find('atom:title', ns)
            summary_elem = entry.find('atom:summary', ns)
            link_elem = entry.find('atom:id', ns)

            # Clean up text (remove newlines/excess whitespace)
            title = " ".join(title_elem.text.split()) if title_elem is not None else "Untitled"
            summary = " ".join(summary_elem.text.split()) if summary_elem is not None else "No summary."
            paper_url = link_elem.text.strip() if link_elem is not None else "#"

            formatted_results.append({
                "title": title,
                "url": paper_url,
                "content": summary,
            })

            if len(formatted_results) >= max_results:
                break

        if not formatted_results:
            print(f"No recent Arxiv results found for: {query}")

        return formatted_results

    except Exception as e:
        print(f"Arxiv API Error: {e}")
        return []