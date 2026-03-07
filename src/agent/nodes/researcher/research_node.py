# from src.agent.tools.tavily_web_search_tool import search_web # Deactivated for now
from src.agent.tools.arxiv_search_tool import search_arxiv
from src.agent.tools.hackernews_search_tool import search_hackernews
from src.agent.tools.semantic_scholar_tool import search_semantic_scholar
from src.agent.state import ResearchTask

def research_node(state: ResearchTask):
    # state is the Pydantic ResearchTask object from the Send() command
    query = state.query
    source = state.source
    
    print(f"Researching ({source}): {query}")
    
    # Always run fast/open tools
    arxiv_results = search_arxiv(query)
    hn_results = search_hackernews(query)
    
    # Only run Semantic Scholar if explicitly requested (to avoid rate limits)
    ss_results = search_semantic_scholar(query) if source == "semantic_scholar" else []
    
    results = arxiv_results + hn_results + ss_results
        
    print(f"   - Found {len(results)} total results ({len(arxiv_results)} Arxiv, {len(hn_results)} HN, {len(ss_results)} Scholar)")
    
    return {"research_results": [{"query": state.query, "data": results}]}