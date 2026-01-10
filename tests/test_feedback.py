import pytest
from src.feedback import FeedbackCollector


def test_collector_creation():
    """Test collector initialization"""
    collector = FeedbackCollector()

    assert collector.feedback_entries == []


def test_submit_feedback():
    """Test feedback submission"""
    collector = FeedbackCollector()

    entry = collector.submit_feedback("trace-123", 4, "Good response")

    assert len(collector.feedback_entries) == 1
    assert entry["score"] == 4
    assert entry["comment"] == "Good response"


def test_submit_feedback_invalid_score_low():
    """Test rejection of score below 1"""
    collector = FeedbackCollector()

    with pytest.raises(ValueError):
        collector.submit_feedback("trace-123", 0)


def test_submit_feedback_invalid_score_high():
    """Test rejection of score above 5"""
    collector = FeedbackCollector()

    with pytest.raises(ValueError):
        collector.submit_feedback("trace-123", 6)


def test_get_summary_empty():
    """Test summary with no feedback"""
    collector = FeedbackCollector()
    summary = collector.get_summary()

    assert summary["total_feedback"] == 0


def test_get_summary_with_feedback():
    """Test summary with recorded feedback"""
    collector = FeedbackCollector()

    collector.submit_feedback("trace-1", 5)
    collector.submit_feedback("trace-2", 4)
    collector.submit_feedback("trace-3", 3)

    summary = collector.get_summary()

    assert summary["total_feedback"] == 3
    assert summary["avg_score"] == 4.0


def test_get_insights():
    """Test insight generation"""
    collector = FeedbackCollector()

    collector.submit_feedback("trace-1", 5)
    collector.submit_feedback("trace-2", 5)
    collector.submit_feedback("trace-3", 4)

    insights = collector.get_insights()

    assert len(insights) > 0
    assert any("High satisfaction" in i for i in insights)
