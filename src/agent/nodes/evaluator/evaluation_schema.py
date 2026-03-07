from pydantic import BaseModel, Field


class EvaluationResult(BaseModel):
    """Structured evaluation of a single research paper or article."""

    title: str = Field(description="Title of the paper or article.")
    url: str = Field(description="Source URL.")

    novelty_score: float = Field(
        ge=0, le=10,
        description=(
            "Does this item present PRIMARY research with genuinely new findings, methods, or models? "
            "Scoring anchors: "
            "9-10 = breakthrough contribution that advances the field; "
            "7-8 = solid new research with clear novel contribution; "
            "5-6 = incremental improvement on existing work; "
            "3-4 = very minor or derivative; "
            "1-2 = no new research (survey, recap, commentary); "
            "0 = news article, blog post, opinion piece, or social content — score MUST be 0."
        ),
    )
    empirical_impact_score: float = Field(
        ge=0, le=10,
        description=(
            "Is the impact backed by DEMONSTRATED empirical evidence in this item (benchmarks, trials, ablations, datasets)? "
            "Scoring anchors: "
            "9-10 = strong quantitative results on rigorous benchmarks or real-world deployments; "
            "7-8 = promising results with some caveats or limited scope; "
            "5-6 = theoretical with plausible but unverified claims; "
            "3-4 = weak evidence or highly speculative; "
            "1-2 = anecdotal, no data, or purely qualitative; "
            "0 = no research basis whatsoever (news, blog, opinion) — score MUST be 0."
        ),
    )
    venue_authority_score: float = Field(
        ge=0, le=10,
        description=(
            "How authoritative is this as a RESEARCH venue? "
            "Scoring anchors: "
            "9-10 = top-tier peer-reviewed venue (Nature, Science, NeurIPS, ICML, ACL, ICLR, CVPR, top journal); "
            "7-8 = reputable peer-reviewed conference or journal; "
            "5-6 = arxiv preprint from a credible institution or well-known authors; "
            "3-4 = obscure preprint or unknown authors; "
            "1-2 = technical blog, newsletter, or industry report; "
            "0 = news outlet, social media, YouTube, podcast, or opinion site — score MUST be 0."
        ),
    )
    academic_traction_score: float = Field(
        ge=0, le=10,
        description=(
            "Is this being actively discussed or cited in RESEARCH and TECHNICAL communities "
            "(academic Twitter/X, Papers with Code, Semantic Scholar citation velocity, Hacker News technical threads)? "
            "Scoring anchors: "
            "9-10 = viral among researchers, rapid citation growth, widely replicated; "
            "7-8 = actively discussed in technical forums, strong community interest; "
            "5-6 = moderate interest in a niche research area; "
            "3-4 = limited traction, early-stage awareness; "
            "1-2 = little to no presence in research/technical communities; "
            "0 = only discussed in general media with no research community uptake — score MUST be 0."
        ),
    )

    weighted_score: float = Field(
        description=(
            "Weighted composite score: "
            "(novelty * 0.30) + (empirical_impact * 0.35) + (venue_authority * 0.20) + (academic_traction * 0.15). "
            "Maximum is 10.0."
        )
    )
    include_in_digest: bool = Field(
        description=(
            "True ONLY if: (1) weighted_score >= 7.5, AND (2) this is verifiably primary research "
            "(not a news article, blog, opinion piece, or general-interest content). "
            "When in doubt, set False."
        )
    )
    reasoning: str = Field(
        description="1-2 sentences explaining the score. If excluded, state the primary reason why."
    )
