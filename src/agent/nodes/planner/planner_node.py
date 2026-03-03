# this node translates an input of interested to search queries
# we need to use pdantic .with_structured_output to force a set response schema
# LEARN: how does with_structured_output work under the hood? 

from langchain_google_genai import ChatGoogleGenerativeAI
from src.agent.state import AgentState  # Assuming this exists from earlier
from .response_schema import ResearchPlan

# Initialize Gemini
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

# Bind the Pydantic model to the LLM
planner_llm = llm.with_structured_output(ResearchPlan)

def planner_node(state: AgentState):
    """Takes a single interest and generates a structured research plan."""
    
    # Grab the interest from the graph state
    interest = state.get("interest", "AI agents") 
    
    prompt = f"""
    You are a Senior Research Architect. 
    The user is interested in: {interest}
    
    Your goal: Create 3 specific, distinct search tasks to find the newest and 
    most impactful research from the last 30 days. 
    Focus on finding breakthroughs that have practical code implementations.
    """
    
    # The LLM returns a ResearchPlan object (thanks to Pydantic)
    plan = planner_llm.invoke(prompt)
    
    # We return a dictionary that updates the 'plan' key in our Graph State
    return {"plan": plan.tasks}

