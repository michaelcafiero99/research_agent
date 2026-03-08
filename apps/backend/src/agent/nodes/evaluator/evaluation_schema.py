from pydantic import BaseModel, Field


class EvaluationResult(BaseModel):
    """Structured evaluation of a single item (paper, post, article, implementation, etc.)."""

    title: str = Field(description="Title of the item.")
    url: str = Field(description="Source URL.")

    relevance_score: float = Field(
        ge=0, le=10,
        description=(
            "How directly does this item address the user's research interest? "
            "9-10 = core topic, exactly what was asked; "
            "7-8 = closely related, covers the main subject; "
            "5-6 = tangentially related, useful context; "
            "3-4 = loosely connected, minor overlap; "
            "1-2 = barely relevant; "
            "0 = unrelated, or pure noise (job posting, spam, sales pitch)."
        ),
    )
    depth_score: float = Field(
        ge=0, le=10,
        description=(
            "How substantive and informative is the content? "
            "9-10 = deep technical or analytical content: original research, rigorous benchmarks, detailed implementation, thorough analysis; "
            "7-8 = solid depth: meaningful technical detail, real data, or well-argued insights; "
            "5-6 = moderate depth: useful overview, some supporting evidence, practical examples; "
            "3-4 = shallow: surface-level summary, limited detail, mostly opinion; "
            "1-2 = minimal substance: vague, anecdotal, or content-free; "
            "0 = no substantive content whatsoever."
        ),
    )
    credibility_score: float = Field(
        ge=0, le=10,
        description=(
            "How credible is the source for this type of content? "
            "9-10 = highly authoritative: top-tier journal, well-known research lab, recognized expert or practitioner; "
            "7-8 = credible: reputable publication, established technical blog, known company engineering blog; "
            "5-6 = reasonably credible: individual practitioner with evident expertise, preprint from known institution; "
            "3-4 = uncertain credibility: anonymous or unknown author, obscure outlet; "
            "1-2 = low credibility: no discernible expertise or track record; "
            "0 = actively misleading, spam, or pure self-promotion."
        ),
    )
    traction_score: float = Field(
        ge=0, le=10,
        description=(
            "Is this getting meaningful attention in relevant communities? "
            "9-10 = viral in the relevant community, widely shared or cited; "
            "7-8 = strong community engagement, actively discussed; "
            "5-6 = moderate interest, some discussion or citations; "
            "3-4 = limited traction, early awareness; "
            "1-2 = little to no pickup; "
            "0 = no community presence at all."
        ),
    )

    weighted_score: float = Field(
        description=(
            "Weighted composite score: "
            "(relevance * 0.35) + (depth * 0.30) + (credibility * 0.20) + (traction * 0.15). "
            "Maximum is 10.0."
        )
    )
    include_in_digest: bool = Field(
        description=(
            "True if weighted_score >= 5.0 AND the item is relevant to the user's interest. "
            "When in doubt, set False."
        )
    )
    reasoning: str = Field(
        description="1-2 sentences explaining the score. If excluded, state the primary reason why."
    )
