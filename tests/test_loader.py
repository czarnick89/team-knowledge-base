import pytest
import os
import tempfile
from src.loader import parse_metadata, load_knowledge_base, create_chunks

@pytest.fixture
def sample_doc_content():
    return """---
Author: Test Author
Date: 2024-01-15
Topic: Test Topic
Summary: A test document.
---

This is the actual content of the test document.
It has multiple sentences and paragraphs.

This is another paragraph with more content.
"""

@pytest.fixture
def temp_knowledge_base(sample_doc_content):
    """Create temporary knowledge base for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create test document
        doc_path = os.path.join(tmpdir, "test_doc.txt")
        with open(doc_path, "w") as f:
            f.write(sample_doc_content)
        yield tmpdir

def test_parse_metadata_extracts_fields(sample_doc_content):
    """Test that metadata is correctly parsed."""
    metadata, content = parse_metadata(sample_doc_content)
    
    assert metadata['author'] == 'Test Author'
    assert metadata['topic'] == 'Test Topic'
    assert 'actual content' in content

def test_parse_metadata_handles_no_header():
    """Test parsing document without metadata header."""
    content = "Just plain content without header."
    metadata, result = parse_metadata(content)
    
    assert metadata == {}
    assert result == content

def test_load_knowledge_base(temp_knowledge_base):
    """Test loading documents from directory."""
    documents = load_knowledge_base(temp_knowledge_base)
    
    assert len(documents) == 1
    assert documents[0].metadata['author'] == 'Test Author'

def test_create_chunks(temp_knowledge_base):
    """Test document chunking."""
    documents = load_knowledge_base(temp_knowledge_base)
    chunks = create_chunks(documents, chunk_size=100, chunk_overlap=20)
    
    assert len(chunks) >= 1
    assert all('source' in chunk.metadata for chunk in chunks)