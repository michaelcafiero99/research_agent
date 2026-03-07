import os
from dotenv import load_dotenv
from src.agent.graph import graph
from src.agent.logging_config import get_logger

load_dotenv()

logger = get_logger(__name__)


def main():
    initial_input = {"interest": "DeepSeek R1 vs Gemini 2.0 Flash"}
    logger.info("Starting research agent")

    final_output = None

    for event in graph.stream(initial_input, stream_mode="values"):
        final_output = event

        if "plan" in event and "research_results" not in event:
            logger.info("Plan ready — %d tasks queued", len(event["plan"]))

    print("\n" + "=" * 60)
    print("RESEARCH DIGEST")
    print("=" * 60)

    digest = final_output.get("digest") if final_output else None

    if digest:
        print(f"\n{len(digest)} papers ranked for your digest:\n")
        for rank, paper in enumerate(digest, start=1):
            print(f"  {rank}. {paper.title}")
            print(f"     Score : {paper.weighted_score:.2f}  "
                  f"(N={paper.novelty_score:.1f}  "
                  f"CE={paper.clinical_efficacy_score:.1f}  "
                  f"SA={paper.source_authority_score:.1f}  "
                  f"TS={paper.trending_signal_score:.1f})")
            print(f"     URL   : {paper.url}")
            print(f"     Why   : {paper.reasoning}")
            print()
    else:
        logger.warning("No digest produced. Raw research results below.")
        for entry in (final_output or {}).get("research_results", []):
            print(f"\n[{entry.get('query')}]")
            for source in entry.get("data", []):
                print(f"  • {source.get('title')} — {source.get('url')}")

    print("=" * 60)


if __name__ == "__main__":
    main()
