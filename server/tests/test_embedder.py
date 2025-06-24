# tests/test_embedder.py
import pytest
from unittest.mock import patch, MagicMock
from botocore.exceptions import BotoCoreError, ClientError

from app.services.embedder import get_embeddings


class TestGetEmbeddings:
    """Test cases for the get_embeddings function."""

    @patch('app.services.embedder.call_embedding_model')
    def test_get_embeddings_single_chunk(self, mock_call_embedding_model):
        """Test get_embeddings with a single text chunk."""
        # Arrange
        chunks = ["This is a test document"]
        expected_embedding = [0.1, 0.2, 0.3, 0.4, 0.5]
        mock_call_embedding_model.return_value = expected_embedding
        
        # Act
        result = get_embeddings(chunks)
        
        # Assert
        assert len(result) == 1
        assert result[0] == expected_embedding
        mock_call_embedding_model.assert_called_once_with("This is a test document")

    @patch('app.services.embedder.call_embedding_model')
    def test_get_embeddings_multiple_chunks(self, mock_call_embedding_model):
        """Test get_embeddings with multiple text chunks."""
        # Arrange
        chunks = [
            "First document chunk",
            "Second document chunk", 
            "Third document chunk"
        ]
        expected_embeddings = [
            [0.1, 0.2, 0.3],
            [0.4, 0.5, 0.6],
            [0.7, 0.8, 0.9]
        ]
        mock_call_embedding_model.side_effect = expected_embeddings
        
        # Act
        result = get_embeddings(chunks)
        
        # Assert
        assert len(result) == 3
        assert result == expected_embeddings
        assert mock_call_embedding_model.call_count == 3
        
        # Verify each chunk was called correctly
        expected_calls = [
            (("First document chunk",),),
            (("Second document chunk",),),
            (("Third document chunk",),)
        ]
        actual_calls = [call.args for call in mock_call_embedding_model.call_args_list]
        assert actual_calls == [call[0] for call in expected_calls]

    @patch('app.services.embedder.call_embedding_model')
    def test_get_embeddings_empty_list(self, mock_call_embedding_model):
        """Test get_embeddings with an empty list of chunks."""
        # Arrange
        chunks = []
        
        # Act
        result = get_embeddings(chunks)
        
        # Assert
        assert result == []
        mock_call_embedding_model.assert_not_called()

    @patch('app.services.embedder.call_embedding_model')
    def test_get_embeddings_empty_string_chunk(self, mock_call_embedding_model):
        """Test get_embeddings with empty string chunks."""
        # Arrange
        chunks = ["", "non-empty chunk", ""]
        expected_embeddings = [
            [0.0, 0.0, 0.0],  # Empty string embedding
            [0.1, 0.2, 0.3],  # Non-empty chunk embedding
            [0.0, 0.0, 0.0]   # Another empty string embedding
        ]
        mock_call_embedding_model.side_effect = expected_embeddings
        
        # Act
        result = get_embeddings(chunks)
        
        # Assert
        assert len(result) == 3
        assert result == expected_embeddings
        assert mock_call_embedding_model.call_count == 3

    @patch('app.services.embedder.call_embedding_model')
    def test_get_embeddings_with_special_characters(self, mock_call_embedding_model):
        """Test get_embeddings with chunks containing special characters."""
        # Arrange
        chunks = [
            "Text with émojis 😀🎉",
            "Special chars: @#$%^&*()",
            "Unicode: 中文测试",
            "Newlines\nand\ttabs"
        ]
        expected_embeddings = [
            [0.1, 0.2],
            [0.3, 0.4], 
            [0.5, 0.6],
            [0.7, 0.8]
        ]
        mock_call_embedding_model.side_effect = expected_embeddings
        
        # Act
        result = get_embeddings(chunks)
        
        # Assert
        assert len(result) == 4
        assert result == expected_embeddings
        assert mock_call_embedding_model.call_count == 4

    @patch('app.services.embedder.call_embedding_model')
    def test_get_embeddings_with_long_text(self, mock_call_embedding_model):
        """Test get_embeddings with very long text chunks."""
        # Arrange
        long_text = "This is a very long text. " * 1000  # Create a long string
        chunks = [long_text]
        expected_embedding = [0.1] * 1536  # Common embedding dimension
        mock_call_embedding_model.return_value = expected_embedding
        
        # Act
        result = get_embeddings(chunks)
        
        # Assert
        assert len(result) == 1
        assert result[0] == expected_embedding
        mock_call_embedding_model.assert_called_once_with(long_text)

    @patch('app.services.embedder.call_embedding_model')
    def test_get_embeddings_runtime_error_propagation(self, mock_call_embedding_model):
        """Test that RuntimeError from call_embedding_model is properly propagated."""
        # Arrange
        chunks = ["test chunk"]
        mock_call_embedding_model.side_effect = RuntimeError("Failed to get embedding: Network error")
        
        # Act & Assert
        with pytest.raises(RuntimeError, match="Failed to get embedding: Network error"):
            get_embeddings(chunks)
        
        mock_call_embedding_model.assert_called_once_with("test chunk")

    @patch('app.services.embedder.call_embedding_model')
    def test_get_embeddings_partial_failure(self, mock_call_embedding_model):
        """Test behavior when one chunk fails but others succeed."""
        # Arrange
        chunks = ["chunk1", "chunk2", "chunk3"]
        mock_call_embedding_model.side_effect = [
            [0.1, 0.2],  # First chunk succeeds
            RuntimeError("Network error"),  # Second chunk fails
            [0.5, 0.6]   # This won't be reached due to failure
        ]
        
        # Act & Assert
        with pytest.raises(RuntimeError, match="Network error"):
            get_embeddings(chunks)
        
        # Only the first chunk should have been processed
        assert mock_call_embedding_model.call_count == 2

    @patch('app.services.embedder.call_embedding_model')
    def test_get_embeddings_different_embedding_dimensions(self, mock_call_embedding_model):
        """Test get_embeddings with embeddings of different dimensions."""
        # Arrange
        chunks = ["short text", "medium length text here", "much longer text content here for testing"]
        expected_embeddings = [
            [0.1, 0.2, 0.3],           # 3D embedding
            [0.4, 0.5, 0.6, 0.7],      # 4D embedding  
            [0.8, 0.9, 1.0, 1.1, 1.2] # 5D embedding
        ]
        mock_call_embedding_model.side_effect = expected_embeddings
        
        # Act
        result = get_embeddings(chunks)
        
        # Assert
        assert len(result) == 3
        assert len(result[0]) == 3
        assert len(result[1]) == 4
        assert len(result[2]) == 5
        assert result == expected_embeddings

    @patch('app.services.embedder.call_embedding_model')
    def test_get_embeddings_numeric_values_in_text(self, mock_call_embedding_model):
        """Test get_embeddings with chunks containing numeric values."""
        # Arrange
        chunks = [
            "Price: $19.99",
            "Temperature: 25.5°C", 
            "ID: 12345",
            "Percentage: 85.7%"
        ]
        expected_embeddings = [
            [0.1, 0.2],
            [0.3, 0.4],
            [0.5, 0.6], 
            [0.7, 0.8]
        ]
        mock_call_embedding_model.side_effect = expected_embeddings
        
        # Act
        result = get_embeddings(chunks)
        
        # Assert
        assert len(result) == 4
        assert result == expected_embeddings
        assert mock_call_embedding_model.call_count == 4

    @patch('app.services.embedder.call_embedding_model')
    def test_get_embeddings_whitespace_only_chunks(self, mock_call_embedding_model):
        """Test get_embeddings with chunks containing only whitespace."""
        # Arrange
        chunks = ["   ", "\t\t", "\n\n", "  \t\n  "]
        expected_embeddings = [
            [0.0, 0.0],
            [0.0, 0.0],
            [0.0, 0.0],
            [0.0, 0.0]
        ]
        mock_call_embedding_model.side_effect = expected_embeddings
        
        # Act
        result = get_embeddings(chunks)
        
        # Assert
        assert len(result) == 4
        assert result == expected_embeddings
        assert mock_call_embedding_model.call_count == 4

    @patch('app.services.embedder.call_embedding_model')
    def test_get_embeddings_preserves_order(self, mock_call_embedding_model):
        """Test that get_embeddings preserves the order of input chunks."""
        # Arrange
        chunks = [f"Chunk {i}" for i in range(10)]
        expected_embeddings = [[float(i), float(i+1)] for i in range(10)]
        mock_call_embedding_model.side_effect = expected_embeddings
        
        # Act
        result = get_embeddings(chunks)
        
        # Assert
        assert len(result) == 10
        for i, embedding in enumerate(result):
            assert embedding == [float(i), float(i+1)]
        
        # Verify chunks were called in correct order
        for i, call in enumerate(mock_call_embedding_model.call_args_list):
            assert call[0][0] == f"Chunk {i}"