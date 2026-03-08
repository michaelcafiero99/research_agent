import urllib.request
import urllib.parse
import urllib.error
import json
import ssl
import time
from datetime import datetime, timedelta

def search_semantic_scholar(query: str, max_results: int = 3):
    """
    Searches Semantic Scholar for papers and returns formatted results using the raw API.
    Only returns papers published in the last 2 months.
    """
    try:
        # Create unverified context to avoid SSL errors
        context = ssl._create_unverified_context()

        base_url = "https://api.semanticscholar.org/graph/v1/paper/search"

        # Define the fields we want to retrieve
        fields = "title,url,citationCount,influentialCitationCount,tldr,year,paperId,publicationDate"

        # Date range: last 2 months
        end = datetime.utcnow()
        start = end - timedelta(days=60)

        params = {
            "query": query,
            "limit": max_results,
            "fields": fields,
            "publicationDateOrYear": f"{start.strftime('%Y-%m-%d')}:{end.strftime('%Y-%m-%d')}",
        }
        
        query_string = urllib.parse.urlencode(params)
        url = f"{base_url}?{query_string}"
        
        data = {}
        for attempt in range(3):
            try:
                with urllib.request.urlopen(url, context=context) as response:
                    data = json.loads(response.read().decode())
                break
            except urllib.error.HTTPError as e:
                if e.code == 429 and attempt < 2:
                    time.sleep(2 ** (attempt + 1)) # Backoff: 2s, 4s
                    continue
                raise e
            
        results = data.get("data", [])
        formatted_results = []
        
        for paper in results:
            title = paper.get('title', 'Untitled')
            url = paper.get('url')
            paper_id = paper.get('paperId')
            
            # Fallback URL construction
            if not url and paper_id:
                 url = f"https://www.semanticscholar.org/paper/{paper_id}"
            
            tldr_obj = paper.get('tldr')
            tldr = tldr_obj.get('text') if tldr_obj else "No TLDR available."
            
            citations = paper.get('citationCount', 0)
            influential = paper.get('influentialCitationCount', 0)
            year = paper.get('year', 'Unknown')
            
            # Combine metrics into the content field for the report
            content = f"Year: {year} | Citations: {citations} (Influential: {influential}) | TLDR: {tldr}"
            
            formatted_results.append({
                "title": title,
                "url": url,
                "content": content
            })
            
        return formatted_results

    except Exception as e:
        print(f"Semantic Scholar Error: {e}")
        return []