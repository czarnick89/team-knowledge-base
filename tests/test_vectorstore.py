from unittest.mock import Mock
from src.vectorstore import search, search_with_scores


def test_search_returns_results():
    """Test that search returns expected number of results."""
    # Mock vectorstore
    mock_vectorstore = Mock()
    mock_doc = Mock()
    mock_doc.page_content = "Test content"
    mock_doc.metadata = {"source": "test.txt"}
    mock_vectorstore.similarity_search.return_value = [mock_doc]

    results = search(mock_vectorstore, "test query", k=1)

    assert len(results) == 1
    mock_vectorstore.similarity_search.assert_called_once_with(
        "test query", k=1
    )


def test_search_with_scores_returns_tuples():
    """Test that search_with_scores returns docs with scores."""
    mock_vectorstore = Mock()
    mock_doc = Mock()
    mock_doc.page_content = "Test content"
    mock_vectorstore.similarity_search_with_score.return_value = [
        (mock_doc, 0.5)
    ]

    results = search_with_scores(mock_vectorstore, "test query", k=1)

    assert len(results) == 1
    assert results[0][1] == 0.5
