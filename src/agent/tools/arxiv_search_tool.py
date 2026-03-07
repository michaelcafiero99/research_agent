import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import ssl

def search_arxiv(query: str, max_results: int = 3):
    """
    Searches the Arxiv API for the given query and returns formatted results.
    """
    base_url = "http://export.arxiv.org/api/query?"
    
    # "all:" prefix searches title, abstract, authors, etc.
    # We sort by submittedDate descending to get the newest research.
    params = {
        "search_query": f"all:{query}",
        "start": 0,
        "max_results": max_results,
        "sortBy": "submittedDate",
        "sortOrder": "descending"
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
            title_elem = entry.find('atom:title', ns)
            summary_elem = entry.find('atom:summary', ns)
            link_elem = entry.find('atom:id', ns)
            
            # Clean up text (remove newlines/excess whitespace)
            title = " ".join(title_elem.text.split()) if title_elem is not None else "Untitled"
            summary = " ".join(summary_elem.text.split()) if summary_elem is not None else "No summary."
            url = link_elem.text.strip() if link_elem is not None else "#"
            
            formatted_results.append({
                "title": title,
                "url": url,
                "content": summary
            })
            
        if not formatted_results:
            print(f"No Arxiv results found for: {query}")
            
        return formatted_results

    except Exception as e:
        print(f"Arxiv API Error: {e}")
        return []