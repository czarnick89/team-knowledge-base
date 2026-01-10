from typing import TypedDict, Optional


class ResearchState(TypedDict):
    """State that flows through research workflows"""
    query: str                    # User's research question
    research_results: str         # Raw research output
    analysis: str                 # Analysis of research
    summary: str                  # Final summary
    quality_score: int            # Quality metric (0-3)
    iteration_count: int          # Track loop iterations
    step_count: int               # Total steps executed
    error: Optional[str]          # Error tracking


def create_initial_state(query: str) -> ResearchState:
    """Create a fresh state for a new workflow run"""
    return {
        "query": query,
        "research_results": "",
        "analysis": "",
        "summary": "",
        "quality_score": 0,
        "iteration_count": 0,
        "step_count": 0,
        "error": None
    }


def get_state_summary(state: ResearchState) -> dict:
    """Get a summary of the current state"""
    return {
        "query": state["query"],
        "steps": state["step_count"],
        "quality": state["quality_score"],
        "has_error": state["error"] is not None
    }
