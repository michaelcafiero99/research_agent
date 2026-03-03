from src.agent.tools.web_search_tool import search_web
from src.agent.state import ResearchTask

def research_node(state: ResearchTask):
    # state is the Pydantic ResearchTask object from the Send() command
    query = state.query
    
    print(f"Researching: {query}")
    
    # Call our new tool
    results = search_web(query)
    print(f"   - Found {len(results) if results else 0} results")
    
    return {"research_results": [{"query": state.query, "data": results}]}