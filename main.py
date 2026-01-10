from src.rag import TeamKnowledgeBase
from src.state import create_initial_state, get_state_summary
from src.workflows import run_research_workflow
from src.agents import run_agent

def test_linear_workflow():
    print("=" * 50)
    print("TESTING LINEAR WORKFLOW")
    print("=" * 50)
    
    result = run_research_workflow("benefits of solar energy", "linear")
    summary = get_state_summary(result)
    
    print(f"Steps: {summary['steps']}")
    print(f"Summary: {result['summary'][:200]}...")

def test_conditional_workflow():
    print("\n" + "=" * 50)
    print("TESTING CONDITIONAL WORKFLOW")
    print("=" * 50)
    
    result = run_research_workflow("solar panel costs", "conditional")
    print(f"Steps: {result['step_count']}")
    print(f"Summary: {result['summary'][:200]}...")

def test_agent():
    print("\n" + "=" * 50)
    print("TESTING AGENT")
    print("=" * 50)
    
    result = run_agent("Research renewable energy benefits")
    print(f"Result: {result[:300]}...")

def main():
    print("🚀 Team Knowledge Base RAG System")
    print("=" * 50)
    
    # Initialize
    kb = TeamKnowledgeBase()
    
    # Load and process
    num_docs = kb.load("knowledge_base")
    print(f"📚 Loaded {num_docs} documents")
    
    num_chunks = kb.process()
    print(f"📄 Created {num_chunks} chunks")
    
    num_vectors = kb.index()
    print(f"🔢 Indexed {num_vectors} vectors")
    
    # Test questions
    questions = [
        "What is progressive overload?",
        "How much protein do I need?",
        "What is complete protein?"
    ]
    
    print("\n" + "=" * 50)
    print("Testing RAG Queries")
    print("=" * 50)
    
    for q in questions:
        print(f"\n❓ {q}")
        result = kb.ask(q)
        print(f"🤖 {result['answer'][:200]}...")
        print(f"📚 Sources: {[s['file'] for s in result['sources']]}")

if __name__ == "__main__":
    #main()
    test_linear_workflow()
    test_conditional_workflow()
    test_agent()