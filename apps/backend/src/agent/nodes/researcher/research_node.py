from src.agent.tools.arxiv_search_tool import search_arxiv
from src.agent.tools.hackernews_search_tool import search_hackernews
from src.agent.tools.semantic_scholar_tool import search_semantic_scholar
from src.agent.nodes.planner.response_schema import ResearchTask
from src.agent.logging_config import get_logger

logger = get_logger(__name__)


def research_node(state: ResearchTask) -> dict:
    """Executes a single search task and returns structured results."""
    query = state.query
    source = state.source
    logger.info("Researching (%s): %s", source, query)

    arxiv_results = search_arxiv(query)
    hn_results = search_hackernews(query)
    ss_results = search_semantic_scholar(query) if source == "semantic_scholar" else []

    results = arxiv_results + hn_results + ss_results
    logger.info(
        "Found %d total results (%d Arxiv, %d HN, %d Scholar)",
        len(results), len(arxiv_results), len(hn_results), len(ss_results),
    )

    return {"research_results": [{"query": state.query, "data": results}]}
