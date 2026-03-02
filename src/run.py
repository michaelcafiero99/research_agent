import os
from dotenv import load_dotenv
from src.agent.graph import graph

# 1. Load environment variables
load_dotenv()

def main():
    # 2. Prepare the initial state
    # LangGraph expects a dictionary matching your 'AgentState'
    initial_input = {
        "messages": [
            {"role": "user", "content": "Hello Gemini! Confirm you are running locally."}
        ]
    }

    print("--- Starting Local Workflow ---\n")

    # 3. Stream the execution
    # streaming allows you to see which node is active in real-time
    for event in graph.stream(initial_input, stream_mode="values"):
        if "messages" in event:
            last_message = event["messages"][-1]
            # Use .content as Gemini returns a BaseMessage object
            print(f"[{last_message.type.upper()}]: {last_message.content}")

if __name__ == "__main__":
    main()