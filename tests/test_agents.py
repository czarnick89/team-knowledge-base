from src.agents import create_agent_tools, create_research_agent, run_agent


def test_create_agent_tools_exists():
    """Test tool creation function exists"""
    assert callable(create_agent_tools)


def test_create_research_agent_exists():
    """Test agent creation function exists"""
    assert callable(create_research_agent)


def test_run_agent_exists():
    """Test run_agent function exists"""
    assert callable(run_agent)
