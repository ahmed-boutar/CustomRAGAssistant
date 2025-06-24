from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from ..models import ChatSession, ChatMessage
from ..database import get_db
from ..auth import get_current_user
from pydantic import BaseModel

class CreateSessionRequest(BaseModel):
    title: str

router = APIRouter(prefix="/sessions", tags=["Chat Sessions"])

@router.post("/")
def create_session(request: CreateSessionRequest, db: Session = Depends(get_db), user=Depends(get_current_user)):
    new_session = ChatSession(user_id=user.id, title=request.title)
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    return {"id": new_session.id, "title": new_session.title, "created_at": new_session.created_at}

@router.get("/")
def get_sessions(db: Session = Depends(get_db), user=Depends(get_current_user)):
    sessions = db.query(ChatSession).filter_by(user_id=user.id).order_by(ChatSession.updated_at.desc()).all()
    return [
        {
            "id": s.id,
            "title": s.title,
            "created_at": s.created_at,
            "updated_at": s.updated_at,
        }
        for s in sessions
    ]


@router.get("/{session_id}/messages")
def get_session_messages(
    session_id: int = Path(..., description="ID of the chat session"),
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    # Verify session belongs to user
    session = db.query(ChatSession).filter_by(id=session_id, user_id=user.id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    messages = db.query(ChatMessage).filter_by(session_id=session_id).order_by(ChatMessage.created_at).all()

    return [
        {
            "id": msg.id,
            "role": msg.role,
            "content": msg.content,
            "created_at": msg.created_at
        }
        for msg in messages
    ]

@router.delete("/{session_id}")
def delete_session(
    session_id: int = Path(..., description="ID of the chat session"),
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    session = db.query(ChatSession).filter_by(id=session_id, user_id=user.id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    db.delete(session)
    db.commit()
    return {"message": "Session deleted successfully"}
