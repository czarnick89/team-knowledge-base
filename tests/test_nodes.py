from src.nodes import (
    research_node, analysis_node, summary_node,
    cost_research_node, expand_research_node,
    decide_after_research
)


def test_research_node_exists():
    """Test research node is callable"""
    assert callable(research_node)


def test_analysis_node_exists():
    """Test analysis node is callable"""
    assert callable(analysis_node)


def test_summary_node_exists():
    """Test summary node is callable"""
    assert callable(summary_node)


def test_cost_research_node_exists():
    """Test cost research node is callable"""
    assert callable(cost_research_node)


def test_expand_research_node_exists():
    """Test expand research node is callable"""
    assert callable(expand_research_node)


def test_decide_after_research_cost():
    """Test decision function with cost keywords"""
    state = {"research_results": "This is expensive and costly"}
    result = decide_after_research(state)
    assert result == "cost_research"


def test_decide_after_research_short():
    """Test decision function with short content"""
    state = {"research_results": "Brief content"}
    result = decide_after_research(state)
    assert result == "expand_research"


def test_decide_after_research_sufficient():
    """Test decision function with sufficient content"""
    state = {"research_results": "A" * 400}
    result = decide_after_research(state)
    assert result == "analysis"
