from langchain_google_genai import ChatGoogleGenerativeAI

from src.agent.nodes.evaluator.evaluation_schema import EvaluationResult
from src.agent.config import settings
from src.agent.logging_config import get_logger

logger = get_logger(__name__)

_llm = ChatGoogleGenerativeAI(model=settings.model, temperature=settings.temperature)
_evaluator_llm = _llm.with_structured_output(EvaluationResult)

# Default weights (research articles)
_WEIGHTS_DEFAULT = {
    "relevance": 0.35,
    "depth": 0.30,
    "credibility": 0.20,
    "traction": 0.15,
}

# Twitter weights — traction matters more than depth for social content
_WEIGHTS_TWITTER = {
    "relevance": 0.35,
    "depth": 0.10,
    "credibility": 0.20,
    "traction": 0.35,
}

# Minimum weighted score for digest inclusion
_DIGEST_THRESHOLD = 5.0


def evaluate_paper_node(state: dict) -> dict:
    """Evaluates a single item via LLM structured output and returns an EvaluationResult.

    Receives a state dict with a "paper" key and an "interest" key (injected by Send).
    Returns {"evaluated_papers": [EvaluationResult]} so the reducer can append it
    to the shared list in the graph state.
    """
    paper = state["paper"]
    interest = state.get("interest", "")
    source = paper.get("source", "")
    title = paper.get("title", "Unknown")
    url = paper.get("url", "")
    content = paper.get("content", "")

    weights = _WEIGHTS_TWITTER if source == "twitter" else _WEIGHTS_DEFAULT

    logger.info("Evaluating: %s", title)

    prompt = f"""You are a content curator assembling a high-quality digest on a specific topic.
You evaluate any type of content — research papers, technical blog posts, implementations,
industry reports, community discussions — and score it on relevance, depth, credibility, and traction.

## User's research interest
{interest}

## Item to evaluate
Title: {title}
URL: {url}
Content: {content}

## Scoring rules

**DISQUALIFY (all scores = 0) only if:**
- The item is completely unrelated to the user's interest
- The item is a job posting, spam, or pure sales/marketing with no informational value

**SCORE EACH CRITERION 0–10:**

1. **Relevance** — How directly does this address the user's interest?
   - 9-10: Core topic, exactly on point
   - 7-8: Closely related, covers the main subject
   - 5-6: Useful context, tangentially related
   - 3-4: Loosely connected
   - 0: Unrelated or disqualified

2. **Depth** — How substantive is the content?
   - 9-10: Deep technical or analytical content (original research, benchmarks, detailed implementation, thorough analysis)
   - 7-8: Solid depth with real data, meaningful technical detail, or well-argued insights
   - 5-6: Useful overview with some supporting evidence or practical examples
   - 3-4: Shallow, surface-level, mostly opinion
   - 0: No substantive content

3. **Credibility** — How credible is the source?
   - 9-10: Top-tier journal, well-known research lab, recognized expert
   - 7-8: Reputable publication, established technical blog, known engineering team
   - 5-6: Individual practitioner with evident expertise, credible preprint
   - 3-4: Unknown author, uncertain background
   - 0: Spam or actively misleading

4. **Traction** — Is this getting meaningful attention?
   - 9-10: Viral in the relevant community, widely shared or cited
   - 7-8: Strong engagement, actively discussed
   - 5-6: Moderate interest
   - 3-4: Limited pickup
   - 0: No presence

## weighted_score
Compute as: (relevance * 0.35) + (depth * 0.30) + (credibility * 0.20) + (traction * 0.15)

Set include_in_digest = True if weighted_score >= {_DIGEST_THRESHOLD} and the item is relevant."""

    result: EvaluationResult = _evaluator_llm.invoke(prompt)

    # Recompute weighted_score deterministically to override any LLM approximation
    result.weighted_score = round(
        result.relevance_score * weights["relevance"]
        + result.depth_score * weights["depth"]
        + result.credibility_score * weights["credibility"]
        + result.traction_score * weights["traction"],
        2,
    )

    # Enforce threshold programmatically as a hard gate
    if result.weighted_score < _DIGEST_THRESHOLD:
        result.include_in_digest = False

    logger.info(
        "Scored '%s': %.2f (include=%s)", title, result.weighted_score, result.include_in_digest
    )
    return {"evaluated_papers": [result]}
