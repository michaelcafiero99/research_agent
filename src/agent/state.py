from typing import Annotated, Sequence, TypedDict, List
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

from src.agent.nodes.planner.response_schema import ResearchTask


class AgentState(TypedDict, total=False):

    messages: Annotated[Sequence[BaseMessage], add_messages]
    interest: str
    plan: List[ResearchTask]

