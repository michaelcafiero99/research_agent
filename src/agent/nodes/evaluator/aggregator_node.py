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

    included = [p for p in evaluated if p.include_in_digest]
    ranked = sorted(included, key=lambda p: p.weighted_score, reverse=True)

    logger.info(
        "%d / %d papers qualify for digest",
        len(ranked),
        len(evaluated),
    )
    return {"digest": ranked}
