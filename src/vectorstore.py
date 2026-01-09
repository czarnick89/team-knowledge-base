from langchain_aws import BedrockEmbeddings
from langchain_community.vectorstores import FAISS
import boto3


def create_embeddings():
    """Create BedrockEmbeddings instance."""
    client = boto3.client(
        service_name="bedrock-runtime",
        region_name="us-east-1"
    )
    return BedrockEmbeddings(
        client=client,
        model_id="amazon.titan-embed-text-v2:0"
    )


def create_vector_store(chunks, embeddings=None):
    """Create FAISS vector store from chunks."""
    if embeddings is None:
        embeddings = create_embeddings()

    vectorstore = FAISS.from_documents(chunks, embeddings)
    return vectorstore


def save_vector_store(vectorstore, path="vector_index"):
    """Save vector store to disk."""
    vectorstore.save_local(path)


def load_vector_store(path="vector_index", embeddings=None):
    """Load vector store from disk."""
    if embeddings is None:
        embeddings = create_embeddings()

    return FAISS.load_local(
        path,
        embeddings,
        allow_dangerous_deserialization=True
    )


def search(vectorstore, query, k=3):
    """Search for relevant documents."""
    return vectorstore.similarity_search(query, k=k)


def search_with_scores(vectorstore, query, k=3):
    """Search with similarity scores."""
    return vectorstore.similarity_search_with_score(query, k=k)
