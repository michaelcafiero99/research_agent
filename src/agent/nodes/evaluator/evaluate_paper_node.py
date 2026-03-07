from langchain_google_genai import ChatGoogleGenerativeAI

from src.agent.nodes.evaluator.evaluation_schema import EvaluationResult
from src.agent.config import settings
from src.agent.logging_config import get_logger

logger = get_logger(__name__)

_llm = ChatGoogleGenerativeAI(model=settings.model, temperature=settings.temperature)
_evaluator_llm = _llm.with_structured_output(EvaluationResult)

# Weights must sum to 1.0
_WEIGHTS = {
    "novelty": 0.30,
    "empirical_impact": 0.35,
    "venue_authority": 0.20,
    "academic_traction": 0.15,
}

# Minimum weighted score for digest inclusion
_DIGEST_THRESHOLD = 7.5


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

    prompt = f"""You are an expert research curator with a high bar for scientific quality. Your job is to separate genuine primary research from noise.

## Item to evaluate
Title: {title}
URL: {url}
Content: {content}

## Scoring rules — read these carefully before scoring

**MANDATORY DISQUALIFIERS** — if ANY of these apply, ALL four scores MUST be 0:
- The item is a news article, magazine piece, or general-interest journalism (BBC, CNN, Reuters, NYT, etc.)
- The item is a blog post, newsletter, or opinion/commentary
- The item is a podcast, video, or social media post
- The item is a product announcement, press release, or marketing content
- The item has no original data, experiments, or methodology

**SCORE EACH CRITERION 0–10 using these anchors:**

1. **Research Novelty** — Primary research with new findings, methods, or models?
   - 9-10: Breakthrough that meaningfully advances the field
   - 7-8: Clear novel contribution (new architecture, dataset, benchmark, proof)
   - 5-6: Incremental improvement on prior work
   - 3-4: Derivative or very minor contribution
   - 1-2: No new research (survey, meta-analysis only, recap)
   - 0: Not primary research — MANDATORY 0

2. **Empirical Impact** — Impact backed by demonstrated evidence in THIS item?
   - 9-10: Strong quantitative results on rigorous benchmarks or real deployments
   - 7-8: Solid results with some scope/generalizability caveats
   - 5-6: Theoretical contributions with limited empirical validation
   - 3-4: Weak or cherry-picked evidence
   - 1-2: Purely anecdotal, no data
   - 0: No research basis — MANDATORY 0

3. **Venue Authority** — How authoritative as a research publication?
   - 9-10: Top-tier peer-reviewed venue (Nature, NeurIPS, ICML, ICLR, ACL, CVPR, top journals)
   - 7-8: Reputable peer-reviewed conference or journal
   - 5-6: arxiv preprint from known institution or credible authors
   - 3-4: Obscure preprint, unknown authors
   - 1-2: Technical blog, industry report, white paper
   - 0: News outlet, general media, social platform — MANDATORY 0

4. **Academic Traction** — Discussed/cited in research and technical communities?
   - 9-10: Viral in research community, rapid citation growth, widely replicated
   - 7-8: Active discussion in technical forums, Papers with Code, academic Twitter/X
   - 5-6: Moderate niche interest
   - 3-4: Early awareness, limited pickup
   - 1-2: Little to no presence in research communities
   - 0: Only in general media, no research community uptake — MANDATORY 0

## Threshold
- Set **include_in_digest = True** ONLY IF weighted_score >= {_DIGEST_THRESHOLD} AND the item is verifiably primary research.
- When uncertain, set **include_in_digest = False**.

## weighted_score
Compute as: (novelty * 0.30) + (empirical_impact * 0.35) + (venue_authority * 0.20) + (academic_traction * 0.15)

Be ruthlessly selective. A high-quality BBC article is still a 0 across the board."""

    result: EvaluationResult = _evaluator_llm.invoke(prompt)

    # Recompute weighted_score deterministically to override any LLM approximation
    result.weighted_score = round(
        result.novelty_score * _WEIGHTS["novelty"]
        + result.empirical_impact_score * _WEIGHTS["empirical_impact"]
        + result.venue_authority_score * _WEIGHTS["venue_authority"]
        + result.academic_traction_score * _WEIGHTS["academic_traction"],
        2,
    )

    # Enforce threshold programmatically as a hard gate
    if result.weighted_score < _DIGEST_THRESHOLD:
        result.include_in_digest = False

    logger.info(
        "Scored '%s': %.2f (include=%s)", title, result.weighted_score, result.include_in_digest
    )
    return {"evaluated_papers": [result]}
