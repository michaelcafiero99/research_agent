from langgraph.graph import StateGraph, START, END
from src.agent.state import AgentState
from src.agent.nodes.planner.planner_node import planner_node

builder = StateGraph(AgentState)

builder.add_node("planner", planner_node)

builder.add_edge(START, "planner")
builder.add_edge("planner", END)

# Export for LangGraph Studio / Deployment
graph = builder.compile()