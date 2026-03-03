import os
from dotenv import load_dotenv
from src.agent.graph import graph

load_dotenv()

def main():
    initial_input = {
        "interest": "DeepSeek R1 vs Gemini 2.0 Flash"
    }

    print("--- Starting Local Workflow ---\n")

    for event in graph.stream(initial_input, stream_mode="updates"):
        if "planner" in event:
            plan = event["planner"].get("plan", [])
            print(f"--- Strategy Generated ---")
            
            for i, task in enumerate(plan, 1):
                # 1. Normalize the task to a dictionary
                # If it's a Pydantic object, convert it; if it's already a dict, keep it.
                t = task.model_dump() if hasattr(task, "model_dump") else task
                
                # 2. Now you can safely use .get()
                query = t.get("query")
                source = t.get("source")
                rationale = t.get("rationale")
                
                print(f"{i}. [{str(source).upper()}] {query}")
                print(f"   Rationale: {rationale}\n")

if __name__ == "__main__":
    main()