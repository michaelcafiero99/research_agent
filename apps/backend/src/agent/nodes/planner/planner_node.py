from langchain_google_genai import ChatGoogleGenerativeAI
from src.agent.state import AgentState
from src.agent.config import settings
from src.agent.logging_config import get_logger
from .response_schema import ResearchPlan

logger = get_logger(__name__)

llm = ChatGoogleGenerativeAI(model=settings.model, temperature=settings.temperature)
planner_llm = llm.with_structured_output(ResearchPlan)


def planner_node(state: AgentState) -> dict:
    """Takes a single interest and generates a structured research plan."""
    interest = state.get("interest", "AI agents")
    logger.info("Planning research for: %s", interest)

    prompt = f"""
    You are a research curator who writes targeted search queries for different content sources.
    The user is interested in: {interest}

    Your goal: Create {settings.num_tasks} specific, distinct search tasks covering the topic from
    different angles — academic research, practitioner content, and community discussion.

    Source assignment rules (use each source the stated number of times):
    - 'arxiv': exactly 1 task — write a precise, technical academic query using field-specific terminology
    - 'semantic_scholar': exactly 1 task — write a query focused on citations and foundational work
    - 'twitter': exactly 1 task — write a short, conversational query (3-5 words) that reflects how
      people discuss and debate this topic on social media

    Each query must target a distinct sub-angle of the topic.
    """

    plan = planner_llm.invoke(prompt)
    logger.info("Generated %d research tasks", len(plan.tasks))
    return {"plan": plan.tasks}
