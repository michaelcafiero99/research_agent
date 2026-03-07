from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # LLM
    model: str = "gemini-2.5-flash"
    temperature: float = 0.0

    # Planner
    num_tasks: int = 3

    # Tavily search
    search_depth: str = "basic"
    max_results: int = 3

    model_config = {"env_prefix": "AGENT_"}


settings = Settings()
