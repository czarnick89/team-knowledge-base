from src.state import ResearchState
from src.client import create_client, create_llm


def get_llm():
    """Get LLM instance"""
    client = create_client()
    return create_llm(client)


def research_node(state: ResearchState) -> ResearchState:
    """Research node - gathers information"""
    print(f"🔍 Research Node: Investigating '{state['query']}'")

    llm = get_llm()
    prompt = f"Research and provide key information about: {state['query']}"

    try:
        response = llm.invoke(prompt)
        research_results = response.content
        error = None
    except Exception as e:
        research_results = ""
        error = f"Research failed: {str(e)}"

    return {
        **state,
        "research_results": research_results,
        "step_count": state["step_count"] + 1,
        "error": error
    }


def analysis_node(state: ResearchState) -> ResearchState:
    """Analysis node - analyzes research results"""
    print("🧠 Analysis Node: Analyzing research")

    llm = get_llm()
    prompt = f"Analyze this research and provide insights:\n{state['research_results']}"

    try:
        response = llm.invoke(prompt)
        analysis = response.content
        error = None
    except Exception as e:
        analysis = ""
        error = f"Analysis failed: {str(e)}"

    return {
        **state,
        "analysis": analysis,
        "step_count": state["step_count"] + 1,
        "error": error
    }


def summary_node(state: ResearchState) -> ResearchState:
    """Summary node - creates final summary"""
    print("📝 Summary Node: Creating summary")

    llm = get_llm()
    prompt = f"Create a summary for {state['query']}:\n{state['analysis']}"

    try:
        response = llm.invoke(prompt)
        summary = response.content
        error = None
    except Exception as e:
        summary = ""
        error = f"Summary failed: {str(e)}"

    return {
        **state,
        "summary": summary,
        "step_count": state["step_count"] + 1,
        "error": error
    }


def cost_research_node(state: ResearchState) -> ResearchState:
    """Research cost-related solutions"""
    print("💰 Cost Research Node: Finding solutions")

    llm = get_llm()
    prompt = f"Research cost solutions for: {state['research_results'][:500]}"

    try:
        response = llm.invoke(prompt)
        enhanced = state['research_results'] + f"\n\nCost Solutions:\n{response.content}"
    except Exception:
        enhanced = state['research_results']

    return {
        **state,
        "research_results": enhanced,
        "step_count": state["step_count"] + 1
    }


def expand_research_node(state: ResearchState) -> ResearchState:
    """Expand brief research"""
    print("📚 Expand Research Node: Gathering more info")

    llm = get_llm()
    prompt = f"Expand on this research: {state['research_results']}"

    try:
        response = llm.invoke(prompt)
        enhanced = state['research_results'] + f"\n\nExpanded:\n{response.content}"
    except Exception:
        enhanced = state['research_results']

    return {
        **state,
        "research_results": enhanced,
        "step_count": state["step_count"] + 1
    }


# Decision functions
def decide_after_research(state: ResearchState) -> str:
    """Decide next step based on research"""
    research = state.get("research_results", "").lower()

    if any(word in research for word in ["expensive", "costly", "high cost"]):
        print("💡 Decision: Cost concerns -> cost_research")
        return "cost_research"
    elif len(research) < 300:
        print("💡 Decision: Brief results -> expand_research")
        return "expand_research"
    else:
        print("💡 Decision: Sufficient -> analysis")
        return "analysis"
