from src.workflows import (
    create_linear_workflow,
    create_conditional_workflow,
    run_research_workflow
)


def test_create_linear_workflow():
    """Test linear workflow creation"""
    workflow = create_linear_workflow()
    assert workflow is not None


def test_create_conditional_workflow():
    """Test conditional workflow creation"""
    workflow = create_conditional_workflow()
    assert workflow is not None


def test_run_research_workflow_exists():
    """Test run function exists"""
    assert callable(run_research_workflow)
