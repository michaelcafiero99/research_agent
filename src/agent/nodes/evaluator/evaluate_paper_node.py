from langchain_google_genai import ChatGoogleGenerativeAI

from src.agent.nodes.evaluator.evaluation_schema import EvaluationResult
from src.agent.config import settings
from src.agent.logging_config import get_logger

logger = get_logger(__name__)

_llm = ChatGoogleGenerativeAI(model=settings.model, temperature=settings.temperature)
_evaluator_llm = _llm.with_structured_output(EvaluationResult)

# Weights must sum to 1.0
_WEIGHTS = {
    "novelty": 0.25,
    "clinical_efficacy": 0.30,
    "source_authority": 0.25,
    "trending_signal": 0.20,
}


def evaluate_paper_node(state: dict) -> dict:
    """Evaluates a single paper via LLM structured output and returns an EvaluationResult.

    Receives a state dict with a single "paper" key (injected by Send).
    Returns {"evaluated_papers": [EvaluationResult]} so the reducer can append it
    to the shared list in the graph state.
    """
    paper = state["paper"]
    title = paper.get("title", "Unknown")
    url = paper.get("url", "")
    content = paper.get("content", "")

    logger.info("Evaluating: %s", title)

    prompt = f"""You are a rigorous research analyst evaluating the relevance and quality of a paper or article.

Title: {title}
URL: {url}
Content: {content}

Score this paper on each criterion from 0 (lowest) to 10 (highest):

1. **Novelty** — How original or groundbreaking is this work? Does it introduce genuinely new ideas, methods, or findings?
2. **Clinical Efficacy** — What is the practical real-world impact or applicability? Could it meaningfully improve outcomes or systems?
3. **Source Authority** — How credible is the source? Consider the publication venue, known authors, institution, or journal quality.
4. **Trending Signal** — How much current traction does this topic have? Is it being widely discussed, cited, or replicated right now?

Then compute:
- **weighted_score**: (novelty * 0.25) + (clinical_efficacy * 0.30) + (source_authority * 0.25) + (trending_signal * 0.20)
- **include_in_digest**: Set True if weighted_score >= 6.0 AND the paper is genuinely high quality and relevant
- **reasoning**: A concise 1-2 sentence explanation of your overall evaluation

Be objective, critical, and consistent across papers."""

    result: EvaluationResult = _evaluator_llm.invoke(prompt)

    # Recompute weighted_score deterministically to override any LLM approximation
    result.weighted_score = round(
        result.novelty_score * _WEIGHTS["novelty"]
        + result.clinical_efficacy_score * _WEIGHTS["clinical_efficacy"]
        + result.source_authority_score * _WEIGHTS["source_authority"]
        + result.trending_signal_score * _WEIGHTS["trending_signal"],
        2,
    )

    logger.info(
        "Scored '%s': %.2f (include=%s)", title, result.weighted_score, result.include_in_digest
    )
    return {"evaluated_papers": [result]}
