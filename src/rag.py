from langchain_aws import ChatBedrock
from src.loader import load_knowledge_base, create_chunks
from src.vectorstore import (
    create_embeddings, create_vector_store,
    save_vector_store, load_vector_store, search
)
import boto3


class TeamKnowledgeBase:
    """Complete RAG system for team knowledge base."""

    def __init__(self):
        self.documents = []
        self.chunks = []
        self.vectorstore = None
        self.llm = None
        self._init_llm()

    def _init_llm(self):
        """Initialize the LLM."""
        client = boto3.client(
            service_name="bedrock-runtime",
            region_name="us-east-1"
        )
        self.llm = ChatBedrock(
            model_id="us.amazon.nova-lite-v1:0",
            client=client,
            model_kwargs={"max_tokens_to_sample": 1500, "temperature": 0.7}
        )

    def load(self, directory="knowledge_base"):
        """Load documents from directory."""
        self.documents = load_knowledge_base(directory)
        return len(self.documents)

    def process(self, chunk_size=500, chunk_overlap=50):
        """Process documents into chunks."""
        self.chunks = create_chunks(
            self.documents,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        return len(self.chunks)

    def index(self):
        """Create vector store index."""
        embeddings = create_embeddings()
        self.vectorstore = create_vector_store(self.chunks, embeddings)
        return self.vectorstore.index.ntotal

    def save(self, path="vector_index"):
        """Save vector store to disk."""
        if self.vectorstore:
            save_vector_store(self.vectorstore, path)

    def load_index(self, path="vector_index"):
        """Load existing vector store."""
        embeddings = create_embeddings()
        self.vectorstore = load_vector_store(path, embeddings)

    def ask(self, question, k=3):
        """Ask a question and get an answer with sources."""
        if not self.vectorstore:
            return {
                "answer": "Knowledge base not initialized.",
                "sources": []
            }

        # Retrieve relevant chunks
        relevant_docs = search(self.vectorstore, question, k=k)

        if not relevant_docs:
            return {
                "answer": (
                    "No relevant information found in the knowledge base."
                ),
                "sources": []
            }

        # Build context
        context = "\n\n".join([doc.page_content for doc in relevant_docs])

        # Create prompt
        prompt = (
            "Based on the following context from our team knowledge "
            "base, please answer the question. Only use information "
            "from the context provided.\n\n"
            f"Context:\n{context}\n\n"
            f"Question: {question}\n\nAnswer:"
        )

        # Generate answer
        response = self.llm.invoke(prompt)

        # Extract sources
        sources = []
        for doc in relevant_docs:
            sources.append({
                "file": doc.metadata.get('source', 'Unknown'),
                "author": doc.metadata.get('author', 'Unknown'),
                "topic": doc.metadata.get('topic', 'Unknown')
            })

        return {
            "question": question,
            "answer": response.content,
            "sources": sources
        }
