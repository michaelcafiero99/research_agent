from langchain_google_genai import ChatGoogleGenerativeAI
from src.agent.state import AgentState  # Assuming this exists from earlier

research_llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

def research_node(state: AgentState):

    # access the specific research task: the Send function causes this node to NOT
    # recieve the entire AgentState. Instead, it only recieves the payload of the Send

   # research_task = state["task"]
    query = state.query
    source = state.source

    prompt = f"Search for {query} on {source}. Rationale: {state.rationale}"

    research_result = research_llm.invoke(prompt)
    print(research_result.content)
    return {"research_results": [research_result.content]}
    

