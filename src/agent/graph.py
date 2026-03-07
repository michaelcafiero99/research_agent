from langgraph.graph import StateGraph, START, END
from langgraph.types import Send
from src.agent.state import AgentState
from src.agent.nodes.planner.planner_node import planner_node
from src.agent.nodes.researcher.research_node import research_node
from src.agent.nodes.synthesizer.synthesizer_node import synthesizer_node


builder = StateGraph(AgentState)


def fan_out(state: AgentState):
    return [Send("research_node", task) for task in state["plan"]]


builder.add_node("planner", planner_node)
builder.add_node("research_node", research_node)
builder.add_node("synthesizer", synthesizer_node)

builder.add_edge(START, "planner")
builder.add_conditional_edges("planner", fan_out)
builder.add_edge("research_node", "synthesizer")
builder.add_edge("synthesizer", END)

graph = builder.compile()
