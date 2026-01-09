import os
from pathlib import Path
from langchain_community.document_loaders import TextLoader
from langchain.schema import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

def parse_metadata(content):
    """Parse metadata header from document content."""
    metadata = {}
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            header = parts[1].strip()
            for line in header.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    metadata[key.strip().lower()] = value.strip()
            return metadata, parts[2].strip()
    return metadata, content

def load_knowledge_base(directory="knowledge_base"):
    """Load all documents from knowledge base directory."""
    documents = []
    doc_path = Path(directory)
    
    for file in doc_path.glob("*.txt"):
        loader = TextLoader(str(file))
        docs = loader.load()
        
        for doc in docs:
            metadata, content = parse_metadata(doc.page_content)
            metadata['source'] = file.name
            metadata['filepath'] = str(file)
            
            documents.append(Document(
                page_content=content,
                metadata=metadata
            ))
    
    return documents

def get_document_stats(documents):
    """Get statistics about loaded documents."""
    authors = set(doc.metadata.get('author', 'Unknown') for doc in documents)
    topics = set(doc.metadata.get('topic', 'Unknown') for doc in documents)
    
    return {
        "total_documents": len(documents),
        "unique_authors": len(authors),
        "authors": list(authors),
        "topics": list(topics)
    }

def create_chunks(documents, chunk_size=500, chunk_overlap=50):
    """Split documents into chunks while preserving metadata."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""]
    )
    
    chunks = text_splitter.split_documents(documents)
    return chunks