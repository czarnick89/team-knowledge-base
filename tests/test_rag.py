from unittest.mock import patch


def test_team_knowledge_base_init():
    """Test TeamKnowledgeBase initialization."""
    with patch('src.rag.boto3.client'):
        with patch('src.rag.ChatBedrock'):
            from src.rag import TeamKnowledgeBase
            kb = TeamKnowledgeBase()
            assert kb.documents == []
            assert kb.chunks == []


def test_ask_without_index():
    """Test asking without initialized index."""
    with patch('src.rag.boto3.client'):
        with patch('src.rag.ChatBedrock'):
            from src.rag import TeamKnowledgeBase
            kb = TeamKnowledgeBase()
            result = kb.ask("test question")
            assert "not initialized" in result["answer"]
            assert result["sources"] == []
