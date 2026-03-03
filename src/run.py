import os
from dotenv import load_dotenv
from src.agent.graph import graph

load_dotenv()

def main():
    initial_input = {"interest": "DeepSeek R1 vs Gemini 2.0 Flash"}
    print("--- Starting Local Workflow ---\n")

    # We use this variable to store the final state emitted by the graph
    final_output = None

    for event in graph.stream(initial_input, stream_mode="values"):
        # 'values' mode is better for final inspection because 
        # it always gives you a snapshot of the ENTIRE state.
        final_output = event
        
        # Optional: Print progress updates as they happen
        if "plan" in event and "research_results" not in event:
             print(f"Plan generated with {len(event['plan'])} tasks...")

    # --- FINAL PRINTING ---
    print("\n" + "="*50)
    print("FINAL RESEARCH REPORT")
    print("="*50)

    # Access the aggregated list from your Reducer
    results = final_output.get("research_results", [])
    
    if not results:
        print("No research results were collected.")
        # Debugging: Print available keys to help identify mismatches
        print(f"DEBUG: Final State Keys: {list(final_output.keys())}")
    else:
        for i, entry in enumerate(results, 1):
            print(f"\nTASK {i}: {entry.get('query')}")
            print("-" * 30)
            for source in entry.get("data", []):
                print(f"• {source.get('title')}")
                print(f"  URL: {source.get('url')}")
                # Print a small snippet of the content
                snippet = source.get('content', '')[:150] + "..."
                print(f"  Snippet: {snippet}\n")

                
if __name__ == "__main__":
    main()