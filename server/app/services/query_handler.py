# app/services/query_handler.py
from app.services.bedrock_client import call_bedrock_model
from ..models import ChatSession, ChatMessage
from ..services.pinecone_client import query_similar_chunks
from ..services.embedder import get_embeddings
from ..database import get_db
from sqlalchemy.orm import Session

def build_claude_prompt(system_prompt: str, chat_history: list, user_input: str) -> str:
    """
    Claude on Bedrock now uses structured messages format.
    We'll convert everything into a single user message.
    TODO: Modify to support chat history
    """
    # Combine history into a flat prompt for now (or modify to support multiple messages)
    history_text = ""
    for turn in chat_history:
        role = turn["role"]
        content = turn["content"]
        prefix = "User" if role == "user" else "Assistant"
        history_text += f"{prefix}: {content}\n"

    full_text = f"{system_prompt}\n{history_text}User: {user_input}"
    return full_text


def build_titan_prompt(system_prompt: str, chat_history: list, user_input: str) -> str:
    """
    Titan uses a flat text prompt.
    """
    history_parts = []
    for msg in chat_history:
        if msg.get('content'):  # Only add if content exists
            history_parts.append(f"{msg['role'].capitalize()}: {msg['content']}")
    
    history = "\n".join(history_parts)
    return f"{system_prompt}\n{history}\nUser: {user_input}\nAssistant:"

def run_chat(
    db: Session,
    user_id: int,
    session_id: int,
    model: str,
    system_prompt: str,
    user_input: str,
    enable_rag: bool = False,
):
    try:
        session = db.query(ChatSession).filter_by(id=session_id, user_id=user_id).first()
        if not session:
            raise ValueError("Session not found.")

        # Add null checks for content field
        chat_history = []
        messages = (db.query(ChatMessage)
                    .filter_by(session_id=session_id)
                    .order_by(ChatMessage.created_at)
                    .all())
        
        for msg in messages:
            # Skip messages with null/empty content
            if msg.content is not None and msg.content.strip():
                chat_history.append({
                    "role": msg.role, 
                    "content": msg.content
                })

        # Save user message
        user_msg = ChatMessage(session_id=session_id, role="user", content=user_input)
        db.add(user_msg)
        db.commit()

        context = ""
        if enable_rag:
            from .embedder import get_embeddings
            from .pinecone_client import query_similar_chunks

            query_embedding = get_embeddings([user_input])[0]
            matches = query_similar_chunks(user_id, query_embedding, top_k=4)
            context_chunks = [match["metadata"]["text"] for match in matches]
            context = "\n".join(context_chunks)

        final_prompt = f"{system_prompt}\n\nContext:\n{context}" if context else system_prompt

        if model == "claude":
            prompt = build_claude_prompt(final_prompt, chat_history, user_input)
        elif model == "titan":
            prompt = build_titan_prompt(final_prompt, chat_history, user_input)
        else:
            raise ValueError("Unsupported model")

        from .bedrock_client import call_bedrock_model
        response = call_bedrock_model(model, prompt)

        # Save assistant reply
        assistant_msg = ChatMessage(session_id=session_id, role="assistant", content=response)
        db.add(assistant_msg)
        db.commit()

        return response
    
    except Exception as e:
        print(f"Error during chat run: {e}")
        raise RuntimeError(f"Error during chat run: {str(e)}") from e



