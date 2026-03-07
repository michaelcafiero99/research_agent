from typing import Annotated, Any, List, Optional, Sequence, TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
import operator

from src.agent.nodes.planner.response_schema import ResearchTask


class AgentState(TypedDict, total=False):

    # ── Core ──────────────────────────────────────────────────────────────────
    messages: Annotated[Sequence[BaseMessage], add_messages]
    interest: str
    plan: List[ResearchTask]

    # ── Research phase (fan-out / fan-in via operator.add) ────────────────────
    research_results: Annotated[List[dict], operator.add]

    # ── Evaluation phase ──────────────────────────────────────────────────────
    # Flat list of individual papers produced by prepare_candidates_node
    candidate_papers: List[dict]

    # Single paper injected per-node by the Send() fan-out in map_papers
    paper: Optional[dict]

    # Parallel evaluations appended by each evaluate_paper_node instance
    evaluated_papers: Annotated[List[Any], operator.add]

    # Final ranked digest produced by aggregator_node
    digest: List[Any]

    # ── Legacy synthesis (kept for backwards compatibility) ───────────────────
    synthesis: str
