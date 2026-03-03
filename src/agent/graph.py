from langgraph.graph import StateGraph, START, END
from src.agent.state import AgentState
from src.agent.nodes.planner.planner_node import planner_node
from src.agent.nodes.researcher.research_node import research_node
from langgraph.types import Send # syntax: Send("target_node", payload)


builder = StateGraph(AgentState)

# implement fan out strategy: the planner node outputs List[ResearchTask] 
# we want each task to be handled in parallel by the next node

def fan_out(state: AgentState):
    send_list = []
    for task in state["plan"]:
        send_list.append(Send("research_node", task))
    
    return send_list # need to return a list of send objects


builder.add_node("planner", planner_node)
builder.add_node("research_node", research_node)


builder.add_edge(START, "planner")
builder.add_conditional_edges("planner", fan_out)
builder.add_edge("research_node", END)

# Export for LangGraph Studio / Deployment
graph = builder.compile()