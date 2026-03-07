# Research Agent

A LangGraph-based research orchestration agent that decomposes a topic into parallel searches across arXiv, Hacker News, and Semantic Scholar, then synthesizes the results into a structured report.

## Architecture

```
START
  └─► planner          — Gemini generates N focused search tasks
        └─► [fan-out]
              ├─► research_node  — arXiv + HN + Semantic Scholar (parallel)
              ├─► research_node  — arXiv + HN + Semantic Scholar (parallel)
              └─► research_node  — arXiv + HN + Semantic Scholar (parallel)
                    └─► synthesizer  — Gemini synthesizes all results
                              └─► END
```

## Setup

### 1. Install dependencies

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure environment variables

```bash
cp .env.example .env
```

| Variable         | Required | Description                        |
|------------------|----------|------------------------------------|
| `GOOGLE_API_KEY` | Yes      | Google AI Studio or Vertex API key |
| `TAVILY_API_KEY` | Yes      | Tavily search API key              |

### 3. Run

```bash
python -m src.run
```

## Configuration

Tune agent behaviour without code changes using `AGENT_`-prefixed environment variables:

| Variable             | Default            | Description                                        |
|----------------------|--------------------|----------------------------------------------------|
| `AGENT_MODEL`        | `gemini-2.5-flash` | Gemini model for planner & synthesizer             |
| `AGENT_TEMPERATURE`  | `0.0`              | LLM temperature                                    |
| `AGENT_NUM_TASKS`    | `3`                | Number of parallel research tasks                  |
| `AGENT_SEARCH_DEPTH` | `basic`            | Tavily search depth (`basic` or `advanced`)        |
| `AGENT_MAX_RESULTS`  | `3`                | Max Tavily results per query                       |

## Project Structure

```
src/
├── run.py                          # Entry point
└── agent/
    ├── config.py                   # Centralised settings (pydantic-settings)
    ├── logging_config.py           # Shared logger factory
    ├── state.py                    # LangGraph AgentState
    ├── graph.py                    # Graph definition and fan-out logic
    ├── nodes/
    │   ├── planner/
    │   │   ├── planner_node.py     # Generates research tasks via LLM
    │   │   └── response_schema.py  # ResearchTask / ResearchPlan schemas
    │   ├── researcher/
    │   │   └── research_node.py    # Executes searches across all sources
    │   └── synthesizer/
    │       └── synthesizer_node.py # Synthesizes results into a report
    └── tools/
        ├── arxiv_search_tool.py
        ├── hackernews_search_tool.py
        ├── semantic_scholar_tool.py
        └── tavily_web_search_tool.py
```
