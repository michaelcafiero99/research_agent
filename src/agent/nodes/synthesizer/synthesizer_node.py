from langchain_google_genai import ChatGoogleGenerativeAI
from src.agent.state import AgentState
from src.agent.config import settings
from src.agent.logging_config import get_logger

logger = get_logger(__name__)

llm = ChatGoogleGenerativeAI(model=settings.model, temperature=settings.temperature)


def synthesizer_node(state: AgentState) -> dict:
    """Synthesizes parallel research results into a structured report."""
    interest = state.get("interest", "")
    research_results = state.get("research_results", [])

    logger.info("Synthesizing %d research results", len(research_results))

    sources_text = ""
    for entry in research_results:
        sources_text += f"\n### Query: {entry['query']}\n"
        for source in entry.get("data", []):
            snippet = source.get("content", "")[:400]
            sources_text += f"- **{source.get('title')}** ({source.get('url')})\n  {snippet}\n"

    prompt = f"""You are a research analyst. The user is interested in: {interest}

Based on the following gathered sources, produce a concise synthesis report.

{sources_text}

Structure your report as:
## Key Findings
(3-5 bullet points highlighting the most important developments)

## Notable Sources
(2-3 sources most worth following up on, with a one-line reason each)

## Summary
(1-2 paragraph overview)
"""

    response = llm.invoke(prompt)
    logger.info("Synthesis complete")
    return {"synthesis": response.content}
