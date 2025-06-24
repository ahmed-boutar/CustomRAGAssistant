# tests/test_query_handler.py
import pytest
from unittest.mock import MagicMock, patch
from app.services import query_handler
from app.models import ChatSession, ChatMessage
from sqlalchemy.orm import Session

print("RUNNING QUERY HANDLER TESTS")
def test_build_claude_prompt():
    system_prompt = "You are a helpful assistant."
    chat_history = [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi, how can I help?"},
    ]
    user_input = "Tell me a joke"
    
    result = query_handler.build_claude_prompt(system_prompt, chat_history, user_input)
    
    expected = (
        "You are a helpful assistant.\n"
        "User: Hello\n"
        "Assistant: Hi, how can I help?\n"
        "User: Tell me a joke"
    )
    
    assert result == expected


def test_build_titan_prompt():
    system_prompt = "System Start"
    chat_history = [
        {"role": "user", "content": "Ping"},
        {"role": "assistant", "content": "Pong"},
        {"role": "user", "content": None},  # Should be ignored
    ]
    user_input = "What's the weather?"
    
    result = query_handler.build_titan_prompt(system_prompt, chat_history, user_input)
    
    expected = (
        "System Start\n"
        "User: Ping\n"
        "Assistant: Pong\n"
        "User: What's the weather?\n"
        "Assistant:"
    )
    assert result == expected


# @patch("app.services.query_handler.call_bedrock_model")
# @patch("app.services.query_handler.get_embeddings")
# @patch("app.services.query_handler.query_similar_chunks")
# def test_run_chat_with_rag(
#     mock_query_similar_chunks, mock_get_embeddings, mock_call_model
# ):
#     # Setup
#     db = MagicMock(spec=Session)
    
#     # Mock ChatSession and ChatMessage retrieval
#     mock_session = ChatSession(id=1, user_id=1)
#     db.query.return_value.filter_by.return_value.first.return_value = mock_session

#     mock_messages = [
#         ChatMessage(role="user", content="Hello", session_id=1),
#         ChatMessage(role="assistant", content="Hi!", session_id=1),
#         ChatMessage(role="user", content=" ", session_id=1),  # Should be ignored
#     ]
#     db.query.return_value.filter_by.return_value.order_by.return_value.all.return_value = mock_messages

#     # Mock vector DB + embeddings
#     mock_get_embeddings.return_value = [[0.1, 0.2, 0.3]]
#     mock_query_similar_chunks.return_value = [
#         {"metadata": {"text": "Relevant context 1"}},
#         {"metadata": {"text": "Relevant context 2"}},
#     ]

#     # Mock model output
#     mock_call_model.return_value = "This is a response."

#     response = query_handler.run_chat(
#         db=db,
#         user_id=1,
#         session_id=1,
#         model="claude",
#         system_prompt="You are a test bot.",
#         user_input="Tell me something.",
#         enable_rag=True,
#     )

#     assert "This is a response." == response
#     mock_call_model.assert_called_once()


# @patch("app.services.query_handler.call_bedrock_model", return_value="Reply")
# def test_run_chat_unsupported_model(mock_call):
#     db = MagicMock(spec=Session)
#     mock_session = ChatSession(id=1, user_id=1)
#     db.query.return_value.filter_by.return_value.first.return_value = mock_session
#     db.query.return_value.filter_by.return_value.order_by.return_value.all.return_value = []

#     with pytest.raises(ValueError, match="Unsupported model"):
#         query_handler.run_chat(
#             db=db,
#             user_id=1,
#             session_id=1,
#             model="gpt4",
#             system_prompt="Bot start.",
#             user_input="Hi",
#         )


def test_run_chat_no_session():
    db = MagicMock(spec=Session)
    db.query.return_value.filter_by.return_value.first.return_value = None

    with pytest.raises(RuntimeError, match="Session not found."):
        query_handler.run_chat(
            db=db,
            user_id=42,
            session_id=999,
            model="claude",
            system_prompt="System here.",
            user_input="Yo!",
        )
