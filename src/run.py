import os
from dotenv import load_dotenv
from src.agent.graph import graph

# 1. Load environment variables
load_dotenv()

def main():
    # 2. Prepare the initial state
    # LangGraph expects a dictionary matching your 'AgentState'
    initial_input = {
        "interest": "DeepSeek R1 vs Gemini 2.0 Flash"
    }

    print("--- Starting Local Workflow ---\n")

    # 3. Stream the execution
    # streaming allows you to see which node is active in real-time
    for event in graph.stream(initial_input, stream_mode="values"):
        if "plan" in event:
            for i, task in enumerate(event["plan"], 1):
                print(f"{i}. [{task.source.upper()}] {task.query}\n   Rationale: {task.rationale}\n")

if __name__ == "__main__":
    main()