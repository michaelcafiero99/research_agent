import json
import asyncio
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from src.agent.graph import graph
from src.agent.logging_config import get_logger

logger = get_logger(__name__)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def state_serializer(obj):
    if hasattr(obj, "model_dump"): return obj.model_dump()
    if hasattr(obj, "dict"): return obj.dict()
    return str(obj)

@app.post("/chat")
async def chat(payload: dict):
    interest = payload.get("input")
    logger.info("Received chat request: %s", interest)
    
    async def event_generator():
        try:
            # SWITCH: Using "updates" mode to see which node is running
            async for mode, event in graph.astream(
                {"interest": interest}, 
                stream_mode=["updates", "values"]
            ):
                # 1. Handle Node Status Updates (The "Clean" part)
                if mode == "updates":
                    node_name = list(event.keys())[0]
                    # Map technical node names to pretty UI names
                    display_names = {
                        "planner": "Strategizing research path...",
                        "research_node": "Searching Arxiv and Semantic Scholar...",
                        "prepare_candidates": "Consolidating research...",
                        "evaluate_paper_node": "Scoring paper relevance and impact...",
                        "aggregator": "Building final research digest..."
                    }
                    status_msg = display_names.get(node_name, f"Executing {node_name}...")
                    
                    yield f"data: {json.dumps({'type': 'status', 'message': status_msg})}\n\n"

                # 2. Handle the Final Result
                # Only send the big 'report' content when the aggregator node finishes
                if mode == "updates" and "aggregator" in event:
                    final_report = event["aggregator"].get("digest", [])
                    yield f"data: {json.dumps({'type': 'report', 'content': final_report}, default=state_serializer)}\n\n"

            yield "data: [DONE]\n\n"
        except Exception as e:
            logger.error("Stream error: %s", e)
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)