from langgraph.graph import StateGraph, START, END
from src.agent.state import AgentState
from src.agent.nodes import call_gemini

builder = StateGraph(AgentState)

builder.add_node("gemini_agent", call_gemini)

builder.add_edge(START, "gemini_agent")
builder.add_edge("gemini_agent", END)

# Export for LangGraph Studio / Deployment
graph = builder.compile()