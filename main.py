from src.rag import TeamKnowledgeBase
from src.state import create_initial_state, get_state_summary
from src.workflows import run_research_workflow
from src.agents import run_agent
from src.tracing import create_traced_state, get_trace_summary
from src.performance import PerformanceMonitor
from src.errors import ErrorTracker
from src.feedback import FeedbackCollector

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

def test_tracing():
    print("=" * 50)
    print("TESTING TRACING")
    print("=" * 50)
    
    state = create_traced_state("test query")
    summary = get_trace_summary(state)
    
    print(f"Trace ID: {summary['trace_id'][:8]}...")
    print(f"Query: {summary['query']}")

def test_performance():
    print("\n" + "=" * 50)
    print("TESTING PERFORMANCE MONITOR")
    print("=" * 50)
    
    monitor = PerformanceMonitor()
    
    # Simulate runs
    for i in range(3):
        state = {
            "query": f"test {i}",
            "execution_time": 3.0 + i,
            "step_count": 3,
            "token_estimate": 500,
            "cost_estimate": 0.001,
            "error": None,
            "trace_metadata": {"steps": []}
        }
        monitor.record_run(state)
    
    monitor.print_report()

def test_errors():
    print("\n" + "=" * 50)
    print("TESTING ERROR TRACKER")
    print("=" * 50)
    
    tracker = ErrorTracker()
    
    tracker.log_error("Connection timeout after 30 seconds")
    tracker.log_error("Rate limit exceeded")
    tracker.log_error("Token limit exceeded: 4096 max")
    
    tracker.print_report()

def test_feedback():
    print("\n" + "=" * 50)
    print("TESTING FEEDBACK COLLECTOR")
    print("=" * 50)
    
    collector = FeedbackCollector()
    
    collector.submit_feedback("trace-1", 5, "Excellent!")
    collector.submit_feedback("trace-2", 4, "Good")
    collector.submit_feedback("trace-3", 3, "Average")
    collector.submit_feedback("trace-4", 2, "Needs work")
    
    collector.print_report()

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

    # test_linear_workflow()
    # test_conditional_workflow()
    # test_agent()

    test_tracing()
    test_performance()
    test_errors()
    test_feedback()
    print("\n✅ All monitoring tests completed!")