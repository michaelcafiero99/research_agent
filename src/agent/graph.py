from langgraph.graph import StateGraph, START, END
from langgraph.types import Send

from src.agent.state import AgentState
from src.agent.nodes.planner.planner_node import planner_node
from src.agent.nodes.researcher.research_node import research_node
from src.agent.nodes.researcher.prepare_candidates_node import prepare_candidates_node
from src.agent.nodes.evaluator.evaluate_paper_node import evaluate_paper_node
from src.agent.nodes.evaluator.aggregator_node import aggregator_node


builder = StateGraph(AgentState)


# ── Fan-out: one research_node per planned task ────────────────────────────────
def fan_out(state: AgentState):
    return [Send("research_node", task) for task in state["plan"]]


# ── Map step: one evaluate_paper_node per candidate paper ─────────────────────
def map_papers(state: AgentState):
    return [Send("evaluate_paper_node", {"paper": p}) for p in state.get("candidate_papers", [])]


# ── Nodes ─────────────────────────────────────────────────────────────────────
builder.add_node("planner", planner_node)
builder.add_node("research_node", research_node)
builder.add_node("prepare_candidates", prepare_candidates_node)
builder.add_node("evaluate_paper_node", evaluate_paper_node)
builder.add_node("aggregator", aggregator_node)

# ── Edges ─────────────────────────────────────────────────────────────────────
#
#  START
#    └──► planner
#           └──► [fan_out] ──► research_node (× N, parallel)
#                                └──► prepare_candidates   (fan-in barrier)
#                                       └──► [map_papers] ──► evaluate_paper_node (× M, parallel)
#                                                               └──► aggregator    (fan-in barrier)
#                                                                      └──► END
#
builder.add_edge(START, "planner")
builder.add_conditional_edges("planner", fan_out)
builder.add_edge("research_node", "prepare_candidates")
builder.add_conditional_edges("prepare_candidates", map_papers)
builder.add_edge("evaluate_paper_node", "aggregator")
builder.add_edge("aggregator", END)

graph = builder.compile()
