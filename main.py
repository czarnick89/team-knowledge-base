from src.rag import TeamKnowledgeBase

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
    main()