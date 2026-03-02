# what do we need to create a node?
# we need the model
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from src.agent.state import AgentState

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    max_retries=2,
)


def call_gemini(state:AgentState):

    response = model.invoke(state["messages"])
    return {"messages":[response]}
