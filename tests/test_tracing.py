from src.tracing import (
    create_traced_state, generate_trace_id,
    estimate_tokens, estimate_cost, get_trace_summary
)


def test_create_traced_state():
    """Test traced state creation"""
    state = create_traced_state("test query")

    assert state["query"] == "test query"
    assert state["result"] == ""
    assert state["execution_time"] == 0.0
    assert state["step_count"] == 0
    assert state["token_estimate"] == 0
    assert state["cost_estimate"] == 0.0
    assert state["error"] is None
    assert "trace_metadata" in state


def test_traced_state_has_metadata():
    """Test that traced state includes metadata"""
    state = create_traced_state("test")

    assert "trace_id" in state["trace_metadata"]
    assert "start_time" in state["trace_metadata"]
    assert "steps" in state["trace_metadata"]


def test_generate_trace_id():
    """Test trace ID generation"""
    id1 = generate_trace_id()
    id2 = generate_trace_id()

    assert isinstance(id1, str)
    assert len(id1) > 0
    assert id1 != id2  # IDs should be unique


def test_estimate_tokens():
    """Test token estimation"""
    text = "This is a test string with some words"
    tokens = estimate_tokens(text)

    assert isinstance(tokens, int)
    assert tokens > 0


def test_estimate_cost():
    """Test cost estimation"""
    cost = estimate_cost(1000)

    assert isinstance(cost, float)
    assert cost > 0


def test_get_trace_summary():
    """Test trace summary function"""
    state = create_traced_state("test query")
    state["execution_time"] = 5.0
    state["step_count"] = 3

    summary = get_trace_summary(state)

    assert summary["query"] == "test query"
    assert summary["execution_time"] == 5.0
    assert summary["steps"] == 3
    assert summary["has_error"] is False
