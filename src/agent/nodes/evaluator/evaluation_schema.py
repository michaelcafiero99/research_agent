from pydantic import BaseModel, Field


class EvaluationResult(BaseModel):
    """Structured evaluation of a single research paper or article."""

    title: str = Field(description="Title of the paper or article.")
    url: str = Field(description="Source URL.")

    novelty_score: float = Field(
        ge=0, le=10,
        description="How novel or original is this work? Does it introduce new ideas, methods, or findings? (0-10)",
    )
    clinical_efficacy_score: float = Field(
        ge=0, le=10,
        description="Practical real-world impact or applicability — could it improve outcomes or systems? (0-10)",
    )
    source_authority_score: float = Field(
        ge=0, le=10,
        description="Credibility of the source: venue, authors, institution, or publication type. (0-10)",
    )
    trending_signal_score: float = Field(
        ge=0, le=10,
        description="How much traction is this topic getting right now? Is it widely discussed or cited? (0-10)",
    )

    weighted_score: float = Field(
        description=(
            "Weighted composite score computed as: "
            "(novelty * 0.25) + (clinical_efficacy * 0.30) + (source_authority * 0.25) + (trending_signal * 0.20)"
        )
    )
    include_in_digest: bool = Field(
        description="True if this paper should be included in the final digest (weighted_score >= 6.0 and genuinely high quality)."
    )
    reasoning: str = Field(description="Brief 1-2 sentence explanation of the evaluation.")
