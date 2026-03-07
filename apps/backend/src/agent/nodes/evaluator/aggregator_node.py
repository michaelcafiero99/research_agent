from src.agent.logging_config import get_logger

logger = get_logger(__name__)


def aggregator_node(state: dict) -> dict:
    """Reduce step: sorts all evaluated papers by weighted score and filters to digest-worthy entries.

    Runs once after all parallel evaluate_paper_node instances complete.
    Returns {"digest": [...]} with papers sorted descending by weighted_score,
    limited to those where include_in_digest is True.
    """
    evaluated = state.get("evaluated_papers", [])
    logger.info("Aggregating %d evaluated papers", len(evaluated))

    # Sort all papers by score descending
    all_ranked = sorted(evaluated, key=lambda p: p.weighted_score, reverse=True)

    # Filter for those meeting the threshold
    digest = [p for p in all_ranked if p.include_in_digest]

    # Fallback: If no papers met the threshold, include the top result
    if not digest and all_ranked:
        logger.info("No papers met threshold. Including top result as fallback.")
        digest = [all_ranked[0]]

    logger.info(
        "%d / %d papers qualify for digest",
        len(digest),
        len(evaluated),
    )
    return {"digest": digest}
