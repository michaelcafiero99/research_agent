from src.agent.tools.arxiv_search_tool import search_arxiv
from src.agent.tools.hackernews_search_tool import search_hackernews
from src.agent.tools.semantic_scholar_tool import search_semantic_scholar
from src.agent.tools.twitter_search_tool import search_twitter
from src.agent.nodes.planner.response_schema import ResearchTask
from src.agent.logging_config import get_logger

logger = get_logger(__name__)


def research_node(state: ResearchTask) -> dict:
    """Executes a single search task and returns structured results."""
    query = state.query
    source = state.source
    logger.info("Researching (%s): %s", source, query)

    arxiv_results = search_arxiv(query) if source == "arxiv" else []
    hn_results = search_hackernews(query) if source == "hackernews" else []
    ss_results = search_semantic_scholar(query) if source == "semantic_scholar" else []
    twitter_results = search_twitter(query) if source == "twitter" else []

    for r in arxiv_results:   r["source"] = "arxiv"
    for r in hn_results:      r["source"] = "hackernews"
    for r in ss_results:      r["source"] = "semantic_scholar"
    for r in twitter_results: r["source"] = "twitter"

    results = arxiv_results + hn_results + ss_results + twitter_results
    logger.info(
        "Found %d total results (%d Arxiv, %d HN, %d Scholar, %d Twitter)",
        len(results), len(arxiv_results), len(hn_results), len(ss_results), len(twitter_results),
    )

    return {"research_results": [{"query": state.query, "data": results}]}
