from src.agent.logging_config import get_logger

logger = get_logger(__name__)


def prepare_candidates_node(state: dict) -> dict:
    """Fan-in / flatten step: converts accumulated research_results into a deduplicated
    flat list of individual candidate papers, ready for parallel evaluation.

    Runs once after all parallel research_node instances complete (LangGraph fan-in).
    """
    research_results = state.get("research_results", [])

    papers: list[dict] = []
    for entry in research_results:
        papers.extend(entry.get("data", []))

    # Deduplicate by URL, preserving order
    seen: set[str] = set()
    unique: list[dict] = []
    for paper in papers:
        url = paper.get("url", "")
        if url and url not in seen:
            seen.add(url)
            unique.append(paper)

    logger.info(
        "Prepared %d unique candidate papers from %d research queries (%d duplicates removed)",
        len(unique),
        len(research_results),
        len(papers) - len(unique),
    )
    return {"candidate_papers": unique}
