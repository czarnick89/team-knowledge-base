from langgraph.graph import StateGraph, END
from src.state import ResearchState, create_initial_state
from src.nodes import (
    research_node, analysis_node, summary_node,
    cost_research_node, expand_research_node,
    decide_after_research
)


def create_linear_workflow():
    """Create a simple linear workflow"""
    workflow = StateGraph(ResearchState)

    workflow.add_node("research", research_node)
    workflow.add_node("analysis", analysis_node)
    workflow.add_node("summary", summary_node)

    workflow.add_edge("research", "analysis")
    workflow.add_edge("analysis", "summary")
    workflow.add_edge("summary", END)

    workflow.set_entry_point("research")

    return workflow.compile()


def create_conditional_workflow():
    """Create a workflow with conditional branching"""
    workflow = StateGraph(ResearchState)

    workflow.add_node("research", research_node)
    workflow.add_node("cost_research", cost_research_node)
    workflow.add_node("expand_research", expand_research_node)
    workflow.add_node("analysis", analysis_node)
    workflow.add_node("summary", summary_node)

    workflow.add_conditional_edges(
        "research",
        decide_after_research,
        {
            "cost_research": "cost_research",
            "expand_research": "expand_research",
            "analysis": "analysis"
        }
    )

    workflow.add_edge("cost_research", "analysis")
    workflow.add_edge("expand_research", "analysis")
    workflow.add_edge("analysis", "summary")
    workflow.add_edge("summary", END)

    workflow.set_entry_point("research")

    return workflow.compile()


def run_research_workflow(query: str, workflow_type: str = "linear") -> dict:
    """Run a research workflow"""
    if workflow_type == "conditional":
        app = create_conditional_workflow()
    else:
        app = create_linear_workflow()

    initial_state = create_initial_state(query)
    final_state = app.invoke(initial_state)

    return final_state
