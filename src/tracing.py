import time
import uuid
from typing import TypedDict, Optional


class TracedState(TypedDict):
    """State with built-in tracing metadata"""
    query: str                    # User's question
    result: str                   # Final result
    execution_time: float         # Total execution time
    step_count: int               # Steps executed
    token_estimate: int           # Estimated tokens used
    cost_estimate: float          # Estimated cost
    error: Optional[str]          # Error message if any
    trace_metadata: dict          # Custom trace metadata


def create_traced_state(query: str) -> TracedState:
    """Create initial state with tracing metadata"""
    return {
        "query": query,
        "result": "",
        "execution_time": 0.0,
        "step_count": 0,
        "token_estimate": 0,
        "cost_estimate": 0.0,
        "error": None,
        "trace_metadata": {
            "trace_id": generate_trace_id(),
            "start_time": time.time(),
            "steps": []
        }
    }


def generate_trace_id() -> str:
    """Generate a unique trace ID"""
    return str(uuid.uuid4())


def estimate_tokens(text: str) -> int:
    """Estimate token count (rough approximation)"""
    return len(text) // 4


def estimate_cost(tokens: int, rate: float = 0.000002) -> float:
    """Estimate cost based on token count"""
    return tokens * rate


def get_trace_summary(state: TracedState) -> dict:
    """Get a summary of the trace"""
    return {
        "trace_id": state["trace_metadata"].get("trace_id", "unknown"),
        "query": state["query"],
        "execution_time": state["execution_time"],
        "steps": state["step_count"],
        "tokens": state["token_estimate"],
        "cost": state["cost_estimate"],
        "has_error": state["error"] is not None
    }
