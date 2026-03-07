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
    You are a Senior Research Architect.
    The user is interested in: {interest}

    Your goal: Create {settings.num_tasks} specific, distinct search tasks to find the newest and
    most impactful research from the last 30 days.
    Focus on finding breakthroughs that have practical code implementations.

    For the 'source' field, set exactly one task to 'semantic_scholar' for deep citation analysis.
    Set the other tasks to 'arxiv' or 'hackernews'.
    """

    plan = planner_llm.invoke(prompt)
    logger.info("Generated %d research tasks", len(plan.tasks))
    return {"plan": plan.tasks}
