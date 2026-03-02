from pydantic import BaseModel, Field
from typing import List

class ResearchTask(BaseModel):
    """A single discrete search task for the agent to execute."""
    query: str = Field(description="The optimized search query for finding new research.")
    source: str = Field(description="The platform to search (e.g., 'arxiv', 'web', 'github').")
    rationale: str = Field(description="Why this specific query will find impactful research.")

class ResearchPlan(BaseModel):
    """The complete set of search tasks generated from an interest."""
    tasks: List[ResearchTask]
    summary: str = Field(description="A brief summary of the research strategy.")