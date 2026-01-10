from src.errors import ErrorTracker


def test_tracker_creation():
    """Test tracker initialization"""
    tracker = ErrorTracker()

    assert tracker.errors == []
    assert tracker.error_counts == {}


def test_classify_timeout():
    """Test timeout error classification"""
    tracker = ErrorTracker()

    result = tracker.classify_error("Connection timeout after 30 seconds")
    assert result == "timeout"


def test_classify_rate_limit():
    """Test rate limit error classification"""
    tracker = ErrorTracker()

    result = tracker.classify_error("Rate limit exceeded")
    assert result == "rate_limit"


def test_classify_token_limit():
    """Test token limit error classification"""
    tracker = ErrorTracker()

    result = tracker.classify_error("Token limit exceeded: 4096 max")
    assert result == "token_limit"


def test_classify_unknown():
    """Test unknown error classification"""
    tracker = ErrorTracker()

    result = tracker.classify_error("Something weird happened")
    assert result == "unknown"


def test_log_error():
    """Test error logging"""
    tracker = ErrorTracker()

    tracker.log_error("Connection timeout", {"step": "research"})

    assert len(tracker.errors) == 1
    assert tracker.error_counts["timeout"] == 1


def test_get_solutions():
    """Test solution retrieval"""
    tracker = ErrorTracker()

    tracker.log_error("Rate limit exceeded")
    solutions = tracker.get_solutions()

    assert "rate_limit" in solutions
    assert len(solutions["rate_limit"]) > 0
