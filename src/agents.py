from langchain_core.tools import Tool
from langchain.agents import create_agent
from src.client import create_client, create_llm


def get_llm():
    """Get LLM instance"""
    client = create_client()
    return create_llm(client)


def create_agent_tools():
    """Create tools for the agent"""
    llm = get_llm()

    def research_tool(topic: str) -> str:
        """Research a topic"""
        print(f"🔍 Tool: Researching '{topic}'")
        try:
            response = llm.invoke(f"Research: {topic}")
            return f"Research: {response.content}"
        except Exception as e:
            return f"Error: {str(e)}"

    def analyze_tool(data: str) -> str:
        """Analyze data"""
        print("📊 Tool: Analyzing")
        try:
            response = llm.invoke(f"Analyze: {data[:500]}")
            return f"Analysis: {response.content}"
        except Exception as e:
            return f"Error: {str(e)}"

    def summarize_tool(content: str) -> str:
        """Summarize content"""
        print("📝 Tool: Summarizing")
        try:
            response = llm.invoke(f"Summarize: {content[:500]}")
            return f"Summary: {response.content}"
        except Exception as e:
            return f"Error: {str(e)}"

    def fact_check_tool(claim: str) -> str:
        """Fact-check a claim"""
        print("✅ Tool: Fact-checking")
        try:
            response = llm.invoke(f"Fact-check: {claim}")
            return f"Fact Check: {response.content}"
        except Exception as e:
            return f"Error: {str(e)}"

    tools = [
        Tool(name="Research", description="Research any topic", func=research_tool),
        Tool(name="Analyze", description="Analyze data for insights", func=analyze_tool),
        Tool(name="Summarize", description="Summarize content", func=summarize_tool),
        Tool(name="FactCheck", description="Verify claim accuracy", func=fact_check_tool),
    ]

    return tools


def create_research_agent():
    """Create a flexible research agent"""
    print("🤖 Building research agent...")

    llm = get_llm()
    tools = create_agent_tools()

    # Create agent using LangGraph
    agent = create_agent(llm, tools)

    print("✅ Research agent created")
    return agent


def run_agent(query: str) -> str:
    """Run the research agent"""
    agent = create_research_agent()
    try:
        result = agent.invoke({"messages": [("user", query)]})
        # Extract the last message content
        output = result['messages'][-1].content
        return output
    except Exception as e:
        return f"Agent error: {str(e)}"


def get_all_tools():
    """Return list of all tools"""
    return create_agent_tools()
